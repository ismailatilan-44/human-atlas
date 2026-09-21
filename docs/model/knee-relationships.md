# Knee bone attachments

`data/anatomy/knee.json` adds 12 source-supported attachment relationships for the eight registered knee structures. It reuses existing entities and mesh parts.

| Structure, on each side | `attaches_to` target |
| --- | --- |
| Anterior cruciate ligament | Ipsilateral femur and tibia |
| Posterior cruciate ligament | Ipsilateral femur and tibia |
| Medial meniscus | Ipsilateral tibia, through its roots |
| Lateral meniscus | Ipsilateral tibia, through its roots |

Canonical bone IDs are `FMA24475` / `FMA24478` for the left femur / tibia and `FMA24474` / `FMA24477` for the right femur / tibia. The subjects are the registered `atlas:left-…` and `atlas:right-…` cruciate ligament and meniscus entities from `knee-structures.json`.

The new predicate `attaches_to` records a structure's attachment to a named bone. Its direction is structure → bone. It does not identify a localized landmark, imply attachment across the entire bone surface, or assert validated mesh contact. It does not assign muscle-style origin or insertion terminology to ligaments. No attachment point coordinates are generated.

Three American Academy of Orthopaedic Surgeons sources were checked on 2026-09-22:

- [Management of Anterior Cruciate Ligament Injuries, plain language summary](https://www.aaos.org/globalassets/quality-and-practice-resources/anterior-cruciate-ligament-injuries/anterior-cruciate-ligament-injuries-plain-language-summary.pdf), page 1, Background: establishes the ACL's femur-to-tibia connection. Source ID: `aaos-acl-summary`.
- [Posterior Cruciate Ligament Injuries](https://www.orthoinfo.org/diseases--conditions/posterior-cruciate-ligament-injuries/), introductory paragraph and Anatomy caption: establishes the PCL's femur-to-tibia connection. Source ID: `aaos-pcl`.
- [Meniscus Repair](https://www.orthoinfo.org/treatment/meniscus-repair/), Anatomy, named medial/lateral menisci and meniscal roots bullet: identifies both menisci and their root attachments to the tibia. Source ID: `aaos-meniscus-repair`.

These facts are encoded independently of model registration and spatial proximity. Bilateral instantiation applies general anatomy to the atlas, rather than claiming independent specimen validation. Every edge retains its source locator, non-exhaustive scope and pending expert review.

The compact model does not split the meniscal roots, cruciate bundles or attachment footprints into additional entities. Other capsular and ligamentous attachments remain outside this addition; omission is not an assertion of absence. The graph does not equate the existing coarse knee region concepts with a complete knee joint.

Validation includes the existing graph endpoint, source evidence, laterality, uniqueness and hierarchy checks, plus a direct check of the 12 knee links and ipsilateral bone targets. Existing five graph tests remain unchanged. The explorer projection must be regenerated after this graph change, and its relationship label table must support `attaches_to` in both directions.
