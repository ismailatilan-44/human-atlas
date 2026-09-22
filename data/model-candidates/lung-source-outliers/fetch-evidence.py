from pathlib import Path
import importlib.util,json,hashlib,urllib.request,zipfile,csv
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
s=importlib.util.spec_from_file_location('dl',ROOT/'work/thyroid-alternative/reference-downloader.py');dl=importlib.util.module_from_spec(s);s.loader.exec_module(dl)
c=D/'session-cookies.txt';records=[]
try:
 dl.get_session(c)
 ids=['FJ2042','FJ2043','FJ2045','FJ2974','FJ6044']
 catalog={r['fj_id']:r for r in csv.DictReader((ROOT/'work/thyroid-alternative/bp3d-v43-manifest.csv').open())}
 bps=['BP7665','BP7668','BP7670']+[catalog[i]['bp_id'] for i in ids[3:]]
 dl.download_zip(ids,bps,D/'comparison-objects.zip',c)
 for cid in ['FMA8620','FMA86342','FMA86344']:
  u='https://lifesciencedb.jp/bp3d/get-fmastratum.cgi?version=4.3&lng=en&t_type=4&bul_id=4&cb_id=5&ci_id=1&md_id=1&mv_id=6&mr_id=1&f_id='+cid
  b=dl._curl([*dl._base_curl(c),u]);(D/(cid+'-pinned43.json')).write_bytes(b);records.append(dict(url=u,file=cid+'-pinned43.json',sha256=hashlib.sha256(b).hexdigest()))
finally:c.unlink(missing_ok=True)
records.append(dict(url=dl.DOWNLOAD_CGI,method='POST',filename='comparison-objects.zip',ids=ids,rep_id=bps,type='art_file',all_downloads=1,sha256=hashlib.sha256((D/'comparison-objects.zip').read_bytes()).hexdigest(),note='Inspect each returned OBJ compatibility version; IDs are not assumed to belong to 4.3.'))
records.append(dict(url=dl.DOWNLOAD_CGI,method='POST',filename='live-outlier-objects.zip',ids=['FJ2041','FJ2044'],rep_id=['BP7661'],type='art_file',all_downloads=1,sha256=hashlib.sha256((D/'live-outlier-objects.zip').read_bytes()).hexdigest(),returnedCompatibilityVersion='4.0'))
for name in ['isa_element_parts.txt','partof_element_parts.txt','isa_parts_list_e.txt','partof_parts_list_e.txt']:
 records.append(dict(url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/'+name,filename=name,sha256=hashlib.sha256((D/name).read_bytes()).hexdigest()))
records.append(dict(filename='../lung-surfaces/FMA2Obj.txt',url='https://lifesciencedb.jp/bp3d/get-info.cgi?version=4.3&cmd=concept-objfiles-list',sha256=hashlib.sha256((D.parent/'lung-surfaces/FMA2Obj.txt').read_bytes()).hexdigest(),headers={'Data Version':'4.3','Objects set':'4.3','Tree version':'FMA3.0'}))
(D/'source-fetch.json').write_text(json.dumps(records,indent=2)+'\n');print('done')
