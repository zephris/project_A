from cadgen import step,build123d as bd
from option_common import hardware_parts
@step(out='../STEP/option_hardware.step')
def option_hardware():
    return bd.Compound(children=hardware_parts(),label='option_retainer_hardware_envelopes')
if __name__=='__main__':option_hardware()
