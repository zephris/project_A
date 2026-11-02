"""Prepare one existing mock part per A1 print file without changing geometry.

Writes standard, named-object 3MFs; Bambu Studio CLI adds its native presets
and slices them. Never contacts a printer. Uses only Python standard library.
"""
from pathlib import Path
import json, struct, zipfile, hashlib, math, subprocess
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
KIT=HERE.parent
PROFILES=Path('D:/Bambu Studio/resources/profiles/BBL')
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',NS)
def tag(t): return '{'+NS+'}'+t

def read_mesh(path):
    raw=path.read_bytes(); n=struct.unpack_from('<I',raw,80)[0]
    assert len(raw)==84+50*n
    vertices=[]; triangles=[]; index={}
    for i in range(n):
        vals=struct.unpack_from('<12fH',raw,84+50*i)
        ids=[]
        for k in (3,6,9):
            v=tuple(vals[k:k+3])
            if v not in index: index[v]=len(vertices);vertices.append(v)
            ids.append(index[v])
        triangles.append(ids)
    lo=[min(v[j] for v in vertices) for j in range(3)]
    hi=[max(v[j] for v in vertices) for j in range(3)]
    return vertices,triangles,lo,[hi[j]-lo[j] for j in range(3)]

def write3mf(path,items):
    root=ET.Element(tag('model'),unit='millimeter',attrib={'xml:lang':'en-US'})
    ET.SubElement(root,tag('metadata'),name='Title').text=path.stem
    ET.SubElement(root,tag('metadata'),name='Description').text='MOCK ONLY; unpowered. A1 256 mm; named independent objects; no scaling.'
    resources=ET.SubElement(root,tag('resources'));build=ET.SubElement(root,tag('build'))
    oid=0
    for q in items:
        e=q['entry'];vs,ts,lo,sz=read_mesh(KIT/e['file'])
        parent=list(range(len(vs)))
        def find(v):
            while parent[v]!=v:
                parent[v]=parent[parent[v]];v=parent[v]
            return v
        for tri in ts:
            r=find(tri[0])
            for v in tri[1:]:parent[find(v)]=r
        chunks={}
        for tri in ts:chunks.setdefault(find(tri[0]),[]).append(tri)
        # A single native CAD solid can have several tessellation shells.
        # Keep that physical component intact rather than separating cap tips.
        if e['solid_count']==1:chunks={0:ts}
        q['entry']['model_count']=len(chunks)
        for ci,faces in enumerate(chunks.values(),1):
            oid+=1
            used=sorted({v for tri in faces for v in tri})
            remap={v:i for i,v in enumerate(used)}
            points=[]
            for v in used:
                vx,vy,vz=vs[v];x,y=vx-lo[0],vy-lo[1]
                if q['rot']==90:x,y=sz[1]-y,x
                points.append((x,y,vz-lo[2]))
            low=[min(v[j] for v in points) for j in range(3)]
            label=Path(e['file']).stem
            if len(chunks)>1:label+=f'__piece_{ci:02d}'
            obj=ET.SubElement(resources,tag('object'),id=str(oid),type='model',name=label)
            mesh=ET.SubElement(obj,tag('mesh'));verts=ET.SubElement(mesh,tag('vertices'))
            for xyz in points:
                ET.SubElement(verts,tag('vertex'),**{k:f'{xyz[j]-low[j]:.7f}' for j,k in enumerate(('x','y','z'))})
            tris=ET.SubElement(mesh,tag('triangles'))
            for a,b,c in faces:ET.SubElement(tris,tag('triangle'),v1=str(remap[a]),v2=str(remap[b]),v3=str(remap[c]))
            ET.SubElement(build,tag('item'),objectid=str(oid),transform=f'1 0 0 0 1 0 0 0 1 {q["x"]+low[0]:.7f} {q["y"]+low[1]:.7f} {low[2]:.7f}')
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))

def complete(kind,name):
    data=json.loads((PROFILES/kind/(name+'.json')).read_text())
    base=complete(kind,data['inherits']) if data.get('inherits') else {}
    for inc in data.get('include',[]):base.update(complete(kind,inc))
    base.update(data)
    for key in ('inherits','include'):base.pop(key,None)
    return base

