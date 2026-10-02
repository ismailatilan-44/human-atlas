"""Read-only P3 planning audit. Deterministic output from pinned/frozen inputs."""
import copy,datetime,hashlib,json,math,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
REV='0a501618801a5fbc8db44599d24eb50dfde0fba4'
load=lambda p:json.loads((ROOT/p).read_text())
hashfile=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
# Explicit source-scoped requirements, not discovered-only targets or a completeness denominator.
FAMILIES={
 'skeletal-support':[1143,1145,1150,1151,1152,1159,1162,1163,1164,1168,1180,1181,1184,1185,1186,1210,1216,1230,1740,1744,1745,1746,1747,1748,1749,1750,1751,1754,1755,1756,1764,1765,1767,1768,1769,1770,1771,1772,1773,1774,1775,1776,1777,1778,7138,7152,7153,2557,2558],
 'muscle-tendon-fascia':[2226,2227,2228,2229,2231,2232,2233,2234,2301,2302,2303,2305,2306,2307,2452,2453,2454,2455,2457,2458,2459,2460,2462,2464,2465,2466,2468,2469,2471,2472,2473,2474,2541,2542,2543,2318,2467,2510],
 'neurovascular-lymph':[6395,6397,6398,6399,6400,6401,6402,6403,6404,6405,6406,6409,6410,6411,6415,6416,6417,6419,6421,6422,6423,6424,6428,6429,6430,6431,6432,6433,6434,6435,6436,6438,6440,6441,6442,6444,6445,6446,6449,6450,6458,6459,6461,6476,4616,4618,4619,4620,4622,4623,4624,4625,4627,4628,4629,4630,4631,4632,4634,4637,4638,4639,4640,4963,4964,4979,4982,5236,5237,5238,5239,5240,5241,4537,4599,4606,4953],
 'organs-cavities-internal':[140,2463,2470],
}
paths={'ta2':'work/open-assets-review/TA2.csv','base':'public/models/atlas.json','registry':'public/models/extensions/index.json','names':'data/model-candidates/coverage-labels/bp3d-isa-parts-list-e.txt','membership':'data/model-candidates/concept-selection-review/isa_element_parts.txt','upperArm':'data/anatomy/upper-arm.json','forearm':'data/anatomy/forearm.json','rotator':'data/anatomy/rotator-cuff.json','plexus':'data/anatomy/brachial-plexus.json','scope':'docs/model/model-scope-and-acceptance.md','partofNames':'data/model-candidates/concept-selection-review/partof_parts_list_e.txt','partofMembership':'data/model-candidates/concept-selection-review/partof_element_parts.txt'}
terms={}
for i,line in enumerate((ROOT/paths['ta2']).read_text().splitlines(),1):
 cells=line.strip('"').split(';')
 if len(cells)>2 and cells[0].isdigit():terms[int(cells[0])]=dict(numericId=int(cells[0]),en=cells[1],la=cells[2],csvLine=i)
assert all(i in terms for ids in FAMILIES.values() for i in ids)
registry=load(paths['registry']);manifests=[paths['base']]+['public'+p for p in registry['manifests']]
landmark_paths=['public'+p for p in registry['landmarks']]
for p in manifests+landmark_paths:paths[p]=p
# Freeze mutable graph/coverage/scope contract records once. Subsequent checks never silently reread a changed graph.
snapshot_path=OUT/'frozen-inputs.json'
if not snapshot_path.exists() or '--refresh-inputs' in sys.argv:
 original_paths=['data/anatomy/knowledge.json','data/anatomy/coverage.json','data/anatomy/model-inventory.json']
 graph=load(original_paths[0]);coverage=load(original_paths[1]);inventory=load(original_paths[2])
 region=next(r for r in inventory['regions'] if r['id']=='shoulder-axilla-arm')
 frozen=dict(capturedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision=REV,workingTreeNote='Root support integration changes concurrent; snapshot is local observed state, not a clean committed or deployed revision',sourceSnapshots=[dict(path=p,sha256=hashfile(p)) for p in original_paths],scopeContract=region,scopeDocument=(ROOT/paths['scope']).read_text(),graph=dict(entities=graph['entities'],relations=graph['relations'],sources=graph['sources']),coverage=coverage,immutableInputHashes={p:hashfile(p) for p in paths.values()})
 snapshot_path.write_text(json.dumps(frozen,ensure_ascii=False,separators=(',',':'))+'\n')
