"""Reproduce the bounded metadata proposal from retained inputs; no network or activation."""
import csv, hashlib, json, re, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads((ROOT/p).read_text())
base=read('public/models/atlas.json'); graph=read('data/anatomy/knowledge.json')
seed=read('data/anatomy/regional-targets-lower-limb-v1.json')
# The audited identities remain fixed after another dataset binds geometry.
# Current representation status must not redefine a historical BP3D audit.
audited_terms={6579,6574,6586,6590,6593,4727,1919,1920,1921}
targets=[t for t in seed['targets'] if t['terminology']['ta2TableId'] in audited_terms]
assert len(targets)==18
registry=read('public/models/extensions/index.json')
manifest_paths=['public/models/atlas.json']+['public'+p for p in registry['manifests']]
manifests={p:read(p) for p in manifest_paths}
patterns={6579:r'deep[ -]+(?:fibular|peroneal)[ -]+nerve',6574:r'superficial[ -]+(?:fibular|peroneal)[ -]+nerve',6586:r'sural[ -]+nerve',6590:r'medial[ -]+plantar[ -]+nerve',6593:r'lateral[ -]+plantar[ -]+nerve',4727:r'(?:fibular|peroneal)[ -]+artery',1919:r'anterior[ -]+(?:talofibular|talo[ -]fibular|fibulotalar)[ -]+ligament',1920:r'posterior[ -]+(?:talofibular|talo[ -]fibular|fibulotalar)[ -]+ligament',1921:r'(?:calcaneofibular|calcaneo[ -]fibular|fibulocalcaneal)[ -]+ligament'}
name_paths=['data/model-candidates/coverage-labels/bp3d-isa-parts-list-e.txt','data/model-candidates/coverage-labels/bp3d-partof-parts-list-e.txt']
catalog_path='data/model-candidates/lung-surfaces/bp3d-v43-object-catalog.csv'
catalog=list(csv.DictReader((ROOT/catalog_path).open()))
mapping_path='data/model-candidates/lung-surfaces/bp3d-v43-mapping.zip'
with zipfile.ZipFile(ROOT/mapping_path) as z:payload=z.read('FMA2Obj.txt')
mapping=[]
for i,line in enumerate(payload.decode().splitlines(),1):
 if not line.startswith('#'):
  concept,tree,parts=line.split('\t');mapping.append(dict(conceptId=concept,tree=tree,partIds=parts.split('+'),line=i))
assert payload.startswith(b'# Data Version\t4.3')
assert hashlib.sha256(payload).hexdigest()=='c3d16c891016da13447de2fc3241d05d92e8f9dc460e363233c03f420b935d4f'
source_records=[]
for ident in ['FMA43922','FMA43923','FMA43921','FMA43901']:
 p=OUT/'source'/f'{ident}.json'
 source_records.append(dict(id='bp3d43-'+ident,url=f'https://lifesciencedb.jp/bp3d/get-fmastratum.cgi?version=4.3&lng=en&t_type=4&bul_id=4&cb_id=5&ci_id=1&md_id=1&mv_id=6&mr_id=1&f_id={ident}',retrievedOn='2026-10-02',path=str(p.relative_to(ROOT)),sha256=sha(p),sourceDataVersion='4.3',sourceTreeVersion='FMA3.0'))
unsided=json.loads((OUT/'source/FMA43921.json').read_text())['images'][0]
assert unsided['name']=='Peroneal artery'
assert unsided['partof_path2root'][0]['fma'][0]['name_l']=='Arteria fibularis'
parts={p['id']:p for p in base['parts']}; proposals=[];relations=[]
with zipfile.ZipFile(OUT/'source/artery-source.zip') as z:
 obj_headers={}
 for name in z.namelist():
  if name.endswith('.obj'):
   body=z.read(name); fields={}
   for line in body.decode().splitlines():
    m=re.match(r'# ([^:]+?)\s*:\s*(.*)',line)
    if m:fields[m[1].strip()]=m[2]
   obj_headers[fields['File ID']]=dict(member=name,sha256=hashlib.sha256(body).hexdigest(),fields=fields)
