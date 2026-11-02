# Print-parameter tuning and material breakdown

Updated 23 October 2026. A1 / 0.4 mm nozzle / Textured PEI / AMS Lite. Bambu brand is confirmed; PETG Basic versus HF is unknown. All results are file/slicer estimates. No physical calibration or print was performed.

## Candidate slices

| Profile | Estimated hours | PLA + PETG | Model-layer choice |
|---|---:|---:|---|
| Previous stack profile | 65.25 | 958.9 g | Uniform 0.10 mm |
| Thinner skins, fine surfaces | 60.26 | 830.7 g | Uniform 0.10 mm |
| Same, with protected 0.20 mm interior bands | 59.73 | 829.8 g | 0.10 / 0.20 mm |
| Selected: faster interfaces / tower | 55.61 | 830.7 g | Uniform 0.10 mm |

The selected profile saves **9.64 hours (14.8%)** and **128.2 g (13.4%)** against the previous package. This is the best tested balance, not an experimentally established optimum.

## Applied settings and purpose

| Setting | Previous | Applied |
|---|---|---|
| Model layers / first layer | 0.10 / 0.10 mm | 0.10 / 0.10 mm |
| Top shell | 1.0 mm minimum, effectively 10 layers | 4 layers / 0.4 mm minimum |
| Bottom shell | 3 layers | 3 layers / 0.3 mm minimum |
| Infill | 8% | 10% rectilinear, supporting the thinner skins |
| Outer wall | 200 mm/s, 5,000 mm/s² | 100 mm/s, 2,000 mm/s² |
| Inner wall | 300 mm/s | 200 mm/s, 4,000 mm/s² |
| Small perimeters | Threshold disabled | 6 mm threshold, 35 mm/s |
| Top surface | 200 mm/s | 80 mm/s, 1,500 mm/s² |
| First-layer wall / infill | 50 / 105 mm/s | 30 / 50 mm/s |
| Support interface | 40 mm/s | 80 mm/s; dense two-layer PETG contacts retained |
| Prime tower speed cap | 90 mm/s | 120 mm/s; tower remains enabled |
| Travel speed cap | 700 mm/s | 500 mm/s |
| PLA profile | Generic PLA | Installed Bambu PLA Basic, 220 °C, 21 mm³/s limit, 0.98 flow ratio |
| PETG profile | Generic PETG, 255 °C | Conservative Bambu interface: 245 °C, 8 mm³/s limit, 0.94 flow ratio |
| Change-material purge | 800 mm³ each way, 255 °C | 800 mm³ each way, 245 °C |

The large time saving comes from removing excess solid skin and raising interface speed; external surfaces and small features are deliberately slower. The 0.4 mm top skin has four passes, and higher infill backs it. Two perimeter walls remain. Tiny washers and thin interfaces remain solid where wall/skin counts fill them. These are shape surrogates, not qualified structural parts.

The variable-layer test protected horizontal features but saved only 32 minutes over the fine candidate. Uniform layers avoid changing vertical fit resolution for that small gain. The final geometry XML hash matches the pre-tuning input, actual 3MF mesh transforms match the part manifest, and every part's first/last model-layer heights remain within 0.051 mm of the source bounds. Every elevated part retains PETG below it. Support and material checks are in `stack-verification.json` and the independent file receipts.

PETG Basic and HF have different stock settings. The selected PETG profile uses their common 0.94 flow ratio, a conservative 8 mm³/s cap and 245 °C; it is explicitly a custom compromise, not an exact HF preset. Confirm the spool label when practical. No unmeasured pressure-advance constant, flow calibration or reduced cross-material purge was invented. The hardware's physical flow and release behavior still need the trial.

## Full-job material, including purges

| Category | PLA | PETG | Combined |
|---|---:|---:|---:|
| Mock parts + adhesion brim | 341.5 g | 0.0 g | 341.5 g |
| Support scaffold + transition layers | 187.1 g | 0.0 g | 187.1 g |
| PETG release interfaces | 0.0 g | 102.2 g | 102.2 g |
| Prime / wipe tower | 31.3 g | 15.2 g | 46.5 g |
| Purge and material-change waste (inferred remainder) | 76.4 g | 77.0 g | 153.5 g |
| **Full job total** | **636.3 g** | **194.4 g** | **830.7 g** |

The prime tower is **separate from purged filament**. The slicer's main mass excludes that tower; the purge row is total mass minus main mass minus measured tower extrusion. Support/scaffold and interface masses come from their G-code feature volumes. The parts row includes the small adhesion brim and approximately 0.07 g of rounding/unclassified deposition so the table reconciles to the slicer's totals. This is an estimate, not a weighed audit; see [material-breakdown.json](material-breakdown.json).

Approximate filament lengths: **210.0 m PLA / 63.6 m PETG**, at 1.75 mm diameter and assumed densities 1.26 / 1.27 g/cm³. Basic/HF PETG density differs slightly, so that material's grams can shift by a few percent.

| What to allow for | PLA | PETG | Total |
|---|---:|---:|---:|
| Six-part quality/separation trial | 11.1 g | 7.3 g | 18.4 g |
| Full job plus one trial | 647.4 g | 201.7 g | 849.1 g |
| Practical minimum available, with margin | 750 g | 250 g | 1,000 g |

Startup priming, printer calibration, cleaning, runout recovery and failures can use additional material; the margin covers some of that uncertainty. A full 1 kg PLA spool and at least 300 g PETG are a comfortable alternative if remaining spool weights are uncertain. AMS changes remain **160**; support contacts and the 800 mm³ flushing matrix were preserved.

## Physical trial before the long job

Print `separator_trial.gcode.3mf`: two screen frames, two 0.50 mm washers, one option cap and one screen stop. Peel both stacked pairs without tearing them. Measure frame and washer thickness, inspect PETG residue, verify the post bore/seat and slide the cap in its real guide. Look for weak PLA layers after PETG changes. Adjust only after observing a concrete defect; a successful slice cannot establish release, accuracy or layer adhesion on the actual printer.

## References

- [Prusa: layers, perimeters and solid skins](https://help.prusa3d.com/article/layers-and-perimeters_1748): layer-height/time tradeoff and top-skin support by infill.
- [Prusa: variable layers](https://help.prusa3d.com/article/variable-layer-height-function_1750): use fine layers where shape needs them, coarser regions elsewhere. Here the measured gain was too small to select it.
- Bambu material values were read from the installed A1 `Bambu PLA Basic`, `Bambu PETG Basic` and `Bambu PETG HF` presets, not inferred from brand alone.
