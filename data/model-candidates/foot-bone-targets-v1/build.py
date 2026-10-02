"""Deterministic, offline candidate audit; writes only beside this script."""
import copy, hashlib, json, math, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
REVISION='41723bdf937ce50976c118230b0a29441700d4a2'
read=lambda p:json.loads((ROOT/p).read_text())
sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
paths={'base':'public/models/atlas.json','reference':'public/models/lower-limb-nerve-reference/atlas.json','referenceLabels':'data/anatomy/lower-limb-reference.json','labels':'data/anatomy/labels.json','knowledge':'data/anatomy/knowledge.json','terms':'work/open-assets-review/TA2.csv','names':'data/model-candidates/coverage-labels/bp3d-isa-parts-list-e.txt','membership':'data/model-candidates/concept-selection-review/isa_element_parts.txt','relations':'data/anatomy/vendor/bodyparts3d/partof_inclusion_relation_list.txt'}
paths.update(parentNames='data/model-candidates/coverage-labels/bp3d-partof-parts-list-e.txt',parentMembership='data/model-candidates/concept-selection-review/partof_element_parts.txt',producer=str(Path(__file__).resolve().relative_to(ROOT)))
base=read(paths['base']);ref=read(paths['reference']);metadata=read(paths['referenceLabels']);graph=read(paths['knowledge']);active_labels=read(paths['labels'])['entries']
concepts={r['id']:r for r in base['concepts']};parts={r['id']:r for r in base['parts']};byname={r['name']:r for r in base['concepts']}
refconcepts={r['id']:r for r in ref['concepts']};refparts={r['id']:r for r in ref['parts']};entities={r['id']:r for r in graph['entities']}
terms={}
for i,line in enumerate((ROOT/paths['terms']).read_text().splitlines(),1):
 c=line.strip('"').split(';')
 if len(c)>2:terms[c[1]]=dict(sourceRowId=c[0],en=c[1],la=c[2],csvLine=i)
