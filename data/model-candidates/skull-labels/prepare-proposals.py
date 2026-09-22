"""Rebuild bounded skull label candidate files; never write active app/data files."""
from pathlib import Path
import csv,hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
write=lambda n,x:(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
selection_path=ROOT/'data/model-candidates/concept-selection-review/skull-bones-proposal.json'
selection=read(selection_path)
labels_path=ROOT/'data/anatomy/labels.json'
labels=read(labels_path)
existing={id:e for e in labels['entries'] for id in e['ids']}
manifest_path=ROOT/'public/models/atlas.json'
atlas=read(manifest_path)
parts={p['id']:p for p in atlas['parts']}
concepts={c['id']:c for c in atlas['concepts']}
ta=ROOT/'work/open-assets-review/TA2.csv'
assert sha(ta)=='0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
terms={}
for number,line in enumerate(ta.read_text().splitlines(),1):
 c=line.strip().strip('"').split(';')
 if len(c)>2 and c[0].isdigit():terms[c[1]]=dict(upstreamTableId=int(c[0]),english=c[1],latin=c[2],line=number)
official={}
sourcefiles=[]
for tree in ['isa','partof']:
 p=ROOT/f'data/model-candidates/concept-selection-review/{tree}_parts_list_e.txt'
 sourcefiles.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),url=f'https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/{tree}_parts_list_e.txt'))
 for line,row in enumerate(csv.DictReader(p.open(),delimiter='\t'),2):official.setdefault(row['concept id'],[]).append(dict(file=str(p.relative_to(ROOT)),line=line,english=row['en'],representationId=row['representation id']))
spec={
 'ethmoid':('Ethmoid bone','Etmoid kemik',['kalbur kemiği','etmoid']),
 'frontal bone':('Frontal bone','Frontal kemik',['alın kemiği']),
 'inferior nasal concha':('Inferior nasal concha bone','Alt burun konkası',['alt konka','alt burun konkası kemiği']),
 'lacrimal bone':('Lacrimal bone','Lakrimal kemik',['gözyaşı kemiği']),
 'maxilla':('Maxilla','Maksilla',['üst çene','üst çene kemiği']),
 'nasal bone':('Nasal bone','Nazal kemik',['burun kemiği']),
 'palatine bone':('Palatine bone','Palatin kemik',['damak kemiği']),
 'parietal bone':('Parietal bone','Parietal kemik',['duvar kemiği']),
 'temporal bone':('Temporal bone','Temporal kemik',['şakak kemiği']),
 'zygomatic bone':('Zygomatic bone','Zigomatik kemik',['elmacık kemiği']),
 'mandible':('Mandible','Mandibula',['alt çene','çene kemiği']),
 'occipital bone':('Occipital bone','Oksipital kemik',['artkafa kemiği','art kafa kemiği']),
 'sphenoid bone':('Sphenoid bone','Sfenoid kemik',['sfenoid']),
 'vomer':('Vomer','Vomer',['sapan kemiği']),
}
entries=[];retained=[];evidence=[]
for p in selection['parts']:
 id=p['sourceConceptId'];name=p['sourceName'];pid=p['partId']
 assert parts[pid]['conceptId']==id and parts[pid]['name']==name
 assert concepts[id]['elements']==[pid],(id,concepts[id]['elements'])
 refs=[r for r in official[id] if r['english'].casefold()==name.casefold()]
 assert refs,(id,name)
 side='left' if name.startswith('Left ') else 'right' if name.startswith('Right ') else None
 generic=name.split(' ',1)[1] if side else name
 key,tr,aliases=spec[generic.casefold()];term=terms[key]
 evidence.append(dict(id=id,partId=pid,sourceEnglish=name,bp3d=refs,ta2=term,semanticMapping='Generic bone term; side retained in a separate side field' if side else 'Corresponding single bone term'))
 if id in existing:
  assert all(existing[id].get(l) for l in ['tr','en','la'])
  retained.append(dict(id=id,partId=pid,existingLabel=existing[id]));continue
 entries.append(dict(ids=[id],datasetId='male-body',geometryPartIds=[pid],sourceEnglish=name,tr=tr,en=generic,la=term['latin'],side=side,ta2TableId=term['upstreamTableId'],aliases=aliases,evidenceRef=f'source-evidence.json#{id}',expertReview='pending',trStatus='editorial'))
term=terms['Bones of cranium']
aggregate=dict(ids=['atlas:skull-bones'],datasetId='male-body',geometryPartIds=selection['elements'],sourceEnglish=selection['name'],tr='Kafatası kemikleri',en='Skull bones',la=term['latin'],side=None,ta2TableId=term['upstreamTableId'],aliases=['kafatası kemikleri','kraniyal kemikler'],evidenceRef='source-evidence.json#atlas:skull-bones',expertReview='pending',trStatus='editorial',scopeNote='Project selection of 22 source bone objects including mandible; excludes eye/lacrimal gland, hyoid, teeth and auditory ossicles. Term evidence does not independently validate selection membership.')
if 'atlas:skull-bones' not in existing:entries.append(aggregate)
else:retained.append(dict(id='atlas:skull-bones',existingLabel=existing['atlas:skull-bones']))
evidence.append(dict(id='atlas:skull-bones',ta2=term,selectionSource=str(selection_path.relative_to(ROOT)),semanticMapping='Project selection label supported by Bones of cranium / Ossa cranii; not a new FMA assertion'))
write('proposals.json',dict(schemaVersion=1,status='proposal_only_not_applied',scope='22 selected skull bones and the project aggregate only',entries=entries,retainExisting=retained))
inputs=[selection_path,labels_path,manifest_path,ROOT/'app/atlas-metadata.ts']
write('source-evidence.json',dict(schemaVersion=1,inputSnapshots=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in inputs],sources=sourcefiles+[dict(path=str(ta.relative_to(ROOT)),sha256=sha(ta),url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv',limitation='Pinned upstream TA2 distribution; not a fresh FIPAT publisher PDF verification. Table IDs are upstream CSV row IDs.')],entries=evidence,cautions=['Turkish labels and aliases are editorial, not official Turkish terminology endorsement.','Generic Latin is copied exactly; existing anatomyLabel helper supplies L/R markers, not invented Latin declensions.','Inferior nasal concha uses the osteology bone entry 740 Concha nasalis inferior, not the separate respiratory entry 3151 Concha inferior nasi.','Selection membership is inherited from the independent concept-selection review; this is an ID/name label audit, not a fresh mesh review.']))
assert len(selection['parts'])==len({p['partId'] for p in selection['parts']})==22
assert len(entries)+len(retained)==23
assert all(e['la'] for e in entries)
write('validation.json',dict(selectedBones=22,scopeIds=23,newLabelRecords=len(entries),retainedExistingRecords=len(retained),sourceIdNameAndSinglePartMatches=22,latinTermsExact=True,sharedFilesWritten=False))
print('Validated',len(entries),'new records;',len(retained),'retained; 22 exact source single-part matches')
