"""Build bounded label proposals from the frozen UI audit; never edit active labels."""
from pathlib import Path
import csv,hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((HERE/'ui-label-audit.json').read_text())
ta=ROOT/'work/open-assets-review/TA2.csv'
assert sha(ta)=='0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
terms={}
for number,line in enumerate(ta.read_text().splitlines(),1):
 cols=line.strip().strip('"').split(';')
 if len(cols)>2 and cols[0].isdigit():terms[cols[1]]=dict(upstreamTableId=int(cols[0]),english=cols[1],latin=cols[2],line=number)
official={}
for tree in ['isa','partof']:
 path=HERE/f'bp3d-{tree}-parts-list-e.txt'
 for number,row in enumerate(csv.DictReader(path.open(),delimiter='\t'),2):official.setdefault(row['concept id'],[]).append(dict(file=path.name,line=number,representationId=row['representation id'],english=row['en']))
# Values: exact upstream TA English key, editorial Turkish, optional explicit side marker.
spec={
 'FMA46565':('Cranium','Kafatası',None),
 'FMA52748':('Mandible','Mandibula',None),
 'FMA50801':('Brain','Beyin',None),
 'FMA62493':('Hippocampus','Hipokampus',None),
 'FMA9915':('Cervical vertebrae','Servikal omurlar',None),
 'FMA55108':('Laryngeal cartilages','Larinks kıkırdakları',None),
 'FMA78454':('Third ventricle','Üçüncü ventrikül',None),
 'FMA78469':('Fourth ventricle','Dördüncü ventrikül',None),
 'FMA75351':('Interventricular foramen','İnterventriküler foramen',None),
 'FMA78450':('Lateral ventricle','Yan ventrikül','left'),
 'FMA78449':('Lateral ventricle','Yan ventrikül','right'),
 'FMA7088':('Heart','Kalp',None),
 'FMA7310':('Left lung','Sol akciğer',None),
 'FMA7309':('Right lung','Sağ akciğer',None),
 'FMA7394':('Trachea','Trakea',None),
 'FMA13295':('Diaphragm','Diyafram',None),
 'FMA7574':('Ribs','Kaburgalar',None),
 'FMA7485':('Sternum','Sternum',None),
 'FMA3734':('Aorta','Aort',None),
 'FMA7131':('Oesophagus','Özofagus',None),
 'FMA7197':('Liver','Karaciğer',None),
 'FMA7148':('Stomach','Mide',None),
 'FMA7198':('Pancreas','Pankreas',None),
 'FMA7196':('Spleen','Dalak',None),
 'FMA7203':('Kidney','Böbrek',None),
 'FMA7202':('Gallbladder','Safra kesesi',None),
 'FMA7200':('Small intestine','İnce bağırsak',None),
 'FMA7201':('Large intestine','Kalın bağırsak',None),
 'FMA14544':('Rectum','Rektum',None),
 'FMA15900':('Urinary bladder','Mesane',None),
 'FMA9600':('Prostate','Prostat',None),
 'FMA16585':('Hip bone','Kalça kemiği',None),
 'FMA16202':('Sacrum','Sakrum',None),
 'FMA13321':('Clavicle','Klavikula',None),
 'FMA23466':('Ulna','Ulna',None),
 'FMA23889':('Carpal bones','Karpal kemikler',None),
 'FMA9611':('Femur','Femur',None),
 'FMA24476':('Tibia','Tibia',None),
 'FMA24479':('Fibula','Fibula',None),
 'FMA24485':('Patella','Patella',None),
 'FMA22314':('Gluteus maximus muscle','Gluteus maximus kası',None),
 'FMA70248':('Femoral artery','Femoral arter',None),
 'FMA24491':('Tarsal bones','Tarsal kemikler',None),
}
plural={'FMA9915','FMA55108','FMA7574','FMA23889','FMA24491'}
zone={'FMA34676':('Deltoid kasının gösterilen bölümleri','Musculus deltoideus'),'FMA22429':('Quadriceps femoris kasının gösterilen bölümleri','Musculus quadriceps femoris')}
manifest=json.loads((ROOT/'public/models/atlas.json').read_text());parts={p['id']:p for p in manifest['parts']};entries=[];selected=[];withheld=[]
for item in audit['entries']:
 cid=item['id']
 if not item['fallback']['tr']:
  if item['fallback']['la']:withheld.append(dict(id=cid,datasetId=item['datasetId'],current=item['current'],language='la',reason='Project-defined unanchored humeral attachment region; no independently matched TA term. Keep documented English fallback; do not imply an identified landmark or invent Latin.'))
  continue
 assert cid in official and any(x['english']==item['name'] for x in official[cid]),cid
 evidence=[dict(sourceId='bp3d-official-names',locator=x) for x in official[cid]]
 geometry=[dict(id=p,name=parts[p]['name']) for p in item['geometryPartIds']]
 common=dict(ids=[cid],datasetId=item['datasetId'],targetId=item['targetId'],sourceEnglish=item['name'],geometryPartIds=item['geometryPartIds'],sourceGeometryNames=geometry,aliases=[item['name']],expertReview='pending',trStatus='editorial_translation_not_official_Turkish_standard')
 if cid in zone:
  tr,rejected=zone[cid];entry=dict(**common,tr=tr,en=item['name'][0].upper()+item['name'][1:],la=None,side=None,proposalStatus='source_scoped_TR_EN_only',evidence=evidence,scopeNote='Retain source zone/group identity and its selected component surfaces; do not rename this concept as the whole muscle.',rejectedLatinAlternative=rejected,latinWithheldReason='TA muscle term exists but is not an exact label for the BP3D zone concept. No matched official Latin zone label was found.')
 else:
  key,tr,side=spec[cid];term=terms[key];selected.append(term);evidence.append(dict(sourceId='zanatomy-ta2-pinned',locator=dict(upstreamTableId=term['upstreamTableId'],line=term['line'],english=term['english'],latin=term['latin'])))
  scope='Canonical term labels the existing source concept only; no change to geometry, relationships, target state or completeness.'
  if cid in plural:scope='Plural display names the existing multi-part class/group selection. Original singular BP3D concept ID/name is preserved; this is not proof that every anatomical member exists.'
  if cid=='FMA46565':evidence.append(dict(sourceId='ifaa-tah-cranium',locator='FMA 46565 / TAH 305: cranium; skull → cranium'))
  entry=dict(**common,tr=tr,en=term['english'],la=term['latin'],side=side,ta2TableId=term['upstreamTableId'],proposalStatus='source_matched_candidate',scopeNote=scope,evidence=evidence)
 entries.append(entry)
