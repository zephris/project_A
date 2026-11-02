from cadgen import step,build123d as bd
from assembly import parts

def presentation_offset(label):
    """Illustration spacing only; label-based so part-list changes cannot mix layers."""
    layers={
        'bottom_acrylic':-145,'bottom_spacer':-105,'foam':-60,
        'top_acrylic':220,'top_spacer':165,'screen_frame':100,
        'mounts':25,'port_seals':165,'option_caps':220,
        'option_retainer':200,'option_hardware':220,
        'switch_plate':45,'case_hardware':20,
        'bottom_acrylic_2mm':-145,
        'printed_bottom_spacer_and_relief_ledge':-105,
        'current_top_USB_PCB_reference':0,
        'top_acrylic_2mm':220,
        'printed_top_spacer_with_foam_capture_pockets':165,
        'screen_corner_retention_frame':100,
        'custom_insulating_screen_and_plate_mounts':25,
        'trial_compressible_port_collars':165,
        'six_captive_option_button_caps':220,
        'option_cap_retainer_with_M2_nut_pockets':200,
        'option_retainer_hardware_envelopes':220,
    }
    if label in layers:return layers[label]
    if label.startswith('upper_foam'):return 135
    if 'foam' in label:return -60
    if 'thermal_pad' in label:return 75
    if 'support_washer' in label:return 65
    if 'rear_insulating' in label or 'POM_retainer' in label:return -25
    if 'hard_stop' in label or label.startswith(('insulating_stop','custom_POM_stop')):return 35
    if 'heatsink' in label:return 100
    if 'retention' in label or 'switch_plate' in label:return 45
    if 'hardware' in label or 'column' in label:return 20
    raise ValueError('Assign an explicit exploded layer for '+label)

@step(out='../STEP/exploded.step')
def exploded():
    items=parts()
    result=[]
    for i,p in enumerate(items):
        label=p.label
        dz=presentation_offset(label)
        result.append(p.moved(bd.Location((0,0,dz))))
    return bd.Compound(children=result,label='EXPLODED_layer_order_not_installed_heights')

if __name__=='__main__':exploded()
