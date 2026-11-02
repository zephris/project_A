"""Pin/placement/preserved-route audit, independent of the autorouter's judgement."""
from pathlib import Path
import json,hashlib,collections,math
import pcbnew as p
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
before=p.LoadBoard(str(HERE/'pcb/before.kicad_pcb'))
after=p.LoadBoard(str(HERE/'pcb/PHBox-ergonomic.kicad_pcb'))
refs={f.GetReference():f for f in before.GetFootprints()}
now={f.GetReference():f for f in after.GetFootprints()}
cfg=json.loads((HERE/'layout.json').read_text())
change=json.loads((HERE/'checks/placement-changes.json').read_text())
def pinmap(f):return sorted((q.GetNumber(),q.GetNetname()) for q in f.Pads())
assert refs.keys()==now.keys() and all(pinmap(refs[r])==pinmap(now[r]) for r in refs)
errors={r:math.hypot(p.ToMM(now[r].GetPosition().x)-xy[0],p.ToMM(now[r].GetPosition().y)-xy[1]) for r,xy in cfg['switch_centres'].items()}
assert max(errors.values())<.000005
changed={r['ref'] for r in change['changes']}
fixed=[r for r in refs if r not in changed]
assert all(refs[r].GetPosition()==now[r].GetPosition() and refs[r].GetOrientationDegrees()==now[r].GetOrientationDegrees() for r in fixed)
tracks={t.m_Uuid.AsString():t for t in after.GetTracks()}
src={t.m_Uuid.AsString():t for t in before.GetTracks()}
kept=change['fixed_core_track_uuids']
missing=[u for u in kept if u not in tracks]
def record(t):
    width=t.GetWidth(p.F_Cu) if isinstance(t,p.PCB_VIA) else t.GetWidth()
    return (t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetLayer(),width,t.GetNetname())
modified=[u for u in kept if u in tracks and record(src[u])!=record(tracks[u])]
pcb=HERE/'pcb/PHBox-ergonomic.kicad_pcb'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
root_unchanged=sha(ROOT/'Flatbox-rev8.kicad_pcb')==change['baseline_sha256']
assert root_unchanged
d=json.loads((HERE/'checks/candidate-drc.json').read_text())
result={'pin_maps_identical':True,'footprints':len(now),'moved_footprints':len(changed),'fixed_footprints_exactly_preserved':len(fixed),
 'max_main_switch_centre_error_mm':max(errors.values()),'protected_core_tracks_requested':len(kept),'protected_core_tracks_missing':missing,'protected_core_tracks_modified':modified,
 'original_root_board_unchanged':root_unchanged,'candidate_sha256':sha(pcb),'drc_error_count':sum(v['severity']=='error' for v in d['violations']),
 'drc_warning_types':dict(collections.Counter(v['type'] for v in d['violations'] if v['severity']=='warning')),'unconnected_items':len(d['unconnected_items']),
 'fabrication_ready':False,'scope':'Physical layout candidate only; remaining connections and dangling copper need completion. No electrical release claim.'}
(HERE/'checks/pcb-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('protected_core_tracks_missing','protected_core_tracks_modified')},indent=2))
print('missing preserved tracks',len(missing),'modified',len(modified))
assert not missing and not modified
