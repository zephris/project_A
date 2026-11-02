"""Measure the revised PCB, including pads and model placements, for CAD."""
from pathlib import Path
import hashlib,json
import pcbnew as p
HERE=Path(__file__).resolve().parent
path=HERE/'pcb/PHBox-ergonomic.kicad_pcb'
b=p.LoadBoard(str(path));mm=p.ToMM
items=[]
for f in b.GetFootprints():
    q=f.GetPosition();bb=f.GetBoundingBox(False,False)
    items.append({'ref':f.GetReference(),'value':f.GetValue(),'pcb_xy':[mm(q.x),mm(q.y)],'rotation_deg':f.GetOrientationDegrees(),'side':'B' if f.IsFlipped() else 'F',
      'bbox_xy':[mm(v) for v in (bb.GetX(),bb.GetY(),bb.GetWidth(),bb.GetHeight())],
      'models':[{'path':m.m_Filename,'offset':[m.m_Offset.x,m.m_Offset.y,m.m_Offset.z],'rotation':[m.m_Rotation.x,m.m_Rotation.y,m.m_Rotation.z],'scale':[m.m_Scale.x,m.m_Scale.y,m.m_Scale.z]} for m in f.Models()],
      'pads':[{'number':q.GetNumber(),'net':q.GetNetname(),'pcb_xy':[mm(q.GetPosition().x),mm(q.GetPosition().y)],'drill_mm':[mm(q.GetDrillSize().x),mm(q.GetDrillSize().y)]} for q in f.Pads()]})
(HERE/'constraints.json').write_text(json.dumps({'source':str(path.relative_to(HERE)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'footprints':items},indent=2)+'\n')
print('Measured',len(items),'footprints')
