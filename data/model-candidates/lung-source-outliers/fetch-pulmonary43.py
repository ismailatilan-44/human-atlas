from pathlib import Path
import importlib.util,csv,json,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
s=importlib.util.spec_from_file_location('dl',ROOT/'work/thyroid-alternative/reference-downloader.py');d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
ids=['FJ6044','FJ6045','FJ6046','FJ6047','FJ6049','FJ6050','FJ6051'];catalog={r['fj_id']:r for r in csv.DictReader((ROOT/'work/thyroid-alternative/bp3d-v43-manifest.csv').open())};bps=[catalog[i]['bp_id'] for i in ids];cookies=D/'session-cookies.txt'
try:
 d.get_session(cookies);d.download_zip(ids,bps,D/'pulmonary-43-source.zip',cookies)
finally:cookies.unlink(missing_ok=True)
(D/'pulmonary-43-request.json').write_text(json.dumps(dict(url=d.DOWNLOAD_CGI,method='POST',ids=ids,rep_id=bps,type='art_file',all_downloads=1,sha256=hashlib.sha256((D/'pulmonary-43-source.zip').read_bytes()).hexdigest()),indent=2)+'\n')
print('done')