for target in targets:
 tid=target['terminology']['ta2TableId'];pattern=re.compile(patterns[tid],re.I)
 matches=[]
 for path,manifest in manifests.items():
  for key in ['concepts','parts']:
   matches.extend(dict(path=path,collection=key,record=r) for r in manifest.get(key,[]) if pattern.search(r.get('name','')))
 graph_matches=[r for r in graph['entities'] if pattern.search(r['name'])]
 table_matches=[dict(path=p,line=i,text=line) for p in name_paths for i,line in enumerate((ROOT/p).read_text().splitlines(),1) if pattern.search(line)]
 catalog_matches=[r for r in catalog if pattern.search(r['name'])]
 line=int(re.search(r'line (\d+)',target['terminology']['locator'])[1]);c=(ROOT/'work/open-assets-review/TA2.csv').read_text().splitlines()[line-1].strip('"').split(';')
 assert [int(c[0]),c[1],c[2]]==[tid,target['terminology']['en'],target['terminology']['la']]
 result=dict(targetId=target['id'],side=target['side'],requiredDetail=target['requiredDetail'],terminology=target['terminology'],searchedNamePattern=patterns[tid],searchEvidence=dict(activeManifestMatches=matches,knowledgeEntityMatches=graph_matches,archiveNameTableMatches=table_matches,bp3d43DiscoveryCatalogMatches=catalog_matches),absenceClaim=False,acceptedRepresentations=[],proposedRepresentations=[],expertReview='pending',status='unresolved_in_bounded_bp3d_audit',confidence='No positive identity binding established; zero textual matches do not establish absence',scopeLimits=['No mesh/subobject visual inspection or global absence conclusion','Source naming is not proof of detail, continuity, attachment or anatomical accuracy'])
 if tid==4727:
  side=target['side'];cid,fj,parent=('FMA43923','FJ2093','FMA43899') if side=='left' else ('FMA43922','FJ2197','FMA43898')
  im=json.loads((OUT/'source'/f'{cid}.json').read_text())['images'][0]
  h=obj_headers[fj];assert h['fields']['Concept ID']==cid and h['fields']['Compatibility version']=='4.3'
  rows=[r for r in mapping if r['conceptId']==cid];assert all(r['partIds']==[fj] for r in rows)
  path=im['partof_path2root'][0]['fma'];assert [r['f_id'] for r in path[:2]]==[cid,parent]
  assert [r['potname'] for r in path[0]['potype']]==['regional_part_of']
  result.update(status='verified_bp3d43_source_candidate_with_base_version_identity_conflict',confidence='High for 4.3 source identity/membership and unsided Latin correspondence; active 4.0 geometry-equivalence unverified',proposedRepresentations=[dict(datasetId='bodyparts3d-4.3-source-candidate',activationStatus='inactive; no main-body binding accepted',conceptId=cid,sourceName=im['name'],sourcePartIds=[fj],sourceVersion='4.3',membershipEvidence=rows,objHeader=h,terminologyCorrespondence=dict(unsidedConceptId='FMA43921',sourceEnglish='Peroneal artery',sourceLatin='Arteria fibularis',ta2TableId=4727,ta2English='Fibular artery',ta2Latin='Arteria fibularis',basis='Exact common Latin term plus explicit lateralized is_a descendants; source-backed terminology correspondence, not a published TA2/FMA crosswalk'))],existingBaseDiscrepancy=dict(datasetId='male-body',sourceVersion='4.0',part=parts[fj],sourceConcept=next(c for c in base['concepts'] if c['id']=='FMA70801'),verifiedOldTableLocator='data/model-candidates/concept-selection-review/isa_element_parts.txt lines 24504–24507',decision='Preserve active source identity pending version-specific geometry/semantic review; shared FJ identifier does not establish geometry-equivalence'))
  relations.append(dict(id=f'{cid}|part_of|{parent}',subject=cid,predicate='part_of',object=parent,datasetId='bodyparts3d-4.3-source-candidate',status='proposed_source_imported_not_active',expertReview='pending',sourcePredicate='regional_part_of',evidence=[dict(sourceId='bp3d43-'+cid,locator='images/0/partof_path2root/0/fma/0..1; child potype regional_part_of')],qualifiers=dict(directSourceParent=True,sourceDataVersion='4.3',sourceTreeVersion='FMA3.0',notBranchOfAssertion=True,physicalContinuityClaim=False,scope='Source ontology hierarchy; no inferred attachment, supply territory or geometry completeness')))
 elif tid in [1919,1920,1921]:
  result['nonEquivalentNearbyRepresentations']=[dict(datasetId='male-body',conceptId='FMA44250' if target['side']=='left' else 'FMA44249',sourceName=target['side']+' long plantar ligament',partIds=['FJ1424M' if target['side']=='left' else 'FJ1424'],decision='Different anatomical structure; do not bind an ankle collateral ligament target to long plantar ligament geometry')]
 proposals.append(result)
