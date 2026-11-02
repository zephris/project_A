"""Saved soft-collar projection closes each rigid lip aperture except mating hole.

Nominal TPU free-state geometry only; no deformation or force qualification.
"""
from pathlib import Path
import sys,json
from cadgen import read_step,read_scene,build123d as bd
from cadgen.geometry import overlap_volume
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from common import *

seals=read_step(HERE/'STEP/port_seals.step')
assert seals.is_valid and len(seals.solids())==2
report={}
for kind,x,axis,w,h,iw,ih,floor,ceiling in (
    ('A',USB_A_X,USB_A_AXIS,*USB_A_ACCESS[:2],14.2,5.5,USB_A_THROAT_BOTTOM,TOP_INNER),
    ('C',USB_C_X,1.605,*USB_C_ACCESS[:2],8.74,3.01,USB_C_FLOOR,USB_C_CEILING)):
    seal=next(s for s in seals.solids() if abs(s.bounding_box().center().X-x)<.01)
    b=seal.bounding_box()
    assert abs(b.max.Y-PORT_SEAL_FRONT)<1e-6 and abs(b.min.Y-(PORT_SEAL_FRONT-PORT_SEAL_STOCK))<1e-6
    # Plane normal points rearward; sample just behind the integral retaining lip.
    access=port_access_cut(kind,PORT_SEAL_FRONT-.15,PORT_SEAL_FRONT-.1)
    hole=bd.Pos(x,PORT_SEAL_FRONT-.1,axis)*bd.Rot(90,0,0)*bd.extrude(rect(0,0,iw,ih,.25 if kind=='A' else 1.155),.05)
    fill=overlap_volume(seal,access.solids()[0])
    expected=access.volume-hole.volume
    assert abs(fill-expected)<1e-5,(kind,'unclosed clearance outside mating hole',fill,expected)
    assert abs(b.max.Z-(ceiling+.2))<1e-6 and abs(b.min.Z-(floor-.2))<1e-6
    report[kind]={'rigid_access_mm':[w,h],'free_mating_hole_mm':[iw,ih],
                 'gap_fill_expected_mm3':expected,'gap_fill_found_mm3':fill,
                 'axial_stock_mm':PORT_SEAL_STOCK,'outer_interference_mm':.2}
reg=json.loads((HEAT/'registration.json').read_text())
scene=read_scene(HEAT/'reference/board.step')
pcb=scene.resolve(str(HEAT/'reference/board.step')+reg['substrate']['ref']).shape()
pb=pcb.bounding_box()
assert all(abs(a-b)<1e-3 for a,b in zip((pb.min.X,pb.max.X,pb.min.Y,pb.max.Y),bounds())), 'Substrate reference must match current PCB outline'
pcb_hits=[]
for dy in (-.5,0,.5):
    for dz in (-TRAVEL,0,TRAVEL):
        pose=pcb.moved(bd.Location((0,dy,dz-reg['front_z_native_mm'])))
        v=sum(overlap_volume(a,b) for a in pose.solids() for b in seals.solids())
        if v>1e-5:pcb_hits.append({'dy':dy,'dz':dz,'overlap_mm3':v})
assert not pcb_hits,('collar loads PCB substrate',pcb_hits)
result={'units':'mm','saved_collars_valid':True,'collars':report,'native_PCB_edge_poses_checked':9,'PCB_overlap_hits':pcb_hits,
        'rear_PCB_rebate':{'front_limit_y':bounds()[3]+.6,'z_limits':[FOAM_TOP-TRAVEL-.1,TRAVEL+.1],'uncut_front_membrane_mm':PORT_SEAL_FRONT-(bounds()[3]+.6)},
        'material':'unfilled nonconductive TPU 95A trial',
        'limitations':'Free-state projection only; outer/inner interference intentional. TPU compliance, membrane print quality, creep, retention strength, dust and liquid ingress require physical trials.'}
(HERE/'port-seals-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
