from cadgen import step,stl
from option_common import retainer_shape
@stl(out='../STL/option_retainer.stl')
@step(out='../STEP/option_retainer.step')
def option_retainer():
    return retainer_shape()
if __name__=='__main__':option_retainer()
