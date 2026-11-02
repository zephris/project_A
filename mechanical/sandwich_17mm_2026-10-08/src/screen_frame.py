from cadgen import step,stl
from common import *

@stl(out='../STL/screen_frame.stl')
@step(out='../STEP/screen_frame.step')
def screen_frame():
    return solid(screen_frame_profile(),4.2,1.0,'screen_corner_retention_frame','#D7C395')

if __name__=='__main__':screen_frame()
