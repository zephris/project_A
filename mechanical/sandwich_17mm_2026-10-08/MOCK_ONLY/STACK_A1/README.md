# A1 stacked fitment kit — inset replacement

**Earlier button layout:** this validated print job does not match the [30 October higher/wider layout candidate](../../../ergonomic_layout_2026-10-30/README.md). Regenerate its parts and slicing before using that PCB revision.

Updated 23 October 2026. **Use this INSET revision.** The earlier stack was reported out of bounds in Bambu Studio; its files and package are quarantined in `SUPERSEDED_DO_NOT_PRINT/`. This replacement was freshly sliced using **Bambu Studio only**, for **A1 / AMS Lite / 0.4 mm nozzle / Textured PEI**.

## Print and review files

1. Follow the [calibration plan](CALIBRATION_A1/PLAN.md), then use the existing small [separator_trial.gcode.3mf](separator_trial.gcode.3mf), about **94 min / 18.4 g**. Check release, thickness, layer cohesion and the real mating parts.
2. Open **[stacked_kit_inset_project.3mf](stacked_kit_inset_project.3mf)** to inspect the complete editable Bambu project. It contains 105 named parts inside one multipart assembly. Keep that assembly intact: splitting to objects, dropping to bed or auto-arranging would destroy the supported vertical placements.
3. The prepared replacement is **[stacked_kit_inset.gcode.3mf](stacked_kit_inset.gcode.3mf)**. Estimated **55.5 h / 661.1 g PLA / 173.6 g PETG / 120 AMS changes**, including estimated tower and purge material. Re-slice if profiles or placements change.
4. Download **[A1_PLA_PETG_stacked_fitment_kit.zip](A1_PLA_PETG_stacked_fitment_kit.zip)**. It contains the INSET files, not the superseded long-job G-code. [Individual per-part fallback](../PRINT_A1/README.md) remains available.

[Geometry-only inset 3MF](stacked_kit_inset.3mf) is supplied for import. Use the editable project to retain Bambu presets. No print or calibration was started.

## What changed

Two independent panel stacks and smaller side/top-pocket parts replace the edge-hugging three-column layout. All **105 source components keep their exact geometry**; six oversized originals remain quartered, with no scaling. The supported gap remains **1 mm**. Source height is **60.35 mm**. The original had circular travel reaching X −0.270 / 256.080 mm; the replacement's ordinary travel, including arc extrema, stays at least **9.766 mm** from the bed edge. Deposition including width is at least 10.451 mm from the edge. The machine's actual 256 mm limits are unchanged.

Read the [bounds investigation and validation](review/INSET_REVISION.md), [layout drawing](review/inset-bed-layout.png), [actual slice audit](review/inset-bounds-audit.json) and [component checks](review/inset-verification.json). The old validation checked endpoints and missed full travel arcs; it is superseded for print-boundary decisions. Historical tuning/assembly records remain in `review/`; use the `inset-` reports for current layout/time/material figures.

## Presets and materials

- PLA model parts and scaffold; PETG for **two contact layers on each model-facing support face**. Zero contact Z gap and interface spacing; support may start on earlier parts. 0.10 mm model/first layers, 2 walls, 10% infill, top 4 layers / 0.4 mm and bottom 3 / 0.3 mm. Original part dimensions remain unchanged.
- Prime tower enabled at X196/Y180 with its own reserve. **800 mm³ flushing each direction**, no flushing into model, infill or support. The 35 mm tower and 3 mm object brim fit with the generated support/travel envelope.
- PLA 220 °C / 21 mm³/s; conservative PETG 245 °C / 8 mm³/s; bed 65 °C. Bambu brand is confirmed, actual PLA grade and PETG Basic/HF still need checking. Current flow ratios 0.98 / 0.94 are preset starting values, not measured calibration.
- Map PLA and PETG to their **actual AMS Lite slots**. Allow at least **750 g PLA / 250 g PETG** for this job, one trial and some margin. [Material breakdown, including purges](review/inset-material-breakdown.json) gives the separate categories.

## Fitment and assembly

Use the **[35-step illustrated mock assembly manual](../output/pdf/PHBox_mock_assembly_manual.pdf)** or its [file-linked instructions](../ASSEMBLY_STEPS.md) after separating the printed parts. Rigid USB collar gauges are bench-checked on the empty surround and removed before final closure over the simplified USB blocks.

This is an **unpowered PLA fitment mock**. Rigid PLA substitutes do not qualify TPU collars, foam compliance or thermal pads. Do not power the board with a plastic heatsink or rigid pad gauge. Some 0.25–0.6 mm features may require the existing individual 0.2 mm-nozzle fallback; a successful slice does not prove they will survive removal.

Peel supports from the top down while supporting thin panels. Reconstruct quartered plates on a flat jig using original coordinates in `../manifest.json`; temporary taped seams do not reproduce a full panel's stiffness. Test actual switches, screen, PCB, screws and dongles. Existing heatsink retainer/thread-engagement and dongle-body-clearance concerns remain in the [assembly review](review/REVIEW.md).

## Rebuild

Run `build_stack.py`, then **`slice_stack.ps1 -Model stacked_kit_inset`** directly from PowerShell, then `verify_inset.py` and `publish_inset.py`. `slice_stack.py` remains a compatibility wrapper. Bambu's executable is the installed `D:/Bambu Studio/bambu-studio.exe`; no other slicer is used. The rebuild uses retained source STLs and profile helpers in the project. The ZIP is a print/review handoff, not a standalone source repository.
