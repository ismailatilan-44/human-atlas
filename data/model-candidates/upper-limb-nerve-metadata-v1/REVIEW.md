# Upper-limb nerve metadata candidate v1

This handoff labels all **127 source objects** in the root-selected independent upper-limb-nerve-reference: 54 new nerve/group curves, 24 previously used nerve context curves and 49 bone context objects. All have Turkish and English labels; 110 have exact sourced Latin and 17 retain explicit null Latin. It adds 26 selected, cited anatomical branch_of candidates. No active app, graph, label, coverage, public model, shared script, document or Git file was written by this worker.

The main-body frame was not accepted for this package. Choosing a separate source frame does not confer main-body geometry on existing concepts. Runtime, publication and anatomical expert acceptance remain root-owned. Observed root revision was 0ac477f; the older delivery handoff records caa938a, and the 352-target frozen planning candidate records 0a501618. Those are different historical states, not interchangeable release evidence.

## Identity and source scope

The frozen input retains the geometry owner's final source-object → part → concept mapping, evaluated source extent and spline checks. Pinned blend SHA-256: 9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd. Final source-frame manifest SHA-256: 299f9eb315dc6ecbb4bdcbd388884595aeed0395a5cdb6d27be20b5e1c5642d0.

Source names, source-frame bounds, exact control-point endpoints, authored spline counts and IDs remain evidence. They are source observations, not anatomical terminal landmarks or accepted individual nerve territories. Source collections are retained without converting them into anatomical parent edges.

Eight muscular-branch selections are plural source groups: axillary, median, radial and ulnar on each side. Each remains one authored object even when it contains several splines; no numbered muscle branches or per-spline innervation are invented. Each ulnar object contains one single-point, geometry-free spline and a 12-point main spline; the remnant is disclosed and not counted as a visible branch.

The 24 older nerve curves are re-used as context in the same source frame. Existing main geometry and registration remain separate. The 49 bones retain source zanatomy IDs, including 16 carpals; no name-based merge with a main-body FMA concept occurs. Cervical bone context does not prove C5–T1 nerve-root identity. The source audit separately observed bilateral Subclavian nerve objects outside the agreed 27-base handoff; they are deferred, not declared absent.

The source's component attribution, license limitations and object-lineage caveats remain owned by the geometry intake and accompanying attribution. This package neither relicenses the source nor treats the archive's general declaration as blanket component clearance.

## Exact terms, custom rows and source defect

The pinned upstream TA2 CSV has SHA-256 0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974. Numeric unsided rows supply 108 labels; source laterality remains separate and no Latin side compounds are generated. Turkish labels are editorial and await expert review. Existing canonical labels are preserved where present.

Pinned row 6442 pairs the English superior lateral brachial cutaneous nerve with a Latin field naming a femoral region. The original value is retained in source-evidence.json, explicitly rejected for display, and never edited in the source CSV. Both display labels instead use **Nervus cutaneus lateralis superior brachii**, separately verified on the [IFAA terminology-rules page](https://ifaa.unifr.ch/Public/EntryPage/TA98RATChangesNew.html), code A14.2.03.061, Remedy column. This is an independently cited correction, not validation of the erroneous cell. The FIPAT Part 5 direct fetch failed; no downloaded PDF is claimed.

Seventeen numbered bone labels keep null Latin: bilateral ribs 3–8 and vertebrae C3, C4, C5, C7 and T2. Their exact source-named rows are starred/custom; numeric generic rib/cervical/thoracic terms are recorded separately and never substituted as the exact numbered label. T1 uses independently present numeric row 1063, First thoracic vertebra, while preserving custom source-name row 1063*1. C6 has exact numeric source row 1055. No custom entry is reported as a verified numeric term.

## Existing graph bindings and relationships

Eight existing meshless concepts match the new curves. Four already matched directly: bilateral suprascapular and axillary nerves. Four provisional IDs were reconciled before the immutable geometry handoff:

| Exact source object | Retained canonical concept |
| --- | --- |
| Superior subscapular nerve.l | atlas:left-upper-subscapular-nerve |
| Superior subscapular nerve.r | atlas:right-upper-subscapular-nerve |
| Inferior subscapular nerve.l | atlas:left-lower-subscapular-nerve |
| Inferior subscapular nerve.r | atlas:right-lower-subscapular-nerve |

Source names and part IDs are unchanged. Identical TA2 rows 6428/6429, exact labels and side establish the nomenclature correspondence. The binding audit preserves all eight original entities and **10 existing main-body motor relations** without alteration. Those relations have muscle endpoints outside this reference and are not imported as its new edges. Their main-body missing-geometry qualification remains valid. Future cross-dataset navigation or geometry-state updates require root integration.

The 26 new branch candidates use exact mapped same-side endpoints and inspected primary university teaching tables: [TTUHSC shoulder/arm](https://anatomy.ttuhscep.edu/musculoskeletal_system/axilla_tables.html) and [forearm/wrist](https://anatomy.ttuhscep.edu/musculoskeletal_system/forearm_tables.html). Every edge includes its Nerves table row/column locator. Selected facts connect suprascapular to the superior trunk; upper/lower subscapular, thoracodorsal, axillary and radial to posterior cord; selected cutaneous branches to their parent nerve; deep/superficial radial branches to radial; and anterior interosseous to median.

The branch_of direction is child → named anatomical parent. It is not transitive, generic part_of, source collection membership, model contact or a complete course. No new innervation is inferred.

The posterior interosseous/deep radial relation is withheld: the university source discusses differing definitions, including synonymy, continuation and a distal articular branch. Distinct source object names alone do not resolve that ambiguity. Anterior/posterior medial antebrachial cutaneous branches have verified labels, but no additional connectivity evidence was audited for this relation set. No medial/lateral cord or root entity is manufactured to close a parent path.

## Reproduction, ownership and remaining gates

Run:

    python3 data/model-candidates/upper-limb-nerve-metadata-v1/build.py
    python3 data/model-candidates/upper-limb-nerve-metadata-v1/build.py --check

Both commands passed. The producer checks frozen source-handoff hashes, 127 unique concept/part/object bindings, 26 unique ipsilateral relation endpoints, numeric/custom term handling, preservation of existing labels and facts, source-group scope and two geometry-free remnants. Default reproduction uses the retained graph snapshot; concurrent root changes cannot silently alter this audit.

The geometry owner replaced runtime pointer strings in custom-property serialization before the final freeze; IDs, coordinates and binaries did not change. This worker refreshed only its owned frozen evidence to the final source hashes. Identity reconciliation and the table defect were resolved before label activation. The extension from 54 to 127 labels followed root's explicit scope update.

Validation reports only candidate checks. No runtime interaction, build, deployment or expert anatomical check was performed here. Root owns projection into the independent reference, visibility of group/extent notes, search → selection → context → relationship → return validation, target-version observations and publication. The 352-target planning candidate and separate BP3D 4.3 intake were not edited.
