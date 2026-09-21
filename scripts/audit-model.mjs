// Offline inventory of the packaged atlas. This does not certify anatomical accuracy.
// Usage: node scripts/audit-model.mjs [path/to/atlas.json] > inventory.json
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {gunzipSync} from 'node:zlib';
import assert from 'node:assert/strict';

const filename = path.resolve(process.argv[2] ?? fileURLToPath(new URL('../public/models/atlas.json', import.meta.url)));
const raw = fs.readFileSync(filename);
const atlas = JSON.parse(raw);
const directory = path.dirname(filename);
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const parts = new Map(atlas.parts.map(part => [part.id, part]));
assert.equal(parts.size, atlas.parts.length, 'Duplicate mesh IDs');
assert.equal(new Set(atlas.concepts.map(c => c.id)).size, atlas.concepts.length, 'Duplicate concept IDs');

const systems = new Map();
const buffers = atlas.chunks.map(chunk => {
  const buffer = fs.readFileSync(path.join(directory, path.basename(chunk.url)));
  assert.equal(buffer.byteLength, chunk.bytes, chunk.url);
  if (chunk.gzip) {
    const compressed = fs.readFileSync(path.join(directory, path.basename(chunk.gzip)));
    assert.equal(compressed.byteLength, chunk.gzipBytes, chunk.gzip);
    assert.ok(gunzipSync(compressed).equals(buffer), `Compressed payload differs: ${chunk.gzip}`);
  }
  return buffer;
});

const geometrySets = new Map();
for (const concept of atlas.concepts) {
  assert.ok(concept.elements.length > 0, `Empty concept: ${concept.id}`);
  for (const id of concept.elements) assert.ok(parts.has(id), `Missing mesh: ${concept.id} -> ${id}`);
  const key = [...new Set(concept.elements)].sort().join(',');
  const group = geometrySets.get(key) ?? [];
  group.push({id: concept.id, name: concept.name});
  geometrySets.set(key, group);
}

let vertices = 0;
let triangles = 0;
let zeroNormals = 0;
let verticesOutsideBounds = 0;
const allBounds = [[Infinity, Infinity, Infinity], [-Infinity, -Infinity, -Infinity]];
for (const part of atlas.parts) {
  const buffer = buffers[part.chunk];
  const positions = new Float32Array(buffer.buffer, buffer.byteOffset + part.positions, part.vertexCount * 3);
  const normals = new Int16Array(buffer.buffer, buffer.byteOffset + part.normals, part.vertexCount * 3);
  const indices = new Uint32Array(buffer.buffer, buffer.byteOffset + part.indices, part.indexCount);
  assert.equal(indices.length % 3, 0, `Non-triangular mesh: ${part.id}`);
  for (const index of indices) assert.ok(index < part.vertexCount, `Invalid index: ${part.id}`);
  for (let i = 0; i < part.vertexCount; i++) {
    let outside = false;
    for (let axis = 0; axis < 3; axis++) {
      const value = positions[i * 3 + axis];
      assert.ok(Number.isFinite(value), `Non-finite position: ${part.id}`);
      // Bounds originate before Float32 quantization and simplification; allow 1 micrometer.
      if (value < part.bounds[0][axis] - 1e-6 || value > part.bounds[1][axis] + 1e-6) outside = true;
      allBounds[0][axis] = Math.min(allBounds[0][axis], value);
      allBounds[1][axis] = Math.max(allBounds[1][axis], value);
    }
    if (outside) verticesOutsideBounds++;
    if (normals[i * 3] === 0 && normals[i * 3 + 1] === 0 && normals[i * 3 + 2] === 0) zeroNormals++;
  }
  vertices += part.vertexCount;
  triangles += part.indexCount / 3;
  const system = systems.get(part.system) ?? {meshes: 0, triangles: 0, chunks: new Set()};
  system.meshes++;
  system.triangles += part.indexCount / 3;
  system.chunks.add(part.chunk);
  systems.set(part.system, system);
}
assert.equal(triangles, atlas.triangles);

const terms = ['biceps brachii', 'musculocutaneous', 'median nerve', 'brachial plexus',
  'sciatic nerve', 'supraglenoid', 'coracoid', 'radial tuberosity', 'cochlea',
  'hippocampus', 'anterior cruciate', 'meniscus', 'alveol', 'nephron', 'ovary', 'uterus'];
const probes = terms.map(term => ({
  term,
  concepts: atlas.concepts.filter(c => c.name.toLowerCase().includes(term)).map(c => ({id: c.id, name: c.name, meshes: c.elements.length})),
  meshes: atlas.parts.filter(p => p.name.toLowerCase().includes(term)).map(p => ({id: p.id, name: p.name, system: p.system})),
}));
const examples = ['spinal cord', 'heart', 'brain'].map(name => {
  const concept = atlas.concepts.find(c => c.name.toLowerCase() === name);
  return {name, id: concept?.id, meshes: concept?.elements.map(id => {
    const part = parts.get(id);
    return {id, name: part.name, system: part.system};
  }) ?? []};
});
const reviewIds = ['FJ1730', 'FJ1731', 'FJ1752', 'FJ1767', 'FJ1814', 'FJ1438', 'FJ1438M'];
const sharedSets = [...geometrySets.values()].filter(group => group.length > 1);
const output = {
  scope: 'Packaged geometry and catalogue inventory; name probes are not proof of anatomical absence or correctness.',
  manifest: {sha256: sha256(raw), bytes: raw.byteLength, version: atlas.version, sex: atlas.sex},
  totals: {meshes: atlas.parts.length, concepts: atlas.concepts.length, vertices, triangles,
    sourceTrianglesReportedByManifest: atlas.sourceTriangles, chunks: atlas.chunks.length,
    geometryBytes: atlas.chunks.reduce((sum, c) => sum + c.bytes, 0),
    compressedGeometryBytes: atlas.chunks.reduce((sum, c) => sum + (c.gzipBytes ?? 0), 0)},
  geometry: {boundsInMeters: allBounds, zeroNormals, verticesOutsideBounds,
    integrityChecksPassed: true, checks: ['unique IDs', 'concept references', 'chunk lengths',
      'gzip equals binary', 'finite positions', 'triangle indices', 'triangle count']},
  catalogueFields: {part: Object.keys(atlas.parts[0]), concept: Object.keys(atlas.concepts[0])},
  systems: Object.fromEntries([...systems].map(([id, s]) => [id, {...s, chunks: [...s.chunks],
    compressedBytesOfRequiredChunks: [...s.chunks].reduce((sum, ci) => sum + (atlas.chunks[ci].gzipBytes ?? 0), 0)}])),
  sharedGeometry: {uniqueSets: geometrySets.size, sharedSets: sharedSets.length,
    conceptsInSharedSets: sharedSets.reduce((sum, group) => sum + group.length, 0),
    caveat: 'Different labels can select identical geometry; this may reflect aliases, aggregate concepts, or partial representation. Requires semantic review.',
    largestExamples: sharedSets.sort((a, b) => b.length - a.length).slice(0,3)},
  classificationReview: reviewIds.map(id => {
    const part = parts.get(id);
    return {id, name: part?.name, conceptId: part?.conceptId, assignedSystem: part?.system};
  }),
  probes,
  conceptGeometryExamples: examples,
};
console.log(JSON.stringify(output, null, 2));
