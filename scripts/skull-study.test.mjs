import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { createServer } from 'vite';
const json = path => JSON.parse(readFileSync(path, 'utf8'));
const pack = json('data/study/whole-skull-v1.json');
const atlas = json('public/models/atlas.json');
const labels = json(pack.labelSource).entries;
test('whole skull: exact 22 source bindings, bilateral labels and bounded answer evidence', () => {
  assert.deepEqual(pack.items.map(it => it.geometryPartId).sort(), json('data/anatomy/skull-bones.json').entities[0].geometryPartIds.toSorted());
  assert.equal(new Set(pack.items.map(it => it.conceptId)).size, 22);
  assert.equal(pack.items.filter(it => it.boneClass === 'cranial').length, 8);
  assert.equal(pack.items.filter(it => it.boneClass === 'facial').length, 14);
  for (const side of ['left', 'right']) assert.equal(pack.items.filter(it => it.side === side).length, 8);
  assert.equal(pack.items.filter(it => !it.side).length, 6);
  for (const input of pack.sourceInputs) assert.equal(createHash('sha256').update(readFileSync(input.path)).digest('hex'), input.sha256);
  for (const it of pack.items) {
    const part = atlas.parts.find(p => p.id === it.geometryPartId);
    assert.deepEqual(atlas.concepts.find(c => c.id === it.conceptId).elements, [part.id]);
    assert.equal(part.name, it.sourceObject); assert.equal(part.conceptId, it.conceptId);
    const label = labels.find(l => l.ids.includes(it.conceptId));
    assert.equal(label.side ?? null, it.side ?? null);
    for (const lang of ['tr', 'en', 'la']) assert.ok(label[lang]);
    assert.ok(part.vertexCount > 0 && part.indexCount > 0);
    assert.ok(it.evidence.some(e => e.locator.includes(part.id)));
  }
});
test('skull separation is source-preserving, stable across selection and reversible; saved state rejects foreign identities', async () => {
  const server = await createServer({ configFile: false, root: process.cwd(), optimizeDeps: { noDiscovery: true, include: [] }, server: { middlewareMode: true }, appType: 'custom' });
  try {
    const { skullOffset, skullStart, skullParts } = await server.ssrLoadModule('/app/skull.ts');
    const { captureScene, validateScene, isSavedScene } = await server.ssrLoadModule('/app/saved-scenes.ts');
    const concepts = new Map(atlas.concepts.map(c => [c.id, c]));
    concepts.set('atlas:skull-bones', {id:'atlas:skull-bones',elements:skullParts});
    for (const part of skullParts) {
      assert.notDeepEqual(skullOffset(part, part), [0,0,0]);
      assert.deepEqual(skullOffset(part), [0,0,0]);
      for (const other of skullParts.filter(p => p !== part)) assert.deepEqual(skullOffset(other, part), [0,0,0]);
    }
    const state = skullStart({ reset: 0 }); state.skull = { separated: skullParts[0] }; state.view = 'inferior';
    const saved = captureScene({ atlas, dataset:'male-body', state, camera:null, chosenId:'atlas:skull-bones', details:true, language:'tr', name:'Skull' });
    assert.equal(validateScene(saved,atlas,concepts),null); assert.deepEqual(saved.state.skull,state.skull);
    assert.equal(saved.state.view,'inferior');
    assert.match(validateScene({...saved,state:{...saved.state,skull:{separated:'FJ99999'}}},atlas,concepts),/geçersiz/);
    assert.equal(isSavedScene({...saved,dataset:'female-pelvis'}),false);
    assert.equal(isSavedScene({...saved,state:{...saved.state,explode:1}}),false);
    assert.equal(isSavedScene({...saved,state:{...saved.state,skull:{separated:'FJ3199',arbitrary:1}}}),false);
    assert.deepEqual(skullStart(state).skull,{});
  } finally { await server.close(); }
});

test('inferior concha prompts retain their separate source row rather than nasal-bone substring matches', () => {
  for (const id of ['FMA54738', 'FMA54737']) {
    const item = pack.items.find(it => it.conceptId === id);
    assert.ok(item.description.includes('yan duvar'));
    assert.ok(item.evidence.some(e => e.locator.endsWith('/ inferior nasal concha')));
    assert.ok(!item.evidence.some(e => e.locator.endsWith('/ nasal')));
  }
});
