# Online model search and intake — 2026-10-07

Three official TI SPICE models and one official TI IBIS archive downloaded, original vendor contents preserved. None has been assigned to the root schematic or substituted into the six planning benches. Historical model-audit files describe the state before this intake.

## Downloaded SPICE models
| Board part | Source archive | Saved model | Ngspice 46 check |
|---|---|---|---|
| U7 TPS2553DBVR | [TI SLVM425B](https://www.ti.com/lit/zip/slvm425b) | TPS2553/SLVM425A/TPS2553_PSPICE_TRANS/tps2553_trans.lib | Parses and executes with PSpice compatibility/XSPICE libraries, but the nominal startup probe returns approximately 0 V: **not ready for integration**. |
| U2 TLV73333PDBV | [TI SBVM471](https://www.ti.com/lit/zip/sbvm471) | TLV73333P/tlv73333p_trans.lib | Nominal 5 V input / 20 mA output probe: 3.29986 V. |
| U6 SN74LV1T34DBVR | [TI SCLM180](https://www.ti.com/lit/zip/sclm180) | SN74LV1T34_SPICE/SN74LV1T34.cir | 3.3 V input pulse, 5 V supply, 15 pF load: high 4.99958 V, low approximately 0 V. |

Official product listings: [TPS2553](https://www.ti.com/product/TPS2553), [TLV733P](https://www.ti.com/product/TLV733P), [SN74LV1T34](https://www.ti.com/product/SN74LV1T34).

Checks only establish execution and simple nominal response. They do not verify startup corners, limiting dynamics, thermal behaviour, control-loop stability, accuracy or agreement with vendor reference simulations. U2 model header mentions TLV713 datasheet despite being published as TLV73333P: preserve the original and qualify rather than assuming full accuracy. U6 vendor model describes typical 25 C behaviour, not complete tolerance coverage.

## Terminal order / candidate DBV adapters
- U7: `TPS2553_TRANS IN GND EN PWPD FAULT_B ILIM OUT`; candidate DBV electrical mapping 1,2,3,extra,4,5,6. PWPD appears only in the subcircuit signature, is unused inside this downloaded body, and was tied to ground for the probe. Vendor archive directory says SLVM425A even though downloaded endpoint is SLVM425B. Do not replace it with the TPS2553-1 latch-off variant.
- U2: `TLV73333P_TRANS EN IN OUT GND`; candidate package mapping 3,1,5,2; NC pin 4 not represented.
- U6: `SN74LV1T34 Y A VCC AGND`; candidate package mapping 4,2,5,3; NC pin 1 not represented.

Mappings are proposed adapter information, not completed schematic assignments. Confirm against the exact symbols and current pin nets during integration. Archive and extracted file SHA-256 values are in manifest.json.

## Additional model sources
| Board component | What was found | Status |
|---|---|---|
| U6 SN74LV1T34DBVR | [TI SCLM119 IBIS](https://www.ti.com/lit/zip/sclm119) | Downloaded: SN74LV1T34_IBIS/SN74LV1T34_IBIS/sn74lv1t34.ibs. Includes exact DBV component; IBIS is for IO/signal integrity, not an internal logic/firmware simulator. |
| D21 ESDA7P120-1U1M | [ST product page](https://www.st.com/en/protections-and-emi-filters/esda7p120-1u1m.html), SPICE .lib/.olb v1.1 | Official listing verified. Download link and public endpoint attempts timed out. **Not downloaded.** |
| U8 USBLC6-2SC6 | [ST product page](https://www.st.com/en/protections-and-emi-filters/usblc6-2.html), SPICE .lib/.olb v1.0 | Official listing verified. Downloads timed out. **Not downloaded.** Datasheet also gives a PSpice equivalent circuit, limited to 27 C. |
| U3 W25Q128JVS | [Winbond exact W25Q128JVSIQ IBIS listing](https://www.winbond.com/hq/support/documentation/?__locale=en&line=/product/code-storage-flash/index.html&family=/product/code-storage-flash/qspi-nor/index.html&pno=W25Q128JVSIQ&category=/.categories/resources/ibis-model/) | Exact SOP-8 candidate listing found; ZIP link is locked/sign-in required. Not downloaded or substituted with another package. Winbond JV family page lists no public SPICE models; IBIS/Verilog are different model types. |
| Samsung MLCCs, including C1525 / CL05B104KO5NNNC | [Samsung Component Library](https://weblib.samsungsem.com/index.do) | Official PSpice/LTspice/S-parameter downloads exist. Exact part availability and condition-specific downloads not verified. Stock suffix C may be omitted in manufacturer's base-name search; do not assume unrelated capacitance/package matches. |
| C19/C43 T520B107M010ATE070 | [KEMET K-SIM part search](https://ksim3.kemet.com/?pn=T520B107M010ATE070), [official download instructions](https://www.kemet.com/en/us/support/design-and-product-information/how-do-i-download-spice-models.html) | Manufacturer can generate SPICE for selected frequency/temperature/bias conditions. Exact export not downloaded or validated. |
| U1 RP2350 | [Official product/model resources](https://pip.raspberrypi.com/categories/1214-rp2350) | No exact public SPICE or IBIS model verified by this search. Existing GPIO envelope remains only a partial abstraction; firmware cannot run in these SPICE models. |
| U4 ECMF2-40A100N6 | [ST exact-part page](https://www.st.com/en/protections-and-emi-filters/ecmf2-40a100n6.html) | Exact part page lists CAD assets, but no exact SPICE/S-parameter download verified. Family-level model listings must not be treated as this exact part. |
| U5 HS13L03W2C01, D1–D20 SK6805-EC15 | Exact-part searches | No exact public SPICE download verified. Use documented load envelopes, not an unrelated display or ordinary diode model. |
| F1 SMD0805-075-12V | Exact-part searches and datasheet | No exact electrothermal model verified. A resistor can approximate cold loss but not temperature-dependent trip behaviour. |
| Y1 ABM8-272-T3 | [Exact Abracon drawing](https://abracon.com/datasheets/ABM8-272-T3.pdf) | No exact motional R/L/C model verified. Other Abracon crystal series publish example parameters but are not valid substitutes for this part. |
| L1 AOTA-B201610S3R3-101-T | [Exact Abracon datasheet](https://abracon.com/datasheets/AOTA-B201610S3R3-101-T.pdf) | No exact downloadable SPICE verified. Built-in L plus datasheet DCR is usable for linear estimates; saturation requires extra characterization. |
| Resistors, ideal switches/connectors, holes | Built-in primitives or connectivity | Vendor files unnecessary for ideal analysis. C41 remains a generic value without an exact selected MPN. |

“Not verified/found” describes this search, not proof a manufacturer has no private model. Archived intake failures and Winbond listing HTML are retained for follow-up.

## Reproducing local compatibility checks
Run `D:/Program Files/bin/python.exe spice/models/smoke_vendor_models.py` from the project root. The isolated worker enables `ngbehavior=ps` and loads all seven KiCad XSPICE code libraries. The DLL command parser mishandles paths with spaces; the worker copies installed code libraries into a temporary directory without spaces and loads those copies. No global KiCad setup or original vendor model is edited. Temporary copies are runtime artifacts, not project model sources. Results and effective probes are under ../qualification_2026-10-07/.

## Remaining integration gates
First reproduce the vendor TPS2553 reference successfully; investigate its failed nominal probe before using it for board tests. Then review terminal mapping and current board topology, adapt U2/U7/U6 into isolated board benches, and add comparison/corner tests. Resolve stale suite provenance only after this review. Current downloaded models and these smoke checks do not validate the complete board.

