"""Publish the validated replacement-only job and explicit consumption estimate."""
from pathlib import Path
import json,hashlib,zipfile,math
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent

def main():
    m=json.loads((HERE/'stack-manifest.json').read_text())
    v=json.loads((HERE/'review/verification.json').read_text())
    a=json.loads((HERE/'review/bounds-audit.json').read_text())
    material=json.loads((HERE/'review/material-breakdown.json').read_text())
    receipt=json.loads((HERE/'review/file-inspection.json').read_text())
    digest=hashlib.sha256((HERE/'reprint_stack.gcode.3mf').read_bytes()).hexdigest()
    assert not v['failures'] and not a['failures'] and digest==a['sha256']==v['Gcode_sha256']==receipt['artifact']['sha256']
    old=json.loads((HERE/'review/initial-order-materials.json').read_text())
    comparison={'initial_estimated_hours':old['estimated_hours'],'selected_estimated_hours':material['estimated_hours'],
                'saved_hours':old['estimated_hours']-material['estimated_hours'],
                'saved_filament_g':sum(old['totals_g'].values())-sum(material['totals_g'].values()),
                'reason':'All broad lower carriers placed below the tall upper spacers; no higher carrier floor over a tall spacer cavity.',
                'part_geometry_changed':False}
    (HERE/'review/ordering-comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
    im=Image.new('RGB',(1500,900),'white');d=ImageDraw.Draw(im)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    title=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',27)
    d.text((30,15),'A1 replacement-only stack — 20 independent parts',font=title,fill='#203849')
    scale=2.25;ox,oy=35,75
    d.rectangle((ox,oy,ox+256*scale,oy+256*scale),fill='#f1f5f8',outline='#203849',width=2)
    def box(p,color):
        x,y=p['x'],p['y'];w,h=p['footprint_mm']
        d.rectangle((ox+x*scale,oy+(256-y-h)*scale,ox+(x+w)*scale,oy+(256-y)*scale),fill=color,outline='#36566d')
    for p in sorted(m['parts'],key=lambda p:p['z']):box(p,'#a8cadc' if p['column'].startswith('panel') else '#edc88f')
    tower=a['xy_bounds_mm']['feature/Prime tower'];x0,y0,x1,y1=tower
    d.rectangle((ox+x0*scale,oy+(256-y1)*scale,ox+x1*scale,oy+(256-y0)*scale),fill='#65a780',outline='#204b35')
    d.text((ox+200*scale,oy+(256-200)*scale),'Tower',font=small,fill='white')
    d.text((35,670),'Stock 256 × 256 mm bed. Ordinary paths retain ≥9.36 mm edge clearance.',font=font,fill='#203849')
    d.text((35,705),'Blue: two panel stacks. Gold: small parts at bed level. Green: actual tower bounds.',font=small,fill='#36566d')
    d.text((700,75),'Vertical print order (bottom → top)',font=title,fill='#203849')
    base_y=650;zs=14
    for ci,col in enumerate(('panel 1','panel 2')):
        x=740+ci*350
        d.text((x,125),col.upper(),font=font,fill='#203849')
        for idx,p in enumerate(m['parts'],1):
            if p['column']!=col:continue
            z=p['z'];h=p['size_mm'][2]
            if z:d.rectangle((x,base_y-z*zs,x+245,base_y-(z-1)*zs),fill='#78b18e')
            d.rectangle((x,base_y-(z+h)*zs,x+245,base_y-z*zs),fill='#91bdd4',outline='white')
            short=p['name'].replace('_SURROGATE','').replace('_QUARTER_',' Q')
            d.text((x+5,base_y-(z+h/2)*zs-7),f'{idx:02d} {short}',font=small,fill='#203849')
    d.text((740,690),'Green intervals: 1 mm supported separation.',font=font,fill='#36566d')
    d.text((740,725),'PLA parts and scaffold; PETG contact layers on both faces.',font=font,fill='#36566d')
    d.text((35,805),f"Estimated {material['estimated_hours']:.2f} h; PLA {material['totals_g']['PLA']:.1f} g / PETG {material['totals_g']['PETG']:.1f} g; {material['AMS_changes']} changes.",font=title,fill='#203849')
    im.save(HERE/'review/bed-and-stack-layout.png')
    rows='\n'.join(f"| {i:02d} | [{p['name']}.stl]({p['source']}) | {p['column']} | {p['z']:.2f} |" for i,p in enumerate(m['parts'],1))
    materials='\n'.join(f"| {r['category']} | {r['PLA_g']:.1f} g | {r['PETG_g']:.1f} g |" for r in material['categories'])
    hours=int(material['estimated_hours']);minutes=round((material['estimated_hours']-hours)*60)
    readme=f'''# A1 replacement-only vertical print job

30 October 2026. **PLA for every model, including the three blanking plugs. PETG
is used only for release interfaces.** This replaces the changed pieces of the
older mock kit; it does not reprint all 105 old parts. No printer was contacted
and no print was started.

## Files and print setup

1. Review [reprint_stack_project.3mf](reprint_stack_project.3mf), the editable
   native Bambu Studio project. Keep its **single multipart assembly intact**;
   do not auto-arrange, split into independently bed-dropped objects, or scale it.
   All 20 parts remain individually named components inside that assembly.
2. The print file is **[reprint_stack.gcode.3mf](reprint_stack.gcode.3mf)**.
   It was sliced using the installed **Bambu Studio only**, for **Bambu A1,
   0.4 mm standard stainless nozzle, Textured PEI, AMS Lite, by-layer printing**.
   Check those settings and map PLA / PETG to their actual AMS slots in the app.
   Confirm a clear bed and inspect the first layer when starting manually.
3. Estimated **{hours} h {minutes:02d} min**, **{material['totals_g']['PLA']:.1f} g PLA +
   {material['totals_g']['PETG']:.1f} g PETG**, including supports, tower and purge;
   **{material['AMS_changes']} AMS changes**. Have approximately **400 g PLA / 125 g PETG**
   available for this job with margin. Actual usage and time can differ.

![Bed and stacking order](review/bed-and-stack-layout.png)

The 14 panel/frame sections form two independently rising stacks. Six small
parts use the otherwise empty right-hand bed pocket. Source height is **31.05 mm**.
The supported gaps are **1 mm**, with two PETG contact layers on both model-facing
support faces and PLA scaffold between them where space permits. The blank clips
also have PETG support beneath their curved arms. PETG release paths were verified
at actual stepped carrier surfaces, not just overall bounding-box heights.

The rearrangement saves **{comparison['saved_hours']:.2f} hours and {comparison['saved_filament_g']:.1f} g**
versus the first replacement slice without altering part geometry: broad carrier
floors sit below tall upper-spacer cavities. [Comparison](review/ordering-comparison.json).

## Included replacement parts

- Four top-cover surrogate quarters, four switch-plate quarters and four lower-spacer quarters.
- Upper-spacer quarters **3 and 4** and one option retainer.
- Lower foam-height gauges **1 and 7**, plus **three PLA blanking-plug trials**.

Reuse the old bottom-cover quarters, upper-spacer quarters 1/2, screen frame and
small mounts, six option plungers, heatsink surrogate/mounting parts, case posts,
washers and USB collars. The two retained upper-spacer quarters were compared
against the old native CAD; both added/removed volumes are zero in
[manifest.json](manifest.json). Actual lower foam pads 1/7 need revised cuts;
the printed gauges below are rigid substitutes and do not damp the PCB.

| ID in layout | Individual replacement mesh | Placement | Base Z (mm) |
|---|---|---|---:|
{rows}

Quarter seams have no new interlocks. Reassemble them on a flat jig and tape
the reverse faces temporarily; [raw source bounds](manifest.json) identify the
original section positions. They do not reproduce full-panel stiffness.

## Presets, support and materials

0.10 mm model and first layers; two walls; 10% infill; four top / three bottom
layers. PLA 220 °C, conservative Bambu PETG interface 245 °C / 8 mm³/s, bed 65 °C.
The exact Bambu PLA grade and PETG Basic/HF variant remain unconfirmed. These are
the existing fitment starting profiles, not measured flow calibration.

PETG interfaces use zero top/bottom contact Z gap and zero interface spacing;
supports may start on earlier parts. Prime tower is enabled at X196/Y180,
35 mm width, with 800 mm³ flushing per material-change direction. No flushing
into models, infill or supports. Let the plate cool, then separate the layers
carefully and clear all support from the plug-arm gaps and fingernail grooves.
If support release has not been trialled, use the earlier small separator trial
before committing to a long stack.

| Estimated category | PLA | PETG |
|---|---:|---:|
{materials}
| **Total** | **{material['totals_g']['PLA']:.1f} g** | **{material['totals_g']['PETG']:.1f} g** |

Tower is measured from deposited extrusion; purge is inferred from slicer total
minus main material minus tower. These are estimates, not weighed consumption.
See [material breakdown](review/material-breakdown.json).

## Verification and limits

- All twenty STLs are watertight, finite, bed-oriented and match native dimensions
  within 0.02 mm; [mesh check](review/mesh-check.json). The source CAD inventory was
  rendered and reviewed in [replacement-parts.png](review/replacement-parts.png).
- The saved slice retains twenty named parts and their source geometry hashes;
  maximum native placement deviation **{v['native_position_max_error_mm']:.6f} mm**.
  [Geometry/settings/interfaces](review/verification.json).
- Every elevated section has PETG below it, and both faces of the panel-stack
  gaps have release-interface paths. This proves path presence, not exhaustive
  underside coverage or successful physical separation.
- Generated travel including full circular extrema stays at least **9.36 mm**
  inside the stock 256 mm bed. Deposition including line width has at least
  **10.045 mm** edge margin. The required check margin was 5 mm.
  [Full bounds audit](review/bounds-audit.json).
- Stock A1 start/change/end service templates are unchanged. Their expected
  off-bed wiping/loading/parking moves are reported separately; no machine
  boundary was enlarged or disabled. [Independent file inspection](review/file-inspection.json)
  confirms A1 / 0.4 mm / PLA+PETG / Textured PEI; it is not printer telemetry.
- The saved Bambu [isometric](review/plate_1.png) and [top](review/top_1.png)
  previews were reviewed for placement. They show model geometry; the G-code
  audit separately checks generated support, tower and travel paths.

This is an **unpowered fitment mock**, including rigid foam gauges and PLA plug
trials. PLA clips are not a repeated-removal durability qualification. For each
plug, remove the keycap, orient the grooves left/right (especially at SW16),
clear support from both curved arms, then press evenly into the new 24 mm opening.
The switch may remain fitted if its real height matches the checked model.
Real hardware, support release, material tolerance,
foam preload and thermal performance remain physical-trial requirements.
The wider PCB is still an unrouted candidate, not a fabrication release.
'''
    (HERE/'README.md').write_text(readme,encoding='utf-8')
    selected=[HERE/'README.md',HERE/'manifest.json',HERE/'stack-manifest.json',HERE/'reprint_stack.gcode.3mf',HERE/'reprint_stack_project.3mf']
    selected+=list((HERE/'STL').glob('*.stl'))
    selected+=list((HERE/'presets').glob('*.json'))
    selected+=[HERE/'review'/name for name in ('verification.json','bounds-audit.json','mesh-check.json','material-breakdown.json','file-inspection.json','ordering-comparison.json','bed-and-stack-layout.png','replacement-parts.png','plate_1.png','top_1.png')]
    hashes='\n'.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(HERE).as_posix() for f in sorted(selected))+'\n'
    (HERE/'checksums.sha256').write_text(hashes)
    selected.append(HERE/'checksums.sha256')
    with zipfile.ZipFile(HERE/'PHBox_A1_reprint_stack.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in selected:z.write(f,f.relative_to(HERE).as_posix())
    print(json.dumps({'zip':'PHBox_A1_reprint_stack.zip','files':len(selected),'hours':material['estimated_hours'],'grams':material['totals_g'],'verified_gcode_sha256':digest},indent=2))

if __name__=='__main__':main()
