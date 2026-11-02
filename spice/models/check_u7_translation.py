"""Compare the original and compatibility-copy XNOR truth tables."""
from pathlib import Path
import subprocess, sys, re, json
root=Path(__file__).resolve().parents[1]
out=root/'models/u7_investigation_2026-10-07'
models={'original':root/'models/vendor/TPS2553/SLVM425A/TPS2553_PSPICE_TRANS/tps2553_trans.lib','adapted':root/'models/adapters/TPS2553_TRANS_ngspice.lib'}
report={}
for label,model in models.items():
    deck=f'U7 {label} XNOR truth table\n.include "{model.as_posix()}"\n'
    for i,(a,b) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
        deck+=f'Va{i} a{i} 0 {a}\nVb{i} b{i} 0 {b}\nX{i} a{i} b{i} y{i} XNOR2_BASIC_GEN\n'
    deck+='.tran 1n 10n\n'+''.join(f'.meas tran y{i} FIND v(y{i}) AT=9n\n' for i in range(4))+'.end\n'
    target=out/f'xnor_{label}.cir';target.write_text(deck)
    p=subprocess.run([sys.executable,str(root/'shared_ngspice.py'),'--dll','D:/Program Files/bin/ngspice.dll','--pspice',str(target)],capture_output=True,text=True,timeout=30)
    log=p.stdout+p.stderr;(out/f'xnor_{label}.log').write_text(log)
    values={k:float(v) for k,v in re.findall(r'^\s*(y\d)\s*=\s*([-+\deE.]+)',log,re.M)}
    report[label]=values
assert all(abs(report['adapted'][f'y{i}']-v)<1e-6 for i,v in enumerate([1,0,0,1]))
assert report['original']['y3']<0.1
(out/'xnor_comparison.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
