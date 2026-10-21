// Keep cached HTML usable across deployments without indefinitely retaining carried assets.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

export const ASSET_RETENTION_SECONDS = 24 * 60 * 60;
const git = (cwd, args) => execFileSync('git', args, { cwd, maxBuffer: 32 * 1024 * 1024 });
const safeAsset = name => typeof name === 'string' && name.startsWith('assets/')
  && !name.split('/').some(part => !part || part === '.' || part === '..') && !name.includes('\\')
  && /-[A-Za-z0-9_-]{8}\.[A-Za-z0-9]+(?:\.map)?$/.test(name);

export function buildAssetPaths(dist) {
  const directory = path.join(dist, 'assets');
  return fs.readdirSync(directory, { recursive: true, withFileTypes: true })
    .filter(entry => entry.isFile())
    .map(entry => path.relative(dist, path.join(entry.parentPath, entry.name)).split(path.sep).join('/'))
    .filter(safeAsset)
    .sort();
}

export function publishedBuildAssets(destination, assets) {
  // Public exporters can create untracked assets during a build. The publisher
  // removes those files; never advertise them as part of the committed release.
  return assets.filter(name => fs.existsSync(path.join(destination, name)));
}

export function collectRetainedAssets(checkout, cutoff) {
  // Include the first older release: it was still served just before the first
  // publication inside this window, regardless of when that release was built.
  const revisions = [];
  for (const row of git(checkout, ['log', '--first-parent', '--format=%H%x09%ct']).toString().trim().split('\n')) {
    const [revision, timestamp] = row.split('\t');
    revisions.push(revision);
    if (Number(timestamp) < cutoff) break;
  }
  const retained = new Map();
  for (const revision of revisions) {
    const files = git(checkout, ['ls-tree', '-r', '--name-only', revision]).toString().trim().split('\n');
    const release = files.includes('release.json')
      ? JSON.parse(git(checkout, ['show', `${revision}:release.json`]).toString()) : {};
    // Legacy releases predate retention, so their assets tree is their original build.
    // New manifests name only original build assets, never assets carried from older releases.
    const assets = release.assets ?? files.filter(safeAsset);
    if (!Array.isArray(assets) || assets.some(name => !safeAsset(name)))
      throw new Error(`Invalid asset paths in published release ${revision}`);
    for (const name of assets) {
      if (!retained.has(name)) retained.set(name, git(checkout, ['show', `${revision}:${name}`]));
    }
  }
  return retained;
}

export function restoreRetainedAssets(destination, retained) {
  for (const [name, content] of retained) {
    fs.mkdirSync(path.dirname(path.join(destination, name)), { recursive: true });
    fs.writeFileSync(path.join(destination, name), content);
  }
}
