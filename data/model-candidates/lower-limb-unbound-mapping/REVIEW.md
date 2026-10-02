# Lower-limb unbound targets: BP3D metadata audit

Reviewed 2 October 2026 at source revision `e879fc92e1bfa6226898d12cdca2863e365858e0`. This candidate-only audit owns this directory. It changes no target seed, active labels, graph, app, model, inventory or release. [proposal.json](proposal.json) contains all 18 dataset-qualified target records, source evidence and exact membership; [audit.py](audit.py) reproduces the bounded audit offline.

## Outcome

Two fibular-artery targets have verified **BodyParts3D 4.3 source candidates**, with an unresolved identity/version discrepancy against existing 4.0 base objects. **No new main-body binding is accepted.** The other 16 targets remain unresolved within this bounded BP3D audit. These counts are not anatomical absence or regional completeness claims. The parallel Z-Anatomy source-geometry audit may provide independent representations.

| Target | Verified 4.3 source concept | Source component | Canonical returned representation |
| --- | --- | --- | --- |
| Left fibular artery, TA2 4727 | FMA43923 — Left peroneal artery | FJ2093 | BP29771 |
| Right fibular artery, TA2 4727 | FMA43922 — Right peroneal artery | FJ2197 | BP29774 |

The official OBJ headers specify Compatibility version 4.3, FMA 3.0 part_of build-up and the exact IDs/names above. The [retained download](source/artery-source.zip) and individual header extracts preserve evidence; geometry itself was not compared with the base mesh. The pinned official `FMA2Obj.txt` has FMA43922/FJ2197 at lines 1358 (`is_a`) and 4534 (`part_of`), and FMA43923/FJ2093 at lines 1359/4535. Each row contains exactly that one component. Its payload SHA-256 is `c3d16c891016da13447de2fc3241d05d92e8f9dc460e363233c03f420b935d4f`.

