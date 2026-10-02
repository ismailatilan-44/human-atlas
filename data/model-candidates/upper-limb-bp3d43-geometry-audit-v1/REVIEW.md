# BodyParts3D4.3 upper-limb geometry audit v1

Baseline HEAD `88ef99654046b62e09ab65de96adfee8acae83c2`. This bounded read-only source audit produces **26 source-preserved selectable parts /24 returned concepts**, with17 left neural files and9 source-frame bones. The two independently named left cord surfaces are technically viable candidates for root's bounded integration decision. No active model, labels, graph, public assets or Git state were changed. Expert anatomy, whole-plexus completeness and cross-source continuity remain unaccepted.

## Source identity and candidate scope

`frozen-intake.json` preserves the completed26-file intake (SHA-256 `84e377567ebd7f5c1073122fa85e768ab927db567aaa2e74b5bf9012a3e30bde`). All original OBJ, archive and license files remain untouched in `upper-limb-bp3d43-intake-v1/`. Rechecking every selected OBJ hash confirms exact source-byte preservation. The official returned4.3 OBJ headers and matching FMA3.0 memberships govern identities; generic/unsided catalog/request IDs never replace them. No new download was needed.

- Lateral cord: `BP43-FJ4274`, sourceFileID **FJ4274**, representation **BP29122**, returned concept **FMA45239**.
- Medial cord: `BP43-FJ4275`, sourceFileID **FJ4275**, representation **BP29196**, returned concept **FMA45241**.

Both names explicitly specify left. No right source counterpart, mirror, or bilateral coverage is inferred. Five C5/C6/C7/C8/T1 files remain **spinal nerve trunks used as context**, not separately accepted ventral rami or isolated plexus-root contributions. Their exact returned identities stay intact. Source demographic/specimen detail is unestablished by this intake; manifest sex is `unknown`.

Two distinct radial files share FMA37071; two distinct axillary files share FMA37074. Each FJ remains a separate part; the two files are aggregated only under their actual shared source concept. The selection omits source radial digital-member files and other unacquired catalog observations, so it is not the complete radial nerve or whole neural tree. The dataset is `upper-limb-bp3d43-reference-candidate`, with `compatibleWithMainAtlas:false` pending root's acceptance choice.

## Existing native frame tested without fitting

`frame-hypothesis.json` pins the historical thyroid4.3 manifest and exact native conversion:

`(x,y,z) millimetres → (0.001x, 0.001z+0.0781112, -0.001y-0.1) metres`.

No ICP, scale estimation, translation optimization, rotation adjustment or individual object movement was performed. Nine actual4.3 source bones were independently compared to same-ID main4.0 surfaces, using all-vertex bidirectional nearest-triangle distances. Different vertex counts reflect source/version/simplification differences; shared IDs alone were not treated as proof. Measurements are vertex-weighted, not clinical error bounds or nerve-course validation.

| Source bone | RMS mm | P95 mm | Max mm |
| --- | ---: | ---: | ---: |
| First thoracic vertebra (FJ3158) | 0.0240 | 0.0558 | 0.1572 |
| Fifth cervical vertebra (FJ3167) | 0.0147 | 0.0000 | 0.1602 |
| Sixth cervical vertebra (FJ3170) | 0.0218 | 0.0498 | 0.1785 |
| Seventh cervical vertebra (FJ3172) | 0.0200 | 0.0270 | 0.1643 |
| Left first rib (FJ3228) | 0.0575 | 0.1197 | 0.2028 |
| Left second rib (FJ3229) | 0.0705 | 0.1445 | 0.2798 |
| Left clavicle (FJ3237) | 0.0763 | 0.2179 | 0.3809 |
| Left humerus (FJ3262) | 0.2411 | 0.5194 | 0.8268 |
| Left scapula (FJ3279) | 0.0472 | 0.0947 | 0.1890 |

The observed RMS range0.0147–0.2411mm and maximum0.8268mm support this native frame for the tested neck/shoulder/upper-arm references. This is stronger local coordinate evidence than the inherited Z-Anatomy arm fit at the thoracic inlet. It does not validate contact or continuous anatomy between these BP43 structures, the registered Z-Anatomy plexus, or the separate source-frame127 reference. Forearm/carpal bone holdouts are outside the acquired nine-bone context, so distal terminal-nerve course acceptance is not established.

## Components, seams and true separated pieces

