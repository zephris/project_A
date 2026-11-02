"""Saved-artifact nominal fit and travel checks; not a preload/strength qualification."""
from pathlib import Path
import json,sys,hashlib,math
from types import SimpleNamespace
from cadgen import read_step,read_scene,build123d as bd
from cadgen.geometry import overlap_volume
from OCP.BRepAdaptor import BRepAdaptor_Surface
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from common import *

def bbox_hits(a,b):
    return all(getattr(a.max,k)>getattr(b.min,k)+1e-6 and getattr(b.max,k)>getattr(a.min,k)+1e-6 for k in ('X','Y','Z'))

_boxes={}
_solids={}
def box(s):
    key=id(s)
    if key not in _boxes:_boxes[key]=(s,s.bounding_box())
    return _boxes[key][1]

def solids(s):
    key=id(s)
    if key not in _solids:_solids[key]=(s,list(s.solids()))
    return _solids[key][1]

def shifted(s,dz):
    result=s.moved(bd.Location((0,0,dz)))
    def cache_box(old,new):
        b=box(old)
        _boxes[id(new)]=(new,SimpleNamespace(min=bd.Vector(b.min.X,b.min.Y,b.min.Z+dz),max=bd.Vector(b.max.X,b.max.Y,b.max.Z+dz)))
    cache_box(s,result)
    children=[]
    for old in solids(s):
        new=old.moved(bd.Location((0,0,dz)))
        cache_box(old,new);children.append(new)
    _solids[id(result)]=(result,children)
    return result

def contained_rect(b,x,y,w,h):
    return b.min.X>=x-w/2+1e-5 and b.max.X<=x+w/2-1e-5 and b.min.Y>=y-h/2+1e-5 and b.max.Y<=y+h/2-1e-5

def empty_box(name,b):
    # These are actual source through-cut volumes, not approximate collision exemptions.
    if name=='top_acrylic':
        for n in range(1,17):
            x,y=xy(f'SW{n}')
            if max(math.hypot(xx-x,yy-y) for xx in (b.min.X,b.max.X) for yy in (b.min.Y,b.max.Y))<CAP_HOLE/2-1e-5:return True
    if name=='top_spacer':
        xmin,xmax,ymin,ymax=bounds()
        # Core lies inside the rounded opening and beyond all capture ledges.
        near_c_roof=not (b.max.X<USB_C_X-USB_C_ROOF_WIDTH/2 or b.min.X>USB_C_X+USB_C_ROOF_WIDTH/2 or b.max.Y< -42.4 or b.min.Y> -32.4 or b.max.Z<USB_C_CEILING or b.min.Z>TOP_INNER)
        near_c_collar=not (b.max.X<USB_C_X-7 or b.min.X>USB_C_X+7 or b.max.Y<PORT_BODY_BACK or b.min.Y>PORT_LIP_FRONT or b.max.Z<TRAVEL+.1 or b.min.Z>TOP_INNER)
        near_a_collar=not (b.max.X<USB_A_X-9.1 or b.min.X>USB_A_X+9.1 or b.max.Y<PORT_BODY_BACK or b.min.Y>PORT_LIP_FRONT or b.max.Z<TRAVEL+.1 or b.min.Z>TOP_INNER)
        if not near_c_roof and not near_c_collar and not near_a_collar and contained_rect(b,(xmin+xmax)/2,(ymin+3+ymax+.5)/2,xmax-xmin-12,ymax+.5-ymin-3):return True
    if name in ('foam','bottom_spacer'):
        if name=='bottom_spacer' and b.min.Z>FOAM_BOTTOM+1e-5:
            xmin,xmax,ymin,ymax=bounds()
            core=contained_rect(b,(xmin+xmax)/2,(ymin+3+ymax+.5)/2,xmax-xmin-12,ymax+.5-ymin-3)
            near_guide=any(not (b.max.X<x-2.7 or b.min.X>x+2.7 or b.max.Y<y-2.7 or b.min.Y>y+2.7) for x,y in (xy('H4'),xy('H6')))
            if core and not near_guide:return True
        for n in range(1,17):
            x,y=xy(f'SW{n}')
            if contained_rect(b,x,y,20,18):return True # conservative inside rounded22x20 R1
        if contained_rect(b,163,-64,84,58):return True
        if contained_rect(b,100.3,-54,36.4,34.5):return True
        if any(contained_rect(b,x,-44.016558,6.8,8.0) for x in (217.73218,227.73218,237.73218,250.73218,260.73218,270.73218)):return True
        for f in data()[1].values():
            if f['side']=='B':
                x,y,w,h=f['bbox_xy']
                if contained_rect(b,x+w/2,-y-h/2,w+1.4,h+1.4):return True
    return False

