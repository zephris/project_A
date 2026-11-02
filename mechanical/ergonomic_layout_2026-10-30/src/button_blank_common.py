"""Removable 24 mm main-button blank. Local Z=0 is the faceplate top.

Curved cantilevers flex in XY; the central roof stays above the unpressed stem.
Two lower-edge scallops expose a lip to a fingernail without a raised handle.
"""
from pathlib import Path
import json
from cadgen import build123d as bd, srgb

HERE=Path(__file__).resolve().parents[1]

def spec():
    return json.loads((HERE/'button-blank-spec.json').read_text())

def cyl(r,z,h):
    return bd.Pos(0,0,z)*bd.Cylinder(r,h,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))

def sector(ri,ro,start,end,z,h):
    # Explicit radial boundaries avoid a sampled polygon approximating the arc.
    outer=bd.Edge.make_circle(ro,start_angle=start,end_angle=end)
    inner=bd.Edge.make_circle(ri,start_angle=start,end_angle=end)
    lines=[bd.Edge.make_line(outer@0,inner@0),bd.Edge.make_line(outer@1,inner@1)]
    wire=bd.Wire.combine([outer,inner,*lines])[0]
    return bd.Pos(0,0,z)*bd.extrude(bd.Face(wire),h)

def latch_parts():
    p=spec();start=p['beam_end_degrees']-p['latch_span_degrees'];end=p['beam_end_degrees']
    pieces=[]
    for (za,ra),(zb,rb) in zip(p['latch_z_radius_stations'],p['latch_z_radius_stations'][1:]):
        outer=bd.Pos(0,0,za)*bd.Cone(ra,rb,zb-za,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN)) if ra!=rb else cyl(ra,za,zb-za)
        annulus=outer-cyl(p['beam_inner_radius'],za-.01,zb-za+.02)
        wedge=sector(p['beam_inner_radius'],p['latch_peak_radius']+.1,start,end,za,zb-za)
        pieces.append(annulus & wedge)
    first=pieces[0]
    for s in pieces[1:]: first=first+s
    return [first,bd.Rot(0,0,180)*first]

def installed_blank():
    p=spec();rise=p['rise_above_face']
    cap=cyl(p['flange_diameter']/2,0,rise)+cyl(p['pilot_radius'],p['roof_underside'],rise-p['roof_underside'])
    beam=sector(p['beam_inner_radius'],p['beam_outer_radius'],p['beam_start_degrees'],p['beam_end_degrees'],p['beam_bottom'],p['beam_top']-p['beam_bottom'])
    root=sector(p['beam_inner_radius'],p['beam_outer_radius'],p['beam_start_degrees'],p['beam_start_degrees']+p['root_span_degrees'],p['beam_bottom'],.1-p['beam_bottom'])
    finger=beam+root+latch_parts()[0]
    cap=cap+finger+(bd.Rot(0,0,180)*finger)
    # Bottom-open scallops leave the full 1.2 mm upper lip in the print datum.
    for side in (-1,1):
        x=side*(p['groove_inner_x']+1.3)
        cut=bd.Pos(x,0,-.05)*bd.extrude(bd.RectangleRounded(2.6,p['groove_width'],.8),p['groove_height']+.05)
        cap=cap-cut
    cap.label='24mm_button_blank_PETG_two_curved_clips'
    cap.color=srgb('#677D92')
    assert cap.is_valid and len(cap.solids())==1
    return cap

def invert_for_print(s):
    # This transform is its own inverse; face rests on Z=0 for the STL.
    return bd.Pos(0,0,spec()['rise_above_face'])*bd.Rot(180,0,0)*s

def coupon_shape():
    slab=bd.Pos(0,0,-2)*bd.extrude(bd.RectangleRounded(100,36,4),2)
    for x,d in ((-32,23.8),(0,24),(32,24.2)):
        slab=slab-(bd.Pos(x,0,0)*cyl(d/2,-2.1,2.2))
    slab.label='optional_2mm_coupon_23p8_24_24p2_left_to_right'
    slab.color=srgb('#BDD5DC')
    return slab
