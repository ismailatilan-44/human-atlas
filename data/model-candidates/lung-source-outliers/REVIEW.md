# FJ2041 / FJ2044 lung-selection outliers

## Finding

**The unexpected lower vessels are inherited from a BP3D 4.0 source concept/geometry inconsistency. The available evidence does not support a faulty Atlas name join or a coordinate conversion error.** Both source objects are explicitly labelled FMA8620, Right anterior segmental artery, and official 4.0 IS-A/PART-OF tables put them in the pulmonary hierarchy. Their actual source geometry is at the right renal arterial level. The most plausible interpretation is a legacy source misassignment of renal-region branch geometry to a pulmonary concept, but its exact renal branch identity remains unverified.

No public, app, raw Atlas, extension, source registry, labels or group membership was changed. No geometry was removed or moved. This investigation is separate from acceptance of the new lung parenchyma package.

## Version and identity evidence

The two FJs are **absent from the official 4.3 object set** in `../lung-surfaces/FMA2Obj.txt` (Data Version4.3, Objects set4.3, Tree versionFMA3.0). A live `download.cgi` request by those old IDs returns valid source OBJs, but both explicitly say **Compatibility version4.0**, not4.3. Their returned representation is BP7722 / FMA3.0 part_of / FMA8620. Requesting through the live service does not turn a legacy object into a4.3 asset.

The official 4.0 archive tables were fetched freshly:

- https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt
- https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_element_parts.txt

Both explicitly map FJ2041 and FJ2044 to FMA8620. PART-OF also explicitly maps them to FMA7359 (right anterior bronchopulmonary segment), FMA7333 (upper lobe of right lung), and FMA7309 (right lung). `evidence.json` retains the matching source rows with line numbers and all base parents. The current converter preserves source IDs and positions; this evidence shows the problematic assignment precedes the app.

The independently pinned4.3 FMA3.0 concept endpoint for FMA8620 uses `version=4.3, cb_id=5, ci_id=1, md_id=1, mv_id=6, mr_id=1`. Its paths confirm that **FMA8620 means a pulmonary artery**, including the explicit FMA8620→FMA7359→FMA7333→FMA7309 path. This is not a legitimate renal synonym of that same FMA concept. Source URL, raw JSON and hash are retained in `source-fetch.json`.

The4.3 FMA8620 memberships are:

- IS-A: FJ6044, FJ6045, FJ6046, FJ6047, FJ6049, FJ6050, FJ6051.
- PART-OF: FJ2974, FJ2975, FJ2976, FJ2977, FJ2979, FJ2980, FJ2981, FJ6044, FJ6045, FJ6046, FJ6047, FJ6049, FJ6050, FJ6051.

A current same-concept object FJ6044 was downloaded: its4.3 header identifies FMA8620 and its Atlas Y bounds are1.354701–1.370331m, at lung level. FJ2974, a retained base pulmonary branch, returns4.3/FMA68677 (posterior branch of right anterior segmental artery) at1.354771–1.370371m. These are comparison evidence, not replacement proposals.

Neighboring legacy renal-labelled objects FJ2042/FJ2043/FJ2045 are also absent from the4.3 object set. Therefore absence alone does **not** prove that the source authors intentionally corrected the two outliers, nor identify a replacement or new renal ID.

## Actual geometry and context

The actual returned source positions were transformed only by the established main Atlas conversion `(x*.001, z*.001+.0781112, -y*.001-.1)` and compared to the actual base binary triangles. Bidirectional sampled vertex-to-triangle distances are negligible, demonstrating that the low position is already in the source; it was not introduced by the lung extension or a displaced app transform.

| Part | Base Y bounds m | Source/base RMS mm | Nearest lung surface mm | Nearest right kidney surface mm |
|---|---:|---:|---:|---:|
| FJ2041 | 1.106701–1.128421 | 0.000000 | 75.946 | 0.120 |
| FJ2044 | 1.092701–1.112551 | 0.004120 | 97.881 | 0.029 |

The nearest sampled distance to FJ3562 (anterior division of right renal artery) is0.005388mm for FJ2041 and0.016750mm for FJ2044. These are surface proximity measurements, **not verified vascular junctions**. The source and base coordinates place the outliers alongside independently renal-labelled FJ2042/2043/2045 and the actual right kidney FJ3147.

Actual-geometry images inspected:

- `outliers-lung-and-renal-context.png`: candidate lung surfaces above, base right kidney and renal arterial context below. The two outliers are orange; other named renal arteries are red. The separation from the lungs is plainly visible.
- `outliers-right-renal-close.png`: the orange surfaces sit within the renal branching context around a translucent blue right kidney. Proximity supports a renal-region interpretation but cannot name an exact branch or prove continuity.
- `outliers-right-renal-oblique.png`: alternate actual-coordinate view retained for inspection.

No image was used to claim complete anatomical approval, and no inferred centerline or replacement geometry was drawn.

## What remains unresolved

Official concept queries show separate FMA86342 (anterior superior segmental branch of right renal artery) and FMA86344 (anterior inferior segmental branch of right renal artery). Their existence does not establish that FJ2041 or FJ2044 belongs to either. No retained source mapping links these FJs to those renal concepts. **Do not automatically assign either renal FMA or a numbered renal segment from apparent position.** The defensible present label for the evidence is “legacy source object with pulmonary ID and renal-region geometry; exact branch unresolved.”