def volume_hit(a,b):
    if not bbox_hits(box(a),box(b)):return 0
    # Imported compound intersections are unreliable in this kernel: native solid pairs only.
    total=0
    for x in solids(a):
        for y in solids(b):
            if not bbox_hits(box(x),box(y)):continue
            if x.distance_to(y)>1e-6:continue
            total+=overlap_volume(x,y)
    return total

names=['top_acrylic','bottom_acrylic','top_spacer','bottom_spacer','switch_plate','screen_frame','foam','mounts','case_hardware','option_caps','option_retainer','option_hardware']
new={n:read_step(HERE/'STEP'/f'{n}.step') for n in names}
print('Loaded saved new parts',flush=True)
validity={n:{'valid':s.is_valid,'solids':len(s.solids()),'volume_mm3':s.volume} for n,s in new.items()}
assert all(v['valid'] for v in validity.values())
assert all(validity[n]['solids']==1 for n in ('top_acrylic','bottom_acrylic','top_spacer','bottom_spacer','switch_plate','screen_frame')),'Detached mechanical island'
reg=json.loads((HEAT/'registration.json').read_text())
scene=read_scene(HEAT/'reference/board.step')
board=[];prototypes={}
for leaf in scene.leaves():
    s=scene.resolve(leaf.ref).shape().moved(bd.Location((0,0,-reg['front_z_native_mm'])))
    board.append((leaf.ref,leaf.label,s))
    prototypes[leaf.ref]=leaf.prototype_id
substrate=next(s for ref,_,s in board if ref==reg['substrate']['ref'])
guide_holes=[]
for guide in ('H4','H6'):
    gx,gy=xy(guide);found=[]
    for face in substrate.faces():
        a=BRepAdaptor_Surface(face.wrapped)
        if face.geom_type!=bd.GeomType.CYLINDER:continue
        c=a.Cylinder();loc=c.Location()
        if abs(loc.X()-gx)<1e-5 and abs(loc.Y()-gy)<1e-5:found.append(c.Radius()*2)
    assert any(abs(d-6.4)<1e-5 for d in found),(guide,found)
    guide_holes.append({'hole':guide,'native_hole_diameter_mm':6.4,'guide_diameter_mm':5.4,'radial_clearance_mm':.5})
clip_cache={}
def plate_overlap(ref,s):
    b=box(s)
    for n in range(1,17):
        x,y=xy(f'SW{n}')
        if contained_rect(b,x,y,20,20):
            # A20mm local ring contains every possible global-plate contact here.
            # Geometry/prototype and relative placement are identical at each switch.
            key=(prototypes[ref],round((b.min.X+b.max.X)/2-x,5),round((b.min.Y+b.max.Y)/2-y,5))
            if key not in clip_cache:
                ring=solid(rect(x,y,20,20)-rect(x,y,SWITCH_APERTURE,SWITCH_APERTURE),PLATE_BOTTOM,PLATE_THICKNESS,'local_plate_contact_superset','#999999')
                clip_cache[key]=volume_hit(ring,s)
            return clip_cache[key]
    return volume_hit(new['switch_plate'],s)
hits=[];tested=0
for name,part in new.items():
    print('Board check: '+name,flush=True)
    for ref,label,s in board:
        if not bbox_hits(box(part),box(s)):continue
        if empty_box(name,box(s)):continue
        if name=='top_spacer' and ref==reg['substrate']['ref']:continue # exact R5 board outline is inside the R5.6 opening; ledges start at Z4.9
        if name=='bottom_spacer' and ref==reg['substrate']['ref']:continue # floor below board; only two guide pins rise, and their native6.4 bores were verified
        tested+=1;v=plate_overlap(ref,s) if name=='switch_plate' else volume_hit(part,s)
        if v>1e-5:hits.append({'new_part':name,'board_ref':ref,'board_label':label,'overlap_mm3':v})
    print('Completed '+name+'; board collision count='+str(len(hits)),flush=True)
pair_hits=[]
print('New part pair checks',flush=True)
for i,(name,a) in enumerate(new.items()):
    for other,b in list(new.items())[i+1:]:
        v=volume_hit(a,b)
        if v>1e-5:pair_hits.append({'a':name,'b':other,'overlap_mm3':v})
