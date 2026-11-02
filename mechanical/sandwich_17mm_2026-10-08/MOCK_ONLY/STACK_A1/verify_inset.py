"""Check inset source geometry, native transforms, contacts, settings and full arcs."""
from pathlib import Path
import hashlib,json,math,sys,zipfile,xml.etree.ElementTree as ET
sys.dont_write_bytecode=True
import numpy as np
from verify_stack import saved_mesh_bounds,native_names_and_project,deposited_paths
from audit_bounds import audit
HERE=Path(__file__).resolve().parent
STEM='stacked_kit_inset'
NS={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}


def main():
    manifest=json.loads((HERE/'stack-manifest_inset.json').read_text());parts=manifest['parts']
    legacy=HERE/'SUPERSEDED_DO_NOT_PRINT'
    old_manifest=(legacy/'stack-manifest.json') if (legacy/'stack-manifest.json').exists() else HERE/'stack-manifest.json'
    old=json.loads(old_manifest.read_text())['parts']
    assert len(parts)==105 and {p['source']:p['sha256'] for p in parts}=={p['source']:p['sha256'] for p in old}
    a=np.array([[p['x'],p['y'],p['z']] for p in parts])
    b=np.array([[p['x']+p['footprint_mm'][0],p['y']+p['footprint_mm'][1],p['z']+p['size_mm'][2]] for p in parts])
    separations=[]
    for i,p in enumerate(parts):
        assert hashlib.sha256((HERE.parent/p['source']).read_bytes()).hexdigest()==p['sha256']
        assert np.min(a[i,:2])>=14-1e-6 and np.max(b[i,:2])<=242+1e-6
        assert not (b[i,0]>182+1e-5 and b[i,1]>166+1e-5)
        for j in range(i):
            if np.all(np.minimum(b[i,:2],b[j,:2])-np.maximum(a[i,:2],a[j,:2])>1e-4):
                gap=max(a[i,2]-b[j,2],a[j,2]-b[i,2]);separations.append(float(gap))
                assert gap>=1-1e-4,(p['name'],parts[j]['name'],gap)
    with zipfile.ZipFile(HERE/(STEM+'.3mf')) as z:
        root=ET.fromstring(z.read('3D/3dmodel.model'))
        assert len(root.findall('m:resources/m:object/m:mesh',NS))==105
        assert len(root.findall('m:build/m:item',NS))==1
    contents,config=native_names_and_project(STEM,parts)
    settings=json.loads(contents['Metadata/project_settings.config'])
    expected={'printer_model':'Bambu Lab A1','nozzle_diameter':['0.4'],
              'printable_area':['0x0','256x0','256x256','0x256'],'bed_exclude_area':[],
              'printable_height':'256','print_sequence':'by layer',
              'filament_type':['PLA','PETG'],'layer_height':'0.1','initial_layer_print_height':'0.1',
              'support_filament':'1','support_interface_filament':'2',
              'support_top_z_distance':'0','support_bottom_z_distance':'0',
              'support_interface_top_layers':'2','support_interface_bottom_layers':'2',
              'support_interface_spacing':'0','support_bottom_interface_spacing':'0',
              'support_on_build_plate_only':'0','enable_prime_tower':'1',
              'wipe_tower_x':['196'],'wipe_tower_y':['180'],'prime_tower_width':'35',
              'flush_into_objects':'0','flush_into_infill':'0','flush_into_support':'0',
              'flush_volumes_matrix':['0','800','800','0'],
              'nozzle_temperature':['220','245'],'filament_max_volumetric_speed':['21','8'],
              'filament_flow_ratio':['0.98','0.94']}
    for key,value in expected.items():assert settings.get(key)==value,(key,settings.get(key),value)
    old_slice=(legacy/'stacked_kit.gcode.3mf') if (legacy/'stacked_kit.gcode.3mf').exists() else HERE/'stacked_kit.gcode.3mf'
    with zipfile.ZipFile(old_slice) as z:
        old_settings=json.loads(z.read('Metadata/project_settings.config'))
    service_keys=('machine_start_gcode','machine_end_gcode','change_filament_gcode','time_lapse_gcode','layer_change_gcode')
    for key in service_keys:assert settings.get(key)==old_settings.get(key),key
    slice_info=ET.fromstring(contents['Metadata/slice_info.config'])
    assert slice_info.find("plate/metadata[@key='outside']").get('value')=='false'
    actual=saved_mesh_bounds(contents)
    native=config.findall('object/part');assert len(native)==105
    max_error=max(float(abs(actual[el.get('id')]-np.array([a[i],b[i]])).max()) for i,el in enumerate(native))
    assert max_error<.02,max_error
    # Retain the actual native model placements and settings, excluding cached G-code.
    project=dict(contents)
    cfg=ET.fromstring(project['Metadata/model_settings.config'])
    for plate in cfg.findall('plate'):
        for meta in list(plate):
            if meta.get('key')=='gcode_file':plate.remove(meta)
    project['Metadata/model_settings.config']=ET.tostring(cfg,encoding='utf-8',xml_declaration=True)
    relpath='Metadata/_rels/model_settings.config.rels'
    if relpath in project:
        rel=ET.fromstring(project[relpath])
        for el in list(rel):
            if '.gcode' in el.get('Target',''):rel.remove(el)
        project[relpath]=ET.tostring(rel,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(HERE/(STEM+'_project.3mf'),'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in project.items():
            if not name.endswith(('.gcode','.gcode.md5')) and name not in ('Metadata/slice_info.config','Metadata/filament_sequence.json'):
                z.writestr(name,data)
    totals,layers,bounds=deposited_paths(HERE/(STEM+'.gcode.3mf'))
    contacts=[]
    for i,p in enumerate(parts):
        if p['z']<=0:continue
        count=0
        for height,segments in layers.items():
            if not p['z']-.251<=height<=p['z']+.051:continue
            for feature,filament,x0,y0,x1,y1 in segments:
                if feature!='Support interface' or filament!=1:continue
                # Conservative segment/footprint intersection, not endpoints alone.
                dx,dy=x1-x0,y1-y0;t0,t1=0.,1.;valid=True
                for u,v in ((-dx,x0-a[i,0]+.25),(dx,b[i,0]+.25-x0),(-dy,y0-a[i,1]+.25),(dy,b[i,1]+.25-y0)):
                    if abs(u)<1e-12:
                        if v<0:valid=False;break
                    elif u<0:t0=max(t0,v/u)
                    else:t1=min(t1,v/u)
                if valid and t0<=t1:count+=1
        assert count>0,p['name']
        contacts.append({'part':p['name'],'z_mm':p['z'],'PETG_segments_below':count})
    result=audit(HERE/(STEM+'.gcode.3mf'),5)
    (HERE/'review/inset-bounds-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    assert not result['failures'],result['failures']
    v={'failures':[],'part_count':105,'source_geometry_hashes_unchanged':True,
       'bbox_min_mm':a.min(axis=0).tolist(),'bbox_max_mm':b.max(axis=0).tolist(),
       'minimum_stacked_bbox_separation_mm':min(separations),'native_position_max_error_mm':max_error,
       'slicer_settings_verified':expected,'stock_service_templates_unchanged':list(service_keys),
       'every_elevated_part_has_PETG_below':True,'contacts':contacts,
       'feature_volumes_mm3':{f'{f} / {("PLA","PETG")[t]}':round(vol,2) for (f,t),vol in totals.items()},
       'feature_xy_bounds_mm':bounds,
       'limitations':'Geometry and file checks only. Interface segments in each elevated footprint do not prove full underside support coverage or physical release; no print was started.'}
    (HERE/'review/inset-verification.json').write_text(json.dumps(v,indent=2),encoding='utf-8')
    for img in ('plate_1.png','top_1.png'):
        if 'Metadata/'+img in contents:(HERE/'review'/('inset-'+img)).write_bytes(contents['Metadata/'+img])
    selected=json.loads((HERE/'review/stacked_kit_inset-slice.json').read_text())['sliced_plates'][0]
    density={'PLA':1.26,'PETG':1.27}
    mass=lambda f,m:v['feature_volumes_mm3'].get(f+' / '+m,0)*density[m]/1000
    scaffold=mass('Support','PLA')+mass('Support transition','PLA')
    tower={m:mass('Prime tower',m) for m in density}
    total={m:selected['filaments'][i]['total_used_g'] for i,m in enumerate(density)}
    main_mass={m:selected['filaments'][i]['main_used_g'] for i,m in enumerate(density)}
    rows=[{'category':'Mock parts + adhesion brim','PLA_g':main_mass['PLA']-scaffold,'PETG_g':0},
          {'category':'PLA scaffold + transition','PLA_g':scaffold,'PETG_g':0},
          {'category':'PETG release interfaces','PLA_g':0,'PETG_g':main_mass['PETG']},
          {'category':'Prime tower','PLA_g':tower['PLA'],'PETG_g':tower['PETG']},
          {'category':'Purge / material-change waste (inferred)','PLA_g':total['PLA']-main_mass['PLA']-tower['PLA'],
           'PETG_g':total['PETG']-main_mass['PETG']-tower['PETG']}]
    for m in density:assert abs(sum(row[m+'_g'] for row in rows)-total[m])<.001
    materials={'categories':rows,'job_totals_g':total,'estimated_hours':selected['total_predication']/3600,
               'AMS_changes':selected['filament_change_times'],
               'method':'Tower from positive XY extrusion. Purge is slicer total minus main minus measured tower. Main excludes tower. PETG main mass is all support interface. Estimates include rounding residuals and are not weighed consumption.'}
    (HERE/'review/inset-material-breakdown.json').write_text(json.dumps(materials,indent=2),encoding='utf-8')
    print(json.dumps({'parts':105,'max_position_error_mm':max_error,'elevated_parts_checked':len(contacts),
                      'bounds':result['xy_bounds_mm'],'hours':materials['estimated_hours'],'grams':total,'failures':[]},indent=2))


if __name__=='__main__':main()
