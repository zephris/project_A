"""Read-only switch LED study; mm; local X=PCB X, Y=-PCB Y, front Z=0."""
from pathlib import Path
import json
from cadgen import build123d as bd, read_step, srgb
PROJECT=Path(__file__).resolve().parents[1]
ROOT=PROJECT.parents[1]
WINDOW_X=2.60
WINDOW_Y=2.40
WINDOW_Z=1.20
def volume(shape):
    return sum(s.volume for s in shape) if isinstance(shape,list) else shape.volume
def parts(row, section=False):
    switch=read_step(ROOT/'3dmodels/SW_Kailh_Choc_V2_red.step').moved(bd.Rot(0,0,180))
    dx=row['led_xy'][0]-row['sw_xy'][0]
    dy=-(row['led_xy'][1]-row['sw_xy'][1])
    led=read_step(ROOT/'3dmodels/SK6805_EC15_EasyEDA.step').moved(bd.Rot(0,0,row['led_angle']))
    led=led.moved(bd.Pos(dx,dy,0))
    coupon=bd.Pos(0,0,-.8)*bd.Box(18,18,1.6)
    for x,y,d in [(0,0,5.05),(0,5.9,3.05),(5,3.8,3.05),(-5,-5.15,1.6),(-5.5,0,1.9),(5.5,0,1.9)]:
        coupon=coupon-bd.Pos(x,y,-1)*bd.Cylinder(d/2,4)
    if section:
        cut=bd.Pos(5,0,3)*bd.Box(10,30,20)
        # Work on located constituent solids; aggregate imported Compound booleans
        # can lose occurrence transforms in this build123d version.
        section_solids=[]
        for solid in switch.solids():
            remainder=solid-cut
            if remainder:
                section_solids.extend(remainder.solids())
        switch=bd.Compound(children=section_solids)
        coupon=coupon-cut
    switch.label=row['switch']+'_ChocV2_reference'+('_sectioned' if section else '')
    led.label=row['led']+'_SK6805_actual_placement'
    coupon.label=row['switch']+'_simplified_PCB_coupon'
    led.color=srgb('#F4B000'); coupon.color=srgb('#287E48')
    return [switch,led,coupon]
def window():
    """Design study clearance gauge, not a measured OEM cavity nor a machining instruction."""
    s=bd.Pos(0,-4.93,WINDOW_Z/2)*bd.Box(WINDOW_X,WINDOW_Y,WINDOW_Z)
    s.label='candidate_LED_clearance_gauge_2p6x2p4x1p2'
    s.color=srgb('#00BCD4',.22)
    return s
def comparisons(section=False):
    rows={r['switch']:r for r in json.loads((PROJECT/'placements.json').read_text())}
    out=[]
    for i,ref in enumerate(['SW2','SW1','SW7','SW13']):
        shift=bd.Pos(i*22,0,0)
        cell=bd.Compound(children=parts(rows[ref],section),label=ref+'_LED_fit')
        out.append(cell.moved(shift))
    return bd.Compound(children=out,label='ChocV2_LED_fit_comparison')
