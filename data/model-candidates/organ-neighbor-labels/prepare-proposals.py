"""Candidate-only organ-neighbor label builder. Never modifies active labels."""
from pathlib import Path
import json,csv,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda n,x:(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
audit=read(HERE/'ui-neighbor-audit.json');rows={r['id']:r for r in audit['entries']}
atlas=read(ROOT/'public/models/atlas.json');parts={p['id']:p for p in atlas['parts']}
ta=ROOT/'work/open-assets-review/TA2.csv'
assert sha(ta)=='0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
terms={}
for n,line in enumerate(ta.read_text().splitlines(),1):
 c=line.strip().strip('"').split(';')
 if len(c)>2 and c[0].isdigit():terms[c[1]]=dict(upstreamTableId=int(c[0]),english=c[1],latin=c[2],line=n)
official={};files=[]
for tree in ['isa','partof']:
 p=ROOT/f'data/model-candidates/concept-selection-review/{tree}_parts_list_e.txt'
 files.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),url=f'https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/{tree}_parts_list_e.txt'))
 for n,r in enumerate(csv.DictReader(p.open(),delimiter='\t'),2):official.setdefault(r['concept id'],[]).append(dict(path=str(p.relative_to(ROOT)),line=n,english=r['en'],representationId=r['representation id']))
spec={
 'FMA7370':('Superior lobe of left lung','Sol akciğer üst lobu',['sol üst lob']),
 'FMA7371':('Inferior lobe of left lung','Sol akciğer alt lobu',['sol alt lob']),
 'FMA7333':('Superior lobe of right lung','Sağ akciğer üst lobu',['sağ üst lob']),
 'FMA7337':('Inferior lobe of right lung','Sağ akciğer alt lobu',['sağ alt lob']),
 'FMA7383':('Middle lobe of right lung','Sağ akciğer orta lobu',['orta lob']),
 'FMA13362':('Right lobe of liver','Karaciğerin sağ lobu',['sağ karaciğer lobu']),
 'FMA13363':('Left lobe of liver','Karaciğerin sol lobu',['sol karaciğer lobu']),
 'FMA15809':('Right part of liver','Karaciğerin sağ fonksiyonel bölümü',['sağ hemikaraciğer','sağ hemiliver']),
 'FMA15810':('Left part of liver','Karaciğerin sol fonksiyonel bölümü',['sol hemikaraciğer','sol hemiliver']),
 'FMA14772':('Proper hepatic artery','Arteria hepatica propria',['hepatik arter propria']),
 'FMA15414':('Right branch of hepatic portal vein','Portal venin sağ dalı',['sağ portal ven']),
 'FMA7393':('Tracheobronchial tree','Trakeobronşiyal ağaç',['soluk borusu ve bronş ağacı']),
 'FMA7486':('Manubrium of sternum','Sternum manubriumu',['manubrium','göğüs kemiği sapı']),
 'FMA7487':('Body of sternum','Sternum gövdesi',['göğüs kemiği gövdesi']),
 'FMA7488':('Xiphoid process','Ksifoid çıkıntı',['ksifoid']),
 'FMA3736':('Ascending aorta','Çıkan aort',[]),
 'FMA3768':('Aortic arch','Aort kemeri',['arkus aorta']),
 'FMA3784':('Descending aorta','İnen aort',[]),
 'FMA7206':('Duodenum','Duodenum',['onikiparmak bağırsağı']),
 'FMA7207':('Jejunum','Jejunum',['boş bağırsak']),
 'FMA7208':('Ileum','İleum',[]),
 'FMA13478':('Vertebral column','Omurga',['vertebral kolon']),
 'FMA9576':('Thorax','Toraks',['göğüs bölgesi']),
}
notes={
 'FMA13362':'Kaynak sağ lob kavramı 17 damar ve safra ağacı yüzeyini seçiyor; bağımsız tam sağ lob parankim yüzeyi değildir.',
 'FMA13363':'Kaynak sol lob kavramı 25 damar/safra ağacı ve kaudat lob yüzeyini seçiyor; bağımsız tam sol lob parankim yüzeyi değildir.',
 'FMA15809':'Sağ hemiliver kaynak grubu hepatovenöz V–VIII segment yüzeylerini içerir; morfolojik sağ lob kavramından ayrıdır.',
 'FMA15810':'Sol hemiliver kaynak grubu hepatovenöz II–IV segment yüzeylerini içerir; morfolojik sol lob kavramından ayrıdır.',
}
lung_ids={'FMA7370','FMA7371','FMA7333','FMA7337','FMA7383'}
ready=[];held=[];evidence=[]
for id,row in rows.items():
 refs=[r for r in official.get(id,[]) if r['english'].casefold()==row['name'].casefold()]
 assert refs,(id,row['name'])
 geometry=[dict(id=pid,name=parts[pid]['name'],conceptId=parts[pid]['conceptId']) for pid in row['geometryPartIds']]
 ev=dict(id=id,sourceEnglish=row['name'],bp3d=refs,via=row['via'],geometry=geometry)
 if id in spec:
  key,tr,aliases=spec[id];term=terms[key];ev['ta2']=term
  note=notes.get(id)
  if id in lung_ids:note='Kaynak lob seçimi bronş ve damar alt yapılarını birlikte içerir; etiket tek başına bağımsız tam lob parankim yüzeyi bulunduğunu doğrulamaz.'
  if id=='FMA7383':ev['mappingNote']='Source term middle lobe of lung is directly part_of right lung FMA7309; exact TA2 right-middle-lobe term preserves this laterality.'
  elif id in ['FMA15809','FMA15810']:ev['mappingNote']='Functional hemiliver mapped to TA2 right/left part; source geometry contains corresponding V–VIII or II–IV segment names. Not mapped to morphological lobe.'
  elif row['name'].casefold()!=key.casefold():ev['mappingNote']='Explicit synonym/word-order match to the exact Latin row; source English retained unchanged.'
  ready.append(dict(ids=[id],datasetId='male-body',sourceEnglish=row['name'],geometryPartIds=row['geometryPartIds'],tr=tr,en=row['name'][0].upper()+row['name'][1:],la=term['latin'],side=None,aliases=aliases,ta2TableId=term['upstreamTableId'],expertReview='pending',trStatus='editorial',evidenceRef=f'source-evidence.json#{id}',scopeNoteTr=note,requiresRepresentationNote=id in notes or id in lung_ids))
 else:
  reason='No exact scope-preserving term established in the pinned TA2 table; do not replace this group/qualified part with its broader organ.'
  if id in ['FMA9465','FMA9466']:reason='Cavity geometry must not be relabeled as the complete atrium/ventricle. Exact cavity Latin not found in pinned table.'
  if id=='FMA9496':
   reason='Pinned row 3974 has suspect Latin Skeleton flbrosum cordis (letter l instead of i); do not silently publish or correct. Source selection contains only three valve leaflets/cusps, not a verified full fibrous skeleton.'
   ev['suspectTa2']=terms['Fibrous skeleton of heart']
  held.append(dict(id=id,sourceEnglish=row['name'],reason=reason,geometryPartIds=row['geometryPartIds']))
 evidence.append(ev)
