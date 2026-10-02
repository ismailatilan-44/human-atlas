# Upper-limb target bindings v2 — candidate

This version proposes **80 additive observations** from the independent upper-limb-nerve-reference against the existing 352 requirements. All 352 target IDs, exact term evidence and corrections, previous representation objects, existing relationship IDs, required relationship types and expert/region criteria are preserved. **272 complete target records remain byte-equivalent after JSON parsing.** No version-1 file, active data, application, public asset, shared script, document or Git state was written by this worker.

The result is a candidate new seed in proposal.json, not an active or published requirement version. Source geometry membership is an observation; every target remains incomplete, anatomically unaccepted and expert-pending.

## Additions and remaining observations

| Observation | Count |
| --- | ---: |
| New reference bindings | 80 |
| Primary nerve/group target bindings | 46 |
| Existing nerve context target bindings | 24 |
| Bone context target bindings | 10 |
| Previously empty representation list, now source-reference observation | 38 |
| Previously meshless canonical concept, now source-reference observation | 8 |
| Additional reference alongside prior main-body geometry | 34 |
| Newly geometry-observed targets across datasets | 46 |
| Targets unchanged | 272 |
| Targets still without any positive representation binding | 166 |
| Existing unresolved humeral reference targets | 2 |
| Expert-accepted targets | 0 |

The v1 total of 132 mesh-observed targets becomes 178 across datasets; the six attachment reference-point targets remain separate. There are 184 manifest-or-anchor observations. These are target-level observations, not anatomical completion counts, and the new reference does not change the main body's geometry.

Eight new bindings represent exact plural muscular-branch requirements and plural source objects. They do not identify separate numbered branches, individual muscle endpoints or a complete branch set. Fourteen protected requirements—bilateral C5–T1 contributions and medial/lateral cords—remain unbound and unchanged. The separate BP3D 4.3 intake contributes no representation.

Forty-seven objects in the 127-object source reference have no eligible exact requirement in this unchanged 352-target scope. They remain in the reference and are listed in binding-diff.json; no new requirement, generic substitute or root identity is fabricated to force a binding. This includes source context and forearm branch objects outside this bounded planning seed.

## Evidence gates

Each added observation passes all of these independent checks:

1. Exact numeric unsided terminology ID, English pair and sourced Latin agree with the preserved target term. Both 6442 labels use the separately corrected IFAA term, and the original wrong-region Latin remains in target evidence.
2. Side agrees between requirement, metadata label, source object mapping and manifest part.
3. The exact source object, concept ID, part ID and nonempty evaluated mesh agree across the pinned geometry manifest and metadata audit.
4. Named-group requirements bind only to matching plural authored groups; named structures are never satisfied by their parent collection or a generic term.

No fuzzy name search, table hierarchy, geometric proximity, general-to-specific term substitution or group-to-individual inference creates a binding. All prior representation records remain at their original indices. Changed binding-status observations retain their v1 status and source hash in bindingObservationHistory.

SourceRole distinguishes primary objects from context. Each binding includes the object's exact source extent, control-point endpoints, group/remnant caveats, display-frame matrix and scope note. The frame is an independent reference with no main-body registration. The old main-body identities remain intact: for example, the subscapular source objects use the existing upper/lower canonical IDs, while bone source IDs stay dataset-scoped rather than being merged into the historical main-body FMA IDs.

## Frozen inputs and reproduction

The active v1 seed was copied into this directory's frozen-inputs.json before proposing changes. The producer does not reread a mutable graph or alter the v1 seed. It checks hashes of the final immutable 127-object source manifest and the complete label/source-evidence handoff.

Pinned source manifest: data/model-candidates/upper-limb-nerve-source-audit-v1/atlas.json; SHA-256 299f9eb315dc6ecbb4bdcbd388884595aeed0395a5cdb6d27be20b5e1c5642d0. Pinned blend SHA-256: 9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd. The source's separate attribution and provenance limitations continue to apply.

Run:

    python3 data/model-candidates/upper-limb-target-bindings-v2/build.py
    python3 data/model-candidates/upper-limb-target-bindings-v2/build.py --check

Both passed. Checks establish 352 stable IDs, 80 additive changes, 272 unchanged records, preservation of every prior representation and term correction, eight same-scope group bindings, 14 protected open requirements and no forced use of 47 unmatched source objects. No runtime, build, publication or expert check is claimed here.

The sourceManifest field intentionally points to the frozen candidate file. runtimeManifestExpected records the intended public path without claiming it exists or passed acceptance when captured. Root must confirm final runtime concept/part membership, search → selection → context → relationship → return flow, and the deployed source revision before activating this candidate. Do not describe the source-only frame as registered to the main body. No region or expert criterion is closed by this proposal.
