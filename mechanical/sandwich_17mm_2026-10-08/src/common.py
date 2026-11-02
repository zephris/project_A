"""17 mm sandwich candidate. mm; X=KiCad X, Y=-KiCad Y, front seating Z=0.

Nominal foam preload and tolerances require first-article verification.
The PCB, display and existing heatsink geometry are read-only inputs.
"""
from pathlib import Path
import json,sys
from cadgen import build123d as bd, srgb
HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]
HEAT=HERE.parent/'heatsink_2026-10-08'
sys.path.insert(0,str(HEAT/'src'))
from heatsink_common import make_plate,make_pads,make_stops,make_support_washers
from heatsink_mounting import rear_hardware

ACRYLIC=2.0
BOTTOM=-7.0
BOTTOM_INNER=-5.0
TOP_INNER=8.0
TOP=10.0
FOAM_BOTTOM=-3.25
FOAM_TOP=-1.601204  # saved substrate underside; adjust to finished-board measurements
LOWER_JOIN=-1.85
PLATE_BOTTOM=3.0
PLATE_THICKNESS=1.3
PLATE_TOP=PLATE_BOTTOM+PLATE_THICKNESS
SWITCH_APERTURE=14.10
TRAVEL=0.25
FIT_CLEARANCE=0.60
CAP_HOLE=26.5
USB_A_X=192.0
USB_A_FACE=-34.14  # C2344:12.86 mm ahead of unchanged contact row
USB_A_AXIS=4.15  # OEM7 high,5.7 mating-shell height:1.3..7
USB_C_X=158.43218
USB_BACK=-33.9  # 0.616 mm outward of PCB edge; does not clamp floating board
USB_MOUTH=-24.516558  # main case edge: no projecting USB tray
HOOD_CEILING=TOP_INNER  # connector roof is now the continuous acrylic panel
HOOD_TOP=TOP
USB_OPEN_START=-33.4  # 0.24 mm beyond shell at its outward-most XY pose
USB_A_BODY_SETBACK=2.0  # trial requirement: overmold begins beyond mating face
USB_A_THROAT_BOTTOM=-1.1  # lower mating axis and conservative body offset/travel
USB_C_FLOOR=-3.645
USB_C_CEILING=6.855
USB_C_ROOF_WIDTH=11.0  # shell swept width9.94 +0.53 mm cover margin per side
PORT_SEAL_FRONT=-33.6
PORT_SEAL_STOCK=2.0
PORT_LIP_FRONT=-33.2
PORT_BODY_BACK=-36.4
PORT_RUNNING_CLEARANCE=.2  # beyond shell XY +/-0.5 and Z +/-0.25 travel
USB_A_ACCESS=(15.8,6.6,.2)
USB_C_ACCESS=(10.34,4.11,1.455)  # native HRO cornerR1.255 +0.2 offset
OPTION_X=(217.73218,227.73218,237.73218,250.73218,260.73218,270.73218)
OPTION_Y=-44.016558
OPTION_GUIDE=6.2

def option_mounts():
    return [(244.23218,-50),(244.23218,-38)]

def data():
    d=json.loads((HEAT/'constraints.json').read_text())
    return d,{f['ref']:f for f in d['footprints']}

def bounds():
    r=json.loads((HEAT/'registration.json').read_text())
    return r['substrate']['bounds'][:4]

def xy(ref):
    f=data()[1][ref]
    return f['pcb_xy'][0],-f['pcb_xy'][1]

def rect(x,y,w,h,r=0):
    return bd.Pos(x,y)* (bd.RectangleRounded(w,h,r) if r else bd.Rectangle(w,h))

def disk(x,y,d):
    return bd.Pos(x,y)*bd.Circle(d/2)

def solid(profile,z,h,label,color):
    s=bd.Pos(0,0,z)*bd.extrude(profile,h)
    s.label=label;s.color=srgb(color)
    assert s.is_valid,label
    return s

def cylinder(x,y,d,z,h):
    return bd.Pos(x,y,z)*bd.Cylinder(d/2,h,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))

