# Lower-limb unbound-source audit and 87-object package

On 2 October 2026, all **18 targets unbound in the seed at revision `e879fc92e1bfa6226898d12cdca2863e365858e0`** were found as independent, selectable evaluated source objects in the pinned `Startup.blend`. This source audit subsequently became an authorized extension of the independent reference: **87 objects = 16 nerve curves + 2 artery curves + 6 ligament surfaces + 63 bone surfaces**. This is source preservation and technical availability, not anatomical acceptance or complete lower-limb coverage.

## Actual source and bounded search

Source: [Z-Anatomy/Models-of-human-anatomy](https://github.com/Z-Anatomy/Models-of-human-anatomy), archive member `Z-Anatomy/Startup.blend`, acquired 8 September 2026 per the existing repository intake. The inspected file SHA-256 is `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. No new download, upstream revision verification or license clearance was performed. The intake identifies the reference as male; donor-specific details remain unavailable.

`inspect.py` scans all source object names, datablock names, readable font text and collection names for fibular/peroneal/peroneus, sural, plantar and ankle-ligament terms. `discovery.json` distinguishes direct object/data/text matches from collection-only matches and includes marker/text alternatives. Some unrelated source font bodies have invalid UTF-8; their names are recorded under `textReadErrors`. Exact target object lookup, evaluated geometry and side checks do not depend on those text bodies. The unrelated oesophagus/profile dependency-cycle warning recurred. Neither issue prevented reading these targets.

Blender 5.2.0 LTS ran with `--disable-autoexec`; embedded source scripts were skipped and the source file was never saved. Source names are exact identifiers within the pinned file, not asserted FMA identifiers. TA2 target correspondence is a named candidate identity requiring expert review; a collection membership does not prove a relationship.

## Eighteen primary objects

Every table row represents two separate objects, with exact source suffixes `.l` and `.r`. Each side is corroborated by all evaluated vertices lying on the expected source-world X side. Counts are **per side**.

| Exact source base name | Source type and authored scope | Evaluated vertices / triangles |
| --- | --- | ---: |
| Deep fibular nerve | CURVE; 1 Bezier spline, 16 control points | 2,172 / 4,320 |
| Superficial fibular nerve | CURVE; 1 spline, 12 points | 1,596 / 3,168 |
| Sural nerve | CURVE; 3 splines, 10 + 4 + 3 points; 3 tube components | 2,052 / 4,032 |
| Medial plantar nerve | CURVE; 3 splines, 4 + 1 + 2 points; only 2 tube components | 600 / 1,152 |
| Lateral plantar nerve | CURVE; 1 spline, 5 points | 588 / 1,152 |
| Fibular artery | CURVE; 5 splines, 13 + 3 + 4 + 3 + 4 points | 3,228 / 6,336 |
| Anterior talofibular ligament | MESH; authored single quad, Subdivision + Solidify | 18 / 32 |
| Posterior talofibular ligament | MESH; authored single quad, Subdivision + Solidify | 18 / 32 |
| Calcaneofibular ligament | MESH; authored single quad, Subdivision + Solidify | 18 / 32 |

Full matrices, bounds, dimensions, geometry hashes, materials/modifiers and spline control/radius data are in `evaluated-candidates.json` and the public manifest. Source unit system is meters; all export objects receive only `(x,y,z) → (x,z,-y)`. No fitting, scale change, translation or independent movement is applied to packaged objects. QA panel offsets are solely render layout.

The medial plantar one-point spline produces **no surface**. Its authored point/handles/radius remain in metadata with `evaluatedRepresentation: authored-point-only-no-surface`; no tube is invented. Other splines remain separate open tubes, including variable arterial radii. Multiple splines are not independently verified named branches. All 18 evaluated candidates have no zero-area triangles, loose vertices or nonmanifold edges; curve boundaries remain open, with 24 edges per actual open tube. Each ligament is a coarse authored ribbon with 0.5 mm Solidify thickness and viewport Subdivision level 1; render level 2 is recorded but is not silently substituted. Fine attachment or fascicular detail is not claimed.

Observed extent is limited: superficial fibular objects end above the foot, medial/lateral plantar objects represent short proximal plantar courses, and separate muscular/digital branches remain outside this package. The fibular artery's five authored splines do not establish complete arterial territory or all named branch identities. There are no whole-atlas absence claims.

## Forty-eight additional foot context objects

`foot-context.json` records 48 evaluated bone objects with exact names, transforms, bounds, polygon/triangle counts and topology checks. They comprise bilateral:

- `Navicular bone`, `Cuboid bone`, `Medial cuneiform bone`, `Intermediate cuneiform bone`, `Lateral cuneiform bone` (10 objects).
- `First` through `Fifth metatarsal bone` (10 objects).
- `Proximal phalanx of {first,second,third,fourth,fifth} finger of foot`, `Middle phalanx of {second,third,fourth,fifth} finger of foot`, and `Distal phalanx of {first,second,third,fourth,fifth} finger of foot` (28 objects).

Every object has `.l`/`.r` suffixes. Source “finger of foot” wording is retained in source and stable IDs; the display alias says “toe.” Opposite-side objects and `.i/.j` marker / `.s/.t` text companions are recorded as related source objects, not interchangeable geometry aliases. No new anatomy is inferred from their presence. All 48 have nonempty evaluated meshes, corroborated laterality, and no zero-area triangles, loose vertices or nonmanifold edges. They total 13,594 vertices / 26,996 triangles. Existing talus/calcaneus reference geometry is retained rather than independently re-exported as another identity.

The exact 66 new part/concept/source mappings are in `new-object-mapping.json`. Nerve/artery/ligament concepts use `atlas:left/right-{name}`; context bones use source-preserving `zanatomy:{name}-{l/r}`. The source roles remain explicit: nerve→nervous/primary, artery→arterial/primary, ligament→skeletal/primary and bone→skeletal/context.

## Package checks and disclosed defects

The public package remains at `public/models/lower-limb-nerve-reference/`, with `compatibleWithMainAtlas:false` and `atlasRegistration:null`. `scripts/export-lower-limb-reference.py` writes current checks/renders here and preserves the historical 21-object candidate evidence directory.

| Property | Final value |
| --- | --- |
| Parts / vertices / triangles | 87 / 63,282 / 125,372 |
| Binary / gzip bytes | 2,643,600 / 1,462,468 |
| Binary SHA-256 | `572a92f6c7f630c226e70fd5e02d93db70714c063c8fd493d4eaa4c87472ca56` |
| Gzip SHA-256 | `a0b631ca5621957160d00427e2b7e9dfe64eea5e1b1901cbd405d98b99c01865` |
| Manifest SHA-256 | `a9b76a85da63937bd3c34230c902457d330cec7b75ab6df41c3db9b1cd8154ed` |

Checks passed for source identity/hash; finite decoded positions; index bounds; four-byte offsets; normalized encoded normals; exact decoded indices; Float32 position equality to rotated source evaluation; nonzero triangle areas; and gzip roundtrip. All 63 position/normal/index array hashes from the previous 21 objects match `baseline-21-array-hashes.json` byte-for-byte. The final render-producing export and subsequent numerical-only export reproduced the three listed hashes. `geometry-checks.json` and `acceptance-evidence.json` retain the results.

Known original fibular loose vertices, calcaneal local normal disagreements and sacral topology/normal defects remain. Eight new bone objects have local nonpositive averaged vertex-normal agreement: each fourth metatarsal has 3 affected triangles; each medial cuneiform, lateral cuneiform and third-toe middle phalanx has 1. These source faces are preserved and disclosed. No new loose/nonmanifold or cancelling-normal defect occurs among the 66 additions. All new nerve/artery/ligament objects have positive averaged normal agreement. No source triangle deletion, capping, welding, synthetic connections or local shape repair occurred. No self-intersection or anatomical expert acceptance is implied.

## Visual evidence and acceptance boundary

The source-only inspection renders (`left-leg-anterior.png`, `left-foot-plantar.png`, `left-ankle-lateral-ligaments.png`) were opened. Final source/decoded comparisons were also opened and inspected:

- `source-decoded-foot-anterior.png`: source left, decoded right; lower-leg nerve/artery courses and foot context.
- `source-decoded-foot-plantar.png`: source left, decoded right; both plantar nerve objects against foot bones, with proximal objects hidden to avoid projection clutter.
- `decoded-ankle-ligaments-lateral.png`: decoded ankle context and ligament sheets.

The decoded panel reads encoded positions, indices and Int16 normals. Both paired views use matching scale/direction and show no gross side, frame, missing-object or course mismatch. The limited plantar extent and coarse ligament ribbons remain visible. The first comparison attempt had cropped/off-center panels and excess proximal clutter; camera framing and visibility were corrected, with package geometry unchanged. These views are technical source-preservation evidence. Browser search/selection/focus/relationships/return, mobile acceptance, deployed revision and named anatomical review remain integration responsibilities. Expert review is pending.

## Intake, reproduction and next action

General Z-Anatomy CC BY-SA 4.0 / Gauthier Kervyn attribution and underlying BodyParts3D–DBCLS CC BY-SA 2.1 Japan / Kousaku Okubo notice remain separate in the public and audit attribution files. Original upstream notices include inner-ear/kidney exceptions; those groups are excluded. Object-specific lineage remains unresolved. Local inspection, derivative export and product integration are distinct statuses; this task preserves existing notices and does not assert new blanket redistribution/commercial clearance.

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python data/model-candidates/lower-limb-unbound-source-audit/inspect.py -- --render

/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python scripts/export-lower-limb-reference.py -- --render
```

Inspection script scope is fixed to the nine bilateral TA2 target terms, so later representation bindings do not change the audit's target set. The measured inspection/render Python run took 26.82 seconds (excluding Blender startup and conversational review); full task elapsed time was not instrumented and is unknown. Rework: invalid unrelated source font text needed a recorded decode-error guard; one-point medial plantar splines required a more precise tube-boundary check; render framing was corrected. No Git mutation, app/label/target changes or deployment was performed by this task.

Next action: integrate dataset-scoped metadata for all 87 objects and exercise the full source-reference product journey while keeping the same-frame and anatomical-review limits visible.

## Integration and technical release acceptance — 2 October 2026

Root integrated all 87 dataset-scoped TR/EN labels, 53 exact Latin labels and 12 sourced branch relationships; 34 digit-specific Latin labels remain unresolved. Source commit `1fbaeac664282f4c6314357b4eda5e5a106e9144` is deployed, static commit `1a83345c9c6ee8c954cbf742a9af3d4e9bffa47c`, successful [Pages run #36989651012](https://github.com/ismailatilan-44/human-atlas/actions/runs/36989651012). Live release metadata matched the source revision. Local desktop/two mobile flows and live 390×844 artery selection/context, deep→common→superficial fibular navigation, Latin isolation and source citation were inspected; live console had no errors/warnings. TypeScript, interaction validation, generated target/inventory checks and production build passed. Complete revision/environment/evidence and measured wall time are in the [owning report](../../../docs/model/progress-report-2026-10-02.md).

This closes technical reference integration, not anatomical expert or whole-region acceptance. Coarse ligament geometry, partial nerve/artery courses, preserved bone defects and main-frame incompatibility remain. Next: enumerate individual digit/segment targets for existing foot context and review sourced bone/ligament relationships. Earlier task-owner integration-pending text is historical evidence.
