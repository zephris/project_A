"""Saved rigid-case tests with conservative body/finger gauges, not vendor CAD."""
from pathlib import Path
import sys,json,itertools
from cadgen import read_step,read_scene,build123d as bd
from cadgen.geometry import overlap_volume
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from common import *

# Restrict case geometry to a native exact intersection covering every possible
# gauge/case contact. This removes distant walls from expensive distance queries.
window=bd.Pos(181.5,-16.5,3.5)*bd.Box(73,73,24)
fixed={}
for n in ('top_acrylic','bottom_acrylic','top_spacer','bottom_spacer'):
    ss=[]
    for s in read_step(HERE/'STEP'/f'{n}.step').solids():
        cut=s.intersect(window)
        if cut is None:continue
        if hasattr(cut,'solids'):ss.extend(cut.solids())
        else:
            for item in cut:ss.extend(item.solids())
    fixed[n]=ss
print('Loaded rigid case solids',flush=True)
_boxes={}
def box(s):
    key=id(s)
    if key not in _boxes:_boxes[key]=(s,s.bounding_box())
    return _boxes[key][1]
def hits(a,b):
    aa=box(a);bb=box(b)
    return all(getattr(aa.max,k)>getattr(bb.min,k)+1e-6 and getattr(bb.max,k)>getattr(aa.min,k)+1e-6 for k in ('X','Y','Z'))
fail=[];tests=0
def check(label,s):
    global tests
    b=box(s)
    assert b.min.X>=145 and b.max.X<=218 and b.min.Y>=-53,(label,'outside checked window')
    for name,ss in fixed.items():
        for a in s.solids():
            for b in ss:
                tests+=1
                if not hits(a,b) or a.distance_to(b)>1e-6:continue
                v=overlap_volume(a,b)
                if v>1e-5:fail.append({'gauge':label,'case_part':name,'overlap_mm3':v})

scene=read_scene(HEAT/'reference/board.step')
front=json.loads((HEAT/'registration.json').read_text())['front_z_native_mm']
shellnode=next(n for n in scene.leaves() if n.label=='C2344_shell_OEM_reference')
usb_a_ref=shellnode.ref.rsplit('.',1)[0]
for name,ref in (('USB_A',usb_a_ref),('USB_C','#o1.26.1')):
    print('Checking native '+name,flush=True)
    shape=scene.resolve(ref if name=='USB_A' else str(HEAT/'reference/board.step')+ref).shape()
    for dx,dy,dz in itertools.product((-.5,0,.5),(-.5,0,.5),(-TRAVEL,0,TRAVEL)):
        check(f'{name}_native_{dx}_{dy}_{dz}',shape.moved(bd.Location((dx,dy,dz-front))))
print('Checking inserted and extracted body gauges',flush=True)

for dx,dy,dz in itertools.product((-.5,.5),(-.5,.5),(-TRAVEL,TRAVEL)):
    for offset in (-.5,.5):  # dongle body-to-plug axis offset is unpublished
        for extraction in (0,6,15,30):
            # 2 mm exposed plug/nose setback is a fit requirement, NOT a vendor datum.
            s=solid(rect(USB_A_X+dx,USB_A_FACE+dy+USB_A_BODY_SETBACK+7.5+extraction,15,15),USB_A_AXIS+dz+offset-4,8,'setback_dongle_body_gauge','#999999')
            check(f'A_body_{dx}_{dy}_{dz}_{offset}_{extraction}',s)
    for extraction in (0,10,28):
        # 13 x 8 is rounded up from manufacturer widths12.5/12.8 and height8.
        # 1.65 mm nose/overmold setback is a trial assumption, not a vendor datum.
        s=solid(rect(USB_C_X+dx,-33.809118+dy+1.65+14+extraction,13,28),1.605+dz-4,8,'USB_C_overmold_gauge','#999999')
        check(f'C_body_{dx}_{dy}_{dz}_{extraction}',s)
for x in (USB_A_X-14,USB_A_X+14):
    finger=bd.Pos(x,USB_A_FACE+17,USB_A_AXIS)*bd.Rot(90,0,0)*bd.Cylinder(6,16)
    check('12mm_side_pinch_finger_'+str(x),finger)

# Keep the incompatible original envelope visible rather than silently relaxing it.
zero_setback=solid(rect(USB_A_X,USB_A_FACE-.5+7.5,15,15),USB_A_AXIS+TRAVEL+.5-4,8,'zero_setback_negative_control','#999999')
zero_overlap=sum(overlap_volume(a,b) for a in zero_setback.solids() for b in fixed['top_acrylic'])
assert zero_overlap>1e-5,'Negative control should expose flat-roof limitation'

report={'units':'mm','main_case_height_mm':TOP-BOTTOM,'hood_height_mm':HOOD_TOP-BOTTOM,
 'maximum_envelope_mm':[292.6,191.0,HOOD_TOP-BOTTOM],
 'USB_A_bay_mm':{'width':43,'open_top':True,'wall_height_above_floor':TOP_INNER-LOWER_JOIN,'depth_from_mating_face':USB_MOUTH-USB_A_FACE,'throat':[20,HOOD_CEILING-USB_A_THROAT_BOTTOM],'connector_roof':ACRYLIC,'roof_owner':'top_acrylic','side_wall':2,'roof_end_y':USB_OPEN_START},
 'USB_C_tunnel_mm':{'width':18,'height':USB_C_CEILING-USB_C_FLOOR,'roof_owner':'top_spacer','rigid_mating_access':list(USB_C_ACCESS),'depth_from_mating_face':-24.516558-(-33.809118)},
 'native_connector_motion_checked_mm':{'x':[-.5,0,.5],'y':[-.5,0,.5],'z':[-TRAVEL,0,TRAVEL]},
 'gauge_assumptions':{'dongle_body':[15,15,8],'dongle_body_setback':USB_A_BODY_SETBACK,'minimum_body_setback_for_no_roof_overlap':USB_OPEN_START-(USB_A_FACE-.5),'dongle_vertical_axis_offset':[-.5,.5],'USB_C_body':[28,13,8],'USB_C_overmold_setback':1.65,'finger_diameter':12},
 'solid_pair_tests':tests,'collisions':fail,
 'incompatible_zero_setback_control':{'roof_overlap_mm3':zero_overlap,'expected_collision':True},
 'exact_case_crop_bounds_mm':[145,218,-53,20,-8.5,15.5],
 'limitations':'Conditional rigid fit only: dongle body requires 2 mm setback from mating face for this test; zero-setback generic envelope is NOT compatible with flat acrylic. Verify actual seated dongle nose/body position and axis offset. Cable nose setback and finger ergonomics require trials. Soft seals excluded; no IP rating.'}
(HERE/'usb-recess-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
assert not fail,'Repair USB recess before export/release'
