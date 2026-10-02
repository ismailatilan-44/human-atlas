"""One-time, explicit capture of bounded planning inputs. Does not run from build.py."""
import datetime, hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
if '--capture' not in sys.argv:
 raise SystemExit('Explicit --capture required; normal reproduction uses build.py --check')
if (OUT/'frozen-inputs.json').exists() and '--replace-snapshot' not in sys.argv:
 raise SystemExit('Snapshot exists; replacement requires --replace-snapshot after source review')

def read(path): return json.loads((ROOT/path).read_text())
def sha(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def slug(text): return re.sub('[^a-z0-9]+','-',text.lower()).strip('-')
FAMILIES={
'skeletal-support':[1210,1230,1225,1226,1247,1250,1251,1252,1253,1254,1255,1256,1257,1258,1259,1260,1269,1281,1761,1781,1782,1784,1785,1786,1787,1788,1789,1791,1792,1798,1800,1801,1804,1807,1809,1819,1823,1824,1825,1826,1830,1838,1842,2545,2546,2550],
'muscle-tendon-fascia':[2478,2479,2480,2481,2482,2483,2484,2485,2486,2487,2488,2489,2491,2492,2493,2496,2497,2498,2499,2500,2502,2503,2504,2505,2506,2507,2508,2509,2510,2512,2513,2514,2515,2516,2517,2518,2520,2521,2522,2523,2524,2525,2526,2527,2528,2529,2530,2531,2532,2533,2534,2544,2547,2549,2553,2573,2574,2575,2577,2578,2579,2580,2581,2582],
'neurovascular-lymph':[6423,6431,6434,6435,6436,6437,6438,6439,6446,6447,6448,6449,6450,6451,6452,6453,6454,6455,6456,6457,6459,6460,6461,6462,6464,6465,6466,4641,4642,4644,4645,4646,4647,4648,4649,4650,4651,4652,4653,4655,4657,4658,4661,4662,4665,4666,4668,4669,4670,4671,4672,4673,4964,4967,4968,4969,4970,4979,4980,4981,4983,4984,4985,4986,4987,4988,4989,4990,5245,5246],
'organs-cavities-internal':[2476,2477,2490,2494,2495,2511,2551,2552]}
terms={}
for lineno,line in enumerate((ROOT/'work/open-assets-review/TA2.csv').read_text().splitlines(),1):
 c=line.strip('"').split(';')
 if len(c)>2: terms[c[0]]={'sourceId':'zanatomy-ta2-pinned','tableId':c[0],'numericId':int(c[0]) if c[0].isdigit() else None,'en':c[1],'rawLatin':c[2],'csvLine':lineno,'rawRow':line,'scope':'Exact unsided source row; no formal FMA crosswalk or sided Latin assertion'}
seeds=[]
GROUP_IDS={1281,2505,2532,2533,2534,6435,6439,6450,6452,6455,6456,6461,6465,6466,4648,4649,4653,4672,4673,4968,4969,4970,4983,4984,4985,4987,4988,4990,5245,5246}
D1_BONES={1210,1230,1250,1252,1253,1254,1255,1257,1258,1259,1269}
D1_MUSCLES={2478,2481,2482,2483,2486,2491,2492,2493,2496,2497,2499,2500,2506,2507,2510,2512,2515,2516,2517,2518,2520,2521,2522,2525,2526,2529,2530,2531}
for family,ids in FAMILIES.items():
 for i in ids:
  term=terms[str(i)].copy(); term['la']=term['rawLatin'] if i not in [2486,4644,4646] else None
  term['displayStatus']='candidate_exact_unsided_numeric_row;not_independently_verified' if i not in [2486,4644,4646] else 'withheld_possible_duplicate_word_or_incomplete_pinned_latin;primary_verification_pending'
  kind='named_group' if i in GROUP_IDS else 'named_part_or_head' if 'head of' in term['en'].lower() or 'part of' in term['en'].lower() else 'named_structure'
  seeds.append(dict(key='ta2-'+str(i),name=term['en'],familyId=family,targetKind=kind,requiredDetail='D1' if i in D1_BONES|D1_MUSCLES or (family=='neurovascular-lymph' and kind=='named_structure' and not any(w in term['en'].lower() for w in ['branch','recurrent','digital','carpal'])) else 'D2',termEvidence=term))
# Preserve nonnumeric Z-Anatomy source identifiers; these are not numeric TA2 IDs.
for key in ['1265*1','1265*2','1265*4','1265*5']+[f'{n}*{d}' for n in [1277,1278,1279] for d in range(1 if n!=1278 else 2,6)]:
 term=terms[key].copy();term.update(la=None,displayStatus='withheld_non_numeric_source_extension;exact_form_requires_primary_verification')
 seeds.append(dict(key='za-term-'+key.replace('*','-'),name=term['en'],familyId='skeletal-support',targetKind='individual_digit_bone',requiredDetail='D1',termEvidence=term))
# Custom subdivisions keep generic numeric evidence separate from the exact requirement.
def custom(key,name,family,generic=None,source=None,locator=None,note=None):
 e=dict(sourceId=source or 'zanatomy-ta2-pinned',exactNumericTerm=None,la=None,unresolvedReason=note or 'Project individualization of a sourced generic class; exact individual numeric/Latin term pending')
 if generic:e['genericTerm']=terms[str(generic)]
 if locator:e['locator']=locator
 seeds.append(dict(key=key,name=name,familyId=family,targetKind='individual_subdivision_requirement',requiredDetail='D2',termEvidence=e))
for d,n in enumerate(['thumb','index finger','middle finger','ring finger','little finger'],1):
 custom(f'mcp-{d}',f'Metacarpophalangeal joint of {n}','skeletal-support',1835)
 if d>1:
  custom(f'pip-{d}',f'Proximal interphalangeal joint of {n}','skeletal-support',1840)
  custom(f'dip-{d}',f'Distal interphalangeal joint of {n}','skeletal-support',1841)
  custom(f'cmc-{d}',f'Carpometacarpal joint of {n}','skeletal-support',1827)
  custom(f'fds-tendon-{d}',f'Flexor digitorum superficialis tendon to {n}','muscle-tendon-fascia',2486)
  custom(f'fdp-tendon-{d}',f'Flexor digitorum profundus tendon to {n}','muscle-tendon-fascia',2491)
 custom(f'fibrous-digital-sheath-{d}',f'Fibrous flexor sheath of {n}','muscle-tendon-fascia',2584)
for i in range(1,5):
 custom(f'lumbrical-{i}',f'{["First","Second","Third","Fourth"][i-1]} lumbrical muscle of hand','muscle-tendon-fascia',2532,'ttuhsc-hand','Muscles of the Hand / lumbrical (hand)', 'Four digit-associated individual requirements; exact ordinal crosswalk/Latin pending; no group binding allowed')
 custom(f'dorsal-interosseous-{i}',f'{["First","Second","Third","Fourth"][i-1]} dorsal interosseous muscle of hand','muscle-tendon-fascia',2533,'ttuhsc-hand','Muscles of the Hand / interosseous, dorsal (hand)','Four individual requirements; exact ordinal crosswalk/Latin pending; no group binding allowed')
for digit in ['index finger','ring finger','little finger']:
 custom('palmar-interosseous-'+slug(digit),'Palmar interosseous muscle for '+digit,'muscle-tendon-fascia',2534,'ttuhsc-hand','Muscles of the Hand / interosseous, palmar','Digit-scoped requirement avoids competing 3-versus-4/ordinal conventions; pollical variation remains unexpanded')
for name in ['Thenar compartment','Hypothenar compartment','Central compartment of hand','Adductor-interosseous compartment of hand']:
 custom(slug(name),name,'organs-cavities-internal',source='ttuhsc-hand',locator='Joints and Associated Structures of the Hand / '+name.split(' of ')[0].lower(),note='Source-defined space; boundaries/contents and exact numeric Latin term pending; no synthetic cavity mesh')
# Exact spelling/scope-preserving query variants. No automatic plural-to-singular mapping.
ALIASES={1253:['Triquetral bone','Triquetral'],2529:['Abductor digiti minimi of hand'],2530:['Flexor digiti minimi brevis of hand'],2531:['Opponens digiti minimi of hand'],2532:['Set of lumbricals of hand'],2533:['Set of dorsal interossei of hand'],2534:['Set of palmar interossei of hand']}
def queries(s,side):
 term=s['termEvidence'];n=s['name']; options=[n]+ALIASES.get(term.get('numericId'),[])
 if ' muscle' in n:options.append(n.replace(' muscle',''))
 if term.get('numericId') in [1250,1252,1254,1255,1257,1258,1259]:options.append(n.replace(' bone',''))
 # A digit noun substitution preserves source term's digit specificity.
 for ordinal,digit in [('first','thumb'),('second','index finger'),('third','middle finger'),('fourth','ring finger'),('fifth','little finger')]:
  phrase=ordinal+' finger of hand'
  if phrase in n:options.append(n.replace(phrase,digit))
 qs=[]
 for name in options:
  name=name.lower();qs.append(side+' '+name)
  if ' of ' in name:
   a,b=name.rsplit(' of ',1);qs.append(a+' of '+side+' '+b)
 return sorted(set(qs))
paths=['public/models/atlas.json']+['public'+p for p in read('public/models/extensions/index.json')['manifests']]+['public/models/upper-limb-nerve-reference/atlas.json']
graph=read('data/anatomy/knowledge.json')
source_tables=['data/model-candidates/coverage-labels/bp3d-isa-parts-list-e.txt','data/model-candidates/concept-selection-review/isa_element_parts.txt','data/model-candidates/concept-selection-review/partof_parts_list_e.txt','data/model-candidates/concept-selection-review/partof_element_parts.txt']
name_rows={}; member_rows={}
for path in source_tables:
 for i,line in enumerate((ROOT/path).read_text().splitlines(),1):
  cells=line.split('\t')
  if len(cells)!=3:continue
  rec=dict(path=path,line=i,rawRow=line,cells=cells)
  (member_rows if 'element' in path else name_rows).setdefault(cells[0],[]).append(rec)
observations=[];related_parts=[];datasets=[]
allqueries={q for s in seeds for side in ['left','right'] for q in queries(s,side)}
for path in paths:
 m=read(path);dataset=m.get('datasetId','male-body')
 if path!='public/models/upper-limb-nerve-reference/atlas.json':dataset='male-body'
 parts={p['id']:p for p in m['parts']}
 selected=[c for c in m['concepts'] if c['name'].lower() in allqueries]
 # Related whole-muscle heads are retained without promoting them to whole-target bindings.
 for seed in seeds:
  if seed['familyId']!='muscle-tendon-fascia' or seed['targetKind']!='named_structure':continue
  for side in ['left','right']:
   suffix=' of '+side+' '+seed['name'].lower().replace(' muscle','')
   for c in m['concepts']:
    if c['name'].lower().endswith(suffix):
     related_parts.append(dict(seedKey=seed['key'],side=side,datasetId=dataset,conceptId=c['id'],sourceName=c['name'],sourceManifest=path,partIds=c['elements'],officialNameRows=name_rows.get(c['id'],[]),officialMembershipRows=member_rows.get(c['id'],[]),status='related named source part only; not a whole-structure binding'))
 if not selected:continue
 datasets.append(dict(datasetId=dataset,manifest=path,version=m.get('version'),source=m.get('source'),coordinateSystem=m.get('coordinateSystem'),registration=m.get('registration'),compatibleWithMainAtlas=m.get('compatibleWithMainAtlas'),scope=m.get('scope'),sourceManifestSha256=sha(path)))
 for c in selected:
  ps=[]
  for pid in c['elements']:
   p=parts[pid]; ps.append({k:p[k] for k in ['id','conceptId','name','side','system','vertexCount','indexCount','bounds','sourceObject','sourceObjectType','sourceScope','componentRole','expertReview'] if k in p})
  observations.append(dict(datasetId=dataset,conceptId=c['id'],sourceName=c['name'],sourceManifest=path,sourceConcept=c,partIds=c['elements'],observedParts=ps,officialNameRows=name_rows.get(c['id'],[]) if dataset=='male-body' else [],officialMembershipRows=member_rows.get(c['id'],[]) if dataset=='male-body' else [],status='manifest_membership_observed',detailAcceptance='pending; nonzero manifest geometry is not anatomical detail or completeness acceptance'))
ids={o['conceptId'] for o in observations}
sourcepaths=paths+source_tables+['work/open-assets-review/TA2.csv','data/anatomy/knowledge.json','data/anatomy/model-inventory.json','docs/model/model-scope-and-acceptance.md','data/model-candidates/upper-limb-nerve-metadata-v1/source-evidence.json','public/models/upper-limb-nerve-reference/ATTRIBUTION.md','public/ATTRIBUTION.md']
reference_metadata=read('data/model-candidates/upper-limb-nerve-metadata-v1/source-evidence.json')
frozen=dict(schemaVersion=1,capturedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),sourceRevision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),captureNote='Historical planning snapshot; only this directory written. Other writers and release work may be active. Original September handoff is historical, not this revision or deployment acceptance.',sourceSnapshots=[dict(path=p,sha256=sha(p)) for p in dict.fromkeys(sourcepaths)],scopeContract=next(r for r in read('data/anatomy/model-inventory.json')['regions'] if r['id']=='forearm-wrist-hand'),scopeRow=next(l for l in (ROOT/'docs/model/model-scope-and-acceptance.md').read_text().splitlines() if l.startswith('| Önkol,')),seeds=seeds,observations=observations,relatedPartObservations=related_parts,datasets=datasets,graphEntities=[e for e in graph['entities'] if e['id'] in ids],graphRelations=[r for r in graph['relations'] if r['subject'] in ids or r['object'] in ids],referenceTermEvidence=[e for e in reference_metadata['entries'] if e['conceptId'] in ids],attribution={'male-body':(ROOT/'public/ATTRIBUTION.md').read_text(),'upper-limb-nerve-reference':(ROOT/'public/models/upper-limb-nerve-reference/ATTRIBUTION.md').read_text()},sourceEvidence=dict(ttuhscHand=dict(url='https://anatomy.ttuhscep.edu/musculoskeletal_system/hand_tables.html',retrievedOn='2026-10-02',observations=['Thenar, hypothenar, central and adductor-interosseous compartments are individually listed.','Dorsal interosseous row describes four muscles; palmar row allows three or four.','Lumbrical row associates muscles with digits 2–5.'],use='Bounded requirement naming only; no imported relationships or asserted exact ordinal mapping')))
# Freeze the queries so the reproduction path needs no mutable source lookup logic.
for s in frozen['seeds']:s['sourceNameQueries']={side:queries(s,side) for side in ['left','right']}
(OUT/'frozen-inputs.json').write_text(json.dumps(frozen,ensure_ascii=False,indent=2)+'\n')
print('Frozen',len(seeds),'unsided requirements and',len(observations),'manifest observations')
if __name__=='__main__':pass
