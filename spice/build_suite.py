"""Generate isolated KiCad 10 simulator sheets and ngspice batch decks."""
import hashlib
import json
from pathlib import Path
import uuid
import shutil

ROOT = Path(__file__).resolve().parent
BOARD = ROOT.parent

def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def uid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "phbox-spice/" + name))

def quote(text):
    return json.dumps(text, ensure_ascii=False)

def sheet(name, description, analysis):
    texts = [
        (25, 25, "PHBox: " + name + "\n" + description),
        (25, 55, "BOARD QUALIFICATION PENDING\nCircuit and model files are local to this bench.\nVendor benches require PSpice compatibility mode.\nLoads/parasitics include assumptions; see suite.json."),
        (25, 90, '.include "circuit.inc"'),
        (25, 105, analysis),
    ]
    body = "\n".join(
        f'(text {quote(text)} (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "{uid(name + str(i))}"))'
        for i, (x, y, text) in enumerate(texts)
    )
    return f'''(kicad_sch (version 20250114) (generator "eeschema")
 (generator_version "10.0") (uuid "{uid(name)}") (paper "A4")
 (lib_symbols)
 {body}
 (embedded_fonts no)
)
'''

HOST = '''* U7 abstraction, NOT a TPS2553 vendor model.
* Positive current flows IN -> OUT. No reverse blocking, UVLO, thermal
* shutdown, real soft-start or FAULT deglitch dynamics are modeled.
.param supply=5 cable_r=0.3 ilimit=0.137 cout=200u en_delay=5m
.param ron=0.1 cap_esr=0.035 load_a=0.060
Vsource upstream 0 PWL(0 0 1m {supply})
Rcable upstream vin {cable_r}
Cinput vin 0 100n
Ven en 0 PULSE(0 3.3 {en_delay} 1u 1u 1 2)
Bswitch vin switched I={(v(en)>1.5) ? min(ilimit,max(0,(v(vin)-v(host))/ron)) : 0}
Vsense switched host 0
Rcap host capnode {cap_esr}
Cbank capnode 0 {cout}
Cbypass host 0 100n
Rbleed host 0 100k
* FAULT is an instantaneous synthetic indicator, not a device prediction.
Bfault fault 0 V={(v(en)>1.5) ? ((v(vin)-v(host)>ilimit*ron) ? 0 : 3.3) : 3.3}
'''

