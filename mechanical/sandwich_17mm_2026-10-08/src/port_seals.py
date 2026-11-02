from cadgen import step,build123d as bd
from port_seal_common import seal_parts

@step(out='../STEP/port_seals.step')
def port_seals():
    return bd.Compound(children=seal_parts(),label='trial_compressible_port_collars')

if __name__=='__main__':port_seals()
