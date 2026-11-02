from pathlib import Path
import urllib.request,zipfile,io,json,hashlib,concurrent.futures
root=Path.cwd()/'spice/models/vendor';tasks=[('TPS2553','slvm425b'),('TLV73333P','sbvm471'),('SN74LV1T34_SPICE','sclm180'),('SN74LV1T34_IBIS','sclm119')]
def fetch(task):
 part,code=task;url='https://www.ti.com/lit/zip/'+code;row={'part':part,'url':url,'download_date':'2026-10-07'}
 try:
  data=urllib.request.urlopen(url,timeout=25).read();z=zipfile.ZipFile(io.BytesIO(data));folder=root/part;folder.mkdir(exist_ok=True,parents=True);(folder/(code+'.zip')).write_bytes(data)
  names=[]
  for info in z.infolist():
   target=(folder/info.filename).resolve();assert target.is_relative_to(folder.resolve())
   if info.is_dir():target.mkdir(parents=True,exist_ok=True);continue
   target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(info));names.append(info.filename)
  row.update(status='downloaded',sha256=hashlib.sha256(data).hexdigest(),files=names)
 except Exception as e:row.update(status='download_failed',error=str(e))
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,tasks))
(root/'download-manifest-2026-10-07.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