CASES = [
    dict(id="usb2_enable", description="R16 weak-pull-up enable compatibility: reset, configured host, pull-up release",
         circuit='''* Datasheet-bound GPIO/TPS2553 leakage envelope; not firmware execution.
* RPU 32..86k at IOVDD=3.3V. 3.2..3.4V rail is a design envelope.
* R16 total +/-2% allowance includes 1% initial tolerance and temperature drift.
* +/-1.5u combines RP2350 specified 1u input leakage and U7 0.5u EN leakage.
* Runtime release bounds apply to A3/A4; A2 E9 with input enabled is NOT modeled.
* At POR/RUN reset RP2350 input enable is clear, per E9 description.
.param rail_v=3.3 rpu=86k rpd=220k leak_a=1.5u
Vrail rail 0 {rail_v}
R16 en 0 {rpd}
Bileak en 0 I={(leak_a>0) ? leak_a*max(0,min(1,v(en)/0.05)) : leak_a}
Cpad en 0 20p
Bpull en 0 I={(time>5m && time<15m) ? (v(en)-v(rail))/rpu : 0}
* Original 10k divider for regression comparison, enabled throughout.
Roldpull rail old_en {rpu}
Roldpd old_en 0 10k
Boldleak old_en 0 I={(leak_a>0) ? leak_a*max(0,min(1,v(old_en)/0.05)) : leak_a}
''', analysis='.tran 1u 20m', measures=[
             '.meas tran en_reset_max MAX v(en) FROM=0 TO=4m',
             '.meas tran en_enabled_min MIN v(en) FROM=6m TO=14m',
             '.meas tran en_release_max MAX v(en) FROM=16m TO=20m',
             '.meas tran old_en_max MAX v(old_en) FROM=6m TO=14m'],
         sweeps={"rail_v": ["3.2", "3.4"], "rpu": ["32k", "86k"], "rpd": ["215.6k", "224.4k"], "leak_a": ["-1.5u", "1.5u"]},
         signals=["v(en)", "v(old_en)"],
         todo="Require EN enabled >=2.0V and reset/release <=0.66V for specified-leakage silicon; inspect A2 E9 separately. Pull capacitance is illustrative. Stock firmware never releases pull-up during suspend; this release test is an electrical envelope only."),
    dict(id="usb2_startup", description="U7, C42, output bank and C44: enable into capacitive/dongle load",
         circuit=HOST + '* Load tapers below 4V; no current drawn from an unpowered rail.\nBload host 0 I={load_a*max(0,min(1,v(host)/4))}\n', analysis='.tran 10u 100m',
         measures=['.meas tran host_final FIND v(host) AT=95m',
                   '.meas tran source_peak MAX i(Vsense) FROM=0 TO=100m',
                   '.meas tran rise_4v WHEN v(host)=4 RISE=1'],
         sweeps={"cout": ["160u", "200u", "240u"], "ilimit": ["0.115", "0.137", "0.159"], "load_a": ["0", "0.060", "0.100"]},
         signals=["v(vin)", "v(host)", "v(en)", "v(fault)", "i(Vsense)"],
         todo="Import TI unencrypted transient model; verify pin mapping, reference circuit and ngspice compatibility; add real EN/FAULT timing and dongle startup load."),
    dict(id="usb2_overload", description="U7: load above the limit, removal and recovery",
         circuit=HOST + 'Vdemand demand 0 PWL(0 0 10m 0 10.01m 0.060 40m 0.060 40.01m 0.250 65m 0.250 65.01m 0.060)\nBload host 0 I={v(demand)*max(0,min(1,v(host)/4))}\n',
         analysis='.tran 10u 100m', measures=[
             '.meas tran host_fault_min MIN v(host) FROM=40m TO=65m',
             '.meas tran host_recovered FIND v(host) AT=95m',
             '.meas tran switch_peak MAX i(Vsense) FROM=40m TO=65m'],
         sweeps={"ilimit": ["0.115", "0.137", "0.159"], "cout": ["160u", "240u"]},
         signals=["v(host)", "v(fault)", "i(Vsense)"],
         todo="Replace abstraction with validated U7 model; define fault deglitch, recovery, thermal shutdown and firmware response criteria."),
    dict(id="shared_5v", description="Cable/source impedance, RGB pulse load and host hot-plug demand",
         circuit='''* Load envelopes are assumptions, not measured firmware behavior.
.param supply=5 cable_r=0.3 cable_l=1u bulk=10u bulk_esr=0.1
.param base_a=0.100 rgb_a=0.189 host_a=0.100
Vsource upstream 0 {supply}
Rcable upstream cable {cable_r}
Lcable cable rail5 {cable_l}
Rbulk rail5 capnode {bulk_esr}
Cbulk capnode 0 {bulk}
Ibase rail5 0 {base_a}
Irgb rail5 0 PULSE(0 {rgb_a} 2m 1u 1u 500u 1m)
Ihost rail5 0 PULSE(0 {host_a} 10m 10u 10u 10m 100m)
''', analysis='.tran 1u 30m', measures=[
             '.meas tran rail_min MIN v(rail5) FROM=2m TO=30m',
             '.meas tran source_peak MAX par(\'-i(Vsource)\') FROM=2m TO=30m',
             '.meas tran source_avg AVG par(\'-i(Vsource)\') FROM=2m TO=30m'],
         sweeps={"cable_r": ["0.1", "0.3", "0.6"], "rgb_a": ["0.189", "0.378"], "supply": ["4.75", "5"]},
         signals=["v(rail5)", "i(Vsource)"],
         todo="Extract actual effective board capacitance; measure RGB PWM, source/cable/fuse impedance and host inrush; define USB power declaration and voltage limits."),
    dict(id="rail_3v3", description="U2 TLV73333 and OLED/MCU load-step planning envelope",
         circuit='''* Ideal rail with finite resistance; does NOT simulate LDO startup/dropout/stability.
.param rail_v=3.3 rail_r=0.1 cout=1u cap_esr=0.05 base_a=0.020 step_a=0.050
Videal ideal 0 PWL(0 0 1m {rail_v})
Rrail ideal rail3 {rail_r}
Resr rail3 capnode {cap_esr}
Cout capnode 0 {cout}
Ibase rail3 0 {base_a}
Istep rail3 0 PULSE(0 {step_a} 5m 1u 1u 5m 20m)
''', analysis='.tran 1u 20m', measures=[
             '.meas tran rail_min MIN v(rail3) FROM=4m TO=15m',
             '.meas tran rail_max MAX v(rail3) FROM=4m TO=15m'],
         sweeps={"cout": ["0.5u", "1u", "2u"], "step_a": ["0.025", "0.050", "0.100"]},
         signals=["v(rail3)", "i(Videal)"],
         todo="Add validated TLV73333 model, input rail and actual input/output capacitor network; include RP2350/OLED loads. Separate core converter bench remains TODO."),
    dict(id="bypass_impedance", description="Single bypass branch AC impedance with assumed ESR/ESL",
         circuit='''* One representative 100n branch, not extracted whole-board PDN.
.param c_eff=100n esr=0.05 esl=1n
Itest 0 pdn AC 1
Rleak pdn 0 1G
Lesl pdn n1 {esl}
Resr n1 n2 {esr}
Ceff n2 0 {c_eff}
''', analysis='.ac dec 100 1k 100Meg', measures=[
             '.meas ac z_1meg FIND vm(pdn) AT=1Meg',
             '.meas ac z_min MIN vm(pdn)'],
         sweeps={"c_eff": ["50n", "100n"], "esl": ["0.5n", "2n"]},
         signals=["v(pdn)"],
         todo="Add measured/bias-adjusted capacitor banks and trace/via parasitics. USB/RGB driver/receiver ringing needs validated IBIS/SPICE models and a separate bench; this does not test data compliance."),
]

