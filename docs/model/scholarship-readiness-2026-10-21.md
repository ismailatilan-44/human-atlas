# Human Atlas — showcase and scholarship readiness

21 October 2026. Inspected implementation baseline: `fb39d24f08885e8369d060f1dc5200e57be3cc68`; integration branch: `codex/scholarship-readiness`. This is a project presentation and acceptance plan, not a scholarship application or a claim about any scholarship's eligibility requirements. No named programme, judging rubric, submission format or deadline has been supplied.

The observable outcome is a reviewer who can open the identified build, complete one coherent anatomy-exploration journey, and distinguish the project's engineering contribution from upstream anatomy and unverified learning claims. The [current delivery handoff](progress-report-2026-10-21.md) owns the integrated revision, checks, deployment status and open acceptance gates. Older [delivery evidence](progress-report-2026-10-02.md) remains historical.

## Suggested project description

Human Atlas is an open-source educational 3D anatomy explorer extended from ashemag's original application. This fork adds source-traceable regional model packages, Turkish/English/Latin labels for selected anatomy, relationship navigation, browser-local saved scenes and bounded recognition practice. A skull workspace supports orientation, individual bone selection and reversible educational separation. The engineering work keeps source identities, component attribution and reference-body boundaries visible while improving selection, camera continuity and mobile-sized interactions.

The project currently demonstrates a working exploration and recognition workflow. It does not establish complete human anatomy, clinical accuracy, expert anatomical acceptance or improved learning outcomes. Reference geometry is adapted from credited sources, rather than claimed as original anatomical modelling. A personal application should describe only work the applicant actually performed and identify collaboration/AI assistance according to the destination's rules; repository features alone do not establish individual authorship.

## Contribution and attribution

