# Pulmonary branch label candidates

2026-09-22. Four bounded TR/EN records: the requested FMA8620 anterior segmental pulmonary artery and its two sub-branches, plus FMA68201, the single existing direct arterial child of the right/left pulmonary artery seeds in the current graph. No research expansion or active-file changes.

All four source FMA IDs and names match the official downloaded BodyParts3D tables. The three requested IDs also match the pinned official4.3 FMA8620 snapshot. Two Latin fields exactly match pinned TA2 terminology; the two qualified sub-branch Latin fields remain null.

| ID | Turkish | English | Latin | Reviewed surfaces |
|---|---|---|---|---:|
| FMA8620 | Sağ akciğer anterior segmental arteri | Right anterior segmental artery | Arteria segmentalis anterior pulmonis dextri | 7 |
| FMA68677 | Sağ anterior segmental pulmoner arterin posterior dalı | Posterior branch of right anterior segmental artery | null | 3 |
| FMA68683 | Sağ anterior segmental pulmoner arterin anterior dalı | Anterior branch of right anterior segmental artery | null | 4 |
| FMA68201 | Sol akciğer alt lob arteri | Left lower lobar artery | Arteria lobaris inferior pulmonis sinistri | 22 |

## Source and display limits

FMA8620 retains the seven reviewed thoracic surfaces. They equal the union of FMA68677 posterior branch (three) and FMA68683 anterior branch (four). rawSourceGeometryPartIds preserves the old nine-member source group as evidence. FJ2041/FJ2044 remain unresolved; this package neither assigns renal identities nor reintroduces them into the reviewed selection. No replacement geometry is proposed.

The pinned official4.3 record gives FMA8620 a legacy Latin wording, Ramus anterior descendens (arteria pulmonalis dextra). The candidate uses the exact pinned TA2 equivalent for the source English anterior segmental artery: Arteria segmentalis anterior pulmonis dextri, table4080. Both source wordings are retained in evidence; no source snapshot is rewritten. The lower/inferior lobar artery uses exact TA2 table4101. No full Latin term was established for either anterior/posterior sub-branch; no Latin compounds were invented.

TR labels already contain laterality, and exact Latin terms also contain the side; side:null avoids duplicated prefixes. The source English is preserved separately and display English only capitalizes its first letter. Turkish labels/aliases are editorial and expert review remains pending.

The current graph has only one direct arterial child of FMA50872/FMA50873, FMA68201. The pulmonary arterial tree is an upstream group, not an additional branch; it was not included. A small usable package was preferred within the maximum20 scope.

proposals.json contains candidates. source-evidence.json contains ID/name table rows, official4.3 JSON paths, graph relation, geometry names and hashes. validation.json verifies counts and the reviewed seven-surface union. prepare-proposals.py writes only to this directory. Re-running after active-data integration creates a new snapshot.

Pinned terminology: https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv

## Integration

All four label records were copied into data/anatomy/labels.json on22September2026, bringing the active file to275records. The immutable proposal/evidence snapshot above remains separate. Source IDs and geometry are unchanged. Local UI accepted ASCII Turkish search,7-surface parent→3-surface posterior branch navigation,390×844 isolated geometry and Latin parent heading; TypeScript passed and browser errors were empty. Publication is recorded in the delivery plan.
