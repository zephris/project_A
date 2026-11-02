from cadgen import step,dxf
from common import *

def profile():
    p=rect(0,0,78,26)
    for x,a in ((-26,14.05),(0,14.10),(26,14.15)):p-=rect(x,0,a,a)
    return p

@step(out='../STEP/switch_coupon.step')
def switch_coupon():
    return solid(profile(),0,PLATE_THICKNESS,'ChocV2_14p05_14p10_14p15_fit_coupon','#9AABB5')

if __name__=='__main__':switch_coupon()
