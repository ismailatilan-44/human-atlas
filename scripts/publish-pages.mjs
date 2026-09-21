// Publish the built static site using the existing repository contents permission.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
function run(command, args, cwd = root, capture = false) {
  return execFileSync(command, args, { cwd, encoding: 'utf8', stdio: capture ? 'pipe' : 'inherit' })?.trim();
}
const remote = run('git', ['remote', 'get-url', 'fork'], root, true);
const match = remote.match(/^https:\/\/github\.com\/([^/]+)\/([^/]+?)(?:\.git)?$/);
if (!match) throw new Error('Expected a GitHub HTTPS fork remote; inspect the publication destination.');
const [, owner, repo] = match;
if (run('git', ['status', '--porcelain', '--untracked-files=no'], root, true)) {
  throw new Error('Commit tracked changes before publishing a reproducible source revision.');
}
const revision = run('git', ['rev-parse', 'HEAD'], root, true);
run('npm', ['run', 'build', '--', `--base=/${repo}/`]);
const destination = fs.mkdtempSync(path.join(os.tmpdir(), 'atlas-pages-'));
try {
  run('git', ['init', '--initial-branch=gh-pages'], destination);
  run('git', ['remote', 'add', 'origin', remote], destination);
  run('git', ['config', 'user.name', run('git', ['config', 'user.name'], root, true)], destination);
  run('git', ['config', 'user.email', run('git', ['config', 'user.email'], root, true)], destination);
  const existing = run('git', ['ls-remote', '--heads', remote, 'gh-pages'], root, true);
  if (existing) {
    run('git', ['fetch', '--depth=1', 'origin', 'gh-pages'], destination);
    run('git', ['checkout', '-B', 'gh-pages', 'FETCH_HEAD'], destination);
  }
  for (const entry of fs.readdirSync(destination)) {
    if (entry !== '.git') fs.rmSync(path.join(destination, entry), { recursive: true, force: true });
  }
  fs.cpSync(path.join(root, 'dist'), destination, { recursive: true });
  const unpublishedPublicFiles = run('git', ['ls-files', '--others', '-z', '--', 'public'], root, true).split('\0').filter(Boolean);
  // Exporters may be producing candidates concurrently; do not publish uncommitted assets.
  for (const file of unpublishedPublicFiles) {
    fs.rmSync(path.join(destination, file.slice('public/'.length)), { recursive: true, force: true });
  }
  fs.writeFileSync(path.join(destination, '.nojekyll'), '');
  fs.writeFileSync(path.join(destination, 'release.json'), JSON.stringify({ revision }) + '\n');
  run('git', ['add', '.'], destination);
  if (run('git', ['status', '--porcelain'], destination, true)) {
    run('git', ['commit', '-m', `Publish anatomy explorer ${revision.slice(0, 7)}`], destination);
    run('git', ['push', 'origin', 'HEAD:refs/heads/gh-pages'], destination);
  }
  console.log(`Published static branch for https://${owner}.github.io/${repo}/; verify Pages deployment before reporting it live.`);
} finally {
  fs.rmSync(destination, { recursive: true, force: true });
}
