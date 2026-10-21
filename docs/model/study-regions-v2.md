# Bounded regional study modules v2

Source inspection began at `b877954fdc85243c48cd302c5d2cfec727bd9a6b`, the merged regional-study baseline. Root `AGENTS.md`, six repository skills and source → producer → check routing were present in Git. The October 2 handoff and scope plan contain historical source/deployment revisions; they do not establish publication of this package. Existing right-ankle questions and source identifiers remain unchanged.

## Scope selected before implementation

Exactly two additional modules were selected after inspecting the versioned target/coverage records and active reference manifests. Their authored records are [left-ankle-v1.json](../../data/study/left-ankle-v1.json) and [right-upper-limb-bones-v1.json](../../data/study/right-upper-limb-bones-v1.json). The shared [catalog](../../app/study-packs.ts) retains the original nine-item right-ankle pack as its first entry.

| Module | Dataset | Finite concepts |
| --- | --- | --- |
| Left ankle region, 9 bones | `lower-limb-nerve-reference` | `zanatomy:talus-l`, `zanatomy:calcaneus-l`, `zanatomy:navicular-bone-l`, `zanatomy:cuboid-bone-l`, `zanatomy:medial-cuneiform-bone-l`, `zanatomy:intermediate-cuneiform-bone-l`, `zanatomy:lateral-cuneiform-bone-l`, `zanatomy:tibia-l`, `zanatomy:fibula-l` |
| Right upper limb, 5 bones | `upper-limb-nerve-reference` | `zanatomy:clavicle-r`, `zanatomy:scapula-r`, `zanatomy:humerus-r`, `zanatomy:radius-r`, `zanatomy:ulna-r` |

Each concept has exactly one distinct active source surface, source object name and matching side. All chosen labels have exact pinned-table Latin terms and existing Turkish/English labels. The upper-limb set tests whole-bone recognition only: the humerus identity does not validate disputed humeral attachment markers. No attachment, articulation, innervation or other relation is scored. Numbered-bone terminology gaps, partial nerves, compound sesamoids, rejected intersesamoid surfaces and other unbound targets remain excluded. No target or coverage acceptance status changes.

The learning goals are to match a highlighted source surface to its existing name and side, recognize it in isolation and in same-source context, and correct a wrong/skipped answer against the source evidence. The original prompts are authored recognition tasks, not imported examination cards. The common study workflow provides inspection → recall → corrective feedback → missed-item retry → finish/return; dataset-specific names and attribution must follow the active pack.

## Source ownership and limits

The new JSON records copy evidence from the owning [lower-limb metadata](../../data/anatomy/lower-limb-reference.json) and [upper-limb metadata](../../data/anatomy/upper-limb-reference.json). They pin SHA-256 hashes of those authored label records and their active public manifests. Each item additionally binds its geometry part ID. These are authored study inputs, not new geometry producers or generated anatomy catalogs. `version: "1"` is the question interpretation version; changing a prompt, answer identity or interpretation requires a version change and explicit learner-history migration/reset rather than crediting old attempts silently.

Geometry remains unchanged in each independent reference frame. The [lower-limb source review](lower-limb-nerve-reference-review.md) and [upper-limb source review](upper-limb-nerve-reference-review.md) retain inherited coarse surfaces and defects. In the upper selection the scapula has two zero-area triangles; the humerus has four boundary edges and two nonmanifold edges. These technical findings are disclosed, not repaired or treated as anatomical certification. Existing [lower-limb attribution](../../public/models/lower-limb-nerve-reference/ATTRIBUTION.md) and [upper-limb attribution](../../public/models/upper-limb-nerve-reference/ATTRIBUTION.md) retain their separate source licenses. This package does not change any licensing.

The selected sets are a bounded recognition exercise within the [lower-limb v4](lower-limb-targets-v4.md), [upper-limb v2](upper-limb-targets-v2.md) and [forearm/hand v1](forearm-hand-targets-v1.md) inventories. They do not establish complete regional coverage or anatomical expert acceptance. Expert review, learner prompt suitability and physical-device interaction remain separate acceptance items.

