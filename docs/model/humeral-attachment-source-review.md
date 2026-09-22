# Coracobrachialis humeral insertion review — 2026-09-22

The two unresolved targets are `atlas:left-humerus-medial-midshaft` and `atlas:right-humerus-medial-midshaft`, under coverage item `coverage:humerus-medial-midshaft`. **Neither receives a coordinate from this review.**

[UAMS, Muscles of the Upper Limb](https://medicine.uams.edu/neuroscience/education/medical-school-courses/human-structure-module/anatomy-tables/muscle-tables/muscles-of-the-upper-limb/), the coracobrachialis row's insertion column, supports the medial midshaft region of the humerus. It does not specify a point or a mesh footprint.

The pinned Z-Anatomy `Startup.blend` was reopened with automatic scripts disabled. Inspection covered 158 objects: humeral/coracobrachialis/medial-shaft name matches and every descendant of both humeri. Both humeri contain Bone/Cartilage materials only and no vertex groups. There is no named coracobrachialis humeral insertion surface or medial-midshaft marker. `Coracobrachialis muscle.ol/.or` are scapular **origin** patches and cannot supply the humeral insertion.

There is additional real source geometry: each `Coracobrachialis muscle.l/.r` has 292 faces assigned to **Tendon**, separate from 868 muscle faces. Each side's tendon material contains two disconnected components (193 and 99 faces). The source labels neither component as an insertion footprint and provides no bone attachment boundary. A distal tendon surface or its nearest humeral point would therefore require a new localization inference. Neither is promoted to an anchor.

The independent evidence package is `data/model-candidates/humeral-attachment/`: object inspection, candidate review with both `position:null`, and two source tendon-material OBJ subsets. OBJ coordinates are original Z-Anatomy world meters; these are review geometry, **not atlas-registered landmark meshes**. Export selects existing faces, applies source world transforms and corrects mirrored winding; it does not create an attachment surface. Attribution and upstream notices accompany them.

**Concrete missing source:** a bilateral, anatomically identified coracobrachialis insertion patch on the humerus, or independently reviewed landmark coordinates tied to this exact humeral mesh and its coordinate frame. A textual regional description and an unlabeled tendon end do not resolve that gap.

Reproduce with Blender background mode, `--disable-autoexec`, the pinned blend and `work/humeral-attachment-review/inspect.py`, then `inspect-tendon.py`. Both scripts are read-only with respect to the blend. Its SHA-256 is `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. No application, coverage, graph or registry file changed.
