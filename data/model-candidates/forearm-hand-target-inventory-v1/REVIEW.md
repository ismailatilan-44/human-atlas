# Forearm, wrist and hand — P4 requirement seed v1

Candidate planning handoff at source revision `e005d53a9cb22cda52c39fb318248a83ba113fe8`. Integration and release ownership returns to root. Only this directory was written. The September 26 delivery handoff is historical; this seed supplies no newer deployed or expert acceptance.

The observable outcome is a reproducible list of **502 bilateral named requirements** (251 unsided definitions), including open targets without positive geometry. All four families from the scope plan's `forearm-wrist-hand` row appear. There are 442 non-group requirements and 60 explicitly plural/group requirements; 162 are D1 and 340 selected D2. This is a bounded seed, not an exhaustive hand syllabus or completeness denominator.

| Family | Requirements | With positive manifest observations | Without positive bindings |
| --- | ---: | ---: | ---: |
| Skeletal/support | 162 | 62 | 100 |
| Muscle/tendon/fascia | 176 | 64 | 112 |
| Neurovascular/lymph | 140 | 62 | 78 |
| Compartments/canals | 24 | 0 | 24 |
| Total | 502 | 188 | 314 |

The 188 positively observed requirements carry **210 dataset-scoped observations: 160 main-body and 50 independent upper-limb reference**. Same concept IDs in different datasets remain different representations. These are exact source-name/member observations, not accepted whole structures. The source table and manifest names, FMA/project IDs, part IDs, source object names where available, source scope, laterality, nonzero counts and bounds remain in the evidence. Base membership is checked against retained official ISA/PART-OF tables. No new geometry, graph facts or UI labels were authored.

## Scope and identity decisions

The requirement selection covers radius/ulna, all eight named carpals, five metacarpals and fourteen digit-specific phalanges per side; selected wrist supports and individual MCP/IP/CMC requirements; regional extrinsic/intrinsic muscles, selected heads, tendons and sheaths; median/ulnar/radial branches, named arteries/veins and cubital lymph-node groups; forearm compartments, carpal/ulnar canals and selected hand compartments. Every row is bilateral as a requirement, regardless of the source's available geometry.

Numeric pinned terminology is preserved exactly, with raw source row and line. The Z-Anatomy table's `1265*1`, `1277*1` and related asterisk IDs are explicitly **nonnumeric source extensions**, never invented numeric TA2 IDs. Their Latin display is null pending verification. The exact third metacarpal numeric row `1269` remains distinct. Pinned Latin rows `2486`, `4644` and `4646` have possible duplicated/incomplete wording: raw values remain untouched, while candidate Latin display is withheld. Other numeric Latin values are exact source-column observations and have not been independently certified or sided by grammatical construction.

The name variants for short BodyParts3D carpal labels, muscle suffixes, hand digits and explicit source muscle sets are retained in `sourceNameQueries`. They are bounded naming comparisons; no fuzzy geometry matching or formal ontology equivalence is asserted. `Flexor digiti minimi of hand` retains numeric row 2530 and the exact source label containing “brevis” separately.

The existing left/right lumbrical, palmar-interosseous and dorsal-interosseous source selections are compound groups. Twenty-two individual intrinsic-muscle requirements retain those only as `relatedGroupEvidence`, with **no direct representation**. The palmar individual requirements use digit scope to avoid asserting a disputed three-versus-four ordinal convention. Their ordinal/individual terminology remains pending. Eight whole-muscle requirements retain named heads as related part evidence without synthesizing whole-muscle geometry. Source part/group membership cannot close a tendon, head, joint, digital branch, or attachment footprint requirement.

The anatomical table at [TTUHSC El Paso](https://anatomy.ttuhscep.edu/musculoskeletal_system/hand_tables.html) supports selected hand compartment names and the bounded intrinsic-muscle requirement expansion. It is used only for these planning facts. Relationships and source geometry still need their own evidence. The frozen observations retain all original numeric terminology and no new individual clinical innervation or attachment claims.

## Open work and next package

All 502 requirements remain anatomically unaccepted; 314 lack a positive binding in this bounded audit. That status is not absence from every source. Existing relationship IDs are historical evidence only, and must be checked for dataset applicability before any activation. The main male body and the independent Z-Anatomy source frame are never overlaid or treated as registered by this inventory.

Named open work includes wrist capsule/cartilage and remaining ligament/plate subdivisions; individually segmented lumbricals/interossei; unexpanded extrinsic tendons, digital pulleys/vincula and synovial sheaths; individual digital nerves/vessels and lymphatic collectors; and complete hand-space boundaries/contents. `unexpandedRequirements` preserves these remaining obligations for every family. Named plural digital-branch requirements do not resolve per-digit targets.

**Next package:** root should review and activate the P4 seed in the versioned target inventory, then audit same-source individual intrinsic hand muscles and wrist supports against these stable IDs. Preserve source groups and reject automatic splitting/numbering. Root owns active data, runtime search → selection → focus/context → relationship → return checks, publication, and final handoff. No runtime, deployed or expert acceptance was performed by this planning task.

## Reproduction and evidence

Run `python3 data/model-candidates/forearm-hand-target-inventory-v1/build.py --check`. It requires only the adjacent frozen snapshot, script and proposal; it never reads today's graph, manifests, terminology CSV or model inventory. The snapshot retains selected original values and source-file hashes, so future active changes do not rewrite history. `capture.py` is a separate explicit one-time acquisition helper; re-capture requires `--capture --replace-snapshot` and a new review, not ordinary reproduction.

`validation.json` binds checks to script/snapshot/proposal hashes and records a successful isolated reproduction with only those three files. A deliberate negative fixture confirms that routing a numbered lumbrical requirement to the existing source set is rejected. The fixture is removed afterward. `timing.json` records measured implementation/validation duration, missing initial planning timing, and rework. Full app checks are unnecessary for this candidate-only directory and were not run. No geometry rendering or anatomical expert review is claimed.
