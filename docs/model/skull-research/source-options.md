# Asset candidates, licenses, and source limits

Research checked **2026-10-02**. No new assets were downloaded or imported. External listings/manifests support **source statements**, not binary or visual validation. Earlier repository measurements remain dated prior evidence. No reviewed candidate is established as a license-resolved, frame-compatible, higher-detail complete replacement for the existing 22-bone assembly.

## Comparison matrix

| Source / inspected version | Intended role | Component rights | Frame / separability | Detail / performance evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Current BP3D 4.0 derivative | Whole-skull baseline | Direct BP3D CC BY 4.0; preserve attribution | TARO shared frame; 22 identified parts | 55,866 triangles; fine features unvalidated | Verified repository inventory; expert review pending |
| Direct BP3D official archives | Compare specific original bones | Official CC BY 4.0 | Same family is promising, exact version/conversion still required | OBJ 99 archive listed 136 MB, PARTOF 62 MB; no proven finer 4.3 skull list | Candidate, not verified upgrade |
| Z-Anatomy `ad876c0` | Targeted fine-feature/object audit | General BY-SA 4.0 plus object exceptions below | Preserve source transforms; not assumed TARO-compatible; names can be text/empty geometry | Archive 86,734,957 bytes; no new skull-wide quality audit | Conditional object-level lead |
| Vanatome `8185b3f`, dataset 1.4.0 | Web packaging reference | MIT code ≠ assets; upstream component terms remain | Normalized coordinates; conversion unaudited; inspected bundle lacks skull bones | Skeletal 3,882,928 bytes; not skull cost | Negative scoped skull finding |
| HRA united male/female and master crosswalk v1.10 | Organ-reference ecosystem | CC BY 4.0 | Distinct reference bodies; no skull asset identified | No skull budget to measure | Negative scoped skull finding |
| HRA Skeleton ASCT+B v1.3 | Target/terminology checklist | CC BY 4.0 | Table only: no anchors, frame or meshes | Feature rows/IDs need review | Content candidate, not geometry |
| SPL head/neck, 2015 release, `head-neck-2016-09.zip` | Independent CT/labelmap comparison | Slicer agreement 1.0 Part B | CT MANIX; different specimen; 22-part separation unknown | CT reduced to 256×256; geometry budget unknown | Source description verified; package uninspected |
| SPL inner ear, February 2018 | Separate high-resolution imaging reference | Same Slicer terms | Frame, laterality, IDs and main fit unknown | Approx. 140 μm source imaging; delivered mesh accuracy unknown | Targeted future comparison |
| Ohio/WitmerLab OUVC 10503, 2018-09-17 | Exploding-skull benchmark | CC BY-NC-ND listing | Component IDs/frame uninspected | 1.1M triangles, 562,900 vertices listed | Reference only; adaptation rights not established |
| Brighton cut skull, 2017-05-04 | Independent interior-view comparison | BY-SA label; exact version unresolved | Physical cap cut, not articulation; 22-part split/units unknown | 1.1M triangles, 551,600 vertices listed | Conditional candidate |
| Ualde disarticulated skull, 2018-03-06 | Secondary gap-specific lead | BY label; exact terms/package unresolved | Specimen, frame and 22-object map unknown | 1.4M triangles, 779,100 vertices listed | Lower-confidence candidate |
| alebogino cranial foramina | Secondary opening-reference lead | BY label; exact terms/package unresolved | Claimed individual CT; institution/frame/segmentation unknown | 895,600 triangles, 445,500 vertices; 18 annotations ≠ verified canals | Lower-confidence candidate |
| Dundee CAHID, 2021-04-25 | Cranial-nerve/foramen lead | Archive says BY 4.0; current listing NoAI/no visible download license | Exact object/version provenance unresolved | 3.5M triangles, 1.7M vertices listed | Rights reconciliation required |

Published polygon counts do not establish target fidelity, transfer, GPU memory, or mobile responsiveness. Millions of triangles exceed the current subset but reliable cost requires an actual package and device test.

## Direct BodyParts3D

[Official download page](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html) lists polygon/relationship packages, including `isa_BP3D_4.0_obj_99.zip`. Its “99% polygon reduction” wording is not evidence of higher detail than the current derivative. No verified finer skull subasset list for 4.3 was obtained. [Official license](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html), updated 2025-02-27, states CC BY 4.0 with BodyParts3D / Database Center for Life Science attribution. This governs direct source distribution; it does not relicense Z-Anatomy additions or third-party NC content.

## Z-Anatomy and existing records