## Verification and publication boundary

`node --test scripts/study-packs.test.mjs` passed three tests: all 14 new source/part/side/label/evidence bindings and frozen input hashes, distinct question identities, preserved left/right scope, and the exact five-item upper-limb boundary. `npm run check` passed after catalog creation. Existing right-ankle tests remain separate. No historical source producer was rerun and no source geometry changed.

Browser acceptance and final publication are the integration owner's responsibility: run each new pack through inspection, wrong/correct/skip feedback, correction/finish and return, including 320/390-pixel layouts and dataset switching. Test persisted sessions against the same pack/version and reject stale identities. Record the exact integrated source and live build in the delivery handoff; this record alone makes no live-site claim. The [human review packet](learning-review-packet.md) records remaining device/expert cases when available.

## Whole-skull orientation extension — 13 October 2026

### Decision: 22-bone orientation and recognition

- Scope/status: user-authorized local first delivery, all 22 instances in `atlas:skull-bones`; whole-bone D0/D1 recognition only. [Authored pack](../../data/study/whole-skull-v1.json) preserves all source IDs and labels; previous 23 items remain unchanged.
- Evidence: [current inventory](skull-research/current-inventory.md#exact-22-part-selection), [integrated label review](../../data/model-candidates/skull-labels/REVIEW.md), [learning options](skull-research/learning-content.md#bounded-content-options--no-product-decision-yet), [renderer/mechanism research](skull-research/interactions-and-pedagogy.md). [TTUHSC bone table](https://anatomy.ttuhscep.edu/anatomytables/bones_head_neck.html), consulted 13 October, named whole-bone rows support brief original location notes. No table, image, feature/canal explanation or third-party question is reproduced.
- Evidence boundary: manifest/labels establish source identity and side; class membership follows the existing reviewed 8 cranial/14 facial inventory. Location notes are sourced anatomy, not certified mesh fidelity. Learning effectiveness and expert acceptance remain untested.
- Choice and reason: use an explicit bounded skull workspace, stable camera/context on selection, direct searchable list for tiny bones, six direction views, optional single-bone educational translation and exact return. Isolation provides access to obscured whole surfaces. Existing recall/correction/scheduling is reused. No need to acquire assets or implement cuts, free assembly or jaw motion for this goal. Research relational-core option is deferred.
- Rights/frame constraints: existing BodyParts3D TARO geometry/attribution unchanged, original shared transform preserved; display translation is reversible, not physiological motion. Independent ear/other reference bodies remain separate. No new rights clearance claimed.
- Owning change/check path: `data/study/whole-skull-v1.json` → `app/study-packs.ts`, shared viewer/study/saved-scene state; targeted binding/state tests, existing validators, loaded browser journeys and final `check:ci`. Model inventory regenerated only for fingerprinted runtime/producer changes.
- Open verification: target-level rendered audit, independent mechanism review, physical device/multitouch/thermal and anatomist review. Fine features, sutures and passage courses are outside this package.
- Review/result: pending implementation and acceptance evidence below; this decision alone claims no rendered or expert acceptance.

### Target audit and rendered acceptance

All 22 active concept/part/label bindings are checked by `scripts/skull-study.test.mjs`, including 8 cranial/14 facial, 8 left/8 right/6 unpaired and source-input hashes. Original public geometry and source coordinates have no diff. Existing atlas validation checks decoded buffers; no new raw-source conversion is performed. Display X is left-positive in this source frame; bounds centers below are observations, not independent identity proof.

Actual loaded Chromium at 1200×942 rendered every item in isolation from front and back using ordinary bone/view selects. All 44 captures show distinct nonempty whole-bone silhouettes with inspectable opposite surfaces. [Contact sheet 1](../../output/playwright/skull-contact-0.jpg) and [contact sheet 2](../../output/playwright/skull-contact-1.jpg) preserve the named rows; full screenshots are retained locally as `output/playwright/skull-audit-FMA*-front/back.png`. These are minimum whole-source inspection views, not named anatomical surfaces or fine-feature acceptance. Coarse angular facets/edges remain conspicuous, particularly on nasal/lacrimal/concha/palatine surfaces and cranial borders. Smoothness, openings, thin plates and suture accuracy are not certified.

| Concept / source part | Source name | Side | Vertices / triangles | Display bounds center X (m) | Rendered check |
|---|---|---|---:|---:|---|
| FMA52740 / FJ3199 | Ethmoid | unpaired | 5334 / 8618 | -0.00065 | front + back, isolated |
| FMA52734 / FJ3200 | Frontal bone | unpaired | 3315 / 5112 | -0.00066 | front + back, isolated |
| FMA54738 / FJ3263 | Left inferior nasal concha | left | 435 / 662 | 0.01027 | front + back, isolated |
| FMA53646 / FJ3265 | Left lacrimal bone | left | 347 / 604 | 0.01263 | front + back, isolated |
| FMA53650 / FJ3269 | Left maxilla | left | 2678 / 3598 | 0.02136 | front + back, isolated |
| FMA53648 / FJ3272 | Left nasal bone | left | 236 / 388 | 0.00234 | front + back, isolated |
| FMA53656 / FJ3273 | Left palatine bone | left | 986 / 1606 | 0.01296 | front + back, isolated |
| FMA52789 / FJ3274 | Left parietal bone | left | 2927 / 3732 | 0.03349 | front + back, isolated |
| FMA52739 / FJ3281 | Left temporal bone | left | 1835 / 2828 | 0.04210 | front + back, isolated |
| FMA52893 / FJ3287 | Left zygomatic bone | left | 721 / 1056 | 0.04757 | front + back, isolated |
| FMA52748 / FJ3289 | Mandible | unpaired | 1207 / 2348 | -0.00065 | front + back, isolated |
| FMA52735 / FJ3309 | Occipital bone | unpaired | 2938 / 4912 | -0.00063 | front + back, isolated |
| FMA54737 / FJ3369 | Right inferior nasal concha | right | 530 / 636 | -0.01161 | front + back, isolated |
| FMA53645 / FJ3371 | Right lacrimal bone | right | 378 / 658 | -0.01276 | front + back, isolated |
| FMA53649 / FJ3375 | Right maxilla | right | 2591 / 3660 | -0.02393 | front + back, isolated |
| FMA53647 / FJ3378 | Right nasal bone | right | 253 / 392 | -0.00495 | front + back, isolated |
| FMA53655 / FJ3379 | Right palatine bone | right | 994 / 1486 | -0.01433 | front + back, isolated |
| FMA52788 / FJ3380 | Right parietal bone | right | 2734 / 3694 | -0.03559 | front + back, isolated |
| FMA52738 / FJ3386 | Right temporal bone | right | 1976 / 2906 | -0.04334 | front + back, isolated |
| FMA52892 / FJ3392 | Right zygomatic bone | right | 717 / 1146 | -0.04891 | front + back, isolated |
| FMA52736 / FJ3394 | Sphenoid bone | unpaired | 2791 / 4238 | -0.00064 | front + back, isolated |
| FMA9710 / FJ3395 | Vomer | unpaired | 820 / 1586 | -0.00065 | front + back, isolated |

Assembled source context is preserved for all 22; dense/deep bones can be occluded. The UI offers ghost context, explicit focus, isolated enlarged inspection and educational translation, rather than asserting all surfaces are visible from one assembled angle. Small-bone list selection is the reliable touch alternative; successful separated-lacrimal picking is a bounded example, not every-pixel/touch-target acceptance.

Verification observed: front/back/left/right/superior/inferior whole-skull cameras; camera and separation retained while changing left→right lacrimal; Back restores the former selection; return clears displacement; group option restores 22 selected IDs. Search/group and source-linked bone navigation retain the bounded workspace. Saved separated scene reopened through inner-ear reference and reload with equal camera, selected ID and displacement. Existing scene schema 1 accepts the optional bounded skull state; old scenes and old 23 question identities remain unchanged. No semantic label/relationship revision is needed because existing anatomy labels/graph are unchanged; new pack has its own identity/version. Malformed skull state and non-member displacement are rejected.

Study acceptance: at390×844, inspected all22 then answered frontal for ethmoid, saw the explicit correct name/location; exited and reloaded, resumed the same wrong-feedback state. At320×568, isolation + separation retained consistent button/state, remaining21 answers were correct, summary21/22 first success, retry corrected the remaining item to22/22 and returned to the captured explorer. [Round/reload evidence](../../output/playwright/skull-study-round.txt), [wrong feedback](../../output/playwright/skull-study-wrong-390.png), [small-screen inspection](../../output/playwright/skull-study-isolated-320.png). Same-source context may remain pedagogically difficult for tiny/deep bones until enlarged/isolated; effectiveness and instructor suitability remain open.

Independent read-only review found and closed: incorrect concha description/source-row substring match, first-entry layer invariants, whole-group select no-op, and study-isolation ownership mismatch. A browser-only reference-transition crash from temporarily absent concept labels was then repaired and independently reviewed; cross-reference/reload journey rerun successfully. [State evidence](../../output/playwright/skull-state-flow.txt), [picking/save](../../output/playwright/skull-picking-save.txt), [cross-reference/reload](../../output/playwright/skull-persistence.txt). Final revision/check results belong to the delivery handoff. No expert, physical-device, live-site or full regional acceptance is implied.

### Decision: explicit study entry and retained results — 2026-10-21

- Scope/status: user-authorized correction of New / Resume / Previous result for all existing packs. No question, scoring, schedule interval, content identity or dataset version changes.
- Evidence: baseline `0c1984a`, `app/page.tsx` module launcher and `app/study-panel.tsx` initialization/reveal; [reopened criterion](progress-report-2026-10-21.md#yeniden-açılan-kriter-çalışma-başlangıcı-tamamlanmış-özeti-gösteriyor). The global last-pack key did not describe each module's stored phase; a completed session loaded behind a start label.
- Choice/reason: choose explicit entry intent from each validated module record. New resets current questions but retains cards/events/completed; Resume restores the unfinished session; Previous result is a separate read-only view. Optional schema-1 `lastResult` retains the latest detailed result across a restart. Legacy summary sessions remain readable without migration writes; aggregate-only legacy results explicitly disclose missing question details. Existing bounded aggregate history (50 rounds) is also visible. Result overview clears question selection/isolation; resuming restores the current item/isolation. Skull detail entry routes through the same chooser.
- Evidence boundary: observed software behavior and regression tests; no new learning-efficacy or anatomical claims. Earlier versions did not retain all per-question histories; missing details are not reconstructed. Explicit New replaces the current unfinished tour, as stated in the chooser.
- Rights/frame: not applicable to this state/navigation fix; geometry, IDs, labels, attribution and reference coordinates unchanged.
- Owning checks: history helpers → study panel and launcher → history/render regressions, full check:ci and actual Chrome interactions. [Delivery evidence](progress-report-2026-10-21.md#çalışma-giriş-düzeltmesi-ve-geçmiş-koruma).
- Review/result: fresh Astra review found the secondary skull entry bypass; corrected and exercised through the UI. No preservation blocker found. Parent verification uses pinned Node22.23.2, 37/37 tests and all CI gates PASS. Reviewer's earlier 9-test run used Node24 and is supplementary only.
- Open verification: physical phone, screen reader, anatomist and learning-effectiveness acceptance remain outside this software correction.
