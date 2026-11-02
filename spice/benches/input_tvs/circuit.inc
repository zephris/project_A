* Board cathode pin1 protected input; anode pin2 GND.
.include "d21.lib"
XD21 input 0 ESDA7P120_1U1M
Rleak input 0 1Meg
Itest 0 input PWL(0 0 1u 0 1.01u 0.1 2u 0.1 2.01u 0 3u 0 3.01u -0.1 4u -0.1 4.01u 0)
