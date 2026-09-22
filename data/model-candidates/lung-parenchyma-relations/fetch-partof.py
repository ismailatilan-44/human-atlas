from pathlib import Path
import urllib.request,urllib.parse,json,hashlib,concurrent.futures
OUT=Path(__file__).resolve().parent
SRC=OUT.parent/'lung-surfaces'
params={'version':'4.3','lng':'en','t_type':'4','bul_id':'4','cb_id':'5','ci_id':'1','md_id':'1','mv_id':'6','mr_id':'1'}
manifest=json.loads((SRC/'lung-parenchyma.json').read_text());ids=[c['id'] for c in manifest['concepts'] if c['id'] not in manifest['extendsConceptIds']]
assert len(ids)==17
(OUT/'source').mkdir(exist_ok=True)

def get(fid,endpoint='get-fmastratum.cgi'):
 url='https://lifesciencedb.jp/bp3d/'+endpoint+'?'+urllib.parse.urlencode({**params,'f_id':fid})
 target=OUT/'source'/(fid+('-partof' if endpoint=='get-partof.cgi' else '')+'.json')
 if not target.exists(): target.write_bytes(urllib.request.urlopen(url,timeout=55).read())
 b=target.read_bytes();d=json.loads(b)
 if endpoint=='get-fmastratum.cgi':assert d['images'][0]['f_id']==fid and d['images'][0]['partof_path2root']
 else:
  matching=[x for x in d['data'] if x.get('f_id')==fid]
  assert matching and all(x['version']=='4.3' and x['concept_info']=='FMA' and x['concept_build']=='3.0' and str(x['cb_id'])=='5' for x in matching),matching[:1]
 return {'conceptId':fid,'url':url,'path':str(target.relative_to(OUT)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'endpoint':endpoint}
proof=get(ids[0],'get-partof.cgi');print('Pinned 4.3/FMA3.0 verified',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 records=list(pool.map(get,ids))
(OUT/'source-fetch.json').write_text(json.dumps({'versionMetadataUrl':'https://lifesciencedb.jp/bp3d/get-version.cgi?lng=en','versionMetadataPath':'versions.json','versionMetadataSha256':hashlib.sha256((OUT/'versions.json').read_bytes()).hexdigest(),'requestedParameters':params,'conceptBuildConfirmed':'FMA3.0','records':[proof]+records},indent=2)+'\n')
print('Downloaded',len(records),'pinned source paths',flush=True)
