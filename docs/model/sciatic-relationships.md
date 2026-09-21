# Sciatic motor relationships: proposed integration package

`data/anatomy/sciatic.json` contains eight `innervates` relationships and no new entities or geometry. Subjects are `atlas:left-sciatic-nerve` and `atlas:right-sciatic-nerve`, matching the existing sciatic extension manifest. Each relationship describes parent-nerve motor supply **through a named division**, rather than a direct muscular branch of an undifferentiated trunk.

| Muscle target | Left ID | Right ID | Required `qualifiers.viaDivision` |
| --- | --- | --- | --- |
| Semitendinosus | `FMA22359` | `FMA22358` | `tibial` |
| Semimembranosus | `FMA22449` | `FMA22448` | `tibial` |
| Biceps femoris, long head | `FMA45889` | `FMA45888` | `tibial` |
| Biceps femoris, short head | `FMA45892` | `FMA45891` | `common_fibular` |

All muscle IDs and laterality were checked against the canonical graph; all have existing geometry. The two sciatic subject IDs were checked against `public/models/extensions/sciatic-nerves.json`. That manifest retains the source's three splines on each side, while omitting separate tibial/common-fibular continuations. None of its splines is reassigned to a named division or muscular branch by this package.

Evidence was verified on 2026-09-22:

- [UAMS Muscles of the Lower Limb](https://medicine.uams.edu/neuroscience/education/medical-school-courses/human-structure-module/anatomy-tables/muscle-tables/muscles-of-the-lower-limb/): the Innervation cells for the three named muscles identify tibial supply, with common fibular supply distinguished for the short biceps head.
- [Ohio University, Organization of the Lower Limb](https://people.ohio.edu/witmerl/Downloads/2011-08-16_MKEastman_LL-Organization.pdf), PDF page 29, Posterior compartment of the thigh, Innervation: explicitly distinguishes tibial-division supply from the common-fibular-division exception for the short biceps head.
- [TTUHSC Hip & Posterior Thigh & Leg tables](https://anatomy.ttuhscep.edu/musculoskeletal_system/gluteal_tables.html), Nerves, sciatic / Motor and tibial / Motor or fibular, common / Motor: identifies the parent sciatic supply through its two components and the respective muscle targets. The UAMS and TTUHSC tables use closely matching educational material; they are corroborating references, not independent specimen studies.

`qualifiers.innervationPath` supplies a readable division name. `directMuscularBranch: false` marks these as parent-level functional summaries. The division qualifier is essential to their meaning; a consuming view must retain and show it. No terminal-branch position, individual motor branch path, root level, fascicular layout, or continuity to the selected muscle mesh is asserted. All edges have pending expert review and typical-anatomy, non-exhaustive scope. Bilateral instantiation is not specimen validation.

## Integration

1. Ensure the bilateral sciatic extension is registered and its geometry source is pinned before merging the package, so both subjects resolve.
2. Merge the three proposed entries from `docs/model/sciatic-sources.json` into the source registry by ID, without duplicating any existing source. Those entries document factual references only; they do not replace the registered geometry source.
3. Load `sciatic.json` with the other relationship packages in the canonical builder; merge its empty entity list, eight relations and coverage scope. No new predicate is required.
4. Preserve both division fields and the indirect-supply semantics in the explorer projection. Display “Tibial bölüm üzerinden” or “Ortak fibular bölüm üzerinden” with the motor relationship. Avoid presenting the short and long biceps heads as sharing the same division.
5. Validate eight unique ipsilateral links, six `tibial` and two `common_fibular`, with evidence and existing endpoints; then regenerate canonical knowledge and explorer output.

Separate semantic division entities could be introduced later if traversal requires them. That would be a deliberate graph normalization, not evidence that distal branch geometry exists. The current package leaves distal leg/foot targets, adductor magnus and other sciatic functions outside its selected scope.
