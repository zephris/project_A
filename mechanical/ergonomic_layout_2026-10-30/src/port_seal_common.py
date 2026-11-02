"""Trial 2 mm unfilled 95A TPU collars; intentional soft contact.

Free-state geometry is shown. Outer edges compress 0.2 mm into the rigid surround;
inner edges interfere nominally0.1 mm with each connector shell. Test pliability,
insertion and foam-mounted board motion before adopting. No environmental rating.
The 0.317 mm relief membrane requires a fine-layer trial print, front face down.
"""
from common import *

def seal_profile(kind):
    outer_w,inner_w,inner_h=(20.4,14.2,5.5) if kind=='A' else (18.4,8.74,3.01)
    ceiling=TOP_INNER if kind=='A' else USB_C_CEILING
    floor=USB_A_THROAT_BOTTOM if kind=='A' else USB_C_FLOOR
    outer_h=ceiling-floor+.4
    centre=(ceiling+floor)/2
    offset=(USB_A_AXIS if kind=='A' else 1.605)-centre
    # True USB-C shell corner is R1.255; 0.1 interference requires R1.155.
    inner_radius=.25 if kind=='A' else 1.155
    return rect(0,0,outer_w,outer_h,.4)-rect(0,offset,inner_w,inner_h,inner_radius)

def seal_parts():
    result=[]
    for kind,x,z in (('A',USB_A_X,(TOP_INNER+USB_A_THROAT_BOTTOM)/2),('C',USB_C_X,(USB_C_CEILING+USB_C_FLOOR)/2)):
        # Seat forward face against spacer lip; trial the outer interference fit.
        s=bd.Pos(x,PORT_SEAL_FRONT,z)*bd.Rot(90,0,0)*bd.extrude(seal_profile(kind),PORT_SEAL_STOCK)
        # Rear rebate clears the entire PCB edge envelope; keep front face intact.
        # This rebate is included in the printable geometry.
        pcb_edge=bounds()[3]+.5+.1
        rear=PORT_SEAL_FRONT-PORT_SEAL_STOCK-.1
        rebate=solid(rect(x,(rear+pcb_edge)/2,24,pcb_edge-rear),FOAM_TOP-TRAVEL-.1,-FOAM_TOP+2*TRAVEL+.2,'PCB_edge_relief','#999999')
        s-=rebate
        s.label=f'trial_TPU95A_USB_{kind}_collar';s.color=srgb('#655F53')
        result.append(s)
    return result

def print_part(kind):
    """Front mating face on Z=0; open rear relief upward without supports."""
    s=seal_parts()[0 if kind=='A' else 1]
    s=bd.Rot(-90,0,0)*s
    b=s.bounding_box()
    s=bd.Pos(-b.min.X,-b.min.Y,-b.min.Z)*s
    s.label=f'USB_{kind}_TPU95A_front_face_down'
    return s
