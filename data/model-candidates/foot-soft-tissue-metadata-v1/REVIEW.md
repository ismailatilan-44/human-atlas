# Foot soft-tissue metadata candidate v1

Baseline: `9e649b6bef0e589a6caa8b7391e10a132a304cea`. This directory is the complete delegated output. Root owns target/product integration, source package acceptance, active labels and release. No active files or Git state were changed by this task.

`proposal.json` contains 32 reference labels, 38 main labels (36 muscle concepts and 2 sesamoid concepts selecting 40 parts), 32 non-exhaustive source-scoped targets, 12 reference and 8 main relationship proposals. All expert acceptance counts are zero. 28 targets have directly observed main manifestations. Every main binding includes the official retained name row, every official membership row, manifest concept/part IDs, graph geometry membership, nonempty part counts and finite bounds. These are independently selectable source identities; anatomical geometry accuracy has not been assessed by this metadata task.

The frozen activation-proposal.json preserves the pre-activation87-part manifest/input snapshot. The refreshed proposal.json now consumes the119-part public reference and active label/graph hashes;it does not rewrite historical intake evidence. Root added the producer fingerprint and top-level reference attachment notes for the existing viewer contract. The 32 new source mappings and evaluated-source records are pinned independently. The producer checks exact source object and part bindings if they are already present in the reference manifest. Regenerate and run `--check` after integration to refresh consumed input hashes; existing identical labels/relations are permitted, conflicting entries fail.

## Identity and representation boundaries

- The 30 reference muscle objects include eight individually named FHB/adductor head objects and six plural lumbrical/interosseous group objects. Their IDs and sides are preserved. Parenthesized opponens identity stays explicit; no prevalence assertion.
- The reference lumbrical group has one connected mesh component. It does not establish four independent or numbered muscles. Main source has four individually named lumbricals and three individually named plantar interossei per side; all exact parts are listed below. Reference groups and main individuals are different source manifestations, never interchangeable meshes.
- Dorsal interossei have four components, plantar interossei three, EDB three. Connectivity does not establish numbered muscle/toe attribution. Reference abductor hallucis retains a tiny three-vertex defect beside the principal component; its disposition belongs to the geometry audit.
- Each sesamoid object has two components. Main source's singular sesamoid concept selects two separately identified parts. The proposed plural display describes that rendered selection without renaming the source ontology or inventing medial/lateral sesamoid identities. No added part-of relation.
- Main EDB and dorsal-interossei foot correspondence remains unresolved in this bounded official-name, membership and manifest audit. No absence claim or borrowed main binding is made.

| Source scope | Main source concepts (left; right) | Parts |
|---|---|---|
| (Opponens digiti minimi muscle of foot) | FMA86035; FMA86034 | FJ1399M, FJ1399 |
| Abductor digiti minimi of foot | FMA37464; FMA37463 | FJ1390M, FJ1390 |
| Abductor hallucis | FMA37460; FMA37459 | FJ1400M, FJ1400 |
| Dorsal interossei muscles of foot | No positive bounded match | — |
| Extensor digitorum brevis | No positive bounded match | — |
| Extensor hallucis brevis | FMA51145; FMA51144 | FJ1407M, FJ1407 |
| Flexor digiti minimi of foot | FMA37472; FMA37471 | FJ1391M, FJ1391 |
| Flexor digitorum brevis | FMA37462; FMA37461 | FJ1413M, FJ1413 |
| Lateral head of flexor hallucis brevis | FMA45974; FMA45973 | FJ1393M, FJ1393 |
| Lumbrical muscles of foot | FMA37718; FMA37720; FMA37486; FMA37484; FMA37717; FMA37719; FMA37485; FMA37483 | FJ1383M, FJ1385M, FJ1387M, FJ1389M, FJ1383, FJ1385, FJ1387, FJ1389 |
| Medial head of flexor hallucis brevis | FMA45972; FMA45971 | FJ1396M, FJ1396 |
| Oblique head of adductor hallucis | FMA46019; FMA46018 | FJ1398M, FJ1398 |
| Plantar interossei muscles | FMA37746; FMA37744; FMA37742; FMA37745; FMA37743; FMA37741 | FJ1384M, FJ1386M, FJ1388M, FJ1384, FJ1386, FJ1388 |
| Quadratus plantae muscle | FMA37466; FMA37465 | FJ1412M, FJ1412 |
| Sesamoid bones of foot | FMA45098; FMA45097 | FJ3266, FJ3270, FJ3372, FJ3376 |
| Transverse head of adductor hallucis | FMA46021; FMA46020 | FJ1445M, FJ1445 |

