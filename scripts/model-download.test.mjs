import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { gzipSync } from 'node:zlib';
import ts from 'typescript';

const js = ts.transpileModule(readFileSync('app/model-download.ts', 'utf8'), {
  compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 },
}).outputText;
const { decodeModelResponse, loadModelChunks } = await import(`data:text/javascript;base64,${Buffer.from(js).toString('base64')}`);
const deferred = () => {
  let resolve, reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
};

test('static-host raw gzip and browser-decoded payloads produce identical geometry', async () => {
  const bytes = new Uint8Array([0, 4, 10, 255, 7, 19]);
  for (const response of [
    new Response(gzipSync(bytes)),
    new Response(bytes, { headers: { 'Content-Encoding': 'gzip' } }),
  ]) {
    assert.deepEqual(new Uint8Array(await decodeModelResponse(response, bytes.length, true)), bytes);
  }
  assert.deepEqual(new Uint8Array(await decodeModelResponse(new Response(bytes), bytes.length, false)), bytes);
});

test('failed HTTP, truncated and corrupt geometry are rejected before assembly', async () => {
  await assert.rejects(decodeModelResponse(new Response('missing', { status: 404 }), 7, false), /could not be loaded/);
  await assert.rejects(decodeModelResponse(new Response(new Uint8Array(3)), 4, false), /incomplete/);
  await assert.rejects(decodeModelResponse(new Response(new Uint8Array([0x1f, 0x8b, 0])), 4, true));
});

test('chunk loading caps simultaneous downloads at three and visits each chunk once', async () => {
  const started = [], waits = Array.from({ length: 7 }, deferred);
  let active = 0, peak = 0;
  const result = loadModelChunks(7, new AbortController().signal, async (index) => {
    started.push(index);
    peak = Math.max(peak, ++active);
    await waits[index].promise;
    active--;
  });
  assert.deepEqual(started, [0, 1, 2]);
  for (const wait of waits) {
    wait.resolve();
    await new Promise(setImmediate);
  }
  await result;
  assert.deepEqual(started, [0, 1, 2, 3, 4, 5, 6]);
  assert.equal(peak, 3);
});

test('one failed chunk cancels sibling fetches and never starts queued chunks', async () => {
  const failure = new Error('incomplete chunk'), failed = deferred();
  const started = [], cancelled = [];
  const result = loadModelChunks(8, new AbortController().signal, async (index, signal) => {
    started.push(index);
    if (index === 0) return failed.promise;
    await new Promise((resolve, reject) => {
      signal.addEventListener('abort', () => { cancelled.push(index); reject(signal.reason); }, { once: true });
    });
  });
  failed.reject(failure);
  await assert.rejects(result, error => error === failure);
  assert.deepEqual(started, [0, 1, 2]);
  assert.deepEqual(cancelled, [1, 2]);
});

test('switching references cancels active workers even after response decoding began', async () => {
  const controller = new AbortController(), decoding = deferred();
  const started = [], signals = [];
  const result = loadModelChunks(8, controller.signal, async (index, signal) => {
    started.push(index);
    signals.push(signal);
    await decoding.promise;
  });
  controller.abort();
  assert.ok(signals.every(signal => signal.aborted));
  decoding.resolve();
  await assert.rejects(result, { name: 'AbortError' });
  assert.deepEqual(started, [0, 1, 2]);
});

test('an already cancelled atlas never downloads geometry and a fresh retry can finish', async () => {
  const controller = new AbortController();
  controller.abort();
  let loaded = 0;
  await assert.rejects(loadModelChunks(2, controller.signal, async () => { loaded++; }), { name: 'AbortError' });
  assert.equal(loaded, 0);
  await loadModelChunks(2, new AbortController().signal, async () => { loaded++; });
  assert.equal(loaded, 2);
});
