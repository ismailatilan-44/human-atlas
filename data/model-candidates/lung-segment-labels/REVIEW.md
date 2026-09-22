# Lung segment labels: 17 intermediate nodes

2026-09-22. This candidate covers exactly 17 existing bronchopulmonary segment IDs found as relation objects in the parenchyma relation proposal. The two already-labeled lung aggregate objects are excluded. No active labels, app, source, geometry or graph files were changed.

All 17 FMA IDs and source English names match official downloaded BodyParts3D name tables. All 17 Latin strings exactly match the corresponding lateralized segment terms in pinned TA2.csv. These IDs identify the segment itself, not its parenchyma. Do not copy these Latin labels onto the separate parenchyma FMA IDs.

Turkish display labels include side and lobe established by the source path. Laterality was checked against the relation evidence and the Latin sinistri/dextri wording. side:null prevents duplicate prefixes. Original source English is preserved; the display English only capitalizes its first letter. Latin segment numerals are retained exactly as present in the source; no additional segment or geometry is inferred.

geometryPartIds records each unchanged base-manifest concept membership. It is evidence, not an instruction to rebind geometry. Existing segment groups include bronchi and vessels, while parenchyma is a distinct child concept. Label matching does not establish anatomical completeness or mesh validity. Turkish is editorial; expert review remains pending.

| FMA | Turkish | Latin | Existing surfaces |
|---|---|---|---:|
| FMA7372 | Sol akciğer üst lob — apikoposterior segment | Segmentum apicoposterius pulmonis sinistri (SI+SII) | 17 |
| FMA7380 | Sol akciğer alt lob — posterior bazal segment | Segmentum basale posterius pulmonis sinistri (SX) | 16 |
| FMA7373 | Sol akciğer üst lob — anterior segment | Segmentum anterius pulmonis sinistri (SIII) | 19 |
| FMA7374 | Sol akciğer üst lob — üst lingular segment | Segmentum lingulare superius pulmonis sinistri (SIV) | 10 |
| FMA7375 | Sol akciğer üst lob — alt lingular segment | Segmentum lingulare inferius pulmonis sinistri (SV) | 6 |
| FMA7376 | Sol akciğer alt lob — superior segment | Segmentum superius pulmonis sinistri (SVI) | 14 |
| FMA7378 | Sol akciğer alt lob — anterior bazal segment | Segmentum basale anterius pulmonis sinistri (SVIII) | 10 |
| FMA7379 | Sol akciğer alt lob — lateral bazal segment | Segmentum basale laterale pulmonis sinistri (SIX) | 12 |
| FMA7338 | Sağ akciğer üst lob — apikal segment | Segmentum apicale pulmonis dextri (SI) | 22 |
| FMA7362 | Sağ akciğer alt lob — posterior bazal segment | Segmentum basale posterius pulmonis dextri (SX) | 21 |
| FMA7339 | Sağ akciğer üst lob — posterior segment | Segmentum posterius pulmonis dextri (SII) | 19 |
| FMA7359 | Sağ akciğer üst lob — anterior segment | Segmentum anterius pulmonis dextri (SIII) | 20 |
| FMA7361 | Sağ akciğer orta lob — lateral segment | Segmentum laterale pulmonis dextri (SIV) | 14 |
| FMA7360 | Sağ akciğer orta lob — medial segment | Segmentum mediale pulmonis dextri (SV) | 11 |
| FMA7366 | Sağ akciğer alt lob — superior segment | Segmentum superius pulmonis dextri (SVI) | 24 |
| FMA7364 | Sağ akciğer alt lob — anterior bazal segment | Segmentum basale anterius pulmonis dextri (SVIII) | 8 |
| FMA7363 | Sağ akciğer alt lob — lateral bazal segment | Segmentum basale laterale pulmonis dextri (SIX) | 12 |

## Evidence and reproduction

proposals.json contains 17 new label records. source-evidence.json records BP3D lines, TA2 terms, original 4.3 relation evidence, geometry names and input hashes. validation.json records all 17 ID/name, Latin and laterality matches. ta2TableId is the upstream CSV identifier; this delivery does not claim a fresh publisher-PDF check for all 17 terms.

Pinned terminology: https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/23d42ff2acf149e4cc0af666b3f80af2ed19909a/TA2.csv

Run python3 data/model-candidates/lung-segment-labels/prepare-proposals.py to reproduce. It writes only to this candidate directory. Running after label integration creates a new snapshot; preserve the delivered pre-integration evidence if needed.
