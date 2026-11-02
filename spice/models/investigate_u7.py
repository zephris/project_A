from pathlib import Path
import subprocess,sys,json,re
r=Path.cwd();base=r/'spice/models/qualification_2026-10-07/TPS2553/bench.cir';out=r/'spice/models/u7_investigation_2026-10-07';out.mkdir(exist_ok=True)
body=base.read_text().replace('.end\n','')
nodes=['vin','en','vout','fault','ilim','xswitch.powerok','xswitch.u1_vccok','xswitch.u1_enok','xswitch.u2_gate','xswitch.gate_off','xswitch.ilim_int','xswitch.u1_n16726884','xswitch.u1_n16726205']
for i,n in enumerate(nodes):body+=f'\n.meas tran debug_{i} FIND v({n}) AT=29m'
body+='\n.end\n';deck=out/'debug.cir';deck.write_text(body)
p=subprocess.run([sys.executable,str(r/'spice/models/qualification_2026-10-07/pspice_worker.py'),'--dll','D:/Program Files/bin/ngspice.dll',str(deck)],cwd=out,capture_output=True,text=True,timeout=50);log=p.stdout+p.stderr;(out/'debug.log').write_text(log)
meas=dict(re.findall(r'^\s*(debug_\d+)\s*=\s*([-+\deE.]+)',log,re.M));print({n:meas.get('debug_'+str(i)) for i,n in enumerate(nodes)})
