# Choc V2 RGB LED fit study — 2026-10-08

The current switch model already includes the underside SMD LED opening. No cut to the OEM switch, switch reference model or manufacturing PCB is proposed. A separate clearance gauge marks the volume to keep clear under the LED window when designing foam, a carrier, or a future model simplification. It is not the switch retention-plate aperture.

## Models

- `STEP/choc_v2_led_fit.step`: four intact switch/LED/PCB-coupon comparisons, in order SW2 (nominal), SW1, SW7, SW13. Coupons have current nominal switch drill locations; they omit copper and hot-swap sockets and are not fabrication files.
- `STEP/choc_v2_led_section.step`: same four comparisons, with the positive-X half of the switch and coupon removed to reveal the LED. LED remains whole. This is an explanatory section, not a proposed switch modification.
- `STEP/choc_v2_led_window_candidate.step`: **2.60 × 2.40 × 1.20 mm** cyan keep-clear gauge. Local centre X=0, Y=-4.93 mm; bottom Z=0, top Z=1.20 mm. Dimensions are an engineering candidate rather than measured OEM cavity dimensions.
- `placements.json`: read-only extraction of SW1–SW16 and D1–D16 positions from the current PCB.
- `fit-check.json`: native geometric collision distances, sensitivity checks, saved artifact validity and PCB hash.
- `review/fit-section.png`, `review/fit-iso.png`, `review/window-gauge.png`: rendered saved STEP files, visually reviewed. The underside-only view is also retained but the PCB obscures the LED from that direction.

All dimensions are millimetres. Local X follows PCB X; local Y is minus PCB Y; Z=0 is the front seating plane. Add (switch PCB X, minus switch PCB Y, 0) to place a study on the heatsink assembly's current datum. Cells in the comparison files are translated by 0, 22, 44 and 66 mm along X for inspection.

## Evidence and limits

Kailh's red CPG135301D01 drawing marks the recommended LED footprint as 2 × 1.5 mm, centred 4.93 mm from the switch centre. Its published drawing does **not** dimension the complete three-dimensional internal LED cavity. The manufacturer's current product page explicitly lists SMD LED support. The current PCB uses 180° model rotation; in its CAD frame the cavity is on Y=-4.93 mm.

The selected OPSCO SK6805-EC15 is nominally 1.50 × 1.50 × 0.65 mm. The imported EasyEDA reference extends to Z=0.67 mm and has a tiny pad protrusion, so tests use its actual saved geometry as well as a chosen 1.70 × 1.70 × 0.80 mm engineering envelope. This envelope covers an extra 0.10 mm on each XY side and additional height; it is **not a certified package maximum or a statistical solder/placement tolerance stack**.

| Placement | Actual LED offset, PCB X/Y | Deviation from nominal centre |
|---|---|---|
| SW1 / D1 | -0.140422, +5.138132 | -0.140422, +0.208132 |
| SW7 / D7 | 0, +4.82 | 0, -0.11 |
| SW13 / D13 | -0.300422, +5.019132 | -0.300422, +0.089132 |
| SW14 / D14 | +0.01, +4.93 | +0.01, 0 |
| Other 12 pairs | 0, +4.93 | 0, 0 |

The 2.60 × 2.40 mm gauge contains the chosen envelope at every measured LED placement, with minimum XY containment margins about 0.150 mm and 0.142 mm respectively. This is a clearance allowance, not a request to cut the existing cavity to those dimensions. Keep foam out of it. Do not drill the PCB beneath these LEDs or make a matching hole in the retention plate without a separate mechanical need; the LEDs sit below the switch inside its supplied cavity.

## Completed geometric checks

All 16 LED/switch pairs have **zero overlap** in the exact model and chosen engineering envelope checks. Minimum exact-model clearance is **0.516868 mm**, minimum sensitivity-envelope clearance **0.416868 mm**, both at SW1/D1. The candidate gauge has zero overlap with the supplied switch geometry and **0.275 mm** minimum clearance. The saved intact fit, corrected section and gauge STEP solids are valid. Manufacturing PCB SHA-256 remains `11697274d842131bd6addc16371991acf702516819850ae38afbac23443ed6d4`.

