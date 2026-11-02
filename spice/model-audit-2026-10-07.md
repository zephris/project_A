> Historical pre-download audit. See models/vendor/README.md for the subsequent model search and intake on 2026-10-07.

# SPICE model installation audit — 2026-10-07

**No complete per-part vendor model set is installed or assigned.** Audited 146 current schematic instances. No explicit Sim.* or Spice_* properties were found anywhere in the root schematic. The project vendor folder contains only its README; six benches use inline primitives and behavioural sources, with no vendor .model/.subckt imports. KiCad bundled example libraries did not contain the board part numbers searched. This checks usable project integration, not every unrelated folder on the computer.

Ngspice 46 DLL at D:/Program Files/bin/ngspice.dll loads and reports its version. A missing spinit warning appears, but DLL initialization succeeds. STEP/3D assets do not supply electrical simulation models.

## Coverage and gaps

| Parts | Available representation | Limitation |
|---|---|---|
| 32 resistors, 44 capacitors, L1 | Built-in R/C/L | No external model required for ideal analysis; individual board parts are not all included in the six benches. Exact ESR/ESL, bias, tolerance, saturation and DCR models are not installed. |
| U7 TPS2553DBVR | Inline Bswitch/Bfault approximations | Exact vendor model missing; real protection/startup/thermal behaviour unverified. |
| U2 TLV73333PDBV | Ideal 3.3 V source plus resistance | Exact regulator model missing; cannot check dropout or stability. |
| U1 RP2350 | Pull-up/leakage envelope and synthetic loads | No MCU/core converter model or firmware execution. |
| U3 W25Q128JVS | None | Exact device/IO model missing. |
| U4 ECMF2-40A100N6 | None | Filter/ESD model or S-parameter network missing. |
| U5 HS13L03W2C01 | Assumed aggregate load only | No exact module model or measured load profile. |
| U6 SN74LV1T34DBVR | None | Exact buffer/IBIS model missing. IBIS would support IO integrity, not complete internal-device behaviour. |
| U8 USBLC6-2SC6 and D21 ESDA7P120-1U1M | None | Clamp/parasitic models missing; ideal or generic diode would not validate ESD survival. |
| D1–D20 SK6805-EC15 | Assumed aggregate RGB load only | No exact driver/controller/PWM or per-LED current model. |
| F1 750 mA hold PPTC | None | No temperature/time-dependent trip model; cable resistance is not a fuse model. |
| Y1 ABM8-272-T3 | None | No selected-crystal equivalent circuit or oscillator startup model. |
| 24 switch/contact references | Built-in ideal switch available | No assignment, bounce or contact-resistance characterization. |
| USB1/USB2 | Ideal connectivity possible | No connector SI/parasitic model; not necessary for basic power-net analysis. |
| H1–H12 | Not electrical | No model required. |

## Existing suite integrity

All six cases have the required entry point and circuit include files, but `run_suite.py --check` exits 1 because current schematic and PCB hashes differ from the suite manifest. Do not just refresh hashes: review circuit values, loading and topology against the current design first. No simulations were rerun and no schematic/model assignments were changed in this audit.

## Priority

1. Qualify and connect U7 TPS2553 and U2 TLV73333 models, checking terminal order and ngspice compatibility against vendor reference circuits.
2. Add a RP2350 core power-converter bench plus realistic MCU, OLED, LED and dongle load envelopes.
3. Add L1 and capacitor nonideal parameters for power analysis; F1 electrothermal behaviour if testing trips.
4. Obtain U6/MCU/flash IO models and U4 network data if signal-integrity analysis is required; add protection models for clamp waveforms, without treating simulation as ESD certification.
5. Review and update bench provenance before running the suite again.

## Per-reference results

