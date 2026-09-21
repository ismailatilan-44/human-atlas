import test from 'node:test';
import assert from 'node:assert/strict';
import { buildKnowledge, validateKnowledge, relatedTo } from './build-anatomy-knowledge.mjs';

test('the source parent/child columns are imported in child-to-parent direction', () => {
  const graph = buildKnowledge();
  const branch = relatedTo(graph, 'FMA3736');
  assert(branch.outgoing.some(e => e.predicate === 'part_of' && e.object === 'FMA3734'));
  assert(!branch.incoming.some(e => e.predicate === 'part_of' && e.subject === 'FMA3734'));
});

test('registered nerve geometry merges with the existing biceps relationships', () => {
  const graph = buildKnowledge();
  const nerve = relatedTo(graph, 'atlas:left-musculocutaneous-nerve');
  assert.deepEqual(nerve.entity.geometryPartIds, ['ZA-MCN-L']);
  assert.equal(nerve.entity.representationStatus, 'registered_geometry');
  assert.equal(nerve.assetBindings[0].status, 'registered_geometry');
  assert(nerve.outgoing.some(e => e.predicate === 'innervates' && e.object === 'atlas:left-biceps-brachii'));
  assert.deepEqual(relatedTo(graph, 'atlas:left-biceps-brachii').entity.geometryPartIds, ['FJ1478M', 'FJ1512M']);
});

test('each registered median nerve innervates the four sourced muscles on its own side', () => {
  const graph = buildKnowledge();
  for (const [side,targets] of Object.entries({
    left: ['atlas:left-pronator-teres', 'FMA38461', 'FMA38464', 'FMA38471'],
    right: ['atlas:right-pronator-teres', 'FMA38460', 'FMA38463', 'FMA38470'],
  })) {
    const nerve = relatedTo(graph, `atlas:${side}-median-nerve`);
    assert.equal(nerve.entity.representationStatus, 'registered_geometry');
    const links = nerve.outgoing.filter(e => e.predicate === 'innervates');
    assert.deepEqual(links.map(e => e.object).sort(), targets.sort());
    for (const link of links) {
      assert.equal(relatedTo(graph, link.object).entity.side, side);
      assert(link.evidence.some(e => e.sourceId === 'uams-upper-limb' && e.locator.endsWith('/ Innervation')));
    }
  }
});

test('broken evidence, wrong-side links and missing endpoints are rejected', () => {
  for (const mutation of [
    edge => { edge.evidence = []; },
    edge => { edge.object = 'atlas:right-biceps-brachii'; edge.id = [edge.subject, edge.predicate, edge.object].join('|'); },
    edge => { edge.object = 'not-a-structure'; },
  ]) {
    const graph = buildKnowledge();
    const edge = graph.relations.find(e => e.subject === 'atlas:left-musculocutaneous-nerve' && e.predicate === 'innervates');
    mutation(edge);
    assert.throws(() => validateKnowledge(graph));
  }
});

test('cycles in part-of data cannot silently enter the graph', () => {
  const graph = buildKnowledge();
  const original = graph.relations.find(e => e.subject === 'FMA3736' && e.object === 'FMA3734');
  graph.relations.push({ ...original, id: 'FMA3734|part_of|FMA3736', subject: 'FMA3734', object: 'FMA3736' });
  assert.throws(() => validateKnowledge(graph), /Cycle/);
});
