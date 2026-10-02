// Repeatable checks of current, committed inputs. Do not run historical
// activation/export scripts here: those need separate source-intake prerequisites.
import { readdirSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const tests = readdirSync(new URL('./', import.meta.url))
  .filter(name => name.endsWith('.test.mjs')).sort().map(name => `scripts/${name}`);
if (!tests.length) throw new Error('No repository test suites found');
const checks = [
  ['TypeScript', 'npm', ['run', 'check']],
  ['All repository unit tests', process.execPath, ['--test', ...tests]],
  ['Current knowledge projection', process.execPath, ['scripts/build-anatomy-knowledge.mjs', '--check']],
  ['Current explorer projection', process.execPath, ['scripts/build-explorer-catalog.mjs', '--check']],
  ['Current source and coverage inventory', process.execPath, ['scripts/build-model-inventory.mjs', '--check']],
  ['Atlas binary and identity validation', process.execPath, ['scripts/validate-atlas.mjs']],
  ['Interaction and reference contracts', process.execPath, ['scripts/validate-interactions.mjs']],
  ['Production build', 'npm', ['run', 'build']],
  ['Production transfer budget', process.execPath, ['scripts/check-performance-budget.mjs']],
];
for (const [label, command, args] of checks) {
  console.log(`\n${label}: ${command} ${args.join(' ')}`);
  const result = spawnSync(command, args, { cwd: root, stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}
