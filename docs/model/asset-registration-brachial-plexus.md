# Brachial plexus source components — 2026-09-22

The **active package exports 20 source curves**, ten per side: three trunks, six divisions and posterior cord. **Both root bundles are excluded** after spline-level source review found an additional superior branch of unresolved anatomical identity. This remains a partial source reference with limited neck/shoulder registration; it is not a complete plexus.

## Active package and identities

`/models/extensions/brachial-plexus.json`, `.bin` and `.bin.gz` use the existing atlas extension layout. Final counts: **20 parts / 23 concepts**, **3,984 vertices / 7,488 triangles**, 161,568 bytes raw and 71,066 bytes gzip.

Aggregate concepts `atlas:brachial-plexus`, `atlas:left-brachial-plexus` and `atlas:right-brachial-plexus` remain partial and contain only active source parts. **There are no empty root concepts or root part IDs in this manifest.** Left part/concept IDs are listed below; right counterparts replace `-L` with `-R` and `atlas:left-` with `atlas:right-`.

| Source object | Part ID | Concept ID |
|---|---|---|
| Superior trunk of brachial plexus.l | ZA-BP-SUP-TRUNK-L | atlas:left-brachial-plexus-superior-trunk |
| Middle trunk of brachial plexus.l | ZA-BP-MID-TRUNK-L | atlas:left-brachial-plexus-middle-trunk |
| Inferior trunk of brachial plexus.l | ZA-BP-INF-TRUNK-L | atlas:left-brachial-plexus-inferior-trunk |
| Anterior division of superior trunk of brachial plexus.l | ZA-BP-SUP-ANT-DIV-L | atlas:left-brachial-plexus-superior-anterior-division |
| Anterior division of middle trunk of brachial plexus.l | ZA-BP-MID-ANT-DIV-L | atlas:left-brachial-plexus-middle-anterior-division |
| Anterior division of inferior trunk of brachial plexus.l | ZA-BP-INF-ANT-DIV-L | atlas:left-brachial-plexus-inferior-anterior-division |
| Posterior division of superior trunk of brachial plexus.l | ZA-BP-SUP-POST-DIV-L | atlas:left-brachial-plexus-superior-posterior-division |
| Posterior division of middle trunk of brachial plexus.l | ZA-BP-MID-POST-DIV-L | atlas:left-brachial-plexus-middle-posterior-division |
| Posterior division of inferior trunk of brachial plexus.l | ZA-BP-INF-POST-DIV-L | atlas:left-brachial-plexus-inferior-posterior-division |
| Posterior cord of brachial plexus.l | ZA-BP-POST-CORD-L | atlas:left-brachial-plexus-posterior-cord |

Coordinates already use atlas meters / X left / Y superior / Z anterior. Do not apply the registration again. Each part records `partial_source_reference`, `limited_neck_shoulder_alignment` and expert review pending.

## Actual coverage and omissions

Each active side contains three named trunk curves, the anterior/posterior divisions of each trunk, and the named posterior cord. No separate medial or lateral cord curve was found. Root bundles are excluded in full; neither their five main branches nor their superior extra branch is relabeled from geometric topology. Existing median and musculocutaneous source objects are not duplicated. Other terminal/collateral branches are outside this package.

The exact retained source spline shapes, bevel settings and endpoints remain unchanged. No missing root, cord or connection was drawn, deformed, welded or snapped into place. Proximity in the render is not verified anatomical connectivity.

## Regional registration checks

The existing upper-arm similarity frame preserves source-coordinate consistency with existing median/musculocutaneous meshes. Independent C5–T1, clavicle and first-rib checks reveal significant residuals. A second similarity fit to those eight references was tested and rejected: it improves thoracic-inlet alignment but worsens both humeri/scapulae and displaces source neural pieces from the existing nerve frame. Both matrices and measurements remain in the manifest.

