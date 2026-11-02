"""Compare model-specific A1 profiles locally; never contacts a printer."""
from pathlib import Path
import sys,json,zipfile,subprocess,math,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'PRINT_A1'))
from prepare_prints import complete,read_mesh
WORK=HERE/'jobs/tuning'

def prepare():
    WORK.mkdir(parents=True,exist_ok=True)
    baseline=json.loads((HERE/'review/stacked_kit-slice.json').read_text())
    target=HERE/'review/parameter-tuning.json'
    if not target.exists():target.write_text(json.dumps({'baseline':baseline['sliced_plates'][0],'candidates':{}},indent=2))
    p=json.loads((HERE/'presets/stack.json').read_text())
    p.update({'name':'PHBox A1 balanced 0.10mm — Bambu PLA / PETG interface',
        'layer_height':'0.1','initial_layer_print_height':'0.1',
        'top_shell_layers':'4','top_shell_thickness':'0.4','bottom_shell_layers':'3','bottom_shell_thickness':'0.3',
        'sparse_infill_density':'10%','outer_wall_speed':['100'],'outer_wall_acceleration':['2000'],
        'inner_wall_speed':['200'],'inner_wall_acceleration':['4000'],
        'small_perimeter_threshold':['6'],'small_perimeter_speed':['35'],
        'top_surface_speed':['80'],'top_surface_acceleration':['1500'],
        'initial_layer_speed':['30'],'initial_layer_infill_speed':['50'],
        'support_interface_speed':['50'],'travel_speed':['500']})
    (WORK/'balanced.json').write_text(json.dumps(p,indent=2))
    faster=dict(p,name='PHBox A1 fitment balanced 0.10mm',support_interface_speed=['80'],prime_tower_max_speed='120')
    (WORK/'interface80.json').write_text(json.dumps(faster,indent=2))
    pla=complete('filament','Bambu PLA Basic @BBL A1')
    pla['filament_settings_id']=['PHBox Bambu PLA Basic @A1']
    pla['filament_colour']=['#3E84B5'];pla['filament_bridge_speed']=['35']
    petg=complete('filament','Bambu PETG Basic @BBL A1')
    petg.update({'name':'PHBox Bambu PETG conservative interface @A1',
        'filament_settings_id':['PHBox Bambu PETG conservative — Basic/HF unconfirmed'],
        'filament_id':'GFG99','filament_max_volumetric_speed':['8'],'filament_density':['1.27'],
        'filament_colour':['#31AD48']})
    for filament in (pla,petg):
        filament['filament_flush_temp']=['245'];filament['filament_flush_temp_fast']=['245']
        for key in ('hot_plate_temp','hot_plate_temp_initial_layer','textured_plate_temp','textured_plate_temp_initial_layer'):
            filament[key]=['65']
    for name,data in [('PLA',pla),('PETG_interface',petg)]:
        (WORK/(name+'.json')).write_text(json.dumps(data,indent=2))
    manifest=json.loads((HERE/'stack-manifest.json').read_text());levels=set()
    for q in manifest['parts']:
        vs,ts,lo,sz=read_mesh(HERE.parent/q['source'])
        for tri in ts:
            zs=[vs[j][2]-lo[2]+q['z'] for j in tri]
            if max(zs)-min(zs)<.0001:levels.add(round(sum(zs)/3,4))
    bands=sorted((max(0,z-.3),min(manifest['height_mm'],z+.3)) for z in levels)
    merged=[]
    for a,b in bands:
        if merged and a<=merged[-1][1]:merged[-1][1]=max(b,merged[-1][1])
        else:merged.append([a,b])
    ranges=[]
    for i in range(len(merged)-1):
        a=math.ceil((merged[i][1]+1e-5)*10)/10;b=math.floor((merged[i+1][0]-1e-5)*10)/10
        b=a+math.floor((b-a+1e-5)/.2)*.2
        if b-a>=.6-1e-5:ranges.append([round(a,3),round(b,3)])
    tree=ET.Element('objects');obj=ET.SubElement(tree,'object',id='1')
    for a,b in ranges:
        region=ET.SubElement(obj,'range',min_z=str(a),max_z=str(b))
        ET.SubElement(region,'option',opt_key='layer_height').text='0.2'
    with zipfile.ZipFile(HERE/'stacked_kit_project.3mf') as z:contents={n:z.read(n) for n in z.namelist()}
    contents['Metadata/layer_config_ranges.xml']=ET.tostring(tree,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(WORK/'hybrid.3mf','w',zipfile.ZIP_DEFLATED) as z:
        for n,b in contents.items():z.writestr(n,b)
    (WORK/'hybrid-ranges.json').write_text(json.dumps({'coarse_0p2_ranges_mm':ranges,'protected_surface_band_halfwidth_mm':.3},indent=2))
    print('Coarse regions:',ranges,flush=True)

def run(name):
    job=WORK/name;job.mkdir(exist_ok=True)
    model=WORK/'hybrid.3mf' if name=='hybrid' else HERE/'stacked_kit_project.3mf'
    process=WORK/(name+'.json') if (WORK/(name+'.json')).exists() else WORK/'balanced.json'
    args=['D:/Bambu Studio/bambu-studio.exe','--load-settings',str(HERE/'presets/printer.json')+';'+str(process),
        '--load-filaments',str(WORK/'PLA.json')+';'+str(WORK/'PETG_interface.json'),
        '--curr-bed-type','Textured PEI Plate','--arrange','0','--slice','0','--debug','2',
        '--outputdir',str(job),'--export-3mf','sliced.3mf',str(model)]
    r=subprocess.run(args,capture_output=True,text=True)
    (job/'cli.log').write_text(r.stdout+r.stderr,encoding='utf-8')
    result=json.loads((job/'result.json').read_text())
    summary={k:v for k,v in result.items() if k!='sliced_plates'}
    if result.get('sliced_plates'):
        plate=result['sliced_plates'][0]
        summary['plate']={k:v for k,v in plate.items() if k not in ('objects','feature_type_times')}
        summary['feature_times_seconds']=plate.get('feature_type_times',{})
    if name=='hybrid':summary['ranges']=json.loads((WORK/'hybrid-ranges.json').read_text())
    out=HERE/'review/parameter-tuning.json';data=json.loads(out.read_text());data['candidates'][name]=summary
    out.write_text(json.dumps(data,indent=2))
    print(json.dumps({'candidate':name,**summary},indent=2),flush=True)

if __name__=='__main__':
    if len(sys.argv)==1:prepare();run('balanced');run('hybrid')
    elif sys.argv[1]=='prepare':prepare()
    else:run(sys.argv[1])
