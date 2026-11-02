"""Inspect saved geometry, material settings and deposited support toolpaths.

This is file-only validation; it never contacts a printer.
"""
from pathlib import Path
import json,zipfile,hashlib,re,math,collections,xml.etree.ElementTree as ET
import numpy as np
HERE=Path(__file__).resolve().parent
KIT=HERE.parent
NS={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}

def deposited_paths(path):
    totals=collections.defaultdict(float);layers=collections.defaultdict(list)
    bounds=collections.defaultdict(lambda:[999.,999.,-999.,-999.])
    filament=0;feature='Custom';xy=[0.,0.];z=0.;relative=True;last_e=0.
    with zipfile.ZipFile(path) as archive:
        entry=next(n for n in archive.namelist() if n.endswith('plate_1.gcode'))
        for line in archive.open(entry):
            if line.startswith(b'; FEATURE:'):feature=line[11:].strip().decode();continue
            if line.startswith(b'; Z_HEIGHT:'):z=float(line.split(b':')[1]);continue
            if re.fullmatch(rb'T[0-9]+\s*',line):
                n=int(line[1:]);filament=n if n<2 else filament
            if line.startswith(b'M83'):relative=True
            elif line.startswith(b'M82'):relative=False
            elif line.startswith(b'G92 E'):last_e=float(line.split(b'E')[1].split()[0])
            if not line.startswith((b'G0 ',b'G1 ',b'G2 ',b'G3 ')):continue
            vals={k.decode():float(v) for k,v in re.findall(rb'([XYE])([-+\d.]+)',line.split(b';')[0])}
            nx,ny=vals.get('X',xy[0]),vals.get('Y',xy[1]);ex=vals.get('E',0.)
            if not relative:
                ex=vals.get('E',last_e)-last_e;last_e=vals.get('E',last_e)
            if ex>0 and ('X' in vals or 'Y' in vals) and math.hypot(nx-xy[0],ny-xy[1])>0.0001:
                totals[(feature,filament)]+=ex*math.pi*(1.75/2)**2
                b=bounds[feature]
                b[0]=min(b[0],xy[0],nx);b[1]=min(b[1],xy[1],ny)
                b[2]=max(b[2],xy[0],nx);b[3]=max(b[3],xy[1],ny)
                if feature!='Custom':layers[round(z,3)].append((feature,filament,xy[0],xy[1],nx,ny))
            xy=[nx,ny]
    return totals,layers,dict(bounds)

def native_names_and_project(name,parts):
    source=HERE/(name+'.gcode.3mf')
    with zipfile.ZipFile(source) as z:contents={n:z.read(n) for n in z.namelist()}
    config=ET.fromstring(contents['Metadata/model_settings.config'])
    native=config.findall('object/part')
    assert len(native)==len(parts)
    for el,p in zip(native,parts):
        el.find("metadata[@key='name']").set('value',f'T{p.get("tier",0):02d}_{p["name"]}')
    new_config=ET.tostring(config,encoding='utf-8',xml_declaration=True)
    changed=new_config!=contents['Metadata/model_settings.config']
    contents['Metadata/model_settings.config']=new_config
    if changed:
        with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED) as z:
            for n,b in contents.items():z.writestr(n,b)
    return contents,config

def saved_mesh_bounds(contents):
    """Use actual 3MF component transforms, not source-import history matrices."""
    models={};out={}
    def model(path):
        if path not in models:models[path]=ET.fromstring(contents[path])
        return models[path]
    def matrix(value):
        raw=np.array(list(map(float,value.split()))).reshape(4,3) if value else np.vstack((np.eye(3),[0,0,0]))
        result=np.eye(4);result[:3,:3]=raw[:3].T;result[:3,3]=raw[3];return result
    def walk(path,oid,transform):
        root=model(path);obj=root.find("m:resources/m:object[@id='"+oid+"']",NS)
        mesh=obj.find('m:mesh',NS)
        if mesh is not None:
            pts=np.array([[float(v.get(k)) for k in 'xyz'] for v in mesh.findall('m:vertices/m:vertex',NS)])
            pts=pts@transform[:3,:3].T+transform[:3,3]
            out[oid]=np.array([pts.min(axis=0),pts.max(axis=0)])
        else:
            for component in obj.findall('m:components/m:component',NS):
                target=component.get('{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}path',path).lstrip('/')
                walk(target,component.get('objectid'),transform@matrix(component.get('transform')))
    for item in model('3D/3dmodel.model').findall('m:build/m:item',NS):
        walk('3D/3dmodel.model',item.get('objectid'),matrix(item.get('transform')))
    return out

def main():
    # The original endpoint-only verification is superseded.
    from verify_inset import main as verify_current
    verify_current()

if __name__=='__main__':main()
