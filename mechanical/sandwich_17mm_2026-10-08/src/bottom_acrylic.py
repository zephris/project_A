from cadgen import step,stl
from common import *

@step(out='../STEP/bottom_acrylic.step')
def bottom_acrylic():
    return acrylic_shape(False)

if __name__=='__main__':bottom_acrylic()
