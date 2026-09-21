import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const predicates = new Set(['part_of', 'originates_at', 'inserts_at', 'innervates', 'supplies', 'passes_through', 'attaches_to']);
const sideOf = name => /\bleft\b/i.test(name) && !/\bright\b/i.test(name) ? 'left' : /\bright\b/i.test(name) && !/\bleft\b/i.test(name) ? 'right' : null;

export function validateKnowledge(graph) {
  const nodes = new Map(graph.entities.map(n => [n.id, n]));
  const sources = new Set(graph.sources.map(s => s.id));
  const parts = new Set(graph.geometryPartIds);
  assert.equal(parts.size, graph.geometryPartIds.length, 'Duplicate geometry part ID');
  assert.equal(nodes.size, graph.entities.length, 'Duplicate entity ID');
  assert.equal(sources.size, graph.sources.length, 'Duplicate source ID');
  const evidenceValid = records => {
    assert(records?.length, 'Missing evidence');
    for (const record of records) {
      assert(sources.has(record.sourceId), 'Unknown evidence source');
      assert(record.locator?.trim(), 'Missing evidence locator');
    }
  };
  for (const node of nodes.values()) {
    assert(node.name && node.representationStatus, 'Incomplete entity');
    for (const id of node.geometryPartIds) assert(parts.has(id), `Unknown geometry part ${id}`);
  }
  const seen = new Set();
  const parents = new Map();
  for (const edge of graph.relations) {
    assert(nodes.has(edge.subject) && nodes.has(edge.object), 'Dangling relation');
    assert(predicates.has(edge.predicate), 'Unknown relation type');
    assert(edge.subject !== edge.object, 'Self relation');
    const key = [edge.subject, edge.predicate, edge.object].join('|');
    assert.equal(edge.id, key, 'Relation ID does not match endpoints');
    assert(!seen.has(key), 'Duplicate relation');
    seen.add(key);
    evidenceValid(edge.evidence);
    assert(['source_imported', 'source_supported'].includes(edge.status), 'Missing review status');
    const left = nodes.get(edge.subject).side, right = nodes.get(edge.object).side;
    assert(!left || !right || left === right || edge.qualifiers?.crossesMidline === true, 'Cross-side relation needs explicit evidence');
    if (edge.predicate === 'part_of') {
      const list = parents.get(edge.subject) ?? [];
      list.push(edge.object);
      parents.set(edge.subject, list);
    }
  }
  const active = new Set(), visited = new Set();
  function visit(id) {
    assert(!active.has(id), 'Cycle in part_of hierarchy');
    if (visited.has(id)) return;
    active.add(id);
    for (const parent of parents.get(id) ?? []) visit(parent);
    active.delete(id);
    visited.add(id);
  }
  for (const id of nodes.keys()) visit(id);
  for (const binding of graph.assetBindings) {
    assert(nodes.has(binding.entityId), 'Dangling asset binding');
    assert(sources.has(binding.sourceId), 'Unknown asset source');
    assert(binding.objectName && binding.objectType, 'Incomplete asset reference');
    evidenceValid(binding.evidence);
  }
}

