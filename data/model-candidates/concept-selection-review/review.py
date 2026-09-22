"""Recompute bounded selection evidence; writes only beside this file."""
from pathlib import Path
import csv,json,hashlib,collections
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rows(name):return list(csv.DictReader((HERE/name).open(),delimiter='\t'))
def save(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
base=read('public/models/atlas.json');parts={p['id']:p for p in base['parts']};concepts={c['id']:c for c in base['concepts']}
source={};graphs={};names={}
for tree in ['isa','partof']:
 source[tree]=collections.defaultdict(list)
 for row in rows(tree+'_element_parts.txt'):source[tree][row['concept id']].append(row['element file id'])
 graphs[tree]=collections.defaultdict(list)
 for row in rows(tree+'_inclusion_relation_list.txt'):
  graphs[tree][row['parent id']].append(row['child id']);names[row['parent id']]=row['parent name'];names[row['child id']]=row['child name']
def descendants(tree,start):
 seen=set();stack=[start]
 while stack:
  id=stack.pop()
  if id in seen:continue
  seen.add(id);stack+=graphs[tree][id]
 return seen
def path(tree,start,goal):
 q=collections.deque([[start]]);seen={start}
 while q:
  route=q.popleft()
  if route[-1]==goal:return [dict(id=id,name=names.get(id)) for id in route]
  for child in graphs[tree][route[-1]]:
   if child not in seen:seen.add(child);q.append(route+[child])
 return None
skull=concepts['FMA46565'];bone_ids=descendants('isa','FMA5018')
kept=[];excluded=[]
for id in skull['elements']:
 p=parts[id];bone=p['conceptId'] in bone_ids
 row=dict(partId=id,sourceConceptId=p['conceptId'],sourceName=p['name'],currentSystem=p['system'],sourceIsABoneOrgan=bone,partOfPath=path('partof','FMA46565',p['conceptId']),isABoneOrganPath=path('isa','FMA5018',p['conceptId']))
 if bone and p['conceptId']!='FMA52749':kept.append(row)
 else:row['exclusionReason']='Hyoid is outside the proposed conventional 22-bone skull scope' if bone else 'Eye/lacrimal structure, not a skull bone';excluded.append(row)
assert len(kept)==22 and len(excluded)==21
assert skull['elements']==source['partof']['FMA46565']
proposal=dict(status='candidate_not_integrated',id='atlas:skull-bones',name='Skull bones',nameTr='Kafatası kemikleri',datasetId='male-body',sourceGroupId='FMA46565',sourceGroupName='skull',elements=[r['partId'] for r in kept],sourceConceptIds=[r['sourceConceptId'] for r in kept],sourceBaseManifestSha256=sha(ROOT/'public/models/atlas.json'),method='Explicit source-part allowlist: source FMA46565 PART-OF elements whose original per-part concept descends from IS-A FMA5018 bone organ, excluding FMA52749 hyoid; reviewed as 8 cranial plus 14 facial bones',scope='22 existing cranial/facial bone surfaces, including mandible; no hyoid, eye/lacrimal soft tissue, or middle-ear ossicles. This is a display composite, not a new FMA assertion or anatomical completeness certificate.',preserve={'sourceManifest':'unchanged','originalConceptId':'FMA46565','originalElements':skull['elements'],'suggestedOriginalLabelTr':'Kafatası (kaynak grubu)','suggestedOriginalNoteTr':'BodyParts3D kaynak grubu kafatası kemikleri yanında göz ve gözyaşı bezi yapıları ile hyoid yüzeylerini içerir.'},parts=kept,excludedSourceParts=excluded,sourceUrls=['https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_element_parts.txt','https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_inclusion_relation_list.txt','https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_inclusion_relation_list.txt','https://openstax.org/books/anatomy-and-physiology-2e/pages/7-1-divisions-of-the-skeletal-system'])
save('skull-bones-proposal.json',proposal)
# Load current additions for membership inspection only. No writes to registries/catalogs.
registry=read('public/models/extensions/index.json')
for url in registry['manifests']:
 ext=read('public'+url);parts.update({p['id']:p for p in ext['parts']})
 for c in ext['concepts']:
  prev=concepts.get(c['id']);concepts[c['id']]={**c,'elements':list(dict.fromkeys((prev['elements'] if prev else [])+c['elements']))}
coverage=read('data/anatomy/coverage.json');targets=[(r['id'],t) for r in coverage['regions'] for t in r['targets']][:65]
review=[];stats=collections.Counter()
special={'coverage:skull':'confirmed_named_scope_overreach','coverage:brain':'internal_cavities_in_source_group_not_automatic_overreach','coverage:heart':'cardiac_cavities_and_coronary_vessels_not_automatic_overreach','coverage:lungs':'bronchovascular_representation_scope_warning_not_overreach','coverage:liver':'hepatic_vessels_and_ducts_scope_warning_not_automatic_overreach','coverage:pancreas':'parenchyma_and_ducts_not_automatic_overreach','coverage:small-intestine':'shared_ileocecal_junction_boundary_not_automatic_overreach','coverage:large-intestine':'shared_ileocecal_junction_boundary_not_automatic_overreach'}
for index,(region,t) in enumerate(targets,1):
 row=dict(index=index,id=t['id'],nameTr=t['nameTr'],region=region,state=t['state'],finding=special.get(t['id'],'no_additional_obvious_overreach_in_id_name_review'),bindings=[])
 if t.get('separateReference'):row['finding']='separate_dataset_no_male_geometry_binding';row['separateReference']=t['separateReference']
 for b in t.get('currentBindings',[]):
  id=b['conceptId'];c=concepts.get(id);ids=c['elements'] if c else b['geometryPartIds'];a=set(source['isa'][id]);p=set(source['partof'][id]);s=set(ids)
  matching=[tree for tree,els in [('isa',a),('partof',p),('union',a|p)] if els and s==els]
  baseC=next((c for c in base['concepts'] if c['id']==id),None)
  baseMatching=[tree for tree,els in [('isa',a),('partof',p),('union',a|p)] if els and baseC and set(baseC['elements'])==els]
  stats['bindings']+=1
  if baseC:stats['baseBindings']+=1;stats['exactOfficialSourceBaseBindings']+=bool(baseMatching)
  row['bindings'].append(dict(conceptId=id,partCount=len(ids),officialCurrentSetMatches=matching,officialBaseSetMatches=baseMatching,parts=[dict(id=i,name=parts[i]['name'],conceptId=parts[i]['conceptId'],system=parts[i]['system']) for i in ids if i in parts],unresolvedPartIds=[i for i in ids if i not in parts]))
 review.append(row)
save('coverage-first-65-review.json',dict(scope='First 65 targets in stored region/target order; ID/name/source-membership review, not anatomical mesh verification',baseManifestSha256=sha(ROOT/'public/models/atlas.json'),coverageSha256=sha(ROOT/'data/anatomy/coverage.json'),stats=dict(stats),targets=review))
save('selection-pipeline-evidence.json',dict(skullExactOrderedMatch=True,sourceRowsOneBased=[10845,10887],sourceFile='partof_element_parts.txt',sourceMappingSha256=sha(HERE/'partof_element_parts.txt'),sourceManifestSha256=sha(ROOT/'public/models/atlas.json'),selectedPartCount=43,proposedBoneCount=22,excludedEyeLacrimalCount=19,excludedHyoidCount=2,codeEvidence=[dict(path=p,sha256=sha(ROOT/p)) for p in ['scripts/convert-anatomy.py','scripts/optimize-anatomy.mjs','app/knowledge.ts','app/page.tsx','app/coverage-panel.tsx','app/scene.tsx']],limitations=['Importer CONCEPT_MAP input is external to the checked-in converter; this review establishes exact agreement with official final source mapping, not provenance of an absent historical intermediate.','No visual rendering or expert surface/anatomical correctness certification performed.','System labels are not used as tissue type evidence.']))
print(dict(stats));print('proposal parts',len(kept),'excluded',len(excluded))
