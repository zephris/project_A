from pathlib import Path
import sys,re,json
sys.path.insert(0,'stage2_work/display_2026-10-05');from revise_display import forms
for _,_,s in forms(Path('Flatbox-rev8.kicad_pcb').read_text()):
 if re.match(r'\(footprint\s',s):
  p=dict(re.findall(r'\(property\s+"([^"]+)"\s+"((?:\\.|[^"\\])*)"',s))
  if p.get('Reference') in ['F1','Y1','L1','U3']:print(json.dumps(p))
