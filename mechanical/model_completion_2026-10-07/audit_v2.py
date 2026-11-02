from pathlib import Path
import json,pcbnew,re
r=Path.cwd();o=r/'mechanical/model_completion_2026-10-07';b=pcbnew.LoadBoard(str(r/'Flatbox-rev8.kicad_pcb'));audit=[]
for f in b.GetFootprints():
 if f.GetReference() not in {f'SW{i}' for i in range(1,17)}:continue
 assert f.GetOrientationDegrees()==0
 holes=[(round(p.GetFPRelativePosition().x/1e6,3),round(p.GetFPRelativePosition().y/1e6,3),round(p.GetDrillSize().x/1e6,3)) for p in f.Pads() if p.GetDrillSize().x]
 assert (0,0,5.05) in holes and (-5,5.15,1.6) in holes
 audit.append({'reference':f.GetReference(),'holes_mm':holes})
assert len(audit)==16
(o/'choc-v2-footprint-audit.json').write_text(json.dumps({'switches':audit,'model_rotation_z_deg':180,'caution':'Community model support-pin position approximate; OEM drawing governs manufacturing geometry.'},indent=2))
# Confirm all changes since the preserved original board are model clauses only.
sys_path=r/'stage2_work/display_2026-10-05'
import sys
sys.path.insert(0,str(sys_path));from revise_display import forms
strip=lambda s: re.sub(r'\s*\(model\s+"[^"]*"\s*\(offset\s*\(xyz[^)]*\)\s*\)\s*\(scale\s*\(xyz[^)]*\)\s*\)\s*\(rotate\s*\(xyz[^)]*\)\s*\)\s*\)','',s)
assert ''.join(strip((o/'before/Flatbox-rev8.kicad_pcb').read_text()).split())==''.join(strip((r/'Flatbox-rev8.kicad_pcb').read_text()).split())
print('16 V2 drill patterns confirmed; source board changes are exclusively 3D model clauses.')
s=(o/'validate_export.py').read_text().replace('PHBox-assembly.step','PHBox-ChocV2-assembly.step').replace('PHBox-single-compound.step','PHBox-ChocV2-single-compound.step').replace('SW_Kailh_Choc_V1','SW_Kailh_Choc_V2_red').replace('final-geometry-validation.json','final-choc-v2-geometry-validation.json')
(o/'validate_v2_export.py').write_text(s)

