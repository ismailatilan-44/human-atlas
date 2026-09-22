"""Build reviewed facts as an inactive candidate only; never write canonical data."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent

def read(p): return json.loads((ROOT/p).read_text())
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

graph=read('data/anatomy/knowledge.json');nodes={e['id']:e for e in graph['entities']}
atlas=read('public/models/atlas.json');concepts={e['id']:e for e in atlas['concepts']}
parts={p['id']:p for p in atlas['parts']}
TA_PATH='work/open-assets-review/TA2.csv'
TA_HASH='0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
assert sha(TA_PATH)==TA_HASH
terms={}
for line_number,line in enumerate((ROOT/TA_PATH).read_text().splitlines(),1):
 fields=line.strip('"').split(';')
 if len(fields)>2 and fields[0].isdigit(): terms[int(fields[0])]={'en':fields[1],'la':fields[2],'line':line_number}
SOURCES=[next(s for s in read('data/anatomy/sources.json') if s['id']=='uams-upper-limb'),
 {'id':'ttuhsc-axilla-shoulder-tables','title':'Texas Tech University Health Sciences Center El Paso — Axilla, Posterior Shoulder, & Arm anatomy tables','url':'https://anatomy.ttuhscep.edu/musculoskeletal_system/axilla_tables.html','retrievedOn':'2026-09-22','use':'Selected muscle origin/insertion/innervation and named nerve motor facts; row/column locators; no images or article copying'},
 {'id':'zanatomy-ta2-terminology','title':'Z-Anatomy TA2 terminology table, pinned revision','url':'https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv','path':TA_PATH,'sha256':TA_HASH,'retrievedOn':'2026-09-22','use':'Exact English/Latin naming rows, not anatomical relationship evidence; Turkish strings are editorial translations with expert review pending'}]
# IDs confirmed independently in canonical graph and main manifest. Ordering is left, right.
MUSCLES=[
 dict(key='supraspinatus',ids=['FMA32545','FMA32544'],parts=['FJ1506M','FJ1506'],ta=2457,tr='Supraspinatus kası',origin='supraspinous fossa of scapula',originTr='Skapulanın supraspinöz fossası',insertion='superior facet of greater tubercle of humerus',insertionTr='Humerusun büyük tüberkülünün üst faseti',nerves=['suprascapular']),
 dict(key='infraspinatus',ids=['FMA32548','FMA32547'],parts=['FJ1500M','FJ1500'],ta=2458,tr='İnfraspinatus kası',origin='infraspinous fossa of scapula',originTr='Skapulanın infraspinöz fossası',insertion='middle facet of greater tubercle of humerus',insertionTr='Humerusun büyük tüberkülünün orta faseti',nerves=['suprascapular']),
 dict(key='teres minor',ids=['FMA32554','FMA32553'],parts=['FJ1508M','FJ1508'],ta=2459,tr='Teres minor kası',origin='superior two-thirds of lateral border of scapula',originTr='Skapulanın dış kenarının üst üçte ikisi',insertion='inferior facet of greater tubercle of humerus',insertionTr='Humerusun büyük tüberkülünün alt faseti',nerves=['axillary']),
 dict(key='subscapularis',ids=['FMA13415','FMA13414'],parts=['FJ1504M','FJ1504'],ta=2460,tr='Subskapularis kası',origin='medial two-thirds of costal surface of scapula, within subscapular fossa',originTr='Skapulanın kostal yüzünün iç üçte ikisi, subskapular fossa',insertion='lesser tubercle of humerus',insertionTr='Humerusun küçük tüberkülü',nerves=['upper-subscapular','lower-subscapular'])]
NERVES={
 'suprascapular':dict(en='suprascapular nerve',tr='Supraskapular sinir',ta=6411,table='suprascapular'),
 'axillary':dict(en='axillary nerve',tr='Aksiller sinir',ta=6440,table='axillary'),
 'upper-subscapular':dict(en='upper subscapular nerve',tr='Üst subskapular sinir',ta=6428,table='upper subscapular'),
 'lower-subscapular':dict(en='lower subscapular nerve',tr='Alt subskapular sinir',ta=6429,table='lower subscapular')}
BONES={'left':{'scapula':'FMA13396','humerus':'FMA23131'},'right':{'scapula':'FMA13395','humerus':'FMA23130'}}
entities=[];relations=[];labels=[];mappings=[]
LATERALITY='Bilateral instantiation of general university anatomy descriptions; not specimen-validated'

def ev(muscle,column):
 return [{'sourceId':'uams-upper-limb','locator':muscle+' row / '+column},{'sourceId':'ttuhsc-axilla-shoulder-tables','locator':'Muscles / rotator cuff / '+muscle+' row / '+column}]
def term_evidence(ta):
 return {'sourceId':'zanatomy-ta2-terminology','locator':f'TA2 ID {ta}; CSV line {terms[ta]["line"]}; English and Latin columns'}
def label(ids,side,ta,tr,aliases):
 labels.append(dict(ids=ids,side=side,tr=tr,en=terms[ta]['en'],la=terms[ta]['la'],ta2Id=ta,aliases=aliases,evidence=[term_evidence(ta)],translationStatus='editorial_turkish_expert_review_pending'))
def edge(s,p,o,evidence,qualifiers):
 relations.append(dict(id='|'.join([s,p,o]),subject=s,predicate=p,object=o,evidence=evidence,status='source_supported',expertReview='pending',scope='typical_anatomy_non_exhaustive',qualifiers={'laterality':LATERALITY,**qualifiers}))
for side in ['left','right']:
 for key,n in NERVES.items():
  id='atlas:'+side+'-'+key+'-nerve'
  assert id not in nodes
  assert not any(n['en'] in e['name'].lower() for e in graph['entities']), 'Nerve identity now exists; re-review canonical mapping'
  entities.append(dict(id=id,name=side.capitalize()+' '+n['en'],side=side,kind='nerve',geometryPartIds=[],representationStatus='missing_geometry',expertReview='pending',anatomicalCoverage='non_exhaustive',evidence=[{'sourceId':'ttuhsc-axilla-shoulder-tables','locator':'Nerves / '+n['table']+' row / Motor'},term_evidence(n['ta'])],geometryNote='Anatomical concept only. No current main-atlas or registered-extension geometry is mapped.'))
  label([id],side,n['ta'],n['tr'],[n['en']])
 for bone,id in BONES[side].items():
  assert nodes[id]['side']==side and nodes[id]['name']==side+' '+bone
  assert nodes[id]['geometryPartIds']==concepts[id]['elements']
  mappings.append(dict(id=id,role='context_bone_not_localized_landmark',name=nodes[id]['name'],side=side,geometryPartIds=nodes[id]['geometryPartIds'],source='Existing canonical graph and atlas manifest; no entity overwrite proposed'))
for m in MUSCLES:
 for index,side in enumerate(['left','right']):
  id=m['ids'][index];part=m['parts'][index]
  assert nodes[id]['side']==side and m['key'] in nodes[id]['name'].lower()
  assert nodes[id]['geometryPartIds']==concepts[id]['elements']==[part]
  assert part in parts
  mappings.append(dict(id=id,name=nodes[id]['name'],side=side,role='existing_muscle',geometryPartIds=[part],source='Existing canonical graph and atlas manifest; no entity overwrite proposed'))
  label([id,part],side,m['ta'],m['tr'],[m['key']])
  for predicate,column,key,bone in [('originates_at','Origin','origin','scapula'),('inserts_at','Insertion','insertion','humerus')]:
   landmark=m[key];tr=m[key+'Tr']
   edge(id,predicate,BONES[side][bone],ev(m['key'],column),dict(landmark=landmark,landmarkTr=tr,attachmentNoteTr=tr+' — kesin yüzey işareti yok',targetRole='context_bone',semantics='Attachment in the named region of this bone, not the whole bone as a precise attachment point',geometry='No coordinates, anchor, footprint segmentation, or mesh contact asserted',requiresLandmarkDisplay=True))
  for nerve in m['nerves']:
   edge('atlas:'+side+'-'+nerve+'-nerve','innervates',id,ev(m['key'],'Innervation')+[{'sourceId':'ttuhsc-axilla-shoulder-tables','locator':'Nerves / '+NERVES[nerve]['table']+' row / Motor'}],dict(coverage='Selected muscle-level motor supply; no complete territory or muscular branch geometry represented',geometry='Nerve concept has no mapped geometry',displayNoteTr='Sinir geometrisi yok'))
assert len(entities)==8 and len(relations)==26 and len(labels)==16
candidate=dict(schemaVersion=1,scope='Bilateral rotator cuff origin/insertion regions and muscle-level innervation; inactive candidate',entities=entities,relations=relations)
write('candidate.json',candidate)
write('entities.json',{'schemaVersion':1,'entities':entities})
write('relations.json',{'schemaVersion':1,'relations':relations})
write('labels.json',{'schemaVersion':1,'scope':'Selected rotator cuff muscle and nerve labels; candidate only','source':SOURCES[2],'entries':labels})
write('evidence.json',{'schemaVersion':1,'sources':SOURCES,'verifiedOn':'2026-09-22','claims':[{'muscle':m['key'],'originRegion':m['origin'],'insertionRegion':m['insertion'],'innervation':[NERVES[n]['en'] for n in m['nerves']],'evidence':ev(m['key'],'Origin / Insertion / Innervation')} for m in MUSCLES],'excludedClaims':['No capsule insertion, tendon footprint extent, origin/insertion coordinates or root-level motor segment assertions','No invented FMA nerve identifiers or unverified nerve geometry binding','No subscapularis territory segmentation or completeness claims']})
write('mapping.json',{'schemaVersion':1,'inputs':[{'path':p,'sha256':sha(p)} for p in ['public/models/atlas.json','data/anatomy/knowledge.json','public/models/extensions/index.json',TA_PATH]],'existingEntities':mappings,'newEntityCount':len(entities),'geometryMappingMethod':'Exact canonical ID/name/side/element comparison; no proximity inference','nerveGeometryAudit':'No matching named suprascapular, axillary, upper or lower subscapular nerve entity in canonical graph or atlas; no source candidate is promoted to registered geometry.'})
print('Wrote inactive candidate: 8 new geometry-free nerve entities; 26 relations; 16 side-specific labels; 12 canonical endpoint mappings.')
