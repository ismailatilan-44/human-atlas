# Bilateral median nerve registration — 2026-09-22

The two verified Z-Anatomy `Median nerve.l/.r` curves are exported as a separate Human Atlas extension after measuring the existing registration across the forearm and wrist. The main atlas and earlier nerve/landmark packages remain unchanged.

## Package

- `/models/extensions/median-nerves.json`, `.bin`, `.bin.gz` use the same chunk/part format as the atlas.
- Part IDs: `ZA-MED-L`, `ZA-MED-R`; concept IDs: `atlas:left-median-nerve`, `atlas:right-median-nerve`; system: `nervous`.
- 2 parts; 5,208 vertices; 10,368 triangles; 218,160 bytes raw and 119,382 bytes gzip.
- Little-endian Float32 positions, normalized Int16 normals and Uint32 indices, with 4-byte-aligned offsets and final Float32 bounds.
- Existing atlas coordinates are already applied. Consumers must not apply the registration a second time; remap extension-local chunk indexes when merging manifests.

Each curve retains its original two splines, 20 control points, bevel settings and open tube ends. The export preserves the source shape without decimation or local path editing. Separate muscular branches, palmar branches, digital branches and communicating branch objects are not included, so this package does not claim the complete median nerve branching tree.

## Why the existing transform was reused

The nerve extension's existing six-bone similarity transform maps source meter/Z-up to Human Atlas meter/Y-up. The scale remains 0.9671866615; the full unchanged 4×4 matrix is recorded in the median manifest. Before exporting, the new script measures twenty anatomically matched source/target bone pairs: bilateral radius and ulna plus all eight carpal bones on each side.

Both radii participated in the original fit and are labeled accordingly. The two ulnae and sixteen carpal bones are independent holdouts. Each statistic combines source vertices to nearest target triangles and target vertices to nearest source triangles, using every vertex. The metric is vertex-weighted, not area-weighted. It measures surface discrepancy, including source edits and target simplification, and is not a clinical accuracy bound.

| Source object | Target part | Role | RMS mm | p95 mm | Maximum mm |
|---|---|---|---:|---:|---:|
| Radius.l | FJ3277 | original_fit_reference | 0.644 | 1.207 | 1.893 |
| Ulna.l | FJ3286 | independent_holdout | 0.500 | 1.028 | 1.673 |
| Scaphoid bone.l | FJ3278 | independent_holdout | 0.540 | 0.986 | 1.262 |
| Lunate bone.l | FJ3268 | independent_holdout | 0.517 | 0.864 | 1.278 |
| Capitate bone.l | FJ3257 | independent_holdout | 0.677 | 1.207 | 2.247 |
| Hamate bone.l | FJ3261 | independent_holdout | 0.440 | 0.747 | 0.978 |
| Pisiform bone.l | FJ3276 | independent_holdout | 0.510 | 0.815 | 0.977 |
| Trapezium bone.l | FJ3283 | independent_holdout | 0.456 | 0.830 | 1.071 |
| Trapezoid bone.l | FJ3284 | independent_holdout | 0.414 | 0.790 | 1.146 |
| Triquetrum bone.l | FJ3285 | independent_holdout | 0.410 | 0.784 | 1.149 |
| Radius.r | FJ3349 | original_fit_reference | 0.608 | 1.026 | 4.037 |
| Ulna.r | FJ3391 | independent_holdout | 0.426 | 0.764 | 1.597 |
| Scaphoid bone.r | FJ3383 | independent_holdout | 0.389 | 0.655 | 0.889 |
| Lunate bone.r | FJ3374 | independent_holdout | 0.385 | 0.612 | 0.773 |
| Capitate bone.r | FJ3361 | independent_holdout | 0.422 | 0.654 | 0.850 |
| Hamate bone.r | FJ3367 | independent_holdout | 0.326 | 0.560 | 0.736 |
| Pisiform bone.r | FJ3382 | independent_holdout | 0.374 | 0.592 | 0.648 |
| Trapezium bone.r | FJ3388 | independent_holdout | 0.345 | 0.589 | 0.711 |
| Trapezoid bone.r | FJ3389 | independent_holdout | 0.301 | 0.550 | 0.735 |
| Triquetrum bone.r | FJ3390 | independent_holdout | 0.304 | 0.543 | 0.885 |

Ulna RMS is **0.426–0.500 mm**; carpal holdout RMS is **0.301–0.677 mm**, with a largest carpal local discrepancy of **2.247 mm**. Radius RMS remains **0.608–0.644 mm**; its right-side maximum is **4.037 mm**. These observations support reusing the existing rigid similarity registration through the wrist. No new forearm fit or local nerve warp was introduced.

Source bone comparisons use the authored base meshes. Lunate and pisiform objects have Subdivision display modifiers, recorded in the manifest but not applied; the other measured bones have no modifiers. The median nerve curves have no object modifiers. A broad 4 mm per-object RMS export sanity gate catches gross registration failure; it is not an anatomical acceptance threshold.

## Conversion and validation

Source SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. Blender 5.2.0 LTS opens the source with `--disable-autoexec`. The source hash is checked before any export. The selected curve objects are converted to triangle tubes. Negative object transforms have their triangle winding reversed. Vertex normals are recomputed and quantized.

Verified finite positions, nondegenerate triangles, valid indices, matching final bounds, normalized normals, consistent face/vertex normal directions and a byte-exact gzip round trip. Binary SHA-256: `889c094ea53cb1f6ae639c8164007a4bdd213c92511fab8ce013f9853e656a7f`.

Two technical QA renders were visually inspected using the actual existing atlas bone/muscle binary geometry and exported median nerve coordinates:

- [Bilateral upper arm, forearm and wrist](../../public/models/extensions/median-nerve-proof-front.png)
- [Left distal forearm and wrist detail](../../public/models/extensions/median-nerve-proof-left-wrist.png)

Both nerves follow continuous bilateral upper-limb paths and reach the wrist with no visible gross scale, axis or laterality error. The wrist detail shows the source tube in the local carpal/flexor context. These renders support technical placement review; neither bone agreement nor visual inspection establishes expert validation of the nerve course, carpal-tunnel boundaries or complete branching anatomy.

## Reproduction and provenance

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend --python scripts/export-median-nerves.py -- --render
```

Omit `-- --render` for geometry export only. The script reads the original atlas and upper-arm registration, but writes only the new median package and its optional proof images. It never saves the source blend.

The attribution append in `public/models/extensions/ATTRIBUTION.md` records the selected source objects and adaptations. Upstream's general CC BY-SA 4.0 declaration and mixed-source/object-lineage limitations remain preserved in the accompanying notices. No blanket commercial clearance or relicensing of the full source archive is asserted.
