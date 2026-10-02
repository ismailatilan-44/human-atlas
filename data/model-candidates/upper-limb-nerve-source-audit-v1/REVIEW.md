# Upper-limb named nerve source audit v1

Baseline revision: `0ac477f2a686991bcb4f4d2a72267c9243547433`. The bounded candidate contains **127 independently selectable source objects:54 new named nerve curves,24 previously exported nerve objects as source context, and49 same-source bones**. Root chose an independent source-frame technical reference after comparison showed the inherited main-atlas transform remains limited in the neck/chest. This is not a complete plexus, a main-body fit, anatomical expert acceptance, or continuity acceptance between datasets.

## Pinned source and bounded discovery

The existing male-source `work/open-assets-review/Startup.blend` has SHA-256 `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. It was opened with Blender5.2.0LTS `--background --disable-autoexec`; no source save or new download occurred. `discovery.json` distinguishes nerve-name CURVEs, surface/marker MESHes, FONT objects and collection membership. This is a bounded named-object inventory, not a whole-atlas anatomical absence claim.

No separate medial/lateral cord CURVE was found. The `Branches of medial/lateral cord of brachial plexus` named records are FONT and zero-polygon marker meshes; collections do not establish independently selectable cord geometry. The prior pinned root review is reused in `prior-evidence.json`, with manifest/report hashes. Roots remain excluded for unresolved extra superior-branch identity. No old root segmentation experiment was repeated and no spline receives a C5–T1 identity.

The agreed27 bilateral bases are listed below. Whole source extents are retained even where they continue into forearm/wrist. Grouped muscular/pectoral/suprascapular branches remain single named objects; no numbered or muscle-specific terminal identities are invented. Palmar/digital nerve groups remain outside this delivery. `Subclavian nerve.l/.r` also exists as named source CURVEs in the discovery and is explicitly deferred for the next bounded collateral review, not claimed absent. No matching intercostobrachial/posterior-brachial-cutaneous object name was found in this nerve-name inventory; alternate source identity remains possible.

| Exact source base, each .l/.r | Vertices / triangles per side | Authored control points per spline |
| --- | ---: | --- |
| Ulnar nerve | 1596 / 3168 | 1,12 |
| Radial nerve | 1164 / 2304 | 9 |
| Axillary nerve | 588 / 1152 | 5 |
| Medial brachial cutaneous nerve | 876 / 1728 | 7 |
| Superior lateral brachial cutaneous nerve | 1020 / 2016 | 8 |
| Inferior lateral brachial cutaneous nerve | 300 / 576 | 3 |
| Medial antebrachial cutaneous nerve | 876 / 1728 | 7 |
| Lateral antebrachial cutaneous nerve | 876 / 1728 | 7 |
| Posterior antebrachial cutaneous nerve | 1308 / 2592 | 10 |
| Anterior branch of medial antebrachial cutaneous nerve | 732 / 1440 | 6 |
| Posterior branch of medial antebrachial cutaneous nerve | 1164 / 2304 | 9 |
| Lateral pectoral nerve | 3660 / 7200 | 10,8,4,5,3 |
| Medial pectoral nerve | 1032 / 2016 | 5,4 |
| Dorsal scapular nerve | 1308 / 2592 | 10 |
| Long thoracic nerve | 2040 / 4032 | 14,2 |
| Thoracodorsal nerve | 2340 / 4608 | 9,6,4 |
| Suprascapular nerve | 2508 / 4896 | 8,4,4,3,3 |
| Superior subscapular nerve | 588 / 1152 | 5 |
| Inferior subscapular nerve | 1032 / 2016 | 5,4 |
| Muscular branches of axillary nerve | 588 / 1152 | 5 |
| Muscular branches of median nerve | 624 / 1152 | 2,2,2,2 |
| Muscular branches of radial nerve | 1356 / 2592 | 4,3,3,2,2 |
| Muscular branches of ulnar nerve | 312 / 576 | 2,2 |
| Anterior interosseous nerve of forearm | 732 / 1440 | 6 |
| Posterior interosseous nerve of forearm | 876 / 1728 | 7 |
| Deep branch of radial nerve | 1020 / 2016 | 8 |
| Superficial branch of radial nerve | 2208 / 4320 | 11,3,3,2 |

`new-object-mapping.json` is the exact54 mapping. Part IDs are `ZA-ULNR-{SOURCE-SLUG}-L/R`; concept IDs use existing canonical `atlas:left/right-*` identities. Source Superior/Inferior subscapular names retain their exact object and part names while mapping to the existing upper/lower-subscapular concepts. Terminology review is separate; in particular the pinned superior-lateral-brachial-cutaneous Latin row is not accepted as anatomical evidence.

`context-mapping.json` retains the original24 nerve part/concept IDs (20 plexus trunk/division/posterior-cord, bilateral median and musculocutaneous), re-evaluated in this dataset's source frame. It adds49 bones:bilateral clavicle/scapula/humerus/radius/ulna, ribs1–8 and eight carpals, plus C3–C7/T1/T2. These are context, not new nerve coverage.

## Geometry and source fidelity

The sole export transformation is the common orthonormal row-vector matrix for `(x,y,z)→(x,z,-y)`, metres. Every object retains source-world relation to every other object. There is no fit, scale change, individual movement, deformation, redraw, cap, weld, decimation or root/cord fabrication. Mirrored object winding is corrected. Source types, matrices, laterality, units/bounds, mesh hashes, materials, modifiers, curve settings, all control points/handles/radii and open-end settings are recorded. `compatibleWithMainAtlas:false`, `registration:null`, datasetId `upper-limb-nerve-reference`.

All54 primary objects have finite selectable evaluated tube geometry; zero zero-area/nonmanifold triangles, no cancelled/loose vertex normals and positive averaged-normal/face agreement. Exact isolated spline conversion in `spline-checks.json` totals to each full object's geometry. Only bilateral ulnar spline0 is a one-point remnant producing0 vertices/triangles; it is retained as source metadata and not fabricated into a tube. Tube ends stay open. Separate source tubes may touch/overlap without being welded; no verified anatomical connectivity is inferred.

Bone context keeps source defects. Bilateral scapulae each retain2 zero-area triangles and25 cancelled/loose normal vertices; clavicles each12 such vertices, sixth ribs each10, C4 has6. Humeri each have2 nonmanifold edges. `geometry-checks.json` lists all boundary, component and normal disagreements, including less severe inherited bone issues. Normal encoding uses the largest incident nonzero face for cancelled normals, or unitY for isolated vertices; no vertex/triangle is removed or repaired. No self-intersection or complete nerve/bone-contact validation was performed.

The candidate has **184,698 vertices /366,040 triangles**. Decoder checks pass for unique IDs, exact mapping, finite Float32 positions, bounds, four-byte offsets, Uint32 indices, normalized Int16 normals (maximum length error0.000025564), and gzip round trip. Two final numerical exports produce byte-identical manifest, raw binary, gzip, attribution and upstream-license files. `validation.json` and `acceptance-evidence.json` bind the final hashes.

- `atlas.json`: `299f9eb315dc6ecbb4bdcbd388884595aeed0395a5cdb6d27be20b5e1c5642d0`
- `anatomy.bin`: `3355121fe3725b885c47f7f0412598ac87e82f83d5022e82e99496a98d949547`
- `anatomy.bin.gz`: `20f1090a1b6a64cb17730a624a593f9069e4af8cfc0a3f797886c535210fde28`

## Existing-matrix comparison; rejected as broad acceptance

`check-registration.py` applies the existing upper-arm similarity matrix unchanged to all54 candidate nerve curves for preview and49 exact source bone counterparts for holdouts. It does not fit or optimize a matrix. `registration-checks.json` pins the registration/main manifest hashes and records all-vertex bidirectional nearest-surface distances. These are vertex-weighted model-comparison statistics, not clinical error bounds or nerve-path validation.

| Bilateral source references | RMS range mm | Maximum mm |
| --- | ---: | ---: |
| Humerus/radius, original fit references |0.608–0.644|4.037|
| Ulna, independent holdout |0.426–0.500|1.673|
| Carpals, independent holdouts |0.301–0.677|2.247|
| Scapulae, original fit references |1.845–1.846|7.663|
| Clavicles, independent holdouts |4.664–4.761|12.930|
| Ribs1–8, independent holdouts |5.774–8.433|13.484|

C3 RMS is7.893mm/max16.172; C4 RMS6.600/max14.039. C5–T1 reproduces the existing roughly4.31–4.80mm limitation. Good distal bone metrics cannot establish all new nerve courses or extend fitting acceptance into neck/thorax. Root therefore retains the entire127-object candidate in independent source coordinates; the registered images are limited comparison evidence only.

## Opened visual evidence

Three paired views—whole arm, shoulder, forearm—were rendered from independently evaluated source meshes (left) and decoded candidate arrays (right), and opened. Gold=new nerve curves; cyan=previous source nerve context; translucent ivory=bones. No gross transfer mismatch was observed. Paired render meshes use Blender triangle shading; Int16 normal quantization is checked numerically, so these images do not constitute browser shader acceptance. The whole view shows full selected course extent; close views intentionally crop peripheral context. Source-authored disconnected/truncated ends remain visible, and no anatomical connection is accepted from proximity. Both sides receive numerical checks; representative renders show the left side.

Two additional registered shoulder/forearm views were opened. They overlay transformed ivory source bones and blue main-atlas bones, using only the old matrix. Visible neck/chest offsets corroborate the holdout measurements; forearm alignment is closer. These images do not authorize main-atlas inclusion. Render camera/panel offsets exist only in the QA scene, never the exported coordinates. `render-evidence.json` specifies views.

## Reproduction, provenance and handoff

From repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec work/open-assets-review/Startup.blend --python data/model-candidates/upper-limb-nerve-source-audit-v1/export.py
python3 data/model-candidates/upper-limb-nerve-source-audit-v1/validate.py
```

