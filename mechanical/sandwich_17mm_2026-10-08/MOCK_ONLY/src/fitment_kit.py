"""Read-only production factories -> nonfunctional, print-oriented fitment proxies.

Run with the existing heatsink CAD interpreter. No geometry compensation or
threads are added. Large parts additionally have four unjoined bed-size sections.
"""
from pathlib import Path
import sys, json, hashlib, re
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from common import *
from option_common import cap_parts,retainer_shape,hardware_parts
from port_seal_common import print_part
from case_hardware import case_hardware
from cadgen import step,stl
HERE=Path(__file__).resolve().parents[1]
PROJECT=HERE.parent

def normalize(s,rotate=None):
    if rotate:s=rotate*s
    b=s.bounding_box()
    return bd.Pos(-b.min.X,-b.min.Y,-b.min.Z)*s

def entries():
    items=[]
    def add(name,s,material='PETG/PLA: geometric mock only',role='Unpowered fit check',flip=False):
        items.append((name,s,material,role,flip))
    # Outline and mounting drills from saved constraints, with coarse selected
    # package envelopes. No copper, switch sockets, solder or small components.
    p=board_profile()
    for f in data()[0]['footprints']:
        if f['ref'].startswith('H'):
            for pad in f['pads']:
                d=pad['drill_mm'][0]
                if d>0:p-=disk(pad['pcb_xy'][0],-pad['pcb_xy'][1],d)
    board=solid(p,FOAM_TOP,-FOAM_TOP,'PCB_ENVELOPE','#6D985B')
    from heatsink_common import CONTACTS
    for ref,c in CONTACTS.items():
        x,y=xy(ref);w,h=c['size']
        board+=solid(rect(x,y,w,h),0,c['package_top'],'package_'+ref,'#6D985B')
    board+=solid(rect(USB_A_X,(-48.24-34.14)/2,14.4,14.10),0,7,'A_BODY','#6D985B')
    board+=solid(rect(USB_C_X,(-42.384118-33.809118)/2,8.94,8.575),0,3.21,'C_BODY','#6D985B')
    add('PCB_SELECTED_ENVELOPES_SURROGATE',board,role='Outline/H drills plus coarse U1/U3 and USB shell boxes; no mating ports or full topography')
    oled=solid(rect(100.3,-54,35.4,33.5),3,1.2,'OLED_PCB','#6D985B')
    for x,y in screen_holes():oled-=cylinder(x,y,2.4,2.9,1.4)
    add('OLED_MODULE_PCB_SURROGATE',oled,role='35.4 x 33.5 mm module PCB and holes only; glass/header height not represented')
    add('top_acrylic_SURROGATE',acrylic_shape(True),role='2 mm acrylic footprint, holes and countersinks; not acrylic stiffness')
    add('bottom_acrylic_SURROGATE',acrylic_shape(False),role='2 mm acrylic footprint and countersinks',flip=True)
    add('top_spacer',top_spacer_shape(),role='Production shape, pockets and port roofs')
    add('bottom_spacer',bottom_spacer_shape(),role='Production shape, guides and support ledges')
    add('switch_plate',solid(plate_profile(),PLATE_BOTTOM,PLATE_THICKNESS,'switch_plate','#A2B7CF'),role='1.3 mm plate aperture/LED fit; print thickness carefully')
    add('screen_frame',solid(screen_frame_profile(),4.2,1.0,'screen_frame','#A2B7CF'))
    add('aluminium_heatsink_SURROGATE',make_plate(),role='Boss/BOOTSEL/RESET and mount fit only: never a powered heatsink',flip=True)
    for s in [*screen_posts(),*plate_posts(),*make_stops(),*make_support_washers(),*rear_hardware()]:
        add(s.label,s,role='Exact existing insulating part envelope; pilot bore only, threads omitted')
    for s in cap_parts():add(s.label,s,role='Option cap travel trial; small underside stem needs support',flip=True)
    add('option_retainer',retainer_shape(),role='Nut pocket and cap capture fit')
    for s in hardware_parts():add(s.label+'_SURROGATE',s,role='Optional hardware visual gauge only; no functional threads')
    # Factory represents installed support/pad height, not the free stock thickness.
    for n,s in enumerate([solid(foam_profile(),FOAM_BOTTOM,FOAM_TOP-FOAM_BOTTOM,'lower_foam','#817D71'),*upper_pads(),*make_pads()],1):
        for j,part in enumerate(s.solids(),1):
            add(f'pad_{n}_{j}_INSTALLED_HEIGHT_GAUGE',part,role='Rigid gauge only: actual foam/pads required for compliance/thermal trials')
    for k in ('A','C'):add('USB_'+k+'_collar',print_part(k),'Unfilled TPU 95A candidate',role='Production front-face-down collar trial, 0.317 mm membrane')
    # Printed stand-ins for all eight acrylic case columns and sixteen washers.
    # A stock 12 mm AF5 column and two 0.5 mm washers make each 13 mm gap.
    for i,(x,y) in enumerate(bolts(),1):
        body=bd.Pos(x,y,-4.5)*bd.extrude(bd.RegularPolygon(5/(3**.5),6),12)
        body-=cylinder(x,y,2.5,-4.6,12.2)
        add(f'acrylic_case_post_{i}_12mm_AF5_SURROGATE',body,role='12 mm female/female M3 envelope, unthreaded; use real hardware to close')
        for end,z in (('bottom',-5),('top',7.5)):
            add(f'acrylic_case_washer_{i}_{end}_0p5_SURROGATE',cylinder(x,y,7,z,.5)-cylinder(x,y,3.4,z-.1,.7),role='0.5 mm height gauge, not a load washer')
    return items

