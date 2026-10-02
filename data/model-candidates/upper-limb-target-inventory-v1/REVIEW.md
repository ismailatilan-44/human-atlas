# Shoulder–axilla–arm target inventory candidate v1

This is next-region P3 planning, not a new active dataset or regional acceptance. Only this directory was written. Root owns integration. Observed Git HEAD was `0a501618801a5fbc8db44599d24eb50dfde0fba4`, with concurrent root-owned foot-support working changes. No labels, anatomical relationships, geometry, app files or Git state were changed by this task.

The frozen scope contract retains all four families and its full Turkish requirement text: girdle/shoulder/elbow joints, capsule/labrum/ligaments; all regional muscles, heads, tendons and sourced attachment regions; plexus/terminal/cutaneous branches and arteries/veins/lymph; regional compartments/passages. Nothing is narrowed to the structures already modeled. The prior 65 coverage rows remain pilot evidence, never the regional denominator.

## Candidate counts and limits

There are 352 bilateral targets from 176 unsided proposed requirements: 100 skeletal/support, 76 muscle/head/fascia, 164 neurovascular/lymph, 12 compartments/passages. D1/D2 requirements are proposed and expert-pending. None is anatomically accepted, and the inventory explicitly remains non-exhaustive.

- 132 targets have observed selectable source mesh memberships; six more have registered attachment-reference points only, producing 138 manifest-or-anchor observations.
- Eight existing concepts have no mesh. The two medial humeral midshaft attachment concepts remain explicitly unresolved/unanchored.
- 204 targets have no positive complete-target binding in the bounded active-source audit. This is not an absence claim. Some have related source-piece evidence, such as the bilateral medial brachial veins.
- Fourteen targets involve source selections containing multiple mesh parts. A group selection is not an independently segmented whole structure or every required substructure.
- 334 targets use exact unsided numeric pinned TA2 terms. Eighteen custom/detail targets (bilateral C5–T1 contributions, medial humeral midshaft regions and three named passage requirements) withhold exact Latin; per-root records retain only the generic roots term as supporting scope.

`proposal.json` includes every stable candidate ID, side, detail, term row/CSV line, dataset-qualified representation, full observed part list and counts/bounds, required relationship types, existing relationship IDs, coverage links and unresolved criteria. Exact source names and IDs are preserved. No inferred laterality compound, formal FMA/TA2 crosswalk, new relationship, or label activation is proposed.

## Material findings for integration

The registered plexus supplies three trunks, six divisions and one posterior cord per side. Its ten-part per-side selection is explicitly partial. C5, C6, C7, C8 and T1 contribution requirements, medial/lateral cords and separately named terminal/cutaneous/motor branch targets remain visible even without bindings. The source root bundle's ambiguous superior/communicating components cannot be assigned to C5–T1 by position or spline count. The registered median and musculocutaneous curves do not close the requirements for their distal continuations or individual branches.

The six existing coracoid/supraglenoid/radial-tuberosity markers are attachment-region reference points with preserved source registration residuals and limitations. They do not segment the entire bone landmark. Both coracobrachialis humeral attachment-region markers remain null; a whole-humerus center or guessed endpoint cannot satisfy them.

Whole pectoralis major concepts FMA13373/FMA13374 select only the source abdominal and sternocostal pieces; the clavicular part is separately present. The two-part source membership is retained and full-muscle extent remains unaccepted. Trapezius/deltoid/triceps and other whole-muscle targets also retain related named head/part evidence without manufacturing a new whole-muscle selection. TA2 pectoralis “head” versus source “part” terminology remains a scope correspondence review, not an accepted crosswalk.

Brachial veins are plural TA2 targets. The main model contains right medial brachial vein FMA22935/FJ2341 and left medial brachial vein FMA22936/FJ2313; those exact memberships are related evidence, not a full paired-vein or tributary-group binding. No vein or lymph absence is inferred. All six named axillary-node group requirements stay visible; further lymph vessels/routes remain an unexpanded requirement.

