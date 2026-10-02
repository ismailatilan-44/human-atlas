# Distal leg nerves: source package and rejected main-atlas registration

Audit date: 2026-10-02. **The sciatic transform is inadequate at the ankle. This package remains inactive in the main atlas.** Four real source curves are preserved as an independently reviewable matched-source candidate; no new viewer reference, shared model registry, graph, labels, or coverage changes are made by this exporter. Anatomical expert review remains pending.

## Deliverables and identifiers

`data/model-candidates/distal-leg-nerves/source-reference.json/.bin/.bin.gz` contains 14 selectable source objects: bilateral tibial and common fibular nerve curves, with bilateral tibia, fibula, patella, talus, and calcaneus context. It declares `datasetId: distal-leg-nerves-source-reference`, `compatibleWithMainAtlas:false`, `atlasRegistration:null`, and inactive candidate status. All objects receive only one common orthonormal display-axis rotation: source (X left, Y posterior, Z superior) → display (X left, Y superior, Z anterior), in meters. No fitting, scale change, translation, path edit, or independent object movement is applied. The original source world bounds, object names, datablocks, transforms, materials, and collection membership remain in the manifest.

`public/models/extensions/distal-leg-nerves.json/.bin/.bin.gz` is the **rejected sciatic-frame diagnostic**, retained to reproduce the failed fit. It explicitly declares `compatibleWithMainAtlas:false` and `releaseStatus:inactive-registration-rejected`; its presence under extensions is not authorization to register it. The source reference is separate from this diagnostic.

| Source object | Part ID | Concept ID | Splines / control points | Vertices / triangles |
| --- | --- | --- | --- | --- |
| Tibial nerve.l | ZA-TIB-L | atlas:left-tibial-nerve | 1 Bezier / 10 | 1308 / 2592 |
| Tibial nerve.r | ZA-TIB-R | atlas:right-tibial-nerve | 1 Bezier / 10 | 1308 / 2592 |
| Common fibular nerve.l | ZA-CFIB-L | atlas:left-common-fibular-nerve | 1 Bezier / 8 | 1020 / 2016 |
| Common fibular nerve.r | ZA-CFIB-R | atlas:right-common-fibular-nerve | 1 Bezier / 8 | 1020 / 2016 |

All four use source bevel depth ~0.0005 m, bevel resolution 4, resolution_u 12, and open ends. Tibial control-point radii range 1–4; common fibular radii are 1. No fixed-radius replacement tubes were drawn. The left source world determinant is negative; winding is corrected before export. Laterality is corroborated by source-world X and retained after the display rotation. Original world control points, Bezier handles, handle types and point radii are recorded.

The proximal control endpoint of every curve matches the corresponding source sciatic distal endpoint within 0.00019 mm after the shared sciatic transform. This is source continuity evidence, not a statement of anatomical precision. In that diagnostic frame, tibial endpoints extend from Y≈0.560 m to Y≈0.069 m; common fibular endpoints from Y≈0.560 m to Y≈0.402 m. The four complete named source objects are exported. Separate deep and superficial fibular, plantar, sural, muscular and digital branch objects are excluded. No claim of full distal innervation, plexus/root coverage or source branch correctness is made.

## Independent placement audit

The exact uniform sciatic registration matrix was tested, not assumed adequate. It is recorded with its source manifest SHA in `registration-report.json`. This run does not fit or optimize that matrix. Measurements compare each matching source and target reference on both sides: every vertex to the opposite triangle surface, in both directions, vertex-weighted rather than area-weighted. Femora are an overlap check with the earlier sciatic fit; tibia/fibula/patella/talus/calcaneus and calf muscles independently test the new distal region. Measurement bands are knee Y=.38–.58m, calf=.12–.38m, ankle/foot=-.05–.12m; these bands are not anatomical segmentation.

| Reference | RMS mm | p95 mm | Maximum mm |
| --- | ---: | ---: | ---: |
| Femur.l | 2.705 | 5.507 | 7.926 |
| Femur.r | 2.673 | 5.474 | 7.849 |
| Tibia.l | 6.535 | 14.642 | 21.217 |
| Tibia.r | 6.467 | 14.688 | 21.265 |
| Fibula.l | 9.581 | 19.869 | 25.147 |
| Fibula.r | 9.276 | 19.632 | 25.135 |
| Patella.l | 4.824 | 8.880 | 9.940 |
| Patella.r | 4.876 | 8.755 | 9.838 |
| Talus.l | 11.863 | 20.839 | 25.152 |
| Talus.r | 11.745 | 20.831 | 24.922 |
| Calcaneus.l | 10.500 | 20.606 | 25.777 |
| Calcaneus.r | 10.279 | 20.579 | 25.760 |
| Medial head of gastrocnemius.l | 9.347 | 19.054 | 24.486 |
| Medial head of gastrocnemius.r | 9.145 | 18.697 | 24.159 |
| Soleus muscle.l | 8.478 | 16.063 | 38.107 |
| Soleus muscle.r | 8.393 | 15.893 | 37.881 |

