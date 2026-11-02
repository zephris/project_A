from pathlib import Path
import json,ezdxf
HERE=Path(__file__).resolve().parents[1]
report={}
for path in sorted((HERE/'DXF').glob('*.dxf')):
    doc=ezdxf.readfile(path);audit=doc.audit()
    report[path.name]={'INSUNITS':doc.header.get('$INSUNITS'),'audit_errors':len(audit.errors),
                       'entity_count':len(doc.modelspace()),'layers':sorted({e.dxf.layer for e in doc.modelspace()})}
    assert not audit.errors and doc.header.get('$INSUNITS')==4,path.name
(HERE/'cut-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
