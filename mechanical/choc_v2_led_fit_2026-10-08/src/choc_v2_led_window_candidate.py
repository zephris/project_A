from cadgen import step
from fit_common import window
@step(out='../STEP/choc_v2_led_window_candidate.step')
def choc_v2_led_window_candidate():
    return window()
if __name__=='__main__':
    choc_v2_led_window_candidate()