frozen=json.loads(snapshot_path.read_text())
for p,h in frozen['immutableInputHashes'].items():
 if p==paths['scope']:assert hashlib.sha256(frozen['scopeDocument'].encode()).hexdigest()==h
 else:assert hashfile(p)==h,'Frozen source changed; review then explicitly refresh inputs: '+p
graph=frozen['graph'];entities={e['id']:e for e in graph['entities']};graphnames={e['name'].lower():e for e in graph['entities']}
base=load(paths['base']);assert base['version']=='BodyParts3D 4.0'
allparts={};allconcepts={};manifestof={}
for path in manifests:
 m=load(path)
 for p in m['parts']:allparts[p['id']]=dict(p,manifest=path)
 for c in m['concepts']:allconcepts[c['id']]=c;manifestof[c['id']]=path
names={};members={}
for i,line in enumerate((ROOT/paths['names']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:names[c[0]]=dict(conceptId=c[0],sourceRepresentationId=c[1],sourceName=c[2],line=i)
for i,line in enumerate((ROOT/paths['membership']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:members.setdefault(c[0],[]).append(dict(conceptId=c[0],sourceName=c[1],partId=c[2],line=i))
for i,line in enumerate((ROOT/paths['partofNames']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3 and c[0] not in names:names[c[0]]=dict(conceptId=c[0],sourceRepresentationId=c[1],sourceName=c[2],line=i,table=paths['partofNames'])
partofmembers={}
for i,line in enumerate((ROOT/paths['partofMembership']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:partofmembers.setdefault(c[0],[]).append(dict(conceptId=c[0],sourceName=c[1],partId=c[2],line=i,table=paths['partofMembership']))
for cid,rows in partofmembers.items():
 if cid not in members:members[cid]=rows
# Only spelling/scope-preserving source naming variants. No fuzzy or geometry-based assignment.
def queries(name,side):
 base=[name.lower()]
 if name.endswith(' muscle'):base.append(name[:-7].lower())
 if ' muscle' in name.lower():base.append(name.lower().replace(' muscle',''))
 if name=='Superior subscapular nerve':base.append('upper subscapular nerve')
 if name=='Inferior subscapular nerve':base.append('lower subscapular nerve')
 if name=='Scapular spinal part of deltoid muscle':base.append('spinal part of deltoid')
 result=[]
 for n in base:
  result.append(side+' '+n)
  if ' of ' in n:
   a,b=n.split(' of ',1);result.append(a+' of '+side+' '+b)
 return list(dict.fromkeys(result))
byname={c['name'].lower():c for c in allconcepts.values()}
anchors={};unresolvedanchors={}
for path in landmark_paths:
 d=load(path)
 for a in d['anchors']:anchors[a['conceptId']]=dict(a,manifest=path)
 for a in d['unresolved']:unresolvedanchors[a['conceptId']]=dict(a,manifest=path)
coverage_targets=[t for r in frozen['coverage']['regions'] for t in r['targets']]
def bindings_for(name,side):
 qs=queries(name,side);ids=[]
 for q in qs:
  if q in byname:ids.append(byname[q]['id'])
  if q in graphnames:ids.append(graphnames[q]['id'])
 out=[]
 for cid in dict.fromkeys(ids):
  entity=entities.get(cid);c=allconcepts.get(cid);partids=c['elements'] if c else (entity or {}).get('geometryPartIds',[])
  assert all(p in allparts for p in partids),'Inactive/missing source part '+cid
  observed=[]
  for pid in partids:
   p=allparts[pid];assert p.get('vertexCount',0)>0 and p.get('indexCount',0)>0
   assert all(math.isfinite(v) for b in p['bounds'] for v in b)
   observed.append({k:p[k] for k in ['id','name','conceptId','system','vertexCount','indexCount','bounds','manifest'] if k in p})
  if c and manifestof[cid]==paths['base']:
   assert names[cid]['sourceName']==c['name']
   exact_membership=sorted(r['partId'] for r in members.get(cid,[]))==sorted(partids) or sorted(r['partId'] for r in partofmembers.get(cid,[]))==sorted(partids)
  if entity and c:assert set(entity.get('geometryPartIds',[]))==set(partids),'Graph/manifest mismatch '+cid
  b=dict(datasetId='male-body',conceptId=cid,sourceName=c['name'] if c else entity['name'],sourceManifest=manifestof.get(cid),partIds=partids,observedParts=observed,sourceConcept=copy.deepcopy(c),graphEntity=copy.deepcopy(entity),status='manifest_membership_observed' if partids else 'existing_concept_without_mesh',selectionScope='single_source_part' if len(partids)==1 else 'source_group_multiple_parts' if partids else 'no_mesh_binding',detailAcceptance='unreviewed; membership and nonzero geometry do not establish required anatomical detail')
  if cid in names:b.update(officialNameRow=names[cid],officialIsaOrFallbackMembershipRows=members.get(cid,[]),officialPartofMembershipRows=partofmembers.get(cid,[]),officialMembershipParity=exact_membership if c and manifestof[cid]==paths['base'] else None)
  if cid in anchors:b['surfaceAnchor']=anchors[cid];b['status']='source_attachment_reference_point_only'
  if cid in unresolvedanchors:b['unresolvedAnchor']=unresolvedanchors[cid]
  if c and 'scope' in c:b['sourceScope']=c['scope']
  if cid.startswith('atlas:') and 'brachial-plexus' in cid:b['scopeLimit']='Partial registered source plexus; only named trunks/divisions/posterior cord. No root, medial/lateral cord, complete branch or specimen validation claim.'
  if 'median-nerve' in cid or 'musculocutaneous-nerve' in cid:b['scopeLimit']='Registered authored source trajectory; distal continuation and separately named motor/cutaneous branches require their own targets and evidence.'
  out.append(b)
 return qs,out
RELATION_NEEDS={'skeletal-support':['articulates_with or part_of where exact joint/bone scope is sourced','attaches_to with named region for ligament/capsule targets; no inferred model footprint'], 'muscle-tendon-fascia':['originates_at','inserts_at','innervates (incoming nerve endpoint; no parent/head inheritance)'], 'neurovascular-lymph':['branch_of or source part_of, distinguished explicitly','innervates/supplies/drains_to only when individually sourced and endpoint scope verified'], 'organs-cavities-internal':['bounded_by/contains or passage relationship only after direct source evidence']}
targets=[]
for family,ids in FAMILIES.items():
 for taid in ids:
  term=terms[taid];name=term['en']
  for side in ['left','right']:
   qs,bindings=bindings_for(name,side)
   kind='named_structure'
   if 'head of' in name.lower() or 'part of' in name.lower():kind='named_part_or_head'
   if name.endswith(('nodes','nerves','branches','veins')) or 'branches of' in name.lower() or name.startswith('Roots of'):kind='named_group'
   if taid in [1145,1150,1151,1152,1159,1162,1163,1164,1181,1184,1185,1186,1216]:kind='bone_landmark'
   detail='D1' if family in ['muscle-tendon-fascia','neurovascular-lymph'] and kind=='named_structure' else 'D2'
   if taid in [1143,1168,1180,1210,1230]:detail='D1'
   slug=re.sub('[^a-z0-9]+','-',name.lower()).strip('-');conceptids={b['conceptId'] for b in bindings}
   cov=[t['id'] for t in coverage_targets if any(b.get('conceptId') in conceptids for b in t.get('currentBindings',[]))]
   relations=[r['id'] for r in graph['relations'] if r['subject'] in conceptids or r['object'] in conceptids]
   targets.append(dict(id='upper-limb-target-v1:'+slug+'-'+side[0],regionId='shoulder-axilla-arm',ownerPackage='P3',familyId=family,name=name,side=side,targetKind=kind,requiredDetail=detail,requirementStatus='proposed;expert_pending;non_exhaustive',termEvidence=dict(sourceId='zanatomy-ta2-pinned',**term,scope='Exact unsided numeric term; no formal FMA crosswalk or side-declension assertion'),representations=bindings,sourceNameQueries=qs,bindingStatus='observed_manifest_or_anchor' if any(b['partIds'] or b.get('surfaceAnchor') for b in bindings) else 'existing_concept_without_geometry' if bindings else 'no_positive_binding_in_bounded_active_source_audit;not_absence',requiredRelationshipTypes=RELATION_NEEDS[family],existingRelationshipIds=relations,relationshipAcceptance='existing facts are evidence only; required regional relationship set remains pending',coverageEvidenceIds=cov,anatomicallyAccepted=False,expertReview='pending',complete=False,absenceClaim=False))
# Related named parts are evidence of available pieces, never a fabricated whole-muscle binding.
for t in targets:
 if t['familyId']!='muscle-tendon-fascia' or t['targetKind']!='named_structure':continue
 stem=t['name'].lower().replace(' muscle','');suffix=' of '+t['side']+' '+stem
 related=[]
 for c in allconcepts.values():
  if c['name'].endswith(suffix):
   rows=members.get(c['id'],[]);prows=partofmembers.get(c['id'],[])
   related.append(dict(conceptId=c['id'],sourceName=c['name'],sourceManifest=manifestof[c['id']],partIds=c['elements'],observedParts=[{k:allparts[x][k] for k in ['id','name','conceptId','vertexCount','indexCount','manifest'] if k in allparts[x]} for x in c['elements']],officialNameRow=names.get(c['id']),officialIsaOrFallbackMembershipRows=rows,officialPartofMembershipRows=prows,status='Related source part evidence; not a binding of this complete named muscle'))
 if related:t['relatedPartEvidence']=related;t['wholeStructureLimit']='Individual source heads/parts do not establish complete whole-muscle extent, separate tendons, fine fibers or automatic relation inheritance'
 if t['name']=='Pectoralis major muscle':t['wholeStructureLimit']='Existing whole-name source selection contains abdominal/sternocostal pieces; separately listed clavicular part is not in that selection. Source membership is preserved and full-muscle extent remains unaccepted.'
for t in targets:
 if t['familyId']!='neurovascular-lymph':continue
 n=t['name'].lower()
 if 'arter' in n:t['requiredRelationshipTypes']=['branch_of with exact source vessel','supplies only after direct regional territory evidence']
 elif 'vein' in n:t['requiredRelationshipTypes']=['drains_to or tributary relation with source endpoint','Regional extent and tributary scope review']
 elif 'nodes' in n:t['requiredRelationshipTypes']=['drains_to with source lymph pathway evidence','part_of for named group membership only after source verification']
 else:t['requiredRelationshipTypes']=['branch_of versus source part_of distinguished','Direct motor innervation and/or sensory distribution as applicable; no inferred group inheritance']
for t in targets:
 if t['name']=='Brachial veins':
  _,partial=bindings_for('Medial brachial vein',t['side'])
  assert len(partial)==1 and len(partial[0]['partIds'])==1
  t['relatedPartEvidence']=partial
  t['wholeStructureLimit']='One independently named medial brachial vein is present per side. This does not establish a full paired-vein group or all tributaries; no whole plural-target binding promoted.'
 if t.get('termEvidence',{}).get('numericId') in [1184,1185]:t['termEvidence']['context']='Humerus section in pinned table; generic English tubercle name is not matched to another bone'
# Explicit requirements remain even when no exact numeric per-root/custom-region term or binding is available.
for name,family,reason,generic in [(f'{r} root contribution to brachial plexus','neurovascular-lymph','Individual root identity is not established by the exported root-like source bundle; do not assign C5-T1 from topology',6397) for r in ['C5','C6','C7','C8','T1']]+[('Medial midshaft attachment region of humerus','skeletal-support','Custom attachment region, not exact named TA2 bone structure; existing two markers remain unresolved',None),('Quadrangular space','organs-cavities-internal','Exact term not found in the pinned English-table audit; source term and boundaries need independent verification',None),('Triangular space','organs-cavities-internal','Exact term not found in the pinned English-table audit; source term and boundaries need independent verification',None),('Triangular interval','organs-cavities-internal','Exact term not found in the pinned English-table audit; source term and boundaries need independent verification',None)]:
 for side in ['left','right']:
  qs,b=bindings_for(name,side)
  slug=re.sub('[^a-z0-9]+','-',name.lower()).strip('-')
  targets.append(dict(id='upper-limb-target-v1:'+slug+'-'+side[0],regionId='shoulder-axilla-arm',ownerPackage='P3',familyId=family,name=name,side=side,targetKind='proposed_detail_requirement',requiredDetail='D2',requirementStatus='proposed;expert_pending;non_exhaustive',termEvidence=dict(exactNumericTerm=None,la=None,unresolvedReason=reason,genericTerm=terms[generic] if generic else None),representations=b,sourceNameQueries=qs,bindingStatus='existing_concept_without_verified_geometry' if b else 'no_positive_binding_in_bounded_active_source_audit;not_absence',requiredRelationshipTypes=RELATION_NEEDS[family],existingRelationshipIds=[],coverageEvidenceIds=[],anatomicallyAccepted=False,expertReview='pending',complete=False,absenceClaim=False))
assert len({t['id'] for t in targets})==len(targets)
assert all(t['side'] in ['left','right'] and not t['anatomicallyAccepted'] for t in targets)
assert all(sum(t['name']==n for t in targets)==2 for n in ['Lateral cord of brachial plexus','Medial cord of brachial plexus','C5 root contribution to brachial plexus','C6 root contribution to brachial plexus','C7 root contribution to brachial plexus','C8 root contribution to brachial plexus','T1 root contribution to brachial plexus'])
assert {t['familyId'] for t in targets}==set(FAMILIES)
assert sum(bool(b.get('surfaceAnchor')) for t in targets for b in t['representations'])==6
assert sum(bool(b.get('unresolvedAnchor')) for t in targets for b in t['representations'])==2
assert all(b.get('officialMembershipParity') is not False for t in targets for b in t['representations'])
counts={s:sum(t['bindingStatus']==s for t in targets) for s in sorted({t['bindingStatus'] for t in targets})}
result=dict(schemaVersion=1,scopeVersion='upper-limb-target-inventory-v1',sourceRevision=REV,status='candidate_planning_only;root_owns_integration',complete=False,scopeContract=frozen['scopeContract'],summary=dict(targets=len(targets),unsidedRequirements=len(targets)//2,families={f:sum(t['familyId']==f for t in targets) for f in FAMILIES},bindingStatusCounts=counts,expertAccepted=0,newLabels=0,newRelationships=0,newGeometry=0),targets=targets,unexpandedRequirements=[dict(familyId='skeletal-support',requirement='Further shoulder/elbow articular surfaces, regional ligaments/capsules/bursae and bone landmarks; full required list remains open'),dict(familyId='muscle-tendon-fascia',requirement='Independently sourced tendons and attachment footprints for every regional muscle/head; general muscles do not satisfy these details'),dict(familyId='neurovascular-lymph',requirement='Additional collateral/terminal/cutaneous branches, muscular branches, artery/vein tributaries and lymph vessels/routes; no absence or completion inferred'),dict(familyId='organs-cavities-internal',requirement='Complete regional compartments/passages and directly sourced boundaries/contents; no mesh-space inference')],sources=[dict(id='zanatomy-ta2-pinned',title='Pinned Z-Anatomy-distributed TA2',url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv'),dict(id='bp3d40-names',title='Official retained BodyParts3D name table',url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt'),dict(id='bp3d40-membership',title='Official retained BodyParts3D element membership',url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt'),dict(id='bp3d40-partof-names',title='Official retained BodyParts3D PART-OF names',url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_parts_list_e.txt'),dict(id='bp3d40-partof-membership',title='Official retained BodyParts3D PART-OF element membership',url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_element_parts.txt')],inputSnapshots=[dict(path=p,sha256=h) for p,h in frozen['immutableInputHashes'].items()]+frozen['sourceSnapshots']+[dict(path=str(snapshot_path.relative_to(ROOT)),sha256=hashfile(str(snapshot_path.relative_to(ROOT)))),dict(path=str(Path(__file__).relative_to(ROOT)),sha256=hashfile(str(Path(__file__).relative_to(ROOT))))],snapshotCapturedAt=frozen['capturedAt'],snapshotState=frozen['workingTreeNote'],limits=['No labels, anatomical relations or geometry are proposed for activation','Bilateral source copies do not establish independent specimen validation','Source groups, whole muscles, heads and reference attachment markers are separate scopes','A source name match is insufficient without actual manifest/part membership','No positive binding does not establish absence; retained sources and active registry bound this audit','Root bundle and missing cords/branch details remain mandatory unresolved targets','Coverage65 pilot rows are evidence only, never a comprehensive denominator','All source licenses/frames remain separate; no geometry registration or redistribution assessment is performed','Existing relationship IDs are source evidence, not satisfaction of full required relations or expert acceptance'])
encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if '--check' in sys.argv:
 assert (OUT/'proposal.json').read_text()==encoded,'Candidate differs from frozen inputs/producer'
 print('PASS',json.dumps(result['summary']))
else:(OUT/'proposal.json').write_text(encoded);print('Wrote',json.dumps(result['summary']))
