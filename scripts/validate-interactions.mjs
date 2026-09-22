import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createExplosionLayout} from '../app/explosion-layout.ts';
import {PointerTap} from '../app/pointer-tap.ts';
import {createServer} from 'vite';
// Use the app's bundler for its TypeScript and JSON dependency imports.
const loader = await createServer({configFile:false, optimizeDeps:{noDiscovery:true}, server:{middlewareMode:true}, appType:'custom'});
let atlasTools, mergeAtlas, loadAtlas, explorerConcepts;
try {
  ({atlasTools} = await loader.ssrLoadModule('/app/agent-tools.ts'));
  ({mergeAtlas, loadAtlas} = await loader.ssrLoadModule('/app/load-atlas.ts'));
  ({explorerConcepts} = await loader.ssrLoadModule('/app/knowledge.ts'));
}
finally { await loader.close(); }

for (const file of ['atlas.json']) {
  let atlas=JSON.parse(await readFile(new URL(`../public/models/${file}`,import.meta.url)));
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
const tap=new PointerTap();
tap.down(1,10,10,5);assert.equal(tap.up(1,12,11),true);
tap.down(1,10,10,5);tap.move(1,40,10);assert.equal(tap.up(1,10,10),false);
tap.down(1,10,10,12);tap.down(2,20,20,12);assert.equal(tap.up(2,20,20),false);assert.equal(tap.up(1,10,10),false);
tap.down(1,10,10,5);tap.cancel(1);assert.equal(tap.up(1,10,10),false);
tap.down(1,10,10,5);assert.equal(tap.up(1,10,10),true);
assert.equal(createExplosionLayout([]).cells.size,0);
console.log('Tap, drag, multitouch, cancellation, and empty-view checks passed.');
