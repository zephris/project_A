"""Read-only KiCad 10 geometry extraction. Run with KiCad's Python."""
from pathlib import Path
import json, hashlib
import pcbnew
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'pcb_geometry'
OUT.mkdir(exist_ok=True)
path=ROOT/'Flatbox-rev8.kicad_pcb'
b=pcbnew.LoadBoard(str(path))
mm=pcbnew.ToMM
def point(p): return [mm(p.x),mm(p.y)]
fps=[]; holes=[]
for f in b.GetFootprints():
    fps.append({'ref':f.GetReference(),'value':f.GetValue(),'footprint':str(f.GetFPID().GetLibItemName()),
                'pcb_xy':point(f.GetPosition()),'rotation_deg':f.GetOrientationDegrees(),
                'side':'B' if f.IsFlipped() else 'F'})
    for p in f.Pads():
        d=p.GetDrillSize()
        if d.x<=0 or d.y<=0: continue
        holes.append({'id':f'{f.GetReference()}:{p.GetNumber()}:{len(holes)+1}',
                      'ref':f.GetReference(),'pad':p.GetNumber(),'pcb_xy':point(p.GetPosition()),
                      'drill_xy_mm':point(d),'rotation_deg':p.GetOrientationDegrees(),
                      'plating':'NPTH' if p.GetAttribute()==pcbnew.PAD_ATTRIB_NPTH else 'PTH',
                      'kind':'round' if d.x==d.y else 'slot'})
for t in b.GetTracks():
    if isinstance(t,pcbnew.PCB_VIA):
        d=mm(t.GetDrillValue())
        holes.append({'id':f'VIA:{len(holes)+1}','ref':'VIA','pad':'','pcb_xy':point(t.GetPosition()),
                      'drill_xy_mm':[d,d],'rotation_deg':0,'plating':'PTH','kind':'round'})
out={'source':path.name,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
     'kicad_version':pcbnew.Version(),'thickness_mm':mm(b.GetDesignSettings().GetBoardThickness()),
     'footprints':fps,'holes':holes}
(OUT/'native-geometry.json').write_text(json.dumps(out,indent=2)+'\n')
from collections import Counter
print('KiCad',out['kicad_version'],'footprints',len(fps),'holes',len(holes),dict(Counter((h['plating'],h['kind']) for h in holes)))
