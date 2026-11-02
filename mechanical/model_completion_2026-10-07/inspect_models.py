from pathlib import Path
import sys,json
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent
sys.path.insert(0,str(root/'stage2_work/enclosure_cad_dependencies'))
import cadquery as cq
result={}
for p in out.glob('*.step'):
 wp=cq.importers.importStep(str(p));sh=wp.val();b=sh.BoundingBox()
 result[p.name]={'valid':sh.isValid(),'solids':len(sh.Solids()),'bounds_mm':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]}
 print(p.name,result[p.name],flush=True)
(out/'raw-model-validation.json').write_text(json.dumps(result,indent=2))