`export.py` provides callable `build_candidate(output_dir=None)` with no import-time writes and a default confined to this candidate directory. For a second numerical run add `-- --output data/model-candidates/upper-limb-nerve-source-audit-v1/reproduction`, then run `validate.py --compare`. For registration evidence use the same Blender invocation with `check-registration.py`; for images, with `render.py` after the registration report exists. `inspect-splines.py` repeats isolated new-spline accounting. The frozen source-reference manifest preserves the inherited source provenance; the main atlas is only read for comparison. No npm/app/browser checks are claimed by this geometry-only task.

`ATTRIBUTION.md` and verbatim `UPSTREAM-LICENSE.txt` retain the existing Z-Anatomy general CC BY-SA4.0 notice and underlying BodyParts3D/other separate notices; inner-ear/kidney exceptions remain explicit and are not selected here. Source-object-specific authorship remains unresolved; no new redistribution clearance is asserted. The existing intake `docs/model/2026-09-08-open-assets-review.md` remains authoritative.

Only this candidate directory was written. Root owns public producer/package integration, all127 dataset-scoped labels, UI search→selection→focus/context→relationship→return tests and release. No Git stage/commit/push or deployment occurred. Verbose `*.log` diagnostics are local only and must not be staged. Root's next action is independent-reference integration with explicit root/cord/hand omissions, then product acceptance; no target/expert criterion closes merely from these source counts.

Timing is in `timing.json`, measured from discovery setup to final handoff preparation, excluding initial reads. Rework: one missing helper import fixed; the initial camera used Blender's Z-up convention and was corrected to explicit display-Y-up, then all five views were opened; deterministic comparison detected runtime pointers in source custom-property string representations, so actual stable property values replaced those strings and two numerical runs passed. No geometry was edited for these corrections. Pre-task scheduling/waiting time is unknown.
