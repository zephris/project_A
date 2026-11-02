# U1 / U4 focused DFM investigation — 6 October 2026

The nine open thermal holes under U1 are a real assembly process concern. Retain the present layout with explicitly specified epoxy filling and copper capping, or consider the isolated no-via-in-pad candidate supplied here. The lateral 0.00 mm entries do not justify moving either component: U4's four entries are reproduced by approximately 0.00005 mm model coordinate errors; U1's lead outlines differ laterally from exact copper by less than 0.0004 mm. Both copper land patterns match their manufacturer's recommended dimensions. These conclusions do not certify the full board for manufacture.

## Verdict and confidence

| Item | Evidence and conclusion | Confidence | Does process alone resolve it? |
|---|---|---|---|
| U1 nine lead-to-hole dangers | Nine Ø0.35 mm plated holes in EP61 are open on the top solderable surface. Paste windows avoid the holes, but solder can still wick during reflow. | High, native PCB plus mask/paste Gerber and drill file | Yes, explicitly accepted epoxy-filled and copper-capped treatment closes the physical solder-wicking paths. DFM may still show the drill intersections. |
| U1 32 left / 28 right entries at 0.00 mm | Exact 0.20 mm copper widths; saved lead polygons have sub-micrometre lateral displacements. Manufacturer recommends those widths. No meaningful lateral placement defect found. | High for native land geometry; medium-high for attribution of all 60 server entries | No fabrication change needed for these entries. Obtain a numerical/model interpretation or engineering disposition if required. |
| U4 four lateral entries at 0.00 mm | Saved model gives two negative margins on each side, −0.0000498 mm; exact copper is manufacturer's 0.70 × 0.20 mm pattern. | High for geometry and reproduction of four negative margins | No physical change needed. |
| U4 pin mapping and CPL | Pins 1/2 connector D+/D−, 3/4 ground, 5/6 IC D−/D+. CPL 0° correctly matches the model's native orientation to the board's KiCad 90°. | High for board/model/CPL consistency and datasheet pin assignment; server model identity remains a limitation | Preserve current placement. |

## Evidence snapshot and method

