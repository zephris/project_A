"""Build nominal mechanical references and a separately labelled tolerance model."""
from pathlib import Path
import sys,json,csv,math,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent; OUT=HERE/'pcb_geometry'
sys.path.insert(0,str(ROOT/'stage2_work/enclosure_cad_dependencies'))
sys.path.insert(0,str(ROOT/'kicad-happy-main/skills/kicad/scripts'))
import cadquery as cq
import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
from matplotlib.transforms import Affine2D
from sexp_parser import parse_file

def child(n,k): return next((a for a in n if isinstance(a,list) and a[0]==k),None)
def main():
    raw=json.loads((OUT/'native-geometry.json').read_text())
    pcb=ROOT/raw['source']; assert hashlib.sha256(pcb.read_bytes()).hexdigest()==raw['source_sha256']
    edges=[n for n in parse_file(str(pcb)) if isinstance(n,list) and n[0].startswith('gr_') and child(n,'layer')==['layer','Edge.Cuts']]
    assert len(edges)==8 and sum(e[0]=='gr_arc' for e in edges)==4
    coords=[child(e,k)[1:3] for e in edges for k in ('start','end')]
    x0=min(float(p[0]) for p in coords); x1=max(float(p[0]) for p in coords)
    y0=min(float(p[1]) for p in coords); y1=max(float(p[1]) for p in coords)
    W=x1-x0; H=y1-y0; R=5.0; T=raw['thickness_mm']
    def xy(p): return [round(p[0]-x0,6),round(y1-p[1],6)]
    fps={f['ref']:dict(f,cad_xy=xy(f['pcb_xy'])) for f in raw['footprints']}
    holes=[dict(h,cad_xy=xy(h['pcb_xy'])) for h in raw['holes']]
    assert W==272.6 and H==171 and T==1.6
    # Verify the R5 assertion against every source arc using its circumcircle.
    for e in edges:
        if e[0]!='gr_arc': continue
        p=[list(map(float,child(e,k)[1:3])) for k in ('start','mid','end')]
        a=math.dist(p[0],p[1]); b=math.dist(p[1],p[2]); c=math.dist(p[2],p[0])
        area=abs((p[1][0]-p[0][0])*(p[2][1]-p[0][1])-(p[1][1]-p[0][1])*(p[2][0]-p[0][0]))/2
        assert abs(a*b*c/(4*area)-R)<0.00001
    mounting=sorted([h for h in holes if h['ref'].startswith('H')],key=lambda h:int(h['ref'][1:]))
    display=[h for h in holes if h['ref']=='U5' and h['plating']=='NPTH']
    switches=[fps[f'SW{i}'] for i in range(1,17)]
    for s in switches:
        assert s['rotation_deg']==0
        peg=next(h for h in holes if h['ref']==s['ref'] and h['drill_xy_mm']==[5.05,5.05])
        assert peg['cad_xy']==s['cad_xy']
    def tol(h):
        d=max(h['drill_xy_mm'])
        if h['plating']=='PTH': return (-0.08,0.13,'Published through-hole/plated-slot size range')
        if d>=6.3: return (-0.2,0.2,'PLANNING ASSUMPTION: routed circular NPTH; confirm diameter and position with JLCPCB')
        return (-0.2,0.2,'PLANNING ASSUMPTION: round NPTH not separately specified on current page; confirm with JLCPCB')
    for h in holes:
        lo,hi,status=tol(h)
        h.update(size_allowance_minus_mm=lo,size_allowance_plus_mm=hi,tolerance_status=status,
                 position_allowance_mm=0.075 if max(h['drill_xy_mm'])<6.3 else None)
    with (OUT/'all-holes.csv').open('w',newline='') as f:
        wr=csv.writer(f); wr.writerow(['ID','Reference','Pad','X_mm','Y_mm','Drill_X_mm','Drill_Y_mm','Angle_deg','Plating','Shape','Size_minus_mm','Size_plus_mm','Position_mm','Tolerance_status'])
        for h in holes: wr.writerow([h['id'],h['ref'],h['pad'],*h['cad_xy'],*h['drill_xy_mm'],h['rotation_deg'],h['plating'],h['kind'],h['size_allowance_minus_mm'],h['size_allowance_plus_mm'],h['position_allowance_mm'],h['tolerance_status']])
    with (OUT/'mounting-and-screen-holes.csv').open('w',newline='') as f:
        wr=csv.writer(f); wr.writerow(['Reference','X_mm','Y_mm','Nominal_diameter_mm','Planning_min_mm','Planning_max_mm','Method','Tolerance_status'])
        for h in mounting+display:
            d=h['drill_xy_mm'][0]; wr.writerow([h['ref'],*h['cad_xy'],d,round(d+h['size_allowance_minus_mm'],3),round(d+h['size_allowance_plus_mm'],3),'CNC routed' if d>=6.3 else 'drilled',h['tolerance_status']])
    with (OUT/'switch-centres-oem-choc-v1.csv').open('w',newline='') as f:
        wr=csv.writer(f); wr.writerow(['Ref','X_mm','Y_mm','Rotation_deg','Housing_envelope_X_mm','Housing_envelope_Y_mm','Rest_height_above_PCB_mm','Travel_mm'])
        for s in switches: wr.writerow([s['ref'],*s['cad_xy'],s['rotation_deg'],15,15,8,3])
    doc=ezdxf.new('R2010'); ms=doc.modelspace(); doc.units=4
    for name,col in [('OUTLINE',7),('MOUNT_NPTH',1),('SCREEN_NPTH',6),('OTHER_NPTH',3),('PTH',8),('SWITCH_OEM_ENVELOPE',5),('REF_CENTRES',2),('REF_TEXT',2),('PLANNING_EDGE_ENVELOPE',30)]: doc.layers.new(name,dxfattribs={'color':col})
    b=math.tan(math.pi/8)
    def outline(w,h,r,offset=0,layer='OUTLINE'):
        pts=[(r,0,0),(w-r,0,b),(w,r,0),(w,h-r,b),(w-r,h,0),(r,h,b),(0,h-r,0),(0,r,b)]
        ms.add_lwpolyline([(x-offset,y-offset,bulge) for x,y,bulge in pts],format='xyb',close=True,dxfattribs={'layer':layer})
    outline(W,H,R)
    # This is an independent +/-0.2 mm edge planning buffer, not an extra factory dimension guarantee.
    outline(W+.4,H+.4,R+.2,.2,'PLANNING_EDGE_ENVELOPE')
    for h in holes:
        x,y=h['cad_xy']; dx,dy=h['drill_xy_mm']
        layer='MOUNT_NPTH' if h['ref'].startswith('H') else 'SCREEN_NPTH' if h['ref']=='U5' else 'OTHER_NPTH' if h['plating']=='NPTH' else 'PTH'
        if h['kind']=='round': ms.add_circle((x,y),dx/2,dxfattribs={'layer':layer})
        else:
            # Capsule with bulged semicircular ends; native pad angle is absolute.
            L=max(dx,dy); r=min(dx,dy)/2; c=(L-2*r)/2
            angle=math.radians(h['rotation_deg']+(90 if dy>dx else 0))
            points=[(-c,-r,0),(c,-r,1),(c,r,0),(-c,r,1)]
            pts=[(x+px*math.cos(angle)-py*math.sin(angle),y+px*math.sin(angle)+py*math.cos(angle),bb) for px,py,bb in points]
            ms.add_lwpolyline(pts,format='xyb',close=True,dxfattribs={'layer':layer})
    for s in switches:
        x,y=s['cad_xy']; ms.add_lwpolyline([(x-7.5,y-7.5),(x+7.5,y-7.5),(x+7.5,y+7.5),(x-7.5,y+7.5)],close=True,dxfattribs={'layer':'SWITCH_OEM_ENVELOPE'})
        ms.add_point((x,y),dxfattribs={'layer':'REF_CENTRES'})
        ms.add_text(s['ref'],dxfattribs={'height':1.5,'insert':(x+8,y),'layer':'REF_TEXT'})
    doc.saveas(OUT/'pcb-geometry-nominal-reference.dxf')
    # Separate outline-only file is safe to use as a nominal CAD import.
    outline_doc=ezdxf.new('R2010'); outline_doc.units=4
    for e in ms.query('LWPOLYLINE[layer=="OUTLINE"]'): outline_doc.modelspace().add_foreign_entity(e.copy())
    outline_doc.saveas(OUT/'pcb-outline-only.dxf')
    bare=cq.Workplane('XY').center(W/2,H/2).rect(W,H).extrude(-T).edges('|Z').fillet(R)
    from collections import defaultdict,Counter
    groups=defaultdict(list)
    for h in holes:
        if h['kind']=='round': groups[h['drill_xy_mm'][0]].append(tuple(h['cad_xy']))
    for diameter,points in groups.items():
        cutters=cq.Workplane('XY').pushPoints(points).circle(diameter/2).extrude(-T)
        bare=bare.cut(cutters)
    for h in holes:
        if h['kind']!='slot': continue
        x,y=h['cad_xy']; dx,dy=h['drill_xy_mm']; a=h['rotation_deg']+(90 if dy>dx else 0)
        bare=bare.cut(cq.Workplane('XY').center(x,y).slot2D(max(dx,dy),min(dx,dy),a).extrude(-T))
    assert bare.val().isValid() and len(bare.solids().vals())==1
    cq.exporters.export(bare,str(OUT/'pcb-bare-nominal-all-holes.step'))
    # OEM envelope is deliberately conservative and labelled; not a detailed switch model.
    sw_assembly=cq.Assembly(name='OEM_Choc_V1_conservative_rest_envelopes')
    for s in switches:
        x,y=s['cad_xy']; envelope=cq.Workplane('XY').center(x,y).rect(15,15).extrude(8)
        sw_assembly.add(envelope,name=s['ref'],color=cq.Color(0.2,0.4,0.8,0.4))
    sw_assembly.save(str(OUT/'oem-choc-v1-rest-envelopes.step'))
    mapped={'source_sha256':raw['source_sha256'],'kicad_version':raw['kicad_version'],
            'datum':{'pcb_xy_origin':[x0,y1],'x':'right','y':'toward USB','z':'PCB front=0; board occupies -1.6..0 nominal'},
            'outline':{'width_mm':W,'height_mm':H,'corner_radius_mm':R,'thickness_mm':T,'source_edge_cuts':edges},
            'published_tolerances_checked_2026_10_05':{'regular_routed_dimension_mm':0.2,'precision_routed_dimension_mm':0.1,'board_thickness_fraction':0.1,'hole_position_mm':0.075,'pth_size_mm':[-.08,.13],'nonplated_slot_size_mm':0.2},
            'planning_assumptions':{'independent_edge_allowance_mm':0.2,'round_npth_size_mm':[-.2,.2],'routed_circular_hole_position':'not established; do not inherit drilled-hole position guarantee'},
            'oem_switch':{'source':'https://www.kailhswitch.com/Content/upload/pdf/202215927/CPG135001D01-16.pdf','base_width_mm':13.8,'max_plan_width_mm':15,'housing_height_mm':5,'stem_projection_mm':3,'rest_height_mm':8,'travel_mm':3,'envelope_type':'conservative 15x15x8 bounding volume, no keycap'},
            'mounting_holes':mounting,'display_holes':display,'switches':switches,'footprints':list(fps.values()),'holes':holes}
    (OUT/'geometry-and-tolerances.json').write_text(json.dumps(mapped,indent=2)+'\n')
    fig=plt.figure(figsize=(17,10)); ax=fig.add_axes([.04,.13,.68,.77]); tab=fig.add_axes([.75,.13,.24,.77]); tab.axis('off')
    ax.add_patch(FancyBboxPatch((-.2,-.2),W+.4,H+.4,boxstyle='round,pad=0,rounding_size=5.2',facecolor='#f3d2bd',edgecolor='#bd7447',linewidth=3))
    ax.add_patch(FancyBboxPatch((0,0),W,H,boxstyle='round,pad=0,rounding_size=5',facecolor='#eef3ef',edgecolor='#365d49',linewidth=1.2))
    for h in holes:
        x,y=h['cad_xy']; dx,dy=h['drill_xy_mm']
        if h['kind']=='round': ax.add_patch(Circle((x,y),dx/2,fill=False,edgecolor='#a2aaa5',linewidth=.45))
        else:
            L=max(dx,dy); r=min(dx,dy)/2; a=h['rotation_deg']+(90 if dy>dx else 0)
            ax.add_patch(FancyBboxPatch((x-L/2,y-r),L,2*r,boxstyle=f'round,pad=0,rounding_size={r}',fill=False,edgecolor='#8c9890',linewidth=.5,transform=Affine2D().rotate_deg_around(x,y,a)+ax.transData))
    for s in switches:
        x,y=s['cad_xy']; ax.add_patch(Rectangle((x-7.5,y-7.5),15,15,fill=False,edgecolor='#497faa',linestyle='--',linewidth=.9))
        ax.plot(x,y,'+',color='#497faa',markersize=5); ax.text(x,y-10,s['ref'],ha='center',fontsize=8)
    for h in mounting+display:
        x,y=h['cad_xy']; d=h['drill_xy_mm'][0]; color='#aa3f37' if h in mounting else '#804394'
        ax.add_patch(Circle((x,y),d/2,facecolor='white',edgecolor=color,linewidth=1.4))
        ax.text(x+4,y+1,h['ref'] if h in mounting else 'OLED',fontsize=7,color=color)
    for ref in ['U1','U5','USB1','USB2','SW19','SW20']:
        x,y=fps[ref]['cad_xy']; ax.plot(x,y,'x',color='#302c30',markersize=6)
        if ref not in ['SW19','SW20']: ax.text(x+3,y-5 if ref=='USB1' else y+3,ref,fontsize=8)
    ax.annotate('',(0,-7),(W,-7),arrowprops={'arrowstyle':'<->','color':'#333'})
    ax.text(W/2,-12,'272.600 mm nominal | regular routing dimension +/-0.200 mm',ha='center',fontsize=9)
    ax.annotate('',(-7,0),(-7,H),arrowprops={'arrowstyle':'<->','color':'#333'})
    ax.text(-13,H/2,'171.000 mm nominal',rotation=90,ha='center',va='center',fontsize=9)
    ax.plot(0,0,'o',color='black',markersize=4); ax.text(2,3,'Origin (0,0)',fontsize=8)
    ax.text(7,H-6,'R5 - four corners',fontsize=8)
    ax.set_aspect('equal'); ax.set_xlim(-18,W+8); ax.set_ylim(-18,H+8)
    ax.set_xlabel('X (mm)'); ax.set_ylabel('Y (mm; towards USB)')
    rows=[[h['ref'],f"{h['cad_xy'][0]:.3f}",f"{h['cad_xy'][1]:.3f}",f"{h['drill_xy_mm'][0]:.2f}"] for h in mounting]
    for i,h in enumerate(sorted(display,key=lambda h:(-h['cad_xy'][1],h['cad_xy'][0]))): rows.append([f'OLED {i+1}',f"{h['cad_xy'][0]:.3f}",f"{h['cad_xy'][1]:.3f}",'3.00'])
    table=tab.table(cellText=rows,colLabels=['Hole','X','Y','Dia.'],loc='upper center',cellLoc='center',bbox=[0,.42,1,.58]); table.auto_set_font_size(False); table.set_fontsize(9)
    for (r,c),cell in table.get_celld().items():
        cell.set_edgecolor('#c1c8ce'); cell.set_facecolor('#d9e6ed' if r==0 else '#f5f8fa' if r%2 else 'white')
    tab.text(0,.38,'FABRICATION / FIT NOTES',fontsize=11,weight='bold')
    tab.text(0,.35,'PCB thickness: 1.60 mm nominal\nPublished range: 1.44-1.76 mm\n\nH1-H7: 6.4 mm CNC routed\nPlanning diameter: 6.2-6.6 mm*\nH8-H12: 2.2 mm drilled NPTH\nPlanning diameter: 2.0-2.4 mm*\nOLED holes: 3.0 mm drilled NPTH\nPlanning diameter: 2.8-3.2 mm*\n\nDrilled-hole position: +/-0.075 mm\nRouted-hole position: confirm\n\n*NPTH size ranges are assumptions,\nnot independently published guarantees.',fontsize=9,va='top',linespacing=1.4)
    fig.suptitle('PHBox PCB mechanical geometry - active KiCad 10 design',fontsize=18,weight='bold')
    fig.text(.045,.045,'Blue dashed boxes: OEM Kailh Choc V1 15 x 15 mm plan envelopes, without keycaps.\nOrange boundary: independent 0.2 mm edge planning buffer. Drawing is an enclosure reference, not a fabrication release.',fontsize=10)
    fig.savefig(OUT/'pcb-geometry-map.png',dpi=170); fig.savefig(OUT/'pcb-geometry-map.svg'); plt.close(fig)
    check=ezdxf.readfile(OUT/'pcb-geometry-nominal-reference.dxf'); assert not check.audit().has_errors
    assert len(check.modelspace().query('CIRCLE'))==sum(h['kind']=='round' for h in holes)
    from collections import Counter
    result={'status':'nominal geometry verified; supplier-specific fit tolerances partly unconfirmed','source_hash_unchanged':True,'outline_mm':[W,H,R,T],
            'holes':len(holes),'hole_counts':{f'{p}_{k}':v for (p,k),v in Counter((h['plating'],h['kind']) for h in holes).items()},
            'mounting_holes':len(mounting),'screen_holes':len(display),'switches':len(switches),'bare_step_solid_valid':True,'dxf_audit_errors':0}
    (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))

if __name__=='__main__': main()