def quarter_parts(name,s):
    b=s.bounding_box();cx=(b.min.X+b.max.X)/2;cy=(b.min.Y+b.max.Y)/2
    for i,(xa,xb,ya,yb) in enumerate(((b.min.X,cx,b.min.Y,cy),(cx,b.max.X,b.min.Y,cy),(b.min.X,cx,cy,b.max.Y),(cx,b.max.X,cy,b.max.Y)),1):
        cutter=bd.Pos((xa+xb)/2,(ya+yb)/2,b.min.Z-1)*bd.Box(xb-xa,yb-ya,b.size.Z+2,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))
        cut=s&cutter
        if cut.volume>1e-5:yield name+f'_QUARTER_{i}',cut

def build():
    assert HERE.name=='MOCK_ONLY' and HERE.parent==PROJECT, 'Refuse export outside mock kit'
    (HERE/'STL').mkdir(parents=True,exist_ok=True)
    manifest=[];layout=[];x=y=0;rowh=0
    source_hash={str(p.relative_to(PROJECT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT/'src').glob('*.py')}
    source_hash.update({'../heatsink_2026-10-08/src/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HEAT/'src').glob('*.py')})
    for name,s,mat,role,flip in entries():
        variants=[(name,s)]
        if max(s.bounding_box().size.X,s.bounding_box().size.Y)>220:
            variants+=list(quarter_parts(name,s))
        for partname,raw in variants:
            rot=bd.Rot(180,0,0) if flip else None
            p=normalize(raw,rot);b=p.bounding_box()
            assert p.is_valid and p.volume>0,partname
            safe=re.sub('[^A-Za-z0-9_-]','_',partname)
            p.label='MOCK_ONLY_'+safe;p.color=srgb('#D6A653') if 'SURROGATE' in safe else srgb('#9EC4DA')
            bd.export_stl(p,str(HERE/'STL'/f'{safe}.stl'),tolerance=.015,angular_tolerance=.15)
            manifest.append({'file':f'STL/{safe}.stl','quantity':1,'material':mat,'purpose':role,'size_mm':[b.size.X,b.size.Y,b.size.Z],'native_volume_mm3':p.volume,'solid_count':len(p.solids()),'raw_bounds_mm':[raw.bounding_box().min.to_tuple(),raw.bounding_box().max.to_tuple()],'flip_X_180':flip,'quarter_option':'QUARTER' in safe,'print_notes':'Support bosses as required' if flip else 'Model bed face is Z=0; preview islands/bridges in slicer'})
            if 'QUARTER' not in safe:
                if x+b.size.X>640:x=0;y+=rowh+15;rowh=0
                layout.append(bd.Pos(x,y,0)*p);x+=b.size.X+15;rowh=max(rowh,b.size.Y)
    (HERE/'manifest.json').write_text(json.dumps({'units':'mm','warning':'MOCK ONLY. No powered tests with plastic heatsink or rigid pad gauges. Threads omitted.','source_hashes':source_hash,'files':manifest},indent=2))
    return bd.Compound(children=layout,label='MOCK_ONLY_print_parts_catalog_not_a_print_bed')

@step(out='../STEP/fitment_kit.step')
@stl(out='../STL/fitment_kit_CATALOG_DO_NOT_SLICE.stl',mesh_tolerance=.015)
def fitment_kit():return build()

if __name__=='__main__':fitment_kit()
