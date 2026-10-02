"""Bounded BP3D4.3 source intake; no network or active integration."""
import csv,hashlib,json,math,re,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
paths={'catalog':ROOT/'work/thyroid-alternative/bp3d-v43-manifest.csv','retainedMapping':ROOT/'work/thyroid-alternative/FMA2Obj.txt','mapping':OUT/'FMA2Obj.txt','license':OUT/'license.html','request':OUT/'request.json','base':ROOT/'public/models/atlas.json','targetInventory':ROOT/'data/model-candidates/upper-limb-target-inventory-v1/proposal.json','ta2':ROOT/'work/open-assets-review/TA2.csv','plexusManifest':ROOT/'public/models/extensions/brachial-plexus.json','sourceFetch':OUT/'source-fetch.json','sourceZip':OUT/'source-objects.zip'}
assert sha(paths['mapping'])==sha(paths['retainedMapping'])
text=paths['mapping'].read_text();assert text.startswith('# Data Version\t4.3\n# Objects set\t4.3\n# Tree version\tFMA3.0')
rows={};allfj=set()
for n,line in enumerate(text.splitlines(),1):
 c=line.split('\t')
 if len(c)==3 and not line.startswith('#'):
  ids=c[2].split('+');allfj.update(ids);rows.setdefault(c[0],[]).append(dict(conceptId=c[0],relationship=c[1],partIds=ids,line=n))
catalog={r['fj_id']:dict(r,csvLine=n) for n,r in enumerate(csv.DictReader(paths['catalog'].open()),2)}
base=read(paths['base']);assert base['version']=='BodyParts3D 4.0'
baseparts={p['id']:p for p in base['parts']};targets=read(paths['targetInventory'])['targets'];request=read(paths['request'])
terms={}
for i,line in enumerate(paths['ta2'].read_text().splitlines(),1):
 c=line.strip('"').split(';')
 if len(c)>2 and c[0].isdigit():terms[c[1]]=dict(id=int(c[0]),en=c[1],la=c[2],csvLine=i)
def mesh(path):
 header={};vs=[];fs=[]
 for line in path.read_text().splitlines():
  if line.startswith('# ') and ':' in line:
   k,v=line[2:].split(':',1);header[k.strip()]=v.strip()
  elif line.startswith('v '):
   v=[float(x) for x in line.split()[1:4]];assert len(v)==3 and all(math.isfinite(x) for x in v);vs.append(v)
  elif line.startswith('f '):fs.append([int(x.split('/')[0]) for x in line.split()[1:]])
 assert vs and fs and all(len(f)>=3 for f in fs)
 assert all(0<abs(i)<=len(vs) for f in fs for i in f)
 assert header['Compatibility version']=='4.3' and 'Bounds(mm)' in header
 fid=header['File ID'];cid=header['Concept ID'];assert fid in allfj
 relevant=rows[cid];assert any(fid in r['partIds'] for r in relevant)
 logic=header['Build-up logic'].split()[-1]
 assert any(r['relationship']==logic and fid in r['partIds'] for r in relevant)
 # Connectivity is basic file availability evidence, not anatomical segmentation.
 parents=list(range(len(vs)))
 def find(x):
  while parents[x]!=x:parents[x]=parents[parents[x]];x=parents[x]
  return x
 used=set()
 for face in fs:
  ind=[x-1 if x>0 else len(vs)+x for x in face];used.update(ind)
  for x in ind[1:]:parents[find(x)]=find(ind[0])
 components={}
 for x in used:components[find(x)]=components.get(find(x),0)+1
 bounds=[[min(v[j] for v in vs) for j in range(3)],[max(v[j] for v in vs) for j in range(3)]]
 record=dict(path=str(path.relative_to(ROOT)),sha256=sha(path),bytes=path.stat().st_size,header=header,sourcePartId=fid,returnedRepresentationId=header['Representation ID'],returnedConceptId=cid,sourceName=header['English name'],version='BodyParts3D4.3;objects4.3;FMA3.0',coordinateUnits='mm as declared by OBJ Bounds(mm) header; no rotation/scale/registration applied',observedMesh=dict(vertices=len(vs),polygons=len(fs),trianglesIfFanTriangulated=sum(len(f)-2 for f in fs),finiteVertices=True,indicesInRange=True,boundsMm=bounds,indexConnectedComponents=len(components),componentVertices=sorted(components.values(),reverse=True),looseVertices=len(vs)-len(used),checkScope='File parsing/counts/bounds/connectivity only; mesh quality, anatomical extent and registration unaccepted'),officialReturnedConceptMembership=copyrows(relevant),main40Comparison=dict(sameFjPresent=fid in baseparts,part=baseparts.get(fid),scope='Shared FJ alone would not establish geometry/version equivalence'),review=dict(anatomy='pending',geometryAudit='pending',registration='pending',labels='not_proposed',relationships='not_proposed'))
 return record
