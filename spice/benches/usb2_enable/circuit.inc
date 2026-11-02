* Datasheet-bound GPIO/TPS2553 leakage envelope; not firmware execution.
* RPU 32..86k at IOVDD=3.3V. 3.2..3.4V rail is a design envelope.
* R16 total +/-2% allowance includes 1% initial tolerance and temperature drift.
* +/-1.5u combines RP2350 specified 1u input leakage and U7 0.5u EN leakage.
* Runtime release bounds apply to A3/A4; A2 E9 with input enabled is NOT modeled.
* At POR/RUN reset RP2350 input enable is clear, per E9 description.
.param rail_v=3.3 rpu=86k rpd=220k leak_a=1.5u
Vrail rail 0 {rail_v}
R16 en 0 {rpd}
Bileak en 0 I={(leak_a>0) ? leak_a*max(0,min(1,v(en)/0.05)) : leak_a}
Cpad en 0 20p
Bpull en 0 I={(time>5m && time<15m) ? (v(en)-v(rail))/rpu : 0}
* Original 10k divider for regression comparison, enabled throughout.
Roldpull rail old_en {rpu}
Roldpd old_en 0 10k
Boldleak old_en 0 I={(leak_a>0) ? leak_a*max(0,min(1,v(old_en)/0.05)) : leak_a}
