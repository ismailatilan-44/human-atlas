# Foot and ankle support metadata candidate v1

Baseline `0a501618801a5fbc8db44599d24eb50dfde0fba4`; inspected 2026-10-02. Only this candidate directory is owned by this task. Root owns active data, app, target integration and release; the geometry worker owns the source audit/package. No active files or Git operations are performed here.

`proposal.json` supplies 20 dataset-scoped reference labels, 2 main labels, 20 additive non-exhaustive source-scoped target proposals, and 32 selected attachment relationships (28 reference, 4 main). All 22 labels have exact scoped numeric Latin terms. Turkish is editorial and every anatomical acceptance remains pending. The 136 prior v3 target IDs are consumed and hashed; this producer does not alter them or create selection-group/part-of concepts.

## Exact identity and term scope

| Source name (bilateral) | Numeric TA2 row / CSV line | Exact Latin |
|---|---|---|
| Flexor retinaculum of ankle | 2714 / 2812 | Retinaculum flexorium tali |
| Superior extensor retinaculum of ankle | 2712 / 2810 | Retinaculum extensorium superius tali |
| Inferior extensor retinaculum of ankle | 2713 / 2811 | Retinaculum extensorium inferius tali |
| Superior fibular retinaculum | 2715 / 2813 | Retinaculum fibulare superius |
| Inferior fibular retinaculum | 2716 / 2814 | Retinaculum fibulare inferius |
| Plantar aponeurosis | 2718 / 2816 | Aponeurosis plantaris |
| Long plantar ligament | 1934 / 2033 | Ligamentum plantare longum |
| Plantar calcaneocuboid ligament | 1940 / 2039 | Ligamentum calcaneocuboideum plantare |
| Plantar calcaneonavicular ligament | 1937 / 2036 | Ligamentum calcaneonaviculare plantare |
| Intersesamoid ligament | 1963 / 2062 | Ligamentum intersesamoideum |

Each row applies to one `.l` and one `.r` source object, with distinct `zanatomy:` concept and `ZA-LLR-` part IDs. The exact geometry-worker mapping is consumed rather than reconstructed from names. Side remains a separate field; TR/EN/LA canonical labels are unsided so the existing dataset display can add its side suffix. Search aliases preserve the exact dotted source object name and exact Latin term. No invented Latin declensions, numbered substructures, formal FMA crosswalk, synonyms or fine attachment identities are introduced.

The [pinned TA2 source CSV](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) is locally available, SHA256 `0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974`. Numeric rows—not starred custom source rows—provide every exact term above. No new external fetch was needed for this bounded mapping; verification dates describe retained-source inspection, not a fresh remote availability claim.

## Main atlas binding evidence

Only these two sided BodyParts3D 4.0 manifestations have positive exact bindings in the bounded audit:

| Concept | Exact official source name | Part | Name-table line | Membership line |
|---|---|---|---|---|
| FMA44249 | right long plantar ligament | FJ1424 | 1572 | 5709 |
| FMA44250 | left long plantar ligament | FJ1424M | 1573 | 5710 |

The manifest and knowledge entity agree on each one-part membership. Right geometry has 1,417 vertices / 3,780 indices; left has 1,419 vertices / 3,798 indices, with finite recorded bounds. These establish separately selectable source parts, not source-to-reference geometric equivalence or expert correctness. The exact retained official [names](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt) and [memberships](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt) are hashed and each relevant row is embedded in `mainBindingAudit`. Their URLs say LATEST; the active manifest's actual BodyParts3D 4.0 identity governs this audit, with no 4.3 substitution.

Existing unsided FMA44248 selects FJ1424 and FJ1424M (name row1571; membership rows5707–5708). Its exact two-part list and source rows are recorded in `existingParentEvidence`; it receives no new label or relationship. Existing wrist retinacula were excluded because their scope is wrist, despite matching the generic retinaculum word. Searches of the retained official names/part-of names, memberships and actual manifest included retinaculum, aponeurosis, plantar/calcaneocuboid/calcaneonavicular/intersesamoid names and older laciniate, spring, annular and peroneal variants. No additional positive binding emerged; this is not an absence claim.

## Source representation and student notes

All 20 evaluated source objects are independently named meshes with one connected component each and verified side. The source evaluator reports no zero-area triangles, loose vertices or non-manifold edges. This is geometry evidence; it does not prove anatomy. The candidate export additionally records five local nonpositive averaged-normal triangles per long plantar ligament, disclosed as possible small shading defects; no vertex-normal cancellations are present. Exact topology, base/evaluated counts and authored modifiers are retained under each reference label's `sourceRepresentation`.

- Inferior fibular retinaculum has 27 open boundary edges per side; plantar aponeurosis has 72. Their student notes describe an open thin surface whose visible thickness is not a tissue measurement. The aponeurosis source enables Solidify for render but disables it in the viewport; the package preserves the evaluated viewport sheet without healing it.
- The four other retinacula have authored approximately 1 mm Solidify. This authored display thickness is not claimed to be anatomically measured thickness.
- Plantar calcaneocuboid starts at 12 vertices / 6 faces and calcaneonavicular at 4 vertices / 1 face; each uses viewport Subdivision1 (render2) and approximately 0.5 mm Solidify. Intersesamoid starts at 15 vertices / 8 faces with approximately 0.5 mm Solidify. Their notes state that simple source surfaces represent the overall shape, with detailed fiber arrangement and real thickness unverified.
- Long plantar ligament is an unmodified named source mesh (1,741 vertices / 3,486 triangles each side). Its selectable object is not separate named layers or bundles; the student note explicitly leaves those and exact attachment regions unresolved. Main atlas labels get their own representation note and do not inherit reference mesh defects or modifier facts.

