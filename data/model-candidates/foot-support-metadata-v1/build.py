"""Deterministic support metadata candidate; writes only its own directory."""
import copy, hashlib, json, math, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
REV='0a501618801a5fbc8db44599d24eb50dfde0fba4'
read=lambda p:json.loads((ROOT/p).read_text())
sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
paths={
 'mapping':'data/model-candidates/foot-support-source-audit-v1/new-object-mapping.json',
 'evaluation':'data/model-candidates/foot-support-source-audit-v1/evaluated-candidates.json',
 'base':'public/models/atlas.json', 'knowledge':'data/anatomy/knowledge.json',
 'activeLabels':'data/anatomy/labels.json',
 'reference':'public/models/lower-limb-nerve-reference/atlas.json',
 'referenceMetadata':'data/anatomy/lower-limb-reference.json',
 'ta2':'work/open-assets-review/TA2.csv',
 'names':'data/model-candidates/coverage-labels/bp3d-isa-parts-list-e.txt',
 'membership':'data/model-candidates/concept-selection-review/isa_element_parts.txt',
 'partofNames':'data/model-candidates/coverage-labels/bp3d-partof-parts-list-e.txt',
 'priorTargets':'data/anatomy/regional-targets-lower-limb-v3.json',
 'producer':'data/model-candidates/foot-support-metadata-v1/build.py',
 'sourceCandidateManifest':'data/model-candidates/foot-support-source-audit-v1/atlas.json',
}
TR={
 'Flexor retinaculum of ankle':'Ayak bileği fleksör retinakulumu',
 'Superior extensor retinaculum of ankle':'Ayak bileği üst ekstansör retinakulumu',
 'Inferior extensor retinaculum of ankle':'Ayak bileği alt ekstansör retinakulumu',
 'Superior fibular retinaculum':'Üst fibular retinakulum',
 'Inferior fibular retinaculum':'Alt fibular retinakulum',
 'Plantar aponeurosis':'Plantar aponevroz',
 'Long plantar ligament':'Uzun plantar bağ',
 'Plantar calcaneocuboid ligament':'Plantar kalkaneokuboid bağ',
 'Plantar calcaneonavicular ligament':'Plantar kalkaneonaviküler bağ',
 'Intersesamoid ligament':'İntersesamoid bağ',
}
TERMS={}
for line_no,line in enumerate((ROOT/paths['ta2']).read_text().splitlines(),1):
 cells=line.strip('"').split(';')
 if len(cells)>2 and cells[1] in TR:
  assert cells[0].isdigit()
  TERMS[cells[1]]=dict(id=int(cells[0]),en=cells[1],la=cells[2],csvLine=line_no)
