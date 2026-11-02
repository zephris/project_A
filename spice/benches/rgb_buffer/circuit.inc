* TI typical 25C buffer; LED input capacitance is assumed.
.include "u6.lib"
.param vcc=5 c_led=15p
Vcc vcc 0 {vcc}
Vgpio gpio 0 PULSE(0 3.3 1u 10n 10n 500n 1.25u)
* DBV pin order Y4 A2 VCC5 GND3; NC1 unused.
XU6 buffered gpio vcc 0 SN74LV1T34
R14 buffered led_in 510
Cled led_in 0 {c_led}
Rload led_in 0 1Meg
