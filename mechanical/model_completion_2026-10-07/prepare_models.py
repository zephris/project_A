from pathlib import Path
import sys,json,shutil
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent;models=root/'3dmodels'
sys.path.insert(0,str(root/'stage2_work/enclosure_cad_dependencies'))
import cadquery as cq
report={}
for src,dest,dz in [('L1-library.step','AOTA_B201610S3R3_101_T_EasyEDA.step',.05),('LED-library.step','SK6805_EC15_EasyEDA.step',.02)]:
 sh=cq.importers.importStep(str(out/src)).val().translate((0,0,dz));cq.exporters.export(sh,str(models/dest));b=sh.BoundingBox()
 report[dest]={'source':src,'seating_translation_z_mm':dz,'valid':sh.isValid(),'bounds_mm':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]}
shutil.copy2(out/'SW_Kailh_Choc_V1.step',models/'SW_Kailh_Choc_V1.step')
# Simplified manufacturer-drawing-derived package references, not vendor CAD.
# Body nominal dimensions and maximum body envelopes are separate files.
def box(x,y,h,z=0):return cq.Workplane('XY').box(x,y,h,centered=(True,True,False)).translate((0,0,z)).val()
for name,body,pads,maxdims in [
 ('ESDA7P120_1U1M_ST_reference',(1.60,1.00,.55),[(x,0,.35,.80) for x in [-.525,.525]],(1.65,1.05,.60)),
 ('ECMF2_40A100N6_ST_reference',(1.35,1.40,.45),[(x,y,.50,.20) for x in [-.425,.425] for y in [-.4,0,.4]],(1.40,1.45,.50))]:
 x,y,h=body;parts=[box(x,y,h-.02,.02)]
 parts += [box(dx,dy,.127).translate((px,py,0)) for px,py,dx,dy in pads]
 # Union makes a compact valid reference; it does not claim lead-frame fidelity.
 sh=parts[0].fuse(*parts[1:]);cq.exporters.export(sh,str(models/(name+'.step')))
 env=box(*maxdims);cq.exporters.export(env,str(out/(name+'_maximum_body_envelope.step')))
 report[name]={'provenance':'project-generated from ST DS14419 Rev4 or DS13913 Rev4; simplified reference only','nominal_body_xyz_mm':body,'maximum_body_xyz_mm':maxdims,'valid':sh.isValid()}
(out/'prepared-model-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