def copyrows(rs):return [dict(r) for r in rs]
objects=[mesh(p) for p in sorted((OUT/'objs').glob('*.obj'))]
assert len(objects)==17 and {o['sourcePartId'] for o in objects}==set(request['requestedIds'])
byfj={o['sourcePartId']:o for o in objects}
TARGET_MAP={
 'FJ4274':('Lateral cord of brachial plexus','named_cord_candidate'),
 'FJ4275':('Medial cord of brachial plexus','named_cord_candidate'),
 'FJ4264':('C5 root contribution to brachial plexus','spinal_nerve_trunk_context_only'),
 'FJ4265':('C6 root contribution to brachial plexus','spinal_nerve_trunk_context_only'),
 'FJ4266':('C7 root contribution to brachial plexus','spinal_nerve_trunk_context_only'),
 'FJ4267':('C8 root contribution to brachial plexus','spinal_nerve_trunk_context_only'),
 'FJ4245':('T1 root contribution to brachial plexus','spinal_nerve_trunk_context_only'),
 'FJ4171':('Axillary nerve','named_nerve_component_candidate'),'FJ4243':('Axillary nerve','named_nerve_component_candidate'),
 'FJ4172':('Radial nerve','named_nerve_component_candidate'),'FJ4240':('Radial nerve','named_nerve_component_candidate'),
 'FJ4258':('Ulnar nerve','named_nerve_candidate'),
 'FJ4185':('Intercostobrachial nerve','specifically_second_intercostobrachial_component'),
 'FJ4222':('Long thoracic nerve','named_trunk_not_whole_nerve_guarantee'),
 'FJ4223':('Medial pectoral nerve','named_collateral_candidate'),
 'FJ4242':('Superior subscapular nerve','named_collateral_candidate'),
 'FJ4256':('Thoracodorsal nerve','named_collateral_candidate'),
}
for o in objects:
 fj=o['sourcePartId'];name,scope=TARGET_MAP[fj];target=next(t for t in targets if t['name']==name and t['side']=='left')
 o['catalogEvidence']=catalog[fj]
 assert o['sourceName']==catalog[fj]['name'],'Returned source name changed; inspect before mapping'
 o['requestedRepresentationId']=catalog[fj]['bp_id']
 o['catalogDiscrepancy']=dict(catalogFmaId=catalog[fj]['fma_id'],returnedFmaId=o['returnedConceptId'],conceptIdDiffers=catalog[fj]['fma_id']!=o['returnedConceptId'],representationIdDiffers=catalog[fj]['bp_id']!=o['returnedRepresentationId'],rule='Returned official OBJ header and explicit source-version membership govern candidate identity; never replace with generic catalog FMA11195/FMA55665')
 assert o['observedMesh']['vertices']==int(catalog[fj]['verts']) and o['observedMesh']['polygons']==int(catalog[fj]['faces'])
 o['targetCorrespondence']=dict(targetId=target['id'],targetDataset='male-body requirement;source candidate unregistered',candidateDataset='bodyparts3d-4.3-source-unregistered',sourceSide='left_explicit_in_header',status=scope,activeTargetRepresentations=target['representations'],scope='Source-object identity only; no source-to-main geometric equivalence or complete-target binding')
 o['termEvidence']=target['termEvidence']
 if 'spinal_nerve_trunk' in scope:o['rootIdentityLimit']='Explicit C5/C6/C7/C8/T1 whole nerve-trunk name does not isolate a ventral ramus or prove this mesh is only the brachial-plexus root contribution. Exact root Latin and root-contribution binding remain withheld.'
 else:o['termCorrespondenceLimit']='Numeric terminology is target scope evidence, not a formal source-FMA crosswalk or anatomical extent acceptance.'
