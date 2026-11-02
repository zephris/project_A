from cadgen import step,stl
from common import *

@stl(out='../STL/top_spacer.stl')
@step(out='../STEP/top_spacer.step')
def top_spacer():
    return top_spacer_shape()

if __name__=='__main__':top_spacer()
