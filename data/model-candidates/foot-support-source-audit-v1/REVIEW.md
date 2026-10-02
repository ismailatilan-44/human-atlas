# Foot-support source candidate v1

On baseline revision `0a501618801a5fbc8db44599d24eb50dfde0fba4`, this bounded audit appends twenty exact bilateral support meshes to the independent 119-object lower-limb reference. The candidate contains 139 selectable records. It is source-preservation evidence, not anatomical completeness or expert acceptance. The two named intersesamoid objects have a material source-placement limitation described below; root has excluded them from the active student reference and retains them candidate-only.

## Source and identity

The source is the existing male-source intake `work/open-assets-review/Startup.blend`, SHA-256 `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`; no new source was downloaded. Blender 5.2.0 LTS opened it in background with `--disable-autoexec`; no blend was saved. Exact `.l`/`.r` names are independent MESH objects with finite evaluated selectable triangles. Their source world-X signs corroborate the named sides. All twenty are individually one connected triangle component. Text/marker companions are recorded separately in `evaluated-candidates.json` and are not exported as anatomy.

`new-object-mapping.json` preserves exact names and assigns `ZA-LLR-{SOURCE-SLUG}-L/R` parts and `zanatomy:{source-slug}-l/r` concepts. Retinacula/aponeuroses use muscular/primary roles; ligaments use skeletal/primary. No layer, fascicle, attachment, or finer component identity is invented. The source display transform is the existing single orthonormal `(x,y,z) → (x,z,-y)` rotation in metres. There is no registration, scale change, fitting, mesh translation, healing, or cross-source blend; main-atlas compatibility remains false.

| Exact base name (each .l/.r) | Evaluated vertices / triangles per side | Source evaluation and limits |
| --- | ---: | --- |
| Flexor retinaculum of ankle | 350 / 696 | Authored 1 mm Solidify |
| Superior extensor retinaculum of ankle | 132 / 260 | Authored 1 mm Solidify |
| Inferior extensor retinaculum of ankle | 160 / 316 | Authored 1 mm Solidify |
| Superior fibular retinaculum | 328 / 652 | Authored 1 mm Solidify |
| Inferior fibular retinaculum | 32 / 35 | Open source sheet, 27 boundary edges |
| Plantar aponeurosis | 240 / 406 | Open source sheet, 72 boundary edges; authored 1 mm Solidify disabled in viewport but enabled for source renders |
| Long plantar ligament | 1,741 / 3,486 | Unmodified mesh; five averaged-normal disagreements per side retained |
| Plantar calcaneocuboid ligament | 70 / 136 | Subdivision level 1 viewport / 2 render and 0.5 mm Solidify; export uses evaluated viewport |
| Plantar calcaneonavicular ligament | 18 / 32 | Subdivision level 1 viewport / 2 render and 0.5 mm Solidify; export uses evaluated viewport |
| Intersesamoid ligament | 30 / 56 | Authored 0.5 mm Solidify; source placement uncertain |

## Preservation and numerical checks

The frozen `baseline119-atlas.json` and `baseline119.bin.gz` are the reproduction baseline. The producer never uses mutable public package count or data. Baseline manifest SHA-256 is `b730ab72e709624fa08d09653209dc822ded549c885573a17026f33bc456d14b`; decompressed baseline SHA-256 is `038387150768d7c34670bdce332ad4870dc15fbcbb622c0e441ab064cc979350`.

All original 119 part records and 119 concept records are deeply identical. The full 3,442,880-byte baseline prefix is byte-identical, so all earlier position/index/normal arrays, offsets, and inherited defects remain unchanged. The twenty new meshes contribute 6,202 vertices and 12,150 triangles, for 88,532 vertices / 175,554 triangles overall. Exact source world geometry hashes agree with the separate inspection. Export positions are Float32, indices Uint32, angle-weighted normals Int16. Mirrored source-object winding is corrected without moving geometry.

Finite coordinates, index ranges, four-byte offsets, decoded bounds, normals, unique IDs, gzip round trip, expected open boundaries, and source-to-decoded arrays pass. All twenty have zero nonmanifold edges, zero zero-area triangles, zero loose vertices, no duplicate faces, and no cancelled vertex normals. The long plantar ligament has five triangles per side whose averaged vertex normal does not agree positively with the face normal; these are disclosed and retained. No geometry/normal repair was applied. No self-intersection or complete contact test is claimed.