# Catalog-only observations outside the small downloaded selection stay distinctly unverified.
pat=r'brachial nerve plexus|(?:first thoracic|fifth cervical|sixth cervical|seventh cervical|eighth cervical) nerve|(?<!maxillary )axillary nerve|ulnar nerve|radial nerve|subscapular nerve|pectoral nerve|thoracodorsal nerve|long thoracic nerve|dorsal scapular nerve|suprascapular nerve|intercostobrachial|antebrachial cutaneous nerve|brachial cutaneous nerve|subclavian nerve'
catalog_only=[dict(r,status='retained_catalog_entry_only;file_not_acquired_or_checked',versionMembershipObserved=r['fj_id'] in allfj) for r in catalog.values() if re.search(pat,r['name'],re.I) and 'maxillary' not in r['name'].lower() and r['fj_id'] not in byfj]
query_names=['Lateral cord of brachial plexus','Medial cord of brachial plexus','Ulnar nerve','Radial nerve','Axillary nerve','Dorsal scapular nerve','Long thoracic nerve','Suprascapular nerve','Lateral pectoral nerve','Medial pectoral nerve','Superior subscapular nerve','Inferior subscapular nerve','Thoracodorsal nerve','Intercostobrachial nerve','Lateral antebrachial cutaneous nerve','Medial antebrachial cutaneous nerve','Medial brachial cutaneous nerve','Superior lateral brachial cutaneous nerve','Inferior lateral brachial cutaneous nerve','Posterior brachial cutaneous nerve','Posterior antebrachial cutaneous nerve']
queries=[]
for name in query_names:
 for side in ['left','right']:
  target=next(t for t in targets if t['name']==name and t['side']==side)
  ids=[o['sourcePartId'] for o in objects if o['targetCorrespondence']['targetId']==target['id']]
  queries.append(dict(targetId=target['id'],name=name,side=side,downloadedCandidatePartIds=ids,status='source_object_candidates_require_audit' if ids else 'no_positive_downloaded_binding_in_bounded_intake;not_absence',activeTargetBindingStatus=target['bindingStatus']))
contexts=[]
if (OUT/'context-objs').exists():
 contexts=[mesh(p) for p in sorted((OUT/'context-objs').glob('*.obj'))]
 context_request=read(OUT/'context-request.json')
 assert {c['sourcePartId'] for c in contexts}==set(context_request['requestedIds']+context_request['reusedIds'])
 for c in contexts:
  c['scope']='Same-version bone context for future frame audit; no registration accepted'
  c['acquisition']='reused_retained_official_source_zip' if c['sourcePartId'] in context_request['reusedIds'] else 'fresh_official_selected_download'
  c['catalogEvidence']=catalog[c['sourcePartId']]
  c['catalogDiscrepancy']=dict(catalogFmaId=c['catalogEvidence']['fma_id'],returnedFmaId=c['returnedConceptId'],catalogRepresentationId=c['catalogEvidence']['bp_id'],returnedRepresentationId=c['returnedRepresentationId'],rule='Keep exact returned header and matching official membership; catalog generic IDs are not substituted')
  assert c['observedMesh']['vertices']==int(c['catalogEvidence']['verts']) and c['observedMesh']['polygons']==int(c['catalogEvidence']['faces'])
 paths['contextRequest']=OUT/'context-request.json';paths['contextFetch']=OUT/'context-fetch.json';paths['contextZip']=OUT/'context-source.zip'
