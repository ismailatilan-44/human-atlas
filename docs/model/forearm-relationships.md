# Forearm relationships and registered geometry

The canonical graph now merges each manifest listed in `public/models/extensions/index.json` into the existing entity map. An extension adds geometry and manifest evidence to an existing canonical ID instead of creating a second entity. In particular, the bilateral musculocutaneous nerve entities and their source-object bindings now report `registered_geometry`; their previous upper-arm anatomical relationships remain unchanged.

Each registered manifest must have a source record in `data/anatomy/sources.json` with its local path and SHA-256 fingerprint. The graph records that source ID in entity evidence and asset bindings. Registration means that exported geometry is placed in the atlas coordinate frame. It does not establish anatomical correctness, complete branching, or expert review. Unregistered candidate source objects retain their previous status.

`data/anatomy/forearm.json` adds eight directed `innervates` assertions, four on each side:

| Muscle | Left target | Right target |
| --- | --- | --- |
| Pronator teres | `atlas:left-pronator-teres` | `atlas:right-pronator-teres` |
| Flexor carpi radialis | `FMA38461` | `FMA38460` |
| Palmaris longus | `FMA38464` | `FMA38463` |
| Flexor digitorum superficialis | `FMA38471` | `FMA38470` |

Subjects are `atlas:left-median-nerve` and `atlas:right-median-nerve`. The [UAMS Muscles of the Upper Limb table](https://medicine.uams.edu/neuroscience/education/medical-school-courses/human-structure-module/anatomy-tables/muscle-tables/muscles-of-the-upper-limb/), verified on 2026-09-22, identifies median innervation in each named muscle's Innervation column. Each assertion retains that row/column locator through `uams-upper-limb`. Bilateral graph instances apply a general anatomical description to the model; they are not independent specimen observations. Palmaris longus is variable and may be absent.

The base atlas represents pronator teres as separate humeral and ulnar heads. Two explicit muscle composites group those same existing mesh parts, and four `part_of` assertions connect the heads to their ipsilateral muscle. The UAMS pronator teres Origin and Notes columns describe the two-head structure. Left head IDs are `FMA38561` and `FMA38563`; right head IDs are `FMA38560` and `FMA38562`. This grouping creates no mesh and carries `composite_unreviewed` status.

All new relationships are `source_supported`, `typical_anatomy_non_exhaustive`, with expert review pending. They come from anatomical references, not mesh proximity. The median extension contains the main source nerve curves; its separate muscular branches are absent, so these muscle-level links do not claim visible branch continuity. Hand innervation, deeper forearm innervation, origin/insertion sites and transit relationships are outside this addition.

Validation uses the graph's existing endpoint, evidence, laterality, uniqueness and acyclic hierarchy checks. Focused tests verify the registered musculocutaneous merge and the four source-backed ipsilateral muscle targets for each median nerve. After registering or modifying extensions, regenerate `knowledge.json` and then the explorer projection with `scripts/build-explorer-catalog.mjs`.
