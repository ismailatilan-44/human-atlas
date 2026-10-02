# Z-Anatomy distal leg nerve candidate

Nerve objects: `Tibial nerve.l`, `Tibial nerve.r`, `Common fibular nerve.l`, and `Common fibular nerve.r` from `Z-Anatomy/Startup.blend` in the [Z-Anatomy archive](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/Z-Anatomy.zip). Reference-context meshes are bilateral `Tibia`, `Fibula`, `Patella`, `Talus`, and `Calcaneus` from that same source file. Each selected nerve is a separate authored Bezier curve; separate deep/superficial fibular, plantar, sural and muscular/digital branches are excluded.

Attribution: **Z-Anatomy — The libre 3D atlas of anatomy — CC BY-SA 4.0**; Gauthier Kervyn (design, 3D, anatomy). Underlying-model attribution retained: **BodyParts3D — The Database Center for Life Science — CC BY-SA 2.1 Japan**; Kousaku Okubo (original BodyParts3D model). The base Human Atlas license does not relicense Z-Anatomy's additions.

These derivatives retain the upstream general [CC BY-SA 4.0 declaration](https://creativecommons.org/licenses/by-sa/4.0/), [upstream license and notices](./UPSTREAM-LICENSE.txt), and the limitation that object-specific author/source lineage is not supplied. Upstream also lists noncommercial inner-ear and kidney references/adaptations; those groups are excluded. No blanket commercial clearance or relicensing of the archive is asserted.

Adaptations: evaluated curve-to-triangle conversion preserving authored splines, radii, bevel settings and open ends; reflected-object winding correction; uniform coordinate transform; angle-weighted normals quantized to Int16; Float32 positions, Uint32 indices and binary/gzip packing. No nerve redrawing, inferred branches, caps, decimation, local warping, or per-structure displacement.

The sciatic-frame diagnostic package has an independently observed distal registration mismatch and is not approved for addition to the main atlas. Same-source context is required to preserve the observed distal relationships. Geometry availability and technical validation do not establish anatomical correctness, full nerve coverage, or expert acceptance.

Source SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`. Source originally obtained 2026-09-08; this package audit: 2026-10-02. Anatomical expert review remains pending.

The source-reference package uses only one display-axis rotation for every object. Its bone context retains source mesh defects documented in `source-reference-checks.json`; no normal or topology repair is claimed.
