import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createExplosionLayout} from '../app/explosion-layout.ts';
import {PointerTap} from '../app/pointer-tap.ts';
import {inspectionDistance} from '../app/inspection-camera.ts';
import {Box3, Vector3, PerspectiveCamera} from 'three';
import {createServer} from 'vite';
// Use the app's bundler for its TypeScript and JSON dependency imports.
const loader = await createServer({configFile:false, optimizeDeps:{noDiscovery:true}, server:{middlewareMode:true}, appType:'custom'});
let atlasTools, mergeAtlas, loadAtlas, explorerConcepts, prepareAtlas, anatomyLabel, relationshipsFor, datasetLabel, referenceDescription;
try {
  ({atlasTools} = await loader.ssrLoadModule('/app/agent-tools.ts'));
  ({mergeAtlas, loadAtlas} = await loader.ssrLoadModule('/app/load-atlas.ts'));
  ({explorerConcepts, relationshipsFor} = await loader.ssrLoadModule('/app/knowledge.ts'));
  ({datasetLabel, referenceDescription} = await loader.ssrLoadModule('/app/reference-datasets.ts'));
  ({prepareAtlas, anatomyLabel} = await loader.ssrLoadModule('/app/atlas-metadata.ts'));
}
finally { await loader.close(); }

for (const file of ['atlas.json']) {
  let atlas=JSON.parse(await readFile(new URL(`../public/models/${file}`,import.meta.url)));
  const baseSource = atlas;
  const untouched = structuredClone(atlas);
  atlas = prepareAtlas(atlas);
  assert.deepEqual(baseSource, untouched, "Display review must not mutate the source manifest");
  assert.equal(untouched.concepts.find(c=>c.id==='FMA8620').elements.length, 9);
  assert.equal(atlas.concepts.find(c=>c.id==='FMA8620').elements.length, 7);
  const registry=JSON.parse(await readFile(new URL('../public/models/extensions/index.json',import.meta.url)));
  for (const url of registry.manifests) {
    const extension=JSON.parse(await readFile(new URL('../public'+url,import.meta.url)));
    const previous=atlas;
    atlas=mergeAtlas(atlas,extension);
    for (const id of extension.extendsConceptIds ?? []) {
      const original=previous.concepts.find(c=>c.id===id);
      const merged=atlas.concepts.find(c=>c.id===id);
      for (const part of original.elements) assert(merged.elements.includes(part), 'Existing geometry was lost during extension');
      assert.throws(()=>mergeAtlas(previous,{...extension,extendsConceptIds:[]}), /yinelenen/);
    }
  }
  assert.deepEqual(prepareAtlas(atlas), atlas, 'Repeated metadata preparation must preserve both selections');
  // The actual foot bounds must fill a useful part of the free area without
  // projecting into the detail sheet or controls, including a depth-heavy view.
  const footIds = new Set(atlas.concepts.find(c=>c.id==='FMA11344').elements);
  const footBounds = new Box3();
  for (const p of atlas.parts.filter(p=>footIds.has(p.id)))
    footBounds.union(new Box3(new Vector3(...p.bounds[0]),new Vector3(...p.bounds[1])));
  for (const [w,h,left,right,top,bottom] of [
    [390,844,20,370,264,430], [320,568,20,300,190,290],
    [844,390,20,512,100,265], [1440,1000,285,1015,110,830],
  ]) for (const direction of [new Vector3(0,0,1),new Vector3(0,0,-1),new Vector3(1,0,0),new Vector3(.35,.1,1).normalize()]) {
    const center=footBounds.getCenter(new Vector3());
    const camera=new PerspectiveCamera(34,w/h,.005,100);
    camera.setViewOffset(w,h,w/2-(left+right)/2,h/2-(top+bottom)/2,w,h);
    camera.position.copy(center).addScaledVector(direction,
      inspectionDistance(footBounds,direction,camera.fov,h,right-left,bottom-top));
    camera.lookAt(center);
    camera.updateMatrixWorld();
    const xs=[],ys=[];
    for(const x of [footBounds.min.x,footBounds.max.x]) for(const y of [footBounds.min.y,footBounds.max.y]) for(const z of [footBounds.min.z,footBounds.max.z]) {
      const projected=new Vector3(x,y,z).project(camera);
      const px=(projected.x+1)*w/2,py=(1-projected.y)*h/2;
      assert(px>=left && px<=right && py>=top && py<=bottom,'Selected foot is clipped by inspection UI');
      assert(projected.z>=-1 && projected.z<=1,'Selected foot crosses a clipping plane');
      xs.push(px);ys.push(py);
    }
    assert(Math.max((Math.max(...xs)-Math.min(...xs))/(right-left),(Math.max(...ys)-Math.min(...ys))/(bottom-top))>.6,
      'Foot framing leaves the selected group too small');
  }
  const reviewedLung = atlas.concepts.find(c=>c.id==='FMA7309');
  const rawLung = atlas.concepts.find(c=>c.id==='atlas:source-membership:FMA7309');
  assert.equal(reviewedLung.elements.length, 163);
  assert.equal(rawLung.elements.length, 165);
  assert.equal(rawLung.elements.filter(id=>id.startsWith('BP43-')).length, 9, 'Source alias must retain subsequently merged tissue');
  assert.equal(atlas.concepts.find(c=>c.id==='atlas:source-membership:FMA8620').elements.length, 9);
  for (const id of ['FJ2041','FJ2044']) {
    assert(!reviewedLung.elements.includes(id));
    assert(rawLung.elements.includes(id));
    const original = untouched.parts.find(p=>p.id===id), current = atlas.parts.find(p=>p.id===id);
    assert.equal(current.sourceConceptId, original.conceptId);
    assert.match(anatomyLabel(current.conceptId,current.name,'tr'), /Kimliği doğrulanmamış damar/);
    for (const field of ['positions','normals','indices','bounds','vertexCount','indexCount','chunk'])
      assert.deepEqual(current[field], original[field], 'Source geometry must not be changed');
  }
  for (const raw of atlas.concepts.filter(c=>c.id.startsWith('atlas:source-membership:'))) {
    const reviewed=atlas.concepts.find(c=>c.id===raw.id.replace('atlas:source-membership:',''));
    assert.deepEqual(reviewed.elements,raw.elements.filter(id=>!['FJ2041','FJ2044'].includes(id)));
  }
  const groups=[atlas.parts,...[...new Set(atlas.parts.map(p=>p.system))].map(system=>atlas.parts.filter(p=>p.system===system))];
  for(const group of groups) for(const aspect of [.46,1,1.7]) {
    const layout=createExplosionLayout(group,aspect),cells=[...layout.cells.values()];
    assert.equal(cells.length,group.length);
    for(let i=0;i<cells.length;i++) {
      const a=cells[i];
      assert.ok(Math.abs(a.x)+a.width/2<=layout.width/2+1e-8);
      assert.ok(Math.abs(a.y)+a.height/2<=layout.height/2+1e-8);
      for(let j=i+1;j<cells.length;j++) {
        const b=cells[j];
        assert.ok(Math.abs(a.x-b.x)>=(a.width+b.width)/2-1e-8 || Math.abs(a.y-b.y)>=(a.height+b.height)/2-1e-8,'Exploded pieces overlap');
      }
    }
  }
  let selected=null;
  const [find,inspect]=atlasTools(atlas,c=>{selected=c;});
  const results=find.execute({query:'femur'});
  assert.ok(results.length>0);
  inspect.execute({id:results[0].id});
  const previous=selected;
  assert.throws(()=>inspect.execute({id:'nonexistent-structure'}));
  assert.equal(selected,previous);
  assert.throws(()=>find.execute({query:' '}));
  const concepts = explorerConcepts(atlas);
  const skull = concepts.find(c => c.id === 'atlas:skull-bones');
  assert.equal(skull.elements.length, 22);
  assert(skull.elements.includes('FJ3289'), 'Skull bones must include the mandible');
  assert(!skull.elements.some(id => ['FJ2772','FJ3201','FJ1289','FJ1340'].includes(id)), 'Skull bone view must exclude hyoid and eye surfaces');
  assert.equal(concepts.find(c => c.id === 'FMA46565').elements.length, 43, 'Source skull group must remain intact');
  const [findEnriched, inspectEnriched] = atlasTools({...atlas, concepts}, c => {selected=c;});
  assert(findEnriched.execute({query:'karaciger'}).some(c => c.id === 'FMA7197'));
  inspectEnriched.execute({id:'atlas:left-suprascapular-nerve'});
  assert.equal(selected.elements.length, 0, 'An unmodeled nerve must not inherit other geometry');
  console.log(`${file} with ${atlas.parts.length} registered pieces: packing at desktop/mobile aspect ratios and search/inspection contracts passed.`);
}
// A reference switch must never fetch male extensions or inherit their concepts.
const originalFetch = globalThis.fetch, referenceRequests = [];
let female;
try {
  globalThis.fetch = async (url) => {
    referenceRequests.push(String(url));
    return new Response(await readFile(new URL('../public' + url, import.meta.url)));
  };
  female = await loadAtlas(new AbortController().signal, 'female-pelvis');
} finally { globalThis.fetch = originalFetch; }
assert.deepEqual(referenceRequests, ['/models/female-pelvis/atlas.json']);
assert.equal(female.parts.length, 27);
assert.equal(female.anchors.length, 0);
const femaleConcepts = explorerConcepts(female);
assert(!femaleConcepts.some(c => c.id === 'atlas:left-median-nerve'));
let femaleSelected;
const [findFemale, inspectFemale] = atlasTools({...female, concepts:femaleConcepts}, c => {femaleSelected=c;});
const ovaries = findFemale.execute({query:'ovary'});
assert.equal(ovaries.length, 2, 'Each ovary should appear once in search');
inspectFemale.execute({id:ovaries[0].id});
assert.equal(femaleSelected.elements.length, 1);
assert.throws(() => inspectFemale.execute({id:'atlas:left-median-nerve'}));
console.log('Female reference loads independently and exposes only its own structures.');
const earRequests = [];
let ear;
try {
  globalThis.fetch = async (url) => {
    earRequests.push(String(url));
    return new Response(await readFile(new URL('../public' + url, import.meta.url)));
  };
  ear = await loadAtlas(new AbortController().signal, 'inner-ear-reference');
} finally { globalThis.fetch = originalFetch; }
assert.deepEqual(earRequests, ['/models/inner-ear-reference/atlas.json']);
assert.equal(ear.parts.length, 6);
assert.equal(ear.anchors.length, 0);
const earConcepts = explorerConcepts(ear);
assert(earConcepts.every(c => c.id.startsWith('inner-ear-reference:')));
const [findEar, inspectEar] = atlasTools({...ear, concepts:earConcepts}, () => {});
assert.equal(findEar.execute({query:'cochlea'}).length, 2);
assert.throws(() => inspectEar.execute({id:ovaries[0].id}));
console.log('Inner-ear reference exposes only its own six structures.');
const lowerRequests = [];
let lower;
try {
  globalThis.fetch = async (url) => {
    lowerRequests.push(String(url));
    return new Response(await readFile(new URL('../public' + url, import.meta.url)));
  };
  lower = await loadAtlas(new AbortController().signal, 'lower-limb-nerve-reference');
} finally { globalThis.fetch = originalFetch; }
assert.deepEqual(lowerRequests, ['/models/lower-limb-nerve-reference/atlas.json']);
assert.equal(lower.parts.length, 119);
assert.equal(lower.compatibleWithMainAtlas, false);
assert.equal(lower.anchors.length, 0);
const lowerConcepts = explorerConcepts(lower), lowerMap = new Map(lowerConcepts.map(c => [c.id, c]));
const [findLower] = atlasTools({...lower,concepts:lowerConcepts}, () => {});
assert.deepEqual(findLower.execute({query:'sol lumbrikal'}).map(r => r.id), ['zanatomy:lumbrical-muscles-of-foot-l']);
assert.deepEqual(findLower.execute({query:'sag plantar interosseoz'}).map(r => r.id), ['zanatomy:plantar-interossei-muscles-r']);
const tibial = lowerMap.get('atlas:left-tibial-nerve');
assert.deepEqual(tibial.elements, ['ZA-TIB-L']);
assert.equal(datasetLabel(lower.datasetId, tibial.id, tibial.name, 'tr'), 'Sol Tibial sinir');
assert.equal(datasetLabel(lower.datasetId, 'zanatomy:sacrum', 'Sacrum', 'la'), 'Os sacrum');
const childEdges = relationshipsFor(tibial.id, lowerMap, lower.datasetId);
assert.equal(childEdges.length, 3);
assert(childEdges.every(r => r.predicate === 'branch_of'));
assert(childEdges.some(r => r.otherId === 'atlas:left-sciatic-nerve'));
assert.deepEqual(childEdges.filter(r => r.object === tibial.id).map(r => r.otherId).sort(),
  ['atlas:left-lateral-plantar-nerve','atlas:left-medial-plantar-nerve']);
