"""Rebuild the active assembly/fabrication bundle without changing artwork."""
from pathlib import Path
import csv,hashlib,json,zipfile
root=Path(__file__).resolve().parent
pkg=root/'PHBox_2026-10-06_DFM_resolved'
def refs(name):
 with (pkg/'assembly'/name).open(newline='') as f:return {ref.strip() for row in csv.DictReader(f) for ref in row['Designator'].split(',')}
assert refs('BOM-JLCPCB.csv')==refs('CPL-JLCDFM.csv')
assert 'C41' in refs('BOM-JLCPCB.csv')
hashes={p.relative_to(pkg).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['fabrication','stencil','assembly'] for p in sorted((pkg/folder).iterdir()) if p.is_file()}
(pkg/'validation/final-file-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
with zipfile.ZipFile(pkg/'upload/PHBox-DFM-resolved-Gerbers.zip') as z:
 assert z.testzip() is None
 assert all(z.read(n)==(pkg/'fabrication'/n).read_bytes() for n in z.namelist())
archive=root/'PHBox_2026-10-06_DFM_resolved.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(pkg.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(pkg).as_posix())
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
archive.with_suffix('.zip.sha256').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
print(f'Packaged {len(refs("BOM-JLCPCB.csv"))} assembly designators; ZIP integrity verified.')
