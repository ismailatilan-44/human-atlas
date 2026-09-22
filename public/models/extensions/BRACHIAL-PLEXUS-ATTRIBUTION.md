# Partial Z-Anatomy brachial plexus source reference

The 20 selected CURVE objects are the bilateral `Superior/Middle/Inferior trunk of brachial plexus`, the `Anterior/Posterior division` of each of those three trunks, and `Posterior cord of brachial plexus`. Exact source names are retained per part and in `brachial-plexus.json`.

Source: `Z-Anatomy/Startup.blend` in the [Z-Anatomy source archive](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/Z-Anatomy.zip), SHA-256 `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`.

Attribution: **Z-Anatomy — The libre 3D atlas of anatomy — CC BY-SA 4.0**; Gauthier Kervyn (design, 3D, anatomy). Underlying source attribution retained as requested upstream: **BodyParts3D — The Database Center for Life Science — CC BY-SA 2.1 Japan**; Kousaku Okubo (original BodyParts3D model). BodyParts3D's current [CC BY 4.0 declaration](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html) does not relicense Z-Anatomy's additions.

These selected derivatives follow the upstream general [CC BY-SA 4.0 declaration](https://creativecommons.org/licenses/by-sa/4.0/). Preserve this file and [upstream notices](./UPSTREAM-LICENSE.txt). Upstream separately lists noncommercial inner-ear/kidney references or adaptations and does not supply object-specific lineage for these curves. Those object groups are not included; no blanket commercial clearance or relicensing of the archive is claimed.

Adaptations: original curve tubes converted to triangle meshes; the existing upper-arm similarity transform applied; mirrored-object winding corrected; vertex normals recomputed and quantized to Int16; binary/gzip packing. No decimation, local deformation, invented cord, root-level segmentation, endpoint welding or anatomical reconnection was performed.

This is incomplete source coverage with limited neck/shoulder registration. Separate medial and lateral cord objects were not found. Both source root bundles are excluded: each includes five main geometric paths, an unverified superior branch and communication, plus three geometry-free one-point remnants. Their topology does not establish per-level C5–T1 identities. Existing median and musculocutaneous nerve objects are not duplicated. Expert anatomical review remains pending; proximity of rendered segments must not be read as verified connectivity.
