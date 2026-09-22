"""Build editorial TR/EN candidates only in this folder; preserve source identities."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[2]
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda n,x:(H/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
prev=R/'data/model-candidates/organ-neighbor-labels'
p=read(prev/'proposals.json');ev=read(prev/'source-evidence.json');by={e['id']:e for e in ev['entries']}
labels=read(R/'data/anatomy/labels.json');existing={i:e for e in labels['entries'] for i in e['ids']}
spec={
'FMA9465':('Sol atriyum boşluğu',False,'Tek yüzey sol atriyumun boşluğunu temsil eder; atriyum duvarı veya tüm atriyum değildir.',['sol kulakçık boşluğu']),
'FMA9466':('Sol ventrikül boşluğu',False,'Tek yüzey sol ventrikülün boşluğunu temsil eder; ventrikül duvarı veya tüm ventrikül değildir.',['sol karıncık boşluğu']),
'FMA79278':('Orta mediastinum içeriği',True,'85 kaynak yüzeyini bir araya getirir; orta mediastinumun ayrı sınır yüzeyi veya eksiksiz içeriği olarak doğrulanmadı.',[]),
'FMA9496':('Kalbin fibröz iskeleti',True,'Bu kaynak grubu yalnız üç kapakçık yüzeyini seçer: mitral kapağın ön yaprakçığı ve aort kapağının sol/sağ posterior küspisleri. Tam fibröz iskelet geometrisi değildir.',['fibröz kalp iskeleti']),
'FMA7166':('Kalbin sol tarafı',True,'36 yüzeylik kaynak seçimi boşluk, duvar, kapakçık, papiller kas ve damar parçalarını birleştirir; tek bir bütün organ yüzeyi değildir.',['sol kalp']),
'FMA68005':('Sol alt pulmoner venin akciğer içi bölümü',False,'12 kaynak damar yüzeyi; venin akciğer dışı bölümü bu seçimde değildir.',[]),
'FMA67995':('Sol pulmoner arterin akciğer içi bölümü',False,'37 kaynak damar yüzeyi; pulmoner arterin bütünü olarak adlandırılmamalıdır.',[]),
'FMA68004':('Sol üst pulmoner venin akciğer içi bölümü',False,'24 kaynak damar yüzeyi; venin akciğer dışı bölümü bu seçimde değildir.',[]),
'FMA85056':('Sol akciğer-plevra kompartımanı',True,'124 kaynak yüzeyi birlikte seçilir; bağımsız plevral boşluk veya tam plevra zarı geometrisi olarak doğrulanmadı.',['sol pulmoplevral kompartıman']),
'FMA68003':('Sağ alt pulmoner venin akciğer içi bölümü',False,'23 kaynak damar yüzeyi; venin akciğer dışı bölümü bu seçimde değildir.',[]),
'FMA67994':('Sağ pulmoner arterin akciğer içi bölümü',False,'54 kaynak damar yüzeyi; pulmoner arterin bütünü olarak adlandırılmamalıdır.',[]),
'FMA68002':('Sağ üst pulmoner venin akciğer içi bölümü',False,'26 kaynak damar yüzeyi; venin akciğer dışı bölümü bu seçimde değildir.',[]),
'FMA45662':('Alt solunum yolları',True,'283 kaynak yüzeyi bronş ve damar alt yapılarını da birlikte seçer; yalnız hava yolu lümeni veya eksiksiz solunum sistemi değildir.',[]),
'FMA24866':('Göğsün sternal bölümü',True,'Bu kaynak seçimi yalnız manubrium, sternum gövdesi ve ksifoid çıkıntıdan oluşur; bölgenin tüm yumuşak dokuları değildir.',[]),
'FMA49894':('Sistemik arter ağacı',True,'324 kaynak arter yüzeyidir; bütün sistemik dalların eksiksiz temsil edildiği iddia edilmez.',['sistemik atardamar ağacı']),
'FMA71132':('Gastrointestinal kanal',True,'136 yüzeylik kaynak grubu özofagus ve bağırsakların yanında karaciğer, pankreas ve ilişkili damar/safra yapılarını da kapsar; yalnız sindirim kanalı lümeni veya duvarı değildir.',['mide bağırsak kanalı']),
'FMA68016':('Karaciğer içi safra ağacı',False,'14 kaynak safra yolu yüzeyini kapsar; karaciğerin tamamı veya tüm mikroskobik safra yolları değildir.',['intrahepatik safra ağacı']),
'FMA63103':('Pankreas kanal ağacı',False,'İki kaynak yüzeyden oluşur: pancreatic duct ve pancreatic duct tree. Pankreas dokusunun tamamı değildir.',[]),
'FMA63120':('Pankreas parankimi',False,'Kaynakta parenchyma of pancreas olarak adlandırılmış tek yüzey; kanal ağacı ayrı kavramdır.',[]),
'FMA14615':('İnce bağırsak duvarı',True,'Bu kaynak grubu yalnız ileoçekal birleşim yüzeyini seçer. İnce bağırsak duvarının bütünü değildir.',[]),
'FMA14619':('Kalın bağırsak duvarı',True,'Bu kaynak grubu yalnız taenia libera, taenia mesocolica ve taenia omentalis yüzeylerini seçer. Kalın bağırsak duvarının bütünü değildir.',[]),
'FMA45659':('Alt idrar yolları',True,'Bu seçim yalnız mesane ve üretra yüzeylerini içerir. Diğer komşu yapılar dahil edilmez.',[]),
'FMA7160':('Genital sistem',True,'Bu kaynak grubu yalnız prostat yüzeyini seçer. Erkek veya kadın genital sisteminin bütünü değildir.',['üreme sistemi kaynak grubu']),
}
entries=[];evidence=[];retained=[]
for w in p['withheld']:
 id=w['id'];tr,group,note,aliases=spec[id];source=w['sourceEnglish'];original=by[id]
 e=dict(ids=[id],datasetId='male-body',sourceEnglish=source,geometryPartIds=w['geometryPartIds'],tr=tr+(' (kaynak grubu)' if group else ''),en=source[0].upper()+source[1:]+(' (source group)' if group else ''),la=None,side=None,aliases=aliases,expertReview='pending',trStatus='editorial',sourceGroupLabel=group,requiresSourceGroupLabelAllLanguages=group,requiresRepresentationNote=True,scopeNoteTr=note,evidenceRef=f'source-evidence.json#{id}',latinStatus='withheld_no_exact_full_scope_term')
 if id in existing and existing[id].get('tr') and existing[id].get('en'):retained.append(dict(id=id,existing=existing[id]))
 else:entries.append(e)
 evidence.append(dict(id=id,sourceEnglish=source,bp3d=original['bp3d'],geometry=original['geometry'],via=original['via'],editorialScopeNote=note))
# Record verified terminology separately from a safe source-group display label.
verified=[dict(id='FMA9496',latin='Skeleton fibrosum cordis',source='FIPAT-TA2-Part-4.pdf',officialTermId=3974,pdfPage=6,printedPage=180,url='https://cdn.dal.ca/content/dam/dalhousie/pdf/library/FIPAT/TA2/FIPAT-TA2-Part-4.pdf',status='official_TA2_2.07_term_verified',reasonNotApplied='Source group contains only three valve surfaces; the qualified source-group display label has no verified complete Latin phrase. Retain exact term here, not the typo flbrosum.'),dict(id='FMA71132',latin='tractus gastrointestinalis',url='https://ifaa.unifr.ch/Public/TNAEntryPage/auto/unit/FR/TAH18883%20Unit%20FR.htm',tahUnit='TAH:U18883',status='IFAA_hosted_TAH_work_in_progress',reasonNotApplied='Work-in-progress source and broad BP3D group geometry require qualified source-group display. Do not invent its Latin qualification.')]
write('proposals.json',dict(schemaVersion=1,status='proposal_only_not_applied',scope='Exactly the 23 previously withheld one-step organ neighbors',entries=entries,retainExisting=retained,verifiedSourceLatinTerms=verified,latinDisplayPolicy='All proposed la values remain null. Two independently verified source terms are retained as evidence, not falsely presented as complete Latin translations of qualified source-group labels.'))
inputs=[prev/'proposals.json',prev/'source-evidence.json',R/'data/anatomy/labels.json',R/'public/models/atlas.json']
write('source-evidence.json',dict(schemaVersion=1,inputSnapshots=[dict(path=str(x.relative_to(R)),sha256=sha(x)) for x in inputs],inheritedBp3dSources=ev['sources'][:2],entries=evidence,primaryTerminology=verified,pdf=dict(file='FIPAT-TA2-Part-4.pdf',sha256=sha(H/'FIPAT-TA2-Part-4.pdf'),license='CC BY-ND 4.0 for unaltered publication; individual terms public domain',retrievedAt='2026-09-22'),boundedSearch=dict(scopeIds=list(spec),queries=['site.ifaa.unifr.ch "Cavity of left atrium"','site.fipat.library.dal.ca "Fibrous skeleton" "Skeleton"','site.ifaa.unifr.ch "gastrointestinal tract"'],pdfChecks=['Cavitas atrii: no match','Cavitas ventriculi: no match','Skeleton fibrosum: matched official term3974'],limitation='No claim of exhaustive absence from all terminology sources. No scope expansion outside these 23 IDs.')))
assert len(entries)+len(retained)==23
assert all(e['la'] is None and e['tr'] and e['en'] for e in entries)
assert {e['ids'][0] for e in entries}|{e['id'] for e in retained}==set(spec)
write('validation.json',dict(scopedIds=23,newBilingualRecords=len(entries),retainedExisting=len(retained),nullLatinCount=len(entries),sourceGroupLabels=sum(e['sourceGroupLabel'] for e in entries),representationNotes=len(entries),verifiedSourceLatinTerms=2,sharedFilesWritten=False))
print('Validated',len(entries),'TR/EN proposals; Latin null; source-group labels',sum(e['sourceGroupLabel'] for e in entries))
