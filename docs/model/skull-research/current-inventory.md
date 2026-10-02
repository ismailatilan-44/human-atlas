# Current skull inventory and representation limits

Research date **2026-10-02**; original audit pin `649926e81ef7909f88f754bc89b10bca417c29fa`. Integration baseline `b5ffe57c5d160844ba40277d95a70c7a4fa43d26` changes no anatomy data, manifests, conversion, metadata, explosion, renderer or saved-scene files relative to that pin. Their bounded findings therefore remain applicable. This is repository evidence, not a fresh live-site or geometry-rendering audit.

## Exact 22-part selection

Active group **`atlas:skull-bones`** is a project display composite, not a new FMA assertion. Eight cranial plus fourteen facial bones comprise six unpaired bones and eight pairs. Cranial bones are not synonymous with calvaria. All 22 have active TR/EN/LA labels; side-specific Latin display uses L/R, without invented declensions. Anatomical expert review remains pending.

| Class | Bone | Side | Source part | Source concept |
| --- | --- | --- | --- | --- |
| Cranial | Ethmoid | Unpaired | FJ3199 | FMA52740 |
| Cranial | Frontal | Unpaired | FJ3200 | FMA52734 |
| Cranial | Occipital | Unpaired | FJ3309 | FMA52735 |
| Cranial | Sphenoid | Unpaired | FJ3394 | FMA52736 |
| Cranial | Parietal | Left | FJ3274 | FMA52789 |
| Cranial | Parietal | Right | FJ3380 | FMA52788 |
| Cranial | Temporal | Left | FJ3281 | FMA52739 |
| Cranial | Temporal | Right | FJ3386 | FMA52738 |
| Facial | Mandible | Unpaired | FJ3289 | FMA52748 |
| Facial | Vomer | Unpaired | FJ3395 | FMA9710 |
| Facial | Zygomatic | Left | FJ3287 | FMA52893 |
| Facial | Zygomatic | Right | FJ3392 | FMA52892 |
| Facial | Maxilla | Left | FJ3269 | FMA53650 |
| Facial | Maxilla | Right | FJ3375 | FMA53649 |
| Facial | Nasal | Left | FJ3272 | FMA53648 |
| Facial | Nasal | Right | FJ3378 | FMA53647 |
| Facial | Lacrimal | Left | FJ3265 | FMA53646 |
| Facial | Lacrimal | Right | FJ3371 | FMA53645 |
| Facial | Palatine | Left | FJ3273 | FMA53656 |
| Facial | Palatine | Right | FJ3379 | FMA53655 |
| Facial | Inferior nasal concha | Left | FJ3263 | FMA54738 |
| Facial | Inferior nasal concha | Right | FJ3369 | FMA54737 |

Owning records: [active group](../../../data/anatomy/skull-bones.json), [base manifest](../../../public/models/atlas.json), [labels](../../../data/anatomy/labels.json), [integrated label review](../../../data/model-candidates/skull-labels/REVIEW.md), [historical selection proposal](../../../data/model-candidates/concept-selection-review/skull-bones-proposal.json). Historical candidate wording does not override active integration. Teeth, hyoid, ear ossicles and eye/lacrimal soft tissues are excluded from this display group; teeth occur elsewhere in the base dataset. Whole-bone identity does not certify every feature of a bone.

## Geometry and frame

The subset has **36,743 vertices, 55,866 triangles**, and **1,331,766 bytes** of position/normal/index arrays (`vertices × (12 + 6) + indices × 4`). This excludes renderer duplication/overhead; it is neither transfer size nor total GPU memory. Shared body chunks 12/13 prevent interpreting selection as a skull-only download. Left/right temporal bones have 2,828/2,906 triangles, which does not prove canal or thin-plate fidelity.

BodyParts3D 4.0 adult male TARO is the base source: 2,234 base meshes, 2,292 with active extensions. Source millimetres `(x,y,z)` become metres `(x*.001, z*.001+.0781112, -y*.001-.1)`, Y up. This is one shared conversion and stage translation, not individual fitting. Recorded meshoptimizer simplification uses `maximumRelativeError .002`; all base meshes were retained, but that tolerance is not anatomical validation. Four concha/lacrimal display layers are corrected to skeletal without rewriting upstream metadata. Sources: [conversion](../../../scripts/convert-anatomy.py), [metadata](../../../app/atlas-metadata.ts), [attribution](../../../public/ATTRIBUTION.md), [inventory](../model-inventory.md).

## Misleading source groups and fine-feature gaps

