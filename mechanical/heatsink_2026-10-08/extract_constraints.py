"""Read current PCB geometry with KiCad Python. Does not modify the board."""
from pathlib import Path
import hashlib
import json
import pcbnew

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
path = ROOT / 'Flatbox-rev8.kicad_pcb'
board = pcbnew.LoadBoard(str(path))
mm = pcbnew.ToMM
items = []
for f in board.GetFootprints():
    p = f.GetPosition()
    bb = f.GetBoundingBox(False, False)
    models = []
    for m in f.Models():
        models.append({'path': m.m_Filename,
                       'offset': [m.m_Offset.x, m.m_Offset.y, m.m_Offset.z],
                       'rotation': [m.m_Rotation.x, m.m_Rotation.y, m.m_Rotation.z],
                       'scale': [m.m_Scale.x, m.m_Scale.y, m.m_Scale.z]})
    items.append({'ref': f.GetReference(), 'value': f.GetValue(),
                  'pcb_xy': [mm(p.x), mm(p.y)],
                  'rotation_deg': f.GetOrientationDegrees(),
                  'side': 'B' if f.IsFlipped() else 'F',
                  'bbox_xy': [mm(bb.GetX()), mm(bb.GetY()), mm(bb.GetWidth()), mm(bb.GetHeight())],
                  'models': models,
                  'pads': [{'number': p.GetNumber(), 'net': p.GetNetname(),
                            'pcb_xy': [mm(p.GetPosition().x), mm(p.GetPosition().y)],
                            'drill_mm': [mm(p.GetDrillSize().x), mm(p.GetDrillSize().y)]}
                           for p in f.Pads()]})
data = {'source': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'kicad_version': pcbnew.Version(), 'pcb_thickness_mm': mm(board.GetDesignSettings().GetBoardThickness()),
        'mechanical_frame': 'X=KiCad X; Y=-KiCad Y; PCB front seating plane Z=0',
        'footprints': items}
(OUT / 'constraints.json').write_text(json.dumps(data, indent=2) + '\n')
print('Extracted', len(items), 'footprints;', data['sha256'])
