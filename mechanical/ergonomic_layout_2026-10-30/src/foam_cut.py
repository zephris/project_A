from cadgen import dxf
from common import *

@dxf(out='../DXF/foam.dxf')
def foam_cut():
    return foam_profile()

if __name__=='__main__':foam_cut()
