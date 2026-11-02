from pathlib import Path
import sys,re,shutil,json
import pcbnew
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent
sys.path.insert(0,str(root/'stage2_work/display_2026-10-05'))
from revise_display import forms
board=root/'Flatbox-rev8.kicad_pcb';text=board.read_text();before=text
backup=out/'before';backup.mkdir(exist_ok=True)
shutil.copy2(board,backup/board.name)
files={'L1':'AOTA_B201610S3R3_101_T_EasyEDA.step','D21':'ESDA7P120_1U1M_ST_reference.step','U4':'ECMF2_40A100N6_ST_reference.step'}
files.update({f'D{i}':'SK6805_EC15_EasyEDA.step' for i in range(1,21)})
files.update({f'SW{i}':'SW_Kailh_Choc_V1.step' for i in range(1,17)})
def model(name):return '\n\t\t(model "${KIPRJMOD}/3dmodels/'+name+'" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))\n'
def strip(s):return re.sub(r'\s*\(model\s+"[^"]*"\s*\(offset\s*\(xyz[^)]*\)\s*\)\s*\(scale\s*\(xyz[^)]*\)\s*\)\s*\(rotate\s*\(xyz[^)]*\)\s*\)\s*\)','',s)
edits=[];seen=[]
for a,b,f in forms(text):
 if not f.startswith('(footprint '):continue
 ref=re.search(r'\(property "Reference" "([^"]+)"',f).group(1)
 if ref not in files:continue
 g=f if ref.startswith('SW') else strip(f)
 g=g[:-1]+model(files[ref])+')';edits.append((a,b,g));seen.append(ref)
assert set(seen)==set(files)
for a,b,g in reversed(edits):text=text[:a]+g+text[b:]
assert ''.join(strip(before).split())==''.join(strip(text).split()),'Non-model data changed'
board.write_text(text,encoding='utf-8')
libfiles={root/'lib.pretty/L_pol_2016.kicad_mod':files['L1'],root/'PHBox.pretty/ESDA7P120_1U1M_ST_Recommended.kicad_mod':files['D21'],root/'PHBox.pretty/ECMF2-40A100N6.kicad_mod':files['U4'],root/'PHBox_Repair.pretty/LED_SK6805_EC15_Optical.kicad_mod':files['D1'],root/'PHBox_Repair.pretty/SW_Hotswap_Kailh_Choc_V1V2_3D_Optical.kicad_mod':files['SW1']}
for p,n in libfiles.items():
 shutil.copy2(p,backup/p.name);s=p.read_text();g=s if n=='SW_Kailh_Choc_V1.step' else strip(s);p.write_text(g.rstrip()[:-1]+model(n)+')\n',encoding='utf-8')
b=pcbnew.LoadBoard(str(board));audit=[]
for f in b.GetFootprints():
 row={'reference':f.GetReference(),'models':[]}
 for m in f.Models():
  p=m.m_Filename.replace('${KIPRJMOD}',str(root)).replace('${KICAD10_3DMODEL_DIR}','D:/Program Files/share/kicad/3dmodels').replace('${KICAD9_3DMODEL_DIR}','D:/Program Files/share/kicad/3dmodels')
  row['models'].append({'path':m.m_Filename,'exists':Path(p).is_file()})
 audit.append(row)
assert all(all(m['exists'] for m in r['models']) for r in audit)
assert all(r['models'] or r['reference'].startswith('H') for r in audit)
(out/'attachment-validation.json').write_text(json.dumps({'non_model_board_data_unchanged':True,'added_or_replaced_references':seen,'footprints':audit},indent=2));print('Attached models at',len(seen),'references. All model files exist. Only H1-H12 intentionally have no model.')