export function buildKnowledge() {
  const sources = JSON.parse(read('data/anatomy/sources.json'));
  for (const source of sources.filter(s => s.path)) {
    assert.equal(hash(read(source.path)), source.sha256, `Changed source ${source.id}; re-review and update fingerprint`);
  }
  const atlas = JSON.parse(read('public/models/atlas.json'));
  const pilot = JSON.parse(read('data/anatomy/upper-arm.json'));
  const forearm = JSON.parse(read('data/anatomy/forearm.json'));
  const knee = JSON.parse(read('data/anatomy/knee.json'));
  const sciatic = JSON.parse(read('data/anatomy/sciatic.json'));
  const entities = atlas.concepts.map(c => ({
    id: c.id, name: c.name, kind: 'source_concept',
    side: sideOf(c.name),
    geometryPartIds: c.elements,
    representationStatus: 'unknown',
    evidence: [{ sourceId: 'human-atlas', locator: `atlas.json / concepts / ${c.id}` }],
  }));
  const entityMap = new Map();
  for (const entity of [...entities, ...pilot.entities, ...forearm.entities, ...knee.entities, ...sciatic.entities]) {
    assert(!entityMap.has(entity.id), `Duplicate authored entity ${entity.id}`);
    entityMap.set(entity.id, entity);
  }
  const geometryPartIds = atlas.parts.map(p => p.id);
  const assetBindings = structuredClone(pilot.assetBindings);
  const registry = JSON.parse(read('public/models/extensions/index.json'));
  for (const url of registry.manifests) {
    assert(url.startsWith('/models/extensions/') && !url.includes('..'), 'Invalid extension manifest path');
    const manifestPath = `public${url}`;
    const source = sources.find(s => s.path === manifestPath);
    assert(source?.sha256, `Register extension provenance and fingerprint in sources.json: ${manifestPath}`);
    const manifest = JSON.parse(read(manifestPath));
    assert(manifest.registration?.method, `Missing geometry registration: ${manifestPath}`);
    geometryPartIds.push(...manifest.parts.map(p => p.id));
    const localParts = new Map(manifest.parts.map(p => [p.id, p]));
    for (const concept of manifest.concepts) {
      assert(concept.elements.length, `Empty registered concept ${concept.id}`);
      for (const id of concept.elements) assert(localParts.has(id), `Missing extension part ${id}`);
      const previous = entityMap.get(concept.id);
      const side = sideOf(concept.name);
      assert(!previous?.side || !side || previous.side === side, `Extension laterality mismatch ${concept.id}`);
      const evidence = [{ sourceId: source.id, locator: `${url} / concepts / ${concept.id}; registration` }];
      entityMap.set(concept.id, {
        id: concept.id, name: concept.name, kind: 'source_concept', side,
        expertReview: 'pending', anatomicalCoverage: 'non_exhaustive',
        ...previous,
        geometryPartIds: [...new Set([...(previous?.geometryPartIds ?? []), ...concept.elements])],
        representationStatus: 'registered_geometry',
        evidence: [...(previous?.evidence ?? []), ...evidence],
      });
      for (const id of concept.elements) {
        const part = localParts.get(id);
        assert(part.sourceObject && part.sourceObjectType, `Missing source object provenance ${id}`);
        const binding = assetBindings.find(b => b.entityId === concept.id && b.objectName === part.sourceObject);
        const registered = {
          entityId: concept.id, sourceId: manifest.source.id,
          objectName: part.sourceObject, objectType: part.sourceObjectType,
          mappingMethod: 'extension manifest canonical concept and source object mapping',
          status: 'registered_geometry', transformStatus: 'registered', geometryEquality: 'not_asserted',
          geometryPartIds: [id], registrationSourceId: source.id,
          evidence: [...(binding?.evidence ?? []), ...evidence],
        };
        if (binding) Object.assign(binding, registered);
        else assetBindings.push(registered);
      }
    }
  }
  const lines = read('data/anatomy/vendor/bodyparts3d/partof_inclusion_relation_list.txt').trim().split(/\r?\n/);
  assert.equal(lines.shift(), 'parent id\tparent name\tchild id\tchild name', 'Unexpected PART-OF columns');
  const relations = lines.map((line, index) => {
    const columns = line.split('\t');
    assert.equal(columns.length, 4, 'Malformed PART-OF row');
    const [parent, , child] = columns;
    return {
      id: `${child}|part_of|${parent}`, subject: child, predicate: 'part_of', object: parent,
      status: 'source_imported', expertReview: 'pending',
      evidence: [{ sourceId: 'bp3d-partof', locator: `line ${index + 2}: parent=${parent}, child=${child}` }],
      qualifiers: { semantics: 'Source PART-OF assertion; not a claim of complete geometry or physical attachment' },
    };
  });
  const graph = {
    schemaVersion: 1,
    coverage: { structural: 'BodyParts3D source PART-OF snapshot', functional: `${pilot.scope}; ${forearm.scope}; ${knee.scope}; ${sciatic.scope}`, complete: false },
    sources, geometryPartIds,
    entities: [...entityMap.values()], relations: [...relations, ...pilot.relations, ...forearm.relations, ...knee.relations, ...sciatic.relations],
    assetBindings,
  };
  validateKnowledge(graph);
  return graph;
}

export function relatedTo(graph, entityId) {
  const entity = graph.entities.find(n => n.id === entityId);
  assert(entity, `Unknown entity ${entityId}`);
  return {
    entity,
    outgoing: graph.relations.filter(r => r.subject === entityId),
    incoming: graph.relations.filter(r => r.object === entityId),
    assetBindings: graph.assetBindings.filter(b => b.entityId === entityId),
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const graph = buildKnowledge();
  const queryIndex = process.argv.indexOf('--entity');
  if (queryIndex >= 0) {
    console.log(JSON.stringify(relatedTo(graph, process.argv[queryIndex + 1]), null, 2));
  } else {
    const output = JSON.stringify(graph, null, 2) + '\n';
    const target = 'data/anatomy/knowledge.json';
    if (process.argv.includes('--check')) assert.equal(read(target), output, 'Generated knowledge is stale');
    else fs.writeFileSync(path.join(root, target), output);
    console.log(JSON.stringify({ entities: graph.entities.length, relations: graph.relations.length, assetBindings: graph.assetBindings.length, output: target }));
  }
}
