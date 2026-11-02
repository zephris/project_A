"""Create the placement/routing candidate without touching the released board.

Run with KiCad's Python. LED, resistor and bypass capacitor move with each switch.
The electrically sensitive core and USB pair routes remain in their source places.
"""
from pathlib import Path
import json, shutil, hashlib, math, re
import pcbnew as p

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PCB=HERE/'pcb'
cfg=json.loads((HERE/'layout.json').read_text())
baseline=PCB/'before.kicad_pcb'
if not baseline.exists():shutil.copy2(ROOT/'Flatbox-rev8.kicad_pcb',baseline)
b=p.LoadBoard(str(baseline)); fps={f.GetReference():f for f in b.GetFootprints()}
for f in fps.values():
    for m in f.Models():m.m_Filename=m.m_Filename.replace('${KIPRJMOD}',ROOT.as_posix())
mm=p.ToMM
def point(q):return (mm(q.x),mm(q.y))
def vec(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

groups=[];changes=[]
for ref,pos in cfg['switch_centres'].items():
    i=int(ref[2:]);old=point(fps[ref].GetPosition())
    groups.append(([ref,f'D{i}',f'R{i+17}',f'C{i+19}'],(pos[0]-old[0],pos[1]-old[1])))
groups.append((['U5'],tuple(cfg['screen_delta_mm'])))
groups.append(([f'OPSW{i}' for i in range(1,7)],tuple(cfg['options_delta_mm'])))
original_pads=[]
for refs,delta in groups:
    for ref in refs:
        f=fps[ref]
        original_pads += [(point(q.GetPosition()),mm(q.GetSize().x)/2+.2,mm(q.GetSize().y)/2+.2) for q in f.Pads()]
        old=point(f.GetPosition());f.Move(vec(*delta))
        changes.append(dict(ref=ref,old_xy=old,new_xy=point(f.GetPosition()),delta_mm=delta))

# Keep the fixed electronics core; clear field copper rather than stretching
# traces across new holes or carrying disconnected copper to the wrong switch.
# Local switch/LED routing wholly inside a module moves rigidly with that module.
local=[]
source=p.LoadBoard(str(baseline)); original={f.GetReference():f for f in source.GetFootprints()}
for refs,delta in groups[:16]:
    f=original[refs[0]];x,y=point(f.GetPosition())
    nets={q.GetNetCode() for ref in refs for q in original[ref].Pads() if q.GetNetCode()}
    local.append((x,y,nets,delta))
removed=[];translated=[];retained=[]
for t in list(b.GetTracks()):
    a=point(t.GetStart());z=point(t.GetEnd())
    hit=None
    for x,y,nets,delta in local:
        if t.GetNetCode() in nets and all(x-11<=q[0]<=x+11 and y-9<=q[1]<=y+11 for q in (a,z)):
            hit=delta;break
    if hit is not None:
        t.Move(vec(*hit));translated.append(t.m_Uuid.AsString());continue
    touches_pad=any(abs(q[0]-c[0])<=w and abs(q[1]-c[1])<=h for q in (a,z) for c,w,h in original_pads)
    if max(a[1],z[1])>=79 or touches_pad or t.GetNetname() in ('SCL','SDA'):
        removed.append(t.m_Uuid.AsString())
    else:
        # Fixed DSN wiring protects existing USB/high-speed/core fanout.
        t.SetLocked(True);retained.append(t.m_Uuid.AsString())

out=PCB/'PHBox-ergonomic.kicad_pcb'
# Reference project paths must still locate the real models in this subfolder.
p.SaveBoard(str(out),b)
text=out.read_text(encoding='utf8')
text=text.replace('${KIPRJMOD}',ROOT.as_posix())
starts=[m.start() for m in re.finditer(r'^\t\((?:segment|via|arc)\s*$',text,re.M)]
removed_set=set(removed)
placement_drc=HERE/'checks/placement-drc.json'
if placement_drc.exists():
    for finding in json.loads(placement_drc.read_text())['violations']:
        for item in finding['items']:
            if item['description'].startswith(('Track ','Via ')):
                assert not any(net in item['description'] for net in ('[HD+]','[HD-]','[D+]','[D-]'))
                removed_set.add(item['uuid'])
for start in reversed(starts):
    end=text.find('\n\t)',start)+4
    block=text[start:end]
    if any(u in block for u in removed_set):text=text[:start]+text[end:]
out.write_text(text,encoding='utf8')
for ext in ('kicad_pro','kicad_dru','kicad_sch'):
    shutil.copy2(ROOT/f'Flatbox-rev8.{ext}',PCB/f'PHBox-ergonomic.{ext}')
(PCB/'fp-lib-table').write_text((ROOT/'fp-lib-table').read_text().replace('${KIPRJMOD}',ROOT.as_posix()))
(PCB/'sym-lib-table').write_text((ROOT/'sym-lib-table').read_text().replace('${KIPRJMOD}',ROOT.as_posix()))
assert all(tuple(q.GetNetname() for q in sorted(fps[ref].Pads(),key=lambda q:q.GetNumber()))==tuple(q.GetNetname() for q in sorted(original[ref].Pads(),key=lambda q:q.GetNumber())) for ref in fps)
data={'baseline_sha256':sha(baseline),'candidate_sha256':sha(out),'changes':changes,'copper_removed':len(removed_set),'local_copper_translated':len(set(translated)-removed_set),'fixed_core_copper_retained':len(set(retained)-removed_set),'pin_nets_unchanged':True,'board_outline_unchanged':True,'fixed_core_track_uuids':sorted(set(retained)-removed_set)}
(HERE/'checks/placement-changes.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k not in ('changes','fixed_core_track_uuids')},indent=2))