def board_profile(clearance=0):
    xmin,xmax,ymin,ymax=bounds()
    return rect((xmin+xmax)/2,(ymin+ymax)/2,xmax-xmin+2*clearance,ymax-ymin+2*clearance,5+clearance)

def outside():
    xmin,xmax,ymin,ymax=bounds()
    return rect((xmin+xmax)/2,(ymin+ymax)/2,xmax-xmin+20,ymax-ymin+20,10)

def bolts():
    xmin,xmax,ymin,ymax=bounds()
    return [(xmin-3,ymin-3),(xmax+3,ymin-3),(xmin-3,ymax+3),(xmax+3,ymax+3),
            (xmin-5,(ymin+ymax)/2),(xmax+5,(ymin+ymax)/2),(240,ymax+5),(188,ymin-5)]

def case_holes(p):
    for x,y in bolts():p-=disk(x,y,3.4)
    return p

def acrylic_shape(upper):
    z=TOP_INNER if upper else BOTTOM
    p=top_profile() if upper else bottom_profile()
    s=solid(p,z,ACRYLIC,'top_acrylic_2mm' if upper else 'bottom_acrylic_2mm','#B4D8E4')
    # Secondary 90-degree countersink operation; DXFs hold only through profiles.
    # Catalog head has OD6.0465; allow its short rim as well as the 90-degree cone.
    for x,y in bolts():
        cone=bd.Cone(1.7,3.35,1.65,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN)) if upper else bd.Cone(3.35,1.7,1.65,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))
        s-=bd.Pos(x,y,TOP-1.65 if upper else BOTTOM)*cone
    s.label='top_acrylic_2mm' if upper else 'bottom_acrylic_2mm';s.color=srgb('#B4D8E4')
    return s

def usb_bay_profile():
    return rect(USB_A_X,(USB_BACK+USB_MOUTH)/2,47,USB_MOUTH-USB_BACK)

def bottom_profile():
    return case_holes(outside())

def port_channels():
    # Engineering clearances, not vendor models. C cable overmold gauge 13 x 8.
    c=solid(rect(USB_C_X,-25,18,22),USB_C_FLOOR,USB_C_CEILING-USB_C_FLOOR,'USB_C_clearance','#999999')
    # A bay floor is LOWER_JOIN; throat admits a conservative 15 x 8 dongle body.
    a=solid(rect(USB_A_X,(USB_BACK+USB_MOUTH)/2,43,USB_MOUTH-USB_BACK+.2),LOWER_JOIN,HOOD_CEILING-LOWER_JOIN,'USB_A_finger_bay','#999999')
    return c,a

def ring_profile():
    p=outside()-board_profile(FIT_CLEARANCE)
    for x,y in bolts():p-=disk(x,y,6.5)
    return p

def port_retaining_lips():
    # Seal seats against the rear of these integral webs. Apertures clear shell
    # movement and metal plug noses; overmolds stay forward of the webs.
    y=(PORT_SEAL_FRONT+PORT_LIP_FRONT)/2
    depth=PORT_LIP_FRONT-PORT_SEAL_FRONT
    a=solid(rect(USB_A_X,y,47,depth),LOWER_JOIN,TOP_INNER-LOWER_JOIN,'A_seal_retaining_lip','#A2B7CF')
    a-=port_access_cut('A',PORT_SEAL_FRONT-.1,PORT_LIP_FRONT+.1)
    c=solid(rect(USB_C_X,y,22,depth),USB_C_FLOOR,USB_C_CEILING-USB_C_FLOOR,'C_seal_retaining_lip','#A2B7CF')
    c-=port_access_cut('C',PORT_SEAL_FRONT-.1,PORT_LIP_FRONT+.1)
    return a,c

def port_access_cut(kind,rear,front):
    x,axis=(USB_A_X,USB_A_AXIS) if kind=='A' else (USB_C_X,1.605)
    w,h,r=USB_A_ACCESS if kind=='A' else USB_C_ACCESS
    # Closed XZ outline, extruded rearwards from the front of the requested range.
    return bd.Pos(x,front,axis)*bd.Rot(90,0,0)*bd.extrude(rect(0,0,w,h,r),front-rear)

