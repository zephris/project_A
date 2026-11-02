# PHBox component models — Choc V2 candidate (2026-10-07)

Current switch choice: OEM Kailh Choc V2 with a cross (+) keycap stem. Red switch CAD is a geometric reference; it does not select a procurement variant.

## Current CAD exports
- PHBox-ChocV2-assembly.step: native KiCad export including PCB and component models.
- PHBox-ChocV2-single-compound.step: one CAD compound containing disconnected solids, not one fused continuous body.
- Units: millimetres. KiCad export origin: 0,0. Register PCB faces before using the enclosure's Z datum; KiCad STEP front face is above its board-bottom datum.
- board-choc-v2-isometric.png: native KiCad render, visually reviewed.
- final-choc-v2-geometry-validation.json: saved STEP validity and round-trip checks.

Earlier PHBox-assembly.step, PHBox-single-compound.step, board-isometric.png and Buttoncap*.stl in this folder are V1 historical references, not current V2 enclosure inputs.

## Component models
| References | Model | Provenance / limitation |
|---|---|---|
| SW1–SW16 | SW_Kailh_Choc_V2_red.step | koktoh community KiCad CAD, 8 valid solids, nominal stem top Z=8.6 mm, pin extent Z=-3.3 mm. Rotate Z=180 degrees in this footprint. Community support pin position is approximate; OEM drawing governs machining dimensions. |
| L1 | AOTA_B201610S3R3_101_T_EasyEDA.step | Exact selected part's EasyEDA model, normalized to seating plane. |
| D1–D20 | SK6805_EC15_EasyEDA.step | Exact selected part's EasyEDA model, normalized to seating plane. Nominal visual model is not a maximum tolerance envelope. |
| D21 | ESDA7P120_1U1M_ST_reference.step | Project-generated simplified nominal body/pads from ST drawing; not downloaded ST CAD. Nominal body 1.60 × 1.00 × 0.55 mm. Separate maximum-body envelope 1.65 × 1.05 × 0.60 mm. |
| U4 | ECMF2_40A100N6_ST_reference.step | Project-generated simplified nominal body/pads from ST drawing; not downloaded ST CAD. Nominal body 1.35 × 1.40 × 0.45 mm. Separate maximum-body envelope 1.40 × 1.45 × 0.50 mm. |
| All 44 capacitors | Existing project-local standard package STEP models | Standard package geometry, not exact vendor detail. |

The downloaded EasyEDA U4 model was rejected: its 0.77 mm height exceeds ST's 0.50 mm maximum. ST's public CAD ZIP downloads timed out. Reference body envelopes do not include assembly placement tolerance, solder variation, thermal-pad compression or enclosure clearance allowances.

## V2 PCB and retention checks
All 16 game-switch footprints have nominal 5.05 mm centre holes and 1.60 mm support-pin holes at local (-5,5.15) mm. The existing footprint is dual V1/V2 compatible at nominal geometry; no drill, pad, routing or BOM changes were made. Audit saved separately. Electrical pins align after rotating the CAD model by 180 degrees.

V2 has a different height and cross stem: do not release the earlier V1 retention plate, V1 keycaps or V1 Z stack unchanged. Recheck V2 latch engagement, housing opening, support pin, full key travel and cap-skirt clearance against the OEM drawing and a fit coupon. Existing socket model remains because it represents the dual-compatible socket, not the installed switch. Remaining holes without 3D hardware models are intentional: the PCB is to be retained in the housing plate assembly, with exact housing hardware still unspecified. Maintain the gasket-supported island; do not create a rigid bridge around its gaskets.

## Round cross-stem cap candidates
- AdditiveArcade explicitly offers Choc V2 round caps, including Flatbox and Cosmox sizes: https://additivearcade.com/products/low-profile-round-choc-v2-3d-printed-button-caps
- NLOFIN lists cross-stem leverless caps in 23 and 26 mm sizes: https://nlofin.shop/
- Haute42 MX cross caps are another candidate: https://focusattack.com/official-haute42-mx-solid-cross-keycaps-25-8mm-blue/
- Public low-profile MX/V2 STEP/STL alternatives exist at https://github.com/DeltaWhy/ols but are keyboard caps, not replicas of the requested round products.

No exact downloadable CAD was verified for the named commercial round caps. Cross-stem compatibility alone does not establish skirt clearance around Choc V2's collar or full travel. No unverified cap model is placed on the board. Select exact diameter and cap profile before final case aperture or Z clearance is released.

## Sources and licensing
Switch source: https://github.com/koktoh/keyswitch_model at commit 2b6bcfac0032f1547e27b18b9a897e065e544b37, choc/v2/KiCad/red.step. Source README retained as choc-v2-README.md: CC BY-NC-SA 4.0. Author use clarification: https://koktoh.hatenablog.com/entry/2023/07/01/031414 (permits PCB design/sales render use, restricts selling reproduced switches or model assets). Preserve attribution and consult those terms before redistributing commercial CAD assets.
OEM switch: https://www.kailh.net/products/kailh-choc-v2-low-profile-switch-set ; downloaded OEM drawing retained as Choc-V2-datasheet.pdf.
Inductor: https://abracon.com/datasheets/AOTA-B201610S3R3-101-T.pdf
LED: https://cdn-shop.adafruit.com/product-files/4492/Datasheet.pdf
ST U4: https://www.st.com/resource/en/datasheet/ecmf2-40a100n6.pdf
ST D21: https://www.st.com.cn/resource/en/datasheet/esda7p120-1u1m.pdf
EasyEDA source URLs are retained in downloads.json; original unmodified assets retained beside prepared derivatives. No broader asset license is asserted.

## Manufacturing status
This is a 3D completion and switch-reference update. The preserved-board comparison confirms every board change is confined to model clauses. Current PCB fabrication, electrical design and assembly data are unchanged. These exports aid enclosure design; they do not certify mechanical fit or heatsink clearance.

CAD Viewer was unavailable because cadgen is not installed in the active runtime. Native KiCad rendering was used for visual review; the self-contained STEP exports can be opened in your CAD application.
