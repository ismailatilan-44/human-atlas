import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';
const source = readFileSync('app/learning-storage.ts', 'utf8');
async function api(dev) {
  const js = ts.transpileModule(source.replaceAll('import.meta.env.DEV', String(dev)), { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }).outputText;
  return import(`data:text/javascript;base64,${Buffer.from(js).toString('base64')}`);
}
test('fixture storage isolates reads, writes and backups; production ignores activation flags', async () => {
  const data = new Map([['human-atlas.study.v1:pack', 'real history'], ['human-atlas.saved-scenes.v1', 'real scene']]);
  const storage = { getItem: k => data.get(k) ?? null, setItem: (k,v) => data.set(k,v) };
  globalThis.window = { localStorage: storage };
  globalThis.location = { hostname:'127.0.0.1', search:'?devqa=1' };
  const dev = await api(true), prod = await api(false);
  assert.equal(dev.fixtureMode(), true);
  assert.equal(dev.learningStorage().getItem('human-atlas.study.v1:pack'), null);
  dev.learningStorage().setItem('human-atlas.study.v1:pack', 'fixture');
  dev.learningStorage().setItem('human-atlas.saved-scenes.v1.backup', 'fixture backup');
  assert.equal(data.get('human-atlas.study.v1:pack'), 'real history');
  assert.equal(data.get('human-atlas.saved-scenes.v1'), 'real scene');
  assert.equal(prod.fixtureMode(), false);
  assert.equal(prod.learningStorage(), storage);
  assert.equal(prod.learningStorage().getItem('human-atlas.study.v1:pack'), 'real history');
  location.hostname = 'public.example';
  assert.equal(dev.fixtureMode(), false);
  location.hostname = 'localhost'; location.search = '?qa=1';
  assert.equal(dev.fixtureMode(), false);
  delete globalThis.window; delete globalThis.location;
});
