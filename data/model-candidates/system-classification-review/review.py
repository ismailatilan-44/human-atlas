"""Compare active base-part systems to official source types; candidate files only."""
from pathlib import Path
import csv,collections,json,hashlib,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,obj):(P/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
snapshot=json.loads((P/'active-systems-snapshot.json').read_text())
assert snapshot['baseManifestSha256']==sha(ROOT/'public/models/atlas.json'),'Refresh active snapshot: base manifest changed'
assert snapshot['prepareAtlasSha256']==sha(ROOT/'app/atlas-metadata.ts'),'Refresh active snapshot: prepareAtlas changed'
assert len(snapshot['parts'])==2234
g=collections.defaultdict(list);names={};edge_lines={}
for line,r in enumerate(csv.DictReader((P/'isa_inclusion_relation_list.txt').open(),delimiter='\t'),2):
 a,b=r['parent id'],r['child id'];g[a].append(b);names[a]=r['parent name'];names[b]=r['child name'];edge_lines[a,b]=line
mapping=collections.defaultdict(set);mapping_lines={}
for line,r in enumerate(csv.DictReader((P/'isa_element_parts.txt').open(),delimiter='\t'),2):
 mapping[r['concept id']].add(r['element file id']);mapping_lines[r['concept id'],r['element file id']]=line
roots={'FMA5018':('bone organ','skeletal'),'FMA5022':('muscle organ','muscular'),'FMA10474':('zone of muscle organ','muscular'),'FMA85453':('head of muscle organ','muscular')}
def descendants(root):
 s=set();q=[root]
 while q:
  i=q.pop()
  if i in s:continue
  s.add(i);q+=g[i]
 return s
def path(root,goal):
 q=collections.deque([[root]]);seen={root}
 while q:
  route=q.popleft()
  if route[-1]==goal:
   return {'concepts':[{'id':x,'name':names[x]} for x in route],'sourceEdgeLines':[edge_lines[a,b] for a,b in zip(route,route[1:])]}
  for child in g[route[-1]]:
   if child not in seen:seen.add(child);q.append(route+[child])
sets={root:descendants(root) for root in roots};candidates=[];manual=[];resolved=[];aligned=[];outside=[];all_rows=[]
for p in snapshot['parts']:
 matches=[root for root in roots if p['conceptId'] in sets[root]]
 row={**p,'sourceClassMatches':[{'rootConceptId':root,'rootName':roots[root][0],'displaySystemForType':roots[root][1],'path':path(root,p['conceptId'])} for root in matches]}
 if not matches:
  row['status']='outside_checked_source_type_roots';outside.append(row)
 else:
  expected={roots[root][1] for root in matches}
  row['officialLeafMeshMappingConfirmed']=p['id'] in mapping[p['conceptId']]
  row['sourceElementMappingLine']=mapping_lines.get((p['conceptId'],p['id']))
  if len(expected)!=1 or not row['officialLeafMeshMappingConfirmed']:
   row.update(status='manual_source_identity_or_type_conflict',proposedSystem=None);manual.append(row)
  else:
   expected=next(iter(expected));row['typeBasedDisplaySystem']=expected
   if p['activeSystem']==expected:
    if p['rawSystem']!=expected:
     row['status']='already_corrected_by_prepareAtlas';resolved.append(row)
    else:row['status']='aligned_with_checked_type';aligned.append(row)
   elif expected=='muscular' and p['activeSystem'] in ['skeletal','connective']:
    row.update(status='proposed_clear_display_system_correction',proposedSystem='muscular',confidence='source_type_and_exact_mesh_mapping_confirmed',reason='Source identifies a named regional muscle organ, while the active display class is bone/connective; follow the existing subscapularis correction policy.');candidates.append(row)
   elif expected=='skeletal':
    row.update(status='manual_bone_display_conflict',proposedSystem=None);manual.append(row)
   else:
    row.update(status='manual_contextual_system_policy_review',proposedSystem=None,reason='Source muscle type is clear, but respiratory/pharyngeal context may be an intentional organ-system membership. Do not equate a type membership with exclusive UI system membership; decide the primary-layer policy or support secondary tags.');manual.append(row)
 all_rows.append(row)
summary={'basePartsScanned':len(all_rows),'classRootMatchCounts':{root:sum(p['conceptId'] in ss for p in snapshot['parts']) for root,ss in sets.items()},'uniquePartsWithinCheckedTypeRoots':len(all_rows)-len(outside),'alreadyAligned':len(aligned),'alreadyCorrected':len(resolved),'proposedClearCorrections':len(candidates),'manualReview':len(manual),'outsideCheckedTypeRoots':len(outside),'activeAdapterCorrectionsOutsideTypeScope':[p for p in snapshot['parts'] if p['rawSystem']!=p['activeSystem'] and not any(p['conceptId'] in ss for ss in sets.values())]}
provenance={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'baseManifestSha256':snapshot['baseManifestSha256'],'prepareAtlasSha256':snapshot['prepareAtlasSha256'],'sourceRelationSha256':sha(P/'isa_inclusion_relation_list.txt'),'sourceMappingSha256':sha(P/'isa_element_parts.txt'),'sourceRelationUrl':'https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_inclusion_relation_list.txt','sourceMappingUrl':'https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt'}
write('proposals.json',{'status':'candidate_not_integrated','provenance':provenance,'summary':summary,'safeDisplayOverrideProposal':{r['id']:r['proposedSystem'] for r in candidates},'candidates':candidates,'manualReview':manual,'alreadyCorrected':resolved})
write('all-parts-audit.json',{'scope':'All 2234 base parts; only four explicit source type roots are evaluated. No claim for unmatched types or anatomical surface correctness.','provenance':provenance,'summary':summary,'parts':all_rows})
print(json.dumps(summary,indent=2))
