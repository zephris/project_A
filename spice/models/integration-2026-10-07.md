# Manufacturer model integration, 2026-10-07

U2, U6, U7, U8 and D21 now have manufacturer models in the isolated board test suite. Samsung's 100nF base-part model has a separate unbiased AC comparison bench. The production schematic and PCB electrical design were not changed.

## U7 investigation

The original TPS2553 model parses in ngspice 46 but produces no output: EN is 3.3V, both inputs of its internal enable XNOR are 1V, yet the XNOR output is 0V. The original behavioral expression uses PSpice's `^` XOR syntax. Isolated truth-table measurements in `u7_investigation_2026-10-07/xnor_comparison.json` give original outputs 1,1,1,0 for inputs 00,01,10,11, versus required XNOR outputs 1,0,0,1.

`adapters/TPS2553_TRANS_ngspice.lib` rewrites just that expression using nested IFs. Original TI content, copyright and disclaimer are preserved; the original downloaded file remains untouched. `create_u7_adapter.py` asserts the exact original expression before replacement. The adapted truth table passes all four states and its isolated startup probe gives 4.995V into 100ohms. This identifies a simulator translation problem; it does not establish a hardware defect.

Reviewed DBV model mapping: IN1, GND2, EN3, model-only unused PWPD tied GND, FAULT4, ILIM5, OUT6. PWPD appears only in the original signature. This is TPS2553 active-high, automatic recovery, not TPS2553-1 latch-off. R15 is 200k 1% on the current PCB; the model's nominal internal current limit is 128.15mA, replacing the old abstraction's 137mA. The 198k/202k sweep covers resistor initial tolerance only.

## Current board mapping review

U2 EN3 and IN1 both connect +5V, OUT5 +3V3, GND2 ground; NC4 omitted. C12 is 4.7uF on +3V3; C2 is on the core +1V1 rail and must not be assigned to U2. The local LDO bench uses C12, an explicit input-capacitor fixture, and synthetic load steps; distributed decoupling remains excluded. U2's vendor header references TLV713 despite the official TLV73333P download: nominal execution is verified, complete model accuracy remains pending.

U6 Y4 feeds R14=510ohms then /LED_DATA_IN, A2 RGB, VCC5 +5V, GND3 ground; NC1 omitted. LED input capacitance 5–30pF is an assumption. TI describes typical 25C model behaviour.

U8 follows package pins 1..6: 1/6 HD+, 3/4 HD-, 2 ground, 5 USB_HOST_5V. Its fixture ties paired signal pins as the actual PCB does. D21 pin1 cathode protects Net-(D21-K), pin2 anode ground. Both protection benches use artificial positive/negative 100mA current injection. They are not IEC ESD, surge or USB compliance tests.

## Direct downloads

- U6 SPICE: https://www.ti.com/lit/zip/sclm180 ; optional IO-only IBIS: https://www.ti.com/lit/zip/sclm119 .
- U8 exact ST model: https://www.st.com/resource/en/spice_model/usblc6-2sc6_pspice.zip . Retrieved from the live USBLC6-2 CAD Resources tab.
- D21 exact ST model: https://www.st.com/resource/en/spice_model/esda7p120_1u1m.zip . Retrieved from the live ESDA7P120-1U1M CAD Resources tab.
- Samsung static PSpice library: https://weblib.samsungsem.com/resources/file/support/software_library/Samsung_PSPICE_Static_Library.zip . June 2026 library downloaded and exact base CL05B104KO5NNN extracted. The model is 0V DC bias, 25C, 100Hz–6GHz; the board's stock ordering suffix C is absent from the library. Do not use this unbiased model as an energized-board capacitance prediction without confirming ordering-code equivalence and bias data.

## Extended manufacturer search