| Layer | Credit and project contribution | Evidence |
| --- | --- | --- |
| Original application | ashemag's Human Atlas provides the upstream viewer foundation. Preserve its MIT copyright; do not present the original explorer as entirely created by this fork. | [Upstream repository](https://github.com/ashemag/human-atlas), [MIT license](../../LICENSE) |
| Base reference anatomy | BodyParts3D / Database Center for Life Science supplies the adult male reference geometry and source concept hierarchy. Browser packaging and source selection are adaptations, not original anatomical discovery. | [Base attribution and adaptations](../../public/ATTRIBUTION.md) |
| Registered extensions | Selected Z-Anatomy and BP3D 4.3 assets are packaged/registered with source IDs, review evidence and limitations. This fork adds integration and bounded metadata rather than ownership of the source meshes. | [Active registry](../../public/models/extensions/index.json), [main model documentation](../../README.md#model-explorer-work), [left cord attribution](../../public/models/extensions/LEFT-CORDS-BP3D43-ATTRIBUTION.md) |
| Independent references | HRA female pelvis and Z-Anatomy regional references retain their own coordinate frames and component terms. The inner-ear package includes noncommercial/share-alike restrictions; the app's MIT license does not replace them. | [Female pelvis](../../public/models/female-pelvis/ATTRIBUTION.md), [inner ear](../../public/models/inner-ear-reference/ATTRIBUTION.md), [lower limb](../../public/models/lower-limb-nerve-reference/ATTRIBUTION.md), [upper limb](../../public/models/upper-limb-nerve-reference/ATTRIBUTION.md) |
| Fork product and engineering | Regional source/term records, relationship navigation, dataset boundaries, saved scenes, finite recognition modules, skull orientation and camera/input fixes are demonstrable fork changes. Use commit/PR evidence to attribute specific contributions to people. | [Workflow and ownership](agent-workflow.md), [study scope](study-regions-v2.md), [saved-scene/device review packet](learning-review-packet.md), [historical implementation acceptance](progress-report-2026-10-02.md) |

These are the repository's recorded component terms, not a new legal clearance. Keep the corresponding credits with screenshots, renders and redistributed packages; consult the owning attribution record for each asset used in a submission.

## A five-minute demo journey

Use the exact build identified in the delivery handoff. The sequence below is a proposed acceptance/demo script; reading the controls in code does not certify a new browser run. Start a fresh practice session or use dedicated demonstration storage so the user's saved study history is preserved.

| Step | Reviewer action | Observable result and honest explanation |
| --- | --- | --- |
| 1. Find and orient | Open the male reference, choose **Kafatası · 22 kemik**, then choose a named bone from the 22-bone list. Rotate manually. | The selected whole bone and surrounding skull are visible. Show its source identity and side; the list covers this bounded bone set, not fine cranial features. |
| 2. Inspect and return | Select another bone, use **Odaklan**, isolate/show context, and use **Geri**. Optionally use **Seçili kemiği ayır** then **Kemiği yerine döndür**. | Selection and context change while manual viewing direction survives ordinary reframing; Back restores recorded state. Separation is an educational displacement, not joint motion or a surgical cut. Named views intentionally choose a new direction. |
| 3. Follow evidence | In the main reference search for `atlas:left-biceps-brachii`, select the labelled project muscle entry, open an available source-backed attachment or nerve relationship, then return. | The destination and its geometry/marker limits remain explicit. A source relationship is an authored/source fact, not a claim that a complete nerve network or attachment footprint is modelled. |
| 4. Practise and correct | Open **Çalışma ve tekrar**, choose the whole-skull module, inspect a prompt, deliberately make one wrong answer, read correction and retry; use **Kaydet ve Geri** to leave. | The workflow separates first-attempt recognition from eventual recognition and restores the explorer. A correct naming response is not proof of clinical reasoning, retention or mastery. |
| 5. Save across references | Save the current skull scene in **Kayıtlı sahneler**, switch to the inner-ear reference, reopen the saved scene, then reload and reopen it again. | Reference, selection, visibility, separation and camera restore. Local history and scenes have no account sync; clearing browser storage removes them. Explain that the ear uses its own source frame. |

For a shorter recording, use steps 1, 2, 4 and 5; retain the attribution and scope explanation. Before recording, complete the chosen flow at desktop and a narrow viewport, inspect rendered geometry, and capture the build's source SHA. Do not edit away a failure and describe the flow as passed.

## Current scope that can be stated

The [generated inventory](model-inventory.md) and active manifests at the inspected baseline contain five datasets: 2,292 main-body parts, 27 female-pelvis parts, six inner-ear parts, 137 lower-limb parts and 127 upper-limb parts. The 2,589 combined parts stay in separate reference bodies. There are 3,838 dataset-qualified catalog records and 1,677 typed relationships; these are not distinct anatomical structures or a completeness denominator.

The main graph contains 3,516 entities and 1,539 relations; its 403 regional label records do not translate the entire source atlas. The four [study modules](study-regions-v2.md) contain 45 whole-bone recognition items: 22 skull, nine right ankle, nine left ankle and five right upper limb. Review scheduling is a transparent local interval rule, not FSRS or a validated mastery model. Scenes and study history are stored in the browser.

The [scope contract](model-scope-and-acceptance.md) retains 208 pending detail cells and three non-exhaustive target seeds totalling 1,010 requirements. No target is anatomically expert-accepted in the current generated inventory. The two registered left plexus cords do not close right-cord/root/continuity gaps; six attachment reference points do not close the two unresolved humeral locations. Source availability, geometric representation, local software acceptance, publication and expert acceptance remain separate.

## Prioritised remaining evidence

These priorities concern a credible bounded showcase. They do not require completing every anatomy region before presenting the existing engineering work.

| Priority | Missing or unresolved item | Smallest acceptance evidence |
| --- | --- | --- |
| Before presenting | Reconcile the exact local, merged and live revisions; older live evidence cannot establish that current skull/camera behavior is published. | Integrated source SHA, successful applicable checks, hosted release metadata matching that SHA, and the selected real demo journey on that hosted build. Root delivery record owns status. |
| Before presenting | Make contribution and source scope obvious to someone unfamiliar with the repository. | Reviewer can locate upstream code credit, asset/component attribution, the bounded contribution narrative and known limits without reading historical reports. Check all presentation links against the chosen build. |
| Before submitting | Tailor the package to an actual programme and the applicant's verifiable role. | Programme-provided rubric/format/deadline, applicant-approved contribution statement and requested artefacts. These inputs are currently unknown; do not invent them. |
| Before claiming device readiness | Physical phone interaction, loading/memory/thermal behavior and assistive-technology acceptance remain open. Desktop narrow viewports and Chromium-generated trusted touch events are narrower evidence. | Named device/browser, network and viewport; actual orbit/pinch/pan/tap, rotation, study exit and saved-scene restore; observed load/performance and accessibility results with failures retained. |
| Before claiming anatomical acceptance | Bounded target identity, laterality, rendered fidelity and prompt suitability need a qualified reviewer. | Named reviewer, date, exact source/version, selected targets and pass/fail/corrections using the [human review packet](learning-review-packet.md). Source-supported is not expert-verified. |
| Before claiming educational benefit | Learning improvement, transfer and usability with intended learners have not been demonstrated. Current practice tests recognition, not relation recall or clinical reasoning. | A defined learner task and consent-appropriate pilot with observations, errors and feedback; any effectiveness claim requires an appropriate study rather than usage counts or a demo score. |
| Subsequent model work | Unbound targets, term gaps, fine anatomy and network continuity remain in versioned regional queues. | One explicitly chosen source-backed package through search → selection → focus/context → relationship → return, with its owning source/target/attribution records and review gates updated. |

The release-and-demo evidence row is now technically closed by the current delivery handoff; it records the final hosted SHA, passing CI and real browser journeys. The next action is the bounded learner/anatomist review. New anatomy acquisition, clinical content, account/backend work and a scholarship submission are separate decisions.

## Verification of this documentation

This record was prepared by reading the active manifests, registry, generated inventory, knowledge/label/reference JSON, runtime reference and study controls, package scripts, attribution and existing acceptance records at `fb39d24`. Counts were recomputed from those files. Documentation checks cover local-link targets and whitespace; final executed commands and integration results belong in the current delivery handoff. No new anatomical review, learning study, physical-device test or live acceptance is established by this document alone. Active work/wait duration was not instrumented and is unknown.
