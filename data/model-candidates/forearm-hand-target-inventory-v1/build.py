"""Deterministic, self-contained P4 planning seed. --check never reads the active graph."""
import copy, hashlib, json, math, sys
from collections import Counter
from pathlib import Path
OUT=Path(__file__).resolve().parent
frozen=json.loads((OUT/'frozen-inputs.json').read_text())
FAMILIES=['skeletal-support','muscle-tendon-fascia','neurovascular-lymph','organs-cavities-internal']
NEEDS={
'skeletal-support':['Sourced articulating structures and support attachments, as applicable','Named joint surfaces and ligament endpoints; whole bone membership does not establish them'],
'muscle-tendon-fascia':['Sourced origin/insertion and incoming motor innervation for each muscle or head','Tendon continuity, sheath extent and support endpoints as applicable; no automatic group/head inheritance'],
'neurovascular-lymph':['Sourced branch hierarchy, direct motor/sensory endpoints or vascular territory/drainage as applicable','Lymph pathway identity and source routes remain pending; no proximity-derived facts'],
'organs-cavities-internal':['Sourced boundaries, contents and passage relationships','Space identity and source geometry must be distinguished; no inferred cavity surface']}
# Independent source frames are never merged by concept ID; observation identity includes dataset.
def representations(seed,side):
 qs=seed['sourceNameQueries'][side]; out=[]
 for o in frozen['observations']:
  if o['sourceName'].lower() not in qs:continue
  b=copy.deepcopy(o);b['selectionScope']='named_source_group_not_individual_members' if seed['targetKind']=='named_group' else 'single_source_part' if len(b['partIds'])==1 else 'multiple_source_parts;extent_unaccepted'
  b['lateralityEvidence']='Exact sided source concept label; source .l/.r where present; no independent specimen-side validation'
  b['scopeLimit']='Positive source-name and manifest membership observation only. Independent individual identity, full anatomical extent, finer subdivisions, complete branch networks and clinical relevance remain pending.'
  if seed['targetKind']=='named_group':b['scopeLimit']+=' Plural source group does not satisfy any individual numbered/member requirement.'
  if b['datasetId']=='upper-limb-nerve-reference':b['scopeLimit']+=' Separate Z-Anatomy reference coordinates; not a main-body binding or regional registration acceptance.'
  for p in b['observedParts']:
   assert p['vertexCount']>0 and p['indexCount']>0
   assert all(math.isfinite(v) for bound in p['bounds'] for v in bound)
  assert sorted(p['id'] for p in b['observedParts'])==sorted(b['partIds'])
  if b['sourceManifest']=='public/models/atlas.json':
   assert any(r['cells'][2]==b['sourceName'] for r in b['officialNameRows']),b['conceptId']
   tables={r['path'] for r in b['officialMembershipRows']}
   assert any(sorted(r['cells'][2] for r in b['officialMembershipRows'] if r['path']==t)==sorted(b['partIds']) for t in tables),b['conceptId']
   b['officialMembershipParity']=True
  out.append(b)
 return out

targets=[]
for s in frozen['seeds']:
 for side in ['left','right']:
  reps=representations(s,side);conceptids={r['conceptId'] for r in reps}
  t=dict(id='forearm-hand-target-v1:'+s['key']+'-'+side[0],regionId='forearm-wrist-hand',ownerPackage='P4',familyId=s['familyId'],name=s['name'],side=side,targetKind=s['targetKind'],requiredDetail=s['requiredDetail'],requirementStatus='proposed;expert_pending;non_exhaustive',termEvidence=copy.deepcopy(s['termEvidence']),representations=reps,sourceNameQueries=s['sourceNameQueries'][side],bindingStatus='observed_manifest_membership' if reps else 'no_positive_binding_in_bounded_source_audit;not_absence',requiredRelationshipTypes=NEEDS[s['familyId']],existingRelationshipIds=[r['id'] for r in frozen['graphRelations'] if r['subject'] in conceptids or r['object'] in conceptids],relationshipAcceptance='Historical existing facts only; required regional set and dataset applicability remain pending',coverageEvidenceIds=[],anatomicallyAccepted=False,expertReview='pending',complete=False,absenceClaim=False)
  # Class/source group observations stay related evidence, not individual bindings.
  if s['targetKind']=='individual_subdivision_requirement' and 'genericTerm' in s['termEvidence']:
   generic=s['termEvidence']['genericTerm']['tableId']
   groups=[x for x in frozen['seeds'] if x['termEvidence'].get('tableId')==generic]
   t['relatedGroupEvidence']=[b for group in groups if group['targetKind']=='named_group' for b in representations(group,side)]
   if t['relatedGroupEvidence']:t['wholeStructureLimit']='Related source class/group cannot identify or select this individual member. Individual identity, segmentation and exact term remain open.'
  related=[p for p in frozen.get('relatedPartObservations',[]) if p['seedKey']==s['key'] and p['side']==side]
  if related:t['relatedPartEvidence']=related;t['wholeStructureLimit']='Named source parts/heads are not a verified whole-muscle or separate tendon representation; no automatic identity or relation inheritance.'
  targets.append(t)
