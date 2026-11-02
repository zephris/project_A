from cadgen import step,build123d as bd
from button_blank import button_blank
from button_blank_coupon import button_blank_coupon
from button_blank_common import invert_for_print

@step(out='../STEP/button_blank_fit.step')
def button_blank_fit():
    panel=button_blank_coupon().moved(bd.Location((0,0,-2)))
    blank=invert_for_print(button_blank())
    return bd.Compound(children=[panel,blank],label='prototype_blank_in_24mm_faceplate_coupon')

if __name__=='__main__':button_blank_fit()
