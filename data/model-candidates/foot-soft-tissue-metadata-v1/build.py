"""Deterministic candidate metadata; writes only this owned directory, no network."""
import copy,hashlib,json,math,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
REV='9e649b6bef0e589a6caa8b7391e10a132a304cea'
read=lambda p:json.loads((ROOT/p).read_text());sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
paths={'mapping':'data/model-candidates/foot-soft-tissue-source-audit-v1/new-object-mapping.json','base':'public/models/atlas.json','knowledge':'data/anatomy/knowledge.json','activeLabels':'data/anatomy/labels.json','reference':'public/models/lower-limb-nerve-reference/atlas.json','referenceMetadata':'data/anatomy/lower-limb-reference.json','ta2':'work/open-assets-review/TA2.csv','names':'data/model-candidates/coverage-labels/bp3d-isa-parts-list-e.txt','membership':'data/model-candidates/concept-selection-review/isa_element_parts.txt','partofNames':'data/model-candidates/coverage-labels/bp3d-partof-parts-list-e.txt'}
paths['sourceEvaluation']='data/model-candidates/foot-soft-tissue-source-audit-v1/evaluated-candidates.json'
paths['producer']='data/model-candidates/foot-soft-tissue-metadata-v1/build.py'
evaluated=read(paths['sourceEvaluation']);evaluated_by_object={c['sourceObject']:c for c in evaluated['candidates']}
assert len(evaluated_by_object)==32
mapping=read(paths['mapping']);base=read(paths['base']);graph=read(paths['knowledge']);active=read(paths['activeLabels'])['entries'];reference=read(paths['reference']);refmeta=read(paths['referenceMetadata'])
assert base['source']=='BodyParts3D' and base['version']=='BodyParts3D 4.0'
assert len(mapping)==32 and len({m['conceptId'] for m in mapping})==32
concepts={c['id']:c for c in base['concepts']};byname={c['name']:c for c in base['concepts']};parts={p['id']:p for p in base['parts']};entities={e['id']:e for e in graph['entities']}
refconcepts={c['id']:c for c in reference['concepts']};refparts={p['id']:p for p in reference['parts']}
terms={}
for i,line in enumerate((ROOT/paths['ta2']).read_text().splitlines(),1):
 c=line.strip('"').split(';')
 if len(c)>2:terms[c[1]]=dict(id=c[0],en=c[1],la=c[2],csvLine=i)
