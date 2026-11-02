from cadgen import step, stl
from port_seal_common import print_part

@step(out='../STEP/usb_a_collar.step')
@stl(out='../STL/usb_a_collar.stl', mesh_tolerance=0.005)
def usb_a_collar():
    return print_part('A')

if __name__=='__main__': usb_a_collar()
