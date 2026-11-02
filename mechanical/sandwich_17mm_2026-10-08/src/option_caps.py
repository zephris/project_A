from cadgen import step,stl,build123d as bd
from option_common import cap_parts
@stl(out='../STL/option_caps.stl')
@step(out='../STEP/option_caps.step')
def option_caps():
    return bd.Compound(children=cap_parts(),label='six_captive_option_button_caps')
if __name__=='__main__':option_caps()
