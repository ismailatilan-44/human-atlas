import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const json = path => JSON.parse(readFileSync(path, 'utf8'));
const modules = [
  ['left-ankle-v1', 'left', 9],
  ['right-upper-limb-bones-v1', 'right', 5],
];

for (const [id, side, count] of modules) {
  test(`${id}: versioned prompts bind distinct source surfaces, side, evidence and exact terms`, () => {
    const pack = json(`data/study/${id}.json`);
    const atlas = json(`public/models/${pack.datasetId}/atlas.json`);
    const metadata = json(pack.labelSource);
    assert.equal(pack.id, id);
    assert.equal(pack.version, '1');
    assert.equal(pack.expertReview, 'pending');
    assert.equal(pack.items.length, count);
    assert.ok(pack.learningGoals.length >= 2);
    assert.ok(pack.scope.includes('değerlendirilmez'));
    assert.ok(readFileSync(`public${pack.attribution}`, 'utf8').includes('Z-Anatomy'));
    assert.equal(new Set(pack.items.map(i => i.id)).size, count);
    assert.equal(new Set(pack.items.map(i => i.geometryPartId)).size, count);
    for (const input of pack.sourceInputs) {
      assert.equal(createHash('sha256').update(readFileSync(input.path)).digest('hex'), input.sha256,
        `Source changed: review question interpretation/version before updating ${input.path} fingerprint`);
    }
    for (const item of pack.items) {
      const concept = atlas.concepts.find(c => c.id === item.conceptId);
      assert.deepEqual(concept.elements, [item.geometryPartId]);
      const part = atlas.parts.find(p => p.id === item.geometryPartId);
      const label = metadata.labels.find(l => l.ids.includes(item.conceptId));
      assert.equal(part.sourceObject, item.sourceObject);
      assert.equal(part.side, side);
      assert.equal(part.componentRole, 'bone');
      assert.ok(part.vertexCount > 0 && part.indexCount > 0);
      assert.equal(label.side, side);
      assert.equal(label.sourceObject, item.sourceObject);
      assert.ok(label.la);
      assert.ok(label.terminologyStatus === 'verified_against_pinned_table' || label.latinStatus === 'exact_unsided_numeric_pinned_term');
      assert.deepEqual(item.evidence, label.evidence);
      assert.ok(item.evidence.some(e => e.sourceId === 'zanatomy-ta2-pinned'));
    }
  });
}

test('new ankle module preserves original recognition scope with separate left identities', () => {
  const right = json('data/study/right-ankle-v1.json');
  const left = json('data/study/left-ankle-v1.json');
  assert.deepEqual(left.items.map(i => i.conceptId), right.items.map(i => i.conceptId.replace(/-r$/, '-l')));
  assert.equal(left.items.some(i => right.items.some(r => r.id === i.id)), false);
  const upper = json('data/study/right-upper-limb-bones-v1.json');
  assert.deepEqual(upper.items.map(i => i.conceptId), ['clavicle', 'scapula', 'humerus', 'radius', 'ulna'].map(n => `zanatomy:${n}-r`));
});
