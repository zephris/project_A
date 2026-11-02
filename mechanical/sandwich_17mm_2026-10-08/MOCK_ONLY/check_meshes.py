"""Verify saved binary STL dimensions/volumes; no print/strength qualification."""
from pathlib import Path
import json,struct,math
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'manifest.json').read_text())
results=[]
for entry in manifest['files']:
    path=HERE/entry['file'];raw=path.read_bytes()
    n=struct.unpack_from('<I',raw,80)[0]
    assert len(raw)==84+n*50,path
    low=[float('inf')]*3;high=[-float('inf')]*3;v=0
    for i in range(n):
        values=struct.unpack_from('<12fH',raw,84+i*50)
        a,b,c=[values[k:k+3] for k in (3,6,9)]
        for p in (a,b,c):
            assert all(math.isfinite(t) for t in p),path
            for j,t in enumerate(p):low[j]=min(low[j],t);high[j]=max(high[j],t)
        v+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
    size=[high[j]-low[j] for j in range(3)]
    err=max(abs(a-b) for a,b in zip(size,entry['size_mm']))
    volume_error=abs(abs(v)-entry['native_volume_mm3'])/entry['native_volume_mm3']
    assert err<.05,(path,err)
    assert abs(low[2])<.001,(path,low)
    assert volume_error<.035,(path,volume_error)
    results.append({'file':entry['file'],'triangles':n,'max_dimension_error_mm':err,'mesh_volume_relative_error':volume_error})
report={'pass':True,'meshes_checked':len(results),'dimension_tolerance_mm':.05,'volume_tolerance_fraction':.035,'results':results,'limitations':['No mechanical thread, strength, adhesion, preload or formal DfAM analysis','Quartered panels are separate temporary mock sections, not load-bearing joints','OLED surrogate omits glass/header and PCB surrogate omits other components']}
(HERE/'mesh-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='results'}))
