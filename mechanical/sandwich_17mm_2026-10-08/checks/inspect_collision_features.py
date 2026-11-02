from pathlib import Path
import json
from cadgen import read_scene,read_step,build123d as bd
here=Path(__file__).resolve().parents[1]
heat=here.parent/'heatsink_2026-10-08'
scene=read_scene(heat/'reference/board.step')
reg=json.loads((heat/'registration.json').read_text())
out=[]
for ref in ('#o1.74.1','#o1.89.1','#o1.95.1','#o1.100.1','#o1.124.1','#o1.134.1','#o1.68.1'):
    s=scene.resolve(ref).shape().moved(bd.Location((0,0,-reg['front_z_native_mm'])))
    b=s.bounding_box()
    row={'ref':ref,'bounds':[b.min.X,b.max.X,b.min.Y,b.max.Y,b.min.Z,b.max.Z]}
    out.append(row)
    print(row,flush=True)
s=read_step(here/'imported/ISO10642_M3x6.step')
print('screw',s.bounding_box(),flush=True)
(here/'collision-features.json').write_text(json.dumps(out,indent=2))
