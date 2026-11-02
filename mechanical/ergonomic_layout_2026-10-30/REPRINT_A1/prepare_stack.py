"""One inset multipart Bambu A1 stack; PLA models/PETG release interfaces."""
from pathlib import Path
import json,math,struct,zipfile,hashlib,shutil,sys,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
OLD=HERE.parents[1]/'sandwich_17mm_2026-10-08/MOCK_ONLY/STACK_A1'
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',NS)
def tag(t):return '{'+NS+'}'+t

def mesh(path):
    raw=path.read_bytes();n=struct.unpack_from('<I',raw,80)[0];assert len(raw)==84+n*50
    vs=[];ts=[];index={}
    for i in range(n):
        f=struct.unpack_from('<12fH',raw,84+50*i);tri=[]
        for j in (3,6,9):
            v=tuple(f[j:j+3])
            if v not in index:index[v]=len(vs);vs.append(v)
            tri.append(index[v])
        ts.append(tri)
    return vs,ts

def export(items):
    root=ET.Element(tag('model'),unit='millimeter',attrib={'xml:lang':'en-US'})
    ET.SubElement(root,tag('metadata'),name='Title').text='PHBox replacement-only vertical stack; PLA models, PETG interfaces'
    res=ET.SubElement(root,tag('resources'))
    for i,p in enumerate(items,1):
        vs,ts=mesh(HERE/p['source']);obj=ET.SubElement(res,tag('object'),id=str(i),type='model',name=p['name'])
        m=ET.SubElement(obj,tag('mesh'));v=ET.SubElement(m,tag('vertices'));t=ET.SubElement(m,tag('triangles'))
        for pt in vs:ET.SubElement(v,tag('vertex'),**{k:f'{pt[j]:.7f}' for j,k in enumerate('xyz')})
        for a,b,c in ts:ET.SubElement(t,tag('triangle'),v1=str(a),v2=str(b),v3=str(c))
    obj=ET.SubElement(res,tag('object'),id='1000',type='model',name='PLA_replacements_supported_vertical_stack')
    components=ET.SubElement(obj,tag('components'))
    for i,p in enumerate(items,1):ET.SubElement(components,tag('component'),objectid=str(i),transform=f'1 0 0 0 1 0 0 0 1 {p["x"]:.7f} {p["y"]:.7f} {p["z"]:.7f}')
    build=ET.SubElement(root,tag('build'));ET.SubElement(build,tag('item'),objectid='1000')
    with zipfile.ZipFile(HERE/'reprint_stack.3mf','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))

def main():
    manifest=json.loads((HERE/'manifest.json').read_text());entries={e['name']:e for e in manifest['files']}
    items=[];slots=[{'x':14.,'y':14.,'z':0.},{'x':14.,'y':118.,'z':0.}]
    def put(name,slot):
        e=entries[name];w,h,d=e['size_mm']
        p={'name':name,'source':e['file'],'sha256':e['sha256'],'size_mm':e['size_mm'],'footprint_mm':[w,h],
           'x':slot['x'],'y':slot['y'],'z':slot['z'],'rotation_deg':0,'column':f'panel {slots.index(slot)+1}'}
        assert p['x']+w<=242 and p['y']+h<=242
        items.append(p);slot['z']=round(math.ceil((slot['z']+d+1-1e-5)*10)/10,5)
    for family in ('top_acrylic_SURROGATE','switch_plate'):
        for q in (1,2,3,4):put(f'{family}_QUARTER_{q}',min(slots,key=lambda s:s['z']))
    # Broad carrier ledges stay below the tall upper walls. Otherwise their
    # floors need scaffold through an upper spacer's entire empty cavity.
    for q in (1,2):put(f'bottom_spacer_QUARTER_{q}',min(slots,key=lambda s:s['z']))
    for q in (3,4):
        slot=min(slots,key=lambda s:s['z'])
        put(f'bottom_spacer_QUARTER_{q}',slot);put(f'top_spacer_QUARTER_{q}',slot)
    # All small parts sit on the bed in the right-hand pocket, outside the tower reserve.
    remaining=[e for e in entries.values() if e['name'] not in {p['name'] for p in items}]
    small=[]
    for e in sorted(remaining,key=lambda e:e['size_mm'][0]*e['size_mm'][1],reverse=True):
        w,h,d=e['size_mm'];best=None
        for x in sorted({174.}|{p['x']+p['footprint_mm'][0]+3 for p in small}):
            for y in sorted({14.}|{p['y']+p['footprint_mm'][1]+3 for p in small}):
                if x+w>242 or y+h>166:continue
                if any(not(x+w+3<=p['x'] or p['x']+p['footprint_mm'][0]+3<=x or y+h+3<=p['y'] or p['y']+p['footprint_mm'][1]+3<=y) for p in small):continue
                score=(y+h,x+w,x,y)
                if best is None or score<best:best=score
        assert best,e['name']
        _,_,x,y=best
        small.append({'name':e['name'],'source':e['file'],'sha256':e['sha256'],'size_mm':e['size_mm'],'footprint_mm':[w,h],
                      'x':x,'y':y,'z':0.,'rotation_deg':0,'column':'bed pocket'})
    items+=small;assert len(items)==20
    export(items)
    (HERE/'presets').mkdir(exist_ok=True)
    for filename in ('printer.json','PLA.json','PETG_interface.json'):
        shutil.copy2(OLD/'presets'/filename,HERE/'presets'/filename)
    process=json.loads((OLD/'presets/stack_inset.json').read_text())
    process['name']='PHBox A1 replacement-only 20-part stack 0.10mm'
    (HERE/'presets/process.json').write_text(json.dumps(process,indent=2)+'\n')
    out={'printer':'Bambu Lab A1','nozzle_mm':.4,'plate':'Textured PEI','model_material':'PLA','support_base':'PLA','support_interface':'PETG',
         'gap_mm':1.,'minimum_source_inset_mm':14.,'minimum_generated_path_margin_mm':5.,'tower_reserve_xy_mm':[182,166,242,232],
         'part_count':20,'height_mm':max(p['z']+p['size_mm'][2] for p in items),'parts':items,
         'warning':'PLA mock and three PLA plug trials; physical support release and fit remain unqualified. Keep multipart assembly intact.'}
    (HERE/'stack-manifest.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'parts':len(items),'source_height_mm':out['height_mm'],'bed_pocket_parts':len(small)},indent=2))

if __name__=='__main__':main()
