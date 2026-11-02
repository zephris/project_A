from cadgen import step,stl
from common import *

@step(out='../STEP/foam.step')
def foam():
    return solid(foam_profile(),FOAM_BOTTOM,FOAM_TOP-FOAM_BOTTOM,'lower_relief_foam_2mm_free','#817D71')

if __name__=='__main__':foam()
