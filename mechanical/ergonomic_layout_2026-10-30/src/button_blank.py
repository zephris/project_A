from cadgen import step,stl
from button_blank_common import installed_blank,invert_for_print

@stl(out='../STL/button_blank.stl',mesh_tolerance=.01)
@step(out='../STEP/button_blank.step')
def button_blank():
    return invert_for_print(installed_blank())

if __name__=='__main__':button_blank()
