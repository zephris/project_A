"""Local fit coupon only; no full enclosure release. Dimensions mm."""
from pathlib import Path
import sys,json
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]; OUT=HERE/'usb_dongle_bay';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'stage2_work/enclosure_cad_dependencies'))
import cadquery as cq
import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
# Local X=0 at socket centre; Y=0 mating face; positive Y outward.
# U-shaped 3 mm plate coupon, open mouth, top -10.55; independent from floating PCB.
plate=cq.Workplane('XY').box(35,40,3,centered=(True,False,False)).translate((0,-5,-13.55))
slot=cq.Workplane('XY').box(21,36,5,centered=(True,False,False)).translate((0,0,-14.55))
plate=plate.cut(slot)
# Two rails with top 0.75 below trial body; 15 mm entry ramp drops 2 mm.
rails=[]
for x in [-13,13]:
 rail=cq.Workplane('YZ').polyline([(0,-13.55),(35,-13.55),(35,-13.3),(20,-11.3),(0,-11.3)]).close().extrude(2).translate((x-1,0,0))
 rails.append(rail)
a=cq.Assembly(name='PROTOTYPE_local_dongle_bay');a.add(plate,name='bottom_plate_coupon')
for i,r in enumerate(rails): a.add(r,name=f'feed_rail_{i+1}')
a.save(str(OUT/'local-bay-fit-coupon.step'))
cq.exporters.export(plate, str(OUT/'bottom-plate-coupon.stl'))
for i,r in enumerate(rails):cq.exporters.export(r,str(OUT/f'feed-rail-{i+1}.stl'))
doc=ezdxf.new('R2010');ms=doc.modelspace();ms.add_lwpolyline([(-17.5,-5),(17.5,-5),(17.5,35),(10.5,35),(10.5,0),(-10.5,0),(-10.5,35),(-17.5,35)],close=True);doc.saveas(OUT/'bottom-plate-coupon.dxf')
meta={'status':'prototype local interface coupon, not full enclosure','coordinates':'X=0 socket centre, Y=0 mating face, Y positive outward; Z=PCB front datum','kicad_socket_face':[192,32.5],'slot_width_mm':21,'thermal_relief_recommended_width_mm':23,'plate_thickness_mm':3,'plate_top_z_mm':-10.55,'guide_top_z_mm':-11.3,'guide_clearance_to_assumed_dongle_mm':.75,'entry_ramp_length_mm':15,'entry_ramp_drop_mm':2,'target_body_mm':[15,15,8],'body_centre_z_assumed_mm':-6.55,'insertion_sweep_mm':50,'limits':['body-to-plug offset unverified','gasket travel and case wall geometry unresolved','rails must not rigidly constrain floating PCB','thermal relief is a local template, not complete heat spreader'],'brep_valid':all(x.val().isValid() for x in [plate]+rails)}
assert meta['brep_valid'];assert not doc.audit().has_errors
(OUT/'dimensions.json').write_text(json.dumps(meta,indent=2))
fig,(ax,side)=plt.subplots(1,2,figsize=(12,6))
ax.add_patch(Rectangle((-17.5,-5),35,40,facecolor='#c3d2dc'));ax.add_patch(Rectangle((-10.5,0),21,35,facecolor='white',edgecolor='#345'));ax.add_patch(Rectangle((-7.5,0),15,15,fill=False,edgecolor='#aa5533',linestyle='--'));ax.axhline(0,color='#344');ax.text(0,-3,'Socket mating face',ha='center');ax.text(0,23,'21 mm clear slot',ha='center');ax.set(xlim=(-21,21),ylim=(-7,40),xlabel='Local X mm',ylabel='Outward Y mm',title='Bottom plate local coupon');ax.set_aspect('equal')
side.add_patch(Rectangle((0,-10.55),15,8,fill=False,edgecolor='#aa5533',linestyle='--'));side.plot([0,20,35],[-11.3,-11.3,-13.3],color='#345',linewidth=3);side.axhline(-10.55,color='#999',linestyle=':');side.text(17,-5,'Trial 8 mm body');side.text(5,-12.5,'0.75 mm guide gap');side.set(xlim=(-5,40),ylim=(-15,0),xlabel='Outward Y mm',ylabel='Z relative to PCB front mm',title='Feed rails and assumed flush datum');side.set_aspect('equal');fig.suptitle('PHBox underside dongle bay - prototype fit coupon');fig.tight_layout();fig.savefig(OUT/'bay-reference.png',dpi=160);fig.savefig(OUT/'bay-reference.svg');plt.close(fig)
(OUT/'README.md').write_text("""# Local underside dongle bay fit coupon

This is a printable/machinable local interface sample, not a released full case. The 21 mm slot accommodates the 15 mm published MagicBoots body width with planning clearance. Its nominal 8 mm body is assumed centred on the USB mating axis; verify this assumption before setting the flush case datum.

STEP contains the bottom plate coupon and two feed rails. STL exports are separate. DXF is the open U-shaped plate outline. The rails descend 2 mm over the final 15 mm of the outward mouth; insertion proceeds inward uphill. Their top is 0.75 mm below the assumed installed body, allowing trial float clearance. Keep the guides independent of the floating PCB. A local bottom heat-spreader relief needs at least 23 mm width, electrically insulated edges, and component-aware final contours.

Nominal local-to-KiCad: X_KiCad=192+X, Y_KiCad=32.5-Y. The case needs room beyond the PCB edge; this coupon deliberately extends 35 mm beyond the mating face. Reserve 50 mm exterior insertion sweep. Brook FGC2 is not the target. Full foam, carrier, gasket hard stops and socket insertion-force support remain to be designed.
""",encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>PHBox dongle bay</title><h1>Prototype underside dongle bay</h1><p>Local fit coupon; full enclosure dimensions remain provisional.</p><img style="max-width:100%" src="bay-reference.svg"><p><a href="README.md">Dimensions and fit limits</a></p>')
print(json.dumps(meta))