Pinned [repository](https://github.com/Z-Anatomy/Models-of-human-anatomy/tree/ad876c0af51563498816c6f0da4283ebd1914ffa), [license](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/ad876c0af51563498816c6f0da4283ebd1914ffa/License.txt), [readme](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/ad876c0af51563498816c6f0da4283ebd1914ffa/Readme.md). The general BY-SA 4.0 notice separately credits historical BP3D BY-SA 2.1 Japan, Dundee Cranial Nerves and Foramina BY 4.0, Dundee inner ear BY-NC-SA 4.0, Lissie Cowley kidney BY-NC 4.0, and Wikipedia-derived definitions BY-SA 3.0 with translation cautions. Archive notice is not per-object provenance or blanket commercial clearance.

[Prior project audit](../2026-09-08-open-assets-review.md) and [evidence](../2026-09-08-open-assets-evidence.json) recorded 7,184 objects: 4,569 meshes, 951 curves, 1,660 texts; only 2,964 mesh objects had polygons, while 1,605 were empty. These counts do not establish skull completeness. Existing [inner-ear reference](current-inventory.md#independent-inner-ear-reference) demonstrates the importance of separate frame/component rights.

## Vanatome: current negative finding, prior findings retained

Pinned [repository](https://github.com/vixotic/Vanatome/tree/8185b3fa46a1dbefdd907390918c57954fd9b816) at 2026-08-05; inspected [1.4.0 manifest](https://github.com/vixotic/Vanatome/blob/8185b3fa46a1dbefdd907390918c57954fd9b816/public/models/z-anatomy-1.4.0-manifest.json), [catalog](https://github.com/vixotic/Vanatome/blob/8185b3fa46a1dbefdd907390918c57954fd9b816/public/atlas/demo-1.4.0/catalog.json), [skeletal metadata](https://github.com/vixotic/Vanatome/blob/8185b3fa46a1dbefdd907390918c57954fd9b816/public/atlas/demo-1.4.0/skeletal.metadata.json), [asset license](https://github.com/vixotic/Vanatome/blob/8185b3fa46a1dbefdd907390918c57954fd9b816/ASSET-LICENSE.md).

Source-object/name searches found no skull, frontal, parietal, temporal, sphenoid, ethmoid, maxilla, mandible, vomer, zygomatic, lacrimal, palatine or nasal bone assets. Skeletal bundle: 181 nodes/184 structure records below the head; SHA-256 `8cbea4cc15fb2063853491634eb2c57b57cf7f104f7160c4eed82cf9e392ab0d`. Full bundle listing: 31,849,556 bytes, 807 structures/984 nodes. These are distinct distribution/catalog measures from the historical review's 749 node-mapped structure IDs; do not silently compare differing denominators as growth. Source Blender hash matches the project's `9f08a17e…35afcd`. No unseen/future head package is ruled out.

## HRA geometry versus target vocabulary

Inspected [hra-kg commit](https://github.com/hubmapconsortium/hra-kg/tree/fca41ae2e23f825f2921843c276e80509fa778f1), complete 7,723-path tree, [female v1.10 crosswalk](https://github.com/hubmapconsortium/hra-kg/blob/fca41ae2e23f825f2921843c276e80509fa778f1/digital-objects/ref-organ/united-female/v1.10/raw/crosswalk.csv), [male crosswalk](https://github.com/hubmapconsortium/hra-kg/blob/fca41ae2e23f825f2921843c276e80509fa778f1/digital-objects/ref-organ/united-male/v1.10/raw/crosswalk.csv), and [master crosswalk](https://github.com/hubmapconsortium/hra-kg/blob/fca41ae2e23f825f2921843c276e80509fa778f1/digital-objects/ref-organ/asct-b-3d-models-crosswalk/v1.10/raw/asct-b-3d-models-crosswalk.csv). Adjacent `metadata.yaml` records 2026-06-15, BY 4.0 and reference creators Kristen Browne/Heidi Schlehlein. DOIs: [female](https://doi.org/10.48539/HBM637.DWBM.744), [male](https://doi.org/10.48539/HBM833.WZWN.425), [master](https://doi.org/10.48539/HBM626.BRWN.943).

No skull/cranial/facial bone matches were identified in those three crosswalks; parietal operculum/palatine tonsil are not bones. This is not absence across every HRA ontology or future release. [Older library](https://github.com/hubmapconsortium/ccf-3d-reference-object-library/tree/f1a3a63f110e27ff0736047d52d04dba5d3087f9) v1.2 filenames also lacked a skull package, but current crosswalks provide the stronger scoped evidence. Earlier useful female-organ findings remain valid for their own scope.

Skeleton ASCT+B [v1.3 table](https://github.com/hubmapconsortium/hra-kg/blob/fca41ae2e23f825f2921843c276e80509fa778f1/digital-objects/asct-b/skeleton/v1.3/raw/asct-b-vh-skeleton.csv), [metadata](https://github.com/hubmapconsortium/hra-kg/blob/fca41ae2e23f825f2921843c276e80509fa778f1/digital-objects/asct-b/skeleton/v1.3/metadata.yaml), [DOI](https://doi.org/10.48539/HBM449.KQWN.983): 2026-06-15, BY 4.0. AS5/AS6 fields include fine features and UBERON IDs, some blank. “cribiform,” “crista galla,” and “tympanic caniliculus” require review. Directory/header v1.3 conflicts with an old v1.1/2024 citation string; preserve that discrepancy. The 84 filtered neurocranium rows are not exhaustive skull coverage. Table entries provide no coordinates or geometry.

## SPL/OpenAnatomy

[Head and neck](https://www.openanatomy.org/atlas-pages/atlas-spl-head-and-neck.html): published September 2015, package `head-neck-2016-09.zip`; CT MANIX reduced to 256×256. Described components include skull, mandible, spine/ribs, neck muscles, cartilage, vessels and glands, with imaging/labelmaps/models. No binary inspection established 22 separable bones, bilateral IDs, fine foramina or budget.

[Inner ear](https://www.openanatomy.org/atlas-pages/atlas-spl-inner-ear.html): February 2018, `inner-ear-2018-02.zip`; approximately 140 μm high-contrast flat-panel CT. Imaging resolution is not delivered-surface accuracy. Laterality, frame, segmentation and budget remain unknown.

Both link [Slicer Contribution and Software License Agreement 1.0, December 2005, Part B](https://www.openanatomy.org/atlas-pages/slicer-license.html). It permits use/reproduction/derivatives/distribution subject to notices, full terms, third-party obligations and modification identification; it cautions against clinical applications. Neither dataset is simply CC BY, and neither is the TARO specimen. No agreement was accepted or package acquired here.

## Institutional and secondary model listings

- [Ohio/WitmerLab exploding skull](https://sketchfab.com/3d-models/visible-interactive-human-exploding-skull-252887e2e755427c90d9e3d0c6d3025f): OUVC 10503, OhioHealth O'Bleness Hospital CT, Ryan Ridgely using Amira/Maya. Listing dated 2018-09-17. CC BY-NC-ND makes adaptation/redistribution into Atlas an unresolved rights question, not an approved source. Listing metadata was accessible in search; direct page returned 403, no viewer geometry inspection.
- [Brighton modern-human cut skull](https://sketchfab.com/3d-models/modern-human-skull-f55ae4d36e52457fa1401edd57d4bb4f): Booth Museum loan collection, donated to medical science, digitized by University of Brighton Cultural Informatics; 2017-05-04. Physical top removed. BY-SA label's exact version unresolved; no binary/viewer inspection or separability proof.
- [Ualde disarticulated skull](https://sketchfab.com/3d-models/craneo-desarticulado-disarticulated-skull-50edae6fcc2e40c4a2023fee215d4555): description lists 15 bone/tooth categories, not a verified 22-object map. Specimen provenance missing in retrieved description. BY listing alone is insufficient acquisition evidence.
- [alebogino foramina](https://sketchfab.com/3d-models/foramenes-craneales-e9a9a10116694f2b8287d532acaa4e2b): claims normal-individual CT, removed top and 18 annotated openings. Annotations do not prove faithful canal courses; institutional provenance and segmentation remain unresolved.
- [Dundee CAHID Cranial Nerves and Foramina](https://sketchfab.com/3d-models/cranial-nerves-and-foramina-a9358ee7a6dd4ea18a3622114405a4c7): Sophia Lappe, 2021-04-25, BP3D-based. Retrieved current page showed NoAI and no visible download license, while [Z archive notice](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/ad876c0af51563498816c6f0da4283ebd1914ffa/License.txt) says BY 4.0. Do not flatten these distinct versions/statements into blanket rights; exact archive-object correspondence must be reconciled first.

## Excluded as freely redistributable geometry

| Source | Evidence | Decision boundary |
| --- | --- | --- |
| [IT'IS MIDA](https://itis.swiss/virtual-population/regional-human-models/mida-model), [DOI](https://doi.org/10.13099/ViP-MIDA-V1.0) | v1.0, 2015-04-22; official 115 structures, 500 μm isotropic, STL/MAT/RAW/NIfTI. [2024 agreement §2.3.2](https://itis.swiss/assets/Downloads/VirtualPopulation/License_Agreements/LicenseAgreementMIDA_2024.pdf) prohibits original/modified model redistribution; free nontransferable use has conditions including disguised face imagery. | Free access is not web redistribution permission. No agreement/download. [Method paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4406723/) partly accessible; useful pointer to verifying holes against slices, not newly inspected geometry evidence. |
| [CranialLab](https://craniallab.org) | Photogrammetry/free-use descriptions alongside copyright/all-rights-reserved; terms inaccessible. | No transferable asset license established; motion claims not anatomy validation. |
| [Smithsonian Kow Swamp cranium](https://www.si.edu/object/3d/homo-sapiens-cranium%3A81b6a3c1-4a09-4416-82ed-937612dcf310) | CC0 metadata distinguished from model conditions describing noncommercial/educational/personal use. | Metadata CC0 does not relicense the model. |

## Future intake gates

For each proposed object separately record identity/name/side/type/polygon existence; release and hash/specimen/creator; exact component rights and attribution; units/axes/handedness/origin/shared transforms; actual surface separability versus teaching cuts; target-specific openings/plates/inner-surface/channel fidelity; compressed transfer, CPU/GPU memory, materials, batching/draw calls, picking and actual device behavior. Preserve source IDs and transformations; do not independently fit mixed-specimen bones until they appear assembled.

Keep identity review, landmark placement, passage relations and lesson-specific geometry acceptance distinct. Watertightness can coexist with an incorrectly closed foramen. A download license, successful export, or larger polygon count cannot close medical acceptance. Reuse current bones first; investigate external geometry only for a demonstrated target-level gap after the product decision.
