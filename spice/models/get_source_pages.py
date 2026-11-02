from pathlib import Path
import urllib.request,concurrent.futures,re,json,html
out=Path('spice/models/vendor');tasks=[('ST_ESDA','https://www.st.com/en/protections-and-emi-filters/esda7p120-1u1m.html'),('ST_USBLC','https://www.st.com/en/protections-and-emi-filters/usblc6-2.html'),('Winbond','https://www.winbond.com/hq/product/code-storage-flash/qspi-nor/w25q-jv/?__locale=en&partNo=W25Q128JVSIQ')]
def get(t):
 name,url=t
 try:
  s=urllib.request.urlopen(url,timeout=15).read().decode('utf-8',errors='replace');(out/(name+'-source-page.html')).write_text(s,encoding='utf-8');links=[html.unescape(x) for x in re.findall(r'(?:href|data-url)=[\"\x27]([^\"\x27]+)',s) if re.search(r'spice|\.zip|\.ibs|\.s\dp',x,re.I)];return {'name':name,'links':links}
 except Exception as e:return {'name':name,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as p:rows=list(p.map(get,tasks))
(out/'source-page-intake.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
