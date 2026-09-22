"""Build direct source PARTOF navigation edges, confined to this candidate directory."""
from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];SRC=OUT.parent/'lung-surfaces'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
manifest=read(SRC/'lung-parenchyma.json');graph=read(ROOT/'data/anatomy/knowledge.json')
existing={r['id']:r for r in graph['relations']};nodes={n['id']:n for n in graph['entities']}
concepts=[c for c in manifest['concepts'] if c['id'] not in manifest['extendsConceptIds']]
assert len(concepts)==17
fetch=read(OUT/'source-fetch.json');records={r['conceptId']:r for r in fetch['records'] if r['endpoint']=='get-fmastratum.cgi'}
mapfile=SRC/'FMA2Obj.txt';mapping={}
for line,text in enumerate(mapfile.read_text().splitlines(),1):
 if text.startswith('#'):continue
 fields=text.split('\t')
 if len(fields)==3:mapping[(fields[0],fields[1])]={'line':line,'elements':fields[2].split('+')}
relations=[];paths=[];skipped=[]
lobes={'FMA7333','FMA7383','FMA7337','FMA7370','FMA7371'};lungs={'FMA7309':'right','FMA7310':'left'}
for c in concepts:
 fid=c['id'];record=records[fid];response=read(OUT/record['path'])
 assert sha(OUT/record['path'])==record['sha256']
 image=response['images'][0];assert image['f_id']==fid and image['name'].lower()==c['name'].lower()
 # Select an explicit source route through an existing named segment, lobe and lung.
 matches=[]
 for i,p in enumerate(image['partof_path2root']):
  f=p['fma']
  if len(f)>3 and f[0]['f_id']==fid and f[1]['f_id'] in nodes and f[2]['f_id'] in lobes and f[3]['f_id'] in lungs:
   matches.append((i,f[:4]))
 assert matches,fid
 index,route=matches[0];ids=[x['f_id'] for x in route]
 assert route[0]['potype']==[{'potabbr':'CPO','potid':2,'potname':'constitutional_part_of'}]
 assert all(x['t_delcause'] is None for x in route)
 assert all(any(p['potname']=='regional_part_of' for p in n['potype']) for n in route[1:3])
 side=lungs[ids[3]]
 explicitSide='left' if 'left' in c['name'].lower() else ('right' if 'right' in c['name'].lower() else None)
 assert explicitSide is None or explicitSide==side
 for n in route[1:]:assert nodes[n['f_id']]['side'] in [None,side]
 imported_edges=[]
 for a,b in zip(ids[1:],ids[2:]):
  key=f'{a}|part_of|{b}';assert key in existing,key
  imported_edges.append({'id':key,'evidence':existing[key]['evidence']})
 sourceMeshes=[p.replace('BP43-','') for p in c['elements']]
 membership=[]
 for concept_id in [fid,ids[2],ids[3]]:
  row=mapping[(concept_id,'part_of')]
  assert set(sourceMeshes)<=set(row['elements'])
  membership.append({'conceptId':concept_id,'line':row['line'],'containedSourceObjects':sourceMeshes})
 key=f'{fid}|part_of|{ids[1]}'
 locator=f"{record['path']}#/images/0/partof_path2root/{index}/fma/0..1; {fid} constitutional_part_of {ids[1]}; request pins version=4.3, ci_id=1, cb_id=5, md_id=1, mv_id=6, mr_id=1, bul_id=4"
 edge={'id':key,'subject':fid,'predicate':'part_of','object':ids[1],
       'evidence':[{'sourceId':'extension-lung-bp3d43','locator':locator,'url':record['url'],'snapshotSha256':record['sha256']}],
       'status':'source_imported','expertReview':'pending','scope':'selected_parenchyma_navigation_non_exhaustive',
       'qualifiers':{'sourceRelation':'constitutional_part_of','directSourceParent':True,'sourceDataVersion':'4.3','sourceTreeVersion':'FMA3.0',
                     'sourcePathToLung':ids,'navigationLobeId':ids[2],'navigationLungId':ids[3],'laterality':side,
                     'semantics':'Direct source anatomical parenchyma-to-segment relation. Lobe and lung membership follows the explicit transitive source path; no direct parent claim to lobe or lung.',
                     'geometry':'No contact, segmentation completeness, innervation or coordinate claim; object-set inclusion is corroboration only'}}
 if key in existing:skipped.append(key)
 else:relations.append(edge)
 paths.append({'parenchymaId':fid,'name':c['name'],'side':side,'sourceObjectIds':sourceMeshes,'sourcePathIndex':index,'sourcePath':[{'id':n['f_id'],'name':n['name'],'sourceRelationToNext':n.get('potype') if j<3 else None} for j,n in enumerate(route)],'newDirectRelationId':key,'existingGraphPathEdges':imported_edges,'sourceSnapshot':record,'objectMappingCorroboration':membership})
