import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createServer } from 'vite';
import react from '@vitejs/plugin-react';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

test('a recall session renders safely while retry clears the atlas, then retains its question', async () => {
  const server = await createServer({
    configFile: false, plugins: [react()],
    optimizeDeps: { noDiscovery: true, include: [] },
    server: { middlewareMode: true, hmr: false, watch: null }, appType: 'custom',
  });
  try {
    const { default: StudyPanel } = await server.ssrLoadModule('/app/study-panel.tsx');
    const { newHistory, saveStudy } = await server.ssrLoadModule('/app/study-history.ts');
    const { startStudy } = await server.ssrLoadModule('/app/study-session.ts');
    const { studyPacks } = await server.ssrLoadModule('/app/study-packs.ts');
    const pack = studyPacks.find(pack => pack.id === 'right-ankle-v1');
    const session = { ...startStudy(pack.items.length), phase: 'recall', index: 3 };
    const history = newHistory(pack, session, Date.now());
    const values = new Map();
    const storage = { getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value) };
    globalThis.window = { localStorage: storage };
    assert.ok(saveStudy(storage, pack, history));
    const before = [...values];
    const render = (concepts, blocked) => renderToStaticMarkup(createElement(StudyPanel, {
      pack, concepts, blocked, reveal() {}, exit() {},
    }));
    const loading = render(new Map(), true);
    assert.match(loading, /Hatırla · 4\/9/);
    assert.match(loading, /<fieldset disabled/);
    assert.match(loading, /class="study-answers"><\/div>/);
    const atlas = JSON.parse(readFileSync('public/models/lower-limb-nerve-reference/atlas.json', 'utf8'));
    const restored = render(new Map(atlas.concepts.map(concept => [concept.id, concept])), false);
    assert.match(restored, /Hatırla · 4\/9/);
    assert.doesNotMatch(restored, /<fieldset disabled/);
    assert.match(restored, /class="study-answers"><button/);
    assert.deepEqual([...values], before, 'rendering does not alter saved answers or scheduling');
  } finally {
    delete globalThis.window;
    await server.close();
  }
});
