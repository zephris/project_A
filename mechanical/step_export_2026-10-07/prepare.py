from pathlib import Path
import re,shutil,json,hashlib
import pcbnew
root=Path(__file__).resolve().parents[2]; out=Path(__file__).parent
pcb=root/'Flatbox-rev8.kicad_pcb'; before=pcb.read_text(); shutil.copy2(pcb,out/'board-before-model-fix.kicad_pcb')
library=Path('D:/Program Files/share/kicad/3dmodels')
names=['C_0402_1005Metric.step','C_0603_1608Metric.step','CP_EIA-3528-21_Kemet-B.step']
for n in names:
    folder='Capacitor_Tantalum_SMD.3dshapes' if n.startswith('CP_') else 'Capacitor_SMD.3dshapes'
    shutil.copy2(library/folder/n,root/'3dmodels'/n)
old='${KICAD8_3RD_PARTY}/3dmodels/com_github_CDFER_JLCPCB-Kicad-Library/JLCPCB.3dshapes/C_0402.step'
new='${KIPRJMOD}/3dmodels/C_0402_1005Metric.step'
text=before.replace(old,new).replace('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0402_1005Metric.step',new).replace('${KICAD10_3DMODEL_DIR}/Capacitor_Tantalum_SMD.3dshapes/CP_EIA-3528-21_Kemet-B.step','${KIPRJMOD}/3dmodels/CP_EIA-3528-21_Kemet-B.step')
# Insert C41 model into its existing footprint without rewriting any other data.
start=text.index('(footprint "Capacitor_SMD:C_0603_1608Metric"')
depth=0;quoted=False;escaped=False;end=None
for i in range(start,len(text)):
    c=text[i]
    if escaped: escaped=False;continue
    if c=='\\' and quoted:escaped=True;continue
    if c=='"':quoted=not quoted
    if not quoted:
        if c=='(':depth+=1
        if c==')':
            depth-=1
            if depth==0:end=i;break
block=text[start:end+1];assert '(property "Reference" "C41"' in block and '(model ' not in block
model='\n\t\t(model "${KIPRJMOD}/3dmodels/C_0603_1608Metric.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))\n\t'
text=text[:end]+model+text[end:];pcb.write_text(text,encoding='utf-8')
for n in ['Samsung_1005_Tolerance005','Samsung_1005_Tolerance015']:
    p=root/'PHBox.pretty'/f'{n}.kicad_mod';t=p.read_text();p.write_text(t.replace(old,new).replace('${KICAD10_3DMODEL_DIR}/Capacitor_SMD.3dshapes/C_0402_1005Metric.step',new),encoding='utf-8')
# Geometry invariant is exact after removing only model clauses.
def strip_models(t):
    return re.sub(r'\s*\(model\s+"[^"]*"\s*\(offset\s*\(xyz[^)]*\)\s*\)\s*\(scale\s*\(xyz[^)]*\)\s*\)\s*\(rotate\s*\(xyz[^)]*\)\s*\)\s*\)','',t)
assert strip_models(before)==strip_models(text),'Non-model data changed'
b=pcbnew.LoadBoard(str(pcb));caps=[];audit=[]
for f in b.GetFootprints():
    paths=[]
    for m in f.Models():
        p=m.m_Filename.replace('${KIPRJMOD}',str(root)).replace('${KICAD10_3DMODEL_DIR}',str(library)).replace('${KICAD9_3DMODEL_DIR}',str(library)).replace('${KICAD7_3DMODEL_DIR}',str(library))
        paths.append({'reference':m.m_Filename,'exists':Path(p).is_file(),'resolved':p})
    audit.append({'ref':f.GetReference(),'models':paths})
    if f.GetReference().startswith('C'):caps.append({'ref':f.GetReference(),'models':paths})
assert len(caps)==44 and all(c['models'] and all(p['exists'] for p in c['models']) for c in caps)
(out/'model-audit.json').write_text(json.dumps({'capacitors':caps,'all_footprints':audit,'non_model_board_data_unchanged':True,'legacy_capacitor_paths_replaced':before.count(old)},indent=2))
print('All 44 capacitors now have existing portable models; non-model board data unchanged.')
