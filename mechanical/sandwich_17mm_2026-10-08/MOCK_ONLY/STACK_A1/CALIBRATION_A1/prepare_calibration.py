"""Prepare local A1 flow tests; never contacts a printer or saves calibration.

Uses the installed Bambu Studio test meshes and its per-object flow recipe:
https://github.com/bambulab/BambuStudio/blob/master/src/slic3r/Utils/CalibUtils.cpp
The speeds are deliberately lower than that wizard's stock A1 settings.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
STACK = HERE.parent
sys.path.insert(0, str(STACK.parent / 'PRINT_A1'))
from prepare_prints import complete

NS = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('', NS)
T = lambda name: '{' + NS + '}' + name


def prepare(material, pass_number=1, baseline=None, slice_file=False):
    name = f'{material}_flow_coarse' if pass_number == 1 else f'{material}_flow_fine'
    source = Path(f'D:/Bambu Studio/resources/calib/filament_flow/flowrate-test-pass{pass_number}.3mf')
    with zipfile.ZipFile(source) as z:
        root = ET.fromstring(z.read('3D/3dmodel.model'))
    objects = root.findall(T('resources') + '/' + T('object'))
    points = [v for o in objects for v in o.findall('.//' + T('vertex'))]
    dx = 128 - (min(float(v.get('x')) for v in points) + max(float(v.get('x')) for v in points)) / 2
    dy = 128 - (min(float(v.get('y')) for v in points) + max(float(v.get('y')) for v in points)) / 2
    for v in points:
        v.set('x', f'{float(v.get("x")) + dx:.7f}')
        v.set('y', f'{float(v.get("y")) + dy:.7f}')
    ET.SubElement(root, T('metadata'), name='Application').text = 'BambuStudio-02.07.01.62'
    ET.SubElement(root, T('metadata'), name='BambuStudio:3mfVersion').text = '1'
    ET.SubElement(root, T('metadata'), name='Description').text = 'Unrun flow test. No calibration result has been selected.'
    cfg = ET.Element('config')
    rows = []
    for obj in objects:
        label = obj.get('name')
        modifier = int(label.removeprefix('flowrate_').replace('m', '-'))
        settings = {'name': label, 'extruder': '1', 'print_flow_ratio': f'{1 + modifier / 100:.5f}'}
        entry = ET.SubElement(cfg, 'object', id=obj.get('id'))
        for key, value in settings.items():
            ET.SubElement(entry, 'metadata', key=key, value=value)
        part = ET.SubElement(entry, 'part', id=obj.get('id'), subtype='normal_part')
        ET.SubElement(part, 'metadata', key='name', value=label)
        rows.append({'name': label, 'modifier_percent': modifier, 'object_flow_multiplier': 1 + modifier / 100})
    filament = json.loads((STACK / 'presets' / ('PLA.json' if material == 'PLA' else 'PETG_interface.json')).read_text())
    if baseline is not None:
        filament['filament_flow_ratio'] = [str(baseline)]
    baseline = float(filament['filament_flow_ratio'][0])
    filament['name'] = f'PHBox {material} UNCALIBRATED flow test @A1'
    filament['filament_settings_id'] = [filament['name']]
    # PETG now contacts the bed, unlike the elevated support interfaces.
    if material == 'PETG':
        filament['textured_plate_temp'] = ['70']
        filament['textured_plate_temp_initial_layer'] = ['70']
    process = complete('process', '0.20mm Standard @BBL A1')
    process.update({
        'name': 'PHBox A1 manual flow test 0.20', 'layer_height': '0.2',
        'initial_layer_print_height': '0.2', 'wall_loops': '3',
        'top_one_wall_type': 'topmost', 'top_area_threshold': '100%',
        'sparse_infill_density': '35%', 'bottom_shell_layers': '1',
        'bottom_shell_thickness': '0', 'top_shell_layers': '5', 'top_shell_thickness': '0',
        'detect_thin_wall': '1', 'sparse_infill_pattern': 'rectilinear',
        'top_surface_line_width': '0.48', 'internal_solid_infill_line_width': '0.48',
        'top_surface_pattern': 'monotonic', 'infill_direction': '45', 'ironing_type': 'no ironing',
        'internal_solid_infill_speed': ['60'], 'top_surface_speed': ['60'],
        'outer_wall_speed': ['60'], 'inner_wall_speed': ['100'],
        'initial_layer_speed': ['30'], 'initial_layer_infill_speed': ['40'],
        'enable_support': '0', 'enable_prime_tower': '0', 'brim_type': 'no_brim',
        'print_sequence': 'by layer', 'reduce_crossing_wall': '1',
    })
    presets = HERE / 'presets'
    presets.mkdir(exist_ok=True)
    printer_path = presets / 'printer.json'
    process_path = presets / 'flow_test.json'
    filament_path = presets / f'{material}_pass{pass_number}.json'
    for path, data in ((printer_path, complete('machine', 'Bambu Lab A1 0.4 nozzle')), (process_path, process), (filament_path, filament)):
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    # Reuse the installed version's known native settings schema. Replace the
    # process and both former filament entries with one calibration material.
    with zipfile.ZipFile(STACK / 'stacked_kit_inset_project.3mf') as z:
        project = json.loads(z.read('Metadata/project_settings.config'))
    for data in (complete('machine', 'Bambu Lab A1 0.4 nozzle'), process, filament):
        for key, value in data.items():
            if key in project and key not in ('name', 'version', 'from', 'type', 'setting_id', 'instantiation'):
                project[key] = value
    project.update(name='project_settings', print_settings_id=process['name'],
                   filament_settings_id=[filament['name']], filament_ids=[filament['filament_id']],
                   filament_colour=['#3E84B5' if material == 'PLA' else '#31AD48'],
                   filament_self_index=['1'], filament_map=['1'], curr_bed_type='Textured PEI Plate',
                   print_flow_ratio='1', enable_wrapping_detection='0',
                   support_filament='0', support_interface_filament='0',
                   top_solid_infill_flow_ratio=['1'], flush_volumes_matrix=['0'], flush_volumes_vector=['0'])
    for key in ('filament_change_length_nc', 'filament_dev_ams_drying_ams_limitations', 'first_x_layer_fan_speed'):
        if isinstance(project.get(key), list):
            project[key] = project[key][:1]
    seed = HERE / f'{name}.3mf'
    with zipfile.ZipFile(source) as z, zipfile.ZipFile(seed, 'w', zipfile.ZIP_DEFLATED) as out:
        for item in z.infolist():
            if item.filename in ('Metadata/thumbnail.png', '_rels/.rels'):
                continue  # Do not keep a thumbnail at the old placement.
            data = ET.tostring(root, encoding='utf-8', xml_declaration=True) if item.filename == '3D/3dmodel.model' else z.read(item.filename)
            out.writestr(item.filename, data)
        out.writestr('_rels/.rels', '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        out.writestr('Metadata/model_settings.config', ET.tostring(cfg, encoding='utf-8', xml_declaration=True))
        out.writestr('Metadata/project_settings.config', json.dumps(project, indent=2))
    report = {'status': 'editable_project_prepared_not_sliced_or_printed', 'printer': 'Bambu Lab A1', 'nozzle_mm': 0.4,
              'material': material, 'pass': pass_number, 'baseline_flow_ratio': baseline,
              'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'patches': rows, 'physical_calibration_applied': False,
              'import_visual_check_required': True}
    with zipfile.ZipFile(seed) as z:
        readback = ET.fromstring(z.read('Metadata/model_settings.config'))
        values = [{m.get('key'): m.get('value') for m in o.findall('metadata')} for o in readback.findall('object')]
        assert sorted((v['name'], float(v['print_flow_ratio'])) for v in values) == sorted((r['name'], r['object_flow_multiplier']) for r in rows)
        assert len(values) == (9 if pass_number == 1 else 10)
        assert max(float(v.get('z')) for v in points) == 1.4
        assert all(0 < float(v.get(k)) < 256 for v in points for k in ('x', 'y'))
    report['file_content_checks_passed'] = ['patch count', 'distinct flow modifiers', 'bed bounds', '1.4 mm height']
    (HERE / f'{name}.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    if not slice_file:
        print(json.dumps({'file': seed.name, 'patches': len(rows), 'base_flow': baseline, 'sliced': False}))
        return
    job = HERE / 'working' / name
    job.mkdir(parents=True, exist_ok=True)
    args = ['D:/Bambu Studio/bambu-studio.exe', '--load-settings', str(printer_path) + ';' + str(process_path),
            '--load-filaments', str(filament_path), '--curr-bed-type', 'Textured PEI Plate',
            '--arrange', '0', '--slice', '0', '--debug', '2', '--outputdir', str(job), '--export-3mf', 'sliced.3mf', str(seed)]
    result = subprocess.run(args, cwd='D:/Bambu Studio', capture_output=True, text=True)
    (job / 'cli.log').write_text(result.stdout + result.stderr, encoding='utf-8')
    if not (job / 'result.json').exists():
        raise RuntimeError(f'Slicer exited {result.returncode} without a result; no printable calibration file was produced.')
    receipt = json.loads((job / 'result.json').read_text())
    if result.returncode or receipt.get('return_code') != 0:
        raise RuntimeError(f'Slice failed; inspect {job / "cli.log"}')
    target = HERE / f'{name}.gcode.3mf'
    shutil.copyfile(job / 'sliced.3mf', target)
    with zipfile.ZipFile(target) as z:
        saved = ET.fromstring(z.read('Metadata/model_settings.config'))
        actual = []
        for obj in saved.findall('object'):
            vals = {v.get('key'): v.get('value') for v in obj.findall('metadata') if v.get('key')}
            actual.append((vals.get('name'), float(vals['print_flow_ratio'])))
        assert sorted(actual) == sorted((r['name'], r['object_flow_multiplier']) for r in rows), actual
        # Editable native project, with all settings but no stale slice previews.
        with zipfile.ZipFile(HERE / f'{name}.3mf', 'w', zipfile.ZIP_DEFLATED) as out:
            for f in z.infolist():
                if any(s in f.filename.lower() for s in ('.gcode', '.md5', 'slice_info', 'plate_')):
                    continue
                out.writestr(f.filename, z.read(f.filename))
    report = {'status': 'prepared_not_printed', 'printer': 'Bambu Lab A1', 'nozzle_mm': 0.4,
              'material': material, 'pass': pass_number, 'baseline_flow_ratio': baseline,
              'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'patches': rows, 'slice': receipt, 'file_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
              'per_object_flow_settings_verified': True, 'physical_calibration_applied': False}
    (HERE / f'{name}.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'file': target.name, 'patches': len(rows), 'base_flow': baseline,
                      'object_modifiers': actual, 'slice_exit': result.returncode}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--material', choices=['PLA', 'PETG', 'both'], default='both')
    parser.add_argument('--fine-baseline', type=float, help='Measured coarse result; never guessed.')
    parser.add_argument('--slice', action='store_true', help='Try the local slicer; currently crashes with 0xC0000005.')
    args = parser.parse_args()
    if args.fine_baseline is not None and (args.material == 'both' or not 0 < args.fine_baseline < 2):
        parser.error('Fine pass requires one material and a valid measured coarse flow ratio.')
    for material in (['PLA', 'PETG'] if args.material == 'both' else [args.material]):
        prepare(material, 2 if args.fine_baseline is not None else 1, args.fine_baseline, args.slice)
