"""Saved print exports: STEP solids, front-face-down relief, and STL topology."""
from pathlib import Path
import sys, json, struct
from collections import Counter
from cadgen import read_step, build123d as bd
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'src'))
from port_seal_common import seal_parts

report={}
for kind,source in zip(('a','c'),seal_parts()):
    name=f'usb_{kind}_collar'
    shape=read_step(HERE/'STEP'/f'{name}.step')
    box=shape.bounding_box()
    assert shape.is_valid and len(shape.solids())==1
    assert abs(box.min.Z)<1e-6 and abs(box.max.Z-2)<1e-6
    assert abs(shape.volume-source.volume)<1e-5
    # With front on bed, the relief reduces upper cross-section volume.
    w,h=box.size.X,box.size.Y
    low=bd.Pos(w/2,h/2,.1)*bd.Box(w+1,h+1,.1)
    high=bd.Pos(w/2,h/2,1.9)*bd.Box(w+1,h+1,.1)
    def volume(result):
        return result.volume if hasattr(result,'volume') else sum(s.volume for s in result)
    front=volume(shape.intersect(low))
    back=volume(shape.intersect(high))
    assert front>back+1e-5,(kind,'rear relief faces bed instead of upward')
    raw=(HERE/'STL'/f'{name}.stl').read_bytes()
    count=struct.unpack_from('<I',raw,80)[0]
    assert len(raw)==84+50*count
    edges=Counter()
    for i in range(count):
        values=struct.unpack_from('<12fH',raw,84+50*i)
        vertices=[tuple(round(v,5) for v in values[j:j+3]) for j in (3,6,9)]
        assert len(set(vertices))==3,'degenerate facet'
        for a,b in zip(vertices,vertices[1:]+vertices[:1]):
            edges[tuple(sorted((a,b)))]+=1
    assert all(n==2 for n in edges.values()),'non-manifold or open STL edge'
    report[kind]={'valid_single_solid':True,'size_mm':[w,h,box.size.Z],
                  'volume_mm3':shape.volume,'front_face_down':True,
                  'STL_triangles':count,'STL_closed_edge_check':True}
result={'parts':report,'limitations':'Geometry and mesh checks only; thin membrane printability and TPU mechanical response require trials.'}
(HERE/'collar-print-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