| Parts | Manufacturer source checked | Outcome and suite handling |
|---|---|---|
| U1 RP2350 | https://pip.raspberrypi.com/categories/1214-rp2350 | No exact public SPICE verified. Retain GPIO leakage/load envelopes; firmware is not simulated. |
| U3 W25Q128JVS | Winbond exact W25Q128JVSIQ documentation listing, saved `vendor/Winbond-IBIS-list.html` | Exact candidate SOP8 IBIS ZIP is locked behind sign-in. No public exact SPICE verified. IBIS cannot simulate internal flash/firmware operation. |
| U4 ECMF2-40A100N6 | https://www.st.com/en/protections-and-emi-filters/ecmf2-40a100n6.html | Exact resource list has CAD files, no exact public SPICE verified. No unrelated family model substituted. |
| U5 HS13L03W2C01 | Hansheng https://www.hslcm.com | Manufacturer site retrieval timed out. No exact model verified; OLED remains load envelope. |
| D1–D20 SK6805-EC15 | OPSCO https://www.opscoled.com | Manufacturer site retrieval timed out. No exact model verified; LED load/receiver capacitance remains assumption. |
| F1 SMD0805-075-12V | SEA&LAND/ALPHA-TOP https://www.sealand-pptc.com ; datasheet supplier identity versus TECHFUSE distributor field | Manufacturer site accessible, no exact electrothermal SPICE verified. Fuse trip behaviour remains unsimulated. |
| Y1 ABM8-272-T3 | https://abracon.com/datasheets/ABM8-272-T3.pdf | Exact 12MHz crystal drawing specifies ESR/C0/load capacitance, not a complete motional model. No unrelated crystal substituted. |
| L1 AOTA-B201610S3R3-101-T | https://abracon.com/parametric/inductors/AOTA-B201610S3R3-101-T | Exact product page exposes datasheet/drawing/3D models; no exact downloadable SPICE verified. RP2350 core regulator remains a missing bench. |
| Samsung MLCCs | https://weblib.samsungsem.com/index.do?designSupportTools=Pspice | Downloaded static library and integrated 100nF base model into unbiased comparison. Other exact MPNs and biased exports remain pending. |
| C19/C43 T520B107M010ATE070 | https://ksim3.kemet.com/?pn=T520B107M010ATE070 ; KEMET/YAGEO model download instructions | Exact condition-specific K-SIM export not retrieved. Host bank remains 200uF with nominal parallel ESR35mohms and capacitance envelope. |
| Uni-Royal resistors | https://www.uni-royal.cn/en/download_category.php | Manufacturer download catalogue checked; exact SPICE not verified. Built-in R primitives and known tolerance suffice for these low-frequency fixtures. |
| C41 generic capacitor | Current board fields | Exact MPN not selected; no exact vendor model can be assigned. |
| Switches, connectors, mounting holes | Current electrical roles | Ideal contact/connectivity primitives; holes excluded. High-frequency connector parasitics are not represented. |

"Not verified" is not proof that private models do not exist. No supplier was contacted or account created.

## Execution and interpretation

Final nominal execution: `../results/vendor-final-2026-10-07/report.json`. Selected U2/U6/U7 corner execution: `../results/vendor-corners-2026-10-07/report.json`, plus U7 FAULT/current measurements in `../results/vendor-u7-final-corners-2026-10-07/report.json`. Original failing U7 probe remains as historical evidence.

Nominal U7 host output is 4.97596V, crosses 4V near 14ms (enable at 5ms), and recovers to 4.97596V after a 250mA requested overload. The synthetic load tapers below 4V, so current-limited output falls to about 2.15V instead of forcing a negative rail. U2 local load-step rail is about 3.2991–3.2999V. U6 LED input is 4.997V, low approximately zero, nominal 10–90% rise18.2ns; selected supply/capacitance corners rise6.0–47.0ns. U8 fixture clamps at +6.101/-1.111V; D21 at +6.925/-0.329V for 100mA. These are fixture responses, not guaranteed silicon limits.

Samsung unbiased 100nF model gives impedance1.971ohms at1MHz versus1.586ohms in the old ideal/assumed-ESL bench. The difference illustrates why manufacturer parasitics matter, but does not establish powered-board PDN performance.

Broad model regression checks are in `../results/vendor-final-2026-10-07/sanity_checks.json`; they do not qualify manufacturing, USB compliance, thermal safety or firmware operation. Vendor reference reproduction and hardware correlation remain pending.

## Reproduction / KiCad10

From the project directory:

```powershell
& 'D:/Program Files/bin/python.exe' spice/build_suite.py
& 'D:/Program Files/bin/python.exe' spice/run_suite.py --check
& 'D:/Program Files/bin/python.exe' spice/run_suite.py --shared-library 'D:/Program Files/bin/ngspice.dll' --output-dir results/recheck
```

The worker loads installed KiCad XSPICE code libraries and sets PSpice compatibility for flagged benches; no global installation/settings changed. Asset SHA256 checks reject changed source or staged model files. Source hashes were refreshed only after current U2/U6/U7/U8/D21 board pin-net/value review.

For GUI simulation open the bench's `.kicad_sch`, use its local `circuit.inc`, and enable **PSpice compatibility** for U2/U6/U7 benches before running. The batch runs are verified; KiCad GUI compatibility/loading is not separately verified. The suite includes local model copies so nested includes remain portable. Retain original vendor terms; D21 specifically restricts unauthorized reproduction/communication. Do not include vendor models in public/manufacturing redistribution bundles without checking permissions.
