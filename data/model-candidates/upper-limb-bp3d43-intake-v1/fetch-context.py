"""Second bounded acquisition phase: source-frame bones, no registration."""
import csv,datetime,hashlib,io,json,urllib.request,urllib.parse,http.cookiejar,zipfile
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
assert (OUT/'phase1-intake.json').exists()
BASE='https://lifesciencedb.jp/bp3d';ids=['FJ3158','FJ3228','FJ3229','FJ3237','FJ3262','FJ3279'];reuse=['FJ3167','FJ3170','FJ3172']
rows={r['fj_id']:r for r in csv.DictReader((ROOT/'work/thyroid-alternative/bp3d-v43-manifest.csv').open())}
fields=dict(ids=json.dumps(ids),rep_id=json.dumps([rows[i]['bp_id'] for i in ids]),filename='upper-limb-bp3d43-context-v1',type='art_file',all_downloads='1')
request=dict(url=BASE+'/download.cgi',method='POST',fields=fields,requestedIds=ids,reusedIds=reuse,catalogRows=[rows[i] for i in ids+reuse],scope='Left scapula/clavicle/humerus, first/second ribs and C5/C6/C7/T1 vertebrae. There is no C8 vertebra; spinal nerve C8 is a separate object. Duplicate-name clavicle/humerus companion components are not silently substituted or equated.')
(OUT/'context-request.json').write_text(json.dumps(request,indent=2)+'\n')
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
opener.open(BASE+'/?lng=en',timeout=60).read()
req=urllib.request.Request(request['url'],data=urllib.parse.urlencode(fields).encode(),headers={'User-Agent':'Mozilla/5.0','Referer':BASE+'/?lng=en'})
with opener.open(req,timeout=60) as response:blob=response.read();status=response.status
assert not (OUT/'context-source.zip').exists()
(OUT/'context-source.zip').write_bytes(blob);(OUT/'context-objs').mkdir(exist_ok=True)
with zipfile.ZipFile(io.BytesIO(blob)) as z:
 for name in z.namelist():
  p=Path(name).name
  if p.endswith('.obj'):assert p.split('_')[0] in ids;(OUT/'context-objs'/p).write_bytes(z.read(name))
archive=ROOT/'work/thyroid-alternative/thyroid-bp3d43-references.zip';reused=[]
with zipfile.ZipFile(archive) as z:
 for name in z.namelist():
  p=Path(name).name
  if p.split('_')[0] in reuse:
   data=z.read(name);(OUT/'context-objs'/p).write_bytes(data);reused.append(dict(member=name,sha256=hashlib.sha256(data).hexdigest()))
log=[dict(url=request['url'],method='POST',path='context-source.zip',retrievedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),status=status,bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest()),dict(method='reuse_retained_official_source_zip',sourcePath=str(archive.relative_to(ROOT)),sourceSha256=hashlib.sha256(archive.read_bytes()).hexdigest(),originalRetrievalDate='2026-09-22 per retained thyroid source review',inspectedOn='2026-10-02',members=reused,versionBasis='Each OBJ compatibility4.3 header + fresh official FMA2Obj membership; not a new HTTP download')]
(OUT/'context-fetch.json').write_text(json.dumps(log,indent=2)+'\n')
print('Context phase:',len(ids),'downloaded and',len(reused),'reused OBJ files')
