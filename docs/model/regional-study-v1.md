# Right ankle-region recognition study v1 — local acceptance

## Reviewed integration baseline

Atlas project association was verified against the app registry: `8161f768-1ca7-467a-8102-ad5669942579`. This work belongs only to Atlas.

The original guidance branch tip was `29b018ea3602586a47e7948269ca44149acbaca3`, including guidance commit `0ab2c2ffa408341dd1f388be9ccccec1bcae97e8`. The separately completed P1–P3 tip was `f1b01e62984cea371ebc768ab3872bfe8ada128f`. Both descend from `2fadd79c8229d3f2b0069b6191c2000b21f6d4c2`. After inspecting ancestry and the source diff, a local fetch and two-parent merge produced `b6a756f6b2c4b005727c711fd9862e334e846400` on `codex/atlas-regional-study`. The only conflict was two new handoff sections; both were retained. Original branch tips and existing untracked QA artifacts were preserved. No remote fetch/push, external PR, remote merge or deployment was performed.

The scope plan and historical handoff record earlier releases; they do not establish the current live revision. No live revision is claimed by this work. Root AGENTS and all six repository skills were verified in Git before study edits. Regional-acceptance and term-mapping guidance informed this package.

## Selected source scope

The versioned input is [right-ankle-v1.json](../../data/study/right-ankle-v1.json). It binds nine existing `lower-limb-nerve-reference` concepts: right talus, calcaneus, navicular, cuboid, medial/intermediate/lateral cuneiform, tibia and fibula. Each has one distinct source surface, right-side metadata, verified pinned-table terminology and preserved object/evidence identifiers. UI names resolve from the existing reference labels; labels are not reauthored in the study data. This is identification of source-model surfaces, not an exam of clinical knowledge, anatomical relationships or complete regional coverage.

Selection is a bounded subset of the [lower-limb v4 target inventory](lower-limb-targets-v4.md); no regional acceptance cell changes. Source geometry remains in its independent coordinate frame, unchanged. The [original reference audit](lower-limb-nerve-reference-review.md) discloses fibula unused vertices and a tiny calcaneal normal defect; these do not create an ambiguous structure identity and are not silently repaired. Compound sesamoids, digit-specific unresolved terms, rejected intersesamoid geometry and partial nerves are excluded. No relationships are scored. Anatomical expert review remains pending. The existing [component attribution](../../public/models/lower-limb-nerve-reference/ATTRIBUTION.md) remains separate and accessible in inspection/feedback.

## Behavior and state boundaries

From the current explorer choose the lower-limb reference, then the nine-bone study button. Nine inspection steps reuse the renderer's focus, ghost context and isolation. Recall asks for the highlighted bone using searchable source-derived name choices. Correct/wrong/skip feedback reveals the source name and evidence. Summary records first-attempt correct/skip and per-item outcomes separately from eventual success; retry queues contain only items not yet correct, and further retries cannot rewrite first attempts.

Scene tooltips, explorer labels/search/details, and agent selection tools are suppressed during study. Answer choices are visible, but no target-specific label/ID/provenance is exposed before submission. Normal render picking is disabled for study so incidental taps do not replace the target. Orbit/zoom remain available. Context uses existing skeletal surfaces; no geometry or camera engine is replaced.

Exit restores the saved scene, selection, panel state, camera pose and original Back history. Automatic rotation is stopped on return. Restart discards progress and starts inspection at item 1. A page refresh ends the memory-only session and loads the normal main-reference initial state; tab switching without reload leaves the session in memory. There is no persistence/account/backend/scheduling model. The UI explains the reset boundary. Search uses the shared Turkish/ASCII matcher.

## Checks actually run

macOS; Node `v22.23.2`, Python `3.9.6`; existing dependencies, no install.

- `npm run check` passed.
- `node --test scripts/anatomy-knowledge.test.mjs` passed all five tests on the combined baseline.
- `node --test scripts/study-session.test.mjs` passed two tests: all nine identity/geometry/label/evidence bindings; wrong/skip/correct/repeated submit, immutable first score, multiple retry rounds and clean restart. The first harness run used TypeScript's old default transpilation target and mishandled Set spread; its explicit ES2022 target corrected the harness, then both tests passed.
- `node scripts/validate-atlas.mjs` passed on the integrated geometry baseline; study adds no geometry.
- `node scripts/validate-interactions.mjs` passed baseline and final UI contracts.
- Knowledge, explorer and model-inventory `--check` passed. Inventory was regenerated only for its consumed `app/anatomy.ts` fingerprint; counts remain 2,589 packaged assets / 3,838 catalog records, zero expert-accepted targets.
- Left-cord package, left-cord v3 target, upper-limb reference package and upper-limb v2 target `--check` passed.
- `npm run build` passed; existing large-JS warning remains (about 390 KB gzip). Vite-backed validators emitted a sandbox WebSocket bind diagnostic at port 24678 but completed assertions with exit 0; this is recorded separately from browser rendering.
- `git diff --check` passed.

## Actual browser observations

The authorized macOS Chrome route rendered the actual local Atlas at port 3016; server working directory was checked against the integration checkout. QA exercised this checkout's study changes, not the earlier deployed product. No browser settings changed. Browser error/warning log was empty.

- Desktop (1710×951): nine inspection steps; source object/TA2 provenance disclosure; highlighted ghost context and isolated surfaces visibly rendered. Recall removed target heading/provenance. One wrong, one skip and seven correct answers yielded 7/9 first score and 7/9 eventual success.
- 390×844: ASCII `asik` narrowed choices to the right talus label. Two retries reached 9/9 eventual success while first score stayed 7/9 and skip stayed 1. Finish restored explorer. Source skeleton context and isolated target were visibly inspected.
- 320×568: selected geometry remained above the scrolling study panel; all nine inspection steps, recall, repeated answer click (one submission), restart and exit worked. Lower actions are reached by panel scroll. An initial entry placement overlapped explorer metadata; moving it above the bottom dock fixed the observed overlap.
- An existing isolated **left** talus selection was preserved across a right-side study interruption. Exit restored the prior left surface/camera, and explorer Back restored its earlier context/details history.
- Refresh during an active study ended the session, cleared its history and returned to the normal main-reference start without browser errors.

Screenshots are under [regional-study-v1](../../output/playwright/regional-study-v1/). They are local browser evidence, not physical-device or anatomical acceptance. No physical touchscreen, real multitouch or anatomist test was performed.

## Remaining boundaries and one next package

The exercise is Turkish-first, nine source-model bones with source English/Latin shown during inspection; no whole-region syllabus or randomized/adaptive scheduling is claimed. Coarse source geometry, physical-device performance and expert anatomical review remain open. Unspecified user-observed bugs remain separate. The next bounded package should be a learner/anatomist review of these nine prompts and camera views before adding another study region; no publication is included in this authorization.
