"""Metal hardware stays outside PCB. Threads are symbolic mating interfaces."""
import math
from cadgen import step,read_step,build123d as bd,srgb
from common import *

@step(out='../STEP/case_hardware.step')
def case_hardware():
    screw=read_step(HERE/'imported/ISO10642_M3x6.step')
    parts=[]
    for i,(x,y) in enumerate(bolts(),1):
        # Manufacturer-specified Harwin R30-1001202 envelope: AF5, body12.
        # Catalog female/female records had inconsistent male/female metadata;
        # this is a dimensioned stand-in, not a vendor STEP or threaded simulation.
        barrel=bd.Pos(x,y,-4.5)*bd.extrude(bd.RegularPolygon(5/math.sqrt(3),6),12)
        barrel-=cylinder(x,y,2.5,-4.6,12.2)
        barrel.label=f'Harwin_R30_1001202_dimensioned_standoff_{i}_threads_omitted'
        barrel.color=srgb('#C3A564');parts.append(barrel)
        for z,end in ((-5,'bottom'),(7.5,'top')):
            washer=cylinder(x,y,7,z,.5)-cylinder(x,y,3.4,z-.1,.7)
            washer.label=f'M3_flat_washer_{i}_{end}_7x3p4x0p5';washer.color=srgb('#C4C9CC');parts.append(washer)
        # ISO10642 catalog head nominal OD6; locate its outer face at acrylic face.
        a=screw.moved(bd.Location((x,y,TOP)));a.label=f'M3x6_case_screw_top_{i}'
        b=screw.moved(bd.Location((0,0,0),(180,0,0))).moved(bd.Location((x,y,BOTTOM)))
        b.label=f'M3x6_case_screw_bottom_{i}'
        parts.extend([a,b])
    return bd.Compound(children=parts,label='continuous_13mm_case_columns_12mm_standoff_plus_two_washers')

if __name__=='__main__':case_hardware()
