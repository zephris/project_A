"""Direct button-body versus other-component checks on saved candidate geometry.

Checks actual board STEP instances, not only case-versus-board collisions.
Keycap checks use the selected diameter's plan envelope; the exact underside
and seating depth of a purchased cap are not modeled.
"""
from pathlib import Path
import json,sys,math,hashlib,re
from cadgen import read_scene,read_step,build123d as bd
from cadgen.geometry import overlap_volume
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from common import *

reg=json.loads((HEAT/'registration.json').read_text())
scene=read_scene(HERE/'reference/board.step')
nodes=scene.roots[0].children
groups={};instances={}
for node in nodes:
    if not re.fullmatch(r'(?:SW\d+|OPSW\d+|[A-Z]+\d+)',node.label):continue
    shape=scene.resolve(node.ref).shape().moved(bd.Location((0,0,-reg['front_z_native_mm'])))
    groups.setdefault(node.label,[]).append(shape)
    instances.setdefault(node.label,[]).append(node.ref)
board={ref:bd.Compound(children=ss,label=ref) for ref,ss in groups.items()}
assert all(f'SW{i}' in board and len(groups[f'SW{i}'])==2 for i in range(1,17))
mounts=read_step(HERE/'STEP/mounts.step')
screen_stops=[]
for s in mounts.solids():
    bb=s.bounding_box(optimal=False);cx=(bb.min.X+bb.max.X)/2;cy=(bb.min.Y+bb.max.Y)/2
    if any(math.hypot(cx-x,cy-y)<.01 for x,y in screen_holes()):screen_stops.append(s)
screen_heads=[cylinder(x,y,4,5.2,1.6) for x,y in screen_holes()]
targets={'heatsink':read_step(HEAT/'STEP/heatsink_plate.step'),
 'screen_frame':read_step(HERE/'STEP/screen_frame.step'),
 'screen_posts_and_rear_caps':bd.Compound(children=screen_stops),
 'screen_screw_head_envelopes':bd.Compound(children=screen_heads),
 'OLED_module':board['U5']}
heat_mounts=[*make_stops(),*make_support_washers(),*rear_hardware()]
for ref in ('H5','H7','H12'):
    x,y=xy(ref);heat_mounts.append(cylinder(x,y,4 if ref=='H12' else 6,7,1.6 if ref=='H12' else 2.4))
targets['heatsink_mounts_and_head_envelopes']=bd.Compound(children=heat_mounts)
boxes={}
def box(s):
    if id(s) not in boxes:boxes[id(s)]=(s,s.bounding_box(optimal=False))
    return boxes[id(s)][1]
def box_gap(a,b):
    aa,bb=box(a),box(b)
    return math.sqrt(sum(max(0,getattr(aa.min,k)-getattr(bb.max,k),getattr(bb.min,k)-getattr(aa.max,k))**2 for k in ('X','Y','Z')))
def penetration(a,b):
    if box_gap(a,b)>1e-7:return 0.
    v=0.
    for x in a.solids():
        for y in b.solids():
            if box_gap(x,y)<1e-7 and x.distance_to(y)<1e-7:v+=overlap_volume(x,y)
    return v

