from pathlib import Path
import sys,re,collections
sys.path.insert(0,'stage2_work/display_2026-10-05');from revise_display import forms
sets=collections.defaultdict(list)
for _,_,s in forms(Path('Flatbox-rev8.kicad_pcb').read_text()):
 if not re.match(r'\(footprint\s',s):continue
 p=dict(re.findall(r'\(property\s+"([^"]+)"\s+"((?:\\.|[^"\\])*)"',s));ref=p.get('Reference','')
 if re.fullmatch(r'[RC]\d+',ref):sets[(p.get('Value'),p.get('MPN'),p.get('LCSC'),p.get('Datasheet'))].append(ref)
for k,v in sets.items():print(k,','.join(v))
