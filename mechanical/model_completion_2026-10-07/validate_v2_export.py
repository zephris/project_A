from pathlib import Path
import sys,json,struct
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent
sys.path.insert(0,str(root/'stage2_work/enclosure_cad_dependencies'))
import cadquery as cq
wp=cq.importers.importStep(str(out/'PHBox-ChocV2-assembly.step'));solids=wp.solids().vals();sh=cq.Compound.makeCompound(solids);bb=sh.BoundingBox()
print('Imported assembly',len(solids),'solids',flush=True)
assert sh.isValid()
cq.exporters.export(sh,str(out/'PHBox-ChocV2-single-compound.step'))
print('Exported single compound',flush=True)
again=cq.importers.importStep(str(out/'PHBox-ChocV2-single-compound.step')).val();assert again.isValid() and len(again.Solids())==len(solids)
report={'assembly_valid':True,'compound_roundtrip_valid':True,'solid_count':len(solids),'bounds_mm':[bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax],'models':{}}
for name in ['SW_Kailh_Choc_V2_red','AOTA_B201610S3R3_101_T_EasyEDA','SK6805_EC15_EasyEDA','ESDA7P120_1U1M_ST_reference','ECMF2_40A100N6_ST_reference']:
 obj=cq.importers.importStep(str(root/'3dmodels'/(name+'.step'))).val();b=obj.BoundingBox()
 report['models'][name]={'valid':obj.isValid(),'bounds_mm':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax],'solid_bounds_mm':[[q.BoundingBox().xmin,q.BoundingBox().xmax,q.BoundingBox().ymin,q.BoundingBox().ymax,q.BoundingBox().zmin,q.BoundingBox().zmax] for q in obj.Solids()]}
# Original STL references remain STL; no lossy mesh-to-STEP claim.
for name in ['Buttoncap.stl','ButtoncapBig.stl']:
 data=(out/name).read_bytes();n=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*n
 points=[struct.unpack_from('<3f',data,84+50*i+12+12*j) for i in range(n) for j in range(3)]
 report[name]={'triangles':n,'bounds_mm':[[min(p[j] for p in points),max(p[j] for p in points)] for j in range(3)],'unpositioned_reference':True}
(out/'final-choc-v2-geometry-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='models'},indent=2),flush=True)
