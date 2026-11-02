from cadgen import step
from fit_common import comparisons
@step(out='../STEP/choc_v2_led_fit.step')
def choc_v2_led_fit():
    return comparisons()
if __name__=='__main__':
    choc_v2_led_fit()
