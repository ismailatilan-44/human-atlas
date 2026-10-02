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

The build's `prebuild` checks the explorer projection, not whether the knowledge graph was freshly derived from its authored inputs. A successful TypeScript check or Pages deployment is not proof that anatomy tests ran. The read-only `.github/workflows/code-checks.yml` runs `npm run check:ci` on pinned Node/actions and the npm lockfile. It discovers all `scripts/*.test.mjs`, checks current projections, atlas/interactions, builds, and enforces the JS transfer budget. Pages publishing remains separate; report actual CI and deployment run evidence separately.

## Source-use for anatomy and learning decisions

Start from the approved task and its owning source records, not every available reference. For skull work, use the [research index](skull-research/README.md) to select the relevant route:

| Decision | Read first | Continue through existing ownership/checks |
| --- | --- | --- |
| Bone identity, group membership, fine-feature claim | [Current inventory and limits](skull-research/current-inventory.md) | Owning anatomy/label/coverage record; knowledge tests and relevant validators above. Whole-bone membership does not prove a landmark or canal. |
| Acquire, adapt or register an asset | [Source options and component terms](skull-research/source-options.md) | Source-intake skill, then asset-audit or imaging workflow as needed; owning intake/attribution/registration record and package checks. |
| Learning objective or answer content | [Learning content and cautions](skull-research/learning-content.md) | Owning target/content record; terminology review where needed; study checks only when study data/state changes. |
| Separation, reveal, cutting, assembly or motion | [Interaction evidence and limits](skull-research/interactions-and-pedagogy.md) | Benchmark/regional-acceptance skills as applicable; viewer/state routing above and actual browser journey below. Research priorities remain proposals. |

For other regions use their corresponding versioned records. Recheck the relevant live source/version when a decision depends on changed external terms or a newer release. A dated source claim is not a current license verification. Keep direct-source license statements separate from downstream component exceptions; preserve specimen identity, object/concept IDs, units/axes and shared coordinate conversions. Do not silently merge reference bodies or substitute viewer-code/metadata rights for geometry rights.

Use the [decision-record template](source-decision-template.md) for material choices affecting anatomical claims, source/rights/frame, or learning behavior. Put the completed entry in the existing owning review or design record; no separate ledger is required. One entry can cover a coherent package. Link only evidence relevant to the choice, record why it was chosen or why research advice was not followed, and retain unknowns. Routine styling and mechanical edits do not need this record. Updating a decision must preserve the superseded rationale where it explains current constraints.

### Lightweight review before acceptance

Use a fresh independent reviewer for a material anatomy/source/mechanism package; guidance-only changes can use a short navigation dry run. Review the relevant changed claims and source links, not the entire research library:

- Trace the decision to a source/version and locator. Separate observed geometry or behavior, source statements, inference, proposals and untested assumptions. Source-backed is **not expert-verified**; identity, placement, passage and clinical acceptance remain distinct.
- Check applicable component licenses, direct-source exceptions, attribution and reference-frame constraints against the proposed use. State unresolved rights or frame evidence instead of assuming compatibility.
- Confirm the actual behavior matches the selected learning goal and represented anatomy. A whole-bone hide is not a calvarial cut, a clip is not CT, and an educational explosion is not physiological movement. Apply these examples only where relevant.
- Select the smallest checks from the ownership table. For visible changes, exercise the relevant search → selection → focus/context → relationship → return journey, including state restoration, laterality and target screen sizes where affected. Use [existing development visual QA](development-qa.md) for its supported state/replay scenarios and the browser evidence route below; do not assume it already contains skull lessons. Record actual rendered behavior, expected/actual results, source revision and limitations. A build, DOM control, or fixture PASS alone is not visual/anatomical acceptance.

Record review findings and checks in the owning record/PR and delivery handoff. Documentation-only changes need relevant source/link/whitespace checks, not a new model test suite or fabricated browser run. No new completeness percentage, compulsory source count, generic harness, or accuracy guarantee follows from this workflow.

## Frozen activation versus reusable validation

Read a historical integration script before selecting it as a check. `scripts/integrate-foot-supports.py` activates a frozen proposal: it rejects changed records with the same identity and asserts global counts (including exactly 401 main labels). Its `--check` verifies that activation snapshot; it is not a universal validator for later label edits/additions. Do not overwrite a reviewed new record with the historical proposal or relax source evidence merely to make that script pass. For later edits use the owning current records, knowledge tests, runtime validators and inventory checks; retain/reconcile historical evidence explicitly. The same distinction applies to frozen candidate builders and later target versions.

## Browser evidence

Use an already authorized browser through its supported controls. Verify a loaded model and a visible change after selection/focus/isolation/return; a canvas element or a WebGL availability flag alone is insufficient. From the repository root, `python3 -m http.server 3018 --bind 127.0.0.1 --directory scripts` serves `http://127.0.0.1:3018/webgl-probe.html`. This exercises an actual WebGL context, draws a triangle and reads back its center pixel; the button redraws in a different color. Stop the diagnostic server after QA. It is a diagnostic page, not a product asset or anatomical acceptance test. Pair its result with screenshots of the real Atlas interaction and the served source revision.

If browser evaluation exposes only a read-only DOM proxy, canvas `getContext()` may be unavailable there; that does not establish missing WebGL. Use the diagnostic page and normal app controls. Do not alter browser security, install a new browser/extension, use forbidden Codex UI controls, or claim physical-device/anatomist acceptance from desktop browser success. Record the precise blocked boundary if the authorized path cannot render.

## Learning and saved scenes

`data/study/*.json` and `app/study-packs.ts` own finite prompt scope, IDs and evidence. Increment a pack version for semantic changes; the persisted full-pack identity also rejects changed evidence. `app/study-history.ts` owns local UTC scheduling/history; `app/saved-scenes.ts` owns validated scene persistence and manifest fingerprints. Update its semantic revision when labels/relationships change without a manifest change. Check all study/saved-scenes tests and run actual reload, cross-reference return and mobile journeys. These records never close regional expert acceptance.
