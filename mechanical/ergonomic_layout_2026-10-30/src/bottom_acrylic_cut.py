from cadgen import dxf
from common import *

@dxf(out='../DXF/bottom_acrylic.dxf')
def bottom_acrylic_cut():
    return bottom_profile()

if __name__=='__main__':bottom_acrylic_cut()