The internal cause is unknown: source name/ID misassignment is strongly supported, but historical editing, export or modelling details are not recoverable from these files. This investigation distinguishes that uncertainty from the confirmed source-vs-app result.

## Bounded follow-up recommendation

Preserve original FJ IDs and raw BP3D4.0 memberships. A future product change can flag this source anomaly and expose an explicitly project-curated pulmonary selection that excludes these two objects while keeping the raw source group accessible. Explain the exclusion; do not silently alter the ontology or present the objects as validated renal anatomy. An expert/source correction would be needed before giving them a new anatomical identity.

If that follow-up is accepted, the current right-lung selection would become163 rather than165 members; the raw source group would remain165. Its right upper-lobe and right anterior-segment display selections also inherit these two source members and need consistent treatment. This report makes no such app change.

## Reproduction and provenance

`fetch-evidence.py` records the source requests; `inspect-geometry.py` generates metrics and actual-coordinate renders under Blender with `--disable-autoexec`; `write-review.py` builds this report. `source-fetch.json` retains source URLs, returned compatibility versions and hashes. Raw source files remain only in this candidate review directory. The live source's attribution/license information is https://lifesciencedb.jp/bp3d/info/license/index.html ; no new public redistribution or license reinterpretation was performed here.


## Follow-up: transferable official 4.3 pulmonary alternative

`right-anterior-pulmonary-43.json/.bin/.bin.gz` contains all seven genuine source objects in the official FMA8620 IS-A row. Each OBJ header independently confirms4.3/FMA8620. This is a **candidate-only alternative representation**, not a registered additive extension: `extendsConceptIds` is empty, the existing FMA8620 ID collision is explicit, and integrationMode requires an explicitly reviewed replacement or source-only view. It contains **7 parts / 1,464 triangles**,35,896binary bytes and19,742gzip bytes. Source attribution is `PULMONARY43-ATTRIBUTION.md`.

Every new surface has a distinct close geometric counterpart among the seven valid pulmonary branch surfaces already present in the base Atlas:

| New4.3 source object | Existing base object | Existing branch concept | RMS mm | Max mm |
|---|---|---|---:|---:|
| FJ6044 | FJ2974 | FMA68677 | 0.097500 | 0.319900 |
| FJ6045 | FJ2975 | FMA68683 | 0.125266 | 0.429893 |
| FJ6046 | FJ2976 | FMA68683 | 0.162874 | 0.451994 |
| FJ6047 | FJ2977 | FMA68683 | 0.092065 | 0.312250 |
| FJ6049 | FJ2979 | FMA68683 | 0.102143 | 0.334220 |
| FJ6050 | FJ2980 | FMA68677 | 0.095974 | 0.291374 |
| FJ6051 | FJ2981 | FMA68677 | 0.024598 | 0.107435 |

These are bidirectional vertex-to-triangle comparisons in unchanged source coordinates; no transform fitting was used. RMS0.024598–0.162874mm and maximum0.451994mm support **substantial spatial overlap**, not byte-identical geometry. The seven existing objects already provide the thoracic geometry. The official4.3 PART-OF row includes both the parent-concept surfaces and the named child-branch surfaces, so additive import of the parent surfaces would duplicate pulmonary representation.

`pulmonary-existing-seven.png` and `pulmonary-source43-seven.png` use the same camera, material and actual right-upper-lobe context to compare the existing branches with the alternative4.3 source surfaces. `pulmonary43-overlap-review.json` retains all49 pair comparisons and the best match for each source surface; `pulmonary43-validation.json` verifies exact source positions, source membership, hashes, normal/index integrity and gzip equality.

**Simplest next product proposal:** preserve raw history and named child IDs, and build an explicitly reviewed pulmonary selection from the existing seven valid thoracic objects (FJ2974/2975/2976/2977/2979/2980/2981). This needs no new overlapping geometry. The transferable4.3 package remains available for a deliberate alternate representation, comparison, or replacement decision; do not merge it blindly. Keep the two old renal-region outliers visible through raw source access with an anomaly note until exact source identity is resolved.

## Viewer integration — 22 September 2026

The source investigation above is preserved. `app/reviewed-selections.ts` now excludes FJ2041/FJ2044 from19 explicit pulmonary/thoracic display selections, retaining each original source membership under `atlas:source-membership:<FMA>`. Later extension members are retained in both variants. This is a display selection review; raw manifests and source ontology are unchanged. Main geometry still contains2290 surfaces. Right lung:163 reviewed /165 source; FMA8620:7 reviewed /9 source. Broad whole-body/vascular selections retain the two surfaces, with explicit unverified display concepts and the original FMA8620 kept in `sourceConceptId`. Their renal branch identity is not asserted. No overlapping4.3 replacement surfaces were added.

A visible toggle switches between reviewed and raw selections while retaining isolation. Direct selection of either disputed surface shows an unverified-vessel title and source discrepancy. Graph membership remains a raw-source record; the UI canonical selection is reviewed. Coverage bindings describe the reviewed selection and explicitly record the two excluded source IDs.