The source ISA element table alone undercounts some active arterial selections. For example, left subscapular artery FMA22679 selects FJ2221/FJ2246/FJ2253, while its direct ISA row contains only FJ2246. The retained PART-OF membership explains the complete active selection. Both table row sets are recorded and exact rendered membership parity is checked against the applicable set. The audit does not relabel those descendant pieces as one independently authored arterial trunk.

Required relationships distinguish attachment/articulation, muscle origin/insertion/innervation, nerve branch/source membership, arterial branch/supply, venous drainage, lymph routing and passage boundaries. These are requirements, not new anatomical claims. Existing graph relation IDs are evidence only; they do not complete the required set or pass expert acceptance. Fine tendons, attachment footprints, capsule/bursa/ligament detail, further branches and regional passages remain expressly unexpanded where individual source evidence is insufficient.

## Evidence and reproducibility

Exact terminology is from the locally pinned [TA2 CSV](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv), SHA256 `0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974`. Numeric rows are kept separate from absent/custom specific terms. The active main manifest is BodyParts3D 4.0; no 4.3 substitution occurs. Retained official [ISA names](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_parts_list_e.txt), [ISA memberships](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt), [PART-OF names](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_parts_list_e.txt) and [PART-OF memberships](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_element_parts.txt) are used with actual manifest/graph membership. LATEST URLs are provenance locators, not claims about today's remote version. No external fetch was needed.

Only registry-listed extension manifests and landmarks contribute active observations. Registered upper-arm/median curves, partial plexus, pilot/rotator metadata and existing graph evidence preserve their source frame, registration limits and separate attribution. No geometry, medical completeness or redistribution-rights review is claimed here.

`frozen-inputs.json` pins the mutable graph, coverage, scope contract/document and their original full-file hashes at `2026-10-02T11:53:20.753847+00:00`. It records local working-state observations, not a deployed source revision. The producer verifies retained static source hashes, and subsequent root foot changes cannot silently change the frozen graph. `--refresh-inputs` is explicit and should only be used after reviewing the changed sources; default generation and `--check` use the frozen snapshot.

Validation actually run: producer generation and `python3 data/model-candidates/upper-limb-target-inventory-v1/build.py --check`; unique bilateral IDs, all four family requirements, mandatory C5–T1 and cord requirements, exact source-table names/memberships, finite nonempty registered part geometry metadata, manifest/graph parity, six reference markers and retained two unresolved landmarks. No UI, geometry visual, anatomy-expert, build, deployment or release acceptance was performed.

Next owner action: root reviews this additive planning contract, resolves source-group/term correspondences, then chooses the next independently verifiable P3 geometry/relationship package. Do not promote the entire planning inventory as completed coverage.

## Root activation and term correction — 2 October 2026

The immutable proposal above remains historical planning evidence. Root activated all 352 requirement IDs in `data/anatomy/regional-targets-upper-limb-v1.json`; 350 full target values remain identical. Two bilateral superior-lateral-brachial-cutaneous records require a correction: pinned row6442 has English upper-arm scope but a Latin femoral-region term. `term-corrections.json` preserves that original value and cites the independently inspected IFAA A14.2.03.061 remedy, `Nervus cutaneus lateralis superior brachii`. The source CSV and original proposal are unchanged; this is a separately evidenced terminology correction, not a formal ontology crosswalk. The active seed has332 unchanged pinned Latin values, two separate primary corrections and18 unresolved exact terms. The historical334 populated pinned fields must not be read as334 independently accepted terms.

`scripts/build-upper-limb-targets.py` rechecks current source memberships, graph/marker endpoints and the preserved bilateral requirements; the general inventory retains unbound targets. Activation is work-scope acceptance only. Runtime geometry, labels, relationships, regional completeness and expert acceptance are unchanged/pending. The next P3 package is an independent source-frame nerve reference, with plexus root/cord identity and main-body registration handled separately.