assert len({t['id'] for t in targets})==len(targets)
assert {t['familyId'] for t in targets}==set(FAMILIES)
assert all(sum(t['id'].rsplit('-',1)[0]==x['id'].rsplit('-',1)[0] for x in targets)==2 for t in targets)
assert not any(t['complete'] or t['anatomicallyAccepted'] or t['absenceClaim'] for t in targets)
assert all(not t['representations'] for t in targets if any(k in t['id'] for k in ['lumbrical-','dorsal-interosseous-','palmar-interosseous-']))
assert all(t['termEvidence'].get('numericId') is None for t in targets if t['termEvidence'].get('tableId','').find('*')>=0)
assert all(b['datasetId'] in ['male-body','upper-limb-nerve-reference'] for t in targets for b in t['representations'])
summary=dict(targets=len(targets),unsidedRequirements=len(frozen['seeds']),families=dict(Counter(t['familyId'] for t in targets)),detailLevels=dict(Counter(t['requiredDetail'] for t in targets)),targetKinds=dict(Counter(t['targetKind'] for t in targets)),bindingStatusCounts=dict(Counter(t['bindingStatus'] for t in targets)),positiveObservations=sum(len(t['representations']) for t in targets),datasetObservations=dict(Counter(b['datasetId'] for t in targets for b in t['representations'])),relatedGroupOnlyTargets=sum(bool(t.get('relatedGroupEvidence')) and not t['representations'] for t in targets),expertAccepted=0,newGeometry=0,newLabels=0,newRelationships=0)
unexpanded=[
 dict(familyId='skeletal-support',requirement='Remaining intercarpal/CMC/intermetacarpal ligament sets, each MCP/IP collateral and palmar plate, capsules/cartilage, individual sesamoids/variants and further landmarks. Named group and whole-bone observations do not close these.'),
 dict(familyId='muscle-tendon-fascia',requirement='Remaining individual extrinsic tendons, each extensor expansion/band, synovial sheaths, A/C pulley subdivisions, vincula, fascial septa, exact individual intrinsic-muscle numbering and pollical palmar-interosseous variation. Digit tendon and sheath requirements are selected D2 only.'),
 dict(familyId='neurovascular-lymph',requirement='Individual digital nerves by digit/side and parent, complete named muscular twigs, numbered/side-specific digital vessels, complete venous tributaries, lymphatic collectors/drainage routes and cross-region continuity. Current plural branch groups never close individual members.'),
 dict(familyId='organs-cavities-internal',requirement='Full compartment/space list, individual dorsal extensor compartments, thenar/midpalmar spaces, septa and directly sourced boundaries/contents; selected named spaces are requirements without inferred surfaces.')]
sources=[dict(id='zanatomy-ta2-pinned',title='Pinned Z-Anatomy-distributed TA2 table; numeric and nonnumeric IDs kept distinct',url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv'),dict(id='bp3d-retained-tables',title='Retained official BodyParts3D naming and membership tables',url='https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html'),dict(id='ttuhsc-hand',title='Texas Tech University Health Sciences Center El Paso anatomy tables — hand',url=frozen['sourceEvidence']['ttuhscHand']['url'],retrievedOn='2026-10-02',locators=['Joints and Associated Structures of the Hand','Muscles of the Hand / lumbrical, dorsal interosseous, palmar interosseous'],use='Bounded selected requirements; no relationship or model acceptance claim')]
result=dict(schemaVersion=1,scopeVersion='forearm-hand-target-inventory-v1',sourceRevision=frozen['sourceRevision'],status='candidate_planning_only;root_owns_integration',complete=False,scopeContract=frozen['scopeContract'],summary=summary,targets=targets,unexpandedRequirements=unexpanded,sources=sources,inputSnapshots=frozen['sourceSnapshots']+[dict(path='data/model-candidates/forearm-hand-target-inventory-v1/frozen-inputs.json',sha256=hashlib.sha256((OUT/'frozen-inputs.json').read_bytes()).hexdigest())],countingPolicy='Named requirements with bilateral IDs; groups and individual targets are explicitly distinct; no denominator of regional completeness. Requirements persist without positive bindings.',acceptance=dict(identity='planning observations only; K0 remains partial',geometry='existing manifest fields observed; no new geometry validation or clinical acceptance',localProduct='not exercised for this candidate-only seed',deployedProduct='not checked; owned by root',expert='pending'))
content=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
path=OUT/'proposal.json'
if '--check' in sys.argv:
 assert path.read_text()==content,'proposal.json differs from deterministic frozen-input projection'
 print(json.dumps(dict(result='PASS',check='deterministic frozen-input projection and identity/side/group/membership invariants',**summary),ensure_ascii=False))
else:
 path.write_text(content);print(json.dumps(summary,ensure_ascii=False))
