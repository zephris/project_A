"""Aluminium-only lumped heat capacity; not a cooling-performance model."""
from pathlib import Path
import json
from cadgen import read_step

HERE=Path(__file__).resolve().parent
DENSITY_KG_M3=2700.0
CP_J_KG_K=896.0

if __name__=='__main__':
    plate=read_step(str(HERE/'STEP/heatsink_plate.step'))
    volume_mm3=plate.volume
    mass_kg=volume_mm3*1e-9*DENSITY_KG_M3
    capacity=mass_kg*CP_J_KG_K
    data={'material':'6061-T6 aluminium','volume_mm3':volume_mm3,
          'density_kg_m3':DENSITY_KG_M3,'specific_heat_J_kg_K':CP_J_KG_K,
          'mass_g':mass_kg*1000,'thermal_mass_J_K':capacity,
          'energy_for_10K_J':capacity*10,'energy_for_20K_J':capacity*20,
          'adiabatic_rise_K_min_at_1W':60/capacity,
          'adiabatic_time_for_10K_s_at_1W':capacity*10,
          'specific_heat_source':'https://publications.anl.gov/anlpubs/2011/06/70320.pdf',
          'scope':'Plate only; constant room-temperature approximation. Excludes PCB, pads, fasteners and washers. Assumes uniform plate temperature. Does not predict steady-state temperature or junction temperatures.'}
    (HERE/'thermal-mass.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
