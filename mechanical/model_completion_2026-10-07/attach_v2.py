from pathlib import Path
import re,json,shutil,sys
import pcbnew
r=Path.cwd();o=r/'mechanical/model_completion_2026-10-07'
shutil.copy2(o/'SW_Kailh_Choc_V2_red.step',r/'3dmodels/SW_Kailh_Choc_V2_red.step')
paths=[r/'Flatbox-rev8.kicad_pcb',r/'PHBox_Repair.pretty/SW_Hotswap_Kailh_Choc_V1V2_3D_Optical.kicad_mod']
pattern=r'\(model "\$\{KIPRJMOD\}/3dmodels/SW_Kailh_Choc_V1.step"\s*\(offset \(xyz 0 0 0\)\)\s*\(scale \(xyz 1 1 1\)\)\s*\(rotate \(xyz 0 0 0\)\)\)'
replacement='(model "${KIPRJMOD}/3dmodels/SW_Kailh_Choc_V2_red.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 180)))'
for p in paths:
 s=p.read_text();t,n=re.subn(pattern,replacement,s);assert n==(16 if p.suffix=='.kicad_pcb' else 1),(p,n);p.write_text(t,encoding='utf-8')
b=pcbnew.LoadBoard(str(paths[0]));audit=[]
for f in b.GetFootprints():
 if not re.fullmatch(r'SW\d+',f.GetReference()):continue
 holes=[(round(p.GetPos0().x/1e6,3),round(p.GetPos0().y/1e6,3),round(p.GetDrillSize().x/1e6,3)) for p in f.Pads() if p.GetDrillSize().x]
 assert (0,0,5.05) in holes and (-5,5.15,1.6) in holes
 audit.append({'reference':f.GetReference(),'holes_mm':holes})
assert len(audit)==16
(o/'choc-v2-footprint-audit.json').write_text(json.dumps({'switches':audit,'model_rotation_z_deg':180,'board_change':'3D model clauses only','caution':'Community CAD stabilizer pin location is approximate; use OEM drawing for drill and retention dimensions.'},indent=2))
print('Replaced 16 switch models and library model; all 16 dual-compatible drill patterns verified.')
