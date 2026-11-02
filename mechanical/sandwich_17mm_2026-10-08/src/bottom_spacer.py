from cadgen import step,stl
from common import *

@stl(out='../STL/bottom_spacer.stl')
@step(out='../STEP/bottom_spacer.step')
def bottom_spacer():
    return bottom_spacer_shape()

if __name__=='__main__':bottom_spacer()
