# Interaction and pedagogy options

Read-only research checked **2026-10-02**. All priorities and effort ratings are **proposals/design estimates**, not implementation authorization or measured development effort. No software, accounts, assets, or application code were installed or changed for the source-interface research.

## Current implementation evidence

The code audit used `649926e81ef7909f88f754bc89b10bca417c29fa`. Documentation integration compared `app/scene.tsx`, `app/saved-scenes.ts`, `app/page.tsx`, `package.json`, and `package-lock.json` against `b5ffe57c5d160844ba40277d95a70c7a4fa43d26`: **no changes in those files**. This supports carrying the bounded code observations forward; it is not a new browser acceptance.

- Three.js declaration `^0.159.0`, locked `0.159.0`; React `19.2.6`; Vite `8.0.13`.
- System geometry is merged, with per-part indices. GPU state supplies XYZ translations and hidden/solid/ghost states; selection uses a separate texture. Picking applies matching translations.
- Ghost opacity is `.07`, skin `.1`; `MeshStandardMaterial` uses `DoubleSide`.
- There is no implemented per-part rotation/skinning system or clipping control/state. Shader includes alone do not establish a clipping feature.
- The skull's 22 bones account for **36,743 vertices / 55,866 triangles**. Position/normal/index arrays total approximately **1.33 MB before duplication/overhead**, derived from the manifest; this is not transfer, GPU-memory, or runtime measurement. Fine features are not separate meshes in this set.
- Skull geometry shares main-body chunks 12 and 13. Hide/isolate does not create a skull-only download.
- Selection resets explosion and ordinarily isolation. Explosion moves from radial/system offsets at `0–.45` to a front-facing inventory at `.45–1`; orientation stays fixed and rotation is disabled near full explosion.
- Saved-scene schema 1 includes dataset/content fingerprint, `chosenId`, language, details, camera, explode, visible, selected, hidden, isolate, view, rotate, focused, ghost, and concealLabels. It has no per-bone transforms, clipping, or animation state.
- Back history is capped at 30. Current standard cameras are front, back, side, and three-quarter; arbitrary orbit cameras can be saved.

