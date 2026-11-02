from cadgen import step, stl
from port_seal_common import print_part

@step(out='../STEP/usb_c_collar.step')
@stl(out='../STL/usb_c_collar.stl', mesh_tolerance=0.005)
def usb_c_collar():
    return print_part('C')

if __name__=='__main__': usb_c_collar()
