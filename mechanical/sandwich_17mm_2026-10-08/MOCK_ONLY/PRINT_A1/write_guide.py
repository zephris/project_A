"""Generate the filename-linked, one-part print guide from validated slices."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def write_guide():
    plan=json.loads((HERE/'print-plan.json').read_text())
    check=json.loads((HERE/'print-check.json').read_text())
    estimates={r['plate']:r for r in check['results']}
    lines=['# Bambu A1 PLA mock kit â€” one part per file','',
        'Updated 18 October 2026. **Every project and sliced file contains one mock part or one quarter-section.** Each physical component is a separate top-level model with its own name; no assembly wrapper combines them. Printer: Bambu Lab A1, 256 Ã— 256 mm, AMS Lite, PLA. Nothing has been sent to a printer.','',
        'Download `A1_PLA_fitment_kit.zip`. `parts/<part-name>.3mf` is an editable unsliced project; `sliced/<part-name>.gcode.3mf` is its validated Bambu Studio slice. Print each required file once. Identical repeated mounts retain separate numbered filenames so the full assembly quantity is explicit.','',
        '## Oversized parts','',
        'Six full parts exceed the usable A1 bed: PCB surrogate, top acrylic surrogate, bottom acrylic surrogate, top spacer, bottom spacer and switch plate. Each is divided into **four quarter-sections**, with a separate file for every section. No full-size alternatives are in this package. The largest section is 146.3 Ã— 95.5 mm. There is no scaling.','',
        'Quarter seams have no interlocking joints. Reconstruct each original part on a flat jig, using the [source manifest](../manifest.json) bounds to identify the original section positions; tape the reverse faces temporarily. Some sections have disconnected islands belonging to that same original part: preserve their positions on the jig. They cannot reproduce full-panel stiffness or support fastening loads.','',
        '## Print order and direct file links','',
        '### 1. Initial dimension trial â€” 0.4 mm nozzle','',
        'Print these small parts first, then measure holes, seats and option-cap travel. Do not print a second copy when these names appear in step 3.','']
    for name in ('screen_frame','printed_screen_stop_1_3mm','OPSW1_captive_cap_H5_trial'):
        lines.append(f'- [{name}.gcode.3mf](sliced/{name}.gcode.3mf) â€” [editable {name}.3mf](parts/{name}.3mf).')
    lines+=['','Check a real Choc V2 switch with [switch_coupon.step](../../STEP/switch_coupon.step) before printing the full switch-plate sections. This separate STEP coupon must be imported and sliced; it is not pre-sliced in this package.','']
    steps=[('2. Simple panel, PCB and case-column surrogates â€” 0.6 mm nozzle',lambda r:not r['optional'] and r['nozzle_mm']==0.6),
           ('3. Spacers, switch plate, heatsink and mounting parts â€” 0.4 mm nozzle',lambda r:not r['optional'] and r['nozzle_mm']==0.4),
           ('4. PLA collar shape surrogates â€” 0.2 mm nozzle',lambda r:not r['optional'] and r['nozzle_mm']==0.2),
           ('5. Optional height gauges and fastener envelopes â€” 0.2 mm nozzle',lambda r:r['optional'])]
    for title,predicate in steps:
        lines+=['### '+title,'','| Print filename (sliced) | Editable project | PLA | Estimated time |','|---|---|---:|---:|']
        for row in plan['print_plan']:
            if not predicate(row):continue
            n=row['plate'];e=estimates[n]
            lines.append(f'| [{n}.gcode.3mf](sliced/{n}.gcode.3mf) | [{n}.3mf](parts/{n}.3mf) | {e["grams"]:.2f} g | {e["seconds"]/60:.0f} min |')
        lines+=['']
    required=check['required'];allparts=check['all']
    lines+=['## Settings and estimates','',
        f'**Required: {required["files"]} separate prints, about {required["grams"]:.0f} g / {required["hours"]:.1f} hours.** All optional gauges included: {allparts["files"]} separate prints, {allparts["grams"]:.0f} g / {allparts["hours"]:.1f} hours. Individual printing adds startup and handling compared with the previous grouped kit. Estimates include slicer startup, supports and brims, but exclude nozzle changes, cooling/removal, manual handling and failures.','',
        '- 0.6 mm simple surrogates and 0.4 mm spacers/case posts: 0.20 mm layers, two walls, two top/bottom shells and 5% rectilinear infill.','- 0.4 mm detail parts: 0.10 mm layers, two walls, three top/bottom shells and 8% infill.','- 0.2 mm collar surrogates: 0.10 mm layers. Optional gauges/envelopes: 0.05 mm layers including the first layer.','- Generic PLA profiles; Textured PEI Plate; 220 Â°C nozzle / 65 Â°C bed. Match the physical bed and actual PLA in Bambu Studio and re-slice if different. Match the installed nozzle to each file before printing. The 0.2 mm profile uses its dedicated flow limit.','- One PLA colour/AMS slot, zero in-print filament changes and no prime tower. Automatic bed-only supports where detected; 3 mm brims for large/simple parts, 2 mm for details. Gauges disable supports.','',
        '## Fitment limits','',
        'The collars are **PLA shape surrogates**, not compliant seals. Test insertion force and sealing with the real TPU95A collars separately. [Bambu A1 documentation](https://cdn1.bambulab.com/documentation/quick-start-f507128172bdf/Quick%20start%20guide%20-%20A1%20combo-EN.pdf) cautions against feeding ordinary flexible TPU through AMS Lite.','',
        'Printed threads are omitted. Use real fasteners for closed fit trials. Clip-on heatsink posts have not been implemented. The heatsink retention design still needs qualification. **Do not power a board with the plastic heatsink or rigid thermal-pad gauges fitted.** Use real electronics, foam and thermal pads to qualify topography and compression.','',
        'Layer quantisation and printer calibration affect fit: measure actual heights, bores and mating shoulders. A successful slice does not establish strength, adhesion or dimensional accuracy. Quarter pieces must remain temporary unpowered mock sections.','',
        '## Verification and rebuilding','',
        '[print-plan.json](print-plan.json) maps every file to its source STL. [print-check.json](print-check.json) verifies 105 separate files, one source part per file, source hashes, independent build objects, native slicer object/part counts, mesh dimensions, bed placement, no scaling, successful A1 slices, matching nozzle/PLA settings, no slicer warnings, no prime tower and no filament changes. The [preview sheet](review/part-overview.png) shows the first 24 individual files; every sliced project also contains its own preview.','',
        'Rebuild with the existing project Python environment: `prepare_prints.py`, `slice_plates.py`, then `check_and_package.py`. The scripts use installed Bambu Studio at `D:/Bambu Studio`; adjust that path on another computer. All slicing runs locally and does not contact a printer. Successful slice records are retained in `slice-results.json`; disposable `jobs/` scratch copies and build logs can be removed after validation.','']
    (HERE/'README.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':write_guide()
