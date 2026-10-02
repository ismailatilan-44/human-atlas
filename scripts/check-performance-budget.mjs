import { readdir, readFile } from 'node:fs/promises';
import { gzipSync } from 'node:zlib';

// Deterministic production transfer budget, separate from real browser/device performance.
const assets = new URL('../dist/assets/', import.meta.url);
const files = (await readdir(assets)).filter(name => name.endsWith('.js'));
if (!files.length) throw new Error('No built JavaScript found; run npm run build first.');
let bytes = 0;
for (const file of files) bytes += gzipSync(await readFile(new URL(file, assets))).length;
const limit = 450_000;
console.log(`Production JavaScript gzip: ${bytes} bytes / ${limit} byte budget (${files.length} files).`);
if (bytes > limit) throw new Error('Production JavaScript transfer budget exceeded.');
