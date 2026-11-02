from cadgen import dxf
from common import *

@dxf(out='../DXF/switch_plate.dxf')
def switch_plate_cut():
    return plate_profile()

if __name__=='__main__':switch_plate_cut()