def port_body_collars():
    # Thick side cheeks register around the forward shell, not against the PCB.
    # The floor starts 0.1 mm above the highest allowed PCB seating plane.
    y=(PORT_BODY_BACK+PORT_SEAL_FRONT)/2
    d=PORT_SEAL_FRONT-PORT_BODY_BACK
    a=solid(rect(USB_A_X,y,18.2,d),TRAVEL+.1,TOP_INNER-TRAVEL-.1,'A_shell_side_cheeks','#A2B7CF')
    # USB-A remains acrylic-roofed: cheeks are open above the shell.
    a-=solid(rect(USB_A_X,y,USB_A_ACCESS[0],d+.2),TRAVEL+.05,TOP_INNER-TRAVEL,'A_open_roof_shell_clearance','#999999')
    c=solid(rect(USB_C_X,y,14,d),TRAVEL+.1,TOP_INNER-TRAVEL-.1,'C_contoured_shell_collar','#A2B7CF')
    c-=port_access_cut('C',PORT_BODY_BACK-.1,PORT_SEAL_FRONT+.1)
    return a,c

def tabs():
    xmin,xmax,ymin,ymax=bounds()
    return [(xmin-2,-105,8,20),(xmin-2,-175,8,20),
            (xmax+2,-105,8,20),(xmax+2,-175,8,20),
            (120,ymin-2,20,8),(250,ymin-2,20,8)]

def tab_profiles(clearance=0):
    p=None
    for x,y,w,h in tabs():
        r=rect(x,y,w+2*clearance,h+2*clearance)
        p=r if p is None else p+r
    return p

def plate_profile():
    xmin,xmax,ymin,ymax=bounds()
    # The electronics area is open. H7 tongue gets an open-edge semicircular relief.
    p=(rect((xmin+xmax)/2,(ymin-80)/2,xmax-xmin,-80-ymin) & board_profile())+tab_profiles()
    for n in range(1,17):
        x,y=xy(f'SW{n}');p-=rect(x,y,SWITCH_APERTURE,SWITCH_APERTURE)
    x,y=xy('H7');p-=disk(x,y,18)
    for ref in ('H1','H2','H3'):
        x,y=xy(ref);p-=disk(x,y,3.4)
    return p

def relieved_support_area():
    # Tray floor footprint has conservative holes around all rear features.
    p=board_profile(-0.8)
    _,fps=data()
    for n in range(1,17):
        x,y=xy(f'SW{n}');p-=rect(x,y,22,20,1)
    p-=rect(163,-64,88,62,2)  # hot electronics and heatsink rear retainers
    p-=rect(100.3,-54,38.4,36.5,2)  # OLED tails and posts
    # Six option-button solder tails extend through the PCB; footprint side is F.
    for x in (217.73218,227.73218,237.73218,250.73218,260.73218,270.73218):
        p-=rect(x,-44.016558,6.8,8.0,.3)
    for ref,f in fps.items():
        if f['side']=='B':
            x,y,w,h=f['bbox_xy'];p-=rect(x+w/2,-y-h/2,w+2,h+2,0.3)
        if ref.startswith('H'):
            x,y=xy(ref);d=max((pad['drill_mm'][0] for pad in f['pads']),default=2.2)
            p-=disk(x,y,d+3.0)
    return p

def foam_profile():
    xmin,xmax,ymin,ymax=bounds()
    p=None
    for x,y,w,h in ((xmin+5,-105,8,18),(xmin+5,-175,8,18),
                     (xmax-5,-105,8,18),(xmax-5,-175,8,18),
                     (120,ymin+5,18,8),(250,ymin+5,18,8),
                     (*xy('H2'),18,18)):
        r=rect(x,y,w,h,.4)
        p=r if p is None else p+r
    return p & relieved_support_area()

