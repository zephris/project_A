from pathlib import Path
import urllib.request,zipfile,io,json,concurrent.futures,hashlib,re
root=Path('spice/models/vendor');tasks=[('ESDA7P120_1U1M','https://www.st.com/resource/en/spice_model/esda7p120-1u1m.zip'),('USBLC6_2SC6','https://www.st.com/resource/en/spice_model/usblc6-2sc6.zip'),('WINBOND_IBIS_LIST','https://www.winbond.com/hq/support/documentation/?__locale=en&line=/product/code-storage-flash/index.html&family=/product/code-storage-flash/qspi-nor/index.html&pno=W25Q128JVSIQ&category=/.categories/resources/ibis-model/')]
def fetch(t):
 part,url=t;row={'part':part,'url':url,'download_date':'2026-10-07'}
 try:
  data=urllib.request.urlopen(url,timeout=15).read()
  if part=='WINBOND_IBIS_LIST':
   s=data.decode('utf-8',errors='replace');(root/'Winbond-IBIS-list.html').write_text(s,encoding='utf-8');row.update(status='page_saved',links=re.findall(r'href=[\"\x27]([^\"\x27]+)',s));return row
  z=zipfile.ZipFile(io.BytesIO(data));folder=root/part;folder.mkdir(exist_ok=True);(folder/'original.zip').write_bytes(data)
  for info in z.infolist():
   target=(folder/info.filename).resolve();assert target.is_relative_to(folder.resolve())
   if not info.is_dir():target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(info))
  row.update(status='downloaded',sha256=hashlib.sha256(data).hexdigest(),files=z.namelist())
 except Exception as e:row.update(status='download_failed',error=str(e))
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as p:rows=list(p.map(fetch,tasks))
(root/'additional-intake-2026-10-07.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
