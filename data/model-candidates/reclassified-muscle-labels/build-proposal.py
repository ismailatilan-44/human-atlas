"""Create label candidates only; no classification or shared label changes."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
BASE=ROOT/'data/model-candidates/system-classification-review'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
proposals=json.loads((BASE/'proposals.json').read_text())
selected=proposals['candidates']+proposals['manualReview']
assert len(selected)==26 and len({r['conceptId'] for r in selected})==26
atlas_path=ROOT/'public/models/atlas.json';atlas=json.loads(atlas_path.read_text())
concepts={r['id']:r for r in atlas['concepts']};parts={r['id']:r for r in atlas['parts']}
label_path=ROOT/'data/anatomy/labels.json';current=json.loads(label_path.read_text())['entries']
ta_path=ROOT/'work/open-assets-review/TA2.csv'
assert digest(ta_path)=='0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974'
terms={}
for i,line in enumerate(ta_path.read_text().splitlines(),1):
 row=line.strip('"').split(';')
 if len(row)>2 and row[0].isdigit(): terms[int(row[0])]={'en':row[1],'la':row[2],'line':i}
# English/Latin are exact pinned TA rows; Turkish is an editorial display translation.
TERMS={
 'fibularis brevis':(2653,'Kısa fibular kas',['fibularis brevis']),
 'fibularis longus':(2652,'Uzun fibular kas',['fibularis longus']),
 'fibularis tertius':(2649,'Üçüncü fibular kas',['fibularis tertius']),
 'tensor fasciae latae':(2602,'Fasya lata gerici kası',['tensor fasciae latae']),
 'tibialis anterior':(2644,'Ön tibial kas',['tibialis anterior']),
 'tibialis posterior':(2666,'Arka tibial kas',['tibialis posterior']),
 'levator scapulae':(2234,'Kürek kemiğini kaldıran kas',['levator scapulae']),
 'inferior pharyngeal constrictor':(2187,'Alt yutak daraltıcı kası',['inferior pharyngeal constrictor']),
 'middle pharyngeal constrictor':(2184,'Orta yutak daraltıcı kası',['middle pharyngeal constrictor']),
 'superior pharyngeal constrictor':(2179,'Üst yutak daraltıcı kası',['superior pharyngeal constrictor']),
 'palatopharyngeus':(2132,'Palatofaringeus kası',['palatopharyngeus','damak-yutak kası']),
 'salpingopharyngeus':(2191,'Salpingofaringeus kası',['salpingopharyngeus','işitme tüpü-yutak kası']),
 'stylopharyngeus':(2190,'Stilofaringeus kası',['stylopharyngeus','stiloid-yutak kası'])}
mapping_path=BASE/'isa_element_parts.txt';map_lines=mapping_path.read_text().splitlines()
assert digest(mapping_path)==proposals['provenance']['sourceMappingSha256']
entries=[];evidence=[];existing=[]
for item in selected:
 concept=item['conceptId'];part=item['id'];source_name=item['name'].lower()
 side,stem=source_name.split(' ',1);assert side in ['left','right']
 assert concepts[concept]['name'].lower()==source_name
 assert concepts[concept]['elements']==[part] and part in parts
 line=item['sourceElementMappingLine'];fields=map_lines[line-1].split('\t')
 assert fields==[concept,source_name,part],(concept,line,fields)
 assert item['officialLeafMeshMappingConfirmed']
 prior=[e for e in current if set([concept,part]).intersection(e['ids'])]
 existing.append(dict(conceptId=concept,partId=part,existingEntries=prior,status='already_labeled_review_merge' if prior else 'no_existing_label'))
 ta,tr,aliases=TERMS[stem];term=terms[ta]
 assert term['en'].lower() in [stem,stem+' muscle'],(stem,term)
 refs=[{'sourceId':'bp3d-isa-element-parts','locator':f'line {line}: {concept} / {source_name} / {part}'},
       {'sourceId':'zanatomy-ta2-terminology','locator':f'TA2 ID {ta}, CSV line {term["line"]}, English/Latin columns'}]
 entries.append(dict(ids=[concept,part],tr=tr,en=term['en'],la=term['la'] or None,ta2Id=ta,aliases=aliases,side=side,evidence=refs,translationStatus='editorial_turkish_expert_review_pending'))
 evidence.append(dict(conceptId=concept,partId=part,side=side,bodyParts3dName=source_name,sourceMappingLine=line,ta2Id=ta,ta2CsvLine=term['line'],ta2English=term['en'],ta2Latin=term['la'],matchMethod='Exact BP3D concept/name/mesh and laterality; side-stripped English matches the TA row with only optional muscle suffix',originalProposalStatus=item['status']))
assert len(entries)==26 and all(e['la'] for e in entries)
assert len({i for e in entries for i in e['ids']})==52
for stem in TERMS:
 assert {x['side'] for x in evidence if x['bodyParts3dName'].split(' ',1)[1]==stem}=={'left','right'}
source_info=[dict(id='bp3d-isa-element-parts',url=proposals['provenance']['sourceMappingUrl'],path=str(mapping_path.relative_to(ROOT)),sha256=digest(mapping_path),role='FMA identity, exact English source name, side and geometry ID'),
 dict(id='zanatomy-ta2-terminology',url='https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv',path=str(ta_path.relative_to(ROOT)),sha256=digest(ta_path),role='English and Latin terms; no Turkish column used'),
 dict(id='human-atlas-local',path=str(atlas_path.relative_to(ROOT)),sha256=digest(atlas_path),role='Current FMA to mesh mapping corroboration'),
 dict(id='current-labels-snapshot',path=str(label_path.relative_to(ROOT)),sha256=digest(label_path),role='Duplicate/conflict check only')]
dump('proposal.json',dict(schemaVersion=1,status='candidate_not_integrated',scope='26 side-specific muscle concepts from 14 clear and 12 pharyngeal source-classification candidates; labels only',source={'id':'zanatomy-ta2-terminology','sha256':digest(ta_path),'expertReview':'pending'},entries=entries))
dump('evidence.json',dict(schemaVersion=1,sources=source_info,mappings=evidence,existingLabelReview=existing,limitations=['Turkish display names are editorial translations, not Turkish content of the pinned TA table.','Latin/English names do not carry synthetic laterality suffixes; the verified side field is separate.','The source TA table sometimes omits Musculus; exact source Latin is retained without grammatical expansion.','No classification override, anatomical relationship, innervation, position or geometry is added.']))
dump('validation.json',dict(status='passed',uniqueFmaConcepts=26,uniqueParts=26,pairedMuscleNames=13,left=13,right=13,exactSourceMappingRows=26,exactEnglishTaMatches=26,latinPresent=26,latinNull=0,existingLabelMatches=sum(bool(x['existingEntries']) for x in existing),sharedFilesWritten=False))
print('26 FMA labels: exact source mappings, 13 left/right pairs, all Latin terms found; existing label matches:',sum(bool(x['existingEntries']) for x in existing))
