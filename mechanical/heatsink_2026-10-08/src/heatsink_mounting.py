"""Mounting layout: PCB-floating heatsink plus independent enclosure references.

All mm; Z=0 is PCB front. Outer plates are layout envelopes, not cut-ready parts.
Screw threads/heads, gasket carrier and the V2 retention plate are not specified.
"""
import json
from cadgen import step, read_step, build123d as bd, srgb
from heatsink_common import PROJECT, xy, MOUNTS, cylinder_at
from heatsink_plate import heatsink_plate
from heatsink_common import make_pads, make_stops, make_support_washers

BOTTOM_Z=-15.0
BOTTOM_THICKNESS=3.0
TOP_Z=8.0
TOP_THICKNESS=3.0
OUTLINE_MARGIN=8.0
WINDOW_MARGIN=1.4


def rear_hardware():
    parts=[]
    for ref,m in MOUNTS.items():
        x,y=xy(ref)
        # Keep a 0.049 mm nominal gap to the exported back seating datum.
        # The washer bears on the finished board, whose thickness is not measured.
        bore=6.3 if m['pilot'] else 2.2
        washer=cylinder_at(x,y,m['stop_od'],-2.15,0.50)
        washer-=cylinder_at(x,y,bore,-2.25,0.70)
        washer.label='rear_insulating_washer_'+ref
        washer.color=srgb('#7562A0')
        cap=cylinder_at(x,y,m['stop_od'],-4.15,2.0)
        # Nominal pilot for a proposed tapped polymer retainer. Threads are omitted.
        cap-=cylinder_at(x,y,2.5 if m['pilot'] else 1.6,-4.25,2.2)
        cap.label='custom_POM_retainer_thread_not_modeled_'+ref
        cap.color=srgb('#E9DDBC')
        parts.extend([washer,cap])
    return parts


def outer_plate_references():
    reg=json.loads((PROJECT/'registration.json').read_text())
    xmin,xmax,ymin,ymax,_,_=reg['substrate']['bounds']
    cx,cy=(xmin+xmax)/2,(ymin+ymax)/2
    w,h=xmax-xmin,ymax-ymin
    outline=bd.RectangleRounded(w+2*OUTLINE_MARGIN,h+2*OUTLINE_MARGIN,8)
    bottom=bd.Pos(cx,cy,BOTTOM_Z)*bd.extrude(outline,BOTTOM_THICKNESS)
    bottom.label='REFERENCE_bottom_outer_plate_3mm_Z_minus15_to_minus12'
    bottom.color=srgb('#6C94C5')
    top=bd.Pos(cx,cy,TOP_Z)*bd.extrude(outline,TOP_THICKNESS)
    opening=bd.Pos(cx,cy,TOP_Z-0.1)*bd.extrude(
        bd.RectangleRounded(w+2*WINDOW_MARGIN,h+2*WINDOW_MARGIN,5),TOP_THICKNESS+0.2)
    top-=opening
    top.label='REFERENCE_top_outer_bezel_3mm_Z8_to11'
    top.color=srgb('#91BBDD')
    posts=[]
    for i,(x,y) in enumerate(((xmin-4,ymin-4),(xmin-4,ymax+4),
                              (xmax+4,ymin-4),(xmax+4,ymax+4)),1):
        # Custom case-height spacers lie outside the PCB. They do not clamp it.
        spacer=cylinder_at(x,y,6,BOTTOM_Z+BOTTOM_THICKNESS,
                           TOP_Z-(BOTTOM_Z+BOTTOM_THICKNESS))
        spacer-=cylinder_at(x,y,3.4,BOTTOM_Z,TOP_Z-BOTTOM_Z+1)
        spacer.label=f'REFERENCE_independent_case_spacer_{i}'
        spacer.color=srgb('#8D959D')
        cutter=cylinder_at(x,y,3.4,BOTTOM_Z-0.1,TOP_Z+TOP_THICKNESS-BOTTOM_Z+0.2)
        top-=cutter
        bottom-=cutter
        posts.append(spacer)
    return [top,bottom,*posts]


def mounting_parts(exploded=False):
    reg=json.loads((PROJECT/'registration.json').read_text())
    board=read_step(str(PROJECT/'reference/board.step'))
    board=board.moved(bd.Location((0,0,-reg['front_z_native_mm'])))
    board.label='Current_PHBox_ChocV2_PCB_reference'
    plate=heatsink_plate()
    plate.label='Milled_aluminium_heatsink'
    # Exploded offsets are solely an inspection layout, never machining dimensions.
    upper=[plate,*make_pads(),*make_stops(),*make_support_washers()]
    lower=rear_hardware()
    shell=outer_plate_references()
    if exploded:
        upper=[p.moved(bd.Location((0,0,22))) for p in upper]
        lower=[p.moved(bd.Location((0,0,-12))) for p in lower]
        shell[0]=shell[0].moved(bd.Location((0,0,42)))
        shell[1]=shell[1].moved(bd.Location((0,0,-30)))
        # Case spacers are omitted from the exploded view to avoid implying contact.
        shell=shell[:2]
    return [board,*upper,*lower,*shell]


@step(out='../STEP/heatsink_mounting.step')
def heatsink_mounting():
    return bd.Compound(children=mounting_parts(),label='PHBox_mounting_layout_candidate')


@step(out='../STEP/heatsink_mounting_exploded.step')
def heatsink_mounting_exploded():
    return bd.Compound(children=mounting_parts(True),label='PHBox_exploded_inspection_NOT_installed_heights')


if __name__=='__main__':
    heatsink_mounting()
    heatsink_mounting_exploded()
