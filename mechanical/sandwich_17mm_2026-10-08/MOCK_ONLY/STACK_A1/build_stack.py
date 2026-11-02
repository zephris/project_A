"""Compose unmodified fitment meshes into a supported vertical PLA stack."""
from pathlib import Path
import sys,json,zipfile,xml.etree.ElementTree as ET,math,hashlib
HERE=Path(__file__).resolve().parent
KIT=HERE.parent
sys.path.insert(0,str(KIT/'PRINT_A1'))
from prepare_prints import write3mf,read_mesh,complete
NS={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
GAP=1.0
STEM='stacked_kit_inset'
MODEL_MIN=14.0
MODEL_MAX=242.0
TOWER_RESERVE=(182.,166.,242.,232.)

def export(path,items):
    write3mf(path,items)
    with zipfile.ZipFile(path) as z:contents={n:z.read(n) for n in z.namelist()}
    root=ET.fromstring(contents['3D/3dmodel.model'])
    build=root.findall('m:build/m:item',NS)
    assert len(build)==len(items)
    resources=root.find('m:resources',NS)
    assembly=ET.SubElement(resources,'{'+NS['m']+'}object',id='1000',type='model',name='PLA_supported_vertical_stack')
    components=ET.SubElement(assembly,'{'+NS['m']+'}components')
    for item,q in zip(build,items):
        transform=item.attrib['transform'].split();transform[11]=f'{q["z"]:.7f}'
        ET.SubElement(components,'{'+NS['m']+'}component',objectid=item.attrib['objectid'],transform=' '.join(transform))
        leaf=resources.find("m:object[@id='"+item.attrib['objectid']+"']",NS)
        leaf.set('name',f'T{q.get("tier",0):02d}_'+leaf.attrib['name'])
    build_element=root.find('m:build',NS)
    for item in build:build_element.remove(item)
    ET.SubElement(build_element,'{'+NS['m']+'}item',objectid='1000')
    contents['3D/3dmodel.model']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for n,data in contents.items():z.writestr(n,data)

def presets():
    (HERE/'presets').mkdir(exist_ok=True)
    p=json.loads((KIT/'PRINT_A1/presets/detail.json').read_text())
    p.update({'name':'PHBox A1 fitment balanced 0.10mm',
        'layer_height':'0.1','initial_layer_print_height':'0.1',
        'top_shell_layers':'4','top_shell_thickness':'0.4','bottom_shell_layers':'3','bottom_shell_thickness':'0.3',
        'sparse_infill_density':'10%','outer_wall_speed':['100'],'outer_wall_acceleration':['2000'],
        'inner_wall_speed':['200'],'inner_wall_acceleration':['4000'],
        'small_perimeter_threshold':['6'],'small_perimeter_speed':['35'],
        'top_surface_speed':['80'],'top_surface_acceleration':['1500'],
        'initial_layer_speed':['30'],'initial_layer_infill_speed':['50'],'travel_speed':['500'],
        'support_on_build_plate_only':'0','support_top_z_distance':'0','support_bottom_z_distance':'0',
        'support_filament':'1','support_interface_filament':'2',
        'support_interface_top_layers':'2','support_interface_bottom_layers':'2','support_interface_spacing':'0',
        'support_bottom_interface_spacing':'0','support_interface_pattern':'rectilinear','support_interface_speed':['80'],
        'raft_first_layer_expansion':'1.5',
        'support_base_pattern_spacing':'3','brim_type':'outer_only','brim_width':'3','wall_generator':'arachne',
        'print_sequence':'by layer','enable_prime_tower':'1','independent_support_layer_height':'0',
        'prime_tower_width':'35','prime_tower_rib_wall':'0','prime_tower_max_speed':'120','wipe_tower_x':['196'],'wipe_tower_y':['180'],
        'flush_into_infill':'0','flush_into_objects':'0','flush_into_support':'0',
        'flush_volumes_matrix':['0','800','800','0'],'flush_volumes_vector':['400','400','400','400'],
        'flush_multiplier':['1'],'wall_filament':'1','solid_infill_filament':'1','sparse_infill_filament':'1'})
    p['name']='PHBox A1 inset bounds 0.10mm'
    (HERE/'presets/stack_inset.json').write_text(json.dumps(p,indent=2))
    petg=complete('filament','Bambu PETG Basic @BBL A1')
    # PETG is used above the PLA scaffold, never as bed-contact material.
    # Match bed temperatures to PLA to avoid an 80 C bed under thin PLA panels.
    for key in ('hot_plate_temp','hot_plate_temp_initial_layer','textured_plate_temp','textured_plate_temp_initial_layer'):
        petg[key]=['65']
    # User confirms Bambu, but cannot identify Basic versus HF. Their flow
    # ratios agree; use a conservative shared interface speed/temperature.
    petg.update({'name':'PHBox Bambu PETG conservative interface @A1',
        'filament_settings_id':['PHBox Bambu PETG conservative â€” Basic/HF unconfirmed'],
        'filament_id':'GFG99','filament_max_volumetric_speed':['8'],'filament_density':['1.27']})
    petg['filament_colour']=['#31AD48']
    petg['filament_flush_temp']=['245'];petg['filament_flush_temp_fast']=['245']
    (HERE/'presets/PETG_interface.json').write_text(json.dumps(petg,indent=2))
    pla=complete('filament','Bambu PLA Basic @BBL A1')
    pla['filament_settings_id']=['PHBox Bambu PLA Basic @A1']
    pla['filament_colour']=['#3E84B5'];pla['filament_bridge_speed']=['35']
    pla['filament_flush_temp']=['245'];pla['filament_flush_temp_fast']=['245']
    (HERE/'presets/PLA.json').write_text(json.dumps(pla,indent=2))

def allowed(x,y,w,h):
    # Inset placements; keep the stock A1 limits and exact part dimensions.
    return (x>=MODEL_MIN and y>=MODEL_MIN and x+w<=MODEL_MAX and y+h<=MODEL_MAX
        and not(x+w>TOWER_RESERVE[0] and y+h>TOWER_RESERVE[1]))

def small_parts(entries,occupied):
    result=[]
    for e in sorted(entries,key=lambda e:e['size_mm'][0]*e['size_mm'][1],reverse=True):
        w,h,d=e['size_mm'];best=None
        zs={0.}|{p['z'] for p in occupied}|{round(math.ceil((max(p['z']+p['entry']['size_mm'][2] for p in occupied+result)+GAP-1e-5)*10)/10,5)}
        for z in sorted(zs):
            neighbours=[p for p in occupied+result if z< p['z']+p['entry']['size_mm'][2]+GAP-1e-5 and p['z']<z+d+GAP-1e-5]
            xs={MODEL_MIN}|{p['x']+p['w']+3 for p in neighbours}
            ys={MODEL_MIN}|{p['y']+p['h']+3 for p in neighbours}
            for x in sorted(xs):
                for y in sorted(ys):
                    for rot,a,b in ((0,w,h),(90,h,w)):
                        if not allowed(x,y,a,b):continue
                        if any(not(x+a+3<=p['x'] or p['x']+p['w']+3<=x or y+b+3<=p['y'] or p['y']+p['h']+3<=y) for p in neighbours):continue
                        score=(z,y+b,x+a,x,y,rot,a,b)
                        if best is None or score<best:best=score
            if best:break
        assert best is not None,e['file']
        z,_,_,x,y,rot,a,b=best
        result.append({'entry':e,'x':x,'y':y,'rot':rot,'w':a,'h':b,'z':z,'column':'infill pockets'})
    return result

def main():
    presets()
    manifest=json.loads((KIT/'manifest.json').read_text())
    e=next(e for e in manifest['files'] if e['file']=='STL/screen_frame.stl')
    items=[{'entry':dict(e),'x':108,'y':108,'z':z,'rot':0,'w':40.4,'h':38.5} for z in (0,1+GAP)]
    washer=next(e for e in manifest['files'] if 'acrylic_case_washer_1_top_0p5_SURROGATE' in e['file'])
    for z in (0,.5+GAP):items.append({'entry':dict(washer),'x':85,'y':108,'z':z,'rot':0,'w':7,'h':7})
    for needle,x,y in [('OPSW1_captive_cap_H5_trial',85,128),('printed_screen_stop_1_3mm',85,145)]:
        e=next(e for e in manifest['files'] if Path(e['file']).stem==needle)
        items.append({'entry':dict(e),'x':x,'y':y,'z':0,'rot':0,'w':e['size_mm'][0],'h':e['size_mm'][1]})
    export(HERE/'separator_trial.3mf',items)
    trial=[]
    for i,p in enumerate(items):
        trial.append({'name':Path(p['entry']['file']).stem+f'_trial_{i+1}',
            'source':p['entry']['file'],'x':p['x'],'y':p['y'],'z':p['z'],
            'size_mm':p['entry']['size_mm'],'tier':i+1})
    (HERE/'trial-manifest.json').write_text(json.dumps(trial,indent=2))
    # Preserve each source mesh and retain its exact fitment dimensions.
    entries=[e for e in manifest['files'] if max(e['size_mm'][:2])<=240]
    flat=[e for e in entries if 'QUARTER' in e['file'] and e['size_mm'][2]<=2.01]
    raised=[e for e in entries if 'PCB_SELECTED' in e['file'] and e not in flat]
    frames=[e for e in entries if 'QUARTER' in e['file'] and e not in flat and e not in raised]
    small=[e for e in entries if 'QUARTER' not in e['file']]
    # Full bottom-cover sections form the widest and most continuous base.
    # Two independently rising panel stacks: no empty space caused by the
    # tallest piece setting every other column's Z. Same-quarter spacer pairs
    # share XY and orientation so their perimeter walls support one another.
    slots=[{'x':14.,'y':14.,'rot':0,'z':0.},
           {'x':14.,'y':118.,'rot':0,'z':0.}]
    all_items=[];tier_records=[]
    def put(e,slot):
        w,h,d=e['size_mm'];a,b=(h,w) if slot['rot']==90 else (w,h)
        p={'entry':e,'x':slot['x'],'y':slot['y'],'rot':slot['rot'],'w':a,'h':b,'z':slot['z'],'column':f'panel {slots.index(slot)+1}'}
        assert allowed(p['x'],p['y'],a,b)
        all_items.append(p)
        slot['z']=round(math.ceil((slot['z']+d+GAP-1e-5)*10)/10,5)
    # Keep broad flat panels below the tall PCB envelopes and perimeter walls.
    flat.sort(key=lambda e:(not 'bottom_acrylic' in e['file'],not 'top_acrylic' in e['file'],e['file']))
    for e in flat+raised:put(e,min(slots,key=lambda s:s['z']))
    for q in (3,4,1,2):
        pair=[next(e for e in frames if f'{name}_QUARTER_{q}' in e['file']) for name in ('bottom_spacer','top_spacer')]
        slot=min(slots,key=lambda s:s['z'])
        for e in pair:put(e,slot)
    for z in sorted({p['z'] for p in all_items}):
        tier=[p for p in all_items if p['z']==z];number=len(tier_records)+1
        for p in tier:p['tier']=number
        height=max(p['entry']['size_mm'][2] for p in tier)
        tier_records.append({'tier':number,'column':'panels','family':'panel sections','z_min':z,'z_max':z+height,'height_mm':height,'parts':[p['entry']['file'] for p in tier]})
    pockets=small_parts(small,all_items)
    for z in sorted({p['z'] for p in pockets}):
        tier=[p for p in pockets if p['z']==z]
        height=max(p['entry']['size_mm'][2] for p in tier);number=len(tier_records)+1
        for p in tier:p['tier']=number
        all_items+=tier
        tier_records.append({'tier':number,'column':'infill pockets','family':'small components','z_min':z,'z_max':z+height,'height_mm':height,'parts':[p['entry']['file'] for p in tier]})
    assert len(all_items)==105
    export(HERE/(STEM+'.3mf'),all_items)
    (HERE/'stack-manifest_inset.json').write_text(json.dumps({'printer':'Bambu Lab A1','nozzle_mm':0.4,'material':'PLA',
        'support_base':'PLA','support_interface':'PETG','contact_z_gap_mm':0,'gap_mm':GAP,
        'model_placement_limits_xy_mm':[MODEL_MIN,MODEL_MIN,MODEL_MAX,MODEL_MAX],
        'required_generated_path_edge_margin_mm':5.,
        'tower_reserve_xy_mm':list(TOWER_RESERVE),
        'tier_count':len(tier_records),'height_mm':max(p['z']+p['entry']['size_mm'][2] for p in all_items),'tiers':tier_records,
        'parts':[{'name':Path(p['entry']['file']).stem,'source':p['entry']['file'],'sha256':hashlib.sha256((KIT/p['entry']['file']).read_bytes()).hexdigest(),
            'tier':p['tier'],'column':p['column'],'x':p['x'],'y':p['y'],'z':p['z'],'rotation_deg':p['rot'],'size_mm':p['entry']['size_mm'],'footprint_mm':[p['w'],p['h']]} for p in all_items]},indent=2))
    print('Stack:',len(tier_records),'tiers,',len(all_items),'parts,',round(max(t['z_max'] for t in tier_records),2),'mm high')

if __name__=='__main__':main()
