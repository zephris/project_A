"""Audit full XY arc envelopes and generated moves, separately from A1 service moves."""
from pathlib import Path
import argparse, collections, hashlib, json, math, re, zipfile

HERE = Path(__file__).resolve().parent
NUMBER = r'[-+]?(?:\d*\.\d+|\d+\.?\d*)'


def arc_points(start, end, values, clockwise):
    if 'I' not in values and 'J' not in values:
        if 'R' in values:
            raise ValueError('R-form arc requires an explicit center calculation')
        return [start, end]
    cx, cy = start[0] + values.get('I', 0), start[1] + values.get('J', 0)
    radius = math.hypot(start[0] - cx, start[1] - cy)
    a = math.atan2(start[1] - cy, start[0] - cx)
    b = math.atan2(end[1] - cy, end[0] - cx)
    sweep = ((a - b) if clockwise else (b - a)) % (2 * math.pi)
    if math.hypot(end[0] - start[0], end[1] - start[1]) < 1e-7:
        sweep = 2 * math.pi
    points = [start, end]
    for angle in (0, math.pi / 2, math.pi, 3 * math.pi / 2):
        delta = ((a - angle) if clockwise else (angle - a)) % (2 * math.pi)
        if delta <= sweep + 1e-8:
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return points


def audit(path, margin=0):
    with zipfile.ZipFile(path) as z:
        text = z.read('Metadata/plate_1.gcode').decode()
        project = json.loads(z.read('Metadata/project_settings.config'))
    bounds = collections.defaultdict(lambda: [math.inf, math.inf, -math.inf, -math.inf])
    x = y = zz = e = 0.0
    relative_e = True
    absolute_xyz = True
    feature = 'Custom'
    width = 0.6  # Conservative fallback before a WIDTH comment.
    arcs = collections.Counter()
    moves = collections.Counter()
    failures = []
    samples = collections.defaultdict(list)
    in_toolchange = False
    in_skippable = False
    last_move_kind = 'service'
    def add(key, points, pad=0):
        b = bounds[key]
        for px, py in points:
            b[0] = min(b[0], px - pad); b[1] = min(b[1], py - pad)
            b[2] = max(b[2], px + pad); b[3] = max(b[3], py + pad)
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.startswith('; CP TOOLCHANGE START'): in_toolchange = True
        elif line.startswith('; CP TOOLCHANGE END'): in_toolchange = False
        elif line.startswith('; SKIPPABLE_START'): in_skippable = True
        elif line.startswith('; SKIPPABLE_END'): in_skippable = False
        if line.startswith('; FEATURE:'):
            feature = line.split(':', 1)[1].strip()
        elif line.startswith('; WIDTH:'):
            width = float(line.split(':', 1)[1])
        code = line.split(';', 1)[0].strip()
        if not code:
            continue
        command = code.split()[0]
        vals = {k: float(v) for k, v in re.findall(r'([XYZEFIJKR])(' + NUMBER + ')', code)}
        if command == 'G90': absolute_xyz = True
        elif command == 'G91': absolute_xyz = False
        elif command == 'M82': relative_e = False
        elif command == 'M83': relative_e = True
        elif command == 'G92':
            x = vals.get('X', x); y = vals.get('Y', y); zz = vals.get('Z', zz); e = vals.get('E', e)
        elif command in ('G0', 'G1', 'G2', 'G3'):
            nx = vals.get('X', x) if absolute_xyz else x + vals.get('X', 0)
            ny = vals.get('Y', y) if absolute_xyz else y + vals.get('Y', 0)
            nz = vals.get('Z', zz) if absolute_xyz else zz + vals.get('Z', 0)
            de = vals.get('E', 0) if relative_e else vals.get('E', e) - e
            if not relative_e: e = vals.get('E', e)
            has_xy = 'X' in vals or 'Y' in vals or command in ('G2', 'G3')
            if has_xy:
                points = arc_points((x, y), (nx, ny), vals, command == 'G2') if command in ('G2', 'G3') else [(x, y), (nx, ny)]
                kind = 'service' if feature == 'Custom' or in_toolchange or in_skippable else 'generated'
                moves[kind] += 1
                if command in ('G2', 'G3'): arcs[kind] += 1
                if kind == 'service':
                    add('service_move_envelope', points)
                    if len(samples['service']) < 5 and any(v < 0 or v > 256 for v in (nx, ny)):
                        samples['service'].append({'line': lineno, 'command': code})
                else:
                    # Service-to-model entry starts outside the bed by design;
                    # its generated destination, not that known service origin,
                    # belongs to the deposited model/travel range.
                    add('generated_destinations', [(nx, ny)])
                    if not (margin - 1e-5 <= nx <= 256 - margin + 1e-5 and margin - 1e-5 <= ny <= 256 - margin + 1e-5):
                        if len(samples['generated_outside_margin']) < 12:
                            samples['generated_outside_margin'].append({'line': lineno, 'feature': feature, 'command': code})
                    if de > 0 and math.hypot(nx - x, ny - y) > 1e-7:
                        add('deposition_centerlines', points)
                        add('deposition_with_line_width', points, width / 2)
                        add('feature/' + feature, points, width / 2)
                    elif last_move_kind == 'service':
                        add('service_return_move_envelope', points)
                    elif 0 <= x <= 256 and 0 <= y <= 256:
                        add('generated_travel_envelope', points)
                        if any(not (margin - 1e-5 <= px <= 256 - margin + 1e-5 and margin - 1e-5 <= py <= 256 - margin + 1e-5) for px, py in points):
                            if len(samples['travel_arc_outside_margin']) < 12:
                                samples['travel_arc_outside_margin'].append({'line': lineno, 'feature': feature, 'command': code,
                                    'start': [x, y], 'extrema': points})
                last_move_kind = kind
            x, y, zz = nx, ny, nz
    for name in ('generated_destinations', 'deposition_with_line_width', 'generated_travel_envelope'):
        b = bounds.get(name)
        if b is None or min(b[:2]) < margin - 1e-4 or max(b[2:]) > 256 - margin + 1e-4:
            failures.append(f'{name} outside {margin}..{256-margin}: {b}')
    return {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'printer': project.get('printer_model'), 'printable_area': project.get('printable_area'),
            'print_sequence': project.get('print_sequence'), 'required_edge_margin_mm': margin,
            'xy_bounds_mm': {k: [round(v, 5) for v in b] for k, b in bounds.items()},
            'moves': dict(moves), 'arcs': dict(arcs), 'samples': dict(samples), 'failures': failures,
            'limits': 'Generated XY audit, including circular extrema and deposited line width. Custom startup/change/end movements are reported separately and must match the stock A1 profile; their off-bed service travel is not classified as a model-boundary violation. No physical machine motion or clearance observation.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=Path)
    parser.add_argument('--margin', type=float, default=0)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.file.resolve(), args.margin)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('file', 'moves', 'arcs', 'failures')}, indent=2))
    print(json.dumps({k: b for k, b in result['xy_bounds_mm'].items() if not k.startswith('feature/')}, indent=2))
    if result['failures']: raise SystemExit(1)
