from cadgen import step,read_step,build123d as bd
from common import *
from top_acrylic import top_acrylic
from bottom_acrylic import bottom_acrylic
from top_spacer import top_spacer
from bottom_spacer import bottom_spacer
from switch_plate import switch_plate
from screen_frame import screen_frame
from foam import foam
from mounts import mounts
from case_hardware import case_hardware
from port_seals import port_seals
from option_caps import option_caps
from option_retainer import option_retainer
from option_hardware import option_hardware

def parts():
    reg=json.loads((HEAT/'registration.json').read_text())
    board=read_step(HEAT/'reference/board.step').moved(bd.Location((0,0,-reg['front_z_native_mm'])))
    board.label='current_top_USB_PCB_reference'
    return [bottom_acrylic(),bottom_spacer(),foam(),board,switch_plate(),
            make_plate(),*make_pads(),*make_stops(),*make_support_washers(),*rear_hardware(),
            mounts(),screen_frame(),top_spacer(),*upper_pads(),top_acrylic(),case_hardware(),port_seals(),option_caps(),option_retainer(),option_hardware()]

@step(out='../STEP/assembly.step')
def assembly():
    return bd.Compound(children=parts(),label='PHBox_17mm_foam_sandwich_candidate')

if __name__=='__main__':assembly()
