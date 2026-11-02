from cadgen import step,stl
from common import *

@step(out='../STEP/switch_plate.step')
def switch_plate():
    return solid(plate_profile(),PLATE_BOTTOM,PLATE_THICKNESS,'ChocV2_retention_plate_1p3mm','#9AABB5')

if __name__=='__main__':switch_plate()
