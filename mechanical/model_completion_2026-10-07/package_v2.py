from pathlib import Path
import zipfile,json
r=Path.cwd();o=r/'mechanical/model_completion_2026-10-07'
files=[o/n for n in ['README.md','PHBox-ChocV2-assembly.step','PHBox-ChocV2-single-compound.step','choc-v2-README.md','Choc-V2-datasheet.pdf','choc-v2-footprint-audit.json','choc-v2-validation.json','downloads.json','board-choc-v2-isometric.png','final-choc-v2-geometry-validation.json']]
files += [r/'3dmodels'/n for n in ['SW_Kailh_Choc_V2_red.step','AOTA_B201610S3R3_101_T_EasyEDA.step','SK6805_EC15_EasyEDA.step','ESDA7P120_1U1M_ST_reference.step','ECMF2_40A100N6_ST_reference.step']]
files += list(o.glob('*maximum_body_envelope.step'))
if not all(p.exists() for p in files):print('Waiting for final geometry validation');raise SystemExit(2)
with zipfile.ZipFile(r/'mechanical/PHBox_3D_models_ChocV2_2026-10-07.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,('3dmodels/' if p.parent.name=='3dmodels' else '')+p.name)
print('Packaged current V2 CAD, validation, models and attribution.')
