import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'vite';
import react from '@vitejs/plugin-react';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

const server = await createServer({
  configFile: false, plugins: [react()],
  optimizeDeps: { noDiscovery: true, include: [] },
  server: { middlewareMode: true, hmr: false, watch: null }, appType: 'custom',
});
try {
  const { studyPacks } = await server.ssrLoadModule('/app/study-packs.ts');
  const {
    buildCustomStudyPack, makeCustomStudyPreset, resolveCustomStudyPreset,
    loadCustomStudyLibrary, saveCustomStudyLibrary, CUSTOM_STUDY_KEY,
  } = await server.ssrLoadModule('/app/custom-study.ts');
  const { newHistory, saveStudy, loadStudy, restartHistory, studyIdentity } =
    await server.ssrLoadModule('/app/study-history.ts');
  const { startStudy } = await server.ssrLoadModule('/app/study-session.ts');
  const { default: Builder } = await server.ssrLoadModule('/app/custom-study-builder.tsx');
  const base = studyPacks.find(p => p.id === 'whole-skull-v1');
  const ids = base.items.slice(0, 5).map(it => it.id);
  const storageValues = new Map();
  const storage = {
    getItem: key => storageValues.get(key) ?? null,
    setItem: (key, value) => storageValues.set(key, value),
  };
  test('custom selection is canonical, deterministic, constrained and preserves source identity', () => {
    const chosen = buildCustomStudyPack(base, [...ids].reverse());
    assert.equal(chosen.items.length, 5);
    assert.deepEqual(chosen.items, base.items.slice(0, 5));
    assert.deepEqual(buildCustomStudyPack(base, ids), chosen);
    assert.equal(chosen.datasetId, base.datasetId);
    assert.equal(chosen.attribution, base.attribution);
    assert.deepEqual(chosen.items[0].evidence, base.items[0].evidence);
    assert.equal(base.items.length, 22, 'original reviewed pack is untouched');
    assert.ok(!buildCustomStudyPack(base, ids.slice(0, 3)));
    assert.ok(!buildCustomStudyPack(base, [...ids, ids[0]]));
    assert.ok(!buildCustomStudyPack(base, [...ids.slice(0, 4), 'unknown-id']));
    const other = studyPacks.find(p => p.id === 'right-ankle-v1');
    assert.ok(!buildCustomStudyPack(other, ids), 'cross-reference selections cannot silently mix geometry');
  });
  test('saved set restores with its own history and never rewrites a built-in module', () => {
    const preset = makeCustomStudyPreset(base, ids);
    const custom = resolveCustomStudyPreset(preset, studyPacks);
    assert.ok(saveCustomStudyLibrary(storage, studyPacks, [preset]));
    assert.deepEqual(loadCustomStudyLibrary(storage, studyPacks).presets, [preset]);
    const history = newHistory(custom, startStudy(custom.items.length), 12);
    history.session.phase = 'recall';
    history.session.index = 2;
    assert.ok(saveStudy(storage, custom, history));
    assert.equal(loadStudy(storage, custom).history.session.index, 2);
    assert.equal(loadStudy(storage, base).history, undefined);
    assert.notEqual(studyIdentity(base), studyIdentity(custom));
    const next = restartHistory(history, custom, startStudy(custom.items.length), 20);
    assert.equal(next.session.index, 0);
    assert.equal(loadStudy(storage, custom).history.session.index, 2, 'new draft cannot change saved session');
    assert.equal(resolveCustomStudyPreset({ ...preset, sourceVersion: 'older' }, studyPacks), undefined);
    assert.equal(loadCustomStudyLibrary(storage, [{ ...base, version: 'older' }]).writable, false);
    assert.equal(storage.getItem(CUSTOM_STUDY_KEY), JSON.stringify({schema:1,presets:[preset]}));
  });
  test('corrupt, duplicate and inaccessible storage cannot erase existing data', () => {
    assert.equal(saveCustomStudyLibrary(storage, studyPacks,
      [makeCustomStudyPreset(base, ids), makeCustomStudyPreset(base, [...ids].reverse())]), false);
    storage.setItem(CUSTOM_STUDY_KEY, '{bad');
    const before = storage.getItem(CUSTOM_STUDY_KEY);
    const load = loadCustomStudyLibrary(storage, studyPacks);
    assert.equal(load.writable, false);
    assert.equal(storage.getItem(CUSTOM_STUDY_KEY), before);
    const inaccessible = { getItem() { throw Error('denied'); }, setItem() { throw Error('denied'); } };
    assert.equal(loadCustomStudyLibrary(inaccessible, studyPacks).writable, false);
    assert.equal(saveCustomStudyLibrary(inaccessible, studyPacks, [makeCustomStudyPreset(base, ids)]), false);
  });
  test('builder exposes regional structure selection and recovery actions', () => {
    globalThis.window = { localStorage: storage };
    storageValues.delete(CUSTOM_STUDY_KEY);
    try {
      const html = renderToStaticMarkup(createElement(Builder, { packs: studyPacks, onStart() {} }));
      assert.match(html, /Özel 3B çalışma seti/);
      assert.match(html, /Tümünü seç/);
      assert.match(html, /type="checkbox"/);
      assert.match(html, /Seti kaydet ve başlat/);
      assert.match(html, /whole-skull-v1/);
    } finally { delete globalThis.window; }
  });
} finally { await server.close(); }