Two final numerical runs produced byte-identical manifest, binary, gzip, attribution, and upstream license. See `acceptance-evidence.json` and `geometry-checks.json`.

| File | SHA-256 |
| --- | --- |
| atlas.json | `b5543dc45b3a897dfc2808d278b0c40d47140dc63994cfb6faafa2bdd56ce6ce` |
| anatomy.bin | `a207ccb80737956445c8966cc99d57a42dd59b30635d0178aea96e5fad97b70d` |
| anatomy.bin.gz | `fa440c9a767fa0f3affc7b286f8cfd44e39e5fde0ad47beccf0141b76a7770a8` |

Binary size is 3,700,320 bytes; gzip is 2,081,460 bytes.

## Opened visual evidence and placement finding

Five paired images were rendered and opened: anterior and lateral retinacula, plantar aponeurosis, plantar ligaments, and an intersesamoid close view. Every image puts fresh source-evaluated geometry on the left and decoded candidate geometry on the right, with common scale/view and same-source bone context. View settings and membership are in `render-evidence.json`. No gross transfer shape, position, or identity mismatch was observed. The lateral retinacula view crops some peripheral forefoot context; the support area remains visible. These are representative left-side comparisons; both sides receive numerical checks. Render-only panel separation is not an export transformation.

The intersesamoid close view prompted a separate actual-source audit (`inspect-intersesamoid.py`, `intersesamoid-placement.json`). On both sides, the named ligament's bounds overlap sesamoid component 0, while a **1.583442 mm source-X gap** separates its bounds from component 1. Sampled nearest-surface minima are approximately 0.033 mm to component 0 versus 2.698 mm from ligament vertices to component 1 (2.475 mm in the reverse vertex sample). These are vertex-sampled BVH distances, not exact contact or attachment tests. No medial/lateral component identity is inferred.

The named mesh therefore does not span both modeled sesamoid components; this concern exists in the source rather than being a projection/transfer defect. Source naming is preserved, but placement, anatomical extent and attachment/course are unaccepted. Root disposition: keep these two candidate-only; reject their connecting geometry/extent for the active student reference. Eighteen other new meshes are eligible for explicitly limited source-reference integration. No intersesamoid attachment edges should be inferred from this geometry. The other eighteen have no comparable newly established placement contradiction, but their anatomical extent and relationships also remain expert-pending.

## Reproduction and integration

Run from repository root with the pinned source:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec work/open-assets-review/Startup.blend --python data/model-candidates/foot-support-source-audit-v1/export.py -- --render
```

For numerical output elsewhere, omit `--render` and supply `--output /absolute/output/directory`. `export.py` has no import-time writes; `build_candidate(output_dir=None, render=False)` is callable with the pinned source already open. Default output and all audit evidence remain in this candidate directory. The source and frozen119 hashes are asserted. A root producer can import this module with importlib and call `build_candidate(output_dir=PUBLIC_DIR)`; it does not need to regenerate or pass the historical119 package.

The root owns public integration, metadata, browser search → selection → focus/context → relationship → return validation, deployment, and release. No browser/product/expert acceptance was performed by this geometry agent. Next action: root filters the last two intersesamoid records/binary arrays, publishes a137-object reference containing the18 eligible supports, and exercises that journey. The complete139 source candidate remains unchanged for audit. No Git staging, commit, push, or deployment was performed here. Verbose `*.log` files are local diagnostics only and must not be staged.

## Provenance and measurement

The existing intake and inherited attribution remain authoritative. `ATTRIBUTION.md` distinguishes the Z-Anatomy general CC BY-SA 4.0 notice from underlying DBCLS BodyParts3D CC BY-SA 2.1 Japan lineage and preserves separate exception notices. Specific object-author lineage is not newly resolved or legally cleared by this audit. The selected objects are not the inner-ear/kidney exceptions; full upstream notices are retained verbatim in `UPSTREAM-LICENSE.txt`.

`timing.json` records elapsed time from mapping/baseline snapshot through verification; initial instruction/state reading is excluded. The first five-view render run took 36.494 seconds within the exporter. Rework consisted of clarifying anatomical-scope wording and the targeted intersesamoid placement audit after visual review. No geometry was redrafted or repaired. Full scheduling/waiting time before the recorded start is unknown.
