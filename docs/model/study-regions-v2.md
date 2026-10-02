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
