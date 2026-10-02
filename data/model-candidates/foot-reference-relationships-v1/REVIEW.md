# Foot bone and ankle ligament relationships — 2 October 2026

Integration baseline `41723bdf937ce50976c118230b0a29441700d4a2`. This bounded delivery adds **48 symmetric bone-articulation records and 12 directed ligament-to-bone attachments** to the independent lower-limb reference. Its 12 existing nerve branches remain. No source geometry, source object identity, coordinate, main-atlas relationship or expert acceptance is changed.

## Evidence and semantics

[TTUHSC foot osteology](https://anatomy.ttuhscep.edu/musculoskeletal_system/leg_tables.html), read on 2 October, explicitly identifies talar, navicular, cuboid, corresponding metatarsal/proximal-phalanx and successive same-toe phalanx articulations. Twenty-four unsided facts are instantiated separately on each source side. The first toe has proximal/distal bones; toes II–V have proximal/middle/distal bones. Generic cuneiform/metatarsal wording is not converted into particular digit pairs. Other bone pairs remain outside this audit, without absence claims.

[Golanó et al. (2010), DOI 10.1007/s00167-010-1100-x](https://doi.org/10.1007/s00167-010-1100-x), inspected through the [University of Barcelona copy](https://diposit.ub.edu/bitstreams/2e6e7803-acea-4dc4-8832-b63ced732f00/download), pages 559–560 and the continuation on 561, identifies the anterior/posterior talofibular ligaments' fibular/talar attachment regions and the calcaneofibular ligament's fibular/calcaneal regions. Six unsided endpoints are instantiated on each source side. The posterior ligament's multifascicular/variable insertion is not reduced to an accepted model footprint. A PMC browser challenge prevented that route; the university's published copy supplied the text. No challenge bypass was attempted. A PDF screenshot failed to fetch; no new dissection-image acceptance is claimed.

`articulates_with` is symmetric and nontransitive: one stored edge exposes either bone from the other. It is distinct from source `part_of` and general proximity. The UI names it “Eklem yaptığı kemik.” It does not create a joint surface, cartilage, capsule or measured geometric contact. `attaches_to` remains ligament→bone with a human-readable regional note. Selecting the whole bone is navigation to its context, not segmentation of the named region. No coordinate or attachment marker is added.

`proposal.json` retains every endpoint, dataset, side, locator, qualifier and input hash. Facts are cited and paraphrased; article/table prose, images and measurements are not redistributed. Geometry/component licensing remains in the existing reference attribution.

## Reproduction and acceptance

```sh
python3 scripts/build-foot-reference-relationships.py --apply
python3 scripts/build-foot-reference-relationships.py --check
```

The producer rejects conflicting existing edges/sources, keeps existing nerve branches, verifies nonempty manifest selections and explicit label role/laterality at both ends, stores each symmetric pair once, and rejects inverse duplicates. This validates knowledge/selection bindings, not anatomy of the encoded meshes. Application TypeScript, navigation, desktop/mobile inspection, publication and named expert acceptance are integration criteria. See the [owning progress record](../../../docs/model/progress-report-2026-10-02.md) for final revision and evidence.

Open: complete foot joint network, cuneiform-to-individual-metatarsal mappings, missing supports, independent articular surfaces, ligament fascicles/footprints, specimen-specific contacts and anatomical expert review. Next: reconcile individual foot targets and exercise bone→bone and ligament→bone→ligament product journeys.


## Root integration — local acceptance

Root integration applied the 60 proposed edges unchanged. The final producer check passed with 48 symmetric articulation and 12 directed attachment records alongside the preserved 12 nerve branches. TypeScript, interaction/inventory checks and desktop/mobile bone/ligament navigation passed. No geometry/footprint or expert acceptance was added. Source revision and publication are recorded separately in the [owning action report](../../../docs/model/progress-report-2026-10-02.md); the preceding delegated/source audit remains historical evidence.


## Root publication acceptance

Published source `0dd4bb19a8bfbacd4e25bd2edc272ce25c6efdac`, static `2c2409c4e641ecdd02f8e039f06a0c21e54c2cc1`, successful Pages run #36994436788; live release.json matched. Bounded live Chromium 390×844 selection/relationship/source journeys passed with zero console errors/warnings. The whole-foot mobile group remains visually small after automatic focus; detailed-study camera acceptance, physical-device performance, geometry detail and expert acceptance remain open. Exact local/live flows and timing are recorded in the owning action report.