assert len(ready)<=40 and len(ready)+len(held)==46
write('proposals.json',dict(schemaVersion=1,status='proposal_only_not_applied',scope='One graph step from thorax and abdomen-pelvis coverage bindings; maximum 40 new concepts',entries=ready,withheld=held))
inputs=['data/anatomy/coverage.json','data/anatomy/explorer.json','data/anatomy/labels.json','data/anatomy/brachial-plexus.json','app/knowledge.ts','app/atlas-metadata.ts','app/reference-datasets.ts','app/female-pelvis-labels.ts','public/models/atlas.json']
write('source-evidence.json',dict(schemaVersion=1,inputSnapshots=[dict(path=p,sha256=sha(ROOT/p)) for p in inputs],sources=files+[dict(path=str(ta.relative_to(ROOT)),sha256=sha(ta),url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv')],entries=evidence,cautions=['Pinned upstream TA2 text, not fresh publisher-PDF verification.','Turkish labels are editorial; expert review pending.','Latin exact-string matching is not independent semantic or mesh validation.','No extra graph step taken to reach individual lobar bronchi or cardiac walls.']))
write('validation.json',dict(seedConcepts=len(audit['seeds']),separateReferenceTargets=len(audit['references']),oneStepEndpoints=len(rows),runtimeMissingTrOrLa=audit['missingTrOrLa'],newConceptProposals=len(ready),withheld=len(held),sourceIdNameMatches=len(evidence),exactLatinMatches=len(ready),requiresRepresentationNote=sum(e['requiresRepresentationNote'] for e in ready),sharedFilesWritten=False))
print(len(ready),'ready;',len(held),'withheld;',sum(e['requiresRepresentationNote'] for e in ready),'need scope note')
