"""Manufacturer fixed-condition impedance benches; not biased-rail predictions."""
def integrate(cases):
    parts = [
        ('vendor_cap_4u7', 'CL05A475MP5NRN', 'C2/C11/C12/C13'),
        ('vendor_cap_1u', 'CL05A105KA5NQN', 'C14/C15'),
        ('vendor_cap_c41', 'CL10B105KA8NNN', 'C41 candidate C29936'),
    ]
    for name, part, refs in parts:
        model = part + '_Precise_DC0V_25degC'
        cases.append(dict(id=name, description=f'{refs}: Samsung static impedance, 0V bias, 25C',
            circuit=f'''* Unbiased comparison only; NOT a powered rail prediction.
.include "cap.lib"
Itest 0 pdn AC 1
Rleak pdn 0 1G
Xcap pdn 0 {model}
''', analysis='.ac dec 100 1k 100Meg',
            measures=['.meas ac z_100k FIND vm(pdn) AT=100k', '.meas ac z_1meg FIND vm(pdn) AT=1Meg', '.meas ac z_min MIN vm(pdn)'],
            sweeps={}, signals=['v(pdn)'], assets={'cap.lib':f'models/vendor/Samsung/{model}_P.lib'},
            model_fidelity='Samsung fixed 0V DC bias, 25C; no PCB parasitics',
            todo='Bias/temperature qualification and ordering suffix equivalence remain pending.'))
    cases.append(dict(id='vendor_kemet_bank', description='C19/C43 exact KEMET parallel bank impedance, 5V/25C',
        circuit='''* Two separate 100uF parts; fixed model fitted around 100kHz.
.include "cap.lib"
Itest 0 pdn AC 1
XC19 pdn 0 T520B107M010ATE070
XC43 pdn 0 T520B107M010ATE070
''', analysis='.ac dec 100 10k 1Meg',
        measures=['.meas ac z_100k FIND vm(pdn) AT=100k', '.meas ac z_min MIN vm(pdn)'],
        sweeps={}, signals=['v(pdn)'], assets={'cap.lib':'models/adapters/T520B107M010ATE070_5V_25C_100kHz.lib'},
        model_fidelity='KEMET fixed 5V/25C/100kHz center-frequency export, two parallel parts',
        todo='Check fitted bandwidth against vendor curves before transient substitution; no tolerance/PCB parasitics.'))
