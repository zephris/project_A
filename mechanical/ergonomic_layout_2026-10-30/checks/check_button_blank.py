"""Saved plug checks. Free-state latch interference is intentional, not FEA."""
from pathlib import Path
import json,sys,math,hashlib
from cadgen import read_step,build123d as bd
from cadgen.geometry import overlap_volume
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from button_blank_common import spec,invert_for_print,latch_parts,cyl
from common import xy,HEAT,TOP,TRAVEL,cylinder,screen_holes,make_stops,make_support_washers,rear_hardware

p=spec();printed=read_step(HERE/'STEP/button_blank.step');plug=invert_for_print(printed)
b=printed.bounding_box(optimal=False)
assert printed.is_valid and len(printed.solids())==1
assert abs(b.min.Z)<1e-5 and abs(b.max.Z-4.4)<1e-5
assert abs(b.size.X-25.8)<1e-5 and abs(b.size.Y-25.8)<1e-5

def gapbox(a,b):
    aa=a.bounding_box(optimal=False);bb=b.bounding_box(optimal=False)
    return math.sqrt(sum(max(0,getattr(aa.min,k)-getattr(bb.max,k),getattr(bb.min,k)-getattr(aa.max,k))**2 for k in ('X','Y','Z')))

def hit(a,b):
    if gapbox(a,b)>1e-6:return 0.
    return sum(overlap_volume(x,y) for x in a.solids() for y in b.solids() if gapbox(x,y)<1e-6)

teeth=latch_parts()
rigid=plug
for t in teeth:rigid=rigid-t
panel_rows=[]
for diameter in p['faceplate_hole_range']+[24]:
    for thick in p['faceplate_thickness_range']+[2]:
        panel=bd.Pos(0,0,-thick)*bd.Box(30,30,thick,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))
        panel=panel-cyl(diameter/2,-thick-.1,thick+.2)
        extra=hit(rigid,panel)
        latch_hit=hit(plug,panel)
        assert extra<1e-5 and latch_hit>0,(diameter,thick,extra,latch_hit)
        panel_rows.append({'diameter_mm':diameter,'thickness_mm':thick,'non_latch_intersection_mm3':extra,'intentional_free_state_latch_interference_mm3':latch_hit})
print('Nine panel size/thickness combinations: rigid body clear; latch interference present',flush=True)

fps={f['ref']:f for f in json.loads((HERE/'constraints.json').read_text())['footprints']}
switch=[];model_inputs=[]
# Use exactly the two zero-offset models selected by the PCB rather than
# loading the 180 MB full board STEP. The saved-board stem top was independently
# measured as 8.6000001 mm in the same front-seating datum.
for m in fps['SW1']['models']:
    assert m['offset']==[0,0,0] and m['scale']==[1,1,1] and m['rotation'][:2]==[0,0]
    source=Path(m['path']);shape=bd.Rot(0,0,m['rotation'][2])*read_step(source)
    switch.append(shape)
    model_inputs.append({'path':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'rotation_deg':m['rotation']})
assert len(switch)==2
sw=bd.Compound(children=switch)
stem_top=max(s.bounding_box(optimal=False).max.Z for s in switch)
assert abs(stem_top-8.6000001)<1e-5,stem_top
budget=json.loads((HERE/'checks/tolerance-budget.json').read_text())
lateral=budget['worst_case_lateral_allowance_mm'];dzmax=TRAVEL+.16
offsets=[(0.,0.)]+[(lateral*math.cos(a*math.pi/4),lateral*math.sin(a*math.pi/4)) for a in range(8)]
switch_hits=[]
for angle in (-10,0,10):
    cap=(bd.Pos(0,0,TOP)*bd.Rot(0,0,angle))*plug
    for dx,dy in offsets:
        for dz in (-dzmax,dzmax):
            body=sw.moved(bd.Location((dx,dy,dz)))
            v=hit(cap,body)
            if v>1e-5:switch_hits.append({'angle_deg':angle,'offset_mm':[dx,dy,dz],'overlap_mm3':v})
assert not switch_hits,switch_hits
print('Switch/socket clearance: 54 displaced/rotated poses pass; stem top',stem_top,flush=True)

