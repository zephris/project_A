* ST model terminal order matches package pins 1..6.
.include "u8.lib"
Vrail host5 0 5
* On board pins1/6 HD+ and pins3/4 HD- are each tied together.
XU8 dp 0 dm dm host5 dp USBLC6-2SC6
Rdm dm 0 1Meg
Rdp dp 0 1Meg
Iinject 0 dp PWL(0 0 1u 0 1.01u 0.1 2u 0.1 2.01u 0 3u 0 3.01u -0.1 4u -0.1 4.01u 0)
