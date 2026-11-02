"""Verify saved roof shields the full USB-A body footprint at all allowed XY poses."""
from pathlib import Path
import sys,json
from cadgen import read_step,read_scene,build123d as bd
from cadgen.geometry import overlap_volume
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from common import *
part=read_step(HERE/'STEP/top_acrylic.step')
scene=read_scene(HEAT/'reference/board.step')
node=next(n for n in scene.leaves() if n.label=='C2344_shell_OEM_reference')
b=scene.resolve(node.ref).shape().bounding_box()
w=b.size.X+1;d=b.size.Y+1
shield=solid(rect((b.min.X+b.max.X)/2,(b.min.Y+b.max.Y)/2,w,d),TOP_INNER+.05,ACRYLIC-.1,'required_roof_material','#999999')
actual=sum(overlap_volume(s,g) for s in part.solids() for g in shield.solids())
assert abs(actual-shield.volume)<1e-5,(actual,shield.volume,'missing connector roof')
opening=solid(rect(192,(USB_OPEN_START+USB_MOUTH)/2,43,USB_MOUTH-USB_OPEN_START),TOP_INNER+.01,ACRYLIC-.02,'required_open_pocket','#999999')
blocked=sum(overlap_volume(s,g) for s in part.solids() for g in opening.solids())
assert blocked<1e-5,('finger pocket roof not removed',blocked)
report={'units':'mm','roof_owner':'top_acrylic','connector_roof_thickness':ACRYLIC,'connector_vertical_clearance_at_up_travel':TOP_INNER-7-TRAVEL,'required_roof_footprint':[w,d],
 'roof_material_expected_mm3':shield.volume,'roof_material_found_mm3':actual,
 'open_pocket_blockage_mm3':blocked,'minimum_roof_extension_beyond_connector_at_outward_pose':USB_OPEN_START-(b.max.Y+.5)}
c=scene.resolve(str(HEAT/'reference/board.step')+'#o1.26.1').shape().bounding_box()
cshield=solid(rect((c.min.X+c.max.X)/2,(c.min.Y+c.max.Y)/2,c.size.X+1,c.size.Y+1),USB_C_CEILING+.05,TOP_INNER-USB_C_CEILING-.1,'C_required_roof','#999999')
cpart=read_step(HERE/'STEP/top_spacer.step')
cv=sum(overlap_volume(s,g) for s in cpart.solids() for g in cshield.solids())
assert abs(cv-cshield.volume)<1e-5,('USB-C missing printed roof',cv,cshield.volume)
report['USB_C']={'roof_owner':'top_spacer','expected_material_mm3':cshield.volume,'found_material_mm3':cv,'rear_roof_clearance_at_up_travel':USB_C_CEILING-3.21-TRAVEL,
 'front_collar_roof_centre_z':1.605+USB_C_ACCESS[1]/2,
 'front_collar_roof_clearance_at_up_travel':1.605+USB_C_ACCESS[1]/2-3.21-TRAVEL,
 'front_collar_corner_radius':USB_C_ACCESS[2]}
(HERE/'roof-shield-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
