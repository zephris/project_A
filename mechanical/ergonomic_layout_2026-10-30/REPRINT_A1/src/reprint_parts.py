"""Exact replacement mock geometry; separate parts, no changes to old print jobs."""
from pathlib import Path
import json,sys,math,hashlib,importlib.util
from cadgen import step,build123d as bd,srgb
HERE=Path(__file__).resolve().parents[1]
CASE=HERE.parent
sys.path.insert(0,str(CASE/'src'))
from common import *
from option_common import retainer_shape
from button_blank_common import installed_blank,invert_for_print
# common exports its own HERE; this generator owns a separate print workspace.
HERE=Path(__file__).resolve().parents[1]

def quarters(s):
    b=s.bounding_box();cx=(b.min.X+b.max.X)/2;cy=(b.min.Y+b.max.Y)/2
    for n,(xa,xb,ya,yb) in enumerate(((b.min.X,cx,b.min.Y,cy),(cx,b.max.X,b.min.Y,cy),(b.min.X,cx,cy,b.max.Y),(cx,b.max.X,cy,b.max.Y)),1):
        tool=bd.Pos((xa+xb)/2,(ya+yb)/2,b.min.Z-1)*bd.Box(xb-xa,yb-ya,b.size.Z+2,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))
        yield n,s&tool

def normalized(s):
    b=s.bounding_box();return s.moved(bd.Location((-b.min.X,-b.min.Y,-b.min.Z)))

def build():
    for folder in ('STL','STEP','review'):(HERE/folder).mkdir(exist_ok=True,parents=True)
    old=CASE.parent/'sandwich_17mm_2026-10-08'
    old_manifest=json.loads((old/'MOCK_ONLY/manifest.json').read_text())
    items=[];reuse=[]
    for family,body,qs in (
        ('top_acrylic_SURROGATE',acrylic_shape(True),(1,2,3,4)),
        ('switch_plate',solid(plate_profile(),PLATE_BOTTOM,PLATE_THICKNESS,'plate','#8899AA'),(1,2,3,4)),
        ('bottom_spacer',bottom_spacer_shape(),(1,2,3,4)),
        ('top_spacer',top_spacer_shape(),(3,4))):
        for n,part in quarters(body):
            if n in qs:items.append((f'{family}_QUARTER_{n}',part,'PLA replacement mock'))
            else:reuse.append((n,part))
    # Verify the two retained upper-spacer quarters against the old native factories.
    loader=importlib.util.spec_from_file_location('old_reprint_common',old/'src/common.py')
    old_common=importlib.util.module_from_spec(loader);loader.loader.exec_module(old_common)
    old_quarters=dict(quarters(old_common.top_spacer_shape()))
    reuse_report=[]
    for n,new in reuse:
        previous=old_quarters[n]
        added=(new-previous).volume;removed=(previous-new).volume
        assert added<1e-5 and removed<1e-5,(n,added,removed)
        reuse_report.append({'part':f'top_spacer_QUARTER_{n}','added_volume_mm3':added,'removed_volume_mm3':removed})
    items.append(('option_retainer',retainer_shape(),'PLA replacement mock'))
    foam=solid(foam_profile(),FOAM_BOTTOM,FOAM_TOP-FOAM_BOTTOM,'foam','#888888')
    for n in (1,7):
        name=f'pad_1_{n}_INSTALLED_HEIGHT_GAUGE'
        previous=next(e for e in old_manifest['files'] if Path(e['file']).stem==name)
        lo,hi=previous['raw_bounds_mm'];cx=(lo[0]+hi[0])/2;cy=(lo[1]+hi[1])/2
        def distance(s):
            b=s.bounding_box();return math.hypot((b.min.X+b.max.X)/2-cx,(b.min.Y+b.max.Y)/2-cy)
        part=min(foam.solids(),key=distance);assert distance(part)<2
        items.append((name,part,'Rigid PLA foam-height gauge only'))
    for n in range(1,4):items.append((f'button_blank_PLA_trial_{n}',invert_for_print(installed_blank()),'PLA clip fit trial; not PETG fatigue qualification'))
    assert len(items)==20
    rows=[];catalog=[];x=y=rowh=0
    for name,raw,role in items:
        s=normalized(raw);b=s.bounding_box()
        assert s.is_valid and s.volume>0
        assert b.size.X<=220 and b.size.Y<=220
        s.label=name;s.color=srgb('#7195B5')
        target=HERE/'STL'/f'{name}.stl'
        bd.export_stl(s,str(target),tolerance=.01,angular_tolerance=.12)
        rows.append({'name':name,'file':f'STL/{name}.stl','size_mm':list(b.size),'solid_count':len(s.solids()),
                     'native_volume_mm3':s.volume,'raw_bounds_mm':[list(raw.bounding_box().min),list(raw.bounding_box().max)],
                     'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'purpose':role})
        if x+b.size.X>620:x=0;y+=rowh+10;rowh=0
        catalog.append(s.moved(bd.Location((x,y,0))));x+=b.size.X+10;rowh=max(rowh,b.size.Y)
    inputs=[CASE/'layout.json',CASE/'constraints.json',CASE/'button-blank-spec.json',CASE/'src/common.py',CASE/'src/option_common.py',CASE/'src/button_blank_common.py']
    result={'units':'mm','part_count':20,'PLA_replacement_and_gauge_parts':17,'PLA_blanking_plug_trials':3,
            'native_verified_reusable_parts':reuse_report,'files':rows,
            'source_sha256':{str(p.relative_to(CASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
            'warning':'Unpowered mock. Rigid foam gauges are not damping foam. PLA plugs require a first fit trial. Earlier full PCB/assembly routing and tolerance limits remain.'}
    (HERE/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    return bd.Compound(children=catalog,label='replacement_parts_inventory_not_a_print_plate')

@step(out='../STEP/reprint_parts.step')
def reprint_parts():return build()

if __name__=='__main__':reprint_parts()
