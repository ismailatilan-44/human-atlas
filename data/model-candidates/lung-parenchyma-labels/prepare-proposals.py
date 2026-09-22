"""Build labels for the 17 source segment-parenchyma concepts only."""
from pathlib import Path
import json,csv,hashlib,zipfile
H=Path(__file__).resolve().parent;R=H.parents[2];S=R/'data/model-candidates/lung-surfaces'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda n,x:(H/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
m=read(S/'lung-parenchyma.json');parts={p['id']:p for p in m['parts']}
catalog={r['fj_id']:r for r in csv.DictReader((S/'bp3d-v43-object-catalog.csv').open())}
sourcezip=zipfile.ZipFile(S/'lung-parenchyma-source.zip')
maprows=[]
for n,line in enumerate((S/'FMA2Obj.txt').read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3 and c[0].startswith('FMA'):maprows.append(dict(line=n,id=c[0],relation=c[1],objects=c[2].split('+')))
# Explicit source segment identity; no segment numbering introduced.
tr={
'FMA27368':'apikoposterior','FMA27394':'posterior bazal','FMA27374':'anterior','FMA27375':'üst lingular','FMA27376':'alt lingular','FMA27386':'superior','FMA27392':'anterior bazal','FMA27390':'lateral bazal','FMA27369':'apikal','FMA27393':'posterior bazal','FMA27371':'posterior','FMA27373':'anterior','FMA27452':'lateral','FMA27448':'medial','FMA27385':'superior','FMA27391':'anterior bazal','FMA27389':'lateral bazal'}
lobes={'FMA7370':('left','üst','upper'),'FMA7371':('left','alt','lower'),'FMA7333':('right','üst','upper'),'FMA7383':('right','orta','middle'),'FMA7337':('right','alt','lower')}
concepts={c['id']:c for c in m['concepts']};labels=read(R/'data/anatomy/labels.json');existing={i:e for e in labels['entries'] for i in e['ids']}
entries=[];evidence=[];retained=[]
for id,segment in tr.items():
 c=concepts[id];raw=[pid.removeprefix('BP43-') for pid in c['elements']]
 matches=[x for x in maprows if x['id']==id and set(x['objects'])==set(raw)]
 assert matches,(id,raw)
 memberships=[gid for gid in lobes if set(c['elements']).issubset(concepts[gid]['elements'])]
 assert len(memberships)==1,(id,memberships)
 gid=memberships[0];side,lobe,enlobe=lobes[gid]
 lobe_matches=[x for x in maprows if x['id']==gid and x['relation']=='part_of' and set(raw).issubset(x['objects'])]
 assert lobe_matches,gid
 sourceparts=[]
 for pid in c['elements']:
  p=parts[pid];r=catalog[pid.removeprefix('BP43-')]
  objpath=next(n for n in sourcezip.namelist() if '/'+r['fj_id']+'_' in n)
  head={}
  for line in sourcezip.read(objpath).decode().splitlines()[:10]:
   if line.startswith('# ') and ' : ' in line:
    k,v=line[2:].split(' : ',1);head[k]=v
  assert p['conceptId']==head['Concept ID']==id and p['name']==r['name']==c['name']==head['English name']
  sourceparts.append(dict(partId=pid,sourceObjectId=r['fj_id'],sourceName=r['name'],sourceFmaId=head['Concept ID'],sourceBpId=head['Representation ID'],objPath=objpath,objHeader=head,legacyCatalogAncestorFmaId=r['fma_id']))
 note='Kaynak segment parankiminin yüzey modelidir; bronş, damar veya segmentin tüm bileşenleri olarak adlandırılmaz.'
 if id=='FMA27368':note+=' Bu tek kavram iki kaynak yüzeyi birlikte içerir (FJ6595 ve FJ6597); iki ayrı segment kimliği oluşturulmaz.'
 e=dict(ids=[id],datasetId='male-body',sourceEnglish=c['name'],geometryPartIds=c['elements'],tr=f"{'Sol' if side=='left' else 'Sağ'} akciğer {lobe} lob — {segment} segment parankimi",en=c['name'],la=None,side=None,aliases=[f'{segment} bronkopulmoner segment parankimi',f'{side} {enlobe} lobe parenchyma'],expertReview='pending',trStatus='editorial',latinStatus='withheld_no_exact_parenchyma_scope_term',context=dict(side=side,lobeConceptId=gid,lobeSourceName=concepts[gid]['name']),scopeNoteTr=note,evidenceRef=f'source-evidence.json#{id}')
 if id in existing and existing[id].get('tr') and existing[id].get('en'):retained.append(dict(id=id,existing=existing[id]))
 else:entries.append(e)
 evidence.append(dict(id=id,sourceEnglish=c['name'],sourceParts=sourceparts,conceptMappingRows=matches,lobeMappingRows=[dict(line=x['line'],id=x['id'],relation=x['relation'],matchedObjects=raw) for x in lobe_matches],candidateLobeConcept=concepts[gid]))
ta=R/'work/open-assets-review/TA2.csv';assert sha(ta)=='0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
relevant=[]
for n,line in enumerate(ta.read_text().splitlines(),1):
 cols=line.strip().strip('"').split(';')
 if len(cols)>2 and cols[0].isdigit() and 3280<=int(cols[0])<=3314:relevant.append(dict(line=n,upstreamTableId=int(cols[0]),english=cols[1],latin=cols[2]))
assert not any('parenchyma' in x['english'].lower() for x in relevant)
write('proposals.json',dict(schemaVersion=1,status='proposal_only_not_applied',scope='17 segment-parenchyma concepts represented by 18 source surfaces; no aggregate lung/lobe labels added',entries=entries,retainExisting=retained,sidePolicy='Display TR already contains verified side and lobe, so entry.side is null to avoid duplicated prefixes. Original English source names are preserved exactly. Context/aliases add source-supported lobe information.',latinPolicy='Segment-only Latin terms do not translate parenchyma identities. All la fields null; no synthetic Latin parenchyma terms.'))
inputs=[S/'lung-parenchyma.json',S/'FMA2Obj.txt',S/'bp3d-v43-object-catalog.csv',S/'source-mapping-review.json',S/'source-fetch.json',S/'lung-parenchyma-source.zip',R/'data/anatomy/labels.json']
write('source-evidence.json',dict(schemaVersion=1,inputSnapshots=[dict(path=str(p.relative_to(R)),sha256=sha(p)) for p in inputs],officialSource=m['source'],mappingUrl='https://lifesciencedb.jp/bp3d/get-info.cgi?version=4.3&cmd=concept-objfiles-list',entries=evidence,latinReview=dict(path=str(ta.relative_to(R)),sha256=sha(ta),url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv',result='Nearby official-nomenclature segment terms were reviewed but none supplies the full parenchyma label. None copied into la.',relatedRowsNotUsedAsParenchymaTranslation=relevant),cautions=['Canonical FMA IDs are from OBJ Concept ID headers corroborated by FMA2Obj; legacy catalog fma_id FMA14065 is an ancestor, not the leaf identity.','Lobe membership uses the reviewed official4.3 part_of groups, not conflicting narrower parenchyma aggregates.','No missing segment, surface, S-number or Latin phrase inferred.','Editorial Turkish labels require expert review; label evidence does not establish geometric completeness.']))
assert len(entries)+len(retained)==17
assert sum(len(concepts[id]['elements']) for id in tr)==18
assert len(concepts['FMA27368']['elements'])==2
write('validation.json',dict(scopedConcepts=17,newTrEnRecords=len(entries),retainedExisting=len(retained),sourceSurfaceCount=18,exactObjHeaderIdentityAndNameMatches=18,exactConceptObjectMappingMatches=17,verifiedSingleLobeMemberships=17,nullLatin=len(entries),apicoposteriorConcept='FMA27368',apicoposteriorSurfaceIds=concepts['FMA27368']['elements'],sharedFilesWritten=False))
print('Validated',len(entries),'new TR/EN records;17 concepts,18 source surfaces;17 Latin withheld')
