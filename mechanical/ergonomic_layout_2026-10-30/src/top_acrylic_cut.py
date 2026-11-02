from cadgen import dxf
from common import *

@dxf(out='../DXF/top_acrylic.dxf')
def top_acrylic_cut():
    return top_profile()

if __name__=='__main__':top_acrylic_cut()