| Reference | Value | Status |
|---|---|---|
| C1 | 100n | built in primitive available not explicitly assigned |
| C2 | 4.7u | built in primitive available not explicitly assigned |
| C3 | 100n | built in primitive available not explicitly assigned |
| C4 | 100n | built in primitive available not explicitly assigned |
| C5 | 100n | built in primitive available not explicitly assigned |
| C6 | 100n | built in primitive available not explicitly assigned |
| C7 | 100n | built in primitive available not explicitly assigned |
| C8 | 100n | built in primitive available not explicitly assigned |
| C9 | 100n | built in primitive available not explicitly assigned |
| C10 | 100n | built in primitive available not explicitly assigned |
| C11 | 4.7u | built in primitive available not explicitly assigned |
| C12 | 4.7u | built in primitive available not explicitly assigned |
| C13 | 4.7u | built in primitive available not explicitly assigned |
| C14 | 1u | built in primitive available not explicitly assigned |
| C15 | 1u | built in primitive available not explicitly assigned |
| C16 | 15p | built in primitive available not explicitly assigned |
| C17 | 15p | built in primitive available not explicitly assigned |
| C18 | 100n | built in primitive available not explicitly assigned |
| C19 | 100u/10V | built in primitive available not explicitly assigned |
| C20 | 100n | built in primitive available not explicitly assigned |
| C21 | 100n | built in primitive available not explicitly assigned |
| C22 | 100n | built in primitive available not explicitly assigned |
| C23 | 100n | built in primitive available not explicitly assigned |
| C24 | 100n | built in primitive available not explicitly assigned |
| C25 | 100n | built in primitive available not explicitly assigned |
| C26 | 100n | built in primitive available not explicitly assigned |
| C27 | 100n | built in primitive available not explicitly assigned |
| C28 | 100n | built in primitive available not explicitly assigned |
| C29 | 100n | built in primitive available not explicitly assigned |
| C30 | 100n | built in primitive available not explicitly assigned |
| C31 | 100n | built in primitive available not explicitly assigned |
| C32 | 100n | built in primitive available not explicitly assigned |
| C33 | 100n | built in primitive available not explicitly assigned |
| C34 | 100n | built in primitive available not explicitly assigned |
| C35 | 100n | built in primitive available not explicitly assigned |
| C36 | 100n | built in primitive available not explicitly assigned |
| C37 | 100n | built in primitive available not explicitly assigned |
| C38 | 100n | built in primitive available not explicitly assigned |
| C39 | 100n | built in primitive available not explicitly assigned |
| C40 | 100n | built in primitive available not explicitly assigned |
| C41 | 1u/10V/X7R | built in primitive available not explicitly assigned |
| C42 | 100n | built in primitive available not explicitly assigned |
| C43 | 100u/10V | built in primitive available not explicitly assigned |
| C44 | 100n | built in primitive available not explicitly assigned |
| D1 | SK6805-EC15 | aggregate load envelope only |
| D2 | SK6805-EC15 | aggregate load envelope only |
| D3 | SK6805-EC15 | aggregate load envelope only |
| D4 | SK6805-EC15 | aggregate load envelope only |
| D5 | SK6805-EC15 | aggregate load envelope only |
| D6 | SK6805-EC15 | aggregate load envelope only |
| D7 | SK6805-EC15 | aggregate load envelope only |
| D8 | SK6805-EC15 | aggregate load envelope only |
| D9 | SK6805-EC15 | aggregate load envelope only |
| D10 | SK6805-EC15 | aggregate load envelope only |
| D11 | SK6805-EC15 | aggregate load envelope only |
| D12 | SK6805-EC15 | aggregate load envelope only |
| D13 | SK6805-EC15 | aggregate load envelope only |
| D14 | SK6805-EC15 | aggregate load envelope only |
| D15 | SK6805-EC15 | aggregate load envelope only |
| D16 | SK6805-EC15 | aggregate load envelope only |
| D17 | SK6805-EC15 | aggregate load envelope only |
| D18 | SK6805-EC15 | aggregate load envelope only |
| D19 | SK6805-EC15 | aggregate load envelope only |
| D20 | SK6805-EC15 | aggregate load envelope only |
| D21 | ESDA7P120-1U1M | missing device model |
| F1 | 750mA hold | missing device model |
| H1 | MountingHole | not electrical |
| H2 | MountingHole | not electrical |
| H3 | MountingHole | not electrical |
| H4 | MountingHole | not electrical |
| H5 | MountingHole | not electrical |
| H6 | MountingHole | not electrical |
| H7 | MountingHole | not electrical |
| H8 | MountingHole | not electrical |
| H9 | MountingHole | not electrical |
| H10 | MountingHole | not electrical |
| H11 | MountingHole | not electrical |
| H12 | MountingHole | not electrical |
| L1 | 3.3u | built in primitive available not explicitly assigned |
| OPSW1 | SW_Push | ideal switch primitive available not assigned |
| OPSW2 | SW_Push | ideal switch primitive available not assigned |
| OPSW3 | SW_Push | ideal switch primitive available not assigned |
| OPSW4 | SW_Push | ideal switch primitive available not assigned |
| OPSW5 | SW_Push | ideal switch primitive available not assigned |
| OPSW6 | SW_Push | ideal switch primitive available not assigned |
| R1 | 33 | built in primitive available not explicitly assigned |
| R2 | 27 | built in primitive available not explicitly assigned |
| R3 | 27 | built in primitive available not explicitly assigned |
| R4 | 1k | built in primitive available not explicitly assigned |
| R5 | 22 | built in primitive available not explicitly assigned |
| R6 | 1k | built in primitive available not explicitly assigned |
| R7 | 22 | built in primitive available not explicitly assigned |
| R8 | 1k | built in primitive available not explicitly assigned |
| R10 | 5.1k | built in primitive available not explicitly assigned |
| R11 | 5.1k | built in primitive available not explicitly assigned |
| R12 | 4.7k | built in primitive available not explicitly assigned |
| R13 | 4.7k | built in primitive available not explicitly assigned |
| R14 | 510R | built in primitive available not explicitly assigned |
| R15 | 200k 1% | built in primitive available not explicitly assigned |
| R16 | 220k | built in primitive available not explicitly assigned |
| R17 | 10k | built in primitive available not explicitly assigned |
| R18 | 100R | built in primitive available not explicitly assigned |
| R19 | 100R | built in primitive available not explicitly assigned |
| R20 | 100R | built in primitive available not explicitly assigned |
| R21 | 100R | built in primitive available not explicitly assigned |
| R22 | 100R | built in primitive available not explicitly assigned |
| R23 | 100R | built in primitive available not explicitly assigned |
| R24 | 100R | built in primitive available not explicitly assigned |
| R25 | 100R | built in primitive available not explicitly assigned |
| R26 | 100R | built in primitive available not explicitly assigned |
| R27 | 100R | built in primitive available not explicitly assigned |
| R28 | 100R | built in primitive available not explicitly assigned |
| R29 | 100R | built in primitive available not explicitly assigned |
| R30 | 100R | built in primitive available not explicitly assigned |
| R31 | 100R | built in primitive available not explicitly assigned |
| R32 | 100R | built in primitive available not explicitly assigned |
| R33 | 100R | built in primitive available not explicitly assigned |
| SW1 | GPIO16 | ideal switch primitive available not assigned |
| SW2 | GPIO9 | ideal switch primitive available not assigned |
| SW3 | GPIO10 | ideal switch primitive available not assigned |
| SW4 | GPIO11 | ideal switch primitive available not assigned |
| SW5 | GPIO22 | ideal switch primitive available not assigned |
| SW6 | GPIO23 | ideal switch primitive available not assigned |
| SW7 | GPIO15 | ideal switch primitive available not assigned |
| SW8 | GPIO19 | ideal switch primitive available not assigned |
| SW9 | GPIO24 | ideal switch primitive available not assigned |
| SW10 | GPIO26 | ideal switch primitive available not assigned |
| SW11 | GPIO28 | ideal switch primitive available not assigned |
| SW12 | GPIO18 | ideal switch primitive available not assigned |
| SW13 | GPIO25 | ideal switch primitive available not assigned |
| SW14 | GPIO27 | ideal switch primitive available not assigned |
| SW15 | GPIO29 | ideal switch primitive available not assigned |
| SW16 | GPIO14 | ideal switch primitive available not assigned |
| SW19 | SW_Push | ideal switch primitive available not assigned |
| SW20 | SW_Push | ideal switch primitive available not assigned |
| U1 | RP2350_60QFN | partial gpio and load envelope only |
| U2 | TLV73333PDBV | ideal rail approximation only |
| U3 | W25Q128JVS | missing device model |
| U4 | ECMF2-40A100N6 | missing device model |
| U5 | HS13L03W2C01 | aggregate load envelope only |
| U6 | SN74LV1T34DBVR | missing device model |
| U7 | TPS2553DBVR | behavioural approximation only |
| U8 | USBLC6-2SC6 | missing device model |
| USB1 | HRO-TYPE-C-31-M-12 | connectivity only no connector parasitic model |
| USB2 | USB_A | connectivity only no connector parasitic model |
| Y1 | ABM8-272-T3 | missing device model |
