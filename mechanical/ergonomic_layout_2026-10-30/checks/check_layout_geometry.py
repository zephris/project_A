"""Check closed aperture lands and the newly introduced heatsink/plate gap."""
from pathlib import Path
import sys,json
from cadgen import read_step
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from common import *
plate=read_step(HERE/'STEP/switch_plate.step')
heat=read_step(HEAT/'STEP/heatsink_plate.step')
gap=plate.distance_to(heat)
dist=BRepExtrema_DistShapeShape(plate.wrapped,heat.wrapped)
closest=[(q.X(),q.Y(),q.Z()) for q in (dist.PointOnShape1(1),dist.PointOnShape2(1))]
print('Overall plate / heatsink gap:',gap,'at',closest,flush=True)
# The existing H7 relief determines the whole-plate minimum. Separately check
# the two new extensions; their target is at least 0.6 mm of nominal clearance.
extension_gaps={}
for ref in ('SW1','SW16'):
    local=plate & solid(rect(*xy(ref),24,30),PLATE_BOTTOM,PLATE_THICKNESS,'extension_check','#999999')
    extension_gaps[ref]=local.distance_to(heat)
assert gap>=.29999,gap
assert min(extension_gaps.values())>=.59999,extension_gaps
profile=plate_profile();cover=top_profile();lands=[]
for n in range(1,17):
    x,y=xy(f'SW{n}')
    ring=rect(x,y,20.1,20.1)-rect(x,y,14.1,14.1)
    missing=max(0,ring.area-(profile & ring).area)
    assert missing<1e-5,(n,missing)
    cover_ring=disk(x,y,CAP_HOLE+.6)-disk(x,y,CAP_HOLE)
    open_area=max(0,cover_ring.area-(cover & cover_ring).area)
    assert open_area<1e-5,(n,open_area)
    lands.append({'switch':f'SW{n}','plate_missing_3mm_land_area_mm2':missing,'cover_missing_0p3mm_land_area_mm2':open_area})
out={'units':'mm','saved_plate_to_heatsink_gap_mm':gap,'closest_points_plate_then_heatsink':closest,'new_extension_gaps_mm':extension_gaps,'all_16_plate_apertures_have_3mm_square_lands':True,
 'all_16_cover_openings_are_separate_from_other_cutouts':True,'aperture_checks':lands,
 'scope':'Nominal geometry; no plate stiffness, cutting tolerance or hand-fit qualification.'}
(HERE/'checks/layout-geometry.json').write_text(json.dumps(out,indent=2)+'\n')
print('Aperture lands: passed; heatsink gap:',gap)