No attachment, innervation, contact or part-of relationship is inferred from a Blender parent/collection, spatial proximity, source name or connected-component count. Source mapping language “Complete named source object” means the authored object is retained; it is not a claim of complete ligament/fascia anatomy or regional completeness.

## Selected sourced attachments

The requested attachment expansion was independently verified on 2026-10-02 in the [TTUHSC joints table](https://anatomy.ttuhscep.edu/musculoskeletal_system/joints_lower_tables.html), [anterior/lateral leg table](https://anatomy.ttuhscep.edu/musculoskeletal_system/leg_tables.html), and [full leg table](https://anatomy.ttuhscep.edu/schemes/leg_tables.html). Exact row/column locators accompany every edge. Per side, selected endpoints are:

| Support | Whole-bone context endpoints; text-qualified region |
|---|---|
| Long plantar | Calcaneus, cuboid; remaining endpoints unresolved |
| Plantar calcaneocuboid | Calcaneus, cuboid; inferior regions |
| Plantar calcaneonavicular | Calcaneus sustentaculum tali, inferior navicular |
| Plantar aponeurosis | Calcaneal tuberosity only |
| Flexor retinaculum | Tibial medial malleolus tip, calcaneus |
| Superior extensor retinaculum | Tibia and fibula proximal to malleoli |
| Inferior extensor retinaculum | Anterosuperior calcaneus only |
| Superior fibular retinaculum | Fibular lateral malleolus tip, calcaneus |

These14 unsided endpoint facts yield28 same-side reference edges. The existing main long plantar sources receive four same-side edges to verified calcaneus/cuboid concepts (left FMA24498/FMA24529, right FMA24497/FMA24528). Inferior fibular and intersesamoid supports receive no guessed edge.

Every edge uses `attaches_to`, an explicit top-level Turkish attachment region note, whole-bone context semantics and `expertReview: pending`. Typical unsided facts are instantiated on each side without validating either source specimen. No coordinates, model footprint, contact, named fine layers or complete endpoint set is asserted.

[Ward and Soames1997](https://pubmed.ncbi.nlm.nih.gov/9347303/) reports variation of ligament shapes, bands and attachments in59 cadaver feet (PMID9347303; DOI10.1177/107110079701801009). Direct PubMed open failed; the indexed primary abstract was readable. [Hiramoto's primary journal abstract](https://www.jstage.jst.go.jp/article/ofaj1936/60/6/60_401/_article) describes variable metatarsal attachment patterns. Consequently, the teaching table's metatarsal endpoint list is not projected onto this source object; only calcaneus/cuboid are linked. This is a deliberate incomplete boundary, not an anatomical absence claim. No source table prose or images are redistributed.

## Provenance, validation and handoff

Pinned Startup.blend SHA256 is `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. The existing [Z-Anatomy source](https://github.com/Z-Anatomy/Models-of-human-anatomy) and BodyParts3D provenance/licenses remain separate. This task inspects retained metadata and evaluates no new distribution rights. Source geometry, coordinate-frame preservation, normal/export quality and component attribution are owned by the source audit; active local interaction, publication and expert acceptance are owned by root.

`inputSnapshots` hashes the exact source mapping/evaluation, pinned terms, retained source tables, main/reference manifests, active label/graph metadata, prior136 targets and producer. The consumed active reference manifest is still the baseline119 at this handoff; the separate source-candidate139 manifest is also pinned and its20 new object/part bindings verified. A source candidate is not an active release claim.

Checks actually run: producer generation plus `python3 data/model-candidates/foot-support-metadata-v1/build.py --check`; exact20 source names/IDs/side and evaluated selectable geometry; expected open boundaries, component and nondegenerate topology assertions; exact numeric term count; main table/manifest/graph membership parity; two main concept/two part count; no old-target ID collision and existing family compatibility. Active identical labels are allowed while conflicting labels fail, making regeneration after integration idempotent. Source rows and geometry membership are checked even when labels are already active. The 32 distinct relation IDs resolve only within their own dataset; 28 reference and4 main are counted. Existing identical relation records are accepted and conflicts fail. There are zero expert-accepted targets. No app/UI/build/deployment checks were run by this metadata task.

Root can freeze `activation-proposal.json` when taking ownership, integrate these candidate records, then regenerate and run `--check` to refresh consumed hashes after the final139 package and labels. Remaining acceptance: real source-specific search → selection → focus/context → return, source shape/extent and term expert review, unresolved fine layers and attachment footprints. Timing/rework is recorded in `timing.json`.

## Root integration disposition — 2 October

Ownership transferred to root. The historical handoff above consumed the 119 baseline; the refreshed proposal consumes the 137 active package and separate 139 candidate. `activation-proposal.json` freezes the reviewed activation content independently of later input-hash refreshes. Eighteen reference labels and all 28 reference/four main sourced facts are active locally; the two intersesamoid labels/targets remain candidate-only because source-space geometry does not span the modeled sesamoid components. No relationships involve these withheld objects.

All 32 facts preserve their top-level Turkish attachment note and also carry the identical `qualifiers.attachmentNoteTr` required by the main explorer's visible-note contract. The initial explorer generation caught the missing qualifier. After that focused adapter correction, knowledge/explorer generation and interaction checks passed. No source fact, geometry, endpoint or expert status was changed by this display correction. Product/browser/publication evidence belongs to the owning action report; this metadata review does not substitute for it.
