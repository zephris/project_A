from pathlib import Path
import sys,json
from cadgen import read_step,build123d as bd
from cadgen.geometry import overlap_volume
here=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(here/'src'))
from common import *
def hit(a,b):
    return sum(overlap_volume(x,y) for x in a.solids() for y in b.solids() if x.distance_to(y)<1e-6)
screw=read_step(HERE/'imported/ISO10642_M3x6.step')
local=bd.Pos(0,0,-2)*bd.extrude(bd.Rectangle(12,12)-bd.Circle(1.7),2)
local-=bd.Pos(0,0,-1.65)*bd.Cone(1.7,3.35,1.65,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))
results={'case_head_overlap_mm3':hit(screw,local)}
plate=solid(plate_profile(),PLATE_BOTTOM,PLATE_THICKNESS,'plate','#888888')
results['plate_heatsink_overlap_mm3']=hit(plate,make_plate())
results['plate_top_spacer_overlap_mm3']=hit(plate,top_spacer_shape())
screen=solid(screen_frame_profile(),4.2,1,'screen','#888888')
oled=read_step(ROOT/'3dmodels/OLED_HS13L03W2C01.step').moved(bd.Location((100.3,-54,3)))
results['screen_frame_module_overlap_mm3']=hit(screen,oled)
mounts=screen_posts()+plate_posts()
results['internal_mount_piece_overlap_mm3']=sum(hit(a,b) for i,a in enumerate(mounts) for b in mounts[i+1:])
print(json.dumps(results,indent=2),flush=True)
(HERE/'corrected-source-check.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(v<1e-5 for v in results.values()),results
