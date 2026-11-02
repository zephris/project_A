from pathlib import Path
import sys,json
root=Path(__file__).resolve().parents[2]; out=Path(__file__).parent
sys.path.insert(0,str(root/'stage2_work/enclosure_cad_dependencies'))
import cadquery as cq
report={}
for name in ['PHBox-assembly','PHBox-fused']:
    wp=cq.importers.importStep(str(out/f'{name}.step'))
    solids=wp.solids().vals(); shape=cq.Compound.makeCompound(solids); bb=shape.BoundingBox()
    report[name]={'solids':len(solids),'valid':shape.isValid(),'bbox_mm':{'xmin':bb.xmin,'xmax':bb.xmax,'ymin':bb.ymin,'ymax':bb.ymax,'zmin':bb.zmin,'zmax':bb.zmax},'volume_mm3':sum(s.Volume() for s in solids)}
    if name=='PHBox-assembly':
        cq.exporters.export(shape,str(out/'PHBox-single-compound.step'))
        reloaded=cq.importers.importStep(str(out/'PHBox-single-compound.step')).val()
        report['PHBox-single-compound']={'valid':reloaded.isValid(),'solids':len(reloaded.Solids()),'volume_mm3':sum(s.Volume() for s in reloaded.Solids())}
        assert reloaded.isValid() and len(reloaded.Solids())==len(solids)
for name in ['C_0402_1005Metric','C_0603_1608Metric','CP_EIA-3528-21_Kemet-B']:
    shape=cq.importers.importStep(str(root/'3dmodels'/f'{name}.step')).val(); bb=shape.BoundingBox()
    report[name]={'valid':shape.isValid(),'x_mm':bb.xlen,'y_mm':bb.ylen,'zmin_mm':bb.zmin,'zmax_mm':bb.zmax}
(out/'geometry-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
