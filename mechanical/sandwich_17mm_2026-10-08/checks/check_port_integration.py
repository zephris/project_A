"""Prove acrylic USB-A roof and integral printed sidewalls/floors."""
from pathlib import Path
import json,sys
from cadgen import read_step
from cadgen.geometry import overlap_volume
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE/'src'))
from common import *
upper=read_step(HERE/'STEP/top_spacer.step')
lower=read_step(HERE/'STEP/bottom_spacer.step')
acrylic=read_step(HERE/'STEP/top_acrylic.step')
for s in (upper,lower):assert s.is_valid and len(s.solids())==1
regions={
 'USB_C_printed_roof':(upper,solid(rect(USB_C_X,-38,10,8),7.1,.7,'probe','#999999')),
 'USB_C_integral_sidewall':(upper,solid(rect(USB_C_X+9.5,-28,1,5),0,6.5,'probe','#999999')),
 'USB_C_integral_lower_floor':(lower,solid(rect(USB_C_X,-28,18,5),-4.8,1.0,'probe','#999999')),
 'USB_A_integral_lower_floor':(lower,solid(rect(USB_A_X,-28,43,5),-4.8,2.8,'probe','#999999')),
 'USB_A_acrylic_roof':(acrylic,solid(rect(USB_A_X,-40,20,10),8.1,1.8,'probe','#999999')),
 'USB_A_integral_sidewall':(upper,solid(rect(USB_A_X+22.5,-28,1,5),0,7.8,'probe','#999999')),
 'USB_A_seal_retainer':(upper,solid(rect(USB_A_X+9,-33.4,1,.3),1,6.5,'probe','#999999')),
 'USB_C_seal_retainer':(upper,solid(rect(USB_C_X+6,-33.4,1,.3),0,6.5,'probe','#999999')),
 'USB_A_shell_cheek':(upper,solid(rect(USB_A_X+8.5,-35,.8,2),.5,7.3,'probe','#999999')),
 'USB_C_close_roof':(upper,solid(rect(USB_C_X,-35,8,2),3.8,3.8,'probe','#999999'))}
report={}
for name,(part,probe) in regions.items():
 v=sum(overlap_volume(a,b) for a in part.solids() for b in probe.solids())
 assert abs(v-probe.volume)<1e-5,(name,v,probe.volume)
 report[name]={'expected_material_mm3':probe.volume,'found_material_mm3':v}
# Printed C roof must leave the cable tunnel open beneath it.
void=solid(rect(USB_C_X,-28,17.8,5),6.0,.7,'clear_C_tunnel','#999999')
blocked=sum(overlap_volume(a,b) for a in upper.solids() for b in void.solids())
assert blocked<1e-5,('blocked C tunnel',blocked)
result={'units':'mm','upper_spacer_valid_single_solid':True,'lower_spacer_valid_single_solid':True,
 'integral_regions':report,'printed_outputs':['STL/top_spacer.stl','STL/bottom_spacer.stl'],
 'C_tunnel_obstruction_mm3':blocked,
 'seal_retention':{'front_seat_y':PORT_SEAL_FRONT,'lip_front_y':PORT_LIP_FRONT,'collar_axial_depth':PORT_SEAL_STOCK,'A_rigid_access':list(USB_A_ACCESS),'C_rigid_access':list(USB_C_ACCESS),'shell_collar_back_y':PORT_BODY_BACK,'clearance_beyond_shell_travel':PORT_RUNNING_CLEARANCE},
 'separate_components':'A roof is top acrylic; lower C roof is integral upper spacer. Sidewalls, floors and seal-retaining lips are integral. TPU 95A trial collars have intentional 0.2 mm outer interference; qualify perimeter adhesive only if needed. Compliance/retention forces require trials.'}
(HERE/'port-integration-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
