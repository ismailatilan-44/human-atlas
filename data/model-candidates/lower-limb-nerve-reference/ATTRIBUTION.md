# Z-Anatomy lower-limb nerve reference

This independent reference derives from `Z-Anatomy/Startup.blend` in the [Z-Anatomy archive](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/Z-Anatomy.zip), acquired 2026-09-08 and reviewed 2026-10-02. Source SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`.

The 21 selectable objects are bilateral `Sciatic nerve`, `Tibial nerve`, `Common fibular nerve`, `Tibia`, `Fibula`, `Patella`, `Talus`, `Calcaneus`, `Femur`, `Hip bone` (each `.l` and `.r`), and `Sacrum`. This male regional reference preserves their common source frame. It is not registered to the main Human Atlas body.

## Attribution and separate notices

**Z-Anatomy — The libre 3D atlas of anatomy — CC BY-SA 4.0.** Gauthier Kervyn (design, 3D, anatomy). General derivative license: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/).

Underlying-model notice retained separately: **BodyParts3D — The Database Center for Life Science — CC BY-SA 2.1 Japan.** Kousaku Okubo (original BodyParts3D model). [BodyParts3D source](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html).

The [verbatim upstream license and notices](UPSTREAM-LICENSE.txt) include noncommercial inner-ear and kidney references/adaptations. Those groups are excluded here. Upstream does not provide object-specific author/source lineage; no blanket commercial clearance of the archive or relicensing of underlying components is asserted. The application's MIT license and base atlas CC BY 4.0 attribution do not replace these notices.

## Adaptations and scope

All objects receive one common orthonormal display-axis rotation from X left / Y posterior / Z superior to X left / Y superior / Z anterior, in meters. No fitting, scale change, translation or independent object movement is applied to package geometry. Authored curve splines, variable radii, bevel settings and open ends are evaluated to triangles. Reflected-object winding is corrected; Float32 positions, Int16 angle-weighted normals, Uint32 indices and deterministic gzip are encoded without decimation.

Source bone topology is retained, including loose fibular vertices, local calcaneal normal disagreement and sacral normal/topology defects. Vertices unused by faces receive a default up normal. Where source bone face normals cancel at a used vertex, the largest incident face supplies its fallback normal; this is disclosed in the manifest and geometry checks. No faces are removed or filled, and no source topology repair is claimed. No synthetic nerve connections, caps, paths or branches are added.

The six named nerve objects are not complete lower-limb innervation. Separate plantar, deep/superficial fibular, sural, muscular and digital branches, independently identified lumbosacral roots, vessels and muscles are outside this package. Geometry availability and technical validation do not establish anatomical expert acceptance, which remains pending.