results=[];hits=[];near_pcb=[]
refs=[f'SW{i}' for i in range(1,17)]+[f'OPSW{i}' for i in range(1,7)]+['SW19','SW20']
for ref in refs:
    a=board[ref];gaps={};basis={}
    for name,b in targets.items():
        lb=box_gap(a,b)
        exact=lb<1e-7 or (ref in ('SW1','SW16') and name in ('heatsink','screen_frame','screen_posts_and_rear_caps','screen_screw_head_envelopes'))
        gap=a.distance_to(b) if exact else lb
        gaps[name]=gap;basis[name]='exact_native_distance' if exact else 'conservative_AABB_lower_bound'
        if gap<1e-7:
            volume=penetration(a,b)
            if volume>1e-5:hits.append({'button':ref,'other':name,'volume_mm3':volume})
    # All other modeled PCB components, including each switch's local LED/R/C.
    # Its own socket and switch-body occurrences share the ref and are excluded.
    candidates=sorted((box_gap(a,b),other,b) for other,b in board.items() if other!=ref)
    nearest=None
    for lb,other,b in candidates:
        if nearest is not None and lb>nearest['distance_mm']+1e-7:break
        gap=a.distance_to(b)
        if nearest is None or gap<nearest['distance_mm']:nearest={'ref':other,'distance_mm':gap}
        if gap<1e-7:
            volume=penetration(a,b)
            if volume>1e-5:hits.append({'button':ref,'other':other,'volume_mm3':volume})
    # A nearer component must not hide a different overlapping candidate.
    for lb,other,b in candidates:
        if lb>1e-7:break
        volume=penetration(a,b)
        if volume>1e-5 and not any(h['button']==ref and h['other']==other for h in hits):hits.append({'button':ref,'other':other,'volume_mm3':volume})
    results.append({'button':ref,'step_occurrences':instances[ref],'clearance_to_targets_mm':gaps,'clearance_basis':basis,'nearest_other_PCB_component':nearest})
    print(ref, 'heat',round(gaps['heatsink'],4),'frame',round(gaps['screen_frame'],4),'nearest',nearest,flush=True)

# Conservative projected footprints extending through the complete obstacle Z
# range. These are clearance guards, not claims about an unspecified keycap.
guards=[];plan_clearances=[]
for i in range(1,17):
    ref=f'SW{i}';x,y=xy(ref);guard=cylinder(x,y,CAP_DIAMETER,0,15)
    for name in ('heatsink','screen_frame','screen_posts_and_rear_caps','screen_screw_head_envelopes','OLED_module'):
        b=targets[name]
        lb=box_gap(guard,b)
        gap=guard.distance_to(b) if lb<1e-7 else lb
        plan_clearances.append({'button':ref,'obstacle':name,'clearance_mm':gap,'basis':'exact_native_distance' if lb<1e-7 else 'conservative_AABB_lower_bound'})
        if gap<1e-7:
            vol=penetration(guard,b)
            if vol>1e-5:guards.append({'button':ref,'obstacle':name,'kind':f'{CAP_DIAMETER:g}mm_keycap_XY_projection_overlap','guard_overlap_mm3':vol,'sufficient_keycap_bottom_z_from_conservative_bounds_mm':box(b).max.Z,'actual_keycap_collision_confirmed':False})
cap_rows=[]
for s in read_step(HERE/'STEP/option_caps.step').solids():
    cap_rows.append({name:box_gap(s,b) for name,b in targets.items()})
pcb=HERE/'pcb/PHBox-ergonomic.kicad_pcb'
report={'units':'mm','source_pcb_sha256':hashlib.sha256(pcb.read_bytes()).hexdigest(),
 'reference_step_sha256':hashlib.sha256((HERE/'reference/board.step').read_bytes()).hexdigest(),
 'modeled_button_refs_checked':refs,'button_results':results,'modeled_body_collision_hits':hits,
 'option_cap_clearance_lower_bounds_mm':cap_rows,'keycap_plan_clearances':plan_clearances,'keycap_plan_guard_concerns':guards,
 'keycap_diameter_assumed_mm':CAP_DIAMETER,'actual_main_keycap_model_or_stroke_not_available':True,
 'existing_case_check':'../fit-check.json','scope':'Nominal saved native solids. No arbitrary exemption for local LEDs or unrelated PCB components. Own socket/switch parts are one designed assembly. Keycap guards are conservative plan envelopes, not actual keycap solids. Pressed switch internals, cap undersides and fabrication tolerances are not qualified.'}
(HERE/'checks/button-interference.json').write_text(json.dumps(report,indent=2)+'\n')
print('Modeled body hits:',hits,flush=True);print('Keycap plan guard concerns:',guards,flush=True)
