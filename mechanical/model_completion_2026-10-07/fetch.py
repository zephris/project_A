from pathlib import Path
import urllib.request,json,concurrent.futures
out=Path(__file__).parent
urls={
 'L1-library.step':'https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/1fea8f9ef5b64dc68dc98052e0860c3b',
 'LED-library.step':'https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/d4730404f94748a88e99bd67434d6079',
 'U4-library.step':'https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/88c2eb8aad2d4cafa03a2c8c19a0142c',
 'kiswitch-tree.json':'https://api.github.com/repos/kiswitch/kiswitch/git/trees/master?recursive=1',
 'L1-datasheet.pdf':'https://abracon.com/datasheets/AOTA-B201610S3R3-101-T.pdf',
 'LED-datasheet.pdf':'https://cdn-shop.adafruit.com/product-files/4492/Datasheet.pdf',
}
def fetch(n,u):
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'PHBox-CAD-model-review'})
  with urllib.request.urlopen(req,timeout=25) as r:data=r.read()
  (out/n).write_bytes(data);return {'file':n,'url':u,'bytes':len(data)}
 except Exception as e:return {'file':n,'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 rows=list(pool.map(lambda x:fetch(*x),urls.items()))
(out/'downloads.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
