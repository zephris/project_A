* Load envelopes are assumptions, not measured firmware behavior.
.param supply=5 cable_r=0.3 cable_l=1u bulk=10u bulk_esr=0.1
.param base_a=0.100 rgb_a=0.189 host_a=0.100
Vsource upstream 0 {supply}
Rcable upstream cable {cable_r}
Lcable cable rail5 {cable_l}
Rbulk rail5 capnode {bulk_esr}
Cbulk capnode 0 {bulk}
Ibase rail5 0 {base_a}
Irgb rail5 0 PULSE(0 {rgb_a} 2m 1u 1u 500u 1m)
Ihost rail5 0 PULSE(0 {host_a} 10m 10u 10u 10m 100m)