Pinned source: [renderer](https://github.com/ismailatilan-44/human-atlas/blob/649926e81ef7909f88f754bc89b10bca417c29fa/app/scene.tsx), [saved scenes](https://github.com/ismailatilan-44/human-atlas/blob/649926e81ef7909f88f754bc89b10bca417c29fa/app/saved-scenes.ts), [page/state controls](https://github.com/ismailatilan-44/human-atlas/blob/649926e81ef7909f88f754bc89b10bca417c29fa/app/page.tsx).

Controlled translations, visibility, cameras, and lesson states fit existing foundations. Detached-bone rotation, capped cutting, articulation, and drag assembly require additional foundations.

## Mechanism matrix

| Option | Purpose | Proposed priority / effort | Conditions and limits |
| --- | --- | --- | --- |
| Preserve state across selection | Change bone without losing arrangement/question | Baseline first / low–medium | Separate selection, focus, isolation, and separation actions. |
| Skull-specific separation | Expose neighbors while retaining spatial relationships | Baseline / medium | Authored translations, original orientation, continuous orbit and appropriate camera fit. Existing packed inventory is not the sole study view. |
| Separate/return one bone | Inspect hidden surfaces then restore exact position | Baseline / medium | Independent offsets and persistent selection; optional active-bone home ghost/connector. |
| Reassemble all | Restore anatomy while retaining lesson/selection/camera where useful | Baseline / low–medium | Distinct from resetting every state field. |
| Hide/fade/isolate with context | Compare in-place, isolated, and neighboring views | Refine baseline / mostly existing | Ghost useful neighbors; overlapping whole-skull transparency may obscure boundaries. |
| Anatomical view controls | Front/back/left/right/superior/inferior access | Baseline / low–medium | Explicit laterality; avoid requiring dexterous orbit to reach inferior/superior views. |
| Selected-bone inside/outside views | Inspect named surfaces and return to assembled context | Baseline after audit / medium | Cameras/visibility presets, not newly created surfaces; verify interpretation of geometry. |
| Cranial-cavity reveal | Show internal organization | Baseline goal, mechanism undecided | List hidden bones or section; whole-frontal hide is not a calvarial cap removal. |
| Group controls | Cranial/facial, paired sides, lesson sets | Baseline / low–medium | Preserve important neighbors and laterality; source groups require membership review. |
| Guided camera sequence | Orient → select → reveal → inspect → restore → answer | Baseline / medium | Pause/reverse/free exploration without losing lesson; snapshots provide foundations. |
| Bone color mode | Distinguish neighbors | Baseline candidate / implementation-dependent | Offer bone appearance; labels/outlines supplement color; quiz must not depend on palette. |
| Landmark hotspots/regions | Learn features while retaining parent identity | Next / medium–high | Checked anchors, names, boundaries and views; whole-bone highlight is not precise segmentation. |
| Single-plane clip | Named sagittal/coronal/axial reveal | Optional advanced / medium, higher with caps | Plane slider/flip/reset; coordinate, transformed geometry, picking and annotation consistency. Does not create anatomy. |
| Arbitrary cuts/cut hole | Complex demonstrations | Later / high | Explicit modes and touch navigation burden; geometry complexity. |
| Free-drag assembly | Recall placement/orientation | Experiment / high | Rotation, snap tolerance, feedback, accessible alternative; motor skill can confound assessment. |
| Constrained assembly question | Choose missing bone/neighbor, then animate return | Prefer before free drag / medium | Uses quiz foundations with lower manipulation burden. |
| Jaw motion | Explain joint relationships | Later / reviewed movement model required | Arbitrary hinge is not physiological TMJ motion. |
| Radiology-linked section | Transfer to CT/MRI | Separate advanced project | Licensed registered imaging, reviewed plane conventions; clipping alone is not imaging. |

## Reference products: observed versus documented

| Reference | Useful pattern | Evidence actually obtained / limit |
| --- | --- | --- |
| [Ohio/WitmerLab Visible Interactive Human](https://people.ohio.edu/witmerl/3D_human.htm), [3D PDF tutorial](https://people.ohio.edu/witmerl/Downloads/Acrobat3D_Tutorial_WitmerLab.pdf), [exploding-skull item](https://sketchfab.com/3d-models/visible-interactive-human-exploding-skull-252887e2e755427c90d9e3d0c6d3025f) | Orientation-preserving separation, labelled/unlabelled passes, assembled/individual transitions; official description includes CT-derived bones, explosion, hide/isolate/transparency and sinus/endocast context. | Official page/tutorial inspected. Embedded players blank; Sketchfab fetch 403. Playback and visual quality **untested**. Reported CC BY-NC-ND item is an interaction reference, not permission to adapt geometry/animation; see [reconciled asset rights](source-options.md#institutional-and-secondary-model-listings). |
| [VOXEL-MAN exploded view](https://www.virtual-body.org/3d-navigators/brain-and-skull/exploded-view/), [brain/skull](https://www.virtual-body.org/3d-navigators/brain-and-skull/) | Separation while retaining rotation, highlights, colors and labels. | Official documented behavior only; no installed application tested. |
| [CranialLab](https://craniallab.org/), [explorer](https://app.craniallab.org/), [sphenoid workspace](https://app.craniallab.org/bone/sphenoid) | Progressive disclosure from assembled skull to bone workspace; group/visibility/inspection/explosion/reset/share controls. | Sphenoid selected and inspection route opened. Landmark panel and double-click pivot instruction observed; panel said no landmarks. Canvas black with WebGL-disabled errors: rendering, explosion and anatomy **untested**. Osteopathic primary respiratory motion content is not adopted as established anatomy. |
| [UpSurgeOn Head Atlas listing](https://apps.apple.com/pt/app/head-atlas/id1193542468) | Layered explanations and question-driven inspection; listing describes three-axis dissection, isolation, explosion, transparency and grouped hotspots. | Developer description only; app not installed/tested, quality and access level unknown. |
| [Complete Anatomy explore](https://3d4medical.com/explore), [cut documentation](https://3d4medical.com/support/complete-heart/cut), [shortcuts](https://cdn.3d4medical.com/media/complete-anatomy/support/mac_shortcuts.pdf) | Preview affected structures, retained side, undo/redo/clear and explicit exit from cutting mode. | Documentation only. Detailed cut page is under Complete Heart; not proof all options exist in the current skull screen. |
| [Visible Body Skull Bones Lab](https://www.visiblebody.com/hubfs/pdf/lab-activities/2020%20Fill-In/lab%20manual_skull%20bones_english_student_fill%20in.pdf), [navigation documentation](https://support.visiblebody.com/hc/en-us/articles/360003174453-Zooming-dissecting-and-rotating-the-3D-model) | Animated disarticulation serves learning how bones fit, rather than being the lesson itself. | Official lesson/documentation only; licensed app not tested. |

## Learning research and limits

| Study | Finding reported by research | Appropriate inference / limit |
| --- | --- | --- |
| [73-student randomized skull study](https://link.springer.com/article/10.1186/s12909-020-02255-6) | VR, cadaver skull, and atlas groups did not differ significantly in post-test scores or score changes; VR rated enjoyable/helpful for spatial understanding. | Supplementation, not automatic score improvement. Short familiarization/repeated questions; separation effect cannot be isolated. |
| [Skull-base clinical atlas report](https://doi.org/10.1055/s-0041-1729975), [paper](https://www.kockro.com/media-kockro/docs/3D-Skull-base-operative-anatomy.pdf) | Interface difficulty prompted a ten-minute tutorial; visibility/navigation frequently used; reduced density helped orientation. | Retrospective experience including 24 written reports, not randomized effectiveness. |
| [2019 VR assembly prototype](https://doi.org/10.1145/3340764.3340792), [paper](https://www.vismd.de/wp-content/uploads/legacy/pohlandt_2019_muc.pdf) | Ten mostly non-medical participants attempted shoulder assembly; none finished on time; small-object selection/knowledge problems; ghost feedback preferred. | Skull illustration is not skull-learning evidence. Supports caution and constrained tasks, not retention benefits or speed-based anatomy scoring. |
| [Color-coded liver-model study](https://doi.org/10.1038/s41598-023-35046-2), [PubMed](https://pubmed.ncbi.nlm.nih.gov/37188811/) | Small randomized comparison favored artistic color coding over photorealistic model on scores. | Skull palette benefit remains an inference. |
| [Functional-anatomy interaction study](https://pubmed.ncbi.nlm.nih.gov/38197466/) | Active interaction/video/control comparison with eight-week retention; benefit depended on visuospatial working memory. | Not skull-specific; familiarization and cognitive load matter. |
| [TEACHANATOMY trial](https://doi.org/10.1097/ACM.0000000000006012), [article](https://academic.oup.com/academicmedicine/article/100/6/695/8361672) | 48-person randomized AR cranial-nerve trial improved short-term theoretical/practical results. | AR condition also added adaptive repetition and gamification; no retention follow-up; cannot isolate display effect. |
| [Geometry/hierarchy-constrained explosion method](https://doi.org/10.1080/21681163.2017.1343686), [record](https://docs.lib.purdue.edu/cgtpubs/14/) | Medical-atlas separation constrained by geometry and hierarchy; applied to brain atlas. | Visualization method, not skull-learning validation. |

Additional pointers with limited inspection: [automated exploded-view diagrams publication](https://research.adobe.com/publication/automated-generation-of-interactive-3d-exploded-view-diagrams/) was verified but full PDF retrieval failed ([Washington PDF](https://grail.cs.washington.edu/wp-content/uploads/2015/08/li2008ago.pdf), [Princeton mirror](https://www.cs.princeton.edu/courses/archive/spr11/cos598A/pdfs/Li08b.pdf)); [anatomy retrieval-practice study](https://journals.physiology.org/doi/full/10.1152/advan.00174.2012) was discovered but full-page opening failed. Neither is treated here as extensively verified full text.

**Design inference:** reduce navigation burden and use purposeful retrieval/comparison. Evaluate what learners identify, relate, and later recall, rather than clicks or spectacle.

## Engineering and accessibility constraints for a later decision

Separation must transform rendering, picking, labels, focus, and home indicators consistently. For clipping, specify whether the plane cuts assembled anatomy before separation or the displaced scene in world coordinates; these are different teaching views.

Transparency is supporting context. Three.js sorts transparent objects rather than every triangle; merged geometry and dense overlapping surfaces need testing. Prefer bounded neighbor ghosting. [Three.js transparency manual](https://threejs.org/manual/pages/transparency.html)

Material clipping discards rendered regions; it does not create an anatomically meaningful section. Plane conventions, picking, annotations, caps, diploe and internal tissue appearance require evidence and implementation. Current online docs are general API references; validate against installed `0.159.0` before code changes. [Material documentation](https://threejs.org/docs/pages/Material.html)

Provide tap/button alternatives to dragging, searchable/list selection for tiny bones, laterality text and outlines alongside color, reduced motion and stepwise transitions. Disable auto-rotation during questions/precise inspection; preserve assembled-return and prior-view actions. Labelled controls alone do not make a canvas fully accessible: provide meaningful structure descriptions and question alternatives. [W3C dragging alternatives (AA)](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements), [interaction animation (AAA)](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions), [WCAG 2.2 target-size context](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/), [pause/stop/hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide).

Triangle count does not establish mobile performance. Test overdraw, labels, passes, shared downloads and animation on actual devices. Demand-driven stationary rendering, limited labels and short cancellable transitions are candidates. Any later saved-state extension needs versioning and compatibility for authored offsets, clipping and lesson position; restore stable state rather than unexpectedly restarting movement.

## Proposed lesson and evaluation

One situated-bone lesson could: locate from a named view → reveal neighbors → separate with home hint → inspect external/internal surfaces → return exactly → hide labels and identify from a new view → answer a relationship question with explanatory feedback. Anatomical wording and targets require review. Separation is an educational arrangement, not natural movement or a surgical procedure.

Evaluate unfamiliar-angle identification, laterality, inside/outside judgments, neighboring relationships, unaided view restoration, misclicks/mode errors, delayed recall separately from immediate completion, and touch/keyboard task success. Proposed order: preserve state; controlled separation/return; authored views/lessons; validated annotations; optional clipping; experimental free assembly and motion. No mechanism is selected or implemented by this document.