def top_profile():
    p=case_holes(outside())
    for n in range(1,17):
        x,y=xy(f'SW{n}');p-=disk(x,y,CAP_HOLE)
    # BOOTSEL/RESET remain below acrylic; the existing heatsink notch stays clear.
    p-=rect(100.3,-54,30,25,1)
    for x,y in screen_holes():p-=disk(x,y,6)
    # Individual captive-plunger apertures replace the exposed option-button slot.
    for x in OPTION_X:p-=disk(x,OPTION_Y,OPTION_GUIDE)
    for x,y in option_mounts():p-=disk(x,y,2.2)
    # Acrylic shields the shell; only the external dongle pocket is open above.
    p-=rect(USB_A_X,(USB_OPEN_START+USB_MOUTH)/2,47.4,USB_MOUTH-USB_OPEN_START)
    # Vent slots over aluminium, avoiding service and support screw locations.
    for x in (143,150,157,164,171,178):p-=rect(x,-65,3,18,1)
    for ref in ('H5','H7','H12'):
        x,y=xy(ref);p-=disk(x,y,8 if ref!='H12' else 6)
    return p

def screen_holes():
    return [(p['pcb_xy'][0],-p['pcb_xy'][1]) for p in data()[1]['U5']['pads'] if not p['number']]

def screen_frame_profile():
    # Frame sits beside the module. Four corner ears retain its PCB, never the glass.
    p=rect(100.3,-54,40.4,38.5,2)-rect(100.3,-54,35.9,34.0,0.2)
    for x,y in screen_holes():
        p+=rect(x,y,6,6,0.6)
    # Glass/viewing surface and header remain clear.
    p-=rect(100.3,-54,34.6,24.4,0.5)
    p-=rect(100.3,-39.25,13,5)
    for x,y in screen_holes():p-=disk(x,y,2.4)
    return p

def screen_posts():
    parts=[]
    for i,(x,y) in enumerate(screen_holes(),1):
        s=cylinder(x,y,4.8,0,3.0)
        s+=cylinder(x,y,2.7,-1.55,1.55)
        s-=cylinder(x,y,2.2,-2.0,5.2)
        s.label=f'printed_screen_stop_{i}_3mm';s.color=srgb('#D7C395');parts.append(s)
        cap=cylinder(x,y,4.8,FOAM_TOP-1.25,1.25)-cylinder(x,y,1.7,FOAM_TOP-1.35,1.5)
        cap.label=f'printed_screen_rear_tapped_cap_{i}_M2';cap.color=srgb('#D7C395');parts.append(cap)
    return parts

def plate_posts():
    parts=[]
    for ref in ('H1','H2','H3'):
        x,y=xy(ref)
        s=cylinder(x,y,8,0,PLATE_BOTTOM)+cylinder(x,y,6.1,-1.55,1.60)
        s-=cylinder(x,y,3.4,-2,PLATE_BOTTOM+2.2)
        s.label='insulating_plate_stop_'+ref;s.color=srgb('#D7C395');parts.append(s)
        c=cylinder(x,y,8,FOAM_TOP-2.0,2.0)-cylinder(x,y,2.5,FOAM_TOP-2.1,2.2)
        c.label='insulating_plate_rear_tapped_cap_'+ref;c.color=srgb('#D7C395');parts.append(c)
    return parts

def upper_pads():
    # Capture pads are shorter than tabs so they leave wall and edge clearance.
    parts=[]
    for i,(x,y,w,h) in enumerate(tabs(),1):
        p=rect(x,y,w-1,h-2)
        parts.append(solid(p,PLATE_TOP,1.2,f'upper_foam_capture_pad_{i}','#817D71'))
    return parts

