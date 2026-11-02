from pathlib import Path
import json,csv,hashlib,collections,difflib,zipfile
root=Path(__file__).resolve().parent.parent
pkg=root/'manufacturing/PHBox_2026-10-06_DFM_resolved'
drc=json.loads((root/'manufacturing/demo-review-drc-2026-10-07.json').read_text())
print('DRC:',dict(collections.Counter(v['type'] for v in drc['violations'])), 'unconnected:',len(drc.get('unconnected_items',[])))
for name in ['Flatbox-rev8.kicad_pcb','Flatbox-rev8.kicad_sch']:
 a=(pkg/'source'/name).read_text();b=(root/name).read_text()
 print(name,'matches exported source ignoring newline:',a==b)
 if a!=b: print('\n'.join(list(difflib.unified_diff(a.splitlines(),b.splitlines()))[:45]))
rows=list(csv.DictReader((pkg/'assembly/BOM-JLCPCB.csv').open()))
cpl=list(csv.DictReader((pkg/'assembly/CPL-JLCDFM.csv').open()))
refs={r.strip() for row in rows for r in row['Designator'].split(',')}
placed={row['Designator'].strip() for row in cpl}
print('BOM groups:',len(rows),'parts:',len(refs),'CPL:',len(cpl),'C41 BOM:', 'C41' in refs,'C41 CPL:','C41' in placed)
print('CPL without BOM:',sorted(placed-refs),'BOM without CPL:',sorted(refs-placed))
hashes=json.loads((pkg/'validation/final-file-hashes.json').read_text())
bad=[name for name,digest in hashes.items() if hashlib.sha256((pkg/name).read_bytes()).hexdigest()!=digest]
print('File hashes verified:',len(hashes),'mismatches:',bad)
import sys,re
sys.path.insert(0,str(root/'stage2_work/display_2026-10-05'))
from revise_display import forms
def without_models(text):
    edits=[]
    for a,b,f in forms(text):
        if f.startswith('(footprint'):
            for x,y,g in forms(f):
                if g.startswith('(model '): edits.append((a+x,a+y))
    for a,b in reversed(edits): text=text[:a]+text[b:]
    return re.sub(r'\s+',' ',text)
print('PCB equal after stripping 3D models/whitespace:',without_models((pkg/'source/Flatbox-rev8.kicad_pcb').read_text())==without_models((root/'Flatbox-rev8.kicad_pcb').read_text()))
z=zipfile.ZipFile(pkg/'upload/PHBox-DFM-resolved-Gerbers.zip')
print('Upload ZIP:',z.namelist())
