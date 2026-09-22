"""17 lung segment intermediate-node labels; candidate-only writes."""
from pathlib import Path
import json,csv,hashlib
H=Path(__file__).resolve().parent;R=H.parents[2]
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda n,x:(H/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
modulepath=R/'data/model-candidates/lung-parenchyma-relations/module-proposal.json';module=read(modulepath)
atlaspath=R/'public/models/atlas.json';atlas=read(atlaspath);concepts={x['id']:x for x in atlas['concepts']};parts={x['id']:x for x in atlas['parts']}
previouspath=R/'data/model-candidates/lung-parenchyma-labels/proposals.json';previous={e['ids'][0]:e for e in read(previouspath)['entries']}
labelsPath=R/'data/anatomy/labels.json';existing={i:e for e in read(labelsPath)['entries'] for i in e['ids']}
ta=R/'work/open-assets-review/TA2.csv';assert sha(ta)=='0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
terms={}
for n,line in enumerate(ta.read_text().splitlines(),1):
 c=line.strip().strip('"').split(';')
 if len(c)>2 and c[0].isdigit():terms[int(c[0])]=dict(upstreamTableId=int(c[0]),english=c[1],latin=c[2],line=n)
spec={'FMA7372':3301,'FMA7380':3314,'FMA7373':3302,'FMA7374':3305,'FMA7375':3306,'FMA7376':3309,'FMA7378':3312,'FMA7379':3313,'FMA7338':3285,'FMA7362':3298,'FMA7339':3286,'FMA7359':3287,'FMA7361':3290,'FMA7360':3291,'FMA7366':3294,'FMA7364':3296,'FMA7363':3297}
official={};sources=[]
for tree in ['isa','partof']:
 p=R/f'data/model-candidates/concept-selection-review/{tree}_parts_list_e.txt';sources.append(dict(path=str(p.relative_to(R)),sha256=sha(p),url=f'https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/{tree}_parts_list_e.txt'))
 for n,c in enumerate(csv.DictReader(p.open(),delimiter='\t'),2):official.setdefault(c['concept id'],[]).append(dict(line=n,path=str(p.relative_to(R)),english=c['en'],representationId=c['representation id']))
entries=[];evidence=[];retained=[]
relations=[r for r in module['relations'] if r['object'] in spec]
assert len(relations)==len({r['object'] for r in relations})==17
for rel in relations:
 id=rel['object'];c=concepts[id];term=terms[spec[id]];parent=previous[rel['subject']]
 refs=[x for x in official[id] if x['english'].casefold()==c['name'].casefold()];assert refs
 assert rel['qualifiers']['laterality']==parent['context']['side']
 expectedSide='left' if 'sinistri' in term['latin'] else 'right' if 'dextri' in term['latin'] else None
 assert expectedSide==rel['qualifiers']['laterality']
 tr=parent['tr'].removesuffix(' parankimi');assert tr.endswith('segment')
 en=c['name'][0].upper()+c['name'][1:]
 note='Bu segment kavramı mevcut bronş ve damar yüzeylerini birlikte seçer. Segment parankimi ayrı bir alt kavramdır; ilişki etiketi mevcut geometri üyeliğini değiştirmez.'
 e=dict(ids=[id],datasetId='male-body',sourceEnglish=c['name'],geometryPartIds=c['elements'],tr=tr,en=en,la=term['latin'],side=None,aliases=[c['name'],tr.replace(' — ',' ')],ta2TableId=term['upstreamTableId'],expertReview='pending',trStatus='editorial',context=parent['context'],scopeNoteTr=note,evidenceRef=f'source-evidence.json#{id}')
 if id in existing and existing[id].get('tr') and existing[id].get('en'):retained.append(dict(id=id,existing=existing[id]))
 else:entries.append(e)
 evidence.append(dict(id=id,sourceEnglish=c['name'],bp3d=refs,ta2=term,sourceParentRelation=rel,baseGeometry=[dict(id=p,name=parts[p]['name'],conceptId=parts[p]['conceptId']) for p in c['elements']],semanticMapping='Bronchopulmonary segment itself, not its parenchyma; exact lateralized TA2 segment term. TA2 numbering retained exactly as written.',parenchymaConceptId=rel['subject']))
assert len(entries)+len(retained)==17
write('proposals.json',dict(schemaVersion=1,status='proposal_only_not_applied',scope='17 existing bronchopulmonary segment intermediate nodes only; no lung/lobe/parenchyma labels',entries=entries,retainExisting=retained,sidePolicy='TR and Latin already contain source-supported side. side:null avoids duplicate prefixes; original source English is retained.',geometryPolicy='geometryPartIds is the unchanged current base-concept membership snapshot; labels must not rebind or replace geometry.'))
inputs=[modulepath,atlaspath,previouspath,labelsPath,R/'app/atlas-metadata.ts']
write('source-evidence.json',dict(schemaVersion=1,inputSnapshots=[dict(path=str(p.relative_to(R)),sha256=sha(p)) for p in inputs],sources=sources+[dict(path=str(ta.relative_to(R)),sha256=sha(ta),url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv')],entries=evidence,cautions=['Exact Latin strings are from pinned upstream TA2 distribution, not fresh publisher-PDF verification of all17.','Table IDs are upstream CSV identifiers.','Segment numerals occur in exact TA2 Latin; no additional reconstructed segment, geometry or relation inferred.','Parent parenchyma labels remain Latin-null; these Latin terms must not be copied to the parenchyma IDs.','Source geometry membership and scientific completeness are not validated by a label match.']))
write('validation.json',dict(scopedSegmentIds=17,matchingRelationObjects=17,newTrEnLaRecords=len(entries),retainedExisting=len(retained),exactBp3dIdNameMatches=17,exactLatinStringMatches=17,lateralityMatches=17,unchangedBaseGeometrySets=17,ignoredAlreadyLabeledLungObjects=['FMA7309','FMA7310'],sharedFilesWritten=False))
print('Validated',len(entries),'new TR/EN/LA records;17 source matches,17 Latin matches')
