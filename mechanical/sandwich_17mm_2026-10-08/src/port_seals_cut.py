"""Profile reference only. TPU manufacture uses the separate collar STL files."""
from cadgen import dxf,build123d as bd
from port_seal_common import seal_profile

@dxf(out='../DXF/port_seals.dxf')
def port_seals_cut():
    return seal_profile('A')+bd.Pos(30,0)*seal_profile('C')

if __name__=='__main__':port_seals_cut()
