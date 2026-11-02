"""Nominal saved mounting layout checks, excluding unchosen screws and gaskets."""
from pathlib import Path
import json
import sys
from cadgen import read_scene,build123d as bd
from cadgen.geometry import overlap_volume
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from heatsink_mounting import rear_hardware,outer_plate_references

reg=json.loads((HERE/'registration.json').read_text())
saved=read_scene(str(HERE/'STEP/heatsink_mounting.step'))
board_scene=read_scene(str(HERE/'reference/board.step'))
new_parts=rear_hardware()+outer_plate_references()
saved_parts=[]
for proposed in new_parts:
    sh=saved.resolve('#'+proposed.label).shape()
    assert sh.is_valid and len(sh.solids())==1,proposed.label
    assert abs(sh.volume-proposed.volume)<1e-3,proposed.label
    saved_parts.append(sh)
hits=[]
tested=0
back_min=None
front_max=None
def boxes_intersect(a,b):
    return all(getattr(a.max,k)>getattr(b.min,k)+1e-6 and
               getattr(b.max,k)>getattr(a.min,k)+1e-6 for k in ('X','Y','Z'))
for leaf in board_scene.leaves():
    obj=board_scene.resolve(leaf.ref).shape().moved(bd.Location((0,0,-reg['front_z_native_mm'])))
    bb=obj.bounding_box(optimal=False)
    back_min=bb.min.Z if back_min is None else min(back_min,bb.min.Z)
    front_max=bb.max.Z if front_max is None else max(front_max,bb.max.Z)
    for proposed in saved_parts:
        if not boxes_intersect(bb,proposed.bounding_box(optimal=False)):
            continue
        for solid in obj.solids():
            tested+=1
            overlap=overlap_volume(proposed.solids()[0],solid)
            if overlap>1e-6:
                hits.append({'part':proposed.label,'board_ref':leaf.ref,'overlap_mm3':overlap})
report={'units':'mm','artifact_sha256':saved.document_hash,'new_part_count':len(saved_parts),
        'board_intersection_tests_after_bbox_filter':tested,'board_collision_hits':hits,
        'board_model_z_envelope':[back_min,front_max],
        'outer_plate_reference_z':{'bottom':[-15,-12],'top':[8,11]},
        'rear_washer_z':[-2.15,-1.65],'rear_retainer_z':[-4.15,-2.15],
        'rear_retainer_to_bottom_plate_vertical_gap_mm':7.85,
        'top_bezel_window_clearance_from_pcb_outline_mm':1.4,
        'scope':'Saved nominal layout only. Outer plates are envelopes. Gasket carrier, bottom spreader, V2 retention plate, screw/head/thread geometry and loaded motion are not released.'}
(HERE/'mounting-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
assert not hits,'Mounting layout collides with PCB components'
