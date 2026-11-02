"""Check execution, finite measurements and repeatability of nominal retest."""
import json, math
from pathlib import Path
root=Path(__file__).resolve().parent
folder=root/'results/static-retest-2026-10-07'
current=json.loads((folder/'report.json').read_text())
previous=json.loads((root/'results/static-integration-2026-10-07/report.json').read_text())
old={r['case']:r for r in previous['results']}
checks=[]
for r in current['results']:
    checks.append({'case':r['case'],'check':'execution and measurements','pass':r['execution']=='ok' and r['returncode']==0 and not r['missing_measurements']})
    for name,value in r['measurements'].items():
        prior=old[r['case']]['measurements'][name]
        checks.append({'case':r['case'],'measurement':name,'check':'finite and repeatable','pass':math.isfinite(value) and math.isclose(value,prior,rel_tol=1e-6,abs_tol=1e-9)})
    if r['case'].startswith('vendor_cap') or r['case'] in ['vendor_bypass_impedance','vendor_kemet_bank']:
        checks.append({'case':r['case'],'check':'positive passive impedance','pass':all(v>0 for v in r['measurements'].values())})
result={'qualification':'nominal execution/repeatability only; hardware acceptance pending','checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks)}
(folder/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'benches':len(current['results']),'passed':result['passed'],'failed':result['failed']}))
assert not result['failed']