| Source reference | Original role | Retained RMS mm | Alternative RMS mm | Retained max mm |
|---|---|---:|---:|---:|
| Vertebra C5 | independent_regional_holdout | 4.800 | 3.029 | 11.824 |
| Vertebra C6 | independent_regional_holdout | 4.499 | 2.432 | 9.498 |
| Vertebra C7 | independent_regional_holdout | 4.359 | 1.339 | 9.719 |
| Vertebra T1 | independent_regional_holdout | 4.309 | 1.332 | 8.228 |
| Clavicle.l | independent_regional_holdout | 4.761 | 3.998 | 12.855 |
| Clavicle.r | independent_regional_holdout | 4.664 | 4.015 | 12.930 |
| First rib.l | independent_regional_holdout | 8.433 | 1.946 | 12.034 |
| First rib.r | independent_regional_holdout | 8.313 | 1.894 | 12.115 |
| Scapula.l | original_fit_reference | 1.845 | 5.207 | 7.608 |
| Scapula.r | original_fit_reference | 1.846 | 5.510 | 7.663 |
| Humerus.l | original_fit_reference | 0.636 | 6.440 | 1.785 |
| Humerus.r | original_fit_reference | 0.615 | 6.356 | 1.705 |

Retained C5–T1/clavicle RMS is **4.31–4.80 mm**, first-rib RMS **8.31–8.43 mm**. The alternative improves C7/T1 and first ribs to **1.33–1.95 mm**, but worsens humeri to **6.36–6.44 mm** and scapulae to **5.21–5.51 mm**. The retained matrix is a qualified source-frame choice; precise regional anatomical registration remains unresolved. Excluding roots addresses the source-identity uncertainty; it does not erase the measured regional errors.

Metrics combine all source vertices to nearest target triangles and all target vertices to nearest source triangles, vertex-weighted rather than area-weighted. The trial ICP samples up to 500 vertices per direction/reference. Shape differences, posture and target simplification contribute; these are not clinical error bounds.

## Root spline review

The root object name alone does **not** establish a pure C5–T1 geometry. Both `Roots of brachial plexus.l/.r` contain ten Bezier splines and 26 control points, but isolated conversion shows only splines **0–6** produce tubes. Splines **7–9** each contain one point and produce **zero vertices/triangles**.

The five main geometric paths, indexes **0–4**, end exactly at the source superior/middle/inferior trunk start points: **0/1 → superior; 2 → middle; 3/4 → inferior**. Index **5** is a higher branch whose medial point lies in the source C3/C4 surface neighborhood; index **6** connects an internal point of 5 to an internal point of 0. This could reflect an intended superior cervical contribution/variant or extra/mislabeled source geometry; the available object names and spline data do not resolve that interpretation. **No C5–T1 per-spline anatomical identities are inferred.**

All measurements below use the original Blender world coordinates **before any atlas registration**: X left, Y posterior, Z superior, meters. Source bone Z bounds and mean Z values are geometric references, not anatomical exit-level boundaries; the bone bounds overlap because each includes processes and other surfaces. C1–T1 were requested, and T2 was added to bound the lowest path.

| Source bone | Minimum Z m | Maximum Z m | Mean vertex Z m |
|---|---:|---:|---:|
| Atlas (C1) | 1.533108 | 1.552756 | 1.542525 |
| Axis (C2) | 1.508525 | 1.551435 | 1.525485 |
| Vertebra C3 | 1.493055 | 1.519706 | 1.508884 |
| Vertebra C4 | 1.480555 | 1.505595 | 1.493932 |
| Vertebra C5 | 1.468895 | 1.491394 | 1.479040 |
| Vertebra C6 | 1.453726 | 1.478326 | 1.464363 |
| Vertebra C7 | 1.438514 | 1.465527 | 1.451366 |
| Vertebra T1 | 1.422607 | 1.453380 | 1.438001 |
| Vertebra T2 | 1.402554 | 1.437572 | 1.421865 |

The following table uses the control point nearest the midline for each left spline. The right-side positions mirror these within 0.00024 mm (including the one-point remnant); counts and endpoint topology agree bilaterally. Nearest-bone distances are point-to-source-triangle distances and do not assign a nerve level.