`geometry-audit.json` records raw source index topology and an **exact-position identification diagnostic**. The diagnostic identifies vertices at identical coordinates only to distinguish duplicate corner/seam records from disconnected surfaces; it does not weld exported vertices or modify any source face. Source-Z bounds below are coordinate extents in millimetres, not named anatomical endpoints or nerve lengths.

| FJ | Exact returned name | Raw index → exact-position components | Source Z extent mm |
| --- | --- | ---: | ---: |
| FJ4171 | Left axillary nerve | 10 → 1 | 1262.46–1317.00 |
| FJ4172 | Left radial nerve | 6 → 1 | 933.38–1042.48 |
| FJ4185 | Left second intercostobrachial nerve | 81 → 2 | 1184.67–1331.42 |
| FJ4222 | Trunk of left long thoracic nerve | 8 → 1 | 1110.58–1401.52 |
| FJ4223 | Left medial pectoral nerve | 76 → 2 | 1158.17–1317.69 |
| FJ4240 | Left radial nerve | 7 → 2 | 786.31–1333.37 |
| FJ4242 | Left superior subscapular nerve | 31 → 1 | 1222.84–1330.08 |
| FJ4243 | Left axillary nerve | 18 → 1 | 1229.96–1277.76 |
| FJ4245 | Trunk of left first thoracic nerve | 5 → 1 | 1358.87–1364.27 |
| FJ4256 | Left thoracodorsal nerve | 36 → 1 | 1068.34–1308.42 |
| FJ4258 | Left ulnar nerve | 3 → 1 | 786.05–1333.66 |
| FJ4264 | Trunk of left fifth cervical nerve | 2 → 1 | 1378.94–1418.67 |
| FJ4265 | Trunk of left sixth cervical nerve | 9 → 1 | 1371.74–1401.15 |
| FJ4266 | Trunk of left seventh cervical nerve | 3 → 1 | 1361.65–1391.19 |
| FJ4267 | Trunk of left eighth cervical nerve | 7 → 1 | 1353.34–1377.35 |
| FJ4274 | Lateral cord of left brachial nerve plexus | 5 → 1 | 1335.88–1362.62 |
| FJ4275 | Medial cord of left brachial nerve plexus | 11 → 2 | 1330.28–1352.59 |

Lateral cord raw5 components become one connected diagnostic surface, with176 unique positions/348 triangles, zero boundary edges, zero nonmanifold edges and zero zero-area triangles. The source bounds span26.2107×10.8530×26.7400mm. This resolves the initial component-count concern as coordinate-identical seam records rather than five named cord branches.

Medial cord raw11 components become two diagnostic components: the dominant1700-triangle surface carries99.9999995301% of surface area; an8-triangle speck carries0.0000004699%. That speck spans approximately0.0016×0.0015×0mm and has a sampled nearest-surface distance0.560mm from the dominant component. Four nonmanifold edges occur in exact-position diagnostics; the whole source has no zero-area triangles. The tiny artifact is retained, disclosed, and never assigned an anatomical branch identity. Whole source bounds span36.6097×9.8314×22.3100mm.

The second intercostobrachial file contains **two substantial disconnected surfaces**, about58.84%/41.16% of area, with a sampled vertex-to-largest-surface minimum9.532mm. Medial pectoral likewise has two substantial surfaces,51.03%/48.97%, sampled minimum2.615mm. The corresponding opened render shows these independent source paths. They must not be promoted as an unbroken complete nerve tree or silently joined. Radial FJ4240 has a dominant4472-triangle surface plus a tiny2-triangle artifact (about0.0000050% of area). Other primary neural index fragmentation resolves to single exact-position components.

`source-proximity.json` gives bounded sampled geometric proximities among the cords and selected neural files. Near-contact does not establish shared topology, anatomical parentage or completeness; these numbers are not relationship edges. No gap was bridged, no endpoint snapped, and no fragment was removed.

## Source-preserved export and opened views

The candidate retains all source vertex records and triangle indices in original order. Source OBJ normals are one-to-one with vertex indices and are preserved through the common proper rotation, normalization and Int16 quantization. No smoothing or generated replacement normals are applied. Output positions are Float32 and indices Uint32; input source millimetre bounds and exact source hashes remain in metadata. Tiny specks and bone defects remain part of the candidate.

