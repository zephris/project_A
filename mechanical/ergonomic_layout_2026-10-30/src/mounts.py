from cadgen import step,stl
from common import *

@stl(out='../STL/mounts.stl')
@step(out='../STEP/mounts.step')
def mounts():
    return bd.Compound(children=[*screen_posts(),*plate_posts()],label='custom_insulating_screen_and_plate_mounts')

if __name__=='__main__':mounts()
