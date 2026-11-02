from cadgen import dxf
from switch_coupon import profile

@dxf(out='../DXF/switch_coupon.dxf')
def switch_coupon_cut():return profile()

if __name__=='__main__':switch_coupon_cut()
