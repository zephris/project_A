# Kailh Choc hot-swap socket model

## Portable capacitor models — 2026-10-07

`C_0402_1005Metric.step`, `C_0603_1608Metric.step` and `CP_EIA-3528-21_Kemet-B.step` are unmodified copies from the installed KiCad 10 standard 3D library. Source: https://gitlab.com/kicad/libraries/kicad-packages3D. License: CC-BY-SA 4.0 with KiCad library exception, https://www.kicad.org/libraries/license/. Original file headers retained. All 44 capacitor PCB instances now reference these local files, replacing 17 obsolete KiCad 8 plugin paths and adding C41's absent model. Generic package geometry is not a verified MPN-specific maximum-height envelope. See mechanical/step_export_2026-10-07/README.md.

Source: https://github.com/perigoso/keyswitch-kicad-library
Pinned revision: `9edbd5ea3f5f4e36cbdfaefdf3d8b5c28277a416`

`SW_Hotswap_Kailh_Choc_V1.step` is the upstream `.stp` file renamed without modifying its contents. Its WRL counterpart is also included. Upstream declares the library dual licensed under MIT and CC-BY-SA 4.0; copies are included alongside these assets. Credit: Rafael Silva (perigoso) and contributors to keyswitch-kicad-library.

This is the socket body model, not the installed switch or keycap. Its matching upstream `SW_Hotswap_Kailh_Choc_V1V2` footprint has exactly the same pads and NPTH geometry as the existing PHBox optical variant. The replacement project-local footprint retains PHBox optical silkscreen adaptations and references `${KIPRJMOD}/3dmodels/SW_Hotswap_Kailh_Choc_V1.step`, with upstream zero offset/rotation and unit scale. All SW1–SW16 PCB instances and schematic footprint properties use `PHBox_Repair:SW_Hotswap_Kailh_Choc_V1V2_3D_Optical`.

Model visualization does not establish switch-housing, keycap or enclosure fit; those release checks remain.

## HS13 OLED module

`OLED_HS13L03W2C01.step` is the unmodified solid model from the JLCEDA/EasyEDA
official C7465997 library, model UUID `ecbc42d7ef3b4c1d91f9dc25f7bf875e`.
Source: https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/ecbc42d7ef3b4c1d91f9dc25f7bf875e
Fetched 2026-10-05. Copyright belongs to the JLCEDA/EasyEDA official library;
the socket models' MIT/CC-BY-SA licenses do not apply to this separate asset.
Original source metadata/notices are preserved in the manufacturing package.

The selected `PHBox:OLED_HS13L03W2C01` footprint matches the 35.4x33.5 mm body,
four 3 mm holes on 30.4x28.5 mm pitch and four 2.54 mm electrical leads.
Scale is 1, XY offset/rotation zero, Z offset +3 mm for insulating standoffs.
CAD includes long pins extending below the host PCB; trim leads to the agreed
assembly profile. Four M2.5 insulating fixing points support the module.
The model does not include screws, standoffs or the enclosure.

## Historical USB2 recessed USB-A reference model

`USB_A_905-761A203S10200_reference.step` is a project-generated simplified model
derived from the selected Jing 905-761A203S10200 / C2763302 manufacturer drawing:
https://atta.szlcsc.com/upload/public/pdf/source/20210526/C2763302_E838F915885D9CD3EFE4E3348A45005B.pdf
The drawing is saved at `datasheets/Jing_905-761A203S10200_C2763302.pdf`.
Generator: `build_usb_a_reference.py`. This is not a manufacturer-issued STEP.

The exact C2763302 JLCEDA/EasyEDA official library entry has no 3D asset. A related
C2763303 model was checked and rejected because its 7 mm height and contacts do
not match the selected connector. No part substitution was made.

The reference represents the 13.1 x 11 x 5.72 mm main shell, insulating tongue,
contact tails and four mounting legs registered to the existing pads. Longitudinal
shell placement and small folded features are approximate; do not derive a final
PCB cutout, panel aperture or plug clearance from it. No keycap/enclosure geometry
is implied. It uses unit scale and zero offset/rotation in the original
`Type-A:C2763302` footprint. KiCad applies the bottom-side flip automatically.

The manufacturer drawing requires a recessed mounting cutout. Existing U-shaped
lines in `Dwgs.User` are reference graphics, not `Edge.Cuts`. The historical PCB had no
corresponding cutout and the reference model intersects it. This issue was resolved in the active design by the C46400 replacement. Adding a 3D model
does not resolve it. See `mechanical/USB2-model-assessment-2026-10-05.md`.

## Active USB2 replacement - 2026-10-05

Active USB2 is fully SMT Jing 904-131A2032S10200 / C46400, on the underside to the right of USB-C, with H12 retained. The previous recessed-body cutout issue is resolved. Previous model assessments and release archives are historical. Active model: 3dmodels/USB_A_904-131A2032S10200_reference.step (simplified OEM drawing-derived reference). See mechanical/USB2-SMD-edge-assessment-2026-10-05.md.

## Option / auxiliary tactile buttons

SW19 and SW20 use SW_TS-1187A-B-A-B_C318884.step, the unmodified C318884 official EasyEDA/LCSC library model (UUID 91b67c1735f643ffb2e7226c23dd3492). Source: https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/91b67c1735f643ffb2e7226c23dd3492. Three valid solids; top at 1.5 mm. Unit scale, zero translation/rotation align its four contacts to the existing footprint. Credit: EasyEDA/LCSC official library. Metadata and original model are retained under stage2_work/option_button_models_2026-10-05. This is library CAD, not measured assembled geometry. The frozen JLCDFM package predates this visualization-only addition; pads, nets, routes and positions are unchanged.

OPSW1-OPSW6 already referenced KiCad SW_PUSH_6mm_H5mm.step. Their model is now copied into the project and references use KIPRJMOD for portability. Source: installed KiCad 10 standard 3D model library, https://gitlab.com/kicad/libraries/kicad-packages3D. KiCad library license: CC-BY-SA 4.0 with library exception, https://www.kicad.org/libraries/license/. These are generic footprint models; exact option-switch MPNs remain unspecified. Their existing assembly exclusions are unchanged.

## 2026-10-07 component completion and Choc V2
Current installed-switch model is SW_Kailh_Choc_V2_red.step (koktoh, CC BY-NC-SA 4.0, source and usage clarification in ../mechanical/model_completion_2026-10-07/README.md). SW_Kailh_Choc_V1.step is historical. SW_Hotswap_Kailh_Choc_V1.step remains the socket model. L1 and LEDs use prepared exact-part EasyEDA assets; U4 and D21 use explicitly simplified ST drawing-derived references. See the linked report for dimensional limits and provenance.
