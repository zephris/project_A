"""Verify exact replacement sources, saved slicer placements, supports and arcs."""
from pathlib import Path
import json,hashlib,math,sys,zipfile,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
OLD=HERE.parents[1]/'sandwich_17mm_2026-10-08/MOCK_ONLY/STACK_A1'
sys.path.insert(0,str(OLD))
from audit_bounds import audit
from verify_stack import saved_mesh_bounds,deposited_paths
from prepare_stack import mesh
import numpy as np
from shapely.geometry import Polygon,LineString
from shapely.ops import unary_union
from shapely.affinity import translate
from shapely.prepared import prep

def main():
    m=json.loads((HERE/'stack-manifest.json').read_text());parts=m['parts']
    assert len(parts)==20 and sum('button_blank' in p['name'] for p in parts)==3
    a=np.array([[p['x'],p['y'],p['z']] for p in parts]);b=a+np.array([p['size_mm'] for p in parts])
    gaps=[];adjacent=[]
    for i,p in enumerate(parts):
        assert hashlib.sha256((HERE/p['source']).read_bytes()).hexdigest()==p['sha256']
        assert min(a[i,:2])>=14-1e-5 and max(b[i,:2])<=242+1e-5
        for j in range(i):
            if np.all(np.minimum(b[i,:2],b[j,:2])-np.maximum(a[i,:2],a[j,:2])>1e-4):
                gap=max(a[i,2]-b[j,2],a[j,2]-b[i,2]);assert gap>=1-1e-4
                gaps.append(float(gap))
    file=HERE/'reprint_stack.gcode.3mf'
    with zipfile.ZipFile(file) as z:contents={n:z.read(n) for n in z.namelist()}
    cfg=ET.fromstring(contents['Metadata/model_settings.config']);native=cfg.findall('object/part')
    assert len(native)==20,(len(native),[el.attrib for el in native])
    # Preserve clear individual labels in the native editable project and print archive.
    for el,p in zip(native,parts):el.find("metadata[@key='name']").set('value',p['name'])
    contents['Metadata/model_settings.config']=ET.tostring(cfg,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(file,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in contents.items():z.writestr(name,data)
    actual=saved_mesh_bounds(contents)
    max_error=max(float(abs(actual[el.get('id')]-np.array([a[i],b[i]])).max()) for i,el in enumerate(native))
    assert max_error<.02,max_error
    settings=json.loads(contents['Metadata/project_settings.config'])
    expected={'printer_model':'Bambu Lab A1','nozzle_diameter':['0.4'],'printable_area':['0x0','256x0','256x256','0x256'],
              'printable_height':'256','print_sequence':'by layer','layer_height':'0.1','initial_layer_print_height':'0.1',
              'filament_type':['PLA','PETG'],'support_on_build_plate_only':'0','support_filament':'1','support_interface_filament':'2',
              'support_top_z_distance':'0','support_bottom_z_distance':'0','support_interface_top_layers':'2','support_interface_bottom_layers':'2',
              'support_interface_spacing':'0','support_bottom_interface_spacing':'0','enable_prime_tower':'1',
              'flush_into_objects':'0','flush_into_support':'0','flush_into_infill':'0','flush_volumes_matrix':['0','800','800','0']}
    for key,value in expected.items():assert settings.get(key)==value,(key,settings.get(key),value)
    baseline=json.loads((HERE/'presets/printer.json').read_text())
    for key in ('machine_start_gcode','machine_end_gcode','change_filament_gcode','time_lapse_gcode','layer_change_gcode'):
        assert settings[key]==baseline[key],key
    slice_info=ET.fromstring(contents['Metadata/slice_info.config'])
    assert slice_info.find("plate/metadata[@key='outside']").get('value')=='false'
    totals,layers,bounds=deposited_paths(file)
    def contacts(p,lo,hi,filament=1):
        x,y=p['x'],p['y'];w,h=p['footprint_mm'];count=0
        for z,segments in layers.items():
            if not lo<=z<=hi:continue
            for feature,tool,x0,y0,x1,y1 in segments:
                if feature!='Support interface' or tool!=filament:continue
                if max(x0,x1)>=x-.25 and min(x0,x1)<=x+w+.25 and max(y0,y1)>=y-.25 and min(y0,y1)<=y+h+.25:count+=1
        return count
    below=[]
    for p in parts:
        if p['z']<=0:continue
        count=contacts(p,p['z']-.251,p['z']+.051)
        assert count>0,p['name']
        below.append({'part':p['name'],'base_z_mm':p['z'],'PETG_interface_segments_below':count})
    def top_face_contacts(p):
        # Stepped carriers have guide pins above their wall/ledge surfaces.
        # Test actual upward horizontal triangles, not only their global Z max.
        vertices,triangles=mesh(HERE/p['source']);vs=np.asarray(vertices)
        groups={}
        for tri in triangles:
            pts=vs[tri];normal=np.cross(pts[1]-pts[0],pts[2]-pts[0])
            if normal[2]<=0 or np.ptp(pts[:,2])>1e-5:continue
            if abs(normal[2])<1e-10:continue
            z=round(float(pts[:,2].mean())+p['z'],3)
            groups.setdefault(z,[]).append(Polygon(pts[:,:2]))
        found=[]
        for face_z,polys in groups.items():
            area=translate(unary_union(polys),xoff=p['x'],yoff=p['y']).buffer(.215)
            prepared=prep(area);count=0
            for height,segments in layers.items():
                if not face_z+.049<=height<=face_z+.251:continue
                for feature,tool,x0,y0,x1,y1 in segments:
                    if feature=='Support interface' and tool==1 and prepared.intersects(LineString([(x0,y0),(x1,y1)])):count+=1
            if count:found.append({'surface_z_mm':face_z,'PETG_interface_segments':count})
        return found
    for p in parts:
        if not p['column'].startswith('panel'):continue
        above=[q for q in parts if q['column']==p['column'] and q['z']>p['z']]
        if not above:continue
        q=min(above,key=lambda q:q['z']);ztop=p['z']+p['size_mm'][2]
        lower_faces=top_face_contacts(p)
        lower_count=sum(row['PETG_interface_segments'] for row in lower_faces)
        upper_count=contacts(q,q['z']-.251,q['z']+.051)
        assert lower_count>0 and upper_count>0,(p['name'],q['name'],lower_count,upper_count)
        adjacent.append({'lower':p['name'],'upper':q['name'],'gap_mm':q['z']-ztop,
                         'PETG_segments_on_lower_face':lower_count,'lower_actual_surface_contacts':lower_faces,
                         'PETG_segments_below_upper_face':upper_count})
    blank_contacts=[]
    for p in parts:
        if 'button_blank' not in p['name']:continue
        count=contacts(p,2.249,2.551)
        assert count>0,p['name']
        blank_contacts.append({'part':p['name'],'PETG_segments_below_curved_arms':count})
    audit_result=audit(file,5)
    (HERE/'review/bounds-audit.json').write_text(json.dumps(audit_result,indent=2)+'\n')
    assert not audit_result['failures'],audit_result['failures']
    # Native editable project without cached toolpaths; exact saved component transforms retained.
    project=dict(contents);pcfg=ET.fromstring(project['Metadata/model_settings.config'])
    for plate in pcfg.findall('plate'):
        for el in list(plate):
            if el.get('key')=='gcode_file':plate.remove(el)
    project['Metadata/model_settings.config']=ET.tostring(pcfg,encoding='utf-8',xml_declaration=True)
    relpath='Metadata/_rels/model_settings.config.rels'
    if relpath in project:
        rel=ET.fromstring(project[relpath])
        for el in list(rel):
            if '.gcode' in el.get('Target',''):rel.remove(el)
        project[relpath]=ET.tostring(rel,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(HERE/'reprint_stack_project.3mf','w',zipfile.ZIP_DEFLATED) as z:
        for name,data in project.items():
            if not name.endswith(('.gcode','.gcode.md5')) and name not in ('Metadata/slice_info.config','Metadata/filament_sequence.json'):z.writestr(name,data)
    for img in ('plate_1.png','top_1.png'):
        if 'Metadata/'+img in contents:(HERE/'review'/img).write_bytes(contents['Metadata/'+img])
    info=json.loads((HERE/'review/slice-result.json').read_text())['sliced_plates'][0]
    density={'PLA':1.26,'PETG':1.27}
    mass=lambda feature,mat:totals.get((feature,0 if mat=='PLA' else 1),0)*density[mat]/1000
    main={mat:info['filaments'][i]['main_used_g'] for i,mat in enumerate(density)}
    total={mat:info['filaments'][i]['total_used_g'] for i,mat in enumerate(density)}
    tower={mat:mass('Prime tower',mat) for mat in density}
    scaffold=mass('Support','PLA')+mass('Support transition','PLA')
    categories=[{'category':'Models and adhesion brim','PLA_g':main['PLA']-scaffold,'PETG_g':0},
                {'category':'Support scaffold and transition','PLA_g':scaffold,'PETG_g':0},
                {'category':'Release interfaces','PLA_g':0,'PETG_g':main['PETG']},
                {'category':'Prime tower','PLA_g':tower['PLA'],'PETG_g':tower['PETG']},
                {'category':'Purge and material-change waste (inferred)','PLA_g':total['PLA']-main['PLA']-tower['PLA'],'PETG_g':total['PETG']-main['PETG']-tower['PETG']}]
    for mat in density:assert abs(sum(row[mat+'_g'] for row in categories)-total[mat])<.001
    material={'estimated_hours':info['total_predication']/3600,'AMS_changes':info['filament_change_times'],
              'totals_g':total,'categories':categories,'method':'Slicer totals; feature extrusion volumes partition supports/tower. Purge is total minus main minus tower, including rounding residuals. No weighed consumption.'}
    (HERE/'review/material-breakdown.json').write_text(json.dumps(material,indent=2)+'\n')
    result={'part_count':20,'failures':[],'source_hashes_match':True,'native_position_max_error_mm':max_error,
            'minimum_vertical_bbox_gap_mm':min(gaps),'height_mm':m['height_mm'],'source_xy_min_mm':a[:,:2].min(axis=0).tolist(),'source_xy_max_mm':b[:,:2].max(axis=0).tolist(),
            'verified_settings':expected,'stock_A1_service_templates_unchanged':True,'elevated_part_contacts':below,
            'interfaces_on_both_faces_of_panel_gaps':adjacent,'blank_arm_support_contacts':blank_contacts,
            'Gcode_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
            'limits':'Sampled interface path presence in footprints does not prove complete underside coverage or physical release. Prototype PLA mock only; no printer contacted.'}
    (HERE/'review/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'parts':20,'position_error_mm':max_error,'hours':material['estimated_hours'],'material_g':total,'failures':[]},indent=2))

if __name__=='__main__':main()
