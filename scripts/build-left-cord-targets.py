"""Add two bounded left source observations; preserve all previous requirements."""
import copy,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads((ROOT/p).read_text())
base=read('data/anatomy/regional-targets-upper-limb-v2.json');result=copy.deepcopy(base)
path='public/models/extensions/left-cords-bp3d43.json';manifest=read(path)
concepts={c['id']:c for c in manifest['concepts']};parts={p['id']:p for p in manifest['parts']}
count=0
for t in result['targets']:
    if t['side']!='left' or t['termEvidence'].get('numericId') not in [6415,6417]:continue
    cid='FMA45239' if t['termEvidence']['numericId']==6415 else 'FMA45241'
    c=concepts[cid]
    t['representations'].append(dict(datasetId='male-body',conceptId=cid,sourceName=c['name'],sourceManifest=path,
        runtimeManifest=path,runtimeManifestSha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),partIds=c['elements'],
        observedParts=[parts[p] for p in c['elements']],sourceConcept=c,status='source_membership_observed',
        activeProductBinding=True,selectionScope='short_source_cord_segment;not_complete_course',
        runtimeAcceptance='local_implementation;see_left_cords_local_acceptance;not_deployed',
        detailAcceptance='pending;not_expert_accepted'))
    t['bindingStatus']='observed_manifest_or_anchor';count+=1
assert count==2
result['previousSummary']=copy.deepcopy(base['summary'])
result['activationInputSnapshots']=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in ['data/anatomy/regional-targets-upper-limb-v2.json',path,'scripts/build-left-cord-targets.py']]
result['productAcceptance']='Local implementation: docs/model/left-cords-local-acceptance.md; live and anatomical expert acceptance pending'
result['previousScopeVersion']=base['scopeVersion'];result['scopeVersion']='upper-limb-targets-v3-left-cords'
result['summary']['observedMeshTargets']=180
result['summary']['bindingStatusCounts']['no_positive_binding_in_bounded_active_source_audit;not_absence']-=2
result['summary']['bindingStatusCounts']['observed_manifest_or_anchor']+=2
result['summary']['addedLeftCordBindings']=2
result['summary']['mainBodyGeometryChanges']=2
result['summary']['newGeometry']=2
result['summary']['newLabels']=2
result['summary']['newRelationships']=3
result['summary']['targetsUnchanged']=350
result['status']='local_source_bindings;expert_review_pending;not_deployed'
assert all(not t['complete'] and not t['anatomicallyAccepted'] for t in result['targets'])
p=ROOT/'data/anatomy/regional-targets-upper-limb-v3.json';out=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if '--check' in sys.argv:assert p.read_text()==out
else:p.write_text(out)
print('352 requirements retained; two left cord bindings added; 180 mesh observations; zero expert acceptance')