assert len(TERMS)==10
mapping=read(paths['mapping']);evaluation=read(paths['evaluation'])
byobject={c['sourceObject']:c for c in evaluation['candidates']}
candidate=read(paths['sourceCandidateManifest']);candidateparts={p['id']:p for p in candidate['parts']};defects={p['partId']:p for p in candidate['inheritedMeshDefects']}
assert {m['sourceObject'] for m in mapping}=={n+'.'+s for n in TR for s in ['l','r']}
assert len(mapping)==len(byobject)==20
base=read(paths['base']);graph=read(paths['knowledge']);ref=read(paths['reference']);refmeta=read(paths['referenceMetadata']);active=read(paths['activeLabels'])['entries'];prior=read(paths['priorTargets'])
assert base['source']=='BodyParts3D' and base['version']=='BodyParts3D 4.0'
assert len(prior['targets'])==136
concepts={c['id']:c for c in base['concepts']};byname={c['name']:c for c in base['concepts']};parts={p['id']:p for p in base['parts']};entities={e['id']:e for e in graph['entities']}
refconcepts={c['id']:c for c in ref['concepts']};refparts={p['id']:p for p in ref['parts']}
names={};members={}
for i,line in enumerate((ROOT/paths['names']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:names[c[0]]=dict(conceptId=c[0],representationId=c[1],name=c[2],line=i)
for i,line in enumerate((ROOT/paths['membership']).read_text().splitlines(),1):
 c=line.split('\t')
 if len(c)==3:members.setdefault(c[0],[]).append(dict(conceptId=c[0],name=c[1],partId=c[2],line=i))
def binding(cid):
 c=concepts[cid];query=c['name'];observed=[parts[p] for p in c['elements']]
 assert names[cid]['name']==query
 assert sorted(r['partId'] for r in members[cid])==sorted(c['elements'])
 assert all(r['name']==query for r in members[cid])
 assert entities[cid]['geometryPartIds']==c['elements']
 for p in observed:
  assert p['vertexCount']>0 and p['indexCount']>0 and all(math.isfinite(n) for b in p['bounds'] for n in b)
 return dict(datasetId='male-body',sourceVersion=base['version'],conceptId=cid,sourceName=query,partIds=c['elements'],sourceManifest=paths['base'],locator='concepts/'+cid,officialNameRow=names[cid],officialMembershipRows=members[cid],observedParts=observed,confidence='exact_source_name_and_manifest_membership_verified;anatomical_geometry_review_pending',scopeCorrespondence='Independent source identity and coordinate frame; no same-geometry claim')
def kind(name):
 return 'retinaculum' if 'retinaculum' in name else 'aponeurosis' if 'aponeurosis' in name else 'ligament'
def note(name):
 if kind(name)=='retinaculum':return 'Kaynakta adlandırılmış tutucu bağ dokusu yüzeyi gösterilir. Ayrı lif katmanları, tendon kılıfları ve kesin kemik tutunma alanları bu seçimde ayırt edilmez. Anatomik uzman incelemesi bekliyor.'
 if kind(name)=='aponeurosis':return 'Kaynakta adlandırılmış plantar aponevroz yüzeyi gösterilir. Ayrı bantlar, parmak uzantıları ve ince lif katmanları bağımsız yapılar olarak doğrulanmaz. Anatomik uzman incelemesi bekliyor.'
 if name=='Intersesamoid ligament':return 'Kaynağın intersesamoid bağ adıyla sunduğu kaba yüzeydir. Kaynak konumu iki sesamoid bileşenini birleştirmediğinden öğrenci referansına alınmaz; doğru geometri veya alternatif kaynak gereklidir. Anatomik uzman incelemesi bekliyor.'
 return 'Kaynakta adlandırılmış bağ yüzeyi gösterilir. Ayrı lif demetleri, katmanlar ve kesin kemik tutunma alanları bu seçimde ayırt edilmez. Anatomik uzman incelemesi bekliyor.'
def label(name,side,cid,dataset,source):
 t=TERMS[name]
 return dict(ids=[cid],datasetId=dataset,sourceEnglish=source,tr=TR[name],en=name,la=t['la'],side=side,aliases=list(dict.fromkeys([source,name])),ta2TableId=t['id'],trStatus='editorial',expertReview='pending',anatomicalScope=kind(name),scopeNoteTr=note(name),representationNoteTr=note(name),latinUnavailableReason=None,sourceTerm=copy.deepcopy(t),evidence=[dict(sourceId='zanatomy-ta2-pinned',locator=f'TA2 table row {t["id"]}; CSV line {t["csvLine"]}; exact English/Latin columns',scope='Exact numeric source term at named scope; no formal FMA crosswalk')])
def guard(entries,new):
 for old in entries:
  if set(old['ids']) & set(new['ids']):assert old==new,'Conflicting integrated label '+new['ids'][0]
refs=[];mains=[];targets=[];audit=[]
for m in mapping:
 source=m['sourceObject'];name=source[:-2];side=m['side'];assert source.endswith('.'+side[0]) and side in ['left','right']
 slug=re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')
 assert m['conceptId']=='zanatomy:'+slug+'-'+side[0] and m['partId']=='ZA-LLR-'+slug.upper()+'-'+side[0].upper()
 geom=byobject[source]['geometry'];assert geom['selectableEvaluatedGeometry'] and geom['observedSide']==side
 l=label(name,side,m['conceptId'],refmeta['datasetId'],name)
 l.update(sourceObject=source,componentRole=m['componentRole'],geometryPartIds=[m['partId']],sourceScope=m['scope'])
 l['aliases']=list(dict.fromkeys([source,name,TERMS[name]['la']]))
 assert geom['topology']['boundaryEdges']==m['expectedBoundaryEdges']
 assert geom['topology']['triangleConnectedComponents']==1
 assert all(geom['topology'][key]==0 for key in ['zeroAreaTriangles','nonManifoldEdges','looseVertices'])
 l['sourceRepresentation']=dict(objectType=geom['sourceObjectType'],baseVertices=geom['baseVertices'],basePolygons=geom['basePolygons'],evaluatedVertices=geom['evaluatedVertices'],evaluatedTriangles=geom['evaluatedTriangles'],modifiers=copy.deepcopy(geom['modifiers']),topology=copy.deepcopy(geom['topology']),geometryReviewPath=paths['evaluation'],scope='Connectivity and open boundaries describe source surface representation, not named anatomical layers or subdivisions')
 if name in ['Inferior fibular retinaculum','Plantar aponeurosis']:
  l['representationNoteTr']='Kaynak modeli kenarları açık, ince bir yüzey olarak gösterilir; gerçek doku kalınlığı bu görünümden ölçülemez. '+note(name)
 elif name in ['Plantar calcaneocuboid ligament','Plantar calcaneonavicular ligament','Intersesamoid ligament']:
  l['representationNoteTr']='Bağın genel biçimi basit bir kaynak yüzeyiyle temsil edilir; ayrıntılı lif düzeni veya gerçek doku kalınlığı gösterilmez. '+note(name)
 if name=='Long plantar ligament':
  l['representationNoteTr']+=' Kaynak yüzeyinin bazı küçük alanlarında gölgelendirme kusuru görülebilir.'
  l['sourceRepresentation']['inheritedNormalDefect']=copy.deepcopy(defects[m['partId']])
  assert defects[m['partId']]['nonpositiveInterpolatedFaceNormals']==5
 assert candidateparts[m['partId']]['sourceObject']==source
 l['scopeNoteTr']=l['representationNoteTr']
 l['evidence'].append(dict(sourceId='zanatomy-lower-limb-source',locator='Z-Anatomy/Startup.blend object '+source,scope='Exact source object, authored support scope and laterality; geometry and license acceptance separate'))
 guard(refmeta['labels'],l)
 if m['conceptId'] in refconcepts:
  assert refconcepts[m['conceptId']]['elements']==[m['partId']] and refparts[m['partId']]['sourceObject']==source
 refs.append(l)
 matches=[]
 query=side+' '+name.lower()
 if query in byname:
  b=binding(byname[query]['id']);assert name=='Long plantar ligament'
  assert len(b['partIds'])==1 and entities[b['conceptId']]['side']==side
  assert b['observedParts'][0]['conceptId']==b['conceptId'] and b['observedParts'][0]['name'].lower()==query
  matches.append(b);audit.append(b)
  ml=label(name,side,b['conceptId'],'male-body',query)
  ml['evidence'] += [dict(sourceId='foot-support-bp3d40-names',locator=f'line {b["officialNameRow"]["line"]}; {b["conceptId"]}'),dict(sourceId='foot-support-bp3d40-membership',locator='; '.join('line '+str(r['line']) for r in b['officialMembershipRows']))]
  guard(active,ml);mains.append(ml)
 targets.append(dict(id='foot-support-v1:'+slug+'-'+side[0],regionId='leg-ankle-foot',familyId='muscle-tendon-fascia' if kind(name) in ['retinaculum','aponeurosis'] else 'skeletal-support',side=side,requiredDetail='D2',targetKind=kind(name),scope=name,requirementStatus='non_exhaustive_source_named_target;curriculum_and_expert_pending',terminology=dict(sourceNumericTerm=TERMS[name],formalFmaCrosswalk='not_asserted',latinDisplayStatus='exact_numeric_source_term'),representations=[dict(datasetId=refmeta['datasetId'],conceptId=m['conceptId'],sourceObject=source,partIds=[m['partId']],mappingPath=paths['mapping'],status='evaluated_named_source_support;export_and_release_acceptance_separate',sourceScope=m['scope'],coverageStatus='named_source_surface_only;fine_layers_and_attachment_footprints_unverified')]+matches,mainBindingStatus='observed_existing_source_binding' if matches else 'no_positive_binding_in_bounded_source_table_and_manifest_audit;not_absence',expertReview='pending',anatomicallyAccepted=False,absenceClaim=False,openCriteria=['Source surface/detail review','Anatomical identity and support extent review','Source-specific user journey and context','Fine layers and attachment footprints unresolved','Expert anatomy acceptance']))
# Each fact is independently verified in the primary teaching table at its exact row.
# Bone concepts are whole-bone context; named regions are text qualifiers only.
FACTS=[
 ('Long plantar ligament','calcaneus','Kalkaneustaki tutunma bölgesi','foot-support-joints-table','Joints - Foot; long plantar ligament; Significance'),
 ('Long plantar ligament','cuboid-bone','Kuboid kemikteki tutunma bölgesi','foot-support-joints-table','Joints - Foot; long plantar ligament; Significance'),
 ('Plantar calcaneocuboid ligament','calcaneus','Kalkaneusun alt yüzündeki tutunma bölgesi','foot-support-joints-table','Joints - Foot; plantar calcaneocuboid (short plantar) ligament; Significance'),
 ('Plantar calcaneocuboid ligament','cuboid-bone','Kuboid kemiğin alt yüzündeki tutunma bölgesi','foot-support-joints-table','Joints - Foot; plantar calcaneocuboid (short plantar) ligament; Significance'),
 ('Plantar calcaneonavicular ligament','calcaneus','Kalkaneusun sustentaculum tali bölgesi','foot-support-joints-table','Joints - Foot; plantar calcaneonavicular ligament; Significance'),
 ('Plantar calcaneonavicular ligament','navicular-bone','Naviküler kemiğin alt yüzü','foot-support-joints-table','Joints - Foot; plantar calcaneonavicular ligament; Significance'),
 ('Plantar aponeurosis','calcaneus','Kalkaneus tüberositesi','foot-support-leg-table','Osteology; calcaneus / calcaneal tuberosity; Notes'),
 ('Flexor retinaculum of ankle','tibia','Tibianın medial malleol ucundaki tutunma bölgesi','foot-support-leg-schemes','Topographic Anatomy; flexor retinaculum; Boundaries/Description'),
 ('Flexor retinaculum of ankle','calcaneus','Kalkaneustaki tutunma bölgesi','foot-support-leg-schemes','Topographic Anatomy; flexor retinaculum; Boundaries/Description'),
 ('Superior extensor retinaculum of ankle','tibia','Tibiada malleolün proksimalindeki tutunma bölgesi','foot-support-leg-table','Topographic Anatomy; extensor retinaculum, superior; Boundaries/Description'),
 ('Superior extensor retinaculum of ankle','fibula','Fibulada malleolün proksimalindeki tutunma bölgesi','foot-support-leg-table','Topographic Anatomy; extensor retinaculum, superior; Boundaries/Description'),
 ('Inferior extensor retinaculum of ankle','calcaneus','Kalkaneusun ön-üst yüzü','foot-support-leg-table','Topographic Anatomy; extensor retinaculum, inferior; Boundaries/Description'),
 ('Superior fibular retinaculum','fibula','Fibulanın lateral malleol ucu','foot-support-leg-table','Topographic Anatomy; fibular retinaculum, superior; Boundaries/Description'),
 ('Superior fibular retinaculum','calcaneus','Kalkaneustaki tutunma bölgesi','foot-support-leg-table','Topographic Anatomy; fibular retinaculum, superior; Boundaries/Description'),
]
relations=[]
for name,bone,region,sourceid,locator in FACTS:
 for side in ['left','right']:
  m=next(m for m in mapping if m['sourceObject']==name+'.'+side[0])
  pairs=[(refmeta['datasetId'],m['conceptId'],'zanatomy:'+bone+'-'+side[0])]
  if name=='Long plantar ligament':pairs.append(('male-body',byname[side+' long plantar ligament']['id'],byname[side+' '+('cuboid bone' if bone=='cuboid-bone' else bone)]['id']))
  for dataset,subject,obj in pairs:
   edge=dict(id=subject+'|attaches_to|'+obj,datasetId=dataset,subject=subject,predicate='attaches_to',object=obj,status='source_supported',expertReview='pending',scope='selected_typical_anatomy;non_exhaustive',attachmentNoteTr=region+' — kesin model yüzey işareti yok',evidence=[dict(sourceId=sourceid,locator=locator)],qualifiers=dict(landmarkTr=region,targetRole='context_bone',laterality='Same-side instantiation of an unsided educational fact; not source-specimen validated',semantics='Selected named region on a whole-bone context target; not a complete endpoint set or whole-bone attachment footprint',geometry='No model coordinates, contact, anchors or segmented attachment surface asserted',requiresLandmarkDisplay=True))
   edge['qualifiers']['attachmentNoteTr']=edge['attachmentNoteTr']
   if name=='Long plantar ligament':
    edge['qualifiers']['incompleteEndpointSet']='Only calcaneus and cuboid selected; metatarsal patterns vary and remain unresolved for this specimen/source object'
    edge['qualifiers']['variationEvidence']=[dict(sourceId='ward-soames-1997',locator='Abstract; shape, bands and attachments vary'),dict(sourceId='hiramoto-1983',locator='Abstract; anterior metatarsal attachment patterns vary')]
   ids=set(concepts) if dataset=='male-body' else set(refconcepts)|{m['conceptId'] for m in mapping}
   assert subject in ids and obj in ids
   if dataset=='male-body':assert entities[subject]['side']==entities[obj]['side']==side
   else:assert obj.endswith('-'+side[0])
   for old in (graph['relations'] if dataset=='male-body' else refmeta['relations']):
    if old['id']==edge['id']:assert {k:v for k,v in old.items() if k!='datasetId'}=={k:v for k,v in edge.items() if k!='datasetId'},'Conflicting integrated relation '+edge['id']
   relations.append(edge)
assert len(relations)==32 and len({(r['datasetId'],r['id']) for r in relations})==32
assert sum(r['datasetId']=='male-body' for r in relations)==4

parent=binding('FMA44248');parent['scope']='Existing unsided source concept selects both long plantar ligament parts; no proposed label, new parent, group or relation'
assert len(refs)==20 and len(mains)==len(audit)==2 and len(targets)==20
assert len({x['ids'][0] for x in refs})==20 and all(l['la'] for l in refs+mains)
assert {x['conceptId'] for x in audit}=={'FMA44249','FMA44250'}
assert {p for x in audit for p in x['partIds']}=={'FJ1424','FJ1424M'}
assert not ({t['id'] for t in targets}&{t['id'] for t in prior['targets']})
assert {t['familyId'] for t in targets}<={t['familyId'] for t in prior['targets']}
sources=[dict(id='zanatomy-ta2-pinned',title='Pinned Z-Anatomy-distributed TA2 table',url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv',path=paths['ta2'],sha256=sha(paths['ta2']),use='Exact numeric scoped terms; no invented laterality, subdivisions or formal FMA crosswalk'),dict(id='zanatomy-lower-limb-source',title='Pinned Z-Anatomy source objects',url='https://github.com/Z-Anatomy/Models-of-human-anatomy',member='Z-Anatomy/Startup.blend',sourceArtifactSha256='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd',mappingPath=paths['mapping'],use='Named source geometry; source package owns license, frame, adaptation and release acceptance'),dict(id='foot-support-bp3d40-names',title='Retained official BodyParts3D 4.0 names',url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt',path=paths['names']),dict(id='foot-support-bp3d40-membership',title='Retained official BodyParts3D 4.0 element memberships',url='https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt',path=paths['membership'])]
for s in sources:s['verifiedOn']='2026-10-02';s['verificationMethod']='Retained pinned local source; no new remote fetch'
sources += [
 dict(id='foot-support-joints-table',title='TTUHSC Anatomy Tables — Joints of the Lower Limb',url='https://anatomy.ttuhscep.edu/musculoskeletal_system/joints_lower_tables.html',locator='Joints - Foot; long plantar, plantar calcaneocuboid and plantar calcaneonavicular rows',use='Selected named attachment facts only'),
 dict(id='foot-support-leg-table',title='TTUHSC Anatomy Tables — Anterior & Lateral Leg & Foot',url='https://anatomy.ttuhscep.edu/musculoskeletal_system/leg_tables.html',locator='Osteology calcaneal tuberosity; Topographic Anatomy extensor and superior fibular retinacula',use='Selected named attachment facts only'),
 dict(id='foot-support-leg-schemes',title='TTUHSC Anatomy Tables — Leg & Foot',url='https://anatomy.ttuhscep.edu/schemes/leg_tables.html',locator='Topographic Anatomy; flexor retinaculum',use='Selected named attachment facts only'),
 dict(id='ward-soames-1997',title='Morphology of the plantar calcaneocuboid ligaments',url='https://pubmed.ncbi.nlm.nih.gov/9347303/',doi='10.1177/107110079701801009',locator='Indexed primary publication abstract',use='Variation rationale, not exact source-specimen attachment proof',fetchConstraint='Direct PubMed open returned internal error; indexed primary abstract read successfully'),
 dict(id='hiramoto-1983',title='Variation of the Long Plantar Ligament in Japanese',url='https://www.jstage.jst.go.jp/article/ofaj1936/60/6/60_401/_article',doi='10.2535/ofaj1936.60.6_401',locator='Primary journal abstract',use='Metatarsal attachment variation rationale; omit source-specimen digit assignment'),
]
for source in sources[4:]:source.update(verifiedOn='2026-10-02',verificationMethod='Primary webpage or indexed primary abstract read via web',redistribution='Original factual paraphrases and anatomical names only; no table prose or images copied')
sourceids={s['id'] for s in sources}
for r in relations:assert all(e['sourceId'] in sourceids for e in r['evidence'])
for l in refs+mains:assert all(e['sourceId'] in sourceids for e in l['evidence'])
result=dict(schemaVersion=1,scopeVersion='foot-support-metadata-v1',sourceRevision=REV,reviewedOn='2026-10-02',status='source_audit_proposal;activation_and_release_owned_by_root',scope='Twenty non-exhaustive named foot/ankle support source objects; layers and attachment footprints unresolved',summary=dict(referenceLabels=20,referenceRetinacula=10,referenceAponeuroses=2,referenceLigaments=8,referenceLatinPresent=20,referenceLatinUnresolved=0,mainLabels=2,mainParts=2,mainLatinPresent=2,mainLatinUnresolved=0,targets=20,targetsWithMainEvidence=2,priorTargetCount=136,referenceRelations=28,mainRelations=4,relationProposals=32,anatomicallyAccepted=0),referenceLabelProposals=refs,mainLabelProposals=mains,targetProposals=targets,relationProposals=relations,mainBindingAudit=audit,existingParentEvidence=[parent],sources=sources,inputSnapshots=[dict(path=p,sha256=sha(p)) for p in paths.values()],limits=['Twenty source objects do not establish regional completeness','Named source geometry and exact TA2 term are separate evidence from anatomical correctness','No named finer layers, fascicles, slips or attachment footprints inferred from mesh connectivity','Existing unsided main long plantar ligament concept is evidence only; no new group or label','No positive bounded main mapping is not evidence of anatomical absence','No source-to-main geometry equivalence or borrowed frame','Selected sourced attachment facts only; no complete endpoint set, model contacts, attachment anchors or innervation asserted','The prior 136 targets are read and hashed, never altered by this producer','Source geometry, local interaction, deployment and expert acceptance remain separate'])
encoded=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if '--check' in sys.argv:
 assert (OUT/'proposal.json').read_text()==encoded,'Candidate differs from current consumed input snapshots'
 print('PASS deterministic 20 reference labels / 2 main labels / 20 targets / 32 selected relations; exact memberships and numeric terms')
else:
 (OUT/'proposal.json').write_text(encoded)
 print('Wrote scoped candidate proposal; assertions passed')
