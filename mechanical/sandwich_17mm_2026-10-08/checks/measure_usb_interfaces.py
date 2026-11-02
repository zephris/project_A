from pathlib import Path
import json
from cadgen import read_scene,build123d as bd
here=Path(__file__).resolve().parents[1]
heat=here.parent/'heatsink_2026-10-08'
scene=read_scene(heat/'reference/board.step')
datum=json.loads((heat/'registration.json').read_text())['front_z_native_mm']
out={}
for name,ref,y in [('USB_A','#o1.65.1',-33.3),('USB_C','#o1.26.1',-34.3)]:
    part=scene.resolve(ref).shape().moved(bd.Location((0,0,-datum)))
    b=part.bounding_box()
    row={'bounds':[b.min.X,b.max.X,b.min.Y,b.max.Y,b.min.Z,b.max.Z],'sections':[]}
    slab=bd.Pos((b.min.X+b.max.X)/2,y,3)*bd.Box(30,.1,20)
    for s in part.solids():
        cut=s.intersect(slab)
        pieces=list(cut) if isinstance(cut,list) else [cut]
        for p in pieces:
            if p and p.volume>1e-7:
                q=p.bounding_box();row['sections'].append({'volume':p.volume,'bounds':[q.min.X,q.max.X,q.min.Y,q.max.Y,q.min.Z,q.max.Z]})
    out[name]=row
    print(name,row,flush=True)
(here/'usb-interface-measurements.json').write_text(json.dumps(out,indent=2)+'\n')
