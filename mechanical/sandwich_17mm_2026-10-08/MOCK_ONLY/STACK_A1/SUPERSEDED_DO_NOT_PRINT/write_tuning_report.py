"""Report measured slicer comparisons and a reconciled filament breakdown."""
from pathlib import Path
import json,math
HERE=Path(__file__).resolve().parent
REVIEW=HERE/'review'

def main():
    tuning=json.loads((REVIEW/'parameter-tuning.json').read_text())
    selected=json.loads((REVIEW/'stacked_kit-slice.json').read_text())['sliced_plates'][0]
    trial=json.loads((REVIEW/'separator_trial-slice.json').read_text())['sliced_plates'][0]
    verification=json.loads((REVIEW/'stack-verification.json').read_text())
    volumes=verification['feature_volumes_mm3']
    density={'PLA':1.26,'PETG':1.27}
    mass=lambda f,m:volumes.get(f+' / '+m,0)*density[m]/1000
    scaffold=mass('Support','PLA')+mass('Support transition','PLA')
    interfaces=mass('Support interface','PETG')
    tower={m:mass('Prime tower',m) for m in density}
    totals={m:selected['filaments'][i]['total_used_g'] for i,m in enumerate(density)}
    main_mass={m:selected['filaments'][i]['main_used_g'] for i,m in enumerate(density)}
    # Slicer main_used_g excludes the prime tower. Keep that tower separate
    # rather than mislabelling all total-minus-main consumption as purge.
    purge={m:totals[m]-main_mass[m]-tower[m] for m in density}
    rows=[{'category':'Mock parts + adhesion brim','PLA_g':main_mass['PLA']-scaffold,'PETG_g':0},
          {'category':'Support scaffold + transition layers','PLA_g':scaffold,'PETG_g':0},
          {'category':'PETG release interfaces','PLA_g':0,'PETG_g':interfaces},
          {'category':'Prime / wipe tower','PLA_g':tower['PLA'],'PETG_g':tower['PETG']},
          {'category':'Purge and material-change waste (inferred remainder)','PLA_g':purge['PLA'],'PETG_g':purge['PETG']}]
    for row in rows:row['total_g']=row['PLA_g']+row['PETG_g']
    for m in density:assert abs(sum(row[m+'_g'] for row in rows)-totals[m])<.001
    all_in={m:totals[m]+trial['filaments'][i]['total_used_g'] for i,m in enumerate(density)}
    data={'method':'Main mass is slicer-reported deposition excluding tower. Category volumes are parsed from positive XY extrusion in saved G-code. Prime tower is measured separately; purge is total minus main minus tower. Parts include brim and a small rounding/unclassified-extrusion residual.',
        'density_g_cm3':density,'filament_diameter_mm':1.75,'categories':rows,'job_totals_g':totals,
        'trial_totals_g':{m:trial['filaments'][i]['total_used_g'] for i,m in enumerate(density)},
        'full_job_plus_trial_g':all_in,'suggested_available_g':{'PLA':750,'PETG':250},
        'filament_length_m':{m:totals[m]/density[m]/(math.pi*(1.75/2)**2) for m in density},
        'limitations':'Slicer predictions, not weighed consumption. Startup/calibration routines, nozzle cleaning, runout recovery and failures can consume additional filament. PETG density is assumed 1.27 g/cm3 because Basic versus HF is unconfirmed.'}
    (REVIEW/'material-breakdown.json').write_text(json.dumps(data,indent=2))
    base=tuning['baseline'];total=lambda p:sum(f['total_used_g'] for f in p['filaments'])
    text='''# Print-parameter tuning and material breakdown

Updated 23 October 2026. A1 / 0.4 mm nozzle / Textured PEI / AMS Lite. Bambu brand is confirmed; PETG Basic versus HF is unknown. All results are file/slicer estimates. No physical calibration or print was performed.

## Candidate slices

| Profile | Estimated hours | PLA + PETG | Model-layer choice |
|---|---:|---:|---|
'''
    text+=f'| Previous stack profile | {base["total_predication"]/3600:.2f} | {total(base):.1f} g | Uniform 0.10 mm |\n'
    for name,label in [('balanced','Thinner skins, fine surfaces'),('hybrid','Same, with protected 0.20 mm interior bands'),('interface80','Selected: faster interfaces / tower')]:
        r=tuning['candidates'][name]['plate'];layers='0.10 / 0.20 mm' if name=='hybrid' else 'Uniform 0.10 mm'
        text+=f'| {label} | {r["total_predication"]/3600:.2f} | {total(r):.1f} g | {layers} |\n'
    text+=f'''
The selected profile saves **{(base['total_predication']-selected['total_predication'])/3600:.2f} hours ({100*(1-selected['total_predication']/base['total_predication']):.1f}%)** and **{total(base)-total(selected):.1f} g ({100*(1-total(selected)/total(base)):.1f}%)** against the previous package. This is the best tested balance, not an experimentally established optimum.

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
'''
    for row in rows:text+=f'| {row["category"]} | {row["PLA_g"]:.1f} g | {row["PETG_g"]:.1f} g | {row["total_g"]:.1f} g |\n'
    text+=f'| **Full job total** | **{totals["PLA"]:.1f} g** | **{totals["PETG"]:.1f} g** | **{sum(totals.values()):.1f} g** |\n'
    text+=f'''
The prime tower is **separate from purged filament**. The slicer's main mass excludes that tower; the purge row is total mass minus main mass minus measured tower extrusion. Support/scaffold and interface masses come from their G-code feature volumes. The parts row includes the small adhesion brim and approximately 0.07 g of rounding/unclassified deposition so the table reconciles to the slicer's totals. This is an estimate, not a weighed audit; see [material-breakdown.json](material-breakdown.json).

Approximate filament lengths: **{data['filament_length_m']['PLA']:.1f} m PLA / {data['filament_length_m']['PETG']:.1f} m PETG**, at 1.75 mm diameter and assumed densities 1.26 / 1.27 g/cm³. Basic/HF PETG density differs slightly, so that material's grams can shift by a few percent.

| What to allow for | PLA | PETG | Total |
|---|---:|---:|---:|
| Six-part quality/separation trial | {data['trial_totals_g']['PLA']:.1f} g | {data['trial_totals_g']['PETG']:.1f} g | {sum(data['trial_totals_g'].values()):.1f} g |
| Full job plus one trial | {all_in['PLA']:.1f} g | {all_in['PETG']:.1f} g | {sum(all_in.values()):.1f} g |
| Practical minimum available, with margin | 750 g | 250 g | 1,000 g |

Startup priming, printer calibration, cleaning, runout recovery and failures can use additional material; the margin covers some of that uncertainty. A full 1 kg PLA spool and at least 300 g PETG are a comfortable alternative if remaining spool weights are uncertain. AMS changes remain **{selected['filament_change_times']}**; support contacts and the 800 mm³ flushing matrix were preserved.

## Physical trial before the long job

Print `separator_trial.gcode.3mf`: two screen frames, two 0.50 mm washers, one option cap and one screen stop. Peel both stacked pairs without tearing them. Measure frame and washer thickness, inspect PETG residue, verify the post bore/seat and slide the cap in its real guide. Look for weak PLA layers after PETG changes. Adjust only after observing a concrete defect; a successful slice cannot establish release, accuracy or layer adhesion on the actual printer.

## References

- [Prusa: layers, perimeters and solid skins](https://help.prusa3d.com/article/layers-and-perimeters_1748): layer-height/time tradeoff and top-skin support by infill.
- [Prusa: variable layers](https://help.prusa3d.com/article/variable-layer-height-function_1750): use fine layers where shape needs them, coarser regions elsewhere. Here the measured gain was too small to select it.
- Bambu material values were read from the installed A1 `Bambu PLA Basic`, `Bambu PETG Basic` and `Bambu PETG HF` presets, not inferred from brand alone.
'''
    (REVIEW/'TUNING.md').write_text(text,encoding='utf-8')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
