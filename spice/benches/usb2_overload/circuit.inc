* U7 TI transient model with documented XNOR compatibility repair.
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
Vdemand demand 0 PWL(0 0 10m 0 10.01m 0.060 40m 0.060 40.01m 0.250 65m 0.250 65.01m 0.060)
Bload host 0 I={v(demand)*max(0,min(1,v(host)/4))}
