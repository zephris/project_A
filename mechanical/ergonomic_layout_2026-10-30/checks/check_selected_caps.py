"""Selected cap plan envelope, saved cover holes and added acrylic clearance.

The keycap cylinders are conservative space claims, not vendor underside models.
Only material added by shrinking the former 26.5 mm cover holes is rechecked
against board geometry; prior checks cover the unchanged case geometry.
"""
from pathlib import Path
import hashlib, json, math, sys
from cadgen import read_scene, read_step, build123d as bd
from cadgen.geometry import overlap_volume
import ezdxf

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / 'src'))
from common import *

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

prior = json.loads((HERE/'checks/button-interference.json').read_text())
pcb_hash = sha(HERE/'pcb/PHBox-ergonomic.kicad_pcb')
reference_hash = sha(HERE/'reference/board.step')
assert prior['source_pcb_sha256'] == pcb_hash
assert prior['reference_step_sha256'] == reference_hash
assert not prior['modeled_body_collision_hits']
assert CAP_DIAMETER == 20 and CAP_HOLE == 24
TOLERANCE=json.loads((HERE/'tolerance-budget.json').read_text())
Z_ALLOWANCE=TRAVEL+TOLERANCE['jlcpcb']['pcb_nominal_thickness_mm']*TOLERANCE['jlcpcb']['pcb_thickness_fraction']

top = read_step(HERE/'STEP/top_acrylic.step')
assert top.is_valid and len(top.solids()) == 1
doc = ezdxf.readfile(HERE/'DXF/top_acrylic.dxf')
assert not doc.audit().errors and doc.header['$INSUNITS'] == 4
circles = list(doc.modelspace().query('CIRCLE'))
hole_rows = []
for i in range(1,17):
    x,y = xy(f'SW{i}')
    found = [c for c in circles if math.hypot(c.dxf.center.x-x,c.dxf.center.y-y)<1e-5]
    assert len(found)==1 and abs(found[0].dxf.radius*2-CAP_HOLE)<1e-5
    void = cylinder(x,y,CAP_HOLE-0.0002,TOP_INNER,ACRYLIC)
    assert overlap_volume(top.solids()[0],void.solids()[0]) < 1e-5
    hole_rows.append({'switch':f'SW{i}','DXF_hole_diameter_mm':found[0].dxf.radius*2})
print(f'All sixteen saved STEP/DXF cover openings match {CAP_HOLE:g} mm',flush=True)

targets = {
    'heatsink':read_step(HEAT/'STEP/heatsink_plate.step'),
    'screen_frame':read_step(HERE/'STEP/screen_frame.step'),
    'screen_and_switch_plate_mounts':read_step(HERE/'STEP/mounts.step'),
    'screen_screw_heads':bd.Compound(children=[cylinder(x,y,4,5.2,1.6) for x,y in screen_holes()]),
    'heatsink_mounts':bd.Compound(children=[*make_stops(),*make_support_washers(),*rear_hardware()]),
}
heat_heads=[]
for ref in ('H5','H7','H12'):
    x,y=xy(ref); heat_heads.append(cylinder(x,y,4 if ref=='H12' else 6,7,1.6 if ref=='H12' else 2.4))
targets['heatsink_screw_heads']=bd.Compound(children=heat_heads)
cap_rows=[]; hits=[]
for i in range(1,17):
    ref=f'SW{i}'; x,y=xy(ref); guard=cylinder(x,y,CAP_DIAMETER,0,15)
    gaps={name:guard.distance_to(target) for name,target in targets.items()}
    for name,gap in gaps.items():
        if gap < 1e-5: hits.append({'button':ref,'target':name,'distance_mm':gap})
    # The OLED's preceding 24 mm guard was clear. A concentric 20 mm guard is
    # a subset, so its clearance remains positive for the unchanged board STEP.
    oled=next(r for r in prior['keycap_plan_clearances'] if r['button']==ref and r['obstacle']=='OLED_module')
    assert oled['clearance_mm']>0
    radius_allowance=(TOLERANCE['design_acceptance_targets_not_supplier_guarantees']['cap_maximum_diameter_mm']-CAP_DIAMETER)/2
    expanded_bounds={name:max(0,gap-radius_allowance) for name,gap in gaps.items()}
    assert min(expanded_bounds.values())>0
    cap_rows.append({'switch':ref,'native_plan_guard_distances_mm':gaps,'max_accepted_cap_guard_distance_lower_bounds_mm':expanded_bounds,'OLED_clear_by_subset_of_prior_24mm_guard':True})
    print(ref, 'heat',round(gaps['heatsink'],4),'frame',round(gaps['screen_frame'],4),flush=True)