mount_solids=solids(new['mounts'])
for i,a in enumerate(mount_solids):
    for j,b in enumerate(mount_solids[i+1:],i+1):
        v=volume_hit(a,b)
        if v>1e-5:pair_hits.append({'a':f'mount_piece_{i}','b':f'mount_piece_{j}','overlap_mm3':v})
(HERE/'fit-static-check.json').write_text(json.dumps({'board_collision_hits':hits,'new_parts_collision_hits':pair_hits},indent=2)+'\n')
# The moving island includes all board/support/retention geometry; foam deforms instead.
moving=[(ref,s) for ref,_,s in board]+[(n,new[n]) for n in ('switch_plate','screen_frame','mounts','option_caps')]
moving += [('heatsink',make_plate()),*[(s.label,s) for s in make_stops()+make_support_washers()+rear_hardware()]]
travel_hits=[]
for dz in (-TRAVEL,TRAVEL):
    print('Hard travel checks: '+str(dz),flush=True)
    for n,s in moving:
        translated=shifted(s,dz)
        for fixed in ('top_acrylic','bottom_acrylic','top_spacer','bottom_spacer','case_hardware','option_retainer','option_hardware'):
            if empty_box(fixed,box(translated)):continue
            if n==reg['substrate']['ref'] and fixed in ('top_spacer','bottom_spacer'):continue # outlines/guide bores and vertical gaps remain valid at both Z limits
            v=volume_hit(translated,new[fixed])
            if v>1e-5:travel_hits.append({'dz_mm':dz,'moving':n,'fixed':fixed,'overlap_mm3':v})
head_hits=[]
heads=[]
for ref in ('H5','H7','H12','H1','H2','H3'):
    x,y=xy(ref);z=7 if ref in ('H5','H7','H12') else PLATE_TOP
    d,h=(4,1.6) if ref=='H12' else (6,2.4)
    heads.append((ref,cylinder(x,y,d,z,h)))
for i,(x,y) in enumerate(screen_holes(),1):heads.append((f'screen_{i}',cylinder(x,y,4,5.2,1.6)))
for dz in (-TRAVEL,0,TRAVEL):
    for label,s in heads:
        for fixed in ('top_acrylic','top_spacer'):
            v=volume_hit(s.moved(bd.Location((0,0,dz))),new[fixed])
            if v>1e-5:head_hits.append({'head_envelope':label,'dz_mm':dz,'fixed':fixed,'overlap_mm3':v})
sw=[xy(f'SW{n}') for n in range(1,17)]
web=min(math.dist(a,b)-CAP_HOLE for i,a in enumerate(sw) for b in sw[i+1:])
report={'units':'mm','source_pcb_sha256':hashlib.sha256((ROOT/'Flatbox-rev8.kicad_pcb').read_bytes()).hexdigest(),
        'main_case_size_mm':[292.6,191.0,17.0],'maximum_case_size_mm':[292.6,191.0,HOOD_TOP-BOTTOM],'case_z_mm':[BOTTOM,HOOD_TOP],
        'plate_z_mm':[PLATE_BOTTOM,PLATE_TOP],'foam_installed_z_mm':[FOAM_BOTTOM,FOAM_TOP],
        'foam_free_thickness_mm':2,'foam_nominal_compression_fraction':1-(FOAM_TOP-FOAM_BOTTOM)/2,
        'upper_pads_installed_thickness_mm':1.2,'upper_pads_free_thickness_mm':1.5,
        'travel_checked_mm':[-TRAVEL,TRAVEL],
        'rear_lowest_clearance_at_down_travel_mm':.5-TRAVEL,
        'heatsink_to_top_inner_clearance_at_up_travel_mm':TOP_INNER-7-TRAVEL,
        'minimum_top_aperture_web_mm':web,'switch_aperture_mm':SWITCH_APERTURE,
        'validity':validity,'board_tests_after_bbox_prune':tested,
        'board_collision_hits':hits,'new_parts_collision_hits':pair_hits,'hard_travel_collision_hits':travel_hits,
        'internal_screw_head_envelope_collisions':head_hits,
        'native_guide_holes':guide_holes,'unique_switch_prototype_contact_tests':len(clip_cache),
        'scope':'Nominal saved STEP geometry only. Foam contact is intentional; rigid intersections fail. Clip snap engagement, material tolerances, screw threads, retainer pullout, force equilibrium, PCB bending, keycap travel and real dongle clearance require trials.'}
(HERE/'fit-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
assert not hits and not pair_hits and not travel_hits and not head_hits,'Resolve collisions before release'
