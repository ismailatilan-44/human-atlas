import test from 'node:test';
import assert from 'node:assert/strict';
import { buildKnowledge, validateKnowledge, relatedTo } from './build-anatomy-knowledge.mjs';

test('the source parent/child columns are imported in child-to-parent direction', () => {
  const graph = buildKnowledge();
  const branch = relatedTo(graph, 'FMA3736');
  assert(branch.outgoing.some(e => e.predicate === 'part_of' && e.object === 'FMA3734'));
  assert(!branch.incoming.some(e => e.predicate === 'part_of' && e.subject === 'FMA3734'));
});

test('missing external nerve remains a candidate while links to existing biceps geometry resolve', () => {
  const graph = buildKnowledge();
  const nerve = relatedTo(graph, 'atlas:left-musculocutaneous-nerve');
  assert.deepEqual(nerve.entity.geometryPartIds, []);
  assert.equal(nerve.entity.representationStatus, 'external_candidate');
  assert(nerve.outgoing.some(e => e.predicate === 'innervates' && e.object === 'atlas:left-biceps-brachii'));
  assert.deepEqual(relatedTo(graph, 'atlas:left-biceps-brachii').entity.geometryPartIds, ['FJ1478M', 'FJ1512M']);
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
