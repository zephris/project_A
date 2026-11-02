from cadgen import step,stl,build123d as bd
from button_blank_common import coupon_shape

@stl(out='../STL/button_blank_coupon.stl',mesh_tolerance=.01)
@step(out='../STEP/button_blank_coupon.step')
def button_blank_coupon():
    return bd.Pos(0,0,2)*coupon_shape()

if __name__=='__main__':button_blank_coupon()