| Source concept | Observed descendant selection | Teaching consequence |
| --- | --- | --- |
| FMA46565 — skull | 43 surfaces, including eye/lacrimal tissue and two hyoid surfaces | Preserve raw source membership, use reviewed 22-part group for bone identity. |
| FMA52801 — basicranium | Only FJ3199 (ethmoid) | Not a verified complete skull-base selection. |
| FMA53672 — neurocranium | Seven surfaces; sphenoid omitted | Not the standard eight-bone teaching set. |
| FMA53673 — viscerocranium | Mixed membership including ethmoid, temporal, sphenoid, eye structures and hyoid | Not the fourteen-facial-bone teaching set. |

The inspected base part/concept and knowledge/explorer catalogs establish no named active skull anchors or separately named bony foramina/sutures. The six anchors and two unanchored targets were upper-limb content. This is a **catalog/annotation gap**, not proof that features are absent inside a whole-bone surface. Bone-related graph predicates found were `part_of`; no verified suture, articulation, boundary or passage relation was established. No skull study pack existed; current packs are right ankle, left ankle and right upper limb. [Scope plan](../model-scope-and-acceptance.md) keeps skull/facial D1–D2 fine-target enumeration open.

Some cranial-nerve pieces exist: inferior CN III FJ1293/FJ1344, superior CN III FJ1321/FJ1372, left optic FJ1313/FJ1772, right optic FJ1364/FJ1819, trochlear FJ1330/FJ1381. This does not establish a complete twelve-nerve passage model. Named-part search did not establish a TMJ/masseter/temporalis/pterygoid teaching assembly. The source “articular disk of symphysis” maps to intervertebral disks, not a TMJ disk. Mandible selectability is not jaw-kinematics validation.

## Independent inner-ear reference

Existing IDs: `IE-COCHLEA-L/R`, `IE-VESTIBULAR-COMPLEX-L/R`, `IE-TEMPORAL-BONE-L/R`. Temporal source objects are `Temporal bone.l/.r`; concepts are `inner-ear-reference:left-temporal-bone` and `inner-ear-reference:right-temporal-bone`.

Each temporal has 7,051 vertices/14,094 triangles; each cochlea 3,110/6,168; each vestibular complex 4,316/8,580. Prior records report closed temporal surfaces with zero non-manifold/degenerate elements; those checks were **not rerun**. More triangles do not certify small canals.

Source metres have X left, Y posterior, Z superior; display uses only `(x,z,-y)`. No translation, scaling or per-object registration; `compatibleWithMainAtlas: false`, source sex unspecified. Do not fuse this specimen into TARO. Blender SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`.

Temporal bones retain the general Z-Anatomy CC BY-SA 4.0 basis. Cochlear/vestibular geometry is conservatively CC BY-NC-SA 4.0; Dundee association is inferred at archive level, not per-object certification. The combined package remains noncommercial under conservative handling. Semicircular canal names are text/two-vertex connectors, not independently polygonal canals; separate sensory/membranous compartments and organ of Corti are unestablished. [Manifest](../../../public/models/inner-ear-reference/atlas.json), [review](../inner-ear-reference-review.md), [attribution](../../../public/ATTRIBUTION.md).

## Goal-to-evidence routing

| Learning goal | Current basis | Next evidence needed; no implementation selected |
| --- | --- | --- |
| 22 bones and side | Separate surfaces, labels, shared frame | Target views and expert identity review; no new geometry need established. |
| Sutures/contributors | Adjoining bones | Reviewed seam/boundary and participants; annotation first if geometry supports it. |
| Inside/outside | Orbit, visibility, double-sided surfaces | Confirm actual inner surface; double-sided rendering creates no thickness. Whole-bone removal is not a cap cut. |
| Foramina/canals | Whole bones | Review opening, bony owners, entrance/exit and course; a void need not become a solid mesh. Notch/foramen variation must not be “repaired” to match a label. |
| Passage contents | Some nerve pieces | Identity, course, spatial registration and relation; schematic lines must be labelled as schematic. |
| Inner ear | Separate six-part reference | Fine targets and missing compartments within its own frame; no blind fusion. |
| Separation/jaw motion | Generic reversible translations and mandible | Authored educational paths versus separately reviewed physiological kinematics. |

Anatomical checks and source rights are detailed in [learning content](learning-content.md); existing and proposed mechanisms in [interaction research](interactions-and-pedagogy.md). No geometry was downloaded, imported, registered, edited, or newly rendered for this research.
