from cadgen import step, build123d as bd, srgb
from heatsink_plate import heatsink_plate
from heatsink_common import make_pads, make_stops, make_support_washers, PROJECT, constraints

@step(out='../STEP/heatsink_fit.step')
def heatsink_fit():
    # Saved assembly is transformed to PCB-front=0 by a measured registration.
    import json
    from cadgen import read_step
    registration=json.loads((PROJECT/'registration.json').read_text())
    board=read_step(str(PROJECT/'reference/board.step'))
    board=board.moved(bd.Location((0,0,-registration['front_z_native_mm'])))
    board.label='PHBox_ChocV2_current_board_reference'
    return bd.Compound(children=[board,heatsink_plate(),*make_pads(),*make_stops(),*make_support_washers()],label='heatsink_fit')

if __name__ == '__main__':
    heatsink_fit()