sourcehashes=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in paths.values()]+[dict(path=o['path'],sha256=o['sha256']) for o in objects+contexts]
sourcehashes.append(dict(path=str(Path(__file__).relative_to(ROOT)),sha256=sha(Path(__file__))))
result=dict(schemaVersion=1,scope='Bounded P3 BodyParts3D4.3 alternative-source intake; no active integration',sourceRevision='0ac477f2a686991bcb4f4d2a72267c9243547433',reviewedOn='2026-10-02',status='candidate_only;root_owns_decision',sources=[dict(id='bp3d43-live',title='BodyParts3D official live source',url='https://lifesciencedb.jp/bp3d/',creator='Database Center for Life Science (DBCLS)',version='Data4.3 / Objects4.3 / FMA3.0',license='CC BY-SA 2.1 Japan',licenseUrl='https://lifesciencedb.jp/bp3d/info_en/license/index.html',sourceLicenseUrl='https://creativecommons.org/licenses/by-sa/2.1/jp/',sourceReferenceBody='Source body; demographic/specimen detail not established in this bounded intake',rightsStatus=dict(privateInspection='permitted under captured public source license',adaptation='attribution/share-alike obligations retained',distribution='not activated; require source attribution/license retained and separate technical/expert acceptance'),coordinateUnits='OBJ source header states mm; no transform applied',access='Public normal selected-download endpoint;no authentication or access restriction bypass',retrievedOn='2026-10-02')],summary=dict(downloadedNeuralObjects=len(objects),namedCordObjects=2,spinalNerveTrunkContextObjects=5,otherNeuralObjects=10,contextBoneFiles=len(contexts),freshContextDownloads=sum(c['acquisition']=='fresh_official_selected_download' for c in contexts),reusedContextFiles=sum(c['acquisition']=='reused_retained_official_source_zip' for c in contexts),catalogOnlyObjects=len(catalog_only),catalogConceptDiscrepancies=sum(o['catalogDiscrepancy']['conceptIdDiffers'] for o in objects),catalogRepDiscrepancies=sum(o['catalogDiscrepancy']['representationIdDiffers'] for o in objects),activeMainSameFjParts=sum(o['main40Comparison']['sameFjPresent'] for o in objects),anatomicallyAccepted=0,registered=0),acquisitionPhases=[dict(phase=1,scope='17 selected nerve/cord/spinal-trunk objects',status='official OBJ availability and version membership verified'),dict(phase=2,scope='Bounded same-source bone context for subsequent frame audit',status='acquired;basic file evidence only' if contexts else 'pending independent acquisition')],objects=objects,contextObjects=contexts,catalogOnlyObservations=catalog_only,boundedTargetQueries=queries,decision=dict(cords='Improved LEFT identity evidence: separate named official files FJ4274/FMA45239 and FJ4275/FMA45241 with singleton is_a memberships; geometry/frame/extent still pending',roots='Improved individual spinal-level trunk naming, but no demonstrated isolated ventral-ramus C5–T1 plexus contribution. Do not accept these as resolved plexus roots.',rightSide='No right-side candidate acquired or positively identified by this bounded catalog audit; not a source-wide or anatomical absence claim',next='Audit named left cord/terminal component geometry with same-source regional bones; independently assess source-to-main registration and anatomical extent; roots remain distinct unresolved work'),inputSnapshots=sourcehashes,limits=['Do not activate candidate identifiers as main IDs','Do not equate generic catalog FMA parent with returned object identity','Two radial and two axillary files preserve component attribution; neither duplicate names nor shared BP imply interchangeable geometry','Catalog rows alone do not prove a mesh exists or its anatomical extent; only downloaded OBJ files have basic availability checks','Index-connected component counts do not name anatomical branches; duplicate-coordinate seams or fragmentation need geometry audit','Fine branches, whole nerve course, bilateral completeness and root connectivity remain unaccepted','No coordinates are fitted, mirrored or borrowed across sources','Source-side header and finite coordinates do not establish patient anatomy or registration','No new labels or anatomical relations proposed'])
encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if '--check' in sys.argv:
 assert (OUT/'proposal.json').read_text()==encoded,'Candidate differs from consumed inputs'
 print('PASS',json.dumps(result['summary']))
else:(OUT/'proposal.json').write_text(encoded);print('Wrote',json.dumps(result['summary']))
