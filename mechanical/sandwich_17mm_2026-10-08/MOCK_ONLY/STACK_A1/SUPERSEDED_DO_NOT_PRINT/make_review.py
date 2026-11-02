"""Write visual and dimensional review of the saved stacked print kit."""
from pathlib import Path
import sys,json,math,csv
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import trimesh
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'PRINT_A1'))
from prepare_prints import read_mesh

def main():
    m=json.loads((HERE/'stack-manifest.json').read_text());parts=m['parts']
    review=HERE/'review';review.mkdir(exist_ok=True)
    fontpath=Path('C:/Windows/Fonts/segoeui.ttf')
    font=ImageFont.truetype(str(fontpath),15);large=ImageFont.truetype(str(fontpath),23);small=ImageFont.truetype(str(fontpath),12)
    colours=['#3579B5','#C05F40','#49866C','#8C68A0','#A7832C','#4B92A2']
    tw,th,cols=400,452,4
    image=Image.new('RGB',(cols*tw,85+math.ceil(len(m['tiers'])/cols)*th),'white');d=ImageDraw.Draw(image)
    d.text((20,10),'PHBox — every stacked print group',font=large,fill='#172A3A')
    d.text((20,43),'Numbers map to part-index.csv. Top projections show each unchanged mesh; support is omitted here.',font=font,fill='#334A5C')
    for k,tier in enumerate(m['tiers']):
        ox=(k%cols)*tw+18;oy=85+(k//cols)*th
        d.text((ox,oy),f'T{tier["tier"]:02d}  ·  start Z {tier["z_min"]:.2f} mm',font=large,fill='#172A3A')
        d.text((ox,oy+32),f'{len(tier["parts"])} parts — {tier["column"]}',font=font,fill='#334A5C')
        bx,by=ox,oy+60;s=1.4
        d.rectangle((bx,by,bx+256*s,by+256*s),fill='#F2F5F7',outline='#A4B0B9')
        def point(x,y):return bx+x*s,by+(256-y)*s
        d.rectangle((*point(5,255),*point(65,202)),fill='#DDE2E6')
        for i,p in enumerate(parts):
            if p['tier']!=tier['tier']:continue
            vs,ts,lo,sz=read_mesh(HERE.parent/p['source']);vs=np.array(vs)-lo
            if p['rotation_deg']==90:vs[:,:2]=np.column_stack((sz[1]-vs[:,1],vs[:,0]))
            vs[:,0]+=p['x'];vs[:,1]+=p['y']
            tris=vs[np.array(ts)]
            for tri in tris[np.argsort(tris[:,:,2].mean(axis=1))]:
                if abs(np.cross(tri[1]-tri[0],tri[2]-tri[0])[2])<1e-7:continue
                d.polygon([point(x,y) for x,y,_ in tri],fill=colours[i%len(colours)])
            w,h=p['footprint_mm'];tx,ty=point(p['x']+w/2,p['y']+h/2)
            label=str(i+1);bbox=d.textbbox((0,0),label,font=small);lw,lh=bbox[2],bbox[3]
            d.rectangle((tx-lw/2-2,ty-lh/2-2,tx+lw/2+2,ty+lh/2+2),fill='white')
            d.text((tx-lw/2,ty-lh/2-3),label,font=small,fill='#172A3A')
    image.save(review/'tier-contact-sheet.png')
    with (review/'part-index.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['Index','Part filename','Group','Column','X_mm','Y_mm','Z_mm','Rotation_deg','Source_SHA256'])
        for i,p in enumerate(parts):w.writerow([i+1,p['name']+'.stl',p['tier'],p['column'],p['x'],p['y'],p['z'],p['rotation_deg'],p['sha256']])
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,Patch
    fig,ax=plt.subplots(figsize=(12,6));zmax=m['height_mm']
    for ci,column in enumerate(['panel 1','panel 2','panel 3']):
        for i,p in enumerate(parts):
            if p['column']!=column:continue
            ax.add_patch(Rectangle((ci*1.15,p['z']),.94,p['size_mm'][2],facecolor=colours[i%6],edgecolor='white',lw=.5))
            ax.text(ci*1.15+.47,p['z']+p['size_mm'][2]/2,str(i+1),ha='center',va='center',fontsize=8,color='white')
            if p['z']>0:ax.add_patch(Rectangle((ci*1.15,p['z']-m['gap_mm']),.94,m['gap_mm'],facecolor='#A9CDB4',edgecolor='none'))
    ax.set(xlim=(-.25,3.55),ylim=(-1,zmax+4),ylabel='Height above bed (mm)',xticks=[.47,1.62,2.77],xticklabels=['Panel stack 1','Panel stack 2','Panel stack 3'],title='Independent stack heights — numbered parts and support separators')
    ax.grid(axis='y',alpha=.2);ax.legend(handles=[Patch(facecolor='#A9CDB4',label='1 mm supported separator: PETG / PLA scaffold / PETG')],loc='upper left',bbox_to_anchor=(0,-.12),frameon=False)
    fig.text(.13,.015,'Each PETG face: 2 × 0.10 mm contact layers. Other supports under local recesses are additional. Small parts use side pockets.',fontsize=9)
    fig.subplots_adjust(bottom=.23);fig.savefig(review/'stack-heights.png',dpi=150);plt.close(fig)
    facts=json.loads((HERE/'dfam-facts.json').read_text(encoding='utf-8-sig'))
    mesh=trimesh.load(HERE/'stacked_kit.3mf',force='mesh');bodies=mesh.split(only_watertight=False)
    lows=[];highs=[]
    for p in parts:
        lows.append([p['x'],p['y'],p['z']]);highs.append([p['x']+p['footprint_mm'][0],p['y']+p['footprint_mm'][1],p['z']+p['size_mm'][2]])
    bounds=np.array([lows,highs]).transpose(1,0,2);mapping=[]
    for b,w in zip(bodies,facts['wall_thickness']['per_body']):
        errors=np.abs(bounds-b.bounds).sum(axis=(1,2));j=int(errors.argmin())
        assert errors[j]<.02
        mapping.append(dict(w,part=parts[j]['name'],bounds_match_error_mm=float(errors[j])))
    (review/'wall-thickness-by-part.json').write_text(json.dumps(mapping,indent=2))
    failed=[w for w in mapping if w['p05_mm'] is not None and w['p05_mm']<1.2]
    uncertain=[w for w in mapping if w['min_mm'] is not None and w['min_mm']<1.2 and (w['p05_mm'] is None or w['p05_mm']>=1.2)]
    result=json.loads((review/'stacked_kit-slice.json').read_text())['sliced_plates'][0]
    actual=json.loads((review/'stack-verification.json').read_text());compare=json.loads((review/'placement-comparison.json').read_text())
    old=compare['two_columns_before_optimization'];total=lambda x:sum(f['total_used_g'] for f in x['filaments'])
    reduction=100*(1-total(result)/total(old));time_reduction=100*(1-result['total_predication']/old['total_predication'])
    report=f'''# Geometry, assembly and stacked-print review

Reviewed 23 October 2026. File checks only; no physical print or load qualification.

## Saved geometry and layout

- {len(parts)} source components: 24 quarter-panel sections and 81 smaller models, including 19 optional gauges/envelopes. Native files retain 105 named parts inside one assembly container. No meshes were fused or resized.
- Watertight input mesh: **{facts['mesh']['watertight']}**; {facts['mesh']['body_count']} bodies, {facts['mesh']['triangle_count']:,} triangles. Millimetre scale confirmed by `dfam-facts.json`.
- Envelope: **{facts['mesh']['bbox_mm']} mm**; minimum overlapping-footprint separation **{actual['minimum_stacked_bbox_separation_mm']:.3f} mm**. Source hashes and native positions checked; maximum native-position error {actual['native_position_max_error_mm']:.3g} mm.
- Every elevated part has positive PETG interface extrusion in its footprint directly below its first model layer. This checks support presence, not full-area contact coverage or release force. Process settings select PETG on both top and bottom interfaces.
- [Every print group](tier-contact-sheet.png), [stack heights](stack-heights.png) and [complete numbered file index](part-index.csv). Independent columns can have different start heights; T-numbers identify groups rather than separate build plates.
- Exact toolpath support volume: **{actual['support_deposited_volume_mm3']/1000:.1f} cm³**, counting support, transition and interface extrusion, excluding purge/prime tower. Filament diameter is 1.75 mm. DfAM's prism volume is only an upper bound and is not the sliced support consumption.

## Placement optimization

Three panel columns share the A1 bed. Each rises independently, eliminating height imposed by the tallest member of a common tier. Same-quarter bottom/top spacers share XY and rotation so their perimeter walls overlap. Broad panels sit below open frames. Small parts use low side pockets. The prime tower has a reserved region. Separators are 1 mm instead of 2 mm; each has two 0.10 mm PETG contact layers at each model-facing surface, with sparse PLA scaffold between.

| Candidate | Total PLA + PETG incl. purge/tower | Estimated time | AMS changes |
|---|---:|---:|---:|
'''
    for label,key in [('Earlier two-column layout','two_columns_before_optimization'),('Three across, common tier heights','three_across_global_tiers'),('Independent columns, matched spacers','optimized_independent_stacks')]:
        r=compare[key];report+=f'| {label} | {total(r):.1f} g | {r["total_predication"]/3600:.1f} h | {r["filament_change_times"]} |\n'
    report+=f'''
Combined layout and parameter reduction against the earlier PETG layout: **{reduction:.1f}% total filament and {time_reduction:.1f}% time**. The final row includes the later profile tuning described in [TUNING.md](TUNING.md); it is not solely a placement comparison. This is the best of the sliced candidates, not proof of a global minimum. The single stacked job remains slower and uses more material than printing parts separately.

## Assembly checks

Nine current CAD checks completed with exit 0; outputs are preserved alongside `assembly-review.json`:

| Check | Result and scope |
|---|---|
| Main saved STEP assembly | No board, rigid-part, screw-head or hard-travel collisions in the modeled cases; board float ±0.50 mm XY / ±0.25 mm Z. |
| Option caps | 864 pair tests, no collisions; generic H5 actuator, assumed 0.35 mm actuation. Actual switch part remains unspecified. |
| USB surround integration | Floors, sidewalls, retaining lips and roof material present. USB-A roof belongs to acrylic; USB-C roof belongs to spacer. |
| USB seals | Nine board-edge poses checked without rigid board overlap. Outer 0.2 mm interference is intentional for real TPU. |
| Port roofs | USB-A roof 2 mm; upward-travel shell clearance 0.75 mm. USB-C front roof clearance 0.20 mm in tested pose. |
| Plug/finger access | 1,116 rigid-pair tests without collisions for stated gauges. Dongle assumes 2 mm body setback; the zero-setback control collides with the acrylic roof. |
| Cut profiles | Seven DXFs in mm, zero audit errors. |
| Collar meshes | Both valid single solids; thin membrane and TPU compliance require a trial. |
| Corrected mating sources | No overlaps at switch plate/heatsink, switch plate/top spacer, screen frame/actual module, internal mount pieces or countersunk case head. |

The production layer order remains top acrylic → upper spacer/internal parts → PCB → foam → lower spacer → bottom acrylic, nominal 17 mm excluding keycaps. Reconstruct quartered pieces using the original `../manifest.json` coordinate bounds, on a flat jig. Seams have no joining pins; temporary rear-face tape cannot reproduce full-panel stiffness.

**Open fitment concerns:** heatsink rear retainers are 2 mm thick and omit threads in the mock. M2/M3 ×10 screws have about 0.85 mm engagement, while ×12 protrude about 0.85 mm; fastening needs the real-hardware trial or the documented retainer redesign. The PCB mock omits most real parts/solder; OLED glass/header and actual dongle overmold geometry are not qualified. Rigid PLA collars/foam/pad gauges test shape only. No structural, thermal or seal rating is implied.

## Conservative FDM feature review

Compared to the CAD plugin's [FDM process-limit table](FDM-process-limits.md): 1.2 mm supported wall / 1.6 mm unsupported wall, 45° self-support angle. `wall-thickness-by-part.json` maps measured bodies to their actual named part, matched by bounds.

**{len(failed)} bodies fall below the conservative 1.2 mm supported-wall guide at p05**, including deliberately thin washers, gauges, screen frame or cap features. {len(uncertain)} additional bodies have a sampled minimum below 1.2 mm but p05 above it. These are not blanket printability passes. Representative part measurements follow (min / p05 mm):

'''
    for w in failed:report+=f'- `{w["part"]}.stl`: {w["min_mm"]:.3f} / {w["p05_mm"]:.3f}.\n'
    report+='''
For a generic robust FDM part, thicken a supported wall to at least 1.2 mm (1.6 mm if unsupported). Applying that to a 0.50 mm washer or exact mounting interface would change the fitment test, so the dimensions were preserved. Use the existing individual fine-nozzle files when thin details fail the 0.4 mm trial; treat them as geometry gauges rather than functional hardware. Small-hole diameters, minimum positive feature and bridge span are not exhaustively measured by this tool.

The axis-orientation study offers much less down-facing area on edge but raises build height to about 245 mm and puts broad panels on narrow edges. That changes the requested horizontal stack, reduces bed anchoring and risks panel accuracy; retain the horizontal layout. Support angle findings are addressed with generated supports, not by calling those overhangs self-supporting.

## Online techniques and limits

- [Prusa support guide](https://help.prusa3d.com/article/support-material_1698): denser interfaces support surfaces while sparse backing limits material; supports need permission to start on earlier parts in a vertical stack. Normal supports were chosen for stable stacked structures.
- [Bambu Studio configuration source](https://github.com/bambulab/BambuStudio/blob/master/src/libslic3r/PrintConfig.cpp): explicit support/interface filament assignments and flushing matrix. Here PETG is only the release interface; PLA forms the support scaffold. All model parts remain PLA. Purging into objects, infill or support is disabled, with 800 mm³ flush each direction and a prime tower. This is a conservative starting value requiring filament-specific confirmation, not a manufacturer-guaranteed setting.
- [Bambu Studio issue #11540](https://github.com/bambulab/BambuStudio/issues/11540): installed 2.7.1.62 has a reported zero-gap interface/bridge classification issue for the inverse material pairing. This slice also uses Bridge features on supported first layers. Dimensional surface quality therefore still needs the supplied separation trial; software success alone does not clear it. No automatic application update was installed.
- The final independent file inspection receipt for A1 / 0.4 mm / textured PEI / PLA + PETG is in `file-inspection.json`. Tuned print temperatures are PLA 220 °C / PETG 245 °C, with a 245 °C material-change flush; the maximum nozzle command in the inspected file is 245 °C. Bed temperature is 65 °C. The receipt does not establish physical printer readiness or authorize dispatch.
- PLA/PETG contact is deliberately weak. Dense PETG with zero nominal top/bottom contact gap is a trial choice for release and lower-face finish. PETG dryness, the actual spool profiles and purge sufficiency determine success. Use gentle top-down removal and keep each thin model supported while peeling. Do not assume PETG is water soluble.
'''
    (review/'REVIEW.md').write_text(report,encoding='utf-8')
    print(f'Review: {len(failed)} below-guide bodies, {len(uncertain)} sampling cautions; layout material reduction {reduction:.1f}%')

if __name__=='__main__':main()
