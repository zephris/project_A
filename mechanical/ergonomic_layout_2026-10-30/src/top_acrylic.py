from cadgen import step,stl
from common import *

@step(out='../STEP/top_acrylic.step')
def top_acrylic():
    return acrylic_shape(True)

if __name__=='__main__':top_acrylic()