def main():
    manifest=json.loads((KIT/'manifest.json').read_text())
    groups={k:[] for k in ('PLA_large','PLA_detail','PLA_collars','OPTIONAL_gauges')}
    excluded=[]
    for e in manifest['files']:
        name=Path(e['file']).stem
        if max(e['size_mm'][:2])>240:excluded.append(e['file']);continue
        if name.startswith('USB_'):g='PLA_collars'
        elif 'INSTALLED_HEIGHT_GAUGE' in name or 'option_retainer_M2' in name:g='OPTIONAL_gauges'
        elif ('QUARTER' in name and not name.startswith('switch_plate')) or name.startswith('acrylic_case_post'):g='PLA_large'
        else:g='PLA_detail'
        groups[g].append(e)
    (HERE/'parts').mkdir(exist_ok=True);(HERE/'presets').mkdir(exist_ok=True)
    printer=complete('machine','Bambu Lab A1 0.4 nozzle')
    filament=complete('filament','Generic PLA @BBL A1')
    process=complete('process','0.20mm Standard @BBL A1')
    process.update({'wall_loops':'2','sparse_infill_density':'5%','sparse_infill_pattern':'rectilinear','top_shell_layers':'2','bottom_shell_layers':'2','enable_prime_tower':'0','brim_type':'outer_only','brim_width':'3','enable_support':'1','support_type':'normal(auto)','support_on_build_plate_only':'1','support_threshold_angle':'45','print_sequence':'by layer'})
    detail=dict(process);detail.update({'layer_height':'0.1','initial_layer_print_height':'0.1','wall_loops':'2','sparse_infill_density':'8%','top_shell_layers':'3','bottom_shell_layers':'3','brim_width':'2'})
    for name,data in [('printer',printer),('PLA',filament),('large',process),('detail',detail)]:
        (HERE/'presets'/f'{name}.json').write_text(json.dumps(data,indent=2))
    printer02=complete('machine','Bambu Lab A1 0.2 nozzle')
    pla02=complete('filament','Generic PLA @BBL A1 0.2 nozzle')
    fine=complete('process','0.10mm Standard @BBL A1 0.2 nozzle')
    fine.update({'enable_prime_tower':'0','enable_support':'1','support_on_build_plate_only':'1','support_threshold_angle':'45','support_type':'normal(auto)','brim_type':'outer_only','brim_width':'2','sparse_infill_density':'10%','print_sequence':'by layer','wall_loops':'2','initial_layer_print_height':'0.1'})
    gauge=dict(fine);gauge.update({'layer_height':'0.05','initial_layer_print_height':'0.05','enable_support':'0'})
    for name,data in [('printer02',printer02),('PLA02',pla02),('fine',fine),('gauge',gauge)]:
        (HERE/'presets'/f'{name}.json').write_text(json.dumps(data,indent=2))
    printer06=complete('machine','Bambu Lab A1 0.6 nozzle')
    pla06=dict(filament);pla06['compatible_printers']=['Bambu Lab A1 0.6 nozzle']
    coarse=complete('process','0.24mm Optimal @BBL A1 0.6 nozzle')
    for key in ('wall_loops','sparse_infill_density','sparse_infill_pattern','top_shell_layers','bottom_shell_layers','enable_prime_tower','brim_type','brim_width','enable_support','support_type','support_on_build_plate_only','support_threshold_angle','print_sequence'):coarse[key]=process[key]
    coarse.update(layer_height='0.2',initial_layer_print_height='0.2')
    for name,data in [('printer06',printer06),('PLA06',pla06),('coarse',coarse)]:
        (HERE/'presets'/f'{name}.json').write_text(json.dumps(data,indent=2))
    plan=[]
    for group,entries in groups.items():
        for e in entries:
            name=Path(e['file']).stem
            w,h=e['size_mm'][:2]
            assert w<=240 and h<=240
            q={'entry':e,'x':(256-w)/2,'y':(256-h)/2,'rot':0,'w':w,'h':h}
            write3mf(HERE/'parts'/f'{name}.3mf',[q])
            proc={'PLA_large':'large','PLA_detail':'detail','PLA_collars':'fine','OPTIONAL_gauges':'gauge'}[group]
            nozzle=0.2 if proc in ('fine','gauge') else 0.4
            if group=='PLA_large' and name.startswith(('top_acrylic','bottom_acrylic','PCB_SELECTED','acrylic_case_post')):
                proc='coarse';nozzle=0.6
            row={'plate':name,'job_id':f'{len(plan)+1:03d}','file':f'parts/{name}.3mf','material':'PLA','process':proc,'nozzle_mm':nozzle,'optional':group=='OPTIONAL_gauges','model_count':e['model_count'],'parts':[{'source':e['file'],'x':q['x'],'y':q['y'],'rotation_deg':0,'bounds_xy':[w,h],'sha256':hashlib.sha256((KIT/e['file']).read_bytes()).hexdigest()}]}
            plan.append(row)
    report={'printer':'Bambu Lab A1','bed_mm':[256,256],'mode':'one part per file','scaled':False,'min_margin_mm':8,'print_plan':plan,'excluded_full_size_alternatives':excluded,'part_count':len(plan)}
    (HERE/'print-plan.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({'plates':len(plan),'parts':report['part_count'],'groups':{g:len(es) for g,es in groups.items()}}))

if __name__=='__main__':main()
