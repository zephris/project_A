"""Publish only the inset revision; exclude the superseded print files."""
from pathlib import Path
import hashlib,json,math,zipfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
HERE=Path(__file__).resolve().parent
REVIEW=HERE/'review'


def main():
    v=json.loads((REVIEW/'inset-verification.json').read_text())
    audit=json.loads((REVIEW/'inset-bounds-audit.json').read_text())
    assert not v['failures'] and not audit['failures']
    assert hashlib.sha256((HERE/'stacked_kit_inset.gcode.3mf').read_bytes()).hexdigest()==audit['sha256']
    m=json.loads((HERE/'stack-manifest_inset.json').read_text())
    material=json.loads((REVIEW/'inset-material-breakdown.json').read_text())
    trial=json.loads((REVIEW/'separator_trial-slice.json').read_text())['sliced_plates'][0]
    old=json.loads((REVIEW/'original-bounds-audit.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(13,6),gridspec_kw={'width_ratios':[1.1,1]})
    ax=axes[0]
    ax.add_patch(Rectangle((0,0),256,256,facecolor='#f1f4f7',edgecolor='#24364b',lw=1.5))
    ax.add_patch(Rectangle((5,5),246,246,fill=False,edgecolor='#c85b37',ls='--',lw=1))
    for part in sorted(m['parts'],key=lambda p:p['z'],reverse=True):
        ax.add_patch(Rectangle((part['x'],part['y']),*part['footprint_mm'],facecolor='#237ba0',alpha=.16,edgecolor='#237ba0',lw=.3))
    tower=audit['xy_bounds_mm']['feature/Prime tower']
    ax.add_patch(Rectangle(tower[:2],tower[2]-tower[0],tower[3]-tower[1],facecolor='#59a26b',alpha=.8))
    ax.text(213,198,'Prime\ntower',ha='center',va='center',fontsize=9,color='white')
    travel=audit['xy_bounds_mm']['generated_travel_envelope']
    ax.add_patch(Rectangle(travel[:2],travel[2]-travel[0],travel[3]-travel[1],fill=False,edgecolor='#172b4d',lw=1.2))
    ax.set(xlim=(-5,261),ylim=(-5,261),aspect='equal',xlabel='X (mm)',ylabel='Y (mm)',title='Inset replacement on the stock A1 bed')
    ax.text(128,-34,'Dashed: 5 mm acceptance margin. Dark outline: generated travel envelope.',ha='center',fontsize=8)
    for ci,col in enumerate(('panel 1','panel 2')):
        for p in m['parts']:
            if p['column']!=col:continue
            z=p['z'];h=p['size_mm'][2]
            if z>0:axes[1].add_patch(Rectangle((ci,z-1),.8,1,facecolor='#83b88c',edgecolor='none'))
            axes[1].add_patch(Rectangle((ci,z),.8,h,facecolor='#267da3',edgecolor='white',lw=.4))
    axes[1].set(xlim=(-.2,2),ylim=(-1,65),ylabel='Height above bed (mm)',xticks=[.4,1.4],xticklabels=['Panel stack 1','Panel stack 2'],title='Independent panel-stack heights')
    axes[1].grid(axis='y',alpha=.2)
    axes[1].text(.5,-.1,'Green intervals: supported separation; small parts occupy side pockets.',transform=axes[1].transAxes,ha='center',fontsize=8)
    fig.tight_layout();fig.subplots_adjust(bottom=.16)
    fig.savefig(REVIEW/'inset-bed-layout.png',dpi=160);plt.close(fig)
    rows=''
    for row in material['categories']:
        rows+=f'| {row["category"]} | {row["PLA_g"]:.1f} g | {row["PETG_g"]:.1f} g |\n'
    totals=material['job_totals_g'];total=sum(totals.values())
    report=f'''# A1 inset revision — bounds investigation

23 October 2026. Bambu Studio **02.07.01.62** was the only slicer used. No printer was contacted and no print/calibration was started.

## Confirmed cause and repair

The A1's stock printing polygon is **X/Y 0–256 mm**, with 256 mm height. The installed and [official A1 profile](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/machine/Bambu%20Lab%20A1%200.4%20nozzle.json) have no bed-exclusion polygon. The part bodies are only one part of this constraint: generated supports, brims, prime tower and curved travel all need room. Sequential-object toolhead clearances are not an instruction to subtract that radius from every bed edge; this job prints **by layer**.

The original file's extrusion stayed on the bed, but its generated circular Z-hop travel reached **X = −0.270 mm and 256.080 mm**. Its support extrusion came as close as about **0.405 mm** to the left edge when line width is included. The previous verifier checked arc endpoints and missed their intermediate extrema. [Original audit](original-bounds-audit.json) identifies the exact file hash and commands; this is consistent with the user's Bambu Studio warning. The warning itself has not been re-observed through live UI control.

The replacement uses **two independent panel stacks**, 14 mm minimum model-placement inset and model coordinates no higher than 242 mm, with a separate prime-tower reserve. All **105 named components** are retained, with the same source hashes and exact source dimensions. Quarter-panel divisions and the 1 mm supported separators remain. Source height is **{m['height_mm']:.2f} mm**. Source/native placement difference is at most **{v['native_position_max_error_mm']:.6f} mm**.

## New saved-slice checks

| Check | Result |
|---|---|
| Bambu CLI slicing / exported outside flag | Success / false |
| Generated deposition including line width | X 10.601–245.200, Y 10.451–245.050 mm |
| Generated travel including circular extrema | X 9.916–245.708, Y 9.766–244.750 mm |
| Required margin from each bed edge | 5 mm; passed, smallest measured ordinary-travel margin 9.766 mm |
| Prime tower including deposited line width | X 192.829–234.171, Y 176.829–218.921 mm |
| Separate meshes / build containers | 105 / one multipart assembly |
| Minimum stacked bounding-box gap | {v['minimum_stacked_bbox_separation_mm']:.3f} mm |
| Elevated parts checked for PETG beneath | {len(v['contacts'])}; all have interface segments in their footprints |
| Ordinary travel arcs checked | {audit['arcs'].get('generated',0):,} |

Stock startup, filament-change, timelapse and shutdown templates are unchanged. Their off-bed loading/wiping/parking motions are reported separately, including return to the model. Those service movements are not model extrusion. No bed size, firmware limit or boundary guard was enlarged or disabled. The audit includes complete XY circles/helices; it distinguishes service blocks by their actual Bambu markers rather than ignoring every out-of-range coordinate.

See [new bounds audit](inset-bounds-audit.json), [geometry/material verification](inset-verification.json), [bed placement](inset-bed-layout.png), [Bambu isometric preview](inset-plate_1.png) and [Bambu top preview](inset-top_1.png). I reviewed both Bambu previews: two broad panel stacks with the smaller parts in side/top pockets; no source part was resized. A separate CAD snapshot process stalled and was stopped; the saved Bambu previews and deterministic saved-mesh checks were used for visual/layout review.

## Time and material

Estimated **{material['estimated_hours']:.2f} hours**, **{totals['PLA']:.1f} g PLA + {totals['PETG']:.1f} g PETG = {total:.1f} g**, **{material['AMS_changes']} AMS changes**. The superseded slice was about 55.61 h / 830.7 g / 160 changes. The new layout gains edge clearance with approximately 4 g additional total material and fewer changes. A 60 mm source height still fits the stock 256 mm Z limit.

| Category | PLA | PETG |
|---|---:|---:|
{rows}| **Total** | **{totals['PLA']:.1f} g** | **{totals['PETG']:.1f} g** |

Tower is measured separately from purge. Purge is the inferred remainder after subtracting slicer main mass and measured tower mass; these are estimates, not weighed consumption. The unchanged six-part trial adds {trial['filaments'][0]['total_used_g']:.1f} g PLA / {trial['filaments'][1]['total_used_g']:.1f} g PETG. With one trial, allow at least 750 g PLA and 250 g PETG available; startup and calibration add uncertainty. See [material breakdown](inset-material-breakdown.json).

Physical first-layer behavior, moisture, material-change strength and support release remain subject to the [calibration plan](../CALIBRATION_A1/PLAN.md). Contact-path presence does not prove complete underside coverage. The fitment mock does not establish production hardware strength, TPU sealing, thermal performance or actual fastener/dongle fit.

## Local slicing runner

Direct PowerShell `Start-Process` execution of the installed Bambu executable completed successfully with the existing presets. Python's direct launch and the MCP wrapper failed earlier; their root cause is not established. `slice_stack.ps1` retains the successful launch method and checks for a fresh result. No alternative slicer was downloaded or installed.
'''
    (REVIEW/'INSET_REVISION.md').write_text(report,encoding='utf-8')
    readme=f'''# A1 stacked fitment kit — inset replacement

Updated 23 October 2026. **Use this INSET revision.** The earlier stack was reported out of bounds in Bambu Studio; its files and package are quarantined in `SUPERSEDED_DO_NOT_PRINT/`. This replacement was freshly sliced using **Bambu Studio only**, for **A1 / AMS Lite / 0.4 mm nozzle / Textured PEI**.

## Print and review files

1. Follow the [calibration plan](CALIBRATION_A1/PLAN.md), then use the existing small [separator_trial.gcode.3mf](separator_trial.gcode.3mf), about **94 min / 18.4 g**. Check release, thickness, layer cohesion and the real mating parts.
2. Open **[stacked_kit_inset_project.3mf](stacked_kit_inset_project.3mf)** to inspect the complete editable Bambu project. It contains 105 named parts inside one multipart assembly. Keep that assembly intact: splitting to objects, dropping to bed or auto-arranging would destroy the supported vertical placements.
3. The prepared replacement is **[stacked_kit_inset.gcode.3mf](stacked_kit_inset.gcode.3mf)**. Estimated **{material['estimated_hours']:.1f} h / {totals['PLA']:.1f} g PLA / {totals['PETG']:.1f} g PETG / {material['AMS_changes']} AMS changes**, including estimated tower and purge material. Re-slice if profiles or placements change.
4. Download **[A1_PLA_PETG_stacked_fitment_kit.zip](A1_PLA_PETG_stacked_fitment_kit.zip)**. It contains the INSET files, not the superseded long-job G-code. [Individual per-part fallback](../PRINT_A1/README.md) remains available.

[Geometry-only inset 3MF](stacked_kit_inset.3mf) is supplied for import. Use the editable project to retain Bambu presets. No print or calibration was started.

## What changed

Two independent panel stacks and smaller side/top-pocket parts replace the edge-hugging three-column layout. All **105 source components keep their exact geometry**; six oversized originals remain quartered, with no scaling. The supported gap remains **1 mm**. Source height is **{m['height_mm']:.2f} mm**. The original had circular travel reaching X −0.270 / 256.080 mm; the replacement's ordinary travel, including arc extrema, stays at least **9.766 mm** from the bed edge. Deposition including width is at least 10.451 mm from the edge. The machine's actual 256 mm limits are unchanged.

Read the [bounds investigation and validation](review/INSET_REVISION.md), [layout drawing](review/inset-bed-layout.png), [actual slice audit](review/inset-bounds-audit.json) and [component checks](review/inset-verification.json). The old validation checked endpoints and missed full travel arcs; it is superseded for print-boundary decisions. Historical tuning/assembly records remain in `review/`; use the `inset-` reports for current layout/time/material figures.

## Presets and materials

- PLA model parts and scaffold; PETG for **two contact layers on each model-facing support face**. Zero contact Z gap and interface spacing; support may start on earlier parts. 0.10 mm model/first layers, 2 walls, 10% infill, top 4 layers / 0.4 mm and bottom 3 / 0.3 mm. Original part dimensions remain unchanged.
- Prime tower enabled at X196/Y180 with its own reserve. **800 mm³ flushing each direction**, no flushing into model, infill or support. The 35 mm tower and 3 mm object brim fit with the generated support/travel envelope.
- PLA 220 °C / 21 mm³/s; conservative PETG 245 °C / 8 mm³/s; bed 65 °C. Bambu brand is confirmed, actual PLA grade and PETG Basic/HF still need checking. Current flow ratios 0.98 / 0.94 are preset starting values, not measured calibration.
- Map PLA and PETG to their **actual AMS Lite slots**. Allow at least **750 g PLA / 250 g PETG** for this job, one trial and some margin. [Material breakdown, including purges](review/inset-material-breakdown.json) gives the separate categories.

## Fitment and assembly

This is an **unpowered PLA fitment mock**. Rigid PLA substitutes do not qualify TPU collars, foam compliance or thermal pads. Do not power the board with a plastic heatsink or rigid pad gauge. Some 0.25–0.6 mm features may require the existing individual 0.2 mm-nozzle fallback; a successful slice does not prove they will survive removal.

Peel supports from the top down while supporting thin panels. Reconstruct quartered plates on a flat jig using original coordinates in `../manifest.json`; temporary taped seams do not reproduce a full panel's stiffness. Test actual switches, screen, PCB, screws and dongles. Existing heatsink retainer/thread-engagement and dongle-body-clearance concerns remain in the [assembly review](review/REVIEW.md).

## Rebuild

Run `build_stack.py`, then **`slice_stack.ps1 -Model stacked_kit_inset`** directly from PowerShell, then `verify_inset.py` and `publish_inset.py`. `slice_stack.py` remains a compatibility wrapper. Bambu's executable is the installed `D:/Bambu Studio/bambu-studio.exe`; no other slicer is used. The rebuild uses retained source STLs and profile helpers in the project. The ZIP is a print/review handoff, not a standalone source repository.
'''
    (HERE/'README.md').write_text(readme,encoding='utf-8')
    names=['README.md','stacked_kit_inset.3mf','stacked_kit_inset_project.3mf','stacked_kit_inset.gcode.3mf',
           'stack-manifest_inset.json','separator_trial.3mf','separator_trial.gcode.3mf','trial-manifest.json',
           'presets/printer.json','presets/stack_inset.json','presets/stack.json','presets/PLA.json','presets/PETG_interface.json',
           'review/INSET_REVISION.md','review/inset-bounds-audit.json','review/inset-verification.json',
           'review/inset-material-breakdown.json','review/stacked_kit_inset-slice.json','review/inset-bed-layout.png',
           'review/inset-plate_1.png','review/inset-top_1.png','review/original-bounds-audit.json',
           'review/REVIEW.md','review/assembly-review.json',
           'CALIBRATION_A1/README.md','CALIBRATION_A1/PLAN.md','CALIBRATION_A1/calibration-status.json',
           'CALIBRATION_A1/PLA_flow_coarse.3mf','CALIBRATION_A1/PETG_flow_coarse.3mf']
    paths=[HERE/name for name in names]
    # Preserve linked historical assembly evidence and calibration instructions,
    # but never include the quarantined long-job G-code or its old package.
    for folder in (REVIEW,HERE/'CALIBRATION_A1'):
        for path in folder.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts and 'working' not in path.parts and path not in paths:
                paths.append(path)
    assert all(p.exists() for p in paths)
    checksum='\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(HERE).as_posix() for p in paths)+'\n'
    (HERE/'checksums.sha256').write_text(checksum,encoding='utf-8')
    archive=HERE/'A1_PLA_PETG_stacked_fitment_kit.zip'
    pending=archive.with_suffix('.zip.pending')
    with zipfile.ZipFile(pending,'w',zipfile.ZIP_DEFLATED,strict_timestamps=False) as z:
        for p in paths+[HERE/'checksums.sha256']:z.write(p,p.relative_to(HERE))
    with zipfile.ZipFile(pending) as z:
        assert z.testzip() is None
        assert 'stacked_kit.gcode.3mf' not in z.namelist()
        assert all('SUPERSEDED' not in name for name in z.namelist())
    pending.replace(archive)
    print(json.dumps({'hours':material['estimated_hours'],'PLA_g':totals['PLA'],'PETG_g':totals['PETG'],
                      'archive':'A1_PLA_PETG_stacked_fitment_kit.zip','files':len(paths)+1,'superseded_gcode_included':False},indent=2))


if __name__=='__main__':main()
