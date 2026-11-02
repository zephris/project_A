from cadgen import step
from heatsink_common import make_plate

@step(out='../STEP/heatsink_plate.step')
def heatsink_plate():
    return make_plate()

if __name__ == '__main__':
    heatsink_plate()