Primary sources retrieved on 2 October 2026: [left concept](https://lifesciencedb.jp/bp3d/get-fmastratum.cgi?version=4.3&lng=en&t_type=4&bul_id=4&cb_id=5&ci_id=1&md_id=1&mv_id=6&mr_id=1&f_id=FMA43923), [right concept](https://lifesciencedb.jp/bp3d/get-fmastratum.cgi?version=4.3&lng=en&t_type=4&bul_id=4&cb_id=5&ci_id=1&md_id=1&mv_id=6&mr_id=1&f_id=FMA43922), [unsided peroneal artery](https://lifesciencedb.jp/bp3d/get-fmastratum.cgi?version=4.3&lng=en&t_type=4&bul_id=4&cb_id=5&ci_id=1&md_id=1&mv_id=6&mr_id=1&f_id=FMA43921). Requests pin version 4.3, FMA3.0 build cb_id=5 and the existing project parameter set; JSON response hashes are in the proposal. The [official membership endpoint](https://lifesciencedb.jp/bp3d/get-info.cgi?version=4.3&cmd=concept-objfiles-list) was inspected through the already retained version-stamped payload, not fetched again.

## Terminology and hierarchy

The unsided official FMA43921 source record gives English `Peroneal artery`, Latin `Arteria fibularis`, with explicit left/right `is_a` children FMA43923/FMA43922. That Latin string matches pinned TA2 4727, CSV line 4813, English `Fibular artery`. This verifies the source terminology correspondence without claiming a published TA2–FMA crosswalk. Side stays separate; lateralized Latin compounds were not invented. There is no active label recommendation before the destination dataset and geometry are accepted.

The official direct paths place FMA43923 under left posterior tibial artery FMA43899 and FMA43922 under right posterior tibial artery FMA43898. The child-node `potype` is **regional_part_of**. The proposal records two inactive `part_of` relationships with this exact source qualifier. It does not upgrade them to `branch_of`; nearby ancestor nodes having a branch_of tag does not change the peroneal node's source assertion. Membership overlap also does not establish branch semantics or physical continuity.

The discovery catalog assigns FMA43901 to both artery objects. The [official FMA43901 record](https://lifesciencedb.jp/bp3d/get-fmastratum.cgi?version=4.3&lng=en&t_type=4&bul_id=4&cb_id=5&ci_id=1&md_id=1&mv_id=6&mr_id=1&f_id=FMA43901) identifies it as **Subdivision of posterior tibial artery**, an ancestor rather than the canonical left/right object concept. Therefore the discovery catalog's FMA column is not used as a leaf identifier. Requested catalog representations BP29005/BP29050 differ from returned canonical BP29771/BP29774; both are explicitly retained.

## Base version discrepancy

The existing main `public/models/atlas.json` contains FJ2093 and FJ2197, but both carry `FMA70801`, “Set of dorsal digital arteries”. FMA70801 includes four elements: FJ2093, FJ2197, FJ2318 and FJ2346. Both base parts have nonzero triangles and a geometry binding; this audit does not say geometry is missing.

The retained official archive `isa_element_parts.txt` lines 24504–24507 also assigns all four pieces to FMA70801. The corresponding name table line 2585 says “set of dorsal digital arteries”. Thus the current base mapping is source-preserved within its old metadata, while the 4.3 mapping differs. This audit found no positive official 4.0 row authorizing a peroneal display correction. Shared FJ numbers alone do not establish geometry-equivalence across versions. Main identity, source memberships and names remain unchanged pending source-version and geometric review; the 4.3 candidate dataset is separate and inactive.

## Remaining 16 targets and ankle context

The following eight terms were searched bilaterally across all base concepts/parts, the eight active extension manifests, 3,514 knowledge entities, retained official archive English ISA/PART-OF name tables, and the pinned 4.3 discovery catalog: deep fibular nerve, superficial fibular nerve, sural nerve, medial plantar nerve, lateral plantar nerve, anterior talofibular ligament, posterior talofibular ligament, calcaneofibular ligament. Fibular/peroneal and talofibular/fibulotalar/calcaneofibular/fibulocalcaneal alternatives were included where relevant. Exact regexes and all matches are in each proposal target.

No positive BP3D identity binding was established for these 16 targets. The name/catalog scan cannot establish absence from anatomy, another release, a subobject, an unnamed component or another source. No FMA ID was guessed. The pinned TA2 entries were checked exactly for all nine audited terms, but a term alone does not prove geometry.

Existing bilateral **long plantar ligaments** are independently represented as FMA44250/FJ1424M (left) and FMA44249/FJ1424 (right). These source names also appear in the retained official archive and the 4.3 discovery catalog. They are not any of the three requested ankle collateral ligament identities. No component overlap, part relation or target coverage is inferred from their nearby anatomical region.

## Intake, checks and ownership

The 4.3 download is retained unchanged for private inspection. Component terms follow the previously retained official [live-source license](https://lifesciencedb.jp/bp3d/info/license/index.html): CC BY-SA 2.1 Japan, BodyParts3D, © 2008 Database Center for Life Science (DBCLS). Its SHA-256 is recorded in the proposal. Attribution and share-alike must accompany any adaptation/distribution; this is separate from the older base archive's license. This task does not publish or activate those files. The license snapshot was reused rather than checked afresh. Reference body is the source's adult male reference; geometry units in returned headers are mm. No coordinate registration or geometric/anatomical acceptance was performed here.

Local macOS/Python 3 validation passed via `python3 data/model-candidates/lower-limb-unbound-mapping/audit.py`: 18 unique target IDs, two verified 4.3 candidates, 16 unresolved targets, zero accepted main bindings, nine exact TA2 term pairs, canonical source header IDs/version, exact pinned membership rows, and two direct regional_part_of source paths. Input snapshot hashes bind the result to the recorded sources. No app/build/browser tests were run because this work does not change an active surface.

Measured interval: 08:43:57–08:50:09 UTC, approximately 6m12s, from first explicit timestamp through source/mapping validation; reading before that timestamp and final report writing are excluded. One initial download attempt returned HTML because it lacked the established viewer session. Retrying with the repository's existing downloader succeeded; both the failed response and successful request details are retained. No broader research blocker remains for this bounded metadata output.

Integration/release owner: parent task. Next action: use the independently audited source-frame reference bindings when accepted, and retain this 4.0/4.3 discrepancy for a separate geometry/semantic comparison before changing the base concept. Expert review, geometry acceptance, selection journeys and release remain open outside this metadata audit.

Integration follow-up: all 18 target identities subsequently gained Z-Anatomy reference bindings. The BP3D audit initially filtered only currently unbound rows and failed after that legitimate change. The integration owner fixed its nine term/two-side identity set independently of active representation status and added `--check` for deterministic output comparison. Regeneration and `--check` passed; current input snapshots pin that repeat verification while `sourceRevision` remains the discovery baseline. The two BP3D candidates remain inactive and the 16 unresolved BP3D identities remain bounded findings; neither status contradicts the new Z-Anatomy reference bindings.