assert len(entries)==45 and len(withheld)==2
result=dict(schemaVersion=1,status='proposal_only_not_applied',scope='65 target rows, 83 directly bound dataset/concept pairs only; no descendant or full-atlas expansion',currentFallbackCounts=audit['counts'],proposalCounts=dict(trEnAdditions=45,latinAdditions=43,latinWithheldSourceZoneGroups=2,latinAlreadyWithheldProjectRegions=2),entries=entries,retainExistingBoundIds=[dict(datasetId=e['datasetId'],id=e['id']) for e in audit['entries'] if not any(e['fallback'].values())],keepFallback=withheld,sourceCautions=['Official BP3D name snapshots were retrieved and every proposed FMA ID/name matched.','Latin spellings are exact pairs from the pinned Z-Anatomy-distributed TA2 table; this is not a fresh full FIPAT publisher-PDF verification.','FIPAT publisher requests returned DNS/502 failures. IFAA TAH FMA46565/cranium was independently accessible and checked.','Upstream CSV IDs are local table identifiers here; do not silently equate them with row numbers in other TA2 editions or publisher PDFs.','Turkish translations are editorial; clinical/anatomist terminology review pending.'])
(HERE/'proposals.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(HERE/'ta2-selected-rows.json').write_text(json.dumps({str(x['upstreamTableId']):x for x in selected},ensure_ascii=False,indent=2)+'\n')
files=['data/anatomy/coverage.json','public/models/atlas.json','data/anatomy/labels.json','data/anatomy/brachial-plexus.json','app/atlas-metadata.ts','app/reference-datasets.ts','app/female-pelvis-labels.ts','public/models/female-pelvis/atlas.json','public/models/inner-ear-reference/atlas.json']
sources=dict(retrievedOn='2026-09-22',inputHashes={p:sha(ROOT/p) for p in files},sources=[dict(id='bp3d-official-names',publisher='Database Center for Life Science / NBDC LSDB Archive',files=[dict(path=f'bp3d-{t}-parts-list-e.txt',url=f'https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/{t}_parts_list_e.txt',sha256=sha(HERE/f'bp3d-{t}-parts-list-e.txt')) for t in ['isa','partof']],use='Original FMA concept ID / representation ID / English source-name comparison'),dict(id='zanatomy-ta2-pinned',url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv',sha256=sha(ta),selectedRows='ta2-selected-rows.json',use='Exact English/Latin term pairs from upstream distributed table; not independent revalidation of the entire TA publication'),dict(id='ifaa-tah-cranium',url='https://ifaa.unifr.ch/Public/TNAEntryPage/auto/part/EN/TAH305%20P2F%20EN.htm',retrievedOn='2026-09-22',verifiedFields=dict(fmaId='FMA46565',tahUid=305,english=['cranium','skull'],latin='cranium'),status='IFAA-hosted TAH work-in-progress page; narrow synonym corroboration'),dict(id='fipat-live-access-attempt',url='https://fipat.library.dal.ca/ta2/',status='502/unavailable; publisher PDF requests also failed; not counted as independently verified text')])
(HERE/'source-evidence.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print(result['proposalCounts'])
