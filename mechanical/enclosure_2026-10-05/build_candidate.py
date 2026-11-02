"""Regenerate the PHBox Choc V1 fit candidate; all dimensions are millimetres.

Run with the bundled Python. CAD libraries are project-local in stage2_work.
The source PCB is read only. Profiles are nominal geometry, not machine toolpaths.
"""
from pathlib import Path
import sys, json, hashlib, math, zipfile
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'stage2_work/enclosure_cad_dependencies'))
sys.path.insert(0, str(ROOT/'kicad-happy-main/skills/kicad/scripts'))
import cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
from sexp_parser import parse_file

def child(n, key):
    return next((a for a in n if isinstance(a, list) and a[0] == key), None)

def main():
    pcb = ROOT/'Flatbox-rev8.kicad_pcb'
    data = parse_file(str(pcb))
    fps = {}
    edges = []
    for n in data:
        if not isinstance(n, list): continue
        if n[0].startswith('gr_') and child(n,'layer') == ['layer','Edge.Cuts']:
            edges.append(n)
        if n[0] == 'footprint':
            ref = next(a[2] for a in n if isinstance(a,list) and a[:2] == ['property','Reference'])
            at = child(n,'at')
            fps[ref] = {'x':float(at[1]),'y':float(at[2]), 'angle':float(at[3]) if len(at)>3 else 0,
                        'footprint': n[1], 'node':n}
    points = [child(e,k)[1:3] for e in edges for k in ('start','end')]
    xmin = min(float(p[0]) for p in points); xmax = max(float(p[0]) for p in points)
    ymin = min(float(p[1]) for p in points); ymax = max(float(p[1]) for p in points)
    width = xmax-xmin; height = ymax-ymin
    # CAD origin is PCB lower-left tangent-box corner. +Y points towards USB.
    def xy(f): return (f['x']-xmin, ymax-f['y'])
    switch = []
    for i in range(1,17):
        ref = f'SW{i}'; f=fps[ref]
        assert f['angle']==0
        central = [n for n in f['node'] if isinstance(n,list) and n[0]=='pad'
                   and 'np_thru_hole' in n and child(n,'at')[1:3]==['0','0']]
        assert len(central)==1 and float(child(central[0],'drill')[1])==5.05
        switch.append({'ref':ref,'cad_xy':xy(f),'pcb_xy':[f['x'],f['y']]})
    service_edge = 80.0
    plate_height = ymax-service_edge
    thickness = 1.3  # fit candidate; verify the actual switch latch with coupons
    aperture = 14.0 # candidate clearance around the manufacturer's 13.8 mm body
    # No case fasteners pass through the floating island. Existing PCB holes are
    # clearance/alignment references for optional fasteners entirely within it.
    holes = []
    for ref in ['H1','H2','H3','H7','H8','H9']:
        f=fps[ref]
        p=next(n for n in f['node'] if isinstance(n,list) and n[0]=='pad')
        holes.append({'ref':ref,'cad_xy':xy(f),'diameter':float(child(p,'drill')[1])})
    tabs = [(-4,35,8,20),(-4,95,8,20),(width+4,35,8,20),(width+4,95,8,20),
            (80,-4,20,8),(200,-4,20,8),(20,plate_height+4,20,8),(width-20,plate_height+4,20,8)]
    def box(x,y,w,h,t):
        return cq.Workplane('XY').center(x,y).rect(w,h).extrude(t)
    plate = box(width/2,plate_height/2,width,plate_height,thickness)
    # Preserve PCB R5 bottom corners while leaving the service boundary straight.
    for x,cx in [(0,5),(width-5,width-5)]:
        corner=box(x+2.5,2.5,5,5,thickness)
        circle=cq.Workplane('XY').center(cx,5).circle(5).extrude(thickness)
        plate=plate.cut(corner.cut(circle))
    for x,y,w,h in tabs: plate=plate.union(box(x,y,w,h,thickness))
    for s in switch:
        x,y=s['cad_xy']; plate=plate.cut(box(x,y,aperture,aperture,thickness))
    for h in holes:
        x,y=h['cad_xy']; plate=plate.cut(cq.Workplane('XY').center(x,y).circle(h['diameter']/2).extrude(thickness))
    plate=plate.clean()
    assert plate.val().isValid() and len(plate.solids().vals())==1
    out=HERE/'candidate'; out.mkdir(exist_ok=True)
    cq.exporters.export(plate,str(out/'choc-v1-retention-1p3mm.step'))
    cq.exporters.export(plate,str(out/'choc-v1-retention-1p3mm.stl'),tolerance=0.03,angularTolerance=0.1)
    cq.exporters.export(plate.section(height=thickness/2),str(out/'choc-v1-retention-nominal.dxf'))
    coupon_sizes=[13.9,14.0,14.1,14.2]
    for t in [1.2,1.3]:
        coupon=box(48,13,96,26,t)
        for i,a in enumerate(coupon_sizes): coupon=coupon.cut(box(12+24*i,13,a,a,t))
        assert coupon.val().isValid()
        name=f'choc-v1-fit-coupon-{str(t).replace(".","p")}mm'
        cq.exporters.export(coupon,str(out/(name+'.stl')),tolerance=0.03)
        cq.exporters.export(coupon,str(out/(name+'.step')))
        if t==1.3: cq.exporters.export(coupon.section(height=t/2),str(out/'choc-v1-fit-coupon-nominal.dxf'))
    # Source audit and explicit prototype assumptions travel with the exports.
    geom={'source_pcb':pcb.name,'source_sha256':hashlib.sha256(pcb.read_bytes()).hexdigest(),
          'units':'mm','cad_origin_pcb_xy':[xmin,ymax], 'cad_axes':'+X right, +Y toward USB; exports Z=0 at plate underside',
          'pcb_outline_mm':{'width':width,'height':height,'corner_radius':5},
          'switches':switch,'alignment_clearances':holes,'gasket_tabs':tabs,
          'candidate':{'thickness':thickness,'square_aperture':aperture,'service_edge_pcb_y':service_edge,
                       'plate_top_above_pcb_front_initial_mm':2.2,'z_fit_requires_physical_verification':True,
                       'gasket_initial_uncompressed_mm':1.5,'gasket_initial_compression_fraction':0.2,
                       'foam_trial_mm':[1,2],'travel_budget_each_direction_mm':0.5},
          'fit_coupon':{'sizes_left_to_right':coupon_sizes,'thicknesses':[1.2,1.3]}}
    (HERE/'candidate-parameters.json').write_text(json.dumps(geom,indent=2)+'\n')
    # Numerical clearance checks supplement solid validity. They do not prove stiffness.
    min_switch_gap = min(max(abs(a['cad_xy'][0]-b['cad_xy'][0])-aperture,
                             abs(a['cad_xy'][1]-b['cad_xy'][1])-aperture)
                         for i,a in enumerate(switch) for b in switch[i+1:])
    min_switch_edge=min(min(x-aperture/2,width-x-aperture/2,y-aperture/2,plate_height-y-aperture/2)
                        for x,y in [s['cad_xy'] for s in switch])
    min_hole_edge=min(min(x-d/2,width-x-d/2,y-d/2,plate_height-y-d/2)
                     for x,y,d in [(h['cad_xy'][0],h['cad_xy'][1],h['diameter']) for h in holes])
    min_hole_switch=min(math.hypot(max(abs(h['cad_xy'][0]-s['cad_xy'][0])-aperture/2,0),
                                  max(abs(h['cad_xy'][1]-s['cad_xy'][1])-aperture/2,0))-h['diameter']/2
                        for h in holes for s in switch)
    assert min(min_switch_gap,min_switch_edge,min_hole_edge,min_hole_switch)>0
    # Read back STEP and DXF rather than relying only on a successful write.
    recovered=cq.importers.importStep(str(out/'choc-v1-retention-1p3mm.step'))
    assert recovered.val().isValid() and len(recovered.solids().vals())==1
    assert abs(recovered.val().Volume()-plate.val().Volume())<0.001
    import ezdxf
    dxf=ezdxf.readfile(out/'choc-v1-retention-nominal.dxf')
    assert not dxf.audit().has_errors
    audit={'status':'GEOMETRY PASS / FIT CANDIDATE ONLY','switch_count':len(switch),'gasket_tab_count':len(tabs),
           'alignment_hole_count':len(holes),'solid_valid':True,'step_roundtrip_valid':True,'dxf_audit_errors':0,
           'min_switch_separation_axis_web_mm':min_switch_gap,'min_switch_to_body_edge_mm':min_switch_edge,
           'min_alignment_hole_to_body_edge_mm':min_hole_edge,'min_alignment_hole_to_switch_mm':min_hole_switch,
           'envelope_mm':[width+16,plate_height+16,thickness],
           'not_verified':['physical switch latch fit','PLA/acrylic stiffness and impact strength','assembled component-height collisions',
                           'final top/bottom enclosure geometry','thermal spreader contact and cooling performance','gasket load/deflection']}
    (HERE/'candidate-validation.json').write_text(json.dumps(audit,indent=2)+'\n')
    fig,ax=plt.subplots(figsize=(14,9))
    ax.add_patch(FancyBboxPatch((0,0),width,height,boxstyle='round,pad=0,rounding_size=5',facecolor='#e3eee7',edgecolor='#648573'))
    ax.add_patch(Rectangle((0,0),width,plate_height,facecolor='#c1daf0',edgecolor='#376f9a',alpha=.88))
    for x,y,w,h in tabs: ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,facecolor='#d8b176',edgecolor='#986727'))
    for s in switch:
        x,y=s['cad_xy']; ax.add_patch(Rectangle((x-7,y-7),14,14,facecolor='white',edgecolor='#254968'))
        ax.plot(x,y,'+',color='#cc4d42',markersize=6); ax.text(x,y-10,s['ref'],ha='center',fontsize=8)
    for h in holes:
        x,y=h['cad_xy']; ax.add_patch(Circle((x,y),h['diameter']/2,facecolor='white',edgecolor='#254968'))
        ax.text(x+4,y,h['ref'],fontsize=7)
    for ref,w,h in [('U5',35.4,33.5),('U1',7,7),('USB1',10,8),('USB2',15,15)]:
        x,y=xy(fps[ref]); ax.add_patch(Rectangle((x-w/2,y-h/2),w,h,fill=False,edgecolor='#555',linestyle='--'))
        ax.text(x,y,ref,ha='center',va='center',fontsize=8)
    ax.text(150,145,'Open electronics zone\nReserved for separate floating thermal spreader\nand screen support carrier',ha='center',fontsize=10)
    ax.set_aspect('equal'); ax.set_xlim(-13,width+13); ax.set_ylim(-13,height+7)
    ax.set_xlabel('CAD X (mm)'); ax.set_ylabel('CAD Y (mm; towards USB)')
    ax.set_title('PHBox — Kailh Choc V1 retention plate candidate\n16 × 14 mm apertures · 1.3 mm trial plate · 8 gasket tabs')
    fig.tight_layout(); fig.savefig(HERE/'candidate-preview.png',dpi=160); plt.close(fig)
    # SVG is a dimensionally correct cut profile; labels are deliberately separate.
    from xml.sax.saxutils import escape
    section=plate.section(height=thickness/2)
    cq.exporters.export(section,str(out/'choc-v1-retention-preview.svg'))
    print(json.dumps(audit,indent=2))

if __name__=='__main__': main()
