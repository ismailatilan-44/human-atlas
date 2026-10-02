import assert from 'node:assert/strict';
import { readFile, writeFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { createServer } from 'vite';

// Read-only with respect to the model: only these two derived artifacts are written.
const root = fileURLToPath(new URL('../', import.meta.url));
const inputs = new Map();
async function read(p) {
  const bytes = await readFile(path.join(root, p));
  inputs.set(p, { path: p, sha256: createHash('sha256').update(bytes).digest('hex') });
  return bytes.toString();
}
const json = async (p) => JSON.parse(await read(p));
const unique = (xs) => [...new Set(xs)];
const key = (datasetId, conceptId) => `${datasetId}::${conceptId}`;
const scopePath = 'docs/model/model-scope-and-acceptance.md';
const scope = await read(scopePath);
await read('scripts/build-model-inventory.mjs');
// Pin runtime inputs as well as manifests; generated inventory itself is not an input.
for (const name of (await readdir(path.join(root, 'data/anatomy'))).sort())
  if (name.endsWith('.json') && name !== 'model-inventory.json') await read(`data/anatomy/${name}`);
for (const name of ['load-atlas', 'atlas-metadata', 'reviewed-selections', 'reference-datasets', 'female-pelvis-labels', 'knowledge', 'anatomy', 'asset-url'])
  await read(`app/${name}.ts`);
const graph = await json('data/anatomy/knowledge.json');
const labels = await json('data/anatomy/labels.json');
const coverage = await json('data/anatomy/coverage.json');
const lowerLimb = await json('data/anatomy/lower-limb-reference.json');
const lowerTargetsPath = 'data/anatomy/regional-targets-lower-limb-v2.json';
const lowerTargets = await json(lowerTargetsPath);
const registry = await json('public/models/extensions/index.json');
const loader = await createServer({ root, configFile: false, optimizeDeps: { noDiscovery: true }, server: { middlewareMode: true }, appType: 'custom' });
let mergeAtlas, prepareAtlas, explorerConcepts, datasetLabel, referenceConcepts, getRepresentationNote, selectionReviewNote, REFERENCE_DATASETS;
try {
  ({ mergeAtlas } = await loader.ssrLoadModule('/app/load-atlas.ts'));
  ({ prepareAtlas, getRepresentationNote } = await loader.ssrLoadModule('/app/atlas-metadata.ts'));
  ({ explorerConcepts } = await loader.ssrLoadModule('/app/knowledge.ts'));
  ({ datasetLabel, referenceConcepts, REFERENCE_DATASETS } = await loader.ssrLoadModule('/app/reference-datasets.ts'));
  ({ selectionReviewNote } = await loader.ssrLoadModule('/app/reviewed-selections.ts'));
} finally { await loader.close(); }
const manifests = [];
for (const [datasetId, p] of [
  ['male-body', 'public/models/atlas.json'],
  ...registry.manifests.map((p) => ['male-body', `public${p}`]),
  ...Object.entries(REFERENCE_DATASETS).map(([datasetId, config]) => [datasetId, `public${config.manifest}`]),
]) manifests.push({ datasetId, path: p, data: await json(p) });
const landmarks = [];
for (const p of registry.landmarks) landmarks.push({ path: `public${p}`, data: await json(`public${p}`) });
const datasetIds = ['male-body', ...Object.keys(REFERENCE_DATASETS)];
const relationRows = [['male-body', graph.relations], ['lower-limb-nerve-reference', lowerLimb.relations]]
  .flatMap(([datasetId, relations]) => relations.map((r) => ({ ...r, id: key(datasetId, r.id), sourceRelationId: r.id, datasetId,
    subjectCatalogId: key(datasetId, r.subject), objectCatalogId: key(datasetId, r.object) })));
const maleManifests = manifests.filter((m) => m.datasetId === 'male-body');
const male = maleManifests.slice(1).reduce((atlas, m) => mergeAtlas(atlas, m.data), prepareAtlas(maleManifests[0].data));
male.datasetId = 'male-body';
const atlases = new Map([['male-body', male], ...manifests.filter((m) => m.datasetId !== 'male-body').map((m) => [m.datasetId, m.data])]);
const graphEntities = new Map(graph.entities.map((e) => [e.id, e]));
const labelEntries = new Map(labels.entries.flatMap((e, i) => e.ids.map((id) => [id, { ...e, index: i }])));
const catalog = new Map();
function ensure(datasetId, id, name) {
  const k = key(datasetId, id);
  if (!catalog.has(k)) catalog.set(k, { id: k, datasetId, conceptId: id, sourceName: name, sourceMemberships: [], classifications: [], coverageTargetIds: [] });
  return catalog.get(k);
}
const assets = [];
for (const m of manifests) {
  for (const c of m.data.concepts) ensure(m.datasetId, c.id, c.name).sourceMemberships.push({ manifest: m.path, locator: `concepts/${c.id}`, sourceName: c.name, assetIds: c.elements, sourceOntologyId: c.sourceOntologyId ?? null });
  for (const p of m.data.parts) {
    const { positions, normals, indices, chunk, ...metadata } = p;
    assets.push({ datasetId: m.datasetId, manifest: m.path, ...metadata });
  }
}
for (const e of graph.entities) ensure('male-body', e.id, e.name);
for (const [datasetId, atlas] of atlases) {
  const viewerConcepts = datasetId === 'male-body' ? explorerConcepts(atlas) : referenceConcepts(atlas);
  const view = new Map(viewerConcepts.map((c) => [c.id, c]));
  for (const c of viewerConcepts) ensure(datasetId, c.id, c.name);
  for (const row of catalog.values()) {
    if (row.datasetId !== datasetId) continue;
    const e = datasetId === 'male-body' ? graphEntities.get(row.conceptId) : undefined;
    const c = view.get(row.conceptId);
    const label = datasetId === 'male-body' ? labelEntries.get(row.conceptId)
      : datasetId === 'lower-limb-nerve-reference' ? lowerLimb.labels.find((l) => l.ids.includes(row.conceptId)) : undefined;
    const rawIds = unique(row.sourceMemberships.flatMap((m) => m.assetIds));
    const anchor = datasetId === 'male-body' ? landmarks.flatMap((m) => [...m.data.anchors, ...m.data.unresolved].filter((a) => a.conceptId === row.conceptId).map((a) => ({ manifest: m.path, ...a }))) : [];
    row.kind = e?.kind ?? (row.conceptId.startsWith('atlas:source-membership:') ? 'source_membership_display_variant' : row.conceptId.startsWith('atlas:unverified-source:') ? 'unverified_identity_display_selection' : row.sourceMemberships.length ? 'manifest_concept' : 'project_concept');
    const explicitAssetSides = unique(assets.filter((p) => p.datasetId === datasetId && rawIds.includes(p.id)).map((p) => p.side).filter(Boolean));
    row.side = e?.side ?? label?.side ?? (explicitAssetSides.length === 1 ? explicitAssetSides[0] : null);
    row.sideStatus = row.side ? 'recorded_in_graph_label_or_manifest_asset' : 'uninspected_or_multiple_sides; no_name_inference';
    row.viewerSelection = { available: !!c, assetIds: c?.elements ?? [], rawManifestAssetIds: rawIds, excludedFromRawMembership: rawIds.filter((id) => !c?.elements.includes(id)), note: datasetId === 'male-body' ? selectionReviewNote(row.conceptId) ?? null : c ? null : 'Source concept retained; duplicate selection alias is filtered by referenceConcepts.' };
    row.surfaceAnchors = anchor;
    row.representation = anchor.some((a) => a.position) ? 'surface_anchor' : c?.elements.length ? 'packaged_selection' : anchor.length ? 'unresolved_surface_anchor' : 'no_active_selection_geometry_recorded';
    row.requiredDetail = null;
    row.detailReview = 'uninspected; packaged membership does not establish D0–D3 acceptance';
    row.labels = { rendered: Object.fromEntries(['tr', 'en', 'la'].map((language) => [language, datasetLabel(datasetId, row.conceptId, row.sourceName, language)])), record: label ? { path: datasetId === 'male-body' ? 'data/anatomy/labels.json' : 'data/anatomy/lower-limb-reference.json', index: label.index, tr: label.tr ?? null, en: label.en ?? null, la: label.la ?? null, ta2Id: label.ta2Id ?? label.ta2TableId ?? null } : null, status: datasetId === 'male-body' ? label ? 'regional_label_record' : 'fallback_or_runtime_display_label; translation_uninspected' : 'dataset_scoped_runtime_labels; terminology_acceptance_pending', runtimeSource: datasetId === 'female-pelvis' ? 'app/female-pelvis-labels.ts' : 'app/reference-datasets.ts' };
    row.relationIds = relationRows.filter((r) => r.datasetId === datasetId && (r.subject === row.conceptId || r.object === row.conceptId)).map((r) => r.id);
    row.relationshipAcceptance = 'pending; relation existence does not satisfy family requirements';
    row.sourceEvidence = e?.evidence ?? [];
    row.graphRepresentationStatus = e?.representationStatus ?? null;
    row.visualAcceptance = { status: 'pending_target_level_reconciliation', sourceRecords: unique(anchor.map((a) => a.manifest)) };
    row.expertReview = 'pending';
    row.openIssues = unique([datasetId === 'male-body' ? getRepresentationNote(row.conceptId) : null, e?.anatomicalCoverage === 'non_exhaustive' ? 'Source record explicitly non_exhaustive.' : null, ...anchor.flatMap((a) => a.limitations ?? [])].filter(Boolean));
  }
}
const regionIds = ['skull-face','central-nervous-system','sensory','neck','thoracic-wall-mediastinum','cardiopulmonary','abdomen-retroperitoneum','pelvis-perineum','shoulder-axilla-arm','forearm-wrist-hand','hip-thigh-knee','leg-ankle-foot','surface-continuity'];
const familyIds = ['skeletal-support','muscle-tendon-fascia','neurovascular-lymph','organs-cavities-internal'];
const owners = ['P9','P10','P9','P9','P6','P6','P7','P8','P3','P4','P5','P4','P11'];
const tableRows = scope.split('\n').filter((line) => line.startsWith('| ') && line.split('|').length === 8 && !line.includes('Bölge |') && !line.includes('---'));
assert.equal(tableRows.length, 13, 'Scope matrix format changed: review generator');
const regions = tableRows.map((line, i) => {
  const cells = line.split('|').slice(1, -1).map((s) => s.trim());
  return { id: regionIds[i], nameTr: cells[0], ownerPackage: owners[i], scopeEvidence: { path: scopePath, tableRow: cells[0] }, requirements: familyIds.map((id, j) => ({ familyId: id, namedTargetsTr: cells[j + 1], targetExpansion: 'pending individual concept and laterality audit' })), detailEvidenceTr: cells[5], requiredDetailLevels: cells[5].startsWith('D1–D3') || cells[5].startsWith('D0–D3') ? ['D0','D1','D2','D3'] : ['D0','D1','D2'] };
});
const coverageMap = {};
function assign(region, family, names) { for (const name of names.split(' ')) coverageMap[`coverage:${name}`] = [region, family]; }
assign(0,0,'skull mandible'); assign(1,3,'brain hippocampus ventricles spinal-cord'); assign(2,3,'cochlea'); assign(3,0,'cervical-vertebrae laryngeal-cartilages'); assign(3,3,'thyroid');
assign(4,0,'ribs sternum'); assign(4,1,'diaphragm'); assign(4,2,'aorta'); assign(4,3,'esophagus'); assign(5,3,'heart lungs trachea');
assign(6,3,'liver stomach pancreas spleen kidneys gallbladder small-intestine large-intestine'); assign(7,3,'rectum urinary-bladder prostate uterus left-ovary right-ovary'); assign(7,0,'hip-bones sacrum');
assign(8,0,'clavicles scapulae humeri coracoid-process supraglenoid-tubercle humerus-medial-midshaft'); assign(8,1,'deltoid-parts biceps-long biceps-short coracobrachialis'); assign(8,2,'brachial-arteries musculocutaneous brachial-plexus');
assign(9,0,'radii ulnae carpals radial-tuberosity'); assign(9,2,'median-nerves'); assign(10,0,'femora patellae medial-menisci lateral-menisci acl pcl'); assign(10,1,'gluteus-maximus quadriceps-parts'); assign(10,2,'femoral-arteries sciatic'); assign(11,0,'tibiae fibulae tarsals');
function classify(row, regionIndex, familyIndex, evidence) {
  if (!row) return;
  const regionId = regionIds[regionIndex], familyId = familyIds[familyIndex];
  if (!row.classifications.some((c) => c.regionId === regionId && c.familyId === familyId)) row.classifications.push({ regionId, familyId, status: 'planning_assignment_from_explicit_record; not_extent_or_acceptance', evidence });
}
const pilotTargets = [];
for (const region of coverage.regions) for (const t of region.targets) {
  const assignment = coverageMap[t.id];
  // Unknown new pilot rows remain unassigned instead of receiving a guessed name match.
  const bindings = (t.currentBindings ?? []).map((b) => ({ datasetId: 'male-body', ...b }));
  if (t.separateReference) for (const conceptId of t.separateReference.conceptIds ?? [t.separateReference.conceptId]) bindings.push({ ...t.separateReference, conceptId });
  const refs = [];
  for (const b of bindings) {
    const row = catalog.get(key(b.datasetId, b.conceptId));
    assert(row, `Unresolved coverage concept ${b.datasetId}/${b.conceptId}`);
    row.coverageTargetIds.push(t.id); refs.push(row.id);
    if (assignment) classify(row, ...assignment, { path: 'data/anatomy/coverage.json', targetId: t.id });
  }
  pilotTargets.push({ id: t.id, nameTr: t.nameTr, recordedState: t.state, catalogIds: refs, representation: t.representation ?? null, note: t.note ?? null, expertReview: t.expertReview, source: 'data/anatomy/coverage.json', scope: 'legacy pilot row; no D-level acceptance inferred' });
}
const moduleRegions = { 'upper-arm':8, 'rotator-cuff':8, forearm:9, knee:10, sciatic:10, thyroid:3, 'spinal-cord':1, 'brachial-plexus':8, 'lung-parenchyma':5, 'skull-bones':0 };
const kindFamilies = { muscle:1, nerve:2, artery:2, vein:2, ligament:0, bone:0, landmark:0, organ:3 };
for (const [name, region] of Object.entries(moduleRegions)) {
  const p = `data/anatomy/${name}.json`, data = await json(p);
  for (const e of data.entities ?? []) {
    const row = catalog.get(key('male-body', e.id));
    if (row && kindFamilies[e.kind] !== undefined) classify(row, region, kindFamilies[e.kind], { path: p, entityId: e.id, recordedKind: e.kind });
  }
}
for (const row of catalog.values()) {
  if (row.datasetId !== 'male-body') {
    const parts = assets.filter((p) => p.datasetId === row.datasetId && row.sourceMemberships.some((m) => m.assetIds.includes(p.id)));
    const systems = unique(parts.map((p) => p.system));
    // Separate-reference scope and explicit manifest tissue systems corroborate assignment.
    if (row.datasetId === 'lower-limb-nerve-reference') {
      const label = lowerLimb.labels.find((l) => l.ids.includes(row.conceptId));
      const proximal = ['zanatomy:femur-l','zanatomy:femur-r','zanatomy:patella-l','zanatomy:patella-r','atlas:left-sciatic-nerve','atlas:right-sciatic-nerve'].includes(row.conceptId);
      const pelvic = ['zanatomy:hip-bone-l','zanatomy:hip-bone-r','zanatomy:sacrum'].includes(row.conceptId);
      if (label) classify(row, pelvic ? 7 : proximal ? 10 : 11, ['nerve','artery'].includes(label.componentRole) ? 2 : 0,
        { manifest: row.sourceMemberships[0]?.manifest, metadata: 'data/anatomy/lower-limb-reference.json', conceptId: row.conceptId, scope: 'Explicit reference work queue; not full anatomical extent.' });
    } else if (systems.length === 1 && ['skeletal','reproductive','sensory'].includes(systems[0])) classify(row, row.datasetId === 'female-pelvis' ? 7 : 2, systems[0] === 'skeletal' ? 0 : 3, { manifest: row.sourceMemberships[0]?.manifest, manifestSystem: systems[0] });
  }
  const targetMatches = lowerTargets.targets.filter((t) => t.representations.some((r) => r.datasetId === row.datasetId && r.conceptId === row.conceptId));
  row.regionalTargetIds = targetMatches.map((t) => t.id);
  if (targetMatches.length) {
    row.requiredDetail = unique(targetMatches.map((t) => t.requiredDetail));
    row.detailRequirementStatus = 'project_proposed; acceptance_pending';
    for (const target of targetMatches) classify(row, regionIds.indexOf(target.regionId), familyIds.indexOf(target.familyId),
      { path: lowerTargetsPath, targetId: target.id, status: target.requirementStatus });
  }
  row.classificationStatus = row.classifications.length ? 'evidence_linked_planning_assignment' : 'unassigned_uninspected';
}
const relationshipRequirements = {
  'skeletal-support': ['joint participating structures and supports', 'source-backed structural hierarchy'],
  'muscle-tendon-fascia': ['source-backed origin', 'source-backed insertion', 'motor innervation'],
  'neurovascular-lymph': ['named source hierarchy', 'verified nerve targets or vascular territories as appropriate', 'cross-region continuity'],
  'organs-cavities-internal': ['source-backed subdivisions', 'related ducts or networks'],
};
const targetMatrix = regions.flatMap((region) => region.requirements.flatMap((requirement) => ['D0','D1','D2','D3'].map((detailLevel) => ({
  id: `scope-v1:${region.id}:${requirement.familyId}:${detailLevel}`, regionId: region.id, familyId: requirement.familyId, detailLevel,
  namedTargetsTr: requirement.namedTargetsTr,
  requirement: region.requiredDetailLevels.includes(detailLevel) ? detailLevel === 'D0' ? 'context_prerequisite' : 'required_regional_scope; per_structure_applicability_pending' : 'pending_scope_decision; not_dropped',
  status: 'pending_target_expansion_and_acceptance', ownerPackage: detailLevel === 'D3' ? 'P12' : region.ownerPackage,
  catalogIdsForInspection: [...catalog.values()].filter((r) => r.classifications.some((c) => c.regionId === region.id && c.familyId === requirement.familyId)).map((r) => r.id),
  individualTargetIds: lowerTargets.targets.filter((t) => t.regionId === region.id && t.familyId === requirement.familyId && t.requiredDetail === detailLevel).map((t) => t.id),
  bindingSemantics: 'Inspection candidates across this family; not proof that each concept represents this detail level or every named target.',
  requiredRelationships: relationshipRequirements[requirement.familyId],
  openWork: ['expand named groups to individual source identities and sides', 'audit existing source concepts and subobjects at requested detail', 'record required geometry/anchor and relation gaps after inspection', 'visual product acceptance and named expert review pending'],
  scopeEvidence: region.scopeEvidence,
}))));
const datasets = datasetIds.map((datasetId) => {
  const ms = manifests.filter((m) => m.datasetId === datasetId), atlas = atlases.get(datasetId);
  return { id: datasetId, sex: atlas.sex, coordinateFrame: atlas.coordinateFrame ?? atlas.coordinates ?? atlas.coordinateSystem ?? 'Human Atlas: X left, Y superior, Z anterior; registered extensions use recorded transforms', viewerStatus: datasetId === 'male-body' ? 'main_reference_with_registered_extensions' : 'separate_selectable_reference', manifestStatus: ms[0].data.status ?? null, parts: atlas.parts.length, manifestConcepts: unique(ms.flatMap((m) => m.data.concepts.map((c) => c.id))).length, catalogRows: [...catalog.values()].filter((r) => r.datasetId === datasetId).length, manifests: ms.map((m) => ({ path: m.path, version: m.data.version, source: m.data.source, status: m.data.status ?? null, registration: m.data.registration ?? null, coordinateFrame: m.data.coordinateFrame ?? m.data.coordinates ?? m.data.coordinateSystem ?? null, appliedDisplayTransform: m.data.appliedDisplayTransform ?? null, licensePolicy: m.data.licensePolicy ?? null, limitations: m.data.limitations ?? [], attribution: m.data.source?.attribution ?? (datasetId === 'male-body' && m === ms[0] ? 'public/ATTRIBUTION.md' : `public/models/${datasetId}/ATTRIBUTION.md`) })) };
});
for (const asset of assets) assert(atlases.get(asset.datasetId).parts.some((p) => p.id === asset.id));
for (const row of catalog.values()) for (const id of [...row.viewerSelection.assetIds, ...row.viewerSelection.rawManifestAssetIds]) assert(assets.some((p) => p.datasetId === row.datasetId && p.id === id), `Unresolved part ${row.id}/${id}`);
for (const relation of relationRows) for (const endpoint of [relation.subjectCatalogId, relation.objectCatalogId]) assert(catalog.has(endpoint), `Unresolved relation endpoint ${endpoint}`);
assert.equal(targetMatrix.length, 208);
assert.equal(new Set(targetMatrix.map((r) => r.id)).size, 208);
const catalogRows = [...catalog.values()].sort((a,b) => a.id.localeCompare(b.id, 'en'));
const summary = { catalogRows: catalogRows.length, assetRows: assets.length, pilotTargetRows: pilotTargets.length, regions: regions.length, familyRequirements: regions.length * familyIds.length, targetMatrixCells: targetMatrix.length, classifiedCatalogRows: catalogRows.filter((r) => r.classifications.length).length, unassignedCatalogRows: catalogRows.filter((r) => !r.classifications.length).length, surfaceAnchorConcepts: catalogRows.filter((r) => r.representation === 'surface_anchor').length, unresolvedAnchorConcepts: catalogRows.filter((r) => r.representation === 'unresolved_surface_anchor').length, relationRecords: relationRows.length };
for (const dataset of datasets) for (const manifest of dataset.manifests) {
  if (manifest.attribution) await read(manifest.attribution.startsWith('/') ? `public${manifest.attribution}` : manifest.attribution);
}
for (const row of catalog.values()) {
  if (row.kind === 'source_membership_display_variant') {
    const canonical = catalog.get(key(row.datasetId, row.conceptId.replace('atlas:source-membership:', '')));
    assert(canonical, `Unresolved source variant ${row.id}`);
    assert.deepEqual([...row.viewerSelection.assetIds].sort(), [...canonical.viewerSelection.rawManifestAssetIds].sort(), `Lost source membership ${row.id}`);
  }
  if (row.representation === 'unresolved_surface_anchor') assert(row.surfaceAnchors.every((a) => a.position === null));
}
const output = { schemaVersion: 1, scopeVersion: 'model-scope-v1', inventoryVersion: 2, generatedBy: 'node scripts/build-model-inventory.mjs', sourceScope: scopePath, complete: false, countingPolicy: 'Dataset-qualified concept records, source assets and pending scope cells are separate units; none is an anatomy completeness denominator.', inputSnapshots: [...inputs.values()].sort((a,b) => a.path.localeCompare(b.path,'en')), summary, datasets, regions, targetMatrix, pilotTargets, regionalTargetSeeds: [lowerTargets], catalog: catalogRows, assets, relations: relationRows, sources: [...graph.sources.map((s) => ({ ...s, datasetId: 'male-body' })), ...lowerLimb.sources.map((s) => ({ ...s, datasetId: lowerLimb.datasetId }))], caveats: ['An input hash pins the local record, not upstream license or anatomical approval.', 'Only registry manifests are active male extensions; other disk candidates are excluded.', 'Raw memberships are retained separately from curated viewer selections and display groups.', 'Source names and system layers do not establish regional identities, independent geometry, detail level or absence.', `Every D0–D3 cell stays pending. Individual target expansion and expert acceptance remain open, including cells with linked concepts. A non-exhaustive lower-limb seed contributes ${lowerTargets.summary.targets} explicit targets; acceptance remains pending.`, 'Female aliases remain in source inventory even when reference search deduplicates them.', `Only the lower-limb reference has ${lowerLimb.relations.length} sourced dataset-scoped relations; other separate-reference relations remain uninspected. No male graph is applied to references.`, 'Generic fallback labels do not count as verified translations.', 'Asset metadata retain reference coordinates and per-component licensing. No geometry is transformed by this generator.'] };
const documentation = `# Model inventory — scope v1\n\nThis reproducible P1 inventory catalogs actual source and viewer identities alongside a **pending** whole-body target matrix. It is not anatomical acceptance or a completion percentage.\n\nRebuild with \`node scripts/build-model-inventory.mjs\`; verify without writing with \`node scripts/build-model-inventory.mjs --check\`. The script validates dataset-qualified concept/asset links, coverage and relationship endpoints, and 13 × 4 × 4 matrix identities. Runtime selections are computed through the viewer's own functions; generation does not render or inspect geometry.\n\nThe machine-readable [inventory](../../data/anatomy/model-inventory.json) pins all consumed manifest/data/runtime files and this generator by SHA-256. Changes in registered extensions require regeneration.\n\n| Dataset | Packaged assets | Unique manifest concepts | Catalog records |\n|---|---:|---:|---:|\n${datasets.map((d) => `| ${d.id} | ${d.parts} | ${d.manifestConcepts} | ${d.catalogRows} |`).join('\n')}\n\nThere are ${summary.catalogRows} dataset-qualified catalog records and ${summary.assetRows} asset records. Catalog rows include source concepts, project/graph concepts and runtime selection variants, which overlap anatomically. They are not counts of distinct anatomical structures. ${summary.classifiedCatalogRows} records have evidence-linked region/family planning assignments, including source-linked individual target proposals; ${summary.unassignedCatalogRows} remain explicitly unassigned and uninspected. No name-based absence or membership inference is made.\n\n${summary.pilotTargetRows} legacy pilot targets link to the catalog without becoming a whole-body denominator. ${summary.surfaceAnchorConcepts} concepts have source-derived surface anchors and ${summary.unresolvedAnchorConcepts} retain unresolved/null anchors. Anchor context bones are not substituted for attachment surfaces. ${summary.relationRecords} typed graph relations retain their evidence and direct/transitive qualifiers; their presence does not prove each family's required relationships are complete.\n\n## Pending scope matrix\n\nThe 13 regional rows and four named family requirements are read verbatim from [the scope contract](model-scope-and-acceptance.md), producing ${summary.familyRequirements} named family requirements and ${summary.targetMatrixCells} D0–D3 cells. Each cell has a package owner, source-linked inspection candidates when available, relationship requirements and explicit open work. D0 is a context prerequisite; D3 remains pending even for regions whose initial scope says D1–D2. Regional ranges do not mean every listed structure requires every level. **Every cell remains pending complete individual target, laterality and detail expansion and acceptance. The lower-limb seed now enumerates ${lowerTargets.summary.targets} individual project targets; it is not exhaustive and closes no cell.** P1 establishes a usable inventory scaffold and source catalog; it does not close the scope contract's requirement to individually enumerate every named target. See [the individual lower-limb seed](lower-limb-targets-v2.md).\n\n| Region | Package owner | Named family requirements | D0–D3 cells |\n|---|---|---:|---:|\n${regions.map((r) => `| ${r.nameTr} | ${r.ownerPackage}; D3: P12 | 4 | 16 |`).join('\n')}\n\nAssignments use explicit pilot IDs, typed entities in regional records, or separate-reference scope plus manifest systems. These assignments identify work queues, not complete regional extent: aorta, esophagus and major nerves can cross regions. There is no propagation from source aggregate membership or label matches. An unassigned base concept remains discoverable by its preserved ID, source name, membership and typed relationships.\n\n## Membership, labels and source boundaries\n\nEach catalog row separates original per-manifest membership from actual curated viewer selection. The pulmonary raw/reviewed variants and unverified source vessels are retained as different records. Project display groups keep their graph kind. Female source aliases remain cataloged even when search deduplicates them. Datasets keep distinct coordinate frames, source/registration records, limitations and attribution. Inner-ear component licenseScope fields remain on asset records. Historical female manifest candidate status is recorded separately from its current selectable-reference status.\n\nLabels report both runtime text and explicit regional-label evidence. Fallback source text is not a verified TR/LA translation. Surface-anchor, graph representation, technical selection and expert statuses remain separate; stale graph-only landmark statuses do not replace registered anchor evidence. The generator retains ${lowerLimb.relations.length} sourced lower-limb reference relationships without borrowing the male graph, and does not invent other reference relationships, infer independent subdivisions from names, inspect binary geometry, or mark absence. Existing visual/source reports require target-level reconciliation; expert review remains pending.\n\nFor queries, use dataset-qualified \`catalog[].id\`; join \`viewerSelection.assetIds\` and \`sourceMemberships[].assetIds\` to \`assets\` by dataset and ID; join \`relationIds\` to \`relations\`; follow \`coverageTargetIds\` into \`pilotTargets\`; follow \`targetMatrix[].catalogIdsForInspection\` into the catalog. The same source concept may legitimately occur in several scopes and detail inspection queues.\n`;
for (const [p, content] of [['data/anatomy/model-inventory.json', JSON.stringify(output, null, 2) + '\n'], ['docs/model/model-inventory.md', documentation]]) {
  if (process.argv.includes('--check')) assert.equal(await readFile(path.join(root, p), 'utf8'), content, `${p} is stale; regenerate inventory`);
  else await writeFile(path.join(root, p), content);
}
console.log(JSON.stringify({ mode: process.argv.includes('--check') ? 'check' : 'build', ...summary }));