## Terms and evidence

The pinned [Z-Anatomy-distributed TA2 CSV](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv) hash is `0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974`. All 16 source scopes have numeric rows. Proposal labels retain exact row IDs, English/Latin source text, and one-based CSV lines. No starred custom row is treated as an official numeric identifier; no formal FMA/TA2 crosswalk is asserted. Sides are separate fields; Latin side compounds are not fabricated. Turkish is editorial and expert-pending.

30 reference Latin displays and 22 main Latin displays use exact numeric-row terms at their supported scope. The two reference and two main flexor digiti minimi labels withhold Latin because numeric row 2682 contains `Flexor digiti minimi pedis pedis`; correcting that source text is unresolved. Main source explicitly says “brevis”; its display preserves this distinction and its correspondence is pending expert review. Fourteen numbered main lumbrical/plantar-interosseous labels withhold Latin because only whole-group plural Latin is verified. The exact source group term remains in `genericTerm`; no singularization or appended Roman numeral is invented.

A synonym audit recovered the two quadratus plantae main bindings missed by the first literal-name scan. The [University of Fribourg TA98 lower-limb table](https://svx-uo7640ifaa2.unifr.ch/Public/EntryPage/TA98%20Tree/TA98%20EN/04.7.02%20TA98%20EN.htm), row A04.7.02.068, explicitly pairs Quadratus plantae and Flexor accessorius. This supports term correspondence; the main IDs and parts remain source-preserved. Latin still comes from pinned numeric TA2 row 2684. Verified through the indexed primary-source table on 2026-10-02; direct fetch returned 502. A TTUHSC-hosted TA2 PDF direct read timed out. These constraints are recorded; inaccessible fetches were not treated as negative evidence.

Main source tables are retained official [BodyParts3D names](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt) and [element memberships](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt). Their local hashes and exact rows are in the proposal. The active manifest identifies BodyParts3D 4.0; no 4.3 identity substitution was used. The URLs use upstream LATEST naming; this audit relies on the pinned retained files and actual active manifest rather than assuming today's remote version.

## Selected direct relations

[TTUHSC's anterior/lateral leg and foot teaching table](https://anatomy.ttuhscep.edu/musculoskeletal_system/leg_tables.html), read on 2026-10-02, directly names abductor hallucis and extensor hallucis brevis origins, insertions and innervation. Only these two whole named muscles receive candidates: same-side calcaneus origin and proximal hallux phalanx insertion in both datasets, plus medial plantar/deep fibular innervation respectively within the reference dataset. This is 20 selected edges, not an exhaustive attachment or nerve network. No head/group relationship inheritance occurs.

Each attachment has a Turkish region qualifier and states that the whole bone is context, with no exact model surface mark, footprint, contact, coordinates or segmentation. Innervation does not claim a modeled motor branch or entry point. Evidence is typical educational anatomy, not validation of either source specimen. All candidate endpoints resolve in their own dataset (existing manifest plus the exact new source mapping). The producer permits an already integrated identical relation and fails on conflicts; root must reuse that existing edge rather than append a duplicate.

## Intake and checks

Existing BodyParts3D and pinned Z-Anatomy inputs retain their distinct provenance and licenses. This task does not acquire or redistribute a new geometry source. The source worker owns Blender/export quality, frame, component-level attribution and inclusion rights. Term/teaching citations are used as bounded evidence, not copied full tables; source IDs, titles, URLs, locators, access dates and fetch constraints are retained.

Checks run: deterministic producer generation and `python3 data/model-candidates/foot-soft-tissue-metadata-v1/build.py --check`; exact 32 source objects/sides; evaluated selectable geometry; 38 main concepts with 40 unique parts and official membership parity; exact numeric term counts and null reasons; 20 distinct dataset-qualified relation endpoint checks; active-label conflict guards. No UI, build, expert or deployment acceptance claimed. Timings and the synonym-review rework are in `timing.json`.

Next: root integrates the source package and these reviewed-scope proposals, refreshes input hashes, and checks search → selection → focus/context → relationship → return. Expert review must resolve the listed terminology/aggregate and anatomical criteria before regional acceptance.
