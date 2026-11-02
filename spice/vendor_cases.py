"""Board-connected vendor-model benches. Loads/parasitics remain envelopes."""
HOST = '''* U7 TI transient model with documented XNOR compatibility repair.
.include "u7.lib"
.param supply=5 cable_r=0.3 r_ilim=200k cout=200u en_delay=5m
.param cap_esr=0.035 load_a=0.060
Vsource upstream 0 PWL(0 0 1m {supply})
Rcable upstream vin {cable_r}
C42 vin 0 100n
Ven en 0 PULSE(0 3.3 {en_delay} 1u 1u 1 2)
* DBV: IN1 GND2 EN3 FAULT4 ILIM5 OUT6; unused model PWPD tied GND.
XU7 vin 0 en 0 fault ilim switched TPS2553_TRANS
R15 ilim 0 {r_ilim}
* FAULT pull-up is a test fixture; firmware GPIO loading not represented.
Rfault vin fault 10k
Vsense switched host 0
Rcap host capnode {cap_esr}
* C19 + C43, 100u each, 70m ESR each => nominal parallel ESR 35m.
Cbank capnode 0 {cout}
C44 host 0 100n
Rbleed host 0 100k
'''

def integrate(cases):
    for c in cases:
        if c['id'] in ('usb2_startup','usb2_overload'):
            old = c['circuit']
            marker = '* Load tapers' if c['id']=='usb2_startup' else 'Vdemand'
            c['circuit'] = HOST + old[old.index(marker):]
            c['sweeps'].pop('ilimit')
            c['sweeps']['r_ilim'] = ['198k','202k']
            c['assets']={'u7.lib':'models/adapters/TPS2553_TRANS_ngspice.lib'}
            c['spice_compatibility']='ps'
            c['model_fidelity']='TI transient model, one documented ngspice compatibility edit; synthetic dongle load'
            c['todo']='Compare against TI reference and physical hardware; thermal/USB protocol qualification remains pending. R15 sweep covers initial 1% resistor tolerance, not all IC current-limit tolerance.'
            if c['id']=='usb2_startup':
                c['measures'] += ['.meas tran host_off FIND v(host) AT=4m']
            else:
                c['measures'] += ['.meas tran limit_current FIND i(Vsense) AT=60m','.meas tran fault_asserted FIND v(fault) AT=60m','.meas tran fault_released FIND v(fault) AT=95m']
        if c['id']=='rail_3v3':
            c['circuit']='''* U2 pin order EN3 IN1 OUT5 GND2; EN tied +5V on board.
.include "u2.lib"
.param supply=5 cout=4.7u cap_esr=0.05 base_a=0.020 step_a=0.050
Vinput vin 0 PWL(0 0 1m {supply})
Cin vin 0 4.7u
* Cin is a local input fixture, not the extracted entire +5V capacitor bank.
XU2 vin vin rail3 0 TLV73333P_TRANS
Resr rail3 capnode {cap_esr}
* C12 alone; distributed MCU/OLED decouplers excluded from this local bench.
C12 capnode 0 {cout}
Ibase rail3 0 {base_a}
Istep rail3 0 PULSE(0 {step_a} 5m 1u 1u 5m 20m)
'''
            c['assets']={'u2.lib':'models/vendor/TLV73333P/tlv73333p_trans.lib'}
            c['sweeps']={'cout':['2.35u','4.7u'],'step_a':['0.025','0.100']}
            c['signals']=['v(rail3)','i(Vinput)']
            c['spice_compatibility']='ps'
            c['model_fidelity']='TI TLV73333P transient model; local C12 and synthetic load'
            c['todo']='Verify effective C12 under bias, distributed decoupling, LDO thermal limits and actual load. Core regulator remains outside this bench.'
    cases.extend([
        dict(id='vendor_bypass_impedance',description='Samsung 100nF base-part model at 0V bias, 25C',
             circuit='''* Model base CL05B104KO5NNN; board stock suffix C is not in library.
* Manufacturer 0V-bias small-signal model, not energized 3.3/5V prediction.
.include "cap.lib"
Itest 0 pdn AC 1
Rleak pdn 0 1G
Xcap pdn 0 CL05B104KO5NNN_Precise_DC0V_25degC
''',analysis='.ac dec 100 1k 100Meg',measures=['.meas ac z_1meg FIND vm(pdn) AT=1Meg','.meas ac z_min MIN vm(pdn)'],sweeps={},signals=['v(pdn)'],assets={'cap.lib':'models/vendor/Samsung/CL05B104KO5NNN_Precise_DC0V_25degC_P.lib'},model_fidelity='Samsung static precise model, 0V DC bias, 25C',todo='Confirm full ordering-code equivalence and obtain biased model before using for energized board PDN. No routing parasitics.'),
        dict(id='input_tvs',description='D21 exact ST model: positive/negative injection fixture',
             circuit='''* Board cathode pin1 protected input; anode pin2 GND.
.include "d21.lib"
XD21 input 0 ESDA7P120_1U1M
Rleak input 0 1Meg
Itest 0 input PWL(0 0 1u 0 1.01u 0.1 2u 0.1 2.01u 0 3u 0 3.01u -0.1 4u -0.1 4.01u 0)
''',analysis='.tran 1n 5u',measures=['.meas tran clamp_positive FIND v(input) AT=1.5u','.meas tran clamp_negative FIND v(input) AT=3.5u'],sweeps={},signals=['v(input)'],assets={'d21.lib':'models/vendor/ESDA7P120-1U1M/ESDA7P120_1U1M.lib'},model_fidelity='ST room-temperature TVS model; artificial 100mA injection',todo='Not surge/ESD certification. Source/fuse/PCB parasitics excluded; vendor model covers room temperature only.'),
        dict(id='rgb_buffer', description='U6 level shifter and R14 first LED input',
             circuit='''* TI typical 25C buffer; LED input capacitance is assumed.
.include "u6.lib"
.param vcc=5 c_led=15p
Vcc vcc 0 {vcc}
Vgpio gpio 0 PULSE(0 3.3 1u 10n 10n 500n 1.25u)
* DBV pin order Y4 A2 VCC5 GND3; NC1 unused.
XU6 buffered gpio vcc 0 SN74LV1T34
R14 buffered led_in 510
Cled led_in 0 {c_led}
Rload led_in 0 1Meg
''', analysis='.tran 1n 5u',
             measures=['.meas tran led_high FIND v(led_in) AT=1.3u','.meas tran led_low FIND v(led_in) AT=1.8u','.meas tran rise_time TRIG v(led_in) VAL=0.5 RISE=1 TARG v(led_in) VAL=4.5 RISE=1'],
             sweeps={'c_led':['5p','30p'],'vcc':['4.75','5']}, signals=['v(gpio)','v(buffered)','v(led_in)'],
             assets={'u6.lib':'models/vendor/SN74LV1T34_SPICE/SN74LV1T34.cir'},spice_compatibility='ps',model_fidelity='TI buffer model; assumed LED load',todo='Actual SK6805 input waveform/threshold and routed parasitics required; no LED firmware model.'),
        dict(id='usb_host_protection',description='U8 USBLC6-2SC6 positive/negative injection fixture',
             circuit='''* ST model terminal order matches package pins 1..6.
.include "u8.lib"
Vrail host5 0 5
* On board pins1/6 HD+ and pins3/4 HD- are each tied together.
XU8 dp 0 dm dm host5 dp USBLC6-2SC6
Rdm dm 0 1Meg
Rdp dp 0 1Meg
Iinject 0 dp PWL(0 0 1u 0 1.01u 0.1 2u 0.1 2.01u 0 3u 0 3.01u -0.1 4u -0.1 4.01u 0)
''', analysis='.tran 1n 5u',measures=['.meas tran clamp_positive FIND v(dp) AT=1.5u','.meas tran clamp_negative FIND v(dp) AT=3.5u'],sweeps={},signals=['v(dp)','v(dm)'],assets={'u8.lib':'models/vendor/USBLC6-2SC6/USBLC6-2SC6.lib'}, model_fidelity='ST ESD array model; artificial 100mA injection',todo='Sanity fixture only: not IEC ESD certification or USB eye/compliance. Supply ideal-clamped; PCB parasitics excluded.')
    ])
