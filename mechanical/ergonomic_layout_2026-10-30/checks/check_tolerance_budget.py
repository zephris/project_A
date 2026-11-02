"""Deterministic conservative cap-opening allocation; not a supplier guarantee."""
from pathlib import Path
import json,math
HERE=Path(__file__).resolve().parents[1]
d=json.loads((HERE/'tolerance-budget.json').read_text())
p=d['design_acceptance_targets_not_supplier_guarantees']
layout=json.loads((HERE/'layout.json').read_text())
routed_hole_max=p['routed_locator_hole_nominal_diameter_mm']+p['routed_locator_hole_diameter_plus_mm']
guide_min=p['printed_guide_nominal_diameter_mm']-p['printed_guide_diameter_minus_mm']
guide_radial_play=(routed_hole_max-guide_min)/2
locator_registration=math.sqrt(2)*(p['routed_locator_position_per_axis_mm']+p['printed_guide_position_per_axis_mm'])
other_position=math.sqrt(2)*(p['switch_position_per_axis_mm']+p['cap_and_switch_seating_play_per_axis_mm']+p['acrylic_hole_position_per_axis_mm'])
worst_lateral=guide_radial_play+locator_registration+other_position
def margin(hole):
    return ((hole-p['acrylic_hole_diameter_minus_mm']-p['cap_maximum_diameter_mm'])/2)-worst_lateral
required_hole=p['acrylic_hole_diameter_minus_mm']+p['cap_maximum_diameter_mm']+2*(worst_lateral+p['required_remaining_radial_clearance_mm'])
out={
    'units':'mm','source':'../tolerance-budget.json','method':'Worst-case linear addition of radial errors; per-axis position targets converted to radial diagonal bounds. No RSS.',
    'locator_max_hole_diameter_mm':routed_hole_max,'locator_min_guide_diameter_mm':guide_min,
    'maximum_locator_radial_play_mm':guide_radial_play,'locator_registration_radial_allowance_mm':locator_registration,
    'switch_cap_and_acrylic_position_radial_allowance_mm':other_position,'worst_case_lateral_allowance_mm':worst_lateral,
    'former_22p5mm_hole_remaining_radial_clearance_mm':margin(22.5),
    'selected_cover_hole_diameter_mm':layout['cover_hole_diameter_mm'],
    'selected_hole_remaining_radial_clearance_mm':margin(layout['cover_hole_diameter_mm']),
    'required_nominal_hole_diameter_for_target_mm':required_hole,
    'required_remaining_radial_clearance_mm':p['required_remaining_radial_clearance_mm'],
    'conditional_cap_opening_budget_pass':margin(layout['cover_hole_diameter_mm'])>=p['required_remaining_radial_clearance_mm'],
    'supplier_acceptance_and_actual_part_measurements_pending':True,
    'entire_case_tolerance_release':False
}
(HERE/'checks/tolerance-budget.json').write_text(json.dumps(out,indent=2)+'\n')
assert out['conditional_cap_opening_budget_pass']
print(json.dumps(out,indent=2))