name_rows={}
for i,line in enumerate((ROOT/paths['names']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:name_rows[c[0]]=dict(conceptId=c[0],representationId=c[1],name=c[2],line=i)
member_rows={}
for i,line in enumerate((ROOT/paths['membership']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:member_rows.setdefault(c[0],[]).append(dict(conceptId=c[0],name=c[1],partId=c[2],line=i))
parent_name_rows={}
for i,line in enumerate((ROOT/paths['parentNames']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:parent_name_rows[c[0]]=dict(conceptId=c[0],representationId=c[1],name=c[2],line=i)
parent_member_rows={}
for i,line in enumerate((ROOT/paths['parentMembership']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:parent_member_rows.setdefault(c[0],[]).append(dict(conceptId=c[0],name=c[1],partId=c[2],line=i))
relrows=[]
for i,line in enumerate((ROOT/paths['relations']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==4:relrows.append(dict(parent=c[0],parentName=c[1],child=c[2],childName=c[3],line=i))
ordinal={1:'first',2:'second',3:'third',4:'fourth',5:'fifth'};toe={1:'big',2:'second',3:'third',4:'fourth',5:'little'}
reference_labels=sorted([r for r in metadata['labels'] if r.get('digit')],key=lambda r:(r['side'],r['digitSystem'],r['digit'],r.get('phalanxPosition','')))
assert len(reference_labels)==38
records=[];mainlabels=[];relationship_records=[];parents={}
for r in reference_labels:
 side,digit=r['side'],r['digit'];position=r.get('phalanxPosition');family='phalanx' if position else 'metatarsal'
 expected=f'{position} phalanx of {side} {toe[digit]} toe' if position else f'{side} {ordinal[digit]} metatarsal bone'
 assert expected in byname,expected
 concept=byname[expected];cid=concept['id'];members=concept['elements'];assert len(members)==1
 part=parts[members[0]];assert part['conceptId']==cid and part['name'].lower()==expected
 assert part['vertexCount']>0 and part['indexCount']>0 and part['indexCount']%3==0 and all(math.isfinite(n) for b in part['bounds'] for n in b)
 assert members==entities[cid]['geometryPartIds']
 assert name_rows[cid]['name']==expected
 assert sorted(x['partId'] for x in member_rows[cid])==members and all(x['name']==expected for x in member_rows[cid])
 refcid=r['ids'][0];refc=refconcepts[refcid];assert len(refc['elements'])==1
 refpart=refparts[refc['elements'][0]];assert refpart['sourceObject']==r['sourceObject'] and refpart['conceptId']==refcid
 generic_name=position.capitalize()+' phalanx of foot' if position else 'Metatarsal bone';generic=terms[generic_name];assert generic['sourceRowId'].isdigit()
 specific=terms[r['sourceEnglish']]
 assert ('*' in specific['sourceRowId'])==(r['la'] is None)
 if r['la'] is not None:assert r['la']==specific['la'] and int(specific['sourceRowId'])==r['ta2TableId']
 targetid=f'foot-bones-v1:{side}:{family}:{digit}'+(':'+position if position else '')
 representations=[dict(datasetId='male-body',sourceVersion=base['version'],conceptId=cid,sourceName=expected,partIds=members,sourceManifest=paths['base'],manifestLocator=f'concepts/{cid}',observedPart=part,officialNameRow=name_rows[cid],officialMembershipRows=member_rows[cid],identityStatus='observed_single_part_source_binding; target correspondence candidate',geometryAcceptance='not_assessed_by_this_metadata_audit'),dict(datasetId=metadata['datasetId'],sourceVersion=ref['version'],conceptId=refcid,sourceName=refc['name'],sourceObject=refpart['sourceObject'],partIds=refc['elements'],sourceManifest=paths['reference'],manifestLocator=f'concepts/{refcid}',identityStatus='observed_single_part_source_binding; independent_source_frame',geometryAcceptance='preserved_existing_reference_status; no_new_geometry_review')]
 scope='Tek kaynak kemik parçası; eklem kıkırdağı, kapsül, bağlar ve yumuşak dokuların tamamını temsil etmez. Anatomik uzman incelemesi bekliyor.'
 label=dict(ids=[cid],datasetId='male-body',tr=r['tr'],en=r['en'],la=r['la'],side=side,digit=digit,digitSystem=r['digitSystem'],aliases=list(dict.fromkeys([expected,r['en'].lower(),r['sourceEnglish'].lower()])),ta2TableId=r['ta2TableId'],genericTerm=copy.deepcopy(generic),trStatus='editorial',expertReview='pending',representationNoteTr=scope,scopeNoteTr=scope,evidence=[dict(sourceId='bp3d40-names',locator=f'line {name_rows[cid]["line"]}; {cid}'),dict(sourceId='bp3d40-membership',locator='; '.join('line '+str(x['line']) for x in member_rows[cid])),dict(sourceId='zanatomy-ta2-pinned',locator=f'CSV line {specific["csvLine"]}; source row {specific["sourceRowId"]}')])
 if position:label['phalanxPosition']=position
 if r['la'] is None:label['latinUnavailableReason']=r['latinUnavailableReason'];label['sourceTableRow']=copy.deepcopy(specific)
 existing_label=next((l for l in active_labels if cid in l['ids']),None)
 assert existing_label is None or existing_label==label,'Conflicting integrated individual label'
 mainlabels.append(label)
 targetrels=[x for x in relrows if x['child']==cid];assert len(targetrels)==1
 existing=[x for x in graph['relations'] if x['subject']==cid and x['predicate']=='part_of'];assert len(existing)==1
 rr=targetrels[0];edge=existing[0];assert edge['object']==rr['parent'] and rr['childName']==expected
 parent=concepts[rr['parent']];assert parent['name']==rr['parentName'] and set(members)<=set(parent['elements'])
 assert ('left' in parent['name'])==(side=='left')
 relationship_records.append(dict(datasetId='male-body',targetId=targetid,existingGraphRelation=copy.deepcopy(edge),sourceRow=rr,action='reuse_existing_graph_navigation; do_not_add_duplicate',scope='Explicit source PART-OF row; not inferred from geometry containment; not transplanted into Z-Anatomy reference'))
 parents[parent['id']]=dict(concept=parent,side=side,digit=digit if position else None,scope='toe' if position else 'foot_proper')
 records.append(dict(id=targetid,regionId='leg-ankle-foot',familyId='skeletal-support',requiredDetail='D1',requirementStatus='project_proposed; curriculum_and_expert_acceptance_pending',side=side,digit=digit,digitSystem=r['digitSystem'],boneType=family,phalanxPosition=position,terminology=dict(genericNumericTa2Term=generic,specificSourceTerm=specific,specificTa2IdentityStatus='numeric_TA2_row_in_pinned_table' if specific['sourceRowId'].isdigit() else 'custom_starred_upstream_row_not_official_per_digit_TA2_ID',formalTa2FmaCrosswalk='not_asserted',scope='Generic term defines bone type/segment; digit and side are separately sourced target attributes'),representations=representations,mainLabelProposalIndex=len(mainlabels)-1,referenceLabelId=refcid,expertReview='pending',anatomicallyAccepted=False,absenceClaim=False,acceptanceScope='Manifest-bound independent source objects only; no anatomical or product-journey acceptance',openCriteria=['Per-target geometry/detail and anatomical review','Source-frame-specific user journey','Proposed main label activation and scope-note display','Named expert acceptance']))
# Preserve the existing toe/foot-proper path to the two source foot parents.
parent_relationship_records=[]
for pid,p in list(parents.items()):
 foot=byname[p['side']+' foot']
 rows=[row for row in relrows if row['child']==pid and row['parent']==foot['id']]
 edges=[edge for edge in graph['relations'] if edge['subject']==pid and edge['predicate']=='part_of' and edge['object']==foot['id']]
 assert len(rows)==len(edges)==1
 assert rows[0]['childName']==p['concept']['name'] and rows[0]['parentName']==foot['name']
 parent_relationship_records.append(dict(datasetId='male-body',existingGraphRelation=copy.deepcopy(edges[0]),sourceRow=rows[0],action='reuse_existing_graph_navigation; do_not_add_duplicate',scope='Explicit existing toe/foot-proper to foot source path; no new relationship'))
for side in ['left','right']:
 c=byname[side+' foot'];parents[c['id']]=dict(concept=c,side=side,digit=None,scope='foot')
assert len(parent_relationship_records)==12
parent_labels=[];parent_scopes=[]
for pid,p in sorted(parents.items()):
 c=p['concept'];side=p['side'];digit=p['digit'];note='';la=None;term=None
 assert all(parts[fj]['system']=='skeletal' for fj in c['elements'])
 assert sorted(x['partId'] for x in parent_member_rows[pid])==sorted(c['elements'])
 assert parent_name_rows[pid]['name']==c['name']
 if p['scope']=='foot':
  term=terms['Foot'];assert term==dict(sourceRowId='166',en='Foot',la='Pes',csvLine=168)
  la=term['la'];tr='Ayak';en='Foot'
  assert len(c['elements'])==26
  assert sum('metatarsal bone' in parts[fj]['name'].lower() for fj in c['elements'])==5
  assert sum('phalanx' in parts[fj]['name'].lower() for fj in c['elements'])==14
  note='Kaynak kavramı ayağı adlandırır; mevcut seçim yalnız 26 kemik parçasını gösterir: yedi tarsal kemik, beş metatars ve 14 falanks. Deri, kas, tendon, damar/sinir ve diğer yumuşak dokular bu kaynak seçim kümesinde temsil edilmez. Tam ayak dokusu modeli değildir; anatomik uzman incelemesi bekliyor.'
 elif p['scope']=='toe':
  termname={1:'Great toe',2:'Second toe',3:'Third toe',4:'Fourth toe',5:'Little toe'}[digit];term=terms[termname];la=term['la'];tr='Ayak başparmağı' if digit==1 else f'{digit}. ayak parmağı';en=termname
  note=f'Kaynak kavramı parmağı adlandırır; mevcut seçim yalnız {len(c["elements"])} falanks kemiğini gösterir. Deri, kas, tendon, damar/sinir, eklem kıkırdağı ve kapsül bu parça kümesinde temsil edilmez. Tam parmak dokusu modeli değildir; anatomik uzman incelemesi bekliyor.'
 else:
  tr='Ayak gövdesi';en='Foot proper';note='Kaynak kavramı ayağın parmaklar dışındaki bölümünü adlandırır; mevcut seçim yalnız beş metatars kemiğini gösterir. Tarsal kemikler ve yumuşak dokular bu kaynak seçim kümesinde yer almaz; tam ayak gövdesi modeli değildir. Anatomik uzman incelemesi bekliyor.'
 parent_labels.append(dict(ids=[pid],datasetId='male-body',tr=tr,en=en,la=la,side=side,digit=digit,aliases=[c['name']],ta2TableId=int(term['sourceRowId']) if term else None,trStatus='editorial',expertReview='pending',representationNoteTr=note,scopeNoteTr=note,latinUnavailableReason=None if term else 'No exact Foot proper scope term verified in the pinned terminology source; broader Foot/Pes is not substituted.',evidence=[dict(sourceId='bp3d40-parent-names',locator=f'line {parent_name_rows[pid]["line"]}; {pid}'),dict(sourceId='bp3d40-parent-membership',locator='; '.join('line '+str(x['line']) for x in parent_member_rows[pid]))]+([dict(sourceId='zanatomy-ta2-pinned',locator=f'TA2 {term["sourceRowId"]}; CSV line {term["csvLine"]}; {term["en"]}',scope=('Unsided Foot/Pes term; separate laterality; bone-only rendered scope explicitly disclosed' if p['scope']=='foot' else 'Unsided toe term; source big toe normalized to great toe; same digit and separate laterality'))] if term else [])))
 parent_scopes.append(dict(datasetId='male-body',conceptId=pid,sourceName=c['name'],partIds=c['elements'],parts=[dict(id=parts[fj]['id'],conceptId=parts[fj]['conceptId'],name=parts[fj]['name'],system=parts[fj]['system']) for fj in c['elements']],sourceManifest=paths['base'],officialNameRow=parent_name_rows[pid],officialMembershipRows=parent_member_rows[pid],scope='Existing anatomical source concept with bone-only rendered membership; not a newly invented display group',representationNoteTr=note,expertReview='pending'))
assert len(parent_labels)==14 and len(records)==38
assert len({r['representations'][0]['partIds'][0] for r in records})==38
assert len({r['representations'][1]['partIds'][0] for r in records})==38
assert sum(r['boneType']=='metatarsal' for r in records)==10
assert sum(r['boneType']=='phalanx' for r in records)==28
assert sum(l['la'] is not None for l in mainlabels)==4
assert sum(l['la'] is not None for l in parent_labels)==12
assert len(relationship_records)==38
for proposed in parent_labels:
 existing_parent=next((l for l in active_labels if proposed['ids'][0] in l['ids']),None)
 assert existing_parent is None or existing_parent==proposed,'Conflicting integrated parent label'
sources=[dict(id='human-atlas-bp3d40',title='Human Atlas / BodyParts3D4.0 current base manifest',path=paths['base'],sourceVersion='4.0',url='https://github.com/ashemag/human-atlas'),dict(id='bp3d40-names',title='Retained official BodyParts3D archive ISA concept names',path=paths['names'],url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt',inspection='Retained source snapshot inspected2026-10-02;no fresh network retrieval'),dict(id='bp3d40-membership',title='Retained official BodyParts3D archive ISA element memberships',path=paths['membership'],url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt',inspection='Retained source snapshot inspected2026-10-02;no fresh network retrieval'),dict(id='bp3d-partof',title='Retained official BodyParts3D PART-OF relationships',path=paths['relations'],url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_inclusion_relation_list.txt'),dict(id='zanatomy-ta2-pinned',title='Pinned Z-Anatomy-distributed TA2 table',path=paths['terms'],url=metadata['sources'][0]['url'],scope='Exact numeric generic and specific terms distinguished from custom star-suffixed rows;not a newly verified official ontology crosswalk'),dict(id='lower-limb-reference',title='Current independent source-frame lower-limb reference',path=paths['reference'],metadataPath=paths['referenceLabels'],sourceArtifactSha256='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd')]
sources.extend([dict(id='bp3d40-parent-names',title='Retained official archive PART-OF concept names',path=paths['parentNames'],url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_parts_list_e.txt'),dict(id='bp3d40-parent-membership',title='Retained official archive PART-OF element memberships',path=paths['parentMembership'],url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_element_parts.txt')])
result=dict(schemaVersion=1,scopeVersion='foot-bone-targets-v1-candidate',sourceRevision=REVISION,reviewedOn='2026-10-02',status='source_audit_proposal; activation_and_release_tracked_in_owning_report',scope='38 individual metatarsal/toe-phalangeal targets already represented in two independent datasets; no coordinate or specimen equivalence claimed',summary=dict(targets=38,metatarsalTargets=10,phalangealTargets=28,mainSinglePartBindings=38,referenceSinglePartBindings=38,mainIndividualLabelProposals=38,parentLabelProposals=14,existingSourceRelationsToReuse=38,existingParentPathRelationsToReuse=12,newAnatomicalRelationsProposed=0,mainIndividualLatinPresent=4,mainIndividualLatinUnresolved=34,parentLatinPresent=12,parentLatinUnresolved=2,anatomicallyAccepted=0),targets=records,mainIndividualLabelProposals=mainlabels,mainParentLabelProposals=parent_labels,parentScopeRecords=parent_scopes,existingRelationshipEvidence=relationship_records,existingParentPathEvidence=parent_relationship_records,referenceRelationshipDecision='No new groups or anatomical part_of edges; male-body source hierarchy is not transplanted into the independent Z-Anatomy reference',sources=sources,inputSnapshots=[dict(path=v,sha256=sha(v)) for v in paths.values()],limits=['Name correspondence alone is not the binding evidence: every candidate has an exact concept→existing part manifest link and official membership row','One part means independently addressable source geometry, not verified anatomy or accepted visual detail','No global absence assertion','No invented digit-specific Latin or formal TA2/FMA crosswalk','No claims of complete toe/foot-proper tissues','No articulates_with or attaches_to investigation in this task','Producer writes only the audit; active integration is owned by root'])
encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n';dest=OUT/'proposal.json'
if '--check' in sys.argv:
 assert dest.read_text()==encoded,'Candidate differs from deterministic inputs'
 print('PASS deterministic candidate and source assertions:38targets/76single-part bindings/52label proposals/38existing individual+12existing parent source edges/0newedges/0expertacceptances')
else:
 dest.write_text(encoded);print('Wrote proposal.json;all source assertions passed')
