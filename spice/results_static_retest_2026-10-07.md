# SPICE retest with static manufacturer models

All 14 nominal benches reran in KiCad's ngspice46 shared library on 2026-10-07. Source and model-file checks passed. Every requested measurement was produced; the accompanying check script validates finite values, positive passive impedances and repeatability against the integration run. This run does not add tolerance corners or hardware acceptance.

Key results:

| Test | Result | Interpretation |
|---|---|---|
| USB host startup | 4.97596V final; 134.027mA peak; crosses 4V at 13.9993ms | Includes enable at 5ms; about 9ms after enable to reach the measurement marker. |
| USB host overload | 134.525mA limiting current; 2.15339V minimum; recovers to 4.97596V | Synthetic overload produces current limiting and recovery. FAULT asserts at 0.02958V and releases to 4.98191V with the bench's 5V pull-up fixture. |
| 3.3V local regulator | 3.29911–3.29986V after load step | Stable in the existing local TI-model fixture; full distributed PDN and thermal behavior excluded. |
| Samsung 4.7uF static | 0.545171ohm at 100kHz; 0.0541563ohm at 1MHz | Fixed 0V/25C frequency-dependent model. |
| Samsung 1uF 0402 static | 2.01408ohm at 100kHz; 0.205716ohm at 1MHz | Fixed 0V/25C comparison. |
| C41 candidate static | 2.03737ohm at 100kHz; 0.207877ohm at 1MHz | CL10B105KA8NNN base model, fixed 0V/25C. |
| KEMET C19+C43 bank | 13.9134mohm impedance magnitude at 100kHz | Two exact vendor networks in parallel at 5V/25C, fitted around 100kHz. Impedance magnitude is not directly equivalent to ESR. |

The retest reproduces the earlier integration measurements. New capacitor models run successfully in their dedicated impedance benches. Samsung DC-bias loss is still not represented in powered-rail tests; KEMET's fitted model is not yet substituted into startup/overload tests. The powered tests therefore retain their documented capacitor assumptions. Remaining unavailable device models and real loads prevent board-level electrical, USB or thermal sign-off.

The simulator reports a missing global spinit file; required compatibility/XSPICE configuration is supplied by the existing per-run worker. All cases executed. Tiny near-zero values, such as the released enable node, are numerical zero rather than physical leakage predictions.

Raw measurements and per-bench logs: results/static-retest-2026-10-07/. Machine-readable checks: results/static-retest-2026-10-07/checks.json.

Cleanup note (9 October 2026): the referenced results/ output directory and checks.json were removed at the user's request. This summary records the historical run; rerun the maintained suite to obtain fresh raw evidence.

