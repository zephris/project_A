"""Separate Z-height sheet: known geometry, candidate heights, unresolved stack."""
from pathlib import Path
import sys,json,hashlib,csv
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent; OUT=HERE/'z_geometry'
OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'stage2_work/enclosure_cad_dependencies'))
sys.path.insert(0,str(ROOT/'kicad-happy-main/skills/kicad/scripts'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from sexp_parser import parse_file

def child(n,k): return next((a for a in n if isinstance(a,list) and a[0]==k),None)
def main():
    pcb=ROOT/'Flatbox-rev8.kicad_pcb'; data=parse_file(str(pcb))
    stack=child(child(data,'setup'),'stackup')
    total=sum(float(child(n,'thickness')[1]) for n in stack if isinstance(n,list) and n[0]=='layer' and child(n,'thickness'))
    entries=[
        ['PCB',-1.6,0,'Nominal 1.6 mm; finished thickness 1.44-1.76 mm'],
        ['Choc V1 resting envelope',0,8,'OEM housing 5 mm plus 3 mm stem; excludes keycap and underside pins'],
        ['Choc V1 stem at full stroke',5,5,'Nominal 3 mm travel from 8 mm resting top'],
        ['Retention plate candidate',.9,2.2,'1.3 mm trial plate; installed top height needs physical latch fit'],
        ['OLED module envelope',2,5.7,'3 mm standoffs plus CAD -1..+2.7 mm body; long pins excluded'],
        ['MCU QFN-60 nominal package',0,.85,'Package A=0.80..0.90 mm; assembled height adds solder stand-off s'],
        ['USB-A SMD main body',-9.4,-3.7,'OEM shell height 5.7 mm; elevated 2.1 mm above underside seating plane'],
        ['Compact dongle trial envelope',-10.55,-2.55,'15 x 15 x 8 mm; connector/body centre alignment assumed, verify fit'],
    ]
    meta={'source_pcb_sha256':hashlib.sha256(pcb.read_bytes()).hexdigest(),'datum':'PCB front seating plane Z=0; positive towards switches; negative towards underside',
          'nominal_board_thickness_mm':1.6,'published_finished_board_thickness_mm':[1.44,1.76],
          'declared_stack_sum_including_masks_mm':round(total,6),'stack_sum_note':'KiCad layer values do not sum to general thickness; final JLC stack must be confirmed',
          'features':entries,'unknowns':['keycap geometry','solder stand-off','assembled heights of remaining ICs and connectors','final outer plate thicknesses',
                                      'thermal spreader profiles and thicknesses','lower carrier and foam clearances','actual gasket deflection','final enclosure height'],
          'thermal_pad_example':{'uncompressed_mm':.5,'illustrative_compression_fraction':.2,'installed_gap_mm':.4,
                                 'boss_contact_face_formula':'Z = solder stand-off s + MCU package height A + installed thermal pad gap',
                                 'nominal_example_mm':'1.25 + s','not_final_design':True}}
    (OUT/'z-height-reference.json').write_text(json.dumps(meta,indent=2)+'\n')
    with (OUT/'z-height-reference.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['Feature','Nominal_Z_min_mm','Nominal_Z_max_mm','Basis_and_limit']);w.writerows(entries)
    fig=plt.figure(figsize=(16,10)); ax=fig.add_axes([.07,.2,.57,.66]); note=fig.add_axes([.68,.17,.30,.69]);note.axis('off')
    ax.axhspan(-1.6,0,color='#acc6b0',alpha=.5);ax.axhline(0,color='#2b5135',linewidth=2)
    ax.axhspan(-1.76,-1.44,color='#729f81',alpha=.4)
    ax.text(.05,-.75,'PCB',ha='left',fontsize=10,weight='bold'); ax.text(.05,.16,'PCB FRONT Z = 0',fontsize=10,weight='bold',color='#2b5135')
    for x,lo,hi,col in [(1,0,5,'#90b5d1'),(2,.9,2.2,'#d4b073'),(3,2,5.7,'#a197c2'),(4,0,.85,'#898e93'),(5,-9.4,-3.7,'#d78e84')]:
        ax.add_patch(Rectangle((x-.28,lo),.56,hi-lo,facecolor=col,edgecolor='#39454d',alpha=.95))
        if x!=1: ax.text(x+.32,hi,f'{hi:+.2f}',fontsize=9,va='center')
        if lo: ax.text(x+.32,lo,f'{lo:+.2f}',fontsize=9,va='center')
    ax.add_patch(Rectangle((.86,5),.28,3,facecolor='#5886b2',edgecolor='#39454d'))
    ax.plot([.65,1.35],[8,8],color='#284e73');ax.text(1.4,8,'+8.00 rest',fontsize=10,va='center')
    ax.plot([.65,1.35],[5,5],color='#284e73',linestyle='--');ax.text(1.4,5,'+5.00 pressed',fontsize=9,va='center')
    ax.add_patch(Rectangle((4.72,-10.55),.56,8,fill=False,linestyle='--',edgecolor='#a53329'))
    ax.text(5.1,-12,'8 mm dongle trial\nflush datum -10.55',ha='center',fontsize=9,color='#a53329')
    ax.annotate('Package top\n+0.85 + solder s',xy=(4,.85),xytext=(4,2.9),ha='center',fontsize=9,arrowprops={'arrowstyle':'->'})
    ax.set_xlim(-.05,5.75);ax.set_ylim(-14.5,9.2);ax.set_ylabel('Z (mm) relative to PCB front');ax.set_yticks(range(-14,10,2))
    ax.set_xticks([1,2,3,4,5],['Choc V1','Retention\nplate trial','OLED U5','MCU U1','USB-A USB2'])
    ax.grid(axis='y',color='#e0e5e8');ax.set_axisbelow(True)
    note.text(0,1,'HEIGHT / STACK NOTES',fontsize=13,weight='bold',va='top')
    note.text(0,.95,'Separate feature sections, not one physical cut.\nSwitch keycaps are not included.\n\nMCU QFN-60 package height A:\n0.80 / 0.85 / 0.90 mm min/nom/max.\nAdd actual solder stand-off s.\n\nThermal-pad contact-face formula:\nZ = s + A + compressed pad thickness.\n0.5 mm pad at 20% compression gives\n0.40 mm gap; example Z = 1.25 + s.\nThis is provisional, not a clamping design.\n\nPCB general thickness: 1.600 mm.\nDeclared layer sum incl. masks: '+f'{total:.6f}'+' mm.\nConfirm the final JLCPCB stack.\n\nUSB-A SMD main body: 5.7 mm high.\nUnderside shell Z=-9.4..-3.7 mm.\nNo recessed body cutout required.\n8 mm dongle Z=-10.55..-2.55 mm\nassumes centred body/plug geometry.\nFlush case height remains provisional.',fontsize=10,va='top',linespacing=1.5)
    fig.suptitle('PHBox - separate Z geometry reference sheet',fontsize=19,weight='bold')
    fig.text(.07,.09,'Bottom-to-top enclosure order: bottom outer plate > lower gasket > bottom spreader > PCB >\nupper spreader interwoven with retention plate > upper gasket > top outer plate.\nOuter plates, spreaders, carrier and foam do not yet have released Z dimensions.',fontsize=11,linespacing=1.5)
    fig.savefig(OUT/'pcb-z-geometry.png',dpi=170);fig.savefig(OUT/'pcb-z-geometry.svg');plt.close(fig)
    # A separate local page opens directly in a browser and also prints cleanly.
    (OUT/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><title>PHBox Z geometry</title>
<style>body{font:16px system-ui;background:#f5f7f8;color:#263540;margin:24px auto;max-width:1500px;padding:0 20px}img{width:100%;background:white;border:1px solid #ccd6de}a{color:#245b88}@media print{body{margin:0;padding:0;background:white}}</style>
<h1>PHBox: Z geometry reference</h1><p>PCB front is Z=0. Feature sections are shown separately. This sheet records known heights and candidate assumptions; the full enclosure stack remains provisional.</p>
<img src="pcb-z-geometry.svg" alt="PCB Z height diagram"><p><a href="README.md">Dimensions, sources and limits</a> · <a href="z-height-reference.csv">Height table</a></p>
</html>''',encoding='utf-8')
    print('Z sheet written; declared stack sum:',total)
if __name__=='__main__':main()
