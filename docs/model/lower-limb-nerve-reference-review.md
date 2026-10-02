# Independent lower-limb nerve reference — 2 October 2026

The browser-ready package contains **21 selectable source objects: six nerve curves and fifteen context bones**, retained in one source coordinate frame. It exposes the bilateral sciatic → tibial/common fibular source continuation with pelvis-to-ankle bone context. It is a bounded regional reference, not complete lower-limb anatomy or expert anatomical acceptance.

## Scope, identity and coordinates

Public files are `public/models/lower-limb-nerve-reference/atlas.json`, `anatomy.bin`, `anatomy.bin.gz`, `ATTRIBUTION.md` and `UPSTREAM-LICENSE.txt`. Dataset ID is `lower-limb-nerve-reference`; sex is `male`, consistent with the [existing source intake](2026-09-08-open-assets-review.md). The manifest declares `compatibleWithMainAtlas:false` and `atlasRegistration:null`.

| Source object(s) | Persistent part ID(s) | Concept ID(s) |
| --- | --- | --- |
| Tibial nerve.l/r | ZA-TIB-L/R | atlas:left/right-tibial-nerve |
| Common fibular nerve.l/r | ZA-CFIB-L/R | atlas:left/right-common-fibular-nerve |
| Sciatic nerve.l/r | ZA-SCI-L/R | atlas:left/right-sciatic-nerve |
| Tibia.l/r | ZA-DLN-TIBIA-L/R | zanatomy:tibia-l/r |
| Fibula.l/r | ZA-DLN-FIBULA-L/R | zanatomy:fibula-l/r |
| Patella.l/r | ZA-DLN-PATELLA-L/R | zanatomy:patella-l/r |
| Talus.l/r | ZA-DLN-TALUS-L/R | zanatomy:talus-l/r |
| Calcaneus.l/r | ZA-DLN-CALCANEUS-L/R | zanatomy:calcaneus-l/r |
| Femur.l/r | ZA-LLR-FEMUR-L/R | zanatomy:femur-l/r |
| Hip bone.l/r | ZA-LLR-HIP-L/R | zanatomy:hip-bone-l/r |
| Sacrum | ZA-LLR-SACRUM | zanatomy:sacrum |

Slash notation abbreviates separate left and right records. Source object identity, datablock, source-world bounds and matrix, determinant, modifiers, materials, collection membership, geometry type and evaluated counts are stored per part. Laterality is corroborated with source-world X, not inferred only from a suffix. Namesakes such as `Femur.i/.j` and `Hip bone.i/.j` are not included.

Every object receives precisely the same proper orthonormal axis rotation `(x,y,z) → (x,z,-y)` from source X left / Y posterior / Z superior to display X left / Y superior / Z anterior, in meters. Original source origin, scale and relative placement are retained; no fitting, translation, local warping, separate object motion or rescaling occurs. Render comparison panel offsets exist only in the temporary QA scene, never in package geometry.

The earlier four-nerve main-frame diagnostic and fourteen-object source candidate remain unchanged and inactive. Their rejection history is preserved in the [distal registration audit](asset-registration-distal-leg-nerves.md). A check against Git HEAD `a0fd55413018ec839e493719369be4f051df53dc` confirmed the old exporter and both old package triples remain byte-identical. All position, normal and index arrays for the fourteen shared parts are byte-identical between the old source candidate and this new package.

## Authored nerve extent

Each tibial object retains one Bezier spline / ten control points, 1,308 vertices and 2,592 triangles. Each common fibular object retains one Bezier spline / eight control points, 1,020 vertices and 2,016 triangles. Each sciatic object retains all three Bezier splines / twenty control points (12 + 4 + 4), 2,484 vertices and 4,896 triangles. Variable point radii, Bezier handles and handle types, curve bevel settings, source-world control points and rotated reference control points/endpoints are recorded in `sourceExtent`.

Open ends remain open: each distal nerve has 24 boundary edges; each sciatic has 72. All six nerves have zero nonmanifold edges and positive interpolated face-normal agreement. No caps or joining faces were manufactured. The proximal endpoint of each tibial/common fibular main spline is within approximately 0.00012–0.00018 mm of its same-side sciatic distal endpoint in this source frame. The manifest records exact distances. This is authored source continuity evidence, not anatomical precision or expert verification.

The common fibular objects end near the proximal leg; tibial objects extend to the ankle. Separate deep/superficial fibular, plantar, sural, muscular and digital branch objects are excluded. The short proximal sciatic splines are retained without assigning unsupported root or branch identities. This package also excludes muscles, vessels, full foot skeleton and detailed joint supports. No complete innervation or root/plexus coverage claim is made.

## Technical acceptance and inherited defects

Blender **5.2.0 LTS** on local macOS evaluated the pinned file with `--disable-autoexec`; embedded source scripts were skipped and the source blend was not saved. The existing unrelated oesophagus/profile dependency-cycle warning recurred; it did not prevent reading these selected objects. Geometry uses Float32 positions, signed normalized Int16 normals and Uint32 triangle indices, with four-byte aligned offsets.

Exporter acceptance passed: source SHA, exact identities/counts, proper rotation, finite decoded coordinates, decoded bounds, index ranges, nonzero triangle areas, normal lengths, aligned offsets, gzip roundtrip, decoded positions equal rotated source values, decoded indices equal evaluated source indices (after mirrored winding correction). Binary, gzip and manifest reproduced byte-for-byte in two completed exports. The second render pass reads encoded normals as well as positions and indices for the decoded panel.

