from pathlib import Path
import hashlib, json, re, sys
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'stage2_work/display_2026-10-05'))
from revise_display import forms
pcb=(root/'Flatbox-rev8.kicad_pcb').read_text()
fp=next(f for _,_,f in forms(pcb) if f.startswith('(footprint') and '(property "Reference" "C41"' in f)
assert 'C_0603_1608Metric' in fp
print(fp[:650])
report=json.loads((root/'spice/results/static-integration-2026-10-07/report.json').read_text())
assert len(report['results'])==14
assert all(r['execution']=='ok' and not r['missing_measurements'] for r in report['results'])
files=list((root/'spice/models/vendor/Samsung').glob('*DC0V*'))
files.append(root/'spice/models/adapters/T520B107M010ATE070_5V_25C_100kHz.lib')
record={'date':'2026-10-07','qualification':'execution verified; bias/temperature/hardware qualification pending',
 'models':[{'file':str(p.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
 'C41_candidate':{'MPN':'CL10B105KA8NNNC','LCSC':'C29936','manufacturer':'Samsung Electro-Mechanics',
 'value':'1uF/25V/X7R/10%','footprint':'Capacitor_SMD:C_0603_1608Metric','nets':['+3V3','GND'],
 'source':'https://jlcpcb.com/partdetail/30690-CL10B105KA8NNNC/C29936',
 'status':'Selected candidate; PCB/schematic metadata and manufacturing packages not changed'},
 'execution_count':14,'new_results':[r for r in report['results'] if r['case'] in ['vendor_cap_4u7','vendor_cap_1u','vendor_cap_c41','vendor_kemet_bank']]}
(root/'spice/models/static-integration-2026-10-07.json').write_text(json.dumps(record,indent=2)+'\n')
print('Verified 14 nominal runs; recorded model hashes and C41 candidate.')
