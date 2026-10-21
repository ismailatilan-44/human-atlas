import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { ASSET_RETENTION_SECONDS, buildAssetPaths, collectRetainedAssets, publishedBuildAssets, restoreRetainedAssets } from './pages-assets.mjs';

const git = (cwd, args, env = {}) => execFileSync('git', args, { cwd, env: { ...process.env, ...env }, stdio: ['ignore', 'pipe', 'pipe'] }).toString().trim();
function repository(root, name) {
  const dir = path.join(root, name);
  fs.mkdirSync(dir);
  git(dir, ['init', '--initial-branch=gh-pages']);
  git(dir, ['config', 'user.name', 'Asset retention test']);
  git(dir, ['config', 'user.email', 'test@example.invalid']);
  return dir;
}
function publish(dir, timestamp, files, assets) {
  for (const name of fs.readdirSync(dir)) if (name !== '.git') fs.rmSync(path.join(dir, name), { recursive: true });
  for (const [name, content] of Object.entries(files)) {
    fs.mkdirSync(path.dirname(path.join(dir, name)), { recursive: true });
    fs.writeFileSync(path.join(dir, name), content);
  }
  fs.writeFileSync(path.join(dir, 'release.json'), JSON.stringify({ revision: String(timestamp), ...(assets ? { assets } : {}) }));
  git(dir, ['add', '.']);
  const date = `${timestamp} +0000`;
  git(dir, ['commit', '-m', String(timestamp)], { GIT_AUTHOR_DATE: date, GIT_COMMITTER_DATE: date });
}

test('migration recovers recent deleted bundles plus the older served boundary without renewing carried assets', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'atlas-assets-test-'));
  try {
    const origin = repository(root, 'origin');
    const now = Math.floor(Date.now() / 1000), cutoff = now - ASSET_RETENTION_SECONDS;
    publish(origin, now - 72 * 3600, { 'assets/expired-01234567.js': 'expired' });
    publish(origin, now - 48 * 3600, { 'assets/index-Cx6lOCmP.js': 'old served HTML bundle' });
    publish(origin, now - 12 * 3600, { 'assets/index-DQw3vV3e.js': 'recent deleted bundle', 'assets/old-abcdefgh.css': 'old CSS' });
    publish(origin, now - 3600, { 'assets/current-12345678.js': 'current', 'assets/expired-01234567.js': 'carried only', 'index.html': 'latest HTML' }, ['assets/current-12345678.js']);
    const checkout = repository(root, 'checkout');
    git(checkout, ['remote', 'add', 'origin', pathToFileURL(origin).href]);
    git(checkout, ['fetch', '--depth=1', 'origin', 'gh-pages']);
    git(checkout, ['checkout', '-B', 'gh-pages', 'FETCH_HEAD']);
    git(checkout, ['fetch', `--shallow-since=${cutoff}`, 'origin', 'gh-pages']);
    git(checkout, ['fetch', '--deepen=1', 'origin', 'gh-pages']);
    const retained = collectRetainedAssets(checkout, cutoff);
    assert.deepEqual([...retained.keys()].sort(), ['assets/current-12345678.js', 'assets/index-Cx6lOCmP.js', 'assets/index-DQw3vV3e.js', 'assets/old-abcdefgh.css']);
    assert.equal(retained.get('assets/index-Cx6lOCmP.js').toString(), 'old served HTML bundle');
    const output = path.join(root, 'output');
    restoreRetainedAssets(output, retained);
    assert.equal(fs.readFileSync(path.join(output, 'assets/index-DQw3vV3e.js'), 'utf8'), 'recent deleted bundle');
    assert.ok(!fs.existsSync(path.join(output, 'index.html')), 'HTML and mutable source data are never carried');
    const build = path.join(root, 'build');
    fs.mkdirSync(path.join(build, 'assets/fonts'), { recursive: true });
    fs.writeFileSync(path.join(build, 'assets/current-12345678.js'), 'new output wins');
    fs.writeFileSync(path.join(build, 'assets/fonts/font-12345678.woff2'), 'font');
    fs.writeFileSync(path.join(build, 'assets/unversioned.js'), 'must not retain');
    fs.writeFileSync(path.join(build, 'assets/untracked-FAKEHASH.js'), 'exporter candidate');
    const declared = buildAssetPaths(build);
    fs.rmSync(path.join(build, 'assets/untracked-FAKEHASH.js'));
    assert.ok(!publishedBuildAssets(build, declared).includes('assets/untracked-FAKEHASH.js'));
    assert.deepEqual(buildAssetPaths(build), ['assets/current-12345678.js', 'assets/fonts/font-12345678.woff2']);
    fs.cpSync(build, output, { recursive: true });
    assert.equal(fs.readFileSync(path.join(output, 'assets/current-12345678.js'), 'utf8'), 'new output wins');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('an old latest release is retained while expired carried assets and ancestor releases are pruned', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'atlas-assets-old-test-'));
  try {
    const dir = repository(root, 'origin'), now = Math.floor(Date.now() / 1000);
    publish(dir, now - 72 * 3600, { 'assets/expired-01234567.js': 'expired' });
    publish(dir, now - 48 * 3600, { 'assets/last-abcdefgh.js': 'last served', 'assets/expired-01234567.js': 'carried' }, ['assets/last-abcdefgh.js']);
    const retained = collectRetainedAssets(dir, now - ASSET_RETENTION_SECONDS);
    assert.deepEqual([...retained.keys()], ['assets/last-abcdefgh.js']);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
