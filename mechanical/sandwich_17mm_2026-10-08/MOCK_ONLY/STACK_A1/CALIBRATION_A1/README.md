# A1 calibration before the stacked fitment kit

Prepared 23 October 2026 for **Bambu A1 / AMS Lite / 0.4 mm standard nozzle / Textured PEI**. Bambu PLA and Bambu PETG are confirmed; PETG Basic versus HF is unknown. **Physical calibration has not run. No new flow ratio or pressure-compensation result has been saved to the printer or main kit.**

The [research-led calibration plan](PLAN.md) compares previous A1 and PLA/PETG trials, ranks the tests by expected benefit, and sets decision gates. It adds a bed-wide first-layer check, a PLA-only control, material-transition strength screening and a wider stack proof. Proposed new diagnostics are explicitly distinguished from files already prepared. Confirm the actual PLA grade as well as PETG grade before using a grade-specific profile.

## Recommended sequence

1. Put the A1 in its intended printing location on a firm surface. Fit and verify the 0.4 mm nozzle. Wash the PEI plate with dish detergent and water, dry it, seat it correctly and clear the motion area. Use dry filament and select its actual AMS slot. Read the PETG spool/RFID to identify Basic or HF; do not declare HF just to increase flow limits.
2. On the A1 touchscreen, open **Calibration** under Settings/Maintenance and run the full machine routine, including vibration compensation, motor-noise calibration and bed leveling where offered. Menu wording depends on firmware. Let it finish and resolve any printer error before printing. This is the routine that measures the machine in its actual location.
3. For the next print, enable **Bed leveling** and **Flow dynamics calibration** in the send dialog. The A1 measures pressure compensation; a value copied from another machine is not a measurement of this nozzle/spool. Bambu Studio's separate **Calibration → Flow Dynamics** workflow can be used if the connected A1 and firmware offer it. Record a successful result, not just that the option was checked.
4. After the plan's bed-wide first-layer check and PLA-only control pass, run the existing [six-part separation trial](../separator_trial.gcode.3mf), using the correct AMS mappings. Its prepared settings use 220 °C PLA, 245 °C conservative PETG, a 65 °C bed and the current 0.98/0.94 flow ratios. These are preset starting values. Check first-layer adhesion, smooth surfaces, release of PETG interfaces, frame flatness, washer thickness, cap travel and post fit. The trial is about 94 minutes and 18.4 g, including estimated tower and purge material. Support release alone does not qualify material-change strength or a larger stack; follow the additional checks in the plan.
5. **Only if extrusion defects remain**, run manual Flow Rate calibration for the affected material. Bambu's official filaments already have tuned starting profiles. Prefer the connected Studio wizard: **Calibration → Flow Rate → Manual Calibration**, coarse followed by fine. Select the actual nozzle, plate and filament. A1 flow-dynamics compensation and the filament's extrusion ratio are separate settings.
6. Save the observed flow result to a new filament preset, then re-slice the trial and main kit with that preset. Editing a preset does not change an existing `.gcode.3mf`. Rerun flow dynamics if printing temperature or volumetric-speed settings change. The two-material trial remains necessary: a single-material flow patch cannot qualify interface release or cross-material purge adequacy.

## Optional local flow-test projects

These **editable, unsliced** projects use the installed Bambu Studio test geometry. They need **Slice plate and visual Preview review** before use. They do not start a calibration wizard or save results automatically. Their import has not been visually verified because desktop control is unavailable.

| File | Material and baseline | Test conditions |
|---|---|---|
| [PLA_flow_coarse.3mf](PLA_flow_coarse.3mf) | Bambu PLA, flow ratio 0.98 | 220 °C nozzle, 65 °C PEI bed |
| [PETG_flow_coarse.3mf](PETG_flow_coarse.3mf) | Conservative PETG, flow ratio 0.94 | 245 °C nozzle, 70 °C PEI bed; PETG touches the bed in this test |

Both have nine separately named patches with **−20, −15, −10, −5, 0, +5, +10, +15, +20%** object flow modifiers. They are centered within the 256 mm bed, 1.4 mm tall with 0.20 mm layers, three walls, 35% rectilinear infill, one bottom layer and five top layers. Top and solid-infill speeds are limited to 60 mm/s to avoid testing maximum throughput at the same time. No supports, ironing, multi-material changes or prime tower are used. These are adaptations of Bambu's recipe, not files exported by its wizard.

Before slicing, inspect the Objects list and verify that each patch retains its own **print_flow_ratio** value from 0.80 to 1.20; the global filament flow ratio stays at the baseline. If import discards these modifiers, use the Studio wizard instead. Printing nine equal-flow patches would not calibrate anything. File-content checks verify the modifiers, patch count, height and bed bounds; they do not prove a successful slicer import or physical print.

Choose the patch with the smoothest central top surface without gaps or raised ridges. Ignore the label and perimeter when judging. The coarse calculation is `new ratio = baseline × (100 + printed modifier) / 100`. For example, **only if observed**, a −5 PLA patch gives `0.98 × 0.95 = 0.931`. This example is not an assigned result. Run the fine pass from the coarse result, not the original baseline, and then save that result. If all patches have defects, resolve moisture, feeding, adhesion or temperature first rather than selecting an arbitrary patch.

The retained local helper can prepare the fine model after a measured baseline is available: `prepare_calibration.py --material PLA --fine-baseline <observed coarse ratio>` (or PETG). It prepares files only by default. Its direct Python `--slice` path failed with **0xC0000005**. Subsequent inset-stack work successfully sliced with the same installed Bambu Studio via a direct PowerShell launch; see `../slice_stack.ps1`. The cause of the launch difference is not established. The flow tests themselves remain unsliced; no flow calibration has been performed.

## Direct-control status

- Windows desktop-control helper failed to initialize, including after one reset; no calibration controls were clicked.
- Bambu cloud/network bridge reports **unconfigured**, with no running agent; the printer's live status and firmware could not be read through that bridge.
- The read-only slicer-inspection MCP also refused execution because it requires tool approval that is unavailable in this session. The project checks above were made directly against their local file contents.
- Automatic approval review rejected importing the private separator trial into signed-in Bambu Connect because the handoff may transmit the CAD/print file to Bambu's cloud. No cloud import or upload was performed.

The remaining physical steps require the A1 touchscreen or a working Bambu Studio connection. Do not treat prepared test files or checked send-dialog options as completed calibration. Record actual results in [calibration-status.json](calibration-status.json).

## Primary references

- [Bambu A1 automatic calibration and pressure sensor](https://us.store.bambulab.com/products/a1).
- [Bambu Textured PEI plate care](https://bambu-lab-jp.myshopify.com/en/products/bambu-dual-sided-textured-pei-plate).
- [Official Studio flow-dynamics and flow-rate guidance](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/CalibrationWizardStartPage.cpp). It distinguishes the two and notes that manual flow-rate tests are generally needed only for remaining defects.
- [Official flow-test preparation](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/Utils/CalibUtils.cpp), function `calib_flowrate`; [result calculation](https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/GUI/CalibrationWizardSavePage.cpp), coarse/fine save pages. Local meshes come from installed Studio 02.07.01.62; online master may change.

The manufacturer wiki returned an access error during research; inaccessible pages were not treated as read. No firmware update, arbitrary K factor, motion calibration value or new global printer profile was applied.