inputs=['data/anatomy/regional-targets-lower-limb-v1.json','scripts/build-lower-limb-targets.py','data/anatomy/knowledge.json','work/open-assets-review/TA2.csv',catalog_path,mapping_path,*name_paths,'data/model-candidates/concept-selection-review/isa_element_parts.txt',*manifest_paths]
result=dict(schemaVersion=1,reviewedOn='2026-10-02',sourceRevision='e879fc92e1bfa6226898d12cdca2863e365858e0',status='candidate_only_no_activation',scope='18 unbound targets from lower-limb-target-seed-v1; existing main manifest, knowledge graph and pinned BP3D metadata audit',summary=dict(targets=18,verifiedBp3d43Candidates=2,unresolvedWithinAudit=16,acceptedNewMainBindings=0,proposedSourceRelations=2),targets=proposals,relations=relations,labelProposals=[],labelDecision='Artery Latin correspondence verified, but no active label recommendation until dataset identity/geometry review; other target bindings unresolved in this audit',sources=source_records,inputSnapshots=[dict(path=p,sha256=sha(ROOT/p)) for p in inputs],mappingPayloadSha256=hashlib.sha256(payload).hexdigest(),geometryDownload=dict(path=str((OUT/'source/artery-source.zip').relative_to(ROOT)),sha256=sha(OUT/'source/artery-source.zip'),request='source/artery-request.json',retrievedOn='2026-10-02',inspection='Canonical OBJ headers only; no geometry comparison performed',license='CC BY-SA 2.1 Japan per retained official live-source license evidence; not the base4.0 archive license',licenseEvidence=dict(path='data/model-candidates/lung-surfaces/bp3d-live-license.html',sha256=sha(ROOT/'data/model-candidates/lung-surfaces/bp3d-live-license.html'),url='https://lifesciencedb.jp/bp3d/info/license/index.html',verification='Reused retained snapshot; not fetched anew for this task'),attribution='BodyParts3D, © 2008 Database Center for Life Science (DBCLS)'),notAsserted=['No absence in all sources','No geometry-equivalence from shared FJ number across versions','No accepted main-atlas source correction','No branch_of inference from regional_part_of or membership','No ankle ligament substitution with long plantar ligament','No new source geometry release or anatomical expert acceptance'])
result['scope']='18 fixed target identities initially unbound at e879fc9; BP3D-only metadata audit independent of later Z-Anatomy bindings'
result['sourceRevisionNote']='Discovery baseline revision; inputSnapshots pin the current local verification inputs. Active reference bindings do not turn these BP3D candidates into accepted main-body mappings.'
result['inputSnapshots'].append(dict(path=str(Path(__file__).resolve().relative_to(ROOT)),sha256=sha(Path(__file__).resolve())))
content=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if '--check' in sys.argv:
 assert (OUT/'proposal.json').read_text()==content, 'proposal is stale; regenerate the bounded audit'
else:
 (OUT/'proposal.json').write_text(content)
assert len(proposals)==18 and len({p['targetId'] for p in proposals})==18
assert sum(bool(p['proposedRepresentations']) for p in proposals)==2
assert all(not p['acceptedRepresentations'] for p in proposals)
print('PASS: 18 unique targets;2 verified4.3 source candidates;16 unresolved;0 accepted main bindings;2 sourced regional_part_of proposals;9 exact TA2 term pairs;all part/header/mapping assertions.')
