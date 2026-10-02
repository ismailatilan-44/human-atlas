# Model inventory — scope v1

This reproducible P1 inventory catalogs actual source and viewer identities alongside a **pending** whole-body target matrix. It is not anatomical acceptance or a completion percentage.

Rebuild with `node scripts/build-model-inventory.mjs`; verify without writing with `node scripts/build-model-inventory.mjs --check`. The script validates dataset-qualified concept/asset links, coverage and relationship endpoints, and 13 × 4 × 4 matrix identities. Runtime selections are computed through the viewer's own functions; generation does not render or inspect geometry.

The machine-readable [inventory](../../data/anatomy/model-inventory.json) pins all consumed manifest/data/runtime files and this generator by SHA-256. Changes in registered extensions require regeneration.

| Dataset | Packaged assets | Unique manifest concepts | Catalog records |
|---|---:|---:|---:|
| male-body | 2292 | 3493 | 3537 |
| female-pelvis | 27 | 31 | 31 |
| inner-ear-reference | 6 | 6 | 6 |
| lower-limb-nerve-reference | 137 | 137 | 137 |
| upper-limb-nerve-reference | 127 | 127 | 127 |

There are 3838 dataset-qualified catalog records and 2589 asset records. Catalog rows include source concepts, project/graph concepts and runtime selection variants, which overlap anatomically. They are not counts of distinct anatomical structures. 764 records have evidence-linked region/family planning assignments, including source-linked individual target proposals; 3074 remain explicitly unassigned and uninspected. No name-based absence or membership inference is made.

65 legacy pilot targets link to the catalog without becoming a whole-body denominator. 6 concepts have source-derived surface anchors and 2 retain unresolved/null anchors. Anchor context bones are not substituted for attachment surfaces. 1677 typed graph relations retain their evidence and direct/transitive qualifiers; their presence does not prove each family's required relationships are complete.

## Pending scope matrix

The 13 regional rows and four named family requirements are read verbatim from [the scope contract](model-scope-and-acceptance.md), producing 52 named family requirements and 208 D0–D3 cells. Each cell has a package owner, source-linked inspection candidates when available, relationship requirements and explicit open work. D0 is a context prerequisite; D3 remains pending even for regions whose initial scope says D1–D2. Regional ranges do not mean every listed structure requires every level. **Every cell remains pending complete individual target, laterality and detail expansion and acceptance. The lower-limb, shoulder-arm and forearm-hand seeds enumerate 156, 352 and 502 individual project targets (1010 total); neither is exhaustive and neither closes a cell.** P1 establishes a usable inventory scaffold and source catalog; it does not close the scope contract's requirement to individually enumerate every named target. See [the individual lower-limb seed](lower-limb-targets-v4.md) , [shoulder-arm seed](upper-limb-targets-v2.md) and [forearm-hand seed](forearm-hand-targets-v1.md). Unbound requirements are retained in `individualTargets`; catalog links alone cannot represent them. D1/D2 requirement IDs join their respective matrix cell; D0 context and D3 detail remain open.

| Region | Package owner | Named family requirements | D0–D3 cells |
|---|---|---:|---:|
| Kafatası ve yüz | P9; D3: P12 | 4 | 16 |
| Beyin, omurilik ve zarlar | P10; D3: P12 | 4 | 16 |
| Göz, kulak ve diğer duyu bağlamı | P9; D3: P12 | 4 | 16 |
| Boyun | P9; D3: P12 | 4 | 16 |
| Toraks duvarı ve mediasten | P6; D3: P12 | 4 | 16 |
| Kalp ve akciğer | P6; D3: P12 | 4 | 16 |
| Abdomen ve retroperiton | P7; D3: P12 | 4 | 16 |
| Pelvis ve perine; kadın/erkek referansları | P8; D3: P12 | 4 | 16 |
| Omuz, aksilla ve kol | P3; D3: P12 | 4 | 16 |
| Önkol, el bileği ve el | P4; D3: P12 | 4 | 16 |
| Kalça, uyluk ve diz | P5; D3: P12 | 4 | 16 |
| Bacak, ayak bileği ve ayak | P4; D3: P12 | 4 | 16 |
| Bütün vücut yüzeyi ve bölgeler arası süreklilik | P11; D3: P12 | 4 | 16 |

Assignments use explicit pilot IDs, typed entities in regional records, or separate-reference scope plus manifest systems. These assignments identify work queues, not complete regional extent: aorta, esophagus and major nerves can cross regions. There is no propagation from source aggregate membership or label matches. An unassigned base concept remains discoverable by its preserved ID, source name, membership and typed relationships.

## Membership, labels and source boundaries

Each catalog row separates original per-manifest membership from actual curated viewer selection. The pulmonary raw/reviewed variants and unverified source vessels are retained as different records. Project display groups keep their graph kind. Female source aliases remain cataloged even when search deduplicates them. Datasets keep distinct coordinate frames, source/registration records, limitations and attribution. Inner-ear component licenseScope fields remain on asset records. Historical female manifest candidate status is recorded separately from its current selectable-reference status.

Labels report both runtime text and explicit regional-label evidence. Fallback source text is not a verified TR/LA translation. Surface-anchor, graph representation, technical selection and expert statuses remain separate; stale graph-only landmark statuses do not replace registered anchor evidence. The generator retains 112 lower-limb and 26 upper-limb sourced reference relationships without borrowing the male graph, and does not invent other reference relationships, infer independent subdivisions from names, inspect binary geometry, or mark absence. Existing visual/source reports require target-level reconciliation; expert review remains pending.

For queries, use dataset-qualified `catalog[].id`; join `viewerSelection.assetIds` and `sourceMemberships[].assetIds` to `assets` by dataset and ID; join `relationIds` to `relations`; follow `coverageTargetIds` into `pilotTargets`; follow `regionalTargetIds` or `targetMatrix[].individualTargetIds` into `individualTargets`; follow `targetMatrix[].catalogIdsForInspection` into the catalog. The same source concept may legitimately occur in several scopes and detail inspection queues.