names={}
for i,line in enumerate((ROOT/paths['names']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:names[c[0]]=dict(conceptId=c[0],representationId=c[1],name=c[2],line=i)
members={}
for i,line in enumerate((ROOT/paths['membership']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:members.setdefault(c[0],[]).append(dict(conceptId=c[0],name=c[1],partId=c[2],line=i))
tr={'(Opponens digiti minimi muscle of foot)':'Ayağın opponens digiti minimi kası','Abductor digiti minimi of foot':'Ayağın abductor digiti minimi kası','Abductor hallucis':'Abductor hallucis kası','Dorsal interossei muscles of foot':'Ayağın dorsal interosseöz kasları','Extensor digitorum brevis':'Extensor digitorum brevis kası','Extensor hallucis brevis':'Extensor hallucis brevis kası','Flexor digiti minimi of foot':'Ayağın flexor digiti minimi kası','Flexor digitorum brevis':'Flexor digitorum brevis kası','Lateral head of flexor hallucis brevis':'Flexor hallucis brevis kasının lateral başı','Medial head of flexor hallucis brevis':'Flexor hallucis brevis kasının medial başı','Lumbrical muscles of foot':'Ayağın lumbrikal kasları','Oblique head of adductor hallucis':'Adductor hallucis kasının oblik başı','Plantar interossei muscles':'Ayağın plantar interosseöz kasları','Quadratus plantae muscle':'Quadratus plantae kası','Sesamoid bones of foot':'Ayak sesamoid kemikleri','Transverse head of adductor hallucis':'Adductor hallucis kasının transvers başı'}
assert len(tr)==16
common_note='Kaynakta adlandırılmış kas nesnesi gösterilir; tüm ayak kasları, tendon kılıfları, innervasyon ağı veya kesin tutunma yüzeyleri bu seçimle doğrulanmaz. Anatomik uzman incelemesi bekliyor.'
def scope_kind(name):
 if name in ['Lumbrical muscles of foot','Dorsal interossei muscles of foot','Plantar interossei muscles']:return 'compound_muscle_group'
 if name=='Sesamoid bones of foot':return 'compound_sesamoid_group'
 if 'head of' in name:return 'muscle_head'
 return 'whole_named_muscle_object'
def main_names(name,side):
 if name=='Lumbrical muscles of foot':return [f'{ord} lumbrical of {side} foot' for ord in ['first','second','third','fourth']]
 if name=='Plantar interossei muscles':return [f'{ord} plantar interosseous of {side} foot' for ord in ['first','second','third']]
 if name=='Sesamoid bones of foot':return [f'sesamoid bone of {side} foot']
 if name=='(Opponens digiti minimi muscle of foot)':return [f'opponens digiti minimi of {side} foot']
 if name=='Flexor digiti minimi of foot':return [f'flexor digiti minimi brevis of {side} foot']
 if name=='Abductor digiti minimi of foot':return [f'abductor digiti minimi of {side} foot']
 if name=='Dorsal interossei muscles of foot':return []
 if name=='Quadratus plantae muscle':return [f'{side} flexor accessorius']
 if 'head of' in name:
  head,muscle=name.lower().split(' head of ');return [f'{head} head of {side} {muscle}']
 return [f'{side} {name.lower()}']
def core_label(name,side,ids,dataset,source_name):
 term=terms[name];assert term['id'].isdigit();kind=scope_kind(name);note=common_note
 if kind=='compound_muscle_group':note='Kaynak tek bir adlandırılmış kas grubu nesnesi sunar; numaralı kaslar bu seçimde bağımsız kimlik veya bağımsız seçim olarak doğrulanmaz. Grup bütünlüğü ve anatomik uzman incelemesi bekliyor.'
 if kind=='muscle_head':note='Yalnız kaynakta adlandırılmış kas başı gösterilir; bütün kasın etiketi veya ilişkileri otomatik olarak bu başa aktarılmaz. Anatomik uzman incelemesi bekliyor.'
 if kind=='compound_sesamoid_group':note='Kaynakta adlandırılmış ayak sesamoid kemikleri grubu gösterilir; tekil medial/lateral veya tibial/fibular kemik kimliği atanmaz. Anatomik uzman incelemesi bekliyor.'
 if name.startswith('('):note='Kaynağın parantezle işaretlediği kas kimliği korunur; varyasyonun sıklığı veya her bireyde bulunması iddia edilmez. Anatomik uzman incelemesi bekliyor.'
 unresolved=name=='Flexor digiti minimi of foot'
 return dict(ids=ids,datasetId=dataset,sourceEnglish=source_name,tr=tr[name],en=name.strip('()'),la=None if unresolved else term['la'],side=side,aliases=[source_name],ta2TableId=None if unresolved else int(term['id']),trStatus='editorial',expertReview='pending',anatomicalScope=kind,scopeNoteTr=note,representationNoteTr=note,latinUnavailableReason='Pinned numeric row2682 contains duplicated Latin pedis pedis; correction is not independently verified. Source text retained without making it a display term.' if unresolved else None,evidence=[dict(sourceId='zanatomy-ta2-pinned',locator=f'TA2 table row {term["id"]}; CSV line {term["csvLine"]}; exact English/Latin columns',scope='Source numeric term; not a formal FMA crosswalk')],sourceTerm=copy.deepcopy(term))
ref_labels=[];main_labels=[];targets=[];main_audit=[];seenmain=set()
for m in mapping:
 source=m['sourceObject'];name=source[:-2];side=m['side'];kind=scope_kind(name);assert name in tr and source.endswith('.'+side[0])
 label=core_label(name,side,[m['conceptId']],refmeta['datasetId'],name);label.update(sourceObject=source,componentRole=m['componentRole'],geometryPartIds=[m['partId']],sourceScope=m['scope'])
 geom=evaluated_by_object[source]['geometry'];topology=geom['topology']
 assert geom['selectableEvaluatedGeometry'] and geom['observedSide']==side
 label['sourceRepresentation']=dict(objectType=geom['sourceObjectType'],triangleConnectedComponents=topology['triangleConnectedComponents'],componentVertices=topology['componentVertices'],geometryReviewPath=paths['sourceEvaluation'],scope='Geometry connectivity only;not independent anatomical substructure identity')
 if name=='Lumbrical muscles of foot':
  label['scopeNoteTr']='Kaynak çoğul lumbrikal kas grubu adı taşır; geometri tek bağlı bileşendir. Dört ayrı veya numaralı lumbrikal kasın bağımsız temsili doğrulanmaz. Anatomik uzman incelemesi bekliyor.'
 elif name in ['Dorsal interossei muscles of foot','Plantar interossei muscles','Extensor digitorum brevis']:
  label['scopeNoteTr']+=f' Kaynak nesnede {topology["triangleConnectedComponents"]} bağlı geometri bileşeni vardır; bunlara ayrı numaralı kas/parmak kimliği atanmaz.'
 elif name=='Abductor hallucis':
  label['scopeNoteTr']+=' Kaynak yüzeyinde küçük bir geometri kusuru vardır; ayrı anatomik yapı sayılmaz.'
 label['representationNoteTr']=label['scopeNoteTr']
 label['aliases']=list(dict.fromkeys([source,name,name.strip('()')]))
 label['evidence'].append(dict(sourceId='zanatomy-lower-limb-source',locator=f'Z-Anatomy/Startup.blend object {source}; source mapping {paths["mapping"]}',scope='Named source object and side; export, quality and release acceptance remain separate'))
 if name.startswith('('):label['sourceParenthesizedIdentity']=True
 existing_reference=next((l for l in refmeta['labels'] if m['conceptId'] in l['ids']),None)
 assert existing_reference is None or existing_reference==label,'Conflicting integrated reference label '+m['conceptId']
 ref_labels.append(label)
 if m['conceptId'] in refconcepts:
  assert refconcepts[m['conceptId']]['elements']==[m['partId']]
  assert refparts[m['partId']]['sourceObject']==source
 candidates=[];queries=main_names(name,side)
 for query in queries:
  if query not in byname:continue
  c=byname[query];cid=c['id'];assert cid not in seenmain;seenmain.add(cid)
  assert names[cid]['name']==query and sorted(r['partId'] for r in members[cid])==sorted(c['elements'])
  assert all(r['name']==query for r in members[cid]);assert entities[cid]['geometryPartIds']==c['elements']
  observed=[parts[fj] for fj in c['elements']]
  for part in observed:
   assert part['conceptId']==cid and part['name'].lower()==query and part['vertexCount']>0 and part['indexCount']>0
   assert all(math.isfinite(n) for b in part['bounds'] for n in b)
  expected_count=2 if name=='Sesamoid bones of foot' else 1;assert len(observed)==expected_count
  binding=dict(datasetId='male-body',sourceVersion='BodyParts3D4.0',conceptId=cid,sourceName=query,partIds=c['elements'],sourceManifest=paths['base'],locator=f'concepts/{cid}',officialNameRow=names[cid],officialMembershipRows=members[cid],observedParts=observed,confidence='exact_source_name_and_manifest_membership_verified;geometry_anatomy_not_assessed',scopeCorrespondence='Named constituent of source group;no new main aggregate concept created' if kind=='compound_muscle_group' else 'Named source object/head or existing sesamoid concept;independent source frame')
  if name=='Quadratus plantae muscle':binding['termCorrespondenceEvidence']=dict(sourceId='ta98-quadratus-plantae-synonym',locator='A04.7.02.068; Quadratus plantae; Flexor accessorius',scope='Explicit terminology synonym, paired with actual manifest membership;not same specimen or same geometry')
  candidates.append(binding);main_audit.append(binding)
  ml=core_label(name,side,[cid],'male-body',query);ml['evidence'] += [dict(sourceId='foot-soft-tissue-bp3d40-names',locator=f'line {names[cid]["line"]}; {cid}'),dict(sourceId='foot-soft-tissue-bp3d40-membership',locator='; '.join('line '+str(r['line']) for r in members[cid]))]
  ml['aliases']=list(dict.fromkeys([query,ml['en'].lower()]))
  if kind=='compound_muscle_group':
   ordinal=query.split()[0];number={'first':1,'second':2,'third':3,'fourth':4}[ordinal];stem='lumbrikal' if 'lumbrical' in query else 'plantar interosseöz'
   ml.update(tr=f'Ayağın {number}. {stem} kası',en=query.replace(side+' ',''),la=None,ta2TableId=None,anatomicalScope='numbered_individual_muscle',muscleNumber=number,genericTerm=copy.deepcopy(terms[name]),latinUnavailableReason='Only a plural whole-group numeric TA2 term was verified;no exact numbered individual Latin term verified. Do not singularize or append an inferred numeral.',scopeNoteTr='Kaynakta ayrı adlandırılmış numaralı kas parçası gösterilir; kas grubu etiketi ve ilişkileri otomatik devralınmaz. Anatomik uzman incelemesi bekliyor.',representationNoteTr='Kaynakta ayrı adlandırılmış numaralı kas parçası gösterilir; kas grubu etiketi ve ilişkileri otomatik devralınmaz. Anatomik uzman incelemesi bekliyor.')
  if name=='Quadratus plantae muscle':
   ml['evidence'].append(dict(sourceId='ta98-quadratus-plantae-synonym',locator='A04.7.02.068; Quadratus plantae; Flexor accessorius'))
   ml['aliases'].extend(['Flexor accessorius','Quadratus plantae'])
   ml['sourceTermCorrespondence']='Official TA98 explicit synonym connects retained main flexor accessorius name to quadratus plantae;no source ID or geometry equivalence alteration.'
  if name=='Flexor digiti minimi of foot':ml.update(tr='Ayağın flexor digiti minimi brevis kası',en='Flexor digiti minimi brevis of foot',sourceTermCorrespondence='Main source specifies brevis;reference/TA2 table title omits brevis. Candidate terminology correspondence pending expert review;never merge geometry or IDs.')
  if name=='Sesamoid bones of foot':ml.update(anatomicalScope='rendered_source_sesamoid_group',sourceTermCorrespondence='Main source concept is singular but selects2sesamoid pieces. Plural TA2 display label describes this rendered group, without changing source concept identity or assigning individual sesamoid identities.',scopeNoteTr='Kaynak kavramı tekil ad taşısa da bu seçim iki ayrı sesamoid kemik parçasını içerir; tekil medial/lateral kimlik atanmaz. Anatomik uzman incelemesi bekliyor.',representationNoteTr='Kaynak kavramı tekil ad taşısa da bu seçim iki ayrı sesamoid kemik parçasını içerir; tekil medial/lateral kimlik atanmaz. Anatomik uzman incelemesi bekliyor.')
  existing=next((l for l in active if cid in l['ids']),None);assert existing is None or existing==ml,'Conflicting integrated main label '+cid
  main_labels.append(ml)
 tid='foot-soft-tissue-v1:'+m['conceptId'].split(':',1)[1]
 targets.append(dict(id=tid,regionId='leg-ankle-foot',familyId='skeletal-support' if name=='Sesamoid bones of foot' else 'muscle-tendon-fascia',side=side,requiredDetail='D2' if kind=='muscle_head' else 'D1',targetKind=kind,scope=name,requirementStatus='non_exhaustive_source_named_target;curriculum_and_expert_pending',terminology=dict(sourceNumericTerm=terms[name],formalFmaCrosswalk='not_asserted',latinDisplayStatus='withheld_source_typography_unresolved' if label['la'] is None else 'exact_numeric_source_term'),representations=[dict(datasetId=refmeta['datasetId'],conceptId=m['conceptId'],sourceObject=source,partIds=[m['partId']],mappingPath=paths['mapping'],status='evaluated_source_object_identity;export_and_release_acceptance_owned_by_geometry_task',sourceScope=m['scope'],coverageStatus='source_group_only;numbered_subdivision_coverage_unresolved' if 'compound' in kind else 'named_source_scope;anatomical_acceptance_pending')]+candidates,mainNameQueries=queries,mainBindingStatus='observed_existing_source_bindings' if candidates else 'no_positive_binding_in_bounded_name_manifest_audit;not_absence',compoundLimits='Numbered subdivisions are not independently verified in this source object' if 'compound' in kind else None,expertReview='pending',anatomicallyAccepted=False,absenceClaim=False,openCriteria=['Source mesh/detail review','Head/group identity scope review','Source-specific user journey and meaningful context','Expert anatomy acceptance']))
# Primary teaching facts apply only to these two explicitly named whole muscles.
source_id='ttuhsc-anterior-lateral-leg-foot-tables'
relations=[]
for side in ['left','right']:
 letter=side[0];calc_ref=f'zanatomy:calcaneus-{letter}';prox_ref=f'zanatomy:proximal-phalanx-of-first-finger-of-foot-{letter}'
 calc_main='FMA24498' if side=='left' else 'FMA24497';prox_main='FMA43254' if side=='left' else 'FMA43253'
 for name,origin_tr,insertion_tr,nerve in [('Abductor hallucis','Kalkaneus tüberositesinin medial bölümü','Başparmağın proksimal falanks tabanının medial bölümü','medial-plantar'),('Extensor hallucis brevis','Kalkaneusun üst-dış yüzü','Başparmağın proksimal falanks tabanının dorsal bölümü','deep-fibular')]:
  m=next(m for m in mapping if m['sourceObject']==name+'.'+letter);maincid=byname[side+' '+name.lower()]['id']
  for dataset,muscle,bone1,bone2 in [(refmeta['datasetId'],m['conceptId'],calc_ref,prox_ref),('male-body',maincid,calc_main,prox_main)]:
   for predicate,target,column,region in [('originates_at',bone1,'Origin',origin_tr),('inserts_at',bone2,'Insertion',insertion_tr)]:
    relations.append(dict(id=f'{muscle}|{predicate}|{target}',datasetId=dataset,subject=muscle,predicate=predicate,object=target,status='source_supported',expertReview='pending',scope='selected_typical_anatomy;non_exhaustive',evidence=[dict(sourceId=source_id,locator=f'Muscles table; {name.lower()} row; {column} column')],qualifiers=dict(laterality='Same-side instantiation of unsided educational fact;not specimen validated',landmarkTr=region,attachmentNoteTr=region+' — kesin model yüzey işareti yok',targetRole='context_bone',semantics='Named attachment region on a whole-bone context target;not a complete-bone attachment footprint',geometry='No anchor, coordinates, footprint segmentation or mesh contact asserted',requiresLandmarkDisplay=True)))
  nerveid=f'atlas:{side}-{nerve}-nerve'
  relations.append(dict(id=f'{nerveid}|innervates|{m["conceptId"]}',datasetId=refmeta['datasetId'],subject=nerveid,predicate='innervates',object=m['conceptId'],status='source_supported',expertReview='pending',scope='selected_typical_anatomy;non_exhaustive',evidence=[dict(sourceId=source_id,locator=f'Muscles table; {name.lower()} row; Innervation column')],qualifiers=dict(laterality='Same-side instantiation of directly named muscle supply;not specimen validated',semantics='Directly named educational motor-supply fact for this muscle;not inherited from a muscle group or parent',modeledMotorBranch=False,geometry='No motor entry point, neural branch trajectory or contact asserted')))
assert len(main_labels)==38 and len(main_audit)==38 and len(ref_labels)==32 and len(targets)==32 and len(relations)==20
assert len({p for r in main_audit for p in r['partIds']})==40
assert sum(r['la'] is not None for r in ref_labels)==30
assert sum(r['la'] is not None for r in main_labels)==22
refids=set(refconcepts)|{m['conceptId'] for m in mapping};mainids=set(concepts)
for r in relations:
 if r['datasetId']==refmeta['datasetId'] and r['qualifiers'].get('attachmentNoteTr'):
  r['attachmentNoteTr']=r['qualifiers']['attachmentNoteTr']
 ids=refids if r['datasetId']==refmeta['datasetId'] else mainids;assert r['subject'] in ids and r['object'] in ids
 existing_relations=graph['relations'] if r['datasetId']=='male-body' else refmeta['relations']
 for existing in existing_relations:
  if existing['id']==r['id']:
   expected={k:v for k,v in r.items() if k!='datasetId'}
   actual={k:v for k,v in existing.items() if k!='datasetId'}
   assert actual==expected,'Conflicting integrated relation '+r['id']
assert len({(r['datasetId'],r['id']) for r in relations})==20
sources=[dict(id='zanatomy-ta2-pinned',title='Pinned Z-Anatomy-distributed TA2 table',url=refmeta['sources'][0]['url'],path=paths['ta2'],sha256=sha(paths['ta2']),use='Exact numeric terms only;no plural→numbered individual transformation;row2682 Latin withheld'),dict(id='zanatomy-lower-limb-source',title='Pinned Z-Anatomy named source objects',url='https://github.com/Z-Anatomy/Models-of-human-anatomy',member='Z-Anatomy/Startup.blend',sourceArtifactSha256='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd',mappingPath=paths['mapping'],use='Source object name,side and head/group scope;license/geometry acceptance owned by source package'),dict(id='foot-soft-tissue-bp3d40-names',title='Retained official BodyParts3D4.0 archive names',url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt',path=paths['names']),dict(id='foot-soft-tissue-bp3d40-membership',title='Retained official BodyParts3D4.0 element memberships',url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt',path=paths['membership']),dict(id=source_id,title='TTUHSC Anatomy Tables — Anterior & Lateral Leg & Foot',url='https://anatomy.ttuhscep.edu/musculoskeletal_system/leg_tables.html',retrievedOn='2026-10-02',locator='Muscles table; abductor hallucis and extensor hallucis brevis rows; Origin,Insertion,Innervation columns',use='Six selected factual cells; no table redistribution;unsided educational descriptions,not specimen validation',fetchStatus='Successful web read;no access restriction or authentication required')]
sources.append(dict(id='ta98-quadratus-plantae-synonym',title='University of Fribourg TA98 terminology — lower limb muscles',url='https://svx-uo7640ifaa2.unifr.ch/Public/EntryPage/TA98%20Tree/TA98%20EN/04.7.02%20TA98%20EN.htm',retrievedOn='2026-10-02',locator='A04.7.02.068; English and Latin synonym columns',use='Explicit quadratus plantae/flexor accessorius synonym only;Latin display remains pinned numeric TA2 row2684',fetchStatus='Primary-source indexed search result read;direct page fetch returned502. TTUHSC TA2 PDF direct read also timed out;no access restriction bypassed.'))
sourceids={s['id'] for s in sources}
for r in ref_labels+main_labels+relations:assert all(e['sourceId'] in sourceids for e in r['evidence'])
result=dict(schemaVersion=1,scopeVersion='foot-soft-tissue-metadata-v1',sourceRevision=REV,reviewedOn='2026-10-02',status='source_audit_proposal;activation_and_release_owned_by_root',scope='Non-exhaustive intrinsic foot muscle/source-group and foot sesamoid candidates;compound and head identity preserved',summary=dict(referenceLabels=32,referenceMuscleObjects=30,referenceSesamoidGroups=2,referenceCompoundMuscleGroups=6,referenceHeadObjects=8,mainLabels=38,mainMuscleConcepts=36,mainSesamoidConcepts=2,mainParts=40,targets=32,targetsWithMainEvidence=28,referenceLatinPresent=30,referenceLatinUnresolved=2,mainLatinPresent=22,mainLatinUnresolved=16,referenceRelations=12,mainRelations=8,anatomicallyAccepted=0),referenceLabelProposals=ref_labels,mainLabelProposals=main_labels,targetProposals=targets,relationProposals=relations,mainBindingAudit=main_audit,sources=sources,inputSnapshots=[dict(path=v,sha256=sha(v)) for v in paths.values()],limits=['Source groups are not counted as independently selected numbered muscles','FHB and adductor heads retain separate identities;no whole-muscle relationship inheritance','Reference groups and main numbered sources are distinct manifestations;no same-geometry claim','No positive main EDB/dorsalinterossei correspondence found in bounded audit;not an absence claim','No model footprints,coordinates,attachment contact,motor entry points or inferred motor branches','No per-sesamoid medial/lateral identity invented','Existing104target list and active files are not edited by this producer','Expert and release acceptance remain separate'])
encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n';dest=OUT/'proposal.json'
if '--check' in sys.argv:
 assert dest.read_text()==encoded,'Candidate differs from current retained inputs';print('PASS deterministic 32 reference / 38 main labels / 32 targets / 20 relations; exact source members; scope and Latin assertions')
else:dest.write_text(encoded);print('Wrote proposal.json;source assertions passed')