groups=[];group_evidence=[]
for lung_id,side in lungs.items():
 source_group=next(c for c in manifest['concepts'] if c['id']==lung_id)
 geometry=source_group['elements']
 assert len(geometry)==9 and len(set(geometry))==9
 assert set(geometry)=={p for c in concepts for p in c['elements'] if any(x['parenchymaId']==c['id'] and x['side']==side for x in paths)}
 group_id='atlas:'+side+'-lung-parenchyma-surfaces'
 assert group_id not in nodes, 'Project display group already exists; review merge before regeneration'
 group_ref={'sourceId':'extension-lung-bp3d43','locator':f'lung-parenchyma.json concepts[id={lung_id}].elements; sourceMembership; surfaceGroups; selected 9 BP43 parenchyma surface parts','snapshotSha256':sha(SRC/'lung-parenchyma.json')}
 groups.append({'id':group_id,'name':side.capitalize()+' lung parenchyma surfaces','side':side,'kind':'display_group','geometryPartIds':geometry,'representationStatus':'project_display_group','expertReview':'pending','anatomicalCoverage':'selected_source_parenchyma_surfaces_not_complete_organ_tissue','evidence':[group_ref],'provenanceKind':'project_derived_selection_group'})
 relations.append({'id':f'{group_id}|part_of|{lung_id}','subject':group_id,'predicate':'part_of','object':lung_id,'evidence':[group_ref],'status':'source_supported','expertReview':'pending','scope':'project_display_selection',
                   'qualifiers':{'semantics':'project display group of source parenchyma surfaces, not complete organ tissue assertion','provenanceKind':'project_derived_selection_group','directSourceParent':False,'laterality':side,'sourceMembershipConceptId':lung_id,'geometry':'Selection group only; no new anatomical FMA identity, surface geometry, segmentation completeness or spatial claim'}})
 group_evidence.append({'id':group_id,'lungId':lung_id,'side':side,'geometryPartIds':geometry,'source':group_ref,'assertionType':'project selection, not a new source anatomical concept'})
module={'schemaVersion':1,'scope':'17 direct source parenchyma-to-segment relations, existing segment/lobe/lung paths, and two separate project display-selection groups','entities':groups,'relations':relations}
write('module-proposal.json',module)
write('evidence.json',{'schemaVersion':1,'sourceId':'extension-lung-bp3d43','sourceVersion':'4.3','sourceTreeVersion':'FMA3.0','sourceRequestParameters':fetch['requestedParameters'],
 'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in [SRC/'lung-parenchyma.json',SRC/'bp3d-v43-mapping.zip',mapfile,ROOT/'data/anatomy/knowledge.json',OUT/'versions.json',OUT/'source-fetch.json']],
 'versionResolutionEvidence':{'metadataUrl':fetch['versionMetadataUrl'],'locator':'versions.json records[tgi_version=4.3]: cb_id=5, ci_id=1, md_id=1, mv_id=6, mr_id=1, tgi_tree_version=FMA3.0','responseProof':'source/FMA27368-partof.json: data entries explicitly report model_version=4.3, concept_info=FMA, concept_build=3.0, cb_id=5, bul_id=4'},
 'paths':paths,'projectDisplayGroups':group_evidence,'existingEdgesSkipped':skipped,'requiredExtensionConceptIds':[c['id'] for c in concepts],
 'integrationDependency':'Register the lung extension first or in the same build so its 17 parenchyma concepts and 18 geometry parts exist. Only two collision-free project selection entities are declared; source concepts are not duplicated.',
 'warnings':['Version=4.3 alone currently resolves a newer concept build (4.12.0-inference); exact model/concept IDs were explicitly pinned to the official 4.3 FMA3.0 metadata.','FMA2Obj PARTOF object sets corroborate membership only; all graph relations come from explicit partof_path2root routes.','Some anatomical names omit left/right; side is resolved from the explicit right/left lung ancestor, not name guessing or coordinates.']})
write('validation.json',{'status':'source_path_checks_passed','parenchymaConcepts':17,'candidateRelations':len(relations),'sourceDirectRelations':len(relations)-2,'projectSelectionRelations':2,'existingEdgesSkipped':len(skipped),'newProjectEntities':2,'displayGroupPartCounts':[len(g['geometryPartIds']) for g in groups],'existingSegmentParents':len({p['sourcePath'][1]['id'] for p in paths}),'lobesReached':len({p['sourcePath'][2]['id'] for p in paths}),'lungsReached':len({p['sourcePath'][3]['id'] for p in paths}),'leftConcepts':sum(p['side']=='left' for p in paths),'rightConcepts':sum(p['side']=='right' for p in paths),'existingHierarchyEdgesReused':len({e['id'] for p in paths for e in p['existingGraphPathEdges']}),'sourceTreePinned':True,'objectSetInclusionUsedAsAnatomicalParentEvidence':False})
print('Prepared',len(relations)-2,'new source edges and 2 project selection edges; all 17 source paths reach existing 5 lobes and 2 lungs.')