| Pair | Exact LED clearance mm | Engineering envelope clearance mm |
|---|---:|---:|
| SW1 / D1 | 0.516868 | 0.416868 |
| SW2 / D2 | 0.725000 | 0.625000 |
| SW3 / D3 | 0.725000 | 0.625000 |
| SW4 / D4 | 0.725000 | 0.625000 |
| SW5 / D5 | 0.725000 | 0.625000 |
| SW6 / D6 | 0.724995 | 0.624995 |
| SW7 / D7 | 0.614995 | 0.514995 |
| SW8 / D8 | 0.725000 | 0.625000 |
| SW9 / D9 | 0.725000 | 0.625000 |
| SW10 / D10 | 0.725000 | 0.625000 |
| SW11 / D11 | 0.725000 | 0.625000 |
| SW12 / D12 | 0.725000 | 0.625000 |
| SW13 / D13 | 0.635868 | 0.535868 |
| SW14 / D14 | 0.725000 | 0.625000 |
| SW15 / D15 | 0.725000 | 0.625000 |
| SW16 / D16 | 0.725000 | 0.625000 |

The installed build123d version returns spurious intersections when `Compound.intersect` is called on the moved imported switch, despite a positive separation distance. Checks therefore use world-space distances and located constituent solid pairs; positive distance proves separation and prunes the individual intersection checks. The section model is likewise cut on located constituent solids. This correction was verified against individual solids and the corrected saved section snapshot; false aggregate-overlap numbers are superseded by `fit-check.json`.

Geometric clearance does not establish brightness, diffusion through the switch, keycap light transmission, LED thermal behaviour, hot-swap socket interference, spring/stem clearance during full travel, or real-part tolerances. The current board seats the LED on the surface; inspect an assembled first article before releasing an optical or enclosure design. The red stem switches need compatible translucent keycaps or an appropriate light path for visible illumination.

## Sources and attribution

- [Kailh Choc V2 manufacturer product page](https://www.kailh.net/products/kailh-choc-v2-low-profile-switch-set), including SMD LED support and red drawing link.
- [Kailh red CPG135301D01 OEM drawing](https://cdn.shopify.com/s/files/1/0657/6075/5954/files/SPEC-CPG135301D01_Kailh_Choc_V2_Low_Profile_Red_Switch_03cd29a8-065e-45f8-8053-b72dcd70616d.pdf?v=1667190153), retained in `../model_completion_2026-10-07/Choc-V2-datasheet.pdf`; package drawing image was inspected.
- [Selected OPSCO SK6805-EC15-001 drawing](../../datasheets/OPSCO_SK6805-EC15-001_C2890035.pdf), retained with the board. Prior iPixel reference is an additional nominal 1.5 × 1.5 × 0.65 mm reference, not a substitute for the selected OPSCO variant.
- [koktoh switch CAD](https://github.com/koktoh/keyswitch_model), commit `2b6bcfac0032f1547e27b18b9a897e065e544b37`, `choc/v2/KiCad/red.step`, CC BY-NC-SA 4.0. [Author's usage clarification](https://koktoh.hatenablog.com/entry/2023/07/01/031414). These fit files contain that switch geometry; preserve its attribution and licence restrictions when redistributing. This is community CAD, not vendor-certified CAD.
- Existing selected-part EasyEDA LED model provenance is recorded in `../model_completion_2026-10-07/README.md` and `downloads.json`.

## Rebuild

Use the existing `../heatsink_2026-10-08/.venv/Scripts/python.exe` interpreter. Set `CADGEN_CACHE_DIR` to this folder's `.cache`, then run the three `src/choc_v2_led_*.py` entrypoints and `checks/check_led_fit.py`. Snapshots use `python -m cadgen.cli step snapshot` with `PLAYWRIGHT_BROWSERS_PATH` pointing at `../heatsink_2026-10-08/.browser`. Separate CAD Viewer serves this study; existing OCP heatsink assembly remains unchanged.
