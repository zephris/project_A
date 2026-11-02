from pathlib import Path
import subprocess,sys,json,re
r=Path.cwd();o=r/'spice/models/qualification_2026-10-07';o.mkdir(exist_ok=True)
worker=(r/'spice/shared_ngspice.py').read_text()
extra="""import tempfile, shutil
    code_dir = Path(tempfile.mkdtemp(prefix='phbox_ngspice_'))
    assert ' ' not in str(code_dir), str(code_dir)
    for name in ['analog', 'table', 'digital', 'spice2poly', 'tlines', 'xtradev', 'xtraevt']:
        source_cm = Path('D:/Program Files/lib/ngspice') / (name + '.cm')
        destination = code_dir / source_cm.name
        shutil.copy2(source_cm, destination)
        library.ngSpice_Command(('codemodel ' + destination.as_posix()).encode())
    library.ngSpice_Command(b'set ngbehavior=ps')
    source = library.ngSpice_Command"""
worker=worker.replace('source = library.ngSpice_Command',extra)
(o/'pspice_worker.py').write_text(worker)
models=r/'spice/models/vendor'
cases={
'TLV73333P':('TLV73333P/tlv73333p_trans.lib','V1 vin 0 PWL(0 0 100u 5)\nVen en 0 PWL(0 0 200u 0 201u 3.3)\nXreg en vin vout 0 TLV73333P_TRANS\nCout vout 0 1u\nRload vout 0 165\n.tran 1u 5m\n.meas tran output_final FIND v(vout) AT=4.9m'),
'TPS2553':('TPS2553/SLVM425A/TPS2553_PSPICE_TRANS/tps2553_trans.lib','V1 vin 0 PWL(0 0 100u 5)\nVen en 0 PWL(0 0 1m 0 1.001m 3.3)\nXswitch vin 0 en 0 fault ilim vout TPS2553_TRANS\nRilim ilim 0 200k\nRfault vin fault 10k\nCout vout 0 200u\nRload vout 0 100\n.tran 5u 30m\n.meas tran output_final FIND v(vout) AT=29m'),
'SN74LV1T34':('SN74LV1T34_SPICE/SN74LV1T34.cir','V1 vcc 0 5\nVin input 0 PULSE(0 3.3 1u 10n 10n 2u 4u)\nXbuf output input vcc 0 SN74LV1T34\nCload output 0 15p\nRload output 0 1Meg\n.tran 1n 10u\n.meas tran output_high FIND v(output) AT=2u\n.meas tran output_low FIND v(output) AT=4u')}
results=[]
for name,(path,body) in cases.items():
 f=o/name;f.mkdir(exist_ok=True);deck=f/'bench.cir';deck.write_text(f'{name} isolated compatibility smoke check\n.include "{(models/path).as_posix()}"\n'+body+'\n.end\n')
 try:
  p=subprocess.run([sys.executable,str(o/'pspice_worker.py'),'--dll','D:/Program Files/bin/ngspice.dll',str(deck)],cwd=f,capture_output=True,text=True,timeout=50)
  log=p.stdout+p.stderr;(f/'ngspice.log').write_text(log,encoding='utf-8');meas=dict(re.findall(r'^\s*(output_\w+)\s*=\s*([-+\deE.]+)',log,re.M));errors=bool(re.search(r'(?im)^\s*(?:fatal|error)\b|timestep too small|unknown subckt|simulation interrupted',log));results.append({'part':name,'returncode':p.returncode,'measurements':meas,'smoke_execution_ok':p.returncode==0 and bool(meas) and not errors,'qualification':'not qualified; only isolated compatibility and nominal output check'})
 except Exception as e:results.append({'part':name,'smoke_execution_ok':False,'error':str(e)})
 print(json.dumps(results[-1]),flush=True)
(o/'report.json').write_text(json.dumps(results,indent=2))