const parentEdges = relationshipsFor('atlas:left-sciatic-nerve', lowerMap, lower.datasetId);
assert.equal(parentEdges.length, 2);
assert(parentEdges.every(r => r.predicate === 'branch_of' && lowerMap.has(r.otherId)));
for (const side of ['left','right']) {
  const plantar = lowerMap.get(`atlas:${side}-medial-plantar-nerve`);
  assert.deepEqual(plantar.elements, [`ZA-MPL-${side[0].toUpperCase()}`]);
  const links = relationshipsFor(plantar.id, lowerMap, lower.datasetId);
  const branches = links.filter(r => r.predicate === 'branch_of');
  assert.equal(branches.length, 1);
  assert.equal(branches[0].otherId, `atlas:${side}-tibial-nerve`);
  assert(links.some(r => r.predicate === 'innervates' && r.otherId === `zanatomy:abductor-hallucis-${side[0]}`));
  assert.equal(lowerMap.get(`atlas:${side}-anterior-talofibular-ligament`).elements.length, 1);
  const suffix = side[0];
  const metatarsalId = `zanatomy:second-metatarsal-bone-${suffix}`;
  const proximalId = `zanatomy:proximal-phalanx-of-second-finger-of-foot-${suffix}`;
  const forward = relationshipsFor(metatarsalId, lowerMap, lower.datasetId);
  const inverse = relationshipsFor(proximalId, lowerMap, lower.datasetId);
  assert(forward.some(r => r.predicate === 'articulates_with' && r.otherId === proximalId));
  assert(inverse.some(r => r.predicate === 'articulates_with' && r.otherId === metatarsalId));
  assert(forward.every(r => r.label === 'Eklem yaptığı kemik'));
  const hallux = relationshipsFor(`zanatomy:proximal-phalanx-of-first-finger-of-foot-${suffix}`, lowerMap, lower.datasetId);
  assert.equal(hallux.filter(r => r.predicate === 'articulates_with').length, 2);
  assert(hallux.every(r => !r.otherId.includes('middle-phalanx')));
  const ligament = relationshipsFor(`atlas:${side}-calcaneofibular-ligament`, lowerMap, lower.datasetId);
  assert.equal(ligament.length, 2);
  assert(ligament.every(r => r.predicate === 'attaches_to' && r.attachmentNoteTr));
  assert.deepEqual(ligament.map(r => r.otherId).sort(), [`zanatomy:calcaneus-${suffix}`,`zanatomy:fibula-${suffix}`]);
  const muscleId = `zanatomy:abductor-hallucis-${suffix}`;
  const muscle = lowerMap.get(muscleId);
  assert.equal(muscle.elements.length, 1);
  const muscleLinks = relationshipsFor(muscleId, lowerMap, lower.datasetId);
  assert.equal(muscleLinks.length, 3);
  assert(muscleLinks.every(r => lowerMap.has(r.otherId)));
  assert(muscleLinks.filter(r => ['originates_at','inserts_at'].includes(r.predicate)).every(r => r.attachmentNoteTr));
  assert(muscleLinks.some(r => r.otherId === `atlas:${side}-medial-plantar-nerve`));
  const headId = `zanatomy:lateral-head-of-flexor-hallucis-brevis-${suffix}`;
  assert.equal(relationshipsFor(headId, lowerMap, lower.datasetId).length, 0, 'Do not inherit whole-muscle links to a head');
  assert.match(referenceDescription(lower.datasetId, headId), /kas başı/);
  assert.match(referenceDescription(lower.datasetId, `zanatomy:lumbrical-muscles-of-foot-${suffix}`), /Dört ayrı/);
  assert.match(referenceDescription(lower.datasetId, `zanatomy:sesamoid-bones-of-foot-${suffix}`), /medial\/lateral/);
  assert.match(referenceDescription(lower.datasetId, `zanatomy:flexor-digiti-minimi-of-foot-${suffix}`), /Latince ad henüz doğrulanmadı/);
  const mainMuscle = side === 'left' ? 'FMA37460' : 'FMA37459';
  const mainLinks = relationshipsFor(mainMuscle, undefined, 'male-body');
  assert(mainLinks.some(r => r.predicate === 'originates_at' && r.otherId === (side === 'left' ? 'FMA24498' : 'FMA24497')));
  assert(!mainLinks.some(r => r.otherId.startsWith('zanatomy:') || r.otherId.includes('plantar-nerve')), 'No reference-only nerve in main graph');
}
assert(relationshipsFor('atlas:left-sciatic-nerve', undefined, 'male-body').some(r => r.predicate === 'innervates'));
assert.deepEqual(relationshipsFor('atlas:left-sciatic-nerve', lowerMap, 'inner-ear-reference'), []);
console.log('Lower-limb reference resolves its own branch geometry without male graph leakage.');
const tap=new PointerTap();
tap.down(1,10,10,5);assert.equal(tap.up(1,12,11),true);
tap.down(1,10,10,5);tap.move(1,40,10);assert.equal(tap.up(1,10,10),false);
tap.down(1,10,10,12);tap.down(2,20,20,12);assert.equal(tap.up(2,20,20),false);assert.equal(tap.up(1,10,10),false);
tap.down(1,10,10,5);tap.cancel(1);assert.equal(tap.up(1,10,10),false);
tap.down(1,10,10,5);assert.equal(tap.up(1,10,10),true);
assert.equal(createExplosionLayout([]).cells.size,0);
console.log('Tap, drag, multitouch, cancellation, and empty-view checks passed.');
