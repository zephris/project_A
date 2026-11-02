from pathlib import Path
from cadgen import read_step,build123d as bd
from cadgen.geometry import overlap_volume
root=Path(__file__).resolve().parents[3]
s=read_step(root/'3dmodels/SW_Kailh_Choc_V2_red.step')
print('switch box',s.bounding_box(),flush=True)
for z in (2.5,2.6,2.7,2.8,2.9):
    p=bd.Pos(0,0,z)*bd.extrude(bd.Rectangle(20,20)-bd.Rectangle(14.1,14.1),1.3)
    hits=[]
    for i,a in enumerate(s.solids()):
        if a.distance_to(p)>1e-6:continue
        v=sum(overlap_volume(a,b) for b in p.solids())
        if v>1e-5:hits.append((i,v,str(a.bounding_box())))
    print(z,hits,flush=True)
