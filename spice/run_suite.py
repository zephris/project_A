"""Stdlib-only smoke runner. Execution success is never board qualification."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ngspice', help='Path to standalone ngspice executable')
    parser.add_argument('--shared-library', help='Path to KiCad ngspice DLL (separate worker per run)')
    parser.add_argument('--case', action='append', help='Case ID; repeat to select several')
    parser.add_argument('--sweep', action='store_true', help='Run Cartesian parameter corners')
    parser.add_argument('--check', action='store_true', help='Check files/source provenance without simulation')
    parser.add_argument('--timeout', type=float, default=60)
    parser.add_argument('--output-dir', default='results', help='Results directory relative to spice/ or absolute')
    args = parser.parse_args()
    suite = json.loads((ROOT / 'suite.json').read_text())
    cases = [c for c in suite['cases'] if not args.case or c['id'] in args.case]
    if args.case and set(args.case) - {c['id'] for c in cases}:
        parser.error('Unknown case ID')
    stale = []
    for name, expected in suite['source_hashes_lf'].items():
        digest = hashlib.sha256((ROOT.parent / name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        if digest != expected:
            stale.append(name)
    for case in cases:
        folder = ROOT / case['path']
        for name in ['circuit.inc', 'bench.cir', case['id'] + '.kicad_sch', case['id'] + '.kicad_pro']:
            if not (folder / name).is_file():
                parser.error(f'Missing {folder / name}')
        text = (folder / 'circuit.inc').read_text()
        for asset, expected_hash in case.get('asset_hashes', {}).items():
            source = ROOT / case['assets'][asset]
            if hashlib.sha256((folder/asset).read_bytes()).hexdigest() != expected_hash or hashlib.sha256(source.read_bytes()).hexdigest() != expected_hash:
                parser.error(f'Model changed: {asset}; review and regenerate the suite')
        for key in case['sweeps']:
            if not re.search(rf'\b{re.escape(key)}\s*=', text):
                parser.error(f'Undefined sweep parameter {key}')
    if stale:
        print('Source changed; review bench inputs before updating provenance: ' + ', '.join(stale))
        return 1
    if args.check:
        print(f'{len(cases)} bench file sets and source hashes checked; simulation/acceptance pending.')
        return 0
    simulator = args.ngspice or shutil.which('ngspice')
    command = [sys.executable, str(ROOT / 'shared_ngspice.py'), '--dll', args.shared_library] if args.shared_library else [simulator] if simulator else None
    report = {'qualification': 'pending', 'source_hashes_lf': suite['source_hashes_lf'], 'results': []}
    output = ROOT / args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    if not command:
        report['results'] = [{'case': c['id'], 'execution': 'skipped', 'reason': 'Standalone ngspice not found', 'acceptance': 'pending'} for c in cases]
    else:
        version = subprocess.run(command + ['--version'], capture_output=True, text=True, timeout=args.timeout)
        report['simulator_version'] = version.stdout + version.stderr
        for case in cases:
            keys = list(case['sweeps']) if args.sweep else []
            corners = itertools.product(*(case['sweeps'][k] for k in keys)) if keys else [()]
            for i, corner in enumerate(corners):
                folder = output / case['id'] / f'{i:03d}'
                folder.mkdir(parents=True, exist_ok=True)
                circuit = (ROOT / case['path'] / 'circuit.inc').read_text()
                parameters = dict(zip(keys, corner))
                for key, value in parameters.items():
                    circuit = re.sub(rf'(\b{re.escape(key)}\s*=)\S+', lambda m: m[1] + value, circuit)
                (folder / 'circuit.inc').write_text(circuit)
                shutil.copyfile(ROOT / case['path'] / 'bench.cir', folder / 'bench.cir')
                for asset in case.get('assets', {}):
                    shutil.copyfile(ROOT / case['path'] / asset, folder / asset)
                if case.get('spice_compatibility') == 'ps':
                    (folder / '.spiceinit').write_text('set ngbehavior=ps\n')
                result = {'case': case['id'], 'corner': i, 'parameters': parameters, 'acceptance': 'pending'}
                try:
                    extra = ['--pspice'] if args.shared_library and case.get('spice_compatibility') == 'ps' else []
                    process = subprocess.run(command + extra + (['bench.cir'] if args.shared_library else ['-b', 'bench.cir']), cwd=folder, capture_output=True, text=True, timeout=args.timeout)
                    log = process.stdout + process.stderr
                    (folder / 'ngspice.log').write_text(log)
                    measures = {}
                    for name, value in re.findall(r'^\s*(\w+)\s*=\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)', log, re.M):
                        measures[name] = float(value)
                    expected = [line.split()[2] for line in case['measures']]
                    missing = [name for name in expected if name not in measures]
                    failed = bool(re.search(r'(?im)^\s*(?:fatal|error)\b|timestep too small|simulation interrupted', log))
                    result.update(execution='ok' if process.returncode == 0 and not missing and not failed else 'error', returncode=process.returncode, measurements=measures, missing_measurements=missing)
                except (OSError, subprocess.TimeoutExpired) as error:
                    result.update(execution='error', reason=str(error))
                report['results'].append(result)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 1 if any(r['execution'] == 'error' for r in report['results']) else 2 if any(r['execution'] == 'skipped' for r in report['results']) else 0

if __name__ == '__main__':
    sys.exit(main())
