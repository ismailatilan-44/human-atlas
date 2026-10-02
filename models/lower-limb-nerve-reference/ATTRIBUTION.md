# Z-Anatomy lower-limb nerve reference

This independent reference derives from `Z-Anatomy/Startup.blend` in the [Z-Anatomy archive](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/Z-Anatomy.zip), acquired 2026-09-08 and reviewed 2026-10-02. Source SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`.

This 119-object candidate preserves the previous 87-object reference and adds thirty source-named intrinsic foot muscle objects plus two compound foot sesamoid objects. Totals: sixteen named nerve curves, two fibular artery curves, six ankle ligament surfaces, thirty muscle objects and sixty-five bone objects. They include the previous pelvis-to-ankle reference plus bilateral deep/superficial fibular, sural, medial/lateral plantar nerves; fibular arteries; anterior/posterior talofibular and calcaneofibular ligaments; navicular/cuboid/cuneiform bones, metatarsals and toe phalanges. Exact source names, including source wording “finger of foot,” remain in the manifest. This male regional reference preserves their common source frame. It is not registered to the main Human Atlas body.

## Attribution and separate notices

**Z-Anatomy — The libre 3D atlas of anatomy — CC BY-SA 4.0.** Gauthier Kervyn (design, 3D, anatomy). General derivative license: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/).

Underlying-model notice retained separately: **BodyParts3D — The Database Center for Life Science — CC BY-SA 2.1 Japan.** Kousaku Okubo (original BodyParts3D model). [BodyParts3D source](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html).

The [verbatim upstream license and notices](UPSTREAM-LICENSE.txt) include noncommercial inner-ear and kidney references/adaptations. Those groups are excluded here. Upstream does not provide object-specific author/source lineage; no blanket commercial clearance of the archive or relicensing of underlying components is asserted. The application's MIT license and base atlas CC BY 4.0 attribution do not replace these notices.

## Adaptations and scope

All objects receive one common orthonormal display-axis rotation from X left / Y posterior / Z superior to X left / Y superior / Z anterior, in meters. No fitting, scale change, translation or independent object movement is applied to package geometry. Authored curve splines, variable radii, bevel settings and open ends are evaluated to triangles. Reflected-object winding is corrected; Float32 positions, Int16 angle-weighted normals, Uint32 indices and deterministic gzip are encoded without decimation.

Source bone topology is retained, including loose fibular vertices, local normal disagreement in calcanei, fourth metatarsals, medial/lateral cuneiforms and third-toe middle phalanges, and sacral normal/topology defects. Vertices unused by faces receive a default up normal. Where source bone face normals cancel at a used vertex, the largest incident face supplies its fallback normal; this is disclosed in the manifest and geometry checks. No faces are removed or filled, and no source topology repair is claimed. No synthetic nerve connections, caps, paths or branches are added.

The named nerve and fibular artery objects are not complete lower-limb innervation or circulation. Each medial plantar nerve has three source splines; its middle one-point spline produces no surface and is retained as metadata. Each ankle ligament is an authored single-quad sheet evaluated with Subdivision and 0.5 mm Solidify modifiers; fine fascicular and attachment detail is not claimed. Separate muscular/digital nerve branches, independently identified lumbosacral roots, remaining vessels, muscles and joint supports are outside this package. Geometry availability and technical validation do not establish anatomical expert acceptance, which remains pending.


## Intrinsic-foot candidate adaptation — 2 October 2026

The exact 32 added source-object/part/concept mappings are in `new-object-mapping.json` beside the candidate exporter. Named flexor hallucis brevis and adductor hallucis heads are separate because the source explicitly supplies those head objects. Lumbrical, plantar/dorsal interosseous and sesamoid objects remain compound source selections; no numbered muscles or medial/lateral sesamoid identity is invented. The source-parenthesized opponens object retains that identity qualification.

All added objects use the same common orthonormal axis rotation and Float32/Int16/Uint32 encoding as the existing reference. Original evaluated positions and triangles are preserved, including a pair of coincident opposing triangles in each abductor hallucis. Three vertices per side have cancelling normals; the largest incident face supplies a disclosed fallback normal. Across twenty-two muscle objects, eighty source triangles have nonpositive averaged vertex-normal agreement. Those faces are retained and recorded; no source mesh repair is claimed. The sesamoid objects have two connected components each and remain a single selectable source group per side.

No other newly inspected foot/ankle support geometry is distributed in this candidate. The support inventory, compound identities, source-normal limitations and pending anatomical expert review remain separate from product integration or full regional acceptance. The preserved baseline87 files are included solely as reproducible source-frame package inputs with their existing attribution and terms.
