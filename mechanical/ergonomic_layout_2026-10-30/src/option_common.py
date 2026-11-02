"""Case-guided tactile caps; generic KiCad6x6 H5 switches, actual MPN unspecified.

Caps rest on the actuator and follow PCB Z motion, returned by the switch spring.
Retaining flanges hide the board through aperture clearances. Trial fit required.
"""
import math
from common import *
ACTUATOR_HEIGHT=5.0  # change only after selecting/measuring the actual switch

def cap_parts():
    parts=[]
    for i,x in enumerate(OPTION_X,1):
        s=cylinder(x,OPTION_Y,1.4,ACTUATOR_HEIGHT,5.6-ACTUATOR_HEIGHT)
        s+=cylinder(x,OPTION_Y,5.6,5.6,5.3)
        s+=bd.Pos(x,OPTION_Y,10.9)*bd.Cone(2.8,2.6,.3,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN))
        s+=cylinder(x,OPTION_Y,8,6.9,.6)
        s.label=f'OPSW{i}_captive_cap_H5_trial';s.color=srgb('#C9AC6B');parts.append(s)
    return parts

def retainer_shape():
    s=solid(rect((OPTION_X[0]+OPTION_X[-1])/2,OPTION_Y,67,12,1),5.2,1.0,'option_retainer','#A2B7CF')
    for x in OPTION_X:s-=cylinder(x,OPTION_Y,OPTION_GUIDE,5.1,1.2)
    for x,y in option_mounts():
        s+=cylinder(x,y,7,5.2,2.8)
        s-=cylinder(x,y,2.2,5.1,3.0)
        # AF4.4 nut pocket,1.7 deep; M2 nut stand-in AF4,t1.6.
        pocket=bd.Pos(x,y)*bd.RegularPolygon(4.4/math.sqrt(3),6,rotation=30)
        s-=solid(pocket,5.1,1.8,'nut_pocket','#999999')
    s.label='option_cap_retainer_with_M2_nut_pockets';s.color=srgb('#A2B7CF')
    assert s.is_valid
    return s

def hardware_parts():
    parts=[]
    for i,(x,y) in enumerate(option_mounts(),1):
        # Explicit fit envelopes, not vendor CAD. Threads and drive recess omitted.
        s=cylinder(x,y,2,5,5)+cylinder(x,y,4,10,1.6)
        s.label=f'option_retainer_M2x5_pan_screw_envelope_{i}';s.color=srgb('#B7BBC2');parts.append(s)
        p=bd.Pos(x,y)*bd.RegularPolygon(4/math.sqrt(3),6,rotation=30)-disk(x,y,2)
        s=solid(p,5.3,1.6,f'option_retainer_M2_nut_envelope_{i}','#B7BBC2');parts.append(s)
    return parts
