# Main-body lower-limb label delivery — 2 October 2026

Base revision `e879fc92e1bfa6226898d12cdca2863e365858e0`. This bounded delivery adds 34 missing main-body TR/EN/LA label records: bilateral nine bones, five muscles and three artery terms. Ten existing records remain. All 44 main-body target representations in the retained [target snapshot](target-snapshot.json) now have the three display languages. This is not complete atlas translation, a formal TA2/FMA crosswalk or anatomical expert acceptance.

[proposal.json](proposal.json) and [source-evidence.json](source-evidence.json) retain exact TA2 numeric row/English/Latin pairs, source concept names/membership, each component's identity/bounds, laterality and the input hashes. Thirty-four directly corresponding primary source part IDs are label aliases; other branches in arterial aggregates are not given the trunk name. Source manifest/geometry/knowledge graph stay unchanged. Turkish translation is editorial; expert review remains pending.

The anterior tibial selection contains four source surfaces, including dorsalis pedis, arcuate and lateral tarsal arteries. The posterior tibial selection contains five, including plantar arteries/arch. Labels expose this scope instead of claiming trunk-only geometry. Popliteal selection is one source surface. The old base fibular-artery identity discrepancy remains separate and is not silently corrected by these labels.

```sh
python3 data/model-candidates/lower-limb-main-labels/build-proposal.py --check
```

Regenerate with no flag. `--apply` applies the reviewed proposal idempotently and rejects conflicting existing labels. The fixed pre-integration target snapshot avoids redefining this audit when the broader target seed gains reference bindings. Checks cover exact source identity/membership, TA2 locator, side/bounds corroboration, 34 unique label records/direct aliases and all 44 labeled representations. They do not inspect target anatomy or mesh shape.

TypeScript and interaction checks passed in the integration task. Real 1440×1000 Chromium search `sol kayik` returned the left single-surface navicular; isolation displayed `Os naviculare (L)` with the preserved source geometry. [Screen evidence](../../../output/playwright/lower-limb-main-navicular-latin.png). See the [owning report](../../../docs/model/progress-report-2026-10-02.md) for final revision/live acceptance. Total active authoring time was not instrumented; expert review remains open. Next: extend individually enumerated foot targets and source-backed labels/relationships without turning these 44 records into a whole-body denominator.
