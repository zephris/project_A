"""PHBox prototype geometry. mm; X=PCB X, Y=-PCB Y, Z=PCB front=0."""
from pathlib import Path
import json
from cadgen import build123d as bd, srgb

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
BASE_Z = 4.0
WEB_THICKNESS = 3.0
TOP_Z = BASE_Z + WEB_THICKNESS
PAD_FREE = 0.50
PAD_INSTALLED = 0.40
SOLDER_ALLOWANCE = 0.05
SUPPORT_RING_INSTALLED = 0.50
# Candidate soldered-package tops; change from first-article measurements.
CONTACTS = {'U1': {'size': (6.0, 6.0), 'package_top': 0.90},
            'U3': {'size': (4.0, 4.0), 'package_top': 2.21}}
MOUNTS = {'H5': {'hole': 3.4, 'stop_od': 8.0, 'bore': 3.4, 'pilot': 6.1},
          'H7': {'hole': 3.4, 'stop_od': 8.0, 'bore': 3.4, 'pilot': 6.1},
          'H12': {'hole': 2.4, 'stop_od': 4.5, 'bore': 2.2, 'pilot': None}}

def constraints():
    data = json.loads((PROJECT / 'constraints.json').read_text())
    return data, {f['ref']: f for f in data['footprints']}

def xy(ref):
    _, fps = constraints()
    x, y = fps[ref]['pcb_xy']
    return x, -y

def box_region(xmin, xmax, pcb_ymin, pcb_ymax, bottom, height, radius=0):
    cx, cy = (xmin+xmax)/2, -(pcb_ymin+pcb_ymax)/2
    profile = bd.RectangleRounded(xmax-xmin, pcb_ymax-pcb_ymin, radius) if radius else bd.Rectangle(xmax-xmin, pcb_ymax-pcb_ymin)
    return bd.Pos(cx, cy, bottom) * bd.extrude(profile, height)

def cylinder_at(x, y, diameter, bottom, height):
    return bd.Pos(x, y, bottom) * bd.Cylinder(diameter/2, height, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))

def make_plate():
    plate = box_region(121, 181, 45, 79, BASE_Z, WEB_THICKNESS, 2)
    # Open-sided service notch, including fingertip/probe clearance above buttons.
    plate -= box_region(115, 136.5, 60, 75, 0, TOP_Z+1, 3)
    _, fps = constraints()
    for ref in ('H5', 'H12'):
        x,y = fps[ref]['pcb_xy']
        plate += box_region(x-5.5, x+5.5, y-5.5, 52, BASE_Z, WEB_THICKNESS, 2)
    x,y = fps['H7']['pcb_xy']
    plate += box_region(x-6, x+6, 76, y+5, BASE_Z, WEB_THICKNESS, 2)
    # Radius the planar outline junctions for a 3 mm diameter end mill.
    vertical = plate.edges().filter_by(bd.Axis.Z)
    sharp = [e for e in vertical if sum(
        f.geom_type == bd.GeomType.PLANE and
        any(e.wrapped.IsSame(fe.wrapped) for fe in f.edges())
        for f in plate.faces()) == 2]
    if sharp:
        plate = bd.fillet(sharp, 1.5)
    for ref,c in CONTACTS.items():
        x,y = xy(ref)
        w,h = c['size']
        face = c['package_top'] + PAD_INSTALLED
        # Large exterior corners on boss; no small closed pockets or undercuts.
        plate += bd.Pos(x,y,face) * bd.extrude(bd.RectangleRounded(w,h,0.5), BASE_Z-face+0.05)
    for ref,m in MOUNTS.items():
        x,y = xy(ref)
        plate -= cylinder_at(x,y,m['hole'],0,TOP_Z+1)
    assert len(plate.solids()) == 1 and plate.is_valid
    plate.label = 'aluminium_6061_T6_heatsink_candidate'
    plate.color = srgb('#B7BCC5')
    return plate

def make_pads():
    pads=[]
    for ref,c in CONTACTS.items():
        x,y=xy(ref); w,h=(d-0.5 for d in c['size'])
        # Reference CAD has no solder stand-off. Show the full CAD gap (0.45 mm);
        # an assembled package 0.05 mm higher leaves the intended 0.40 mm gap.
        pad=bd.Pos(x,y,c['package_top']-SOLDER_ALLOWANCE) * bd.Box(w,h,PAD_INSTALLED+SOLDER_ALLOWANCE,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))
        pad.label='insulating_thermal_pad_'+ref
        pad.color=srgb('#45B6BB')
        pads.append(pad)
    return pads

def make_stops():
    parts=[]
    for ref,m in MOUNTS.items():
        x,y=xy(ref)
        # Outer annulus carries an insulating washer or a qualified compressed
        # O-ring. The central hard-stop land fixes the thermal-pad gap.
        stop=cylinder_at(x,y,m['stop_od'],0,BASE_Z-SUPPORT_RING_INSTALLED)
        stop+=cylinder_at(x,y,m['bore']+1.0,BASE_Z-SUPPORT_RING_INSTALLED,SUPPORT_RING_INSTALLED)
        if m['pilot']:
            stop+=cylinder_at(x,y,m['pilot'],-1.9,1.95)
        stop-=cylinder_at(x,y,m['bore'],-2,BASE_Z+2.1)
        stop.label='custom_POM_stop_'+ref
        stop.color=srgb('#E9DDBC')
        parts.append(stop)
    return parts

def make_support_washers():
    parts=[]
    for ref,m in MOUNTS.items():
        x,y=xy(ref)
        washer=cylinder_at(x,y,m['stop_od'],BASE_Z-SUPPORT_RING_INSTALLED,SUPPORT_RING_INSTALLED)
        washer-=cylinder_at(x,y,m['bore']+1.2,BASE_Z-SUPPORT_RING_INSTALLED-0.1,SUPPORT_RING_INSTALLED+0.2)
        washer.label='insulating_support_washer_'+ref
        washer.color=srgb('#7562A0')
        parts.append(washer)
    return parts
