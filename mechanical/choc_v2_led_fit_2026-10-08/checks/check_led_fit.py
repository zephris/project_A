from pathlib import Path
import json,sys,math,hashlib
from cadgen import read_step, build123d as bd
PROJECT=Path(__file__).resolve().parents[1]
ROOT=PROJECT.parents[1]
sys.path.insert(0,str(PROJECT/'src'))
from fit_common import window,WINDOW_X,WINDOW_Y,WINDOW_Z
def vol(r): return sum(v.volume for v in r) if isinstance(r,list) else r.volume if r else 0
def overlap(a,b):
 # Compound.intersect currently loses imported child placement in this kernel.
 # World-space solids preserve location. Positive distance also proves no overlap.
 if a.distance_to(b)>1e-7:
  return 0.0
 return sum(vol(x.intersect(y)) for x in a.solids() for y in b.solids()
            if x.distance_to(y)<1e-7)
print('Importing exact source models',flush=True)
switch=bd.import_step(ROOT/'3dmodels/SW_Kailh_Choc_V2_red.step').moved(bd.Rot(0,0,180))
led=bd.import_step(ROOT/'3dmodels/SK6805_EC15_EasyEDA.step')
results=[]
measured={}
for row in json.loads((PROJECT/'placements.json').read_text()):
 print('Checking',row['switch'],flush=True)
 dx=row['led_xy'][0]-row['sw_xy'][0];dy=-(row['led_xy'][1]-row['sw_xy'][1])
 assert row['sw_angle']==0,'Study rotation assumes current switch footprint 0 degrees'
 actual=led.moved(bd.Rot(0,0,row['led_angle'])).moved(bd.Pos(dx,dy,0))
 # Package tolerance not certified: chosen engineering sweep plus 0.10mm solder lift.
 envelope=bd.Pos(dx,dy,.40)*bd.Box(1.70,1.70,.80)
 key=(round(dx,6),round(dy,6),row['led_angle'])
 if key not in measured:
  measured[key]={'LED_switch_overlap_mm3':overlap(switch,actual),
   'LED_switch_distance_mm':switch.distance_to(actual),
   'engineering_envelope_overlap_mm3':overlap(switch,envelope),
   'engineering_envelope_distance_mm':switch.distance_to(envelope)}
 results.append({'switch':row['switch'],'led':row['led'],'actual_cad_offset_mm':[dx,dy],
 'deviation_from_OEM_nominal_mm':[dx,dy+4.93],
 **measured[key],
 'candidate_gauge_LED_containment_margin_xy_mm':[(WINDOW_X-1.50)/2-abs(dx),(WINDOW_Y-1.50)/2-abs(dy+4.93)],
 'candidate_gauge_envelope_containment_margin_xy_mm':[(WINDOW_X-1.70)/2-abs(dx),(WINDOW_Y-1.70)/2-abs(dy+4.93)]})
gauge=window()
gauge_overlap=overlap(switch,gauge)
saved=[]
for stem in ['choc_v2_led_fit','choc_v2_led_section','choc_v2_led_window_candidate']:
 print('Checking saved',stem,flush=True)
 path=PROJECT/'STEP'/f'{stem}.step'; shape=bd.import_step(path)
 saved.append({'file':path.name,'valid':shape.is_valid,'solids':len(shape.solids()),'volume_mm3':shape.volume})
out={'frame':'local PCB X, minus PCB Y; switch front seating Z=0 mm',
 'pcb_sha256':hashlib.sha256((ROOT/'Flatbox-rev8.kicad_pcb').read_bytes()).hexdigest(),
 'candidate_gauge_mm':[WINDOW_X,WINDOW_Y,WINDOW_Z],'gauge_switch_overlap_mm3':gauge_overlap,
 'gauge_switch_distance_mm':switch.distance_to(gauge),
 'intersection_method':'Located constituent solid pairs; positive distance prunes nonintersecting pairs. Aggregate Compound.intersect gives spurious results for the moved imported switch in this build123d version.',
 'engineering_envelope_note':'1.70x1.70x0.80 mm chosen sensitivity envelope, not OPSCO certified maximum',
 'threshold_mm3':1e-6,'results':results,'saved_artifacts':saved}
(PROJECT/'fit-check.json').write_text(json.dumps(out,indent=2)+'\n')
assert gauge_overlap<1e-6
assert all(r['LED_switch_overlap_mm3']<1e-6 and r['engineering_envelope_overlap_mm3']<1e-6 for r in results)
assert all(r['valid'] for r in saved)
print('16 LED placements pass nominal and selected engineering envelope collision checks')
print('Minimum exact LED distance:',min(r['LED_switch_distance_mm'] for r in results))
print('Minimum engineering envelope distance:',min(r['engineering_envelope_distance_mm'] for r in results))
