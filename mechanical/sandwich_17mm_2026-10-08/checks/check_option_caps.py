"""Saved cap guidance, retention and assumed travel; does not qualify an actual switch."""
from pathlib import Path
import sys,json,math
from cadgen import read_step,build123d as bd
from cadgen.geometry import overlap_volume
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from common import *
caps=list(read_step(HERE/'STEP/option_caps.step').solids())
assert len(caps)==6 and all(s.is_valid for s in caps)
window=bd.Pos(244.5,-43,8)*bd.Box(73,26,12)
fixed={}
for n in ('top_acrylic','top_spacer','option_retainer','option_hardware'):
    ss=[]
    for s in read_step(HERE/'STEP'/f'{n}.step').solids():
        cut=s.intersect(window)
        if cut is None:continue
        if hasattr(cut,'solids'):ss.extend(cut.solids())
        else:
            for t in cut:ss.extend(t.solids())
    fixed[n]=ss
boxes={}
def box(s):
    if id(s) not in boxes:boxes[id(s)]=(s,s.bounding_box())
    return boxes[id(s)][1]
def hit(a,b):
    aa=box(a);bb=box(b)
    return all(getattr(aa.max,k)>getattr(bb.min,k)+1e-6 and getattr(bb.max,k)>getattr(aa.min,k)+1e-6 for k in ('X','Y','Z'))
collisions=[];tests=0
for i,cap in enumerate(caps,1):
    b=box(cap);cx=(b.min.X+b.max.X)/2;cy=(b.min.Y+b.max.Y)/2
    local_window=bd.Pos(cx,cy,8)*bd.Box(9,9,12)
    local={}
    for name,ss in fixed.items():
        cropped=[]
        for s in ss:
            cut=s.intersect(local_window)
            if cut is None:continue
            if hasattr(cut,'solids'):cropped.extend(cut.solids())
            else:
                for t in cut:cropped.extend(t.solids())
        local[name]=cropped
    print('Checking saved cap '+str(i),flush=True)
    for dz in (-TRAVEL,0,TRAVEL):
        for press in (0,.35,.45):
            for angle in range(0,360,45):
                dx=.3*math.cos(math.radians(angle));dy=.3*math.sin(math.radians(angle))
                moved=cap.moved(bd.Location((dx,dy,dz-press)))
                mb=box(moved)
                assert mb.min.X>=cx-4.5 and mb.max.X<=cx+4.5 and mb.min.Y>=cy-4.5 and mb.max.Y<=cy+4.5 and mb.min.Z>=2 and mb.max.Z<=14
                for name,ss in local.items():
                    for a in moved.solids():
                        for b in ss:
                            tests+=1
                            if not hit(a,b) or a.distance_to(b)>1e-6:continue
                            v=overlap_volume(a,b)
                            if v>1e-5:collisions.append({'cap':i,'PCB_z':dz,'press':press,'guide_offset_angle':angle,'fixed':name,'overlap_mm3':v})
# Flanges cover the entire top aperture at maximum radial guide play.
coverage=(8-OPTION_GUIDE)/2-.3
assert coverage>0
stop_margin=6.9-TRAVEL-.35-6.2
assert stop_margin>=.09999
report={'units':'mm','cap_count':6,'stem_diameter':5.6,'guide_diameter':OPTION_GUIDE,'flange_diameter':8,
 'contact_tip_diameter':1.4,'generic_actuator_height':5,'cap_rest_top':11.2,
 'PCB_z_motion':[-TRAVEL,TRAVEL],'assumed_switch_operating_travel':.35,'tested_mechanical_limit_travel':.45,
 'guide_radial_play':.3,'minimum_projected_board_cover_overlap':coverage,
 'minimum_upper_retention_clearance':8-(7.5+TRAVEL),'minimum_downward_stop_margin_at_operating_travel':stop_margin,
 'minimum_tip_centre_margin_with_XY_board_motion':1.65-math.hypot(.5,.5)-.3,
 'solid_pair_tests':tests,'collisions':collisions,
 'limitations':'Exact option-switch MPN unspecified. Generic H5 model; actual height, stroke, return force, cap friction and manufacturing tolerance require trial. Pressed actuator motion is assumed, not simulated. Flanges hide PCB; not an IP seal.'}
(HERE/'option-caps-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
assert not collisions,'Repair option cap guidance/retention before release'
