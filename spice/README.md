# PHBox KiCad10 SPICE suite

Fourteen isolated test projects under benches/ and matching batch decks. U2/U6/U7/U8/D21 manufacturer models are integrated; Samsung 100nF, 1uF, 4.7uF and C41 models have separate 0V/25C impedance benches. The KEMET bank comparison uses its 5V/25C/100kHz fitted model. Synthetic loads and powered-rail capacitor assumptions remain explicit.

Open a bench .kicad_pro and schematic in KiCad10, then Inspect > Simulator. Load schematic directives; enable full include paths and voltage saving as needed. U2/U6/U7 require PSpice compatibility. Sheets use included decks; avoid duplicating devices with drawn symbols.

Batch commands:

```powershell
python spice/build_suite.py
python spice/run_suite.py --check
python spice/run_suite.py --shared-library 'D:/Program Files/bin/ngspice.dll' --output-dir results/current
python spice/run_suite.py --shared-library 'D:/Program Files/bin/ngspice.dll' --case usb2_startup --sweep --output-dir results/current-corners
```

The generator overwrites benches and suite.json. Edit generators first; rebuild only after reviewing source changes. The runner verifies source and model hashes. Shared-library workers supply PSpice/XSPICE configuration locally.

[Current static-model integration](models/static-integration-2026-10-07.md), [latest results](results_static_retest_2026-10-07.md), [vendor integration](models/integration-2026-10-07.md), and [missing-model coverage](models/conversion-and-coverage-2026-10-07.md).

Saved simulation output sets, including static nominal runs and U2/U6/U7 corners, were removed on 9 October 2026 at the user's request to reduce disk usage. Textual result summaries and model audits remain historical evidence; rerun the suite to recreate raw measurements, logs and machine-readable checks. Source-inventory.json is historical analysis context, not an active pinout/netlist authority. Current schematic and PCB are authoritative.

Execution and repeatability checks passed for all 14 nominal benches. Model/pin mapping, full vendor reference, DC bias, thermal behavior, USB protocol/suspend, core converter and real load behavior remain hardware qualification tasks. Successful SPICE execution does not establish board readiness.