def bottom_spacer_shape():
    # Carrier follows the relieved foam footprint; openings continue to bottom acrylic.
    wall=solid(ring_profile(),BOTTOM_INNER,LOWER_JOIN-BOTTOM_INNER,'wall','#AEBCD0')
    # Extend ledge to outer walls, then cut the same keepouts from a larger outline.
    ledge=relieved_support_area()+(outside()-board_profile(-0.8))
    ledge=case_holes(ledge)
    s=wall+solid(ledge,BOTTOM_INNER,FOAM_BOTTOM-BOTTOM_INNER,'ledge','#AEBCD0')
    # Two loose round guides constrain XY only; no screws pass through PCB here.
    for ref in ('H4','H6'):
        x,y=xy(ref)
        s+=cylinder(x,y,7.5,BOTTOM_INNER,FOAM_BOTTOM-BOTTOM_INNER)
        s+=cylinder(x,y,5.4,FOAM_BOTTOM,3.65)
        # Link the guide base to the outer ledge without bearing on the PCB.
        xmin,xmax,_,_=bounds();edge=xmin-1 if ref=='H6' else xmax+1
        s+=solid(rect((x+edge)/2,y,abs(x-edge)+7,7),BOTTOM_INNER,1.75,'link','#AEBCD0')
    for x,y in bolts():
        s-=cylinder(x,y,6.5,BOTTOM_INNER-.1,3.3)
        s-=cylinder(x,y,7.3,BOTTOM_INNER-.1,.65)
    # Continuous bay floor and closed lower wall; only the C tunnel passes through.
    s+=solid(usb_bay_profile(),BOTTOM_INNER,LOWER_JOIN-BOTTOM_INNER,'bay_floor','#AEBCD0')
    c,_=port_channels();s-=c
    _,lip=port_retaining_lips()
    # Split the USB-C web on the existing case parting plane.
    s+=lip & solid(rect(USB_C_X,-33.4,24,1),USB_C_FLOOR,LOWER_JOIN-USB_C_FLOOR,'lower_lip_clip','#999999')
    s.label='printed_bottom_spacer_and_relief_ledge';s.color=srgb('#A2B7CF')
    return s

def top_spacer_shape():
    s=solid(ring_profile(),LOWER_JOIN,TOP_INNER-LOWER_JOIN,'upper_wall','#A2B7CF')
    # Pockets clear the complete tab and allow +/-0.25 mm motion.
    s-=solid(tab_profiles(.6),PLATE_BOTTOM-TRAVEL,2.5+TRAVEL,'tab_pocket','#A2B7CF')
    # Wall ledges overhang each foam pad, restoring the material above pockets.
    for x,y,w,h in tabs():
        s+=solid(rect(x,y,w+.4,h+.4),PLATE_TOP+1.2,TOP_INNER-PLATE_TOP-1.2,'capture_ledge','#A2B7CF')
    # Spacer provides sidewalls and acrylic supports, with no printed roof.
    outer=solid(usb_bay_profile(),LOWER_JOIN,TOP_INNER-LOWER_JOIN,'USB_A_sidewalls','#A2B7CF')
    c,a=port_channels()
    outer-=a
    # Open outward mouth, retaining sidewalls beneath the acrylic edge.
    outer-=solid(rect(USB_A_X,USB_MOUTH,43,.4),LOWER_JOIN,HOOD_CEILING-LOWER_JOIN,'mouth','#999999')
    s+=outer
    s-=c;s-=a
    # Narrow throat closes the surround behind the generous finger pocket.
    throat=solid(rect(USB_A_X,USB_BACK+.75,47,1.5),LOWER_JOIN,TOP_INNER-LOWER_JOIN,'USB_A_surround','#A2B7CF')
    throat-=solid(rect(USB_A_X,USB_BACK+.75,20,1.7),USB_A_THROAT_BOTTOM,TOP_INNER-USB_A_THROAT_BOTTOM+.1,'USB_A_throat','#999999')
    s+=throat
    a_lip,c_lip=port_retaining_lips()
    s+=a_lip
    s+=c_lip & solid(rect(USB_C_X,-33.4,24,1),LOWER_JOIN,TOP_INNER-LOWER_JOIN,'upper_lip_clip','#999999')
    a_collar,c_collar=port_body_collars()
    s+=a_collar;s+=c_collar
    # Lower USB-C shell uses an integral printed roof, continuous into the rim.
    # Cover its full native footprint plus the allowed +/-0.5 mm XY motion.
    s+=solid(rect(USB_C_X,-37.4,USB_C_ROOF_WIDTH,10),USB_C_CEILING,TOP_INNER-USB_C_CEILING,'USB_C_integral_connector_roof','#A2B7CF')
    # Open-top pocket starts beyond the acrylic edge; all walls stop at Z=8.
    for x,y in bolts():
        s-=cylinder(x,y,6.5,LOWER_JOIN-.1,10.1)
        s-=cylinder(x,y,7.3,TOP_INNER-.55,.65)
    s.label='printed_top_spacer_with_foam_capture_pockets';s.color=srgb('#A2B7CF')
    return s
