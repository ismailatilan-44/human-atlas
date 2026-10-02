# P1–P3 local implementation — 2 October 2026

Base: `2fadd79c8229d3f2b0069b6191c2000b21f6d4c2`, the P1–P7 plan produced in the Codex conversation “Human Atlas projesini incele”. Work is isolated on `codex/atlas-p1-p3` in `Documents/Codex/2026-10-02/task-2/atlas-p1-p3`. The original Desktop/atlas checkout and its untracked evidence are unchanged. No push, merge or deployment was performed. The recorded live source remains e005d53; these changes are local only.

## Delivered behavior

- P1: `app/search.ts` supplies the same Turkish/ASCII normalizer and matcher to UI and WebMCP. Normalization covers both query and index, preserving IDs and sided labels. Existing per-consumer sorting/result limits remain. Production-browser results: `sinir/SİNİR` returned the same 15 options; `biseps/BİSEPS` the same 8. Automated contracts also cover ASCII/diacritics, side and FMA ID queries.
- P2: the knowledge producer derives six `anchored_reference` records from the registered source landmark manifest. These retain zero mesh membership, point coordinates, context bone IDs, source object, evidence and limitations. The two null humeral locations remain unanchored. Explorer and agent inspection retain the representation contract; the UI exposes source limitations. All relationship qualifiers survive catalog reduction, with scope/geometry/variation/coverage/endpoint notes available in source details. Expert review remains pending.
- P2 producer repair: upper-limb reference packaging checks immutable source files plus the relevant current entity identities, existing relations and labels, rather than comparing the entire mutable main graph/labels to historical hashes. The new unrelated cord graph/labels successfully pass this check. A separately pinned semantic digest proves that the 127-object public reference changed only its producer snapshots; historical product acceptance is preserved without re-dating. Its two geometry binaries are unchanged.
- P3: exactly BP43-FJ4274/FMA45239 (left lateral cord) and BP43-FJ4275/FMA45241 (left medial cord) are in the main registry. Two TR/EN/Latin labels, three direct source-supported relationships and two versioned target bindings accompany them. The ten-piece existing left plexus selection remains unchanged. Median contribution facts remain deferred. No right-side mirroring, roots or other candidate neural objects are activated.

## Geometry and source evidence

`python3 scripts/package-left-cords.py --check` reproduces the bounded package from the immutable 26-object candidate, validating its recorded package hashes, copying each selected position/normal/index byte unchanged, and checking finite positions, indices and bounds. It contains 2 parts / 2,056 triangles. Decoded binary SHA-256: `3884338fb9a4b3ad7257d0576d5ec423aecade3a3f0096955f0ed9ee9e3e9180`.

The previous native-frame nine-bone holdout and source/decoded audit are reused because no coordinate or geometry changes were made. Original source files, IDs, authored normals, short segment scope, medial tiny speck and nonmanifold diagnostics remain. DBCLS BodyParts3D CC BY-SA 2.1 Japan attribution and verbatim captured license accompany the new package. These technical observations do not accept complete neural continuity or expert anatomy.

## Actual local verification

Environment: macOS, Node 22.23.2, Python 3.9.6, existing local dependency installation. No install, new Blender export or source download.

Passed: TypeScript; all five existing anatomy-knowledge tests; base atlas buffer validator; expanded interaction contracts including shared Turkish matching, six point representations, two null points, new cord graph scopes and unchanged ten-part plexus selection; knowledge/explorer/inventory freshness; upper-limb reference package and v2 target checks; new cord package and v3 target checks; original candidate read-only geometry and frozen metadata checks; `git diff --check`.

Production build passed with `npm run build -- --configLoader runner`. The normal command first hit a sandbox write restriction on the symlinked original node_modules/.vite-temp; the runner mode avoids that write. Vite's existing large-chunk warning remains (JS gzip about 387 KB). Vite SSR validation printed a sandbox WebSocket bind diagnostic on port 24678 but completed all assertions with exit 0; no test result is inferred from that diagnostic.

The local production dist was served only on 127.0.0.1:4317. Codex in-app browser walkthroughs actually observed:

- Main TR search equivalence above, source ID FMA45239 → left lateral cord.
- 1440×1000: lateral selection/focus, isolated visible mesh, musculocutaneous relationship → return, context visibility/transparency.
- 390×844: medial label search → selection → isolate; exact Latin name and source limitation/defect text; plexus relation → return.
- 320×568: returned medial isolated mesh visible above the scrolling detail panel; no model/panel overlap in the observed screenshot.
- 390×844: left coracoid source point → expanded source limitations; zero mesh count and disabled mesh isolation as expected.
- Switch to independent 127-object upper reference cleared prior history; main-only FMA45239 search returned no match. Return to main reloaded 2,292 pieces.
- Browser error/warning log empty. Screenshots were viewed in the tool conversation, not saved as repository image artifacts.

Counts after projection: main 2,292 parts, main graph 3,516 entities / 1,539 relations, 403 main label records. All datasets: 2,589 parts / 3,838 catalog rows / 1,677 relations. All 1,010 requirements remain; upper v3 retains 352 targets, adds two left source bindings (180 mesh observations, 164 without a positive binding, six reference-point targets, two unresolved locations). No regional completion or expert acceptance is claimed.

## Open acceptance

Live revision/hash and live-mobile checks were intentionally not run: publication is not authorized. Physical device/multitouch, anatomical expert review, complete cord course, cross-source continuity, right cords and C5–T1 contributions remain open. P4–P7 and unspecified user-observed bugs were not implemented. Competitor research is a separate task.