Investigated the board SHA-256 `bbd6fef8b75f61dae91e8a25f4c702376f247c2217f2a4ba6ab37a631a224439`, matching the DFM-fixes release source hash. Its drill/place origin is board XY (166.864500, 95.150000) mm. The uploaded report is [JLCDFM 630223756955443202](https://jlcdfm.com/viewer?pcbUploadFileId=630223756955443202), with count order Danger, Warning, Good.

Read native pads with KiCad 10.0.6 `pcbnew`, cross-checked against raw S-expressions, Gerber X2 component/pin attributes and aperture definitions, Excellon tools, saved component metadata, CPL rows, and manufacturer drawings. Full precision results are in `geometry-audit.json`, `signed-lead-margins.json`, and `u1-holes.json`; scripts are included for reproducibility. The cached component geometry comes from the JLCEDA/EasyEDA component library, used as evidence rather than as the manufacturer authority.

No shared PCB, schematic, project or library was edited, and no browser tab or CPL rotation was changed. The isolated candidate includes a copied project file solely to use the existing design rules.

## U1 land and lateral geometry

U1 is at board XY (144.332180, 58.016558) mm, KiCad 0°. All 60 perimeter lands are 0.875 mm long and 0.200 mm wide, at 0.400 mm pitch. Radial pad centres are ±3.437500 mm: inner edges ±3.000000 and outer edges ±3.875000. The 3.400 × 3.400 mm exposed copper pad is GND pin 61. These dimensions match local `datasheets/RP2350_current.pdf`, section 14.1.2, Figure 148, printed page 1325 / PDF page 1326. The package drawing is Figure 147, printed page 1324: nominal lead width 0.180 mm, range 0.130–0.230 mm. The recommended copper width is therefore not intended to enclose every worst-case physical lead width.

The saved C42411118 model's layer-100 lead polygons are approximately 0.1999996 mm wide. Comparing their lateral bounding edges with exact native pads gives margins −0.0003848 through +0.0003852 mm (under 0.386 µm). U1's cached library **pad centres** can differ radially by about 0.1375 mm from this board; that is a different land-pattern length/centre choice, not a component-origin error. Do not translate U1 to align library land centres.

The local calculation finds 18 negative lower-axis margins and 40 negative upper-axis margins, not the server's 32/28 left/right count split. It also finds near-zero positive margins. The server's left/right orientation, numerical tolerance and precise polygon version are unavailable, so this does **not** reproduce each of its 60 rows one-to-one. It does establish that the available model/copper comparison has only sub-micrometre lateral residuals and that the physical land pattern follows the drawing. Do not widen pads by fractions of a micrometre or move the part solely to satisfy rounded results.

The attached native KiCad 3D model is a **QFN-56 with a 5.6 mm exposed pad**, not RP2350A QFN-60 EP3.4. It is unsuitable for inspecting native lead/exposed-pad registration. Gerber/CPL DFM uses separate uploaded component geometry, so that wrong local visual model does not explain the nine actual holes. Replace it with a correct RP2350A model when maintaining the library; no model or library was changed here.

## U1 paste and exact holes

The four paste-only apertures are 1.200 × 1.200 mm rounded rectangles, corner radius 0.250 mm, centred at local (±0.700, ±0.700). Their net area is 5.545398 mm², or 47.9706% of the 11.560000 mm² exposed pad. The nominal 0.200 mm central web and rounded corners prevent direct hole/aperture overlap: calculated nearest aperture-to-drill-edge clearances are 0.034619 mm at corner holes, 0.052624 mm at edge-middle holes, and 0.069975 mm at the centre. These are artwork clearances, not guaranteed stencil registration allowances. A rectangular-only approximation incorrectly predicts overlap; the rounded corners must be included.

The windows are a reasonable reduced-paste starting point for a **closed** pad surface. They do not close the existing holes, and solder spreading over the continuous EP copper can reach the holes during reflow. Do not add a full-size paste opening or assume increased paste volume is an equivalent remedy.

All nine holes are GND pad 61, nominal Ø0.350 mm drill / Ø0.600 mm land, ring 0.125 mm. Their local X and Y each take −1.375, 0, +1.375 mm. Exact IDs and six-decimal coordinates are in `u1-hole-identification.csv`. The current Excellon file identifies them uniquely as **T4C0.350, nine ComponentDrill holes**, lines 325–334; **T3C0.350 comprises 125 other ViaDrill holes**.

| Gerber X mm | Gerber Y mm (three holes at each X) |
|---|---|
| −23.907320 | 38.508442, 37.133442, 35.758442 |
| −22.532320 | 38.508442, 37.133442, 35.758442 |
| −21.157320 | 38.508442, 37.133442, 35.758442 |

The actual drill output rounds those coordinates to 0.001 mm. Attach the hole map/CSV and identify **U1 EP61 / current T4**, rather than requesting all Ø0.35 mm holes indiscriminately. Tool numbers must be checked again after regeneration.

Suggested order note is supplied in `fabrication-note.txt`. These are electrically thermal vias but encoded as footprint through-hole pads; fabrication options that automatically treat only ViaDrill objects may omit them.

## Process eligibility and alternatives

JLCPCB publishes epoxy-filled/capped support for open pad holes, a ≤0.5 mm hole limit, and a charged POFV option for four-layer boards. Ø0.35 mm / 0.125 mm ring meets the published POFV size/ring ranges. Ordinary ink plugging excludes vias in pads or close to solder openings; tenting is not a flat copper cap. [Via covering](https://jlcpcb.com/help/article/pcb-via-covering), [POFV requirements and four-layer availability](https://jlcpcb.com/news/free-via-in-pad-6-20-layer-pcbs-pofv).

Both [RP2350A C42411118](https://jlcpcb.com/partdetail/RaspberryPi-RP2350A/C42411118) and [ECMF2 C5267592](https://jlcpcb.com/partdetail/STMicroelectronics-ECMF240A100N6/C5267592) are listed for Economic and Standard PCBA. The current [assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) state 0.40 mm minimum lead pitch for Economy and 0.35 mm for Standard. This establishes published component/pitch eligibility; it does not establish that the complete double-sided board, selected finish, colour, quantity and filled-via process qualify for Economy in an actual quote. The quoted service combination, cost and CAM acceptance of these ComponentDrill holes remain unverified. No order was placed.

Recommended retaining-layout route: epoxy fill and copper cap all nine explicitly identified thermal holes; preserve EP copper and paste windows, and obtain CAM confirmation that the holes have a flat solderable top surface. Copper-paste filling is an available alternative, but its extra thermal conductivity is not established as necessary here. Bottom-only tenting does not make the exposed top hole a solderable flat pad. Top solder-mask islands inside EP would require an explicit mask/paste redesign and assembler acceptance; ordinary ink plugging is not a supported substitution for this existing artwork.

**Lower-cost local alternative:** `alternative-no-vip.kicad_pcb` removes just the nine drilled pad-61 objects, retains the solid EP61 copper/mask and four paste windows, and retains surrounding GND vias and routing. KiCad DRC with zone refill reports **zero unconnected items and zero non-library violations**, as does the baseline. Both produce 146 `lib_footprint_issues` in this sandbox. The EP remains electrically connected through top-layer GND copper to outside-pad ground stitching; removing its drill pads does not leave an isolated EP according to the connectivity check.

This is a physically sound way to eliminate open holes under the solder joint without premium filling, but it changes the direct plane-ground and thermal paths. It is a **candidate**, not a production recommendation over the filled-via route: DRC proves geometric/DC connectivity, not comparable high-frequency return impedance or heat spreading. Review the local GND copper and expected RP2350 load/temperature before choosing it; retain short ground connections and outside-pad stitching. No claimed thermal result is based on the datasheet θJA value alone. If adopted, apply only the nine UUID deletions to the parent's final board, refill, update the associated footprint library variant, and regenerate fabrication outputs. Do not replace the parent's newer board wholesale with this snapshot.

`alternative-no-vip.patch` includes the nine pad removals and zone-refill changes; `alternative-change.json` records their UUIDs and source hash. No arbitrary external via relocation is proposed. If comparable ground/thermal performance is required without evaluation, retain and fill the existing array.

## U4 geometry, orientation, nets and stencil

U4 is at board XY (155.832180, 47.916558), KiCad 90°. Six rectangular pads are 0.700 × 0.200 mm at local X ±0.525 and Y −0.4/0/+0.4. Inner gap 0.350, outer span 1.750, transverse span 1.000 mm. Copper Gerber aperture D23 is `R,0.200000X0.700000`, matching the rotated physical pad. This matches [ST DS13913 Rev 4](https://www.st.com/resource/en/datasheet/ecmf2-40a100n6.pdf), Figure 30, page 12; Table 3, page 3 gives the following assignments.

| Pin | Board XY mm | Net/function |
|---|---|---|
| 1 | 155.432180, 48.441558 | Net-(U4-D+_to_connector), connector D+ |
| 2 | 155.832180, 48.441558 | Net-(U4-D-_to_connector), connector D− |
| 3 | 156.232180, 48.441558 | GND |
| 4 | 156.232180, 47.391558 | GND |
| 5 | 155.832180, 47.391558 | D− to IC |
| 6 | 155.432180, 47.391558 | D+ to IC |

CPL remains (−11.032320, 47.233442), Top, **0°**. The cached model at 0° has pins 1–3 on its lower row, left-to-right; this is exactly the board's KiCad 90° arrangement. Its transverse pin centres are ±0.400050 mm versus native ±0.400000 mm, and lead width is 0.1999996 mm. Consequently, the four outer-column lead-side margins are −0.0000498 mm; the opposite margins are +0.0000502 mm. The middle column has +0.0000002 mm on both sides. This directly reproduces four tiny negative entries. Its model land centres at row ±0.5500116 mm differ from corrected native ±0.525 mm because its library land pattern is shorter; do not shift the component to align those centres.

The D− escape's two Ø0.45 / Ø0.30 mm vias and In1 route are outside the pads; they are not U1-style holes in a solder land. Baseline DRC has no clearance or unconnected violation for the correction. No signal-integrity measurement is implied.

One separate assembly detail: current U4 paste equals its 0.700 × 0.200 copper. ST Rev 4 Figure 32, page 13 recommends 0.664 × 0.190 mm paste apertures at the same row centres with a 100 µm stencil. Ask the assembler to use this local aperture reduction (approximately 9.89% less area), or make explicit separate paste apertures if maintaining the stencil artwork. This is unrelated to the four lateral copper/model entries. Do not use an isotropic 0.005 mm shrink and claim it produces ST's anisotropic dimensions.

Preserve U1=0°, U4=0°, USB2=180°, U8=90° in the visually reviewed JLCDFM CPL. The native KiCad angle and vendor CPL angle need not be numerically identical. ST says to orient by the pin-1 mark, because text markings can be rotated. No blanket rotation correction or upload was performed.

## Limits and handoff

The current server's exact model polygons, unrounded check values and left/right rules were not obtained, so attribution of U1's exact 32/28 split remains an inference. A filled-via manufacturing instruction can fix the physical holes while an artwork-only DFM checker continues reporting them. The eight noncentral holes sit inside the EP copper but no automatic suppression was applied.

The included `u4-footprint.png` and `u4-package.png` are from an older Rev 1 local mirror; current Rev 4 text/dimensions were checked through ST's official PDF. Download of the current official PDF timed out and was stopped. Do not mistake the old mirror's figure numbering for current numbering. RP2350 package and footprint images are rendered directly from the local current PDF.

No full electrical, SPICE, EMC, lifecycle or quantitative thermal review was run: this request explicitly limits scope to focused U1/U4 DFM. The included general analyzers were not rerun; native geometry extraction, datasheet spot checks, Gerber/drill checks and comparative native DRC were used instead. Some KiCad user-configuration/library access was denied by the sandbox, explaining library validation limitations; both baseline and candidate were checked under the same conditions. Confidence rollup: geometry/process evidence high, server-only classification inference medium-high, cost/service-combination and thermal equivalence unresolved.

Any later BOM upload must use the separate `https://jlcdfm.com/bomMatch?pcbUploadFileId=ACTUAL_ID` page as instructed. The parent can apply other component fixes independently; these findings are tied to the recorded snapshot. At final validation, the root board hash had advanced to `09c192bbbcd453feef3bdf0d723846764cda39f93a8c9592841253d342ac1555`; the candidate and patch remain based on the original release. Scripts use the immutable release source for reproducibility.