| Artifact property | Verified value |
| --- | --- |
| Parts / vertices / triangles | 21 / 29,108 / 57,864 |
| Binary / gzip bytes | 1,218,328 / 714,473 |
| Source blend SHA-256 | `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd` |
| Binary SHA-256 | `66374fc7903125278ccc3285b7cfae836db19d8d129edefc8759b9e6ab457b92` |
| Gzip SHA-256 | `594789b7fa352d0149fc150e5519340b0d21f23dcaf5c90d79b0a630a1c1095e` |
| Manifest SHA-256 | `2230e2d1b3d92d0dafed463c5c3038580bbff5dc765448a7c2e44820d4913c22` |
| Maximum quantized normal-length error | 0.000023524 |

Source bones have known local defects that are retained, not silently repaired:

- Each fibula retains 19 vertices unused by triangles. Only these unused vertices receive default up normals.
- Each calcaneus retains one tiny triangle with nonpositive averaged vertex-normal agreement (double area about 8.31e-12 m²; dot about -0.574).
- Sacrum retains 21 loose vertices, 13 boundary edges and four edges shared by more than two triangles. One used vertex has exactly cancelling angle-weighted normals; its largest incident face normal is used as a disclosed fallback. Three sacral triangles still have nonpositive averaged vertex-normal agreement (minimum dot -1/3).

All encoded normals remain finite and normalized within the recorded quantization limit. Source triangles and positions were not removed, capped, welded or relocated. These findings are in `inheritedMeshDefects` and [geometry-checks.json](../../data/model-candidates/lower-limb-nerve-reference/geometry-checks.json). No self-intersection, watertight bone or clinical acceptance claim is made.

## Visual QA and remaining product acceptance

The final four PNGs were opened and inspected locally:

- [Source / decoded posterior comparison](../../data/model-candidates/lower-limb-nerve-reference/source-decoded-posterior.png)
- [Source / decoded oblique comparison](../../data/model-candidates/lower-limb-nerve-reference/source-decoded-oblique.png)
- [Decoded knee close view](../../data/model-candidates/lower-limb-nerve-reference/decoded-knee-close.png)
- [Decoded ankle close view](../../data/model-candidates/lower-limb-nerve-reference/decoded-ankle-close.png)

In paired views, the right image panel is the source and the left panel is decoded output, shown with the same camera and scale. Bilateral sciatic trunks, their authored proximal splines and tibial/common fibular continuations remain visible with the expected source knee and ankle context. No gross missing object, mirror/axis reversal or source/output course mismatch was observed. The distal extent limits are visible in the close views. These images establish technical source preservation, not anatomical expert acceptance.

The asset task does not itself establish browser search → selection → focus/context → relationship → return acceptance, deployed source revision, mobile usability or expert anatomical review. Integration and those checks belong to the delivery handoff. Anatomical expert review remains pending. The next product action is to register this as a separate reference and exercise that complete journey; do not merge it into the main-body geometry using the rejected distal fit.

## Provenance and reproduction

Source archive/member and acquisition are inherited from the [8 September intake](2026-09-08-open-assets-review.md); no new source download or licensing clearance is claimed. Z-Anatomy's general CC BY-SA 4.0 declaration/Gauthier Kervyn attribution and the underlying BodyParts3D/DBCLS CC BY-SA 2.1 Japan/Kousaku Okubo notice remain separate. Upstream inner-ear/kidney exceptions remain in the copied notices; neither group is exported. Object-specific authorship lineage remains unresolved. See [package attribution](../../public/models/lower-limb-nerve-reference/ATTRIBUTION.md).

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python scripts/export-lower-limb-reference.py -- --render
```

Without `--render`, this independent script regenerates only this package's geometry/manifest and numerical report. It never imports or runs the historical exporter. Attribution files are reviewed package documents and are retained alongside regenerated geometry. No glTF was produced, so a glTF validator is not applicable.

Asset review base revision: `a0fd55413018ec839e493719369be4f051df53dc`; delivered files are uncommitted additions on `codex/publish-model-explorer`. Elapsed delivery time was not instrumented and is unknown. One initial export stopped on sacral normal cancellation; the corrective change retained the source geometry and explicitly recorded a normal fallback. No remote/deployment acceptance was attempted by this asset task.

## Integration handoff — local product acceptance

The integration owner registered the independent reference with dataset-scoped labels and four branch relationships. TypeScript and the interaction validator passed on the final local application changes. Real Chromium interaction exercised Turkish left-tibial search, source-backed sciatic/branch navigation and isolation on desktop, Latin names and return on 390×844 mobile, and the corrected model frame on 320×568. English right-common-fibular navigation resolved only the right sciatic and its two same-side branches. Returning to the male reference cleared the reference selection and view history. The source inventory and 66-target non-exhaustive seed passed reproducibility checks. See the [owning action report](progress-report-2026-10-02.md) for revision and publication acceptance; this local handoff does not establish live or anatomical expert acceptance.

Publication acceptance: source `09879bf300d38eae14054fcdd55ea4fdc121d1fc`, static `1a13ccf4136780b8c9b4b9a4ab8dbb0d40024f6f`, Pages run `36984762689` succeeded. The live release SHA matched. Actual live 390×844 search → right tibial → right sciatic → right common fibular → isolated Latin view passed with no console errors/warnings; the integration owner opened the saved screenshot. Production build passed with the existing large-JS warning (337.62 KB gzip). This is technical product acceptance; physical-device and anatomical expert criteria remain open. Next: inspect the unbound distal nerve and ankle-support target source objects.
