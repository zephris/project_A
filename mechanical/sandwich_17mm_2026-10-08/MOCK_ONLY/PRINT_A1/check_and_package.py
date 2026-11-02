"""Validate current plate files, collect actual slice estimates and package."""
from pathlib import Path
import json,zipfile,hashlib,math,re
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
KIT=HERE.parent
plan=json.loads((HERE/'print-plan.json').read_text())
slice_records=json.loads((HERE/'slice-results.json').read_text())
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
seen=set();results=[]
review=HERE/'review';review.mkdir(exist_ok=True)
montage=Image.new('RGB',(1440,2260),'#edf1f6');draw=ImageDraw.Draw(montage)
for i,row in enumerate(plan['print_plan']):
    assert len(row['parts'])==1
    objects=[]
    for p in row['parts']:
        assert p['source'] not in seen,p['source'];seen.add(p['source'])
        assert hashlib.sha256((KIT/p['source']).read_bytes()).hexdigest()==p['sha256']
        x,y=p['x'],p['y'];w,h=p['bounds_xy']
        assert x>=8 and y>=8 and x+w<=248.001 and y+h<=248.001
        assert not(x+w>222 and y+h>220)
        for q in objects:
            assert x+w+5.999<=q['x'] or q['x']+q['bounds_xy'][0]+5.999<=x or y+h+5.999<=q['y'] or q['y']+q['bounds_xy'][1]+5.999<=y
        objects.append(p)
    with zipfile.ZipFile(HERE/row['file']) as z:root=ET.fromstring(z.read('3D/3dmodel.model'))
    assert root.attrib['unit']=='millimeter'
    assert not root.findall('m:resources/m:object/m:components',ns), 'Unexpected assembly wrapper'
    model_objects=root.findall('m:resources/m:object',ns)
    items=root.findall('m:build/m:item',ns)
    assert len(model_objects)==len(items)==row['model_count']
    all_vertices=[];triangles=0
    by_id={obj.attrib['id']:obj for obj in model_objects}
    for item in items:
        mesh=by_id[item.attrib['objectid']].find('m:mesh',ns)
        transform=[float(v) for v in item.attrib['transform'].split()]
        assert transform[:9]==[1,0,0,0,1,0,0,0,1]
        for v in mesh.findall('m:vertices/m:vertex',ns):
            xyz=[float(v.attrib[k])+transform[9+j] for j,k in enumerate(('x','y','z'))]
            assert all(math.isfinite(v) for v in xyz)
            all_vertices.append(xyz)
        triangles+=len(mesh.findall('m:triangles/m:triangle',ns))
    low=[min(v[k] for v in all_vertices) for k in range(3)]
    size=[max(v[k] for v in all_vertices)-low[k] for k in range(3)]
    assert max(abs(size[k]-row['parts'][0]['bounds_xy'][k]) for k in (0,1))<.001
    assert abs(low[0]-row['parts'][0]['x'])<.001 and abs(low[1]-row['parts'][0]['y'])<.001
    assert abs(low[2])<.001
    source=KIT/row['parts'][0]['source']
    import struct
    assert triangles==struct.unpack_from('<I',source.read_bytes(),80)[0]
    res=slice_records[row['plate']]
    assert res['input_sha256']==hashlib.sha256((HERE/row['file']).read_bytes()).hexdigest()
    assert res['return_code']==0 and len(res['sliced_plates'])==1
    sliced=res['sliced_plates'][0]
    assert not sliced.get('warning_message'),sliced.get('warning_message')
    assert sliced['filament_change_times']==0
    gcode3mf=HERE/'sliced'/(row['plate']+'.gcode.3mf')
    with zipfile.ZipFile(gcode3mf) as z:
        gc=z.read('Metadata/plate_1.gcode').decode('utf-8')
        config=ET.fromstring(z.read('Metadata/model_settings.config'))
        assert len(config.findall('object'))==row['model_count']
        assert all(len(obj.findall('part'))==1 for obj in config.findall('object'))
    assert '; printer_model = Bambu Lab A1\n' in gc
    assert f'; nozzle_diameter = {row["nozzle_mm"]}\n' in gc
    assert '; filament_type = PLA\n' in gc
    assert '; enable_prime_tower = 0\n' in gc
    expected=json.loads((HERE/'presets'/(row['process']+'.json')).read_text())
    for k in ('wall_loops','sparse_infill_density','top_shell_layers','bottom_shell_layers'):
        assert f'; {k} = {expected[k]}\n' in gc,(row['plate'],k)
    gcode3mf=HERE/'sliced'/(row['plate']+'.gcode.3mf')
    with zipfile.ZipFile(gcode3mf) as z:
        assert 'Metadata/plate_1.gcode' in z.namelist()
        png=z.read('Metadata/top_1.png');(review/(row['plate']+'.png')).write_bytes(png)
    im=Image.open(review/(row['plate']+'.png')).convert('RGBA')
    bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);bg=bg.convert('RGB');bg.thumbnail((342,226))
    cx=(i%4)*360+9;cy=(i//4)*370+30
    if i<24:montage.paste(bg,(cx,cy))
    grams=sum(f['total_used_g'] for f in sliced['filaments']);seconds=sliced['total_predication']
    if i<24:draw.text((cx,cy-20),row['plate'][:45],fill='#122438')
    if i<24:draw.text((cx,cy+232),f'{row["nozzle_mm"]} mm nozzle | {len(row["parts"])} parts',fill='#122438')
    if i<24:draw.text((cx,cy+248),f'{grams:.1f} g | {seconds/60:.0f} min'+(' | optional' if row['optional'] else ''),fill='#122438')
    results.append({'plate':row['plate'],'nozzle_mm':row['nozzle_mm'],'parts':len(row['parts']),'optional':row['optional'],'grams':grams,'seconds':seconds,'filament_changes':0,'warning_message':sliced.get('warning_message',''),'sliced_3mf':gcode3mf.relative_to(HERE).as_posix()})
assert len(seen)==105
montage.save(review/'part-overview.png')
summary={'pass':True,'files':len(results),'parts':len(seen),'one_part_per_file':True,'scale':1,'results':results}
for key,selected in [('all',results),('required',[r for r in results if not r['optional']])]:
    summary[key]={'grams':sum(r['grams'] for r in selected),'hours':sum(r['seconds'] for r in selected)/3600,'files':len(selected)}
summary['independent_models']=sum(row['model_count'] for row in plan['print_plan'])
(HERE/'print-check.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
from write_guide import write_guide
write_guide()
if (HERE/'README.md').exists():
    with zipfile.ZipFile(HERE/'A1_PLA_fitment_kit.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in [HERE/'README.md',HERE/'print-plan.json',HERE/'print-check.json',HERE/'slice-results.json',HERE/'prepare_prints.py',HERE/'slice_plates.py',HERE/'check_and_package.py',HERE/'write_guide.py',review/'part-overview.png']:
            z.write(p,p.relative_to(HERE))
        for p in (HERE/'presets').glob('*.json'):
            if p.stem!='detail_test':z.write(p,p.relative_to(HERE))
        for row in plan['print_plan']:
            for p in [HERE/row['file'],HERE/'sliced'/(row['plate']+'.gcode.3mf')]:
                z.write(p,p.relative_to(HERE))
    print('Packaged',HERE/'A1_PLA_fitment_kit.zip')