Three paired source/decoded views were rendered and opened: whole selected neural extent, cord close-up, and collateral fragments. Source is left; decoded is right. Lateral cord is orange, medial cord magenta, other named nerves gold, second intercostobrachial green, and the contextual spinal nerve trunks blue. Source-authored versus actual decoded Int16 normals are used in shading. No visible transfer mismatch was observed. Cord surfaces appear as short capped source segments; visible proximity/stumps do not establish a complete continuous plexus. Overview bones stop at the humerus because forearm bones were not among the acquired context.

A fourth opened image overlays native-transformed source43 ivory bones and main40 cyan bones; their close agreement corroborates the numerical frame measurements. Render panel shifts are display-only. No inference about right anatomy or expert correctness is made from these images. Exact settings are in `render-evidence.json`.

The final26-part candidate has **42,804 vertices /76,326 triangles**,1,686,408 raw bytes and982,207 gzip bytes. `validation.json` confirms decoded finite positions, normalized authored normals (maximum length error0.000024893), bounds, valid indices, four-byte offsets, unique26 parts/24 concepts, exact returned concepts, all26 unchanged source files and gzip round trip. Two numerical builds produce all five package files byte-identically. No self-intersection, physiological function, clinical-volume or whole-region acceptance test is claimed.

- `atlas.json`: `620a443a9bf345d597e3f13cfa6563e19402589247938713c197afdfe546d2a0`
- `anatomy.bin`: `d67509db4368cdcc7f39b853f23bcd6dbc5864699b6a8d3bf197c0c3ac839f0a`
- `anatomy.bin.gz`: `7a70e6be103f5a183f1325817a8f13c29fe3c66aa4bddb5fefeafaddfd19b36e`

## Reproduction and disposition

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec --python data/model-candidates/upper-limb-bp3d43-geometry-audit-v1/build.py
python3 data/model-candidates/upper-limb-bp3d43-geometry-audit-v1/validate.py
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec --python data/model-candidates/upper-limb-bp3d43-geometry-audit-v1/render.py
```

`build_candidate(output_dir=None)` writes here by default and has no import-time mutations. To repeat the numerical comparison, add `-- --output data/model-candidates/upper-limb-bp3d43-geometry-audit-v1/reproduction` to a second build, then run `validate.py --compare`. The producer rereads and verifies the retained26 OBJ hashes; it never saves a blend. Build and render use Blender5.2.0LTS on macOS. No source software installation or access workaround was needed. Verbose `*.log` files are local diagnostics and must not be staged.

**Decision evidence:** both left cord files now have independent returned identities, reproducible selectable source geometry and strong bounded coordinate compatibility. They are ready for root's limited source-component integration review with the medial speck/nonmanifold diagnostic disclosed. They do not close right-side cords, isolated C5–T1 contributions, precise neural continuity or expert acceptance. Keep substantial collateral splits and partial terminal-member selections explicit if those objects are considered later. Root owns active packaging, source-aware labels/relations, source→search→selection→focus/context→return interaction checks and release. No application/browser/deployment gates were run by this geometry-only task.

Provenance is DBCLS BodyParts3D official live4.3 /Objects4.3 /FMA3.0 as frozen by the preceding intake. `ATTRIBUTION.md` retains its CC BY-SA2.1 Japan notice; `UPSTREAM-LICENSE.html` is the captured official license byte-for-byte. This is separate from main4.0 and Z-Anatomy licenses, and no whole-archive commercial clearance or new demographic fact is inferred. Original acquisition dates/cache distinctions and requested-versus-returned IDs remain in the frozen intake. Timing and any rework are in `timing.json`; initial reads and pre-task scheduling are excluded/unknown.

## Root handoff review

Root opened all four recorded images and rechecked package/audit/render hashes after the127-reference source release. Source/decoded geometry and the native-frame bone overlay support a bounded two-left-cord integration decision; runtime/expert acceptance remains pending. See `root-review.json`. No geometry, parent selection or active dataset was changed.

For routine read-only verification use `python3 data/model-candidates/upper-limb-bp3d43-geometry-audit-v1/check.py`. The historical `validate.py` writes `validation.json`; calling it without `--compare` replaces the recorded comparison result. Root restored the historical report from the identical embedded handoff evidence and retained the original validator. The new checker never writes evidence and reports null when second-output comparison was not requested. The earlier two-export result remains historical; its reproduction folder is no longer available, so a fresh comparison was not claimed.
