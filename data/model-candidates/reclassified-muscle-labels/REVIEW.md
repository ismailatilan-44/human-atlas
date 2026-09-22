# Reclassified muscle label candidates

`proposal.json` contains **26 unique FMA entries / 26 mesh IDs**, representing 13 verified left/right pairs from the 14 clear and 12 pharyngeal classification candidates. No existing shared label matched these IDs at review time. All 13 names have exact English/Latin matches in the pinned TA2 table; no Latin field needed to remain null.

| Muscle pair | Left FMA | Right FMA | TA2 row ID |
|---|---|---|---|
| Fibularis brevis | FMA22555 | FMA22554 | 2653 |
| Fibularis longus | FMA22553 | FMA22552 | 2652 |
| Fibularis tertius | FMA22551 | FMA22550 | 2649 |
| Tensor fasciae latae | FMA22426 | FMA22425 | 2602 |
| Tibialis anterior | FMA22545 | FMA22544 | 2644 |
| Tibialis posterior | FMA65019 | FMA65018 | 2666 |
| Levator scapulae | FMA32541 | FMA32540 | 2234 |
| Inferior pharyngeal constrictor | FMA46636 | FMA46635 | 2187 |
| Middle pharyngeal constrictor | FMA46634 | FMA46633 | 2184 |
| Superior pharyngeal constrictor | FMA46632 | FMA46631 | 2179 |
| Palatopharyngeus | FMA46672 | FMA46671 | 2132 |
| Salpingopharyngeus | FMA46670 | FMA46669 | 2191 |
| Stylopharyngeus | FMA46668 | FMA46667 | 2190 |

Every identity/side/mesh combination was checked against the exact official BP3D `isa_element_parts.txt` row and current atlas manifest. In particular, middle pharyngeal constrictor mapping follows the source (`FJ2742` right, `FJ2754` left), not mesh-number ordering. `evidence.json` records line locators and source hashes.

English and Latin labels retain the exact pinned Z-Anatomy TA2 terminology. The TA table omits “Musculus” for some terms; the candidate does not invent an expansion. Names are side-neutral, with a separate verified `side` field as in the shared label schema. Turkish labels and Turkish search aliases are editorial display translations with expert review pending; they are not attributed to a nonexistent Turkish column in TA2.

`validation.json` records the 26 exact mappings, 13 bilateral pairs and zero existing-label conflicts. `build-proposal.py` reproduces this candidate and writes only this directory. Merge `proposal.json.entries` after a fresh duplicate check; do not replace shared source metadata wholesale. No classification, anatomy relationship, innervation, coordinate, geometry or shared label file was changed.