The full lower-leg bone differences cannot be dismissed by the near-exact sciatic junction. Tibial ankle-band RMS is 10.40–10.57 mm; fibular ankle-band RMS 12.66–13.12 mm. Talus RMS is 11.75–11.86 mm. Soleus ankle-band RMS reaches 33.91–33.97 mm (a small distal subset; inspect sample counts in the report); full soleus maximum reaches 38.11 mm. No universal anatomical error threshold is inferred from these distances. The observed distal relationship change is enough to withhold main-atlas registration. No new local fit was used to conceal that mismatch or break the common source frame.

## Technical and rendered QA

The four-nerve diagnostic contains 4,656 vertices / 9,216 triangles; 194,400 binary bytes / 108,192 gzip bytes. Binary SHA-256: `042687f0bb42c11c9acfba4f2e33bdee2a3f821ec3334117f5494d91135c9738`.

The separate 14-object source reference contains 10,722 vertices / 21,232 triangles; 447,792 binary bytes / 242,442 gzip bytes. Binary SHA-256: `f6e4becc0a923be34e31e4bf1a58615aea01707ca52be20bbd35a12f31b2679e`.

Both packages use Float32 positions, normalized Int16 normals and Uint32 indices with four-byte aligned fields. Export checks include finite values, index bounds, Float32 bounds roundtrip, nonzero triangle areas, gzip roundtrip, byte lengths and binary SHA. All four nerve surfaces have positive interpolated face-normal orientation; each retains 24 open boundary edges and zero nonmanifold edges. No caps or artificial branch connections were added.

Source context limitations are explicit: each fibula retains 19 source vertices unused by triangles, assigned a default up normal for those unused vertices only. Each calcaneus has one tiny source triangle with nonpositive averaged vertex-normal agreement (double area ~8.31e-12 m²; dot≈-0.574). These faces were not deleted or remodeled. The exporter records this inherited local normal issue; it does not claim all context faces pass the nerve-normal criterion. All vertices/normals remain finite and all source context indices remain valid. No self-intersection or clinical acceptance claim is made. Detailed results: `source-reference-checks.json`.

Observed diagnostic renders: `source-target-posterior.png`, `source-target-oblique.png`, `registered-bilateral.png` in the candidate directory. The paired views use identical cameras/scales; the left panel shows source bones/muscles and original evaluated nerves, the right panel target atlas references with nerves reread from the diagnostic binary. No gross side/axis reversal was observed. Near the ankle, the source tibial course hugs the medial ankle contour while the target relationship shifts toward the central ankle region. This visible difference agrees with the distal surface measurements. Those views establish technical mismatch, not anatomical expertise.

The separate reference render, `source-reference-bilateral.png`, decodes the independent source-reference binary and displays its four nerve curves with ten same-source bones. This image was opened and inspected: both sides remain in the common source frame with the authored nerve course beside the source knee/ankle context, and no gross side/axis reversal or missing nerve object was observed. Its geometry is not a main-atlas placement claim.

## Provenance, licenses and reproduction

The existing source intake is `docs/model/2026-09-08-open-assets-review.md`. The previously obtained source was reread locally; no new source download or license clearance is claimed. Source SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. Main atlas manifest SHA-256: `c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee`. Both are checked at export. Blender 5.2.0 LTS ran with `--disable-autoexec`; embedded source scripts were not executed and the source blend was not saved.

Z-Anatomy's general CC BY-SA 4.0 declaration, Gauthier Kervyn attribution, underlying BodyParts3D/DBCLS and Kousaku Okubo attribution, and original notices remain separate from the main atlas license. Object-specific author/source lineage remains unresolved. Inner-ear/kidney exceptions are retained in upstream notices, and those groups are not exported. See candidate `ATTRIBUTION.md` / `UPSTREAM-LICENSE.txt` and `public/models/extensions/DISTAL-LEG-NERVES-ATTRIBUTION.md`.

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python scripts/export-distal-leg-nerves.py -- --render
```

Without `--render`, the exporter reproduces both geometry packages and numerical reports. `node scripts/validate-atlas.mjs` passed for the unchanged active base atlas (2,234 meshes / 2,288,268 triangles); candidate-specific checks are the exporter checks reported above, not that base-atlas result. This asset work does not establish browser interaction acceptance or registration in a release. Next decision is expert review of the source reference and a separate registration strategy if main-atlas inclusion is pursued; local warping was not substituted for that review.
