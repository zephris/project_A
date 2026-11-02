from pathlib import Path
import sys,re,json,collections
r=Path.cwd();sys.path.insert(0,str(r/'stage2_work/display_2026-10-05'));from revise_display import forms
rows=[]
for a,b,f in forms((r/'Flatbox-rev8.kicad_sch').read_text()):
 if not re.match(r'\(symbol\s',f):continue
 props=dict(re.findall(r'\(property\s+"([^"]+)"\s+"((?:\\.|[^"\\])*)"',f))
 ref=props.get('Reference','');val=props.get('Value','')
 if ref.startswith('#'):continue
 rows.append({'reference':ref,'value':val,'lib_id':re.search(r'\(lib_id "([^"]+)"',f).group(1),'simulation_fields':{k:v for k,v in props.items() if k.startswith(('Sim.','Spice_'))}})
print('Components',len(rows))
for value,items in sorted(collections.defaultdict(list).items()):pass
for value in sorted({p['value'] for p in rows}):print(value,':',','.join(p['reference'] for p in rows if p['value']==value))
(r/'spice/model-audit-inventory-2026-10-07.json').write_text(json.dumps(rows,indent=2))

