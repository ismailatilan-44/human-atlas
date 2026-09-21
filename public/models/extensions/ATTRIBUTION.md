# Z-Anatomy upper-arm extensions

Selected source objects: `Musculocutaneous nerve.l` and `Musculocutaneous nerve.r` from `Z-Anatomy/Startup.blend` in the [Z-Anatomy source archive](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/Z-Anatomy.zip).

Attribution: **Z-Anatomy — The libre 3D atlas of anatomy — CC BY-SA 4.0**; Gauthier Kervyn (design, 3D, anatomy). Underlying model attribution retained as requested upstream: **BodyParts3D — The Database Center for Life Science — CC BY-SA 2.1 Japan**; Kousaku Okubo (original BodyParts3D model). The original BodyParts3D database now [declares CC BY 4.0](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html); this does not relicense Z-Anatomy's additions.

The landmark extension also derives six point coordinates from `Coracobrachialis muscle.ol/.or`, `Long head of biceps brachii.ol/.or`, and `Biceps brachii muscle.el/.er` attachment surfaces in the same source file. Area-weighted surface centroids are projected to their source patches and transformed into atlas coordinates. The accompanying technical QA images display these patches with source/atlas bones. Two humeral insertion landmarks remain unresolved.

These selected derivative geometries are distributed under the upstream general [CC BY-SA 4.0 declaration](https://creativecommons.org/licenses/by-sa/4.0/). Preserve this attribution and the accompanying [upstream license and notices](./UPSTREAM-LICENSE.txt), retrieved 2026-09-22 from [License.txt](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/License.txt).

Adaptations: curve-to-triangle conversion preserving source bevel dimensions, measured uniform scaling/rotation/translation into Human Atlas coordinates, reflected-object winding correction, recomputed vertex normals quantized to signed 16-bit, binary packing and gzip compression. No anatomical path editing or geometry decimation.

Upstream lists additional reference/included/adapted materials, including noncommercial inner-ear and kidney sources. Neither of those object groups is exported here. Upstream does not provide object-specific author/source lineage for these selected nerves and attachment surfaces, so the general declaration is recorded with that limitation; no blanket commercial clearance or relicensing of the archive is claimed.

Source SHA-256: `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`.

## Median nerve extension

`median-nerves.json` / `.bin` / `.bin.gz` derive only from `Median nerve.l` and `Median nerve.r` in the same verified `Startup.blend`. Each source object has two splines; the original source curve bevel and both spline geometries are retained. Separate muscular, palmar and digital branch objects are not included. Adaptations are curve-to-mesh conversion, the existing measured atlas similarity transform, mirrored winding correction, recomputed quantized normals and binary/gzip packing. The same upstream CC BY-SA 4.0 declaration, attribution and object-specific provenance limitations above apply. Forearm/wrist bone agreement is measured separately; no complete median nerve arborization or expert anatomical validation is claimed.
