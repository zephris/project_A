# A1 inset revision — bounds investigation

23 October 2026. Bambu Studio **02.07.01.62** was the only slicer used. No printer was contacted and no print/calibration was started.

## Confirmed cause and repair

The A1's stock printing polygon is **X/Y 0–256 mm**, with 256 mm height. The installed and [official A1 profile](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/machine/Bambu%20Lab%20A1%200.4%20nozzle.json) have no bed-exclusion polygon. The part bodies are only one part of this constraint: generated supports, brims, prime tower and curved travel all need room. Sequential-object toolhead clearances are not an instruction to subtract that radius from every bed edge; this job prints **by layer**.

The original file's extrusion stayed on the bed, but its generated circular Z-hop travel reached **X = −0.270 mm and 256.080 mm**. Its support extrusion came as close as about **0.405 mm** to the left edge when line width is included. The previous verifier checked arc endpoints and missed their intermediate extrema. [Original audit](original-bounds-audit.json) identifies the exact file hash and commands; this is consistent with the user's Bambu Studio warning. The warning itself has not been re-observed through live UI control.

The replacement uses **two independent panel stacks**, 14 mm minimum model-placement inset and model coordinates no higher than 242 mm, with a separate prime-tower reserve. All **105 named components** are retained, with the same source hashes and exact source dimensions. Quarter-panel divisions and the 1 mm supported separators remain. Source height is **60.35 mm**. Source/native placement difference is at most **0.000004 mm**.

## New saved-slice checks

| Check | Result |
|---|---|
| Bambu CLI slicing / exported outside flag | Success / false |
| Generated deposition including line width | X 10.601–245.200, Y 10.451–245.050 mm |
| Generated travel including circular extrema | X 9.916–245.708, Y 9.766–244.750 mm |
| Required margin from each bed edge | 5 mm; passed, smallest measured ordinary-travel margin 9.766 mm |
| Prime tower including deposited line width | X 192.829–234.171, Y 176.829–218.921 mm |
| Separate meshes / build containers | 105 / one multipart assembly |
| Minimum stacked bounding-box gap | 1.000 mm |
| Elevated parts checked for PETG beneath | 37; all have interface segments in their footprints |
| Ordinary travel arcs checked | 86,848 |

Stock startup, filament-change, timelapse and shutdown templates are unchanged. Their off-bed loading/wiping/parking motions are reported separately, including return to the model. Those service movements are not model extrusion. No bed size, firmware limit or boundary guard was enlarged or disabled. The audit includes complete XY circles/helices; it distinguishes service blocks by their actual Bambu markers rather than ignoring every out-of-range coordinate.

See [new bounds audit](inset-bounds-audit.json), [geometry/material verification](inset-verification.json), [bed placement](inset-bed-layout.png), [Bambu isometric preview](inset-plate_1.png) and [Bambu top preview](inset-top_1.png). I reviewed both Bambu previews: two broad panel stacks with the smaller parts in side/top pockets; no source part was resized. A separate CAD snapshot process stalled and was stopped; the saved Bambu previews and deterministic saved-mesh checks were used for visual/layout review.

## Time and material

Estimated **55.55 hours**, **661.1 g PLA + 173.6 g PETG = 834.7 g**, **120 AMS changes**. The superseded slice was about 55.61 h / 830.7 g / 160 changes. The new layout gains edge clearance with approximately 4 g additional total material and fewer changes. A 60 mm source height still fits the stock 256 mm Z limit.

| Category | PLA | PETG |
|---|---:|---:|
| Mock parts + adhesion brim | 342.6 g | 0.0 g |
| PLA scaffold + transition | 220.9 g | 0.0 g |
| PETG release interfaces | 0.0 g | 105.1 g |
| Prime tower | 40.3 g | 10.7 g |
| Purge / material-change waste (inferred) | 57.3 g | 57.8 g |
| **Total** | **661.1 g** | **173.6 g** |

Tower is measured separately from purge. Purge is the inferred remainder after subtracting slicer main mass and measured tower mass; these are estimates, not weighed consumption. The unchanged six-part trial adds 11.1 g PLA / 7.3 g PETG. With one trial, allow at least 750 g PLA and 250 g PETG available; startup and calibration add uncertainty. See [material breakdown](inset-material-breakdown.json).

Physical first-layer behavior, moisture, material-change strength and support release remain subject to the [calibration plan](../CALIBRATION_A1/PLAN.md). Contact-path presence does not prove complete underside coverage. The fitment mock does not establish production hardware strength, TPU sealing, thermal performance or actual fastener/dongle fit.

## Local slicing runner

Direct PowerShell `Start-Process` execution of the installed Bambu executable completed successfully with the existing presets. Python's direct launch and the MCP wrapper failed earlier; their root cause is not established. `slice_stack.ps1` retains the successful launch method and checks for a fresh result. No alternative slicer was downloaded or installed.
