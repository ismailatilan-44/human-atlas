# Thyroid source-reference registration — 2026-09-22

A source-authored thyroid mesh is exported as a **low-detail reference**, with a neck-specific transform and explicit unresolved anatomical-quality limits. It is technically valid geometry but should not be presented as a detailed or expert-validated thyroid model. The source form was preserved, including its conspicuously thin, stylized shape.

## Package and identity

Endpoint `/models/extensions/thyroid.json`; chunk `/models/extensions/thyroid.bin` and gzip equivalent. Part `ZA-THYROID`; concept `atlas:thyroid-gland`; display system `endocrine`. No application, graph or coverage edits are part of this export.

The package has **1,302 vertices / 2,600 triangles**, 54,636 bytes raw and 33,072 bytes gzip. It uses the existing Float32 positions / normalized Int16 normals / Uint32 indices layout. The stored coordinates are already Human Atlas meters, X left / Y superior / Z anterior.

## Source evaluation and quality

The verified source object is `Thyroid gland`, not thyroid cartilage or any parathyroid. Its base cage has **84 vertices and 68 polygons**. The export evaluates the original **Mirror → Solidify → Subdivision** stack at the source viewport subdivision level 1; the source render setting is level 2 and is recorded separately. Evaluated geometry adds smoothness, not anatomical information. No hand-authored replacement shape, scan interpretation or inferred missing lobe was added.

The final surface has two incident triangles on every edge and consistent outward normals. Its geometric enclosed volume is **4.322 cm³**; this is a property of the solidified source mesh, **not a physiological thyroid-volume estimate**. The final bounds span approximately 46.8 × 33.0 × 39.8 mm, while the thin source construction encloses much less than that bounding box.

The front and oblique views show a stylized thin form around the laryngeal region, with bilateral portions and a superior central projection. It lacks detailed, separately represented lobe/isthmus morphology. The conspicuous source simplification remains a material limitation even though triangulation and coordinate registration pass. Detailed anatomical teaching or clinical use requires a better source or expert-reviewed replacement. This export does not claim morphological validation.

## Neck registration instead of the arm transform

The prior upper-arm registration failed the nearby-reference check: hyoid/thyroid cartilage/cricoid RMS was 6.67–7.43 mm. Applying it unchanged would have carried a measurable spatial mismatch into the thyroid package.

A new labeled, bidirectional nearest-surface similarity ICP fit uses **hyoid, thyroid cartilage and cricoid cartilage**. These are fitted as distinct identities; the transform has one rotation, one uniform scale and translation, without deformation. C3–C7 vertebrae and trachea are independent holdouts. Duplicate atlas hyoid/cricoid elements were avoided by selecting explicit part IDs.

The fit uses up to 800 evenly spaced vertex indexes per direction per reference. Final metrics use all vertices against the opposite triangulated surface in both directions (vertex-weighted, not area-weighted). It converged in 35 iterations at a coefficient-change sum 9.35e-08; overall source-to-atlas uniform scale is 0.9628015284. The full matrix is in the manifest. It applies only to this thyroid export and must not replace the upper-arm transform for unrelated structures.

| Reference | Use | Prior arm RMS mm | Neck RMS mm | Neck p95 mm | Neck max mm |
|---|---|---:|---:|---:|---:|
| Hyoid bone | local_fit_reference | 7.429 | 1.135 | 2.576 | 3.185 |
| Thyroid cartilage | local_fit_reference | 6.670 | 0.695 | 1.357 | 2.493 |
| Cricoid cartilage | local_fit_reference | 6.746 | 0.526 | 1.055 | 1.251 |
| Vertebra C3 | independent_neck_holdout | 7.893 | 2.766 | 5.219 | 6.729 |
| Vertebra C4 | independent_neck_holdout | 6.600 | 2.267 | 4.586 | 5.945 |
| Vertebra C5 | independent_neck_holdout | 4.800 | 2.385 | 4.538 | 6.246 |
| Vertebra C6 | independent_neck_holdout | 4.499 | 2.773 | 4.666 | 5.891 |
| Vertebra C7 | independent_neck_holdout | 4.359 | 3.873 | 7.389 | 9.328 |
| Trachea | independent_neck_holdout | 5.636 | 2.263 | 4.928 | 6.203 |

The local laryngeal agreement improves to **0.526–1.135 mm RMS**. Trachea remains **2.263 mm RMS** and C3–C7 remain **2.27–3.87 mm RMS**, with local maxima up to 9.33 mm. These residual shape/posture differences are retained openly. This is a local source registration, not specimen identity, organ morphology validation or a clinical localization error bound. The script's 2 mm local-reference RMS guard is only a gross export sanity check.

## Visual and binary checks

The following views were inspected with the **actual target atlas** hyoid, thyroid/cricoid cartilages, C3–C7 and trachea. The thyroid is the evaluated source mesh in the new local coordinates. Registration places it in the corresponding local source-reference region without a gross axis or scale error; the thin stylized form and morphology limits remain visible.

- [Frontal thyroid/source-reference view](../../public/models/extensions/thyroid-proof-front.png)
- [Oblique thyroid/source-reference view](../../public/models/extensions/thyroid-proof-oblique.png)

Verified source SHA, finite positions, nondegenerate triangles, index range, outward face/vertex normal agreement, closed edge topology, final Float32 bounds, quantized-normal lengths and gzip round trip. Binary SHA-256: `efa9cef3553976cba5036a77e4aaee1d35319a06d63d2dcbb86d8c70229255e3`.

## Reproduction and attribution

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend --python scripts/export-thyroid.py -- --render
```

Omit `-- --render` for geometry only. The original atlas and upper-arm transform are read-only inputs; neither source blend nor earlier extension package is saved or changed. The exporter derives the thyroid's own registration each run. Source `Startup.blend` SHA-256 is `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`.

The thyroid-specific [attribution file](../../public/models/extensions/THYROID-ATTRIBUTION.md) records the source object, evaluated modifiers, adaptations and the upstream license/provenance limits. The shared extension attribution file is unchanged by this package.
