* U2 pin order EN3 IN1 OUT5 GND2; EN tied +5V on board.
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