| Spline index | Points | Generated vertices/triangles | Medial control point X,Y,Z m | Two nearest source bones | Observed source topology |
|---:|---:|---:|---|---|---|
| 0 | 4 | 444/864 | 0.013352, 0.015897, 1.489802 | Vertebra C4 (2.446 mm); Vertebra C5 (2.882 mm) | Ends at superior trunk; shares its end with spline 1 |
| 1 | 3 | 300/576 | 0.017300, 0.016809, 1.473072 | Vertebra C6 (3.410 mm); Vertebra C5 (5.438 mm) | Ends at superior trunk; shares its end with spline 0 |
| 2 | 3 | 300/576 | 0.015499, 0.022703, 1.458269 | Vertebra C7 (2.002 mm); Vertebra C6 (5.114 mm) | Ends at middle trunk |
| 3 | 4 | 444/864 | 0.014420, 0.028537, 1.448491 | Vertebra C7 (2.100 mm); Vertebra T1 (2.910 mm) | Ends at inferior trunk; shares its end with spline 4 |
| 4 | 4 | 444/864 | 0.013899, 0.034661, 1.434501 | Vertebra T1 (2.183 mm); Vertebra T2 (3.084 mm) | Ends at inferior trunk; shares its end with spline 3 |
| 5 | 3 | 300/576 | 0.013461, 0.015698, 1.504371 | Vertebra C4 (2.469 mm); Vertebra C3 (2.660 mm) | Additional superior branch; anatomical identity unverified |
| 6 | 2 | 156/288 | 0.024387, 0.008383, 1.498367 | Vertebra C4 (2.747 mm); Vertebra C3 (5.239 mm) | Connects an internal point of spline 5 to an internal point of spline 0 |
| 7 | 1 | 0/0 | 0.266043, -0.044215, 0.777242 | Vertebra T2 (680.208 mm); Vertebra T1 (697.465 mm) | Single-point remnant near distal upper limb; no mesh |
| 8 | 1 | 0/0 | 0.013461, 0.015698, 1.504370 | Vertebra C4 (2.469 mm); Vertebra C3 (2.660 mm) | Single-point duplicate of spline 5 proximal point; no mesh |
| 9 | 1 | 0/0 | 0.013352, 0.015897, 1.489802 | Vertebra C4 (2.446 mm); Vertebra C5 (2.882 mm) | Single-point duplicate of spline 0 proximal point; no mesh |

Spline 5's medial source point Z is **1.504373 m**, versus the main path 0's **1.489798 m**: the additional branch is about **14.6 mm superior** at its medial end. The source nearest surfaces are C4 (2.469 mm) and C3 (2.660 mm), not an independently labeled C5 root. There is no comparable tube extending to source C1/C2 in this object. The initial overview rendered only C5–T1 bones, omitting C3/C4; that limited context further exaggerated the appearance of a floating superior branch. Neither observation validates the extra branch's identity.

**Decision:** both root objects are withheld from the active package. Their geometry is not partially trimmed and renamed. The source findings are preserved in manifest `coverage.unresolved`, `excludedSourceObjects` and `excludedRootSplineReview`. Future inclusion requires source/anatomical identity review, not a guessed transform or a drawn replacement.

## Visual and binary verification

The active 20-part frontal and left-oblique renders were regenerated and inspected with actual atlas bones/arteries and the existing median/musculocutaneous packages. Gold is active new geometry, blue is existing nerve geometry. The root fan is absent; the three source trunks remain visibly proximal-ended, honestly reflecting missing roots.

- [Active 20-part frontal view](../../public/models/extensions/brachial-plexus-proof-front.png)
- [Active 20-part left-oblique view](../../public/models/extensions/brachial-plexus-proof-left-oblique.png)

Earlier 22-part views are retained **only as rejected-root review evidence**, not as the current package preview:

- [Earlier view with excluded roots, frontal](../../public/models/extensions/brachial-plexus-review-with-roots-front.png)
- [Earlier view with excluded roots, oblique](../../public/models/extensions/brachial-plexus-review-with-roots-left-oblique.png)

Verified finite positions, nondegenerate triangles, indices, final Float32 bounds, normalized Int16 normals, face/vertex orientation, gzip round trip, unique part/concept IDs and no existing source-object duplication. Active binary SHA-256: `6362fdadd4b35762e4b7a12ce91729fe24ae26248bd419a4dc29df177954681f`.

## Reproduce and provenance

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend --python scripts/export-brachial-plexus.py -- --render
```

Omit `-- --render` for data only. The default exporter selects the 20 active curves and never creates root concepts. The verified source SHA is `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`; root spline indexes refer to this exact file. The source blend, main atlas, earlier nerve packages, application, registry and graph remain unchanged.

[Separate brachial-plexus attribution](../../public/models/extensions/BRACHIAL-PLEXUS-ATTRIBUTION.md) retains source identity, adaptations and upstream license/provenance limitations.
