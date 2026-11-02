from pathlib import Path
import sys,json,hashlib
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from heatsink_common import constraints, CONTACTS, MOUNTS, BASE_Z, TOP_Z, xy, box_region, cylinder_at, make_pads, make_stops, make_support_washers
from cadgen import read_step,read_scene,build123d as bd
from cadgen.geometry import closest_points,overlap_volume

data,fps=constraints()
assert hashlib.sha256((HERE.parents[1]/data['source']).read_bytes()).hexdigest()==data['sha256']
plate=read_step(str(HERE/'STEP/heatsink_plate.step'))
assert plate.is_valid and len(plate.solids())==1
reg=json.loads((HERE/'registration.json').read_text())
scene=read_scene(str(HERE/'reference/board.step'))
hits=[]; distances=[]; support_hits=[]
stops=make_stops()+make_support_washers()
for entry in reg['nearby_parts']:
    sh=scene.resolve(entry['ref']).shape().moved(bd.Location((0,0,-reg['front_z_native_mm'])))
    for s in sh.solids():
        volume=overlap_volume(plate.solids()[0],s)
        if volume>1e-6: hits.append({'ref':entry['ref'],'volume_mm3':volume})
        d=closest_points(plate.solids()[0],s).distance
        distances.append({'ref':entry['ref'],'label':entry['label'],'distance_mm':d})
        for stop in stops:
            v=overlap_volume(stop.solids()[0],s)
            if v>1e-6: support_hits.append({'stop':stop.label,'ref':entry['ref'],'volume_mm3':v})
service=[]
for ref in ('SW19','SW20'):
    x,y,w,h=fps[ref]['bbox_xy']
    zone=box_region(x-1.5,x+w+1.5,y-1.5,y+h+1.5,-2,15)
    v=overlap_volume(plate.solids()[0],zone.solids()[0])
    service.append({'ref':ref,'net':[p['net'] for p in fps[ref]['pads']],
                    'margin_mm':1.5,'overlap_mm3':v,
                    'clearance_mm':closest_points(plate.solids()[0],zone.solids()[0]).distance})
holes=[]
for ref,m in MOUNTS.items():
    x,y=xy(ref)
    cutter=cylinder_at(x,y,m['hole']-0.002,BASE_Z-0.05,TOP_Z-BASE_Z+0.1)
    v=overlap_volume(plate.solids()[0],cutter.solids()[0])
    holes.append({'ref':ref,'pcb_xy':fps[ref]['pcb_xy'],'plate_hole_diameter_mm':m['hole'],
                  'through_bore_overlap_mm3':v})
pads=[]
for p in make_pads():
    v=overlap_volume(plate.solids()[0],p.solids()[0])
    pads.append({'label':p.label,'plate_overlap_mm3':v,'distance_to_plate_mm':closest_points(plate.solids()[0],p.solids()[0]).distance})
support_contacts=[]
for support in stops:
    support_contacts.append({'label':support.label,
                             'plate_overlap_mm3':overlap_volume(plate.solids()[0],support.solids()[0]),
                             'distance_to_plate_mm':closest_points(plate.solids()[0],support.solids()[0]).distance})
bb=plate.bounding_box()
report={'units':'mm','board_sha256':data['sha256'],'plate_valid':plate.is_valid,
        'solid_count':len(plate.solids()),'bounds_mm':[list(bb.min),list(bb.max)],
        'volume_mm3':plate.volume,'mass_g_at_2p70_g_cm3':plate.volume*0.0027,
        'board_collision_hits':hits,'stop_collision_hits':support_hits,
        'component_clearances':sorted(distances,key=lambda d:d['distance_mm']),
        'button_service_zones':service,'mount_bores':holes,'pad_contact':pads,
        'support_contacts':support_contacts,
        'contact_face_z_mm':{ref:c['package_top']+0.40 for ref,c in CONTACTS.items()},
        'coverage':'Nominal native STEP geometry. Package maxima, placement error, solder variation, pad force, hardware/case travel and thermal performance remain to be qualified.'}
(HERE/'fit-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('component_clearances',)},indent=2),flush=True)
assert not hits and not support_hits
assert all(s['overlap_mm3']<1e-6 for s in service)
assert all(h['through_bore_overlap_mm3']<1e-6 for h in holes)
assert all(p['plate_overlap_mm3']<1e-6 and p['distance_to_plate_mm']<1e-5 for p in pads)
assert all(p['plate_overlap_mm3']<1e-6 and p['distance_to_plate_mm']<1e-5 for p in support_contacts)
