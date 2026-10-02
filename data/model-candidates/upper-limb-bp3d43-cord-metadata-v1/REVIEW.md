# Two left BP3D 4.3 cords — candidate metadata

This package covers exactly **two left cord objects**, with two TR/EN/Latin labels, two source concepts, three direct anatomical relationship candidates and two separately deferred contribution facts. It does not activate geometry, modify main/reference labels or graph, accept the other 15 neural files, mirror a right counterpart or close any C5–T1 contribution requirement.

## Preserved source identities

| Source part | Returned representation | Returned concept | Exact returned name | Candidate export part |
| --- | --- | --- | --- | --- |
| FJ4274 | BP29122 | FMA45239 | Lateral cord of left brachial nerve plexus | BP43-FJ4274 |
| FJ4275 | BP29196 | FMA45241 | Medial cord of left brachial nerve plexus | BP43-FJ4275 |

The original official OBJ header lines 2–7 and version-matched FMA2Obj membership rows 1446–1447 establish these pairs. Each is_a file-membership row contains the corresponding single FJ object; it is not an anatomical branching edge. The broad catalog assignment FMA11195 remains a documented discrepancy and never replaces either returned concept ID.

The current main graph and label registry were checked before proposing IDs: neither FMA45239/FMA45241 nor a differently identified lateral/medial cord concept was present. The candidate therefore retains the actual returned FMA identities, with the geometry owner's distinct export part IDs and original FJ/BP IDs in separate fields.

Pinned TA2 rows 6415/6417 provide the exact unsided English/Latin cord pairs: Fasciculus lateralis plexus brachialis and Fasciculus medialis plexus brachialis. Left laterality comes from the actual OBJ names/identifiers and remains a separate label field. Turkish translations are editorial. This terminology correspondence is not a newly asserted formal FMA/TA2 ontology crosswalk.

## Selected relationships

The [University of Michigan BlueLink lab page](https://sites.google.com/a/umich.edu/bluelink/curricula/m1-foundational-anatomy/sequence-7-neuroanatomy/brachial-plexus-subclavian-vessels-scalene-muscles/lablink), inspected 2026-10-02, gives explicit anatomical meaning:

- Step 9 names the medial and lateral cords as components of the brachial plexus. Two candidate part_of edges point to the existing left plexus concept.
- Step 14 identifies musculocutaneous as a terminal branch of the lateral cord. The existing left musculocutaneous concept is the subject of one branch_of edge to FMA45239. [TTUHSC's nerve table](https://anatomy.ttuhscep.edu/musculoskeletal_system/axilla_tables.html), musculocutaneous/Source and lateral cord/Branches, corroborates the parent.
- Step 12 describes median formation through lateral and medial contributions/roots from the respective cords. Two contributes_to facts are recorded separately in deferredRelations with mandatory viaStructure qualifiers. They are not direct median branch_of edges, innervation claims or new root entities.

The two part_of edges describe anatomy, not file membership or automatic changes to the existing ten-part Z-Anatomy plexus selection. The current partial selection must remain accurately scoped; root owns any later geometry grouping decision. The branch edge does not claim physical contact between the independently sourced BP3D cord and Z-Anatomy musculocutaneous meshes.

The contribution facts require explicit predicate semantics and visible via-root qualifiers before graph activation. If the current renderer cannot retain that meaning, leave them as evidence. No C5–T1 root level, fascicular path, bridging geometry or complete nerve territory is inferred.

## Geometry, rights and gates

Source index-component counts are retained as technical observations, never named branches. Geometry/native-frame/holdout/continuity and source-defect interpretation belong to the separate geometry audit. This package makes no acceptance judgment based on its measured distances or component counts. datasetId remains null until root's narrowly scoped geometry decision; exported part mapping is verified without assuming the full source candidate is released.

The intake's official live source license is CC BY-SA 2.1 Japan, with DBCLS/BodyParts3D attribution retained separately. Do not replace it with the base atlas license or infer blanket permission from Z-Anatomy terms. The original source OBJ SHA-256 values, version/header facts and intake rights record remain in frozen-inputs.json and source-evidence.json. University references supply selected anatomical facts only; no donor images, multimedia or page prose are copied.

Only this candidate directory was written. No active application, data, public model, shared script, documentation or Git file was changed. Remaining gates are root geometry acceptance for these two objects, label/relationship projection, preservation of the parent selection's partial scope, runtime product checks and expert review. Other neural objects, all right-side and root-contribution requirements remain open.

## Checks and handoff

Both commands passed:

    python3 data/model-candidates/upper-limb-bp3d43-cord-metadata-v1/build.py
    python3 data/model-candidates/upper-limb-bp3d43-cord-metadata-v1/build.py --check

They verify original object hashes, actual FJ/BP/FMA header values, official membership rows, exported IDs, no frozen main identity conflict, two left labels, three resolved direct relation endpoints, two qualified deferred contributions and no root/right/innervation expansion. No geometry acceptance, runtime, build, publication or anatomical expert check is claimed. Ownership passes to root after this handoff.
