"""C2344 native STEP pin/PCB registration and mating-opening check."""
from pathlib import Path
import json
from cadgen import read_scene,read_step,build123d as bd
HERE=Path(__file__).resolve().parents[1]
data=json.loads((HERE/'constraints.json').read_text())
fp=next(f for f in data['footprints'] if f['ref']=='USB2')
assert fp['side']=='F' and fp['pcb_xy']==[192.0,47.0]
front=json.loads((HERE/'registration.json').read_text())['front_z_native_mm']
scene=read_scene(HERE/'reference/board.step')
leaves=list(scene.leaves())
shellnode=next(n for n in leaves if n.label=='C2344_shell_OEM_reference')
parent=shellnode.ref.rsplit('.',1)[0]
shell=scene.resolve(shellnode.ref).shape().moved(bd.Pos(0,0,-front))
def merged(q):
    return bd.Compound(children=list(q)) if isinstance(q,bd.ShapeList) else q
contacts=[]
for i in range(1,5):
    n=next(n for n in leaves if n.label==f'C2344_contact_{i}_simplified')
    s=scene.resolve(n.ref).shape().moved(bd.Pos(0,0,-front))
    sec=merged(s.intersect(bd.Pos(192,-47,-.8)*bd.Box(30,30,.01)))
    assert sec
    b=sec.bounding_box();xy=[(b.min.X+b.max.X)/2,-(b.min.Y+b.max.Y)/2]
    pad=next(p for p in fp['pads'] if p['number']==str(i))
    assert max(abs(a-b) for a,b in zip(xy,pad['pcb_xy']))<1e-5
    assert pad['drill_mm']==[.9,.9]
    contacts.append({'number':i,'net':pad['net'],'pin_section_center_pcb_xy_mm':xy,'drill_mm':.9})
for x in (185,199):
    pad=next(p for p in fp['pads'] if p['number']=='5' and abs(p['pcb_xy'][0]-x)<1e-5)
    assert pad['drill_mm']==[2.1,2.1] and abs(pad['pcb_xy'][1]-44.29)<1e-5
    probe=bd.Pos(x,-44.29,-.8)*bd.Box(.41,1.41,.01)
    cut=merged(shell.intersect(probe));assert cut and cut.volume>.005
sb=shell.bounding_box()
assert abs(sb.min.Z+3.7)<1e-5 and abs(sb.max.Z-7)<1e-5
assert abs(sb.max.Y+34.14)<1e-5
probe=bd.Pos(192,-34.5,3.0)*bd.Box(11,.5,2)
usb=scene.resolve(parent).shape().moved(bd.Pos(0,0,-front))
cut=merged(usb.intersect(probe));blocked=cut.volume if cut else 0
assert blocked<1e-5,'Mating insertion gap blocked'
plate=read_step(HERE/'STEP/heatsink_plate.step')
distance=min(a.distance_to(b) for a in usb.solids() for b in plate.solids())
assert distance>0
report={'units':'mm','board_sha256':data['sha256'],'usb2_model_group':parent,
 'contacts':contacts,'shell_pins_registered':True,'PCB_seating_z_mm':0,
 'shell_z_mm':[sb.min.Z,sb.max.Z],'mating_face_cad_y_mm':sb.max.Y,
 'mating_gap_probe_overlap_mm3':blocked,'heatsink_min_distance_mm':distance,
 'scope':'Drawing-derived reference with simplified shell/plastic/contact details. Physical sample and solder clearance trial required.'}
(HERE/'usb-top-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
