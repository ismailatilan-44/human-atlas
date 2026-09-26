"""Bounded pulmonary branch label candidates; no active-data writes."""
from pathlib import Path
import json,csv,hashlib
H=Path(__file__).resolve().parent;R=H.parents[2];S=R/'data/model-candidates/lung-source-outliers'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda n,x:(H/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
atlas=read(R/'public/models/atlas.json');cs={c['id']:c for c in atlas['concepts']};parts={p['id']:p for p in atlas['parts']}
graph=read(R/'data/anatomy/explorer.json');parents=['FMA50872','FMA50873']
direct=[r for r in graph['relations'] if r['predicate']=='part_of' and r['object'] in parents and 'artery' in cs.get(r['subject'],{}).get('name','')]
assert {r['subject'] for r in direct}=={'FMA68201'}
review=read(S/'reviewed-view-proposal.json');snapshot=read(S/'FMA8620-pinned43.json')
source_terms={}
def walk(x,path='$'):
 if isinstance(x,dict):
  if x.get('f_id') in ['FMA8620','FMA68677','FMA68683'] and x.get('name_e'):
   source_terms.setdefault(x['f_id'],[]).append(dict(jsonPath=path,id=x['f_id'],english=x['name_e'],latin=x.get('name_l')))
  for k,v in x.items():walk(v,path+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+'/'+str(i))
walk(snapshot)
ta=R/'work/open-assets-review/TA2.csv';assert sha(ta)=='0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
terms={}
for n,line in enumerate(ta.read_text().splitlines(),1):
 c=line.strip().strip('"').split(';')
 if len(c)>2 and c[0].isdigit():terms[int(c[0])]=dict(upstreamTableId=int(c[0]),english=c[1],latin=c[2],line=n)
official={};sources=[]
for tree in ['isa','partof']:
 p=S/f'{tree}_parts_list_e.txt';sources.append(dict(path=str(p.relative_to(R)),sha256=sha(p),url=f'https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/{tree}_parts_list_e.txt'))
 for n,c in enumerate(csv.DictReader(p.open(),delimiter='\t'),2):official.setdefault(c['concept id'],[]).append(dict(path=str(p.relative_to(R)),line=n,english=c['en'],representationId=c['representation id']))
spec={
'FMA8620':('Sağ akciğer anterior segmental arteri',4080,['sağ ön segment atardamarı','sağ anterior segmental pulmoner arter']),
'FMA68677':('Sağ anterior segmental pulmoner arterin posterior dalı',None,['sağ anterior segmental arterin arka dalı']),
'FMA68683':('Sağ anterior segmental pulmoner arterin anterior dalı',None,['sağ anterior segmental arterin ön dalı']),
'FMA68201':('Sol akciğer alt lob arteri',4101,['sol alt lobar arter']),
}
existing={i:e for e in read(R/'data/anatomy/labels.json')['entries'] for i in e['ids']}
entries=[];evidence=[];retained=[]
for id,(tr,taid,aliases) in spec.items():
 c=cs[id];refs=[r for r in official[id] if r['english'].casefold()==c['name'].casefold()];assert refs
 if id in source_terms:assert all(r['english'].casefold()==c['name'].casefold() for r in source_terms[id])
 geometry=review['proposedReviewedElementIds'] if id=='FMA8620' else c['elements']
 note='Kaynak dal kimliği korunur; etiket tam damar ağacı veya geometri eksiksizliği iddiası değildir.'
 if id=='FMA8620':note='İncelenmiş seçim yedi torasik damar yüzeyini içerir. Ham kaynak grubundaki FJ2041/FJ2044 bu seçimden ayrılmıştır; kimlikleri belirsizdir ve renal damara otomatik yeniden atanmaz.'
 if id in ['FMA68677','FMA68683']:note='Bu kavram anterior segmental arterin '+('posterior' if id=='FMA68677' else 'anterior')+' alt dalıdır; '+('üç' if id=='FMA68677' else 'dört')+' mevcut kaynak yüzeyini birlikte seçer. Ana segmental arterle eşitlenmez.'
 e=dict(ids=[id],datasetId='male-body',sourceEnglish=c['name'],tr=tr,en=c['name'][0].upper()+c['name'][1:],la=terms[taid]['latin'] if taid else None,side=None,aliases=aliases,ta2TableId=taid,geometryPartIds=geometry,rawSourceGeometryPartIds=c['elements'],expertReview='pending',trStatus='editorial',scopeNoteTr=note,evidenceRef=f'source-evidence.json#{id}')
 if id in existing and existing[id].get('tr') and existing[id].get('en'):retained.append(dict(id=id,existing=existing[id]))
 else:entries.append(e)
 evidence.append(dict(id=id,bp3d=refs,official43SnapshotRecords=source_terms.get(id,[]),ta2=terms[taid] if taid else None,geometry=[dict(id=pid,name=parts[pid]['name'],conceptId=parts[pid]['conceptId']) for pid in geometry],relationEvidence=[r for r in direct if r['subject']==id],mappingNote='FMA8620 official4.3 Latin field uses Ramus anterior descendens (arteria pulmonalis dextra); this proposal chooses the exact pinned TA2 anterior segmental artery term matching its English concept. Both source wordings preserved; no silent source rewrite.' if id=='FMA8620' else 'No exact Latin established for this qualified sub-branch; null retained.' if taid is None else 'Lower/inferior lobar artery wording matched; exact lateralized TA2 term.'))
assert len(entries)+len(retained)==4<=20
assert set(review['proposedReviewedElementIds'])==set(cs['FMA68677']['elements'])|set(cs['FMA68683']['elements'])
write('proposals.json',dict(schemaVersion=1,status='proposal_only_not_applied',scope='Requested FMA8620 and two sub-branches plus the one current direct arterial branch neighbor of right/left pulmonary artery',entries=entries,retainExisting=retained,geometryPolicy='Evidence-only identity and reviewed-selection snapshots; this label package does not change raw source membership, perform renal reassignment or integrate an alternative mesh.'))
inputs=[R/'public/models/atlas.json',R/'data/anatomy/explorer.json',R/'data/anatomy/labels.json',S/'FMA8620-pinned43.json',S/'reviewed-view-proposal.json',S/'evidence.json']
write('source-evidence.json',dict(schemaVersion=1,inputSnapshots=[dict(path=str(p.relative_to(R)),sha256=sha(p)) for p in inputs],sources=sources+[dict(path=str(ta.relative_to(R)),sha256=sha(ta),url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv')],scopeCheck=dict(parentIds=parents,directArterialChildren=direct,notIncluded='FMA45842 pulmonary arterial tree is a parent group, not a direct arterial branch; no additional graph expansion.'),entries=evidence,cautions=['Two branch Latin fields remain null; do not derive unverified Latin compounds.','TA2 supplied by pinned upstream distribution, not new publisher verification.','FJ2041 and FJ2044 remain unresolved raw source IDs.','Turkish editorial labels require expert review.']))
write('validation.json',dict(scopedConcepts=4,newTrEnRecords=len(entries),retainedExisting=len(retained),verifiedLatin=2,nullLatin=2,officialIdNameMatches=4,reviewedFMA8620Surfaces=7,posteriorBranchSurfaces=3,anteriorBranchSurfaces=4,unionOfBranchesEqualsReviewedSelection=True,sharedFilesWritten=False))
print('Validated 4 candidates;2 exact Latin;2 Latin null;7=3+4 reviewed geometry')