def main():
    from vendor_cases import integrate
    integrate(CASES)
    from static_cases import integrate as integrate_static
    integrate_static(CASES)
    manifest = {"schema_version": 1, "qualification": "pending", "cases": []}
    for case in CASES:
        name = case['id']
        folder = ROOT / 'benches' / name
        put(folder / 'circuit.inc', case['circuit'])
        for target, source in case.get('assets', {}).items():
            shutil.copyfile(ROOT / source, folder / target)
        case['asset_hashes'] = {target: hashlib.sha256((ROOT/source).read_bytes()).hexdigest() for target, source in case.get('assets', {}).items()}
        commands = case['analysis'] + '\n' + '\n'.join(case['measures'])
        put(folder / 'bench.cir', f'PHBox {name} planning model\n.include "circuit.inc"\n{commands}\n.end\n')
        put(folder / f'{name}.kicad_sch', sheet(name, case['description'], commands))
        put(folder / f'{name}.kicad_pro', json.dumps({"meta": {"filename": name + '.kicad_pro', "version": 1}}, indent=2) + '\n')
        manifest['cases'].append({k: v for k, v in case.items() if k != 'circuit'} | {
            "model_fidelity": case.get('model_fidelity', 'planning abstraction'), "acceptance_limits": None,
            "acceptance_status": "pending", "path": f"benches/{name}"})
    manifest['source_hashes_lf'] = {
        name: hashlib.sha256((BOARD / name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        for name in ['Flatbox-rev8.kicad_sch', 'Flatbox-rev8.kicad_pcb']
    }
    put(ROOT / 'suite.json', json.dumps(manifest, indent=2) + '\n')
    print(f"Generated {len(CASES)} isolated benches under {ROOT}")

if __name__ == '__main__':
    main()
