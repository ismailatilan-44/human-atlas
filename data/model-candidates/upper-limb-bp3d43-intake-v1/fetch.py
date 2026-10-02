"""Bounded official public source acquisition; output only this candidate directory."""
import csv,datetime,hashlib,io,json,urllib.request,urllib.parse,http.cookiejar,zipfile
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
BASE='https://lifesciencedb.jp/bp3d'
ids=['FJ4245','FJ4264','FJ4265','FJ4266','FJ4267','FJ4274','FJ4275','FJ4258','FJ4172','FJ4240','FJ4171','FJ4243','FJ4185','FJ4222','FJ4223','FJ4242','FJ4256']
rows={r['fj_id']:r for r in csv.DictReader((ROOT/'work/thyroid-alternative/bp3d-v43-manifest.csv').open())}
fields=dict(ids=json.dumps(ids),rep_id=json.dumps([rows[i]['bp_id'] for i in ids]),filename='upper-limb-bp3d43-intake-v1',type='art_file',all_downloads='1')
request=dict(url=BASE+'/download.cgi',method='POST',fields=fields,requestedIds=ids,catalogRows=[rows[i] for i in ids],scope='17 small source objects; no broad model download or active integration')
(OUT/'request.json').write_text(json.dumps(request,indent=2)+'\n')
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
log=[]
def fetch(url,name,data=None):
 if (OUT/name).exists():raise RuntimeError('Refuse to overwrite source acquisition '+name)
 req=urllib.request.Request(url,data=data,headers={'User-Agent':'Mozilla/5.0','Referer':BASE+'/?lng=en'})
 with opener.open(req,timeout=60) as response:blob=response.read();status=response.status;ctype=response.headers.get('Content-Type')
 (OUT/name).write_bytes(blob)
 log.append(dict(url=url,method='POST' if data else 'GET',path=name,retrievedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),status=status,contentType=ctype,bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest()))
 (OUT/'source-fetch.json').write_text(json.dumps(log,indent=2)+'\n')
 return blob
opener.open(BASE+'/?lng=en',timeout=60).read()
fetch(BASE+'/info_en/license/index.html','license.html')
blob=fetch(BASE+'/get-info.cgi?version=4.3&cmd=concept-objfiles-list','mapping.zip')
with zipfile.ZipFile(io.BytesIO(blob)) as z:
 txt=next(n for n in z.namelist() if n.endswith('FMA2Obj.txt'));(OUT/'FMA2Obj.txt').write_bytes(z.read(txt))
blob=fetch(request['url'],'source-objects.zip',urllib.parse.urlencode(fields).encode())
with zipfile.ZipFile(io.BytesIO(blob)) as z:
 for info in z.infolist():
  name=Path(info.filename).name
  if name.endswith('.obj'):
   assert name.split('_')[0] in ids
   (OUT/'objs').mkdir(exist_ok=True);(OUT/'objs'/name).write_bytes(z.read(info.filename))
print('Fetched',len(ids),'requested IDs;',len(list((OUT/'objs').glob('*.obj'))),'OBJ members')
