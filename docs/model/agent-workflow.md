# Agent startup and source → producer → check routing

This guide applies to this repository, including isolated checkouts. Start with root `AGENTS.md`, `README.md`, the scope plan and the linked delivery handoff. Compare their recorded source revisions with `git rev-parse HEAD` and `git status --short`; a historical deployment entry does not verify today's live site.

## Portable startup

`AGENTS.md` and `.agents/skills/*/SKILL.md` belong in Git. New worktrees and clones inherit them only from a revision containing these files. Check `git ls-files AGENTS.md '.agents/skills/*/SKILL.md'`: expect the root guide and six skills. If using an older base, report the missing guidance and use an explicitly selected guidance-bearing revision or an authorized, reviewed bootstrap copy. Do not change the implementation base or integrate unrelated work merely to obtain instructions. Existing isolated work is not retroactively updated.

Read only the relevant skill: source-intake for acquisition/provenance; asset-audit for geometry/export; term-mapping for identities, labels and relationships; regional-acceptance for coverage and product QA; product-benchmark for observed competitor tasks; imaging-to-mesh for licensed image-derived candidates. Repository-relative links and commands resolve from the checkout root. Source tools such as Blender and pinned TA2 inputs are task prerequisites, not bundled dependencies; record a missing prerequisite instead of downloading or replacing it implicitly.

## Ownership and dependency order

| Change | Owning inputs | Producer / output | Smallest relevant verification |
| --- | --- | --- | --- |
| Main anatomy concepts, relations, provenance, registered geometry | `data/anatomy/sources.json`, regional modules listed in `buildKnowledge()` (including `upper-arm.json`, `rotator-cuff.json`, `foot-supports.json`), base manifest, `public/models/extensions/index.json` and its manifests | `node scripts/build-anatomy-knowledge.mjs` → `data/anatomy/knowledge.json`; then `node scripts/build-explorer-catalog.mjs` → `data/anatomy/explorer.json` | Both producers with `--check`, then `node --test scripts/anatomy-knowledge.test.mjs`; geometry/selection changes also need atlas and interaction validation |
| Main display labels and selected coverage | `data/anatomy/labels.json`, `coverage.json`, their owning evidence/target records | Authored inputs consumed by runtime and inventory; do not edit generated catalogs to change labels | Knowledge tests and interaction validator; rebuild/check inventory when its inputs change |
| Independent reference geometry, terms and relations | `app/reference-datasets.ts`, reference manifests, `lower-limb-reference.json`, `upper-limb-reference.json`, dataset-specific label modules | Owning package/export/target scripts documented in README and the regional record; not an implicit merge into the male graph | The owning package `--check` and target checks, atlas/interaction validators, actual dataset-switch journey |
| Regional targets and overall catalog | Versioned target inputs/producers in README; runtime metadata, anatomy JSON, manifests and scope plan | `node scripts/build-model-inventory.mjs` → `data/anatomy/model-inventory.json` + `docs/model/model-inventory.md` | `node scripts/build-model-inventory.mjs --check`; this is separate from knowledge/explorer generation |
| Viewer TypeScript/UI | `app/` and relevant assets | Vite build | `npm run check` (TypeScript only); `node scripts/validate-interactions.mjs` for interaction logic; `node scripts/validate-atlas.mjs` for model/layout changes; `npm run build` for bundling changes; browser journey for visible behavior |

Run commands from the repository root using the README's Node version. Regenerate only affected outputs, inspect the diff, then check in dependency order: knowledge → explorer → inventory. `--check` compares/validates without rewriting outputs. The inventory producer fingerprints anatomy JSON, runtime files and scope inputs; a stale snapshot is resolved at its owning source, not by hand-editing hashes in the output. Do not regenerate anatomy artifacts for an instruction-only change.

The build's `prebuild` checks the explorer projection, not whether the knowledge graph was freshly derived from its authored inputs. A successful TypeScript check or Pages deployment is not proof that anatomy tests ran. There is no checked-in `.github/workflows` test pipeline in this baseline; report actual invoked checks and deployment evidence separately.

## Frozen activation versus reusable validation

Read a historical integration script before selecting it as a check. `scripts/integrate-foot-supports.py` activates a frozen proposal: it rejects changed records with the same identity and asserts global counts (including exactly 401 main labels). Its `--check` verifies that activation snapshot; it is not a universal validator for later label edits/additions. Do not overwrite a reviewed new record with the historical proposal or relax source evidence merely to make that script pass. For later edits use the owning current records, knowledge tests, runtime validators and inventory checks; retain/reconcile historical evidence explicitly. The same distinction applies to frozen candidate builders and later target versions.

## Browser evidence

Use an already authorized browser through its supported controls. Verify a loaded model and a visible change after selection/focus/isolation/return; a canvas element or a WebGL availability flag alone is insufficient. From the repository root, `python3 -m http.server 3018 --bind 127.0.0.1 --directory scripts` serves `http://127.0.0.1:3018/webgl-probe.html`. This exercises an actual WebGL context, draws a triangle and reads back its center pixel; the button redraws in a different color. Stop the diagnostic server after QA. It is a diagnostic page, not a product asset or anatomical acceptance test. Pair its result with screenshots of the real Atlas interaction and the served source revision.

If browser evaluation exposes only a read-only DOM proxy, canvas `getContext()` may be unavailable there; that does not establish missing WebGL. Use the diagnostic page and normal app controls. Do not alter browser security, install a new browser/extension, use forbidden Codex UI controls, or claim physical-device/anatomist acceptance from desktop browser success. Record the precise blocked boundary if the authorized path cannot render.