targets={'heatsink':read_step(HEAT/'STEP/heatsink_plate.step'),
         'screen_frame':read_step(HERE/'STEP/screen_frame.step'),
         'screen_plate_posts':read_step(HERE/'STEP/mounts.step')}
heads=[cylinder(x,y,4,5.2,1.6) for x,y in screen_holes()]
for ref in ('H5','H7','H12'):
    x,y=xy(ref);heads.append(cylinder(x,y,4 if ref=='H12' else 6,7,1.6 if ref=='H12' else 2.4))
targets['hardware_envelopes']=bd.Compound(children=[*heads,*make_stops(),*make_support_washers(),*rear_hardware()])
nearby_hits=[];bounds=[]
for i in range(1,17):
    ref=f'SW{i}';x,y=xy(ref);nominal=(bd.Pos(x,y,TOP)*plug)
    gaps={name:nominal.distance_to(target) for name,target in targets.items()}
    bounds.append({'button':ref,'nominal_native_distances_mm':gaps})
    for angle in (-10,0,10):
        cap=(bd.Pos(x,y,TOP)*bd.Rot(0,0,angle))*plug
        for dx,dy in ((0,0),(-.5,-.5),(-.5,.5),(.5,-.5),(.5,.5)):
            for dz in (-dzmax,dzmax):
                for name,target in targets.items():
                    body=target.moved(bd.Location((dx,dy,dz)))
                    v=hit(cap,body)
                    if v>1e-5:nearby_hits.append({'button':ref,'target':name,'angle':angle,'offset':[dx,dy,dz],'overlap_mm3':v})
    print(ref,'nearest target',min(gaps,key=gaps.get),round(min(gaps.values()),3),flush=True)
assert not nearby_hits,nearby_hits
coupon=read_step(HERE/'STEP/button_blank_coupon.step');assert coupon.is_valid and len(coupon.solids())==1
panel_web=30.69789956034064-p['flange_diameter']
free_length=(p['beam_inner_radius']+p['beam_outer_radius'])/2*math.radians(p['beam_end_degrees']-p['beam_start_degrees']-p['root_span_degrees'])
deflection=p['latch_peak_radius']+p['printed_radial_error_target']-min(p['faceplate_hole_range'])/2
strain=1.5*(p['beam_outer_radius']-p['beam_inner_radius'])*deflection/free_length**2
out={'units':'mm','plug_print_bounds_mm':[list(b.min),list(b.max)],'native_valid_single_solid':True,
 'rise_above_face_mm':p['rise_above_face'],'groove_width_mm':p['groove_width'],'groove_height_mm':p['groove_height'],
 'minimum_lip_above_groove_mm':p['rise_above_face']-p['groove_height'],'panel_size_checks':panel_rows,
 'selected_PCB_model_inputs':model_inputs,'saved_board_stem_top_verified_mm':8.6000001,
 'saved_switch_stem_top_mm':stem_top,'roof_clearance_at_up_Z_allowance_mm':TOP+p['roof_underside']-stem_top-dzmax,
 'switch_sampled_radial_offset_mm':lateral,'switch_poses_checked':54,'switch_collision_hits':switch_hits,
 'nearby_component_nominal_distances':bounds,'nearby_component_collision_hits':nearby_hits,
 'nearby_component_motion_samples_XY_mm':.5,'Z_motion_plus_thickness_mm':dzmax,'orientation_range_deg':[-10,10],
 'minimum_adjacent_blank_flange_gap_mm':panel_web,'effective_curved_beam_arc_length_mm':free_length,
 'estimated_maximum_radial_insertion_deflection_mm':deflection,'straight_beam_strain_proxy':strain,
 'strain_scope':'Small-deflection straight-beam estimate applied to arc length; not curved-beam FEA or a material strength qualification.',
 'retention_and_removal_force_measured':False,'fatigue_qualified':False,
 'scope':'Keycap removed; switch retained. Grooves left/right, clips front/back. Free-state latch/panel intersections intentionally require radial flex. Other obstacles tested at stated sampled poses, not a continuous swept tolerance envelope. Actual insertion, removal, acrylic edge condition and print fit require a first article.'}
(HERE/'checks/button-blank.json').write_text(json.dumps(out,indent=2)+'\n')
print('Blank dimensions, clip mating and component checks passed',flush=True)