assert not hits,hits

# The only newly occupied material is the annulus between the new and old
# cover-hole radii. Select every modeled footprint whose 2D bounding rectangle
# can reach an annulus, with 2 mm extra screening allowance. No local LED/R/C
# exemptions: native model bounds and solid intersections decide contacts.
_,fps=data()
centres=[xy(f'SW{i}') for i in range(1,17)]
def near_changed_hole(f):
    x,y,w,h=f['bbox_xy']; lo_x,hi_x=x,x+w; lo_y,hi_y=-y-h,-y
    return any(math.hypot(max(lo_x-cx,0,cx-hi_x),max(lo_y-cy,0,cy-hi_y))<=15.25 for cx,cy in centres)
near_refs={ref for ref,f in fps.items() if near_changed_hole(f)}
scene=read_scene(HERE/'reference/board.step')
reg=json.loads((HEAT/'registration.json').read_text())
rings=[solid(disk(x,y,26.5)-disk(x,y,CAP_HOLE),TOP_INNER,ACRYLIC,'added_acrylic','#999999') for x,y in centres]
ring_boxes=[r.bounding_box(optimal=False) for r in rings]
def box_overlap(a,b):
    return all(getattr(a.max,k)>getattr(b.min,k)+1e-6 and getattr(b.max,k)>getattr(a.min,k)+1e-6 for k in ('X','Y','Z'))
board_hits=[]; selected=[]; exact_tests=0
for node in scene.roots[0].children:
    if node.label not in near_refs: continue
    shape=scene.resolve(node.ref).shape().moved(bd.Location((0,0,-reg['front_z_native_mm'])))
    selected.append({'ref':node.label,'occurrence':node.ref})
    for dz in (-Z_ALLOWANCE,Z_ALLOWANCE):
        for dx,dy in ((0,0),(-.5,-.5),(-.5,.5),(.5,-.5),(.5,.5)):
            placed=shape.moved(bd.Location((dx,dy,dz)))
            bb=placed.bounding_box(optimal=False)
            for n,(ring,rb) in enumerate(zip(rings,ring_boxes),1):
                if not box_overlap(bb,rb): continue
                for part in placed.solids():
                    if not box_overlap(part.bounding_box(optimal=False),rb): continue
                    exact_tests+=1
                    v=overlap_volume(part,ring.solids()[0])
                    if v>1e-5: board_hits.append({'component':node.label,'cap_hole':f'SW{n}','offset_mm':[dx,dy,dz],'overlap_mm3':v})
print('Added acrylic native contacts:',len(board_hits),'exact tests:',exact_tests,flush=True)
out={
    'units':'mm','source_pcb_sha256':pcb_hash,'reference_step_sha256':reference_hash,
    'selected_keycap':LAYOUT['keycap_selection'],'keycap_diameter_mm':CAP_DIAMETER,'cover_hole_diameter_mm':CAP_HOLE,
    'cover_STEP_sha256':sha(HERE/'STEP/top_acrylic.step'),'cover_DXF_sha256':sha(HERE/'DXF/top_acrylic.dxf'),
    'saved_cover_valid_single_solid':True,'cover_holes':hole_rows,
    'nominal_radial_cap_to_cover_gap_mm':(CAP_HOLE-CAP_DIAMETER)/2,
    'sufficient_cap_to_cover_gap_with_XY_corner_offset_mm':(CAP_HOLE-CAP_DIAMETER)/2-math.sqrt(2)*.5,
    'guard_z_range_mm':[0,15],'cap_guard_rows':cap_rows,'cap_guard_contact_hits':hits,
    'prior_unchanged_board_body_checks_reused':True,
    'added_acrylic_component_instances_checked':selected,'added_acrylic_exact_solid_tests':exact_tests,
    'added_acrylic_board_collision_hits':board_hits,'XY_offsets_checked_mm':[[0,0],[-.5,-.5],[-.5,.5],[.5,-.5],[.5,.5]],
    'Z_offsets_checked_mm':[-Z_ALLOWANCE,Z_ALLOWANCE],
    'scope':'Nominal selected 20 mm circular envelope; cap and heatsink/frame move with PCB. Fixed-cover clearance checked at stated motion limits. Other case geometry relies on unchanged prior fit checks. Exact cap stem fit, skirt seating, actuation, material tolerance and purchased-part fit still need physical trials.'
}
(HERE/'checks/selected-caps.json').write_text(json.dumps(out,indent=2)+'\n')
assert not board_hits,board_hits
