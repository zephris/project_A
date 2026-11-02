from cadgen import dxf
from common import *

@dxf(out='../DXF/upper_foam.dxf')
def upper_foam_cut():
    profile=None
    for x,y,w,h in tabs():
        pad=rect(x,y,w-1,h-2)
        profile=pad if profile is None else profile+pad
    return profile

if __name__=='__main__':upper_foam_cut()
