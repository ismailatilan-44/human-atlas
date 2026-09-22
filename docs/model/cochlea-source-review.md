# Bilateral cochlea source and geometry review

Two concrete cochlear surfaces were recovered from the pinned Z-Anatomy archive and exported into `data/model-candidates/cochlea/`. They remain an **inactive noncommercial candidate**, with no application, registry, coverage, labels, source registry or graph changes. The limitation is not missing geometry: it is the narrower upstream inner-ear licensing scope, incomplete object-level provenance, and unvalidated fine anatomical placement.

## Official BodyParts3D checked first

A fresh copy of the [official 4.3 concept-to-object mapping](https://lifesciencedb.jp/bp3d/get-info.cgi?version=4.3&cmd=concept-objfiles-list) is retained as `bp3d-v43-mapping.zip`. It contains no FMA60201 cochlea entry. The existing complete 4.3 object-name catalog was also searched for cochlea, inner ear, labyrinth, semicircular and vestibule. Only vestibulocochlear nerve names matched; those are not cochlear surfaces. The precise scoped negative result is saved in `bp3d-search-evidence.json`. It is not a claim that all possible future or unpublished BP3D data lack a cochlea.

## Source objects and terms

The source blend SHA-256 is `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`, from `Z-Anatomy/Startup.blend`. `Cochlea.l` and `Cochlea.r` are mesh objects parented to `Internal ear.g`. Each has 783 base vertices and 772 base polygons, with an authored visible subdivision modifier at level 1. Neither is a two-vertex marker or text label. Object properties and collection membership are captured in `object-provenance.json`.

The [Z-Anatomy license file](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/License.txt) identifies Dundee's inner-ear work under CC BY-NC-SA 4.0 among its referenced/included/adapted sources. The [University of Dundee's own page](https://www.dundee.ac.uk/tilt/medical-illustration/anatomy-inner-ear) confirms that license and the earlier McGill derivative lineage. Both were checked on 2026-09-22. The raw Z-Anatomy license is retained; selected Dundee facts and the verified URL are in `license-provenance.json` because direct file retrieval returned HTTP 403 even though the web reading tool could access the page.

The blend has no source-author or license property on either cochlea. Their association with Dundee's inner-ear component is therefore an explicit provenance inference. Both objects are isolated under `zanatomy-cochlea-noncommercial`, without laundering the archive's broad BY-SA declaration into object-specific commercial clearance. `ATTRIBUTION.md` preserves the narrower noncommercial/share-alike treatment and the relevant author credits. The source ID `bodyparts3d-4.3-live` is intentionally **not** used for these Z-Anatomy meshes.

## Geometry and registration

Each evaluated surface contains 3,110 vertices and 6,168 triangles. The left source transform is mirrored and triangle winding is corrected. The two authored objects appear as mirror-related surfaces; they are not independent specimen evidence. Isolated left/right renders show a spiral shell-like form. The inner-ear context render shows the same cochlea beside the source vestibular/semicircular model, which is excluded from the exported binary.

Both meshes have 52 boundary edges and no non-manifold edges. Open source boundaries are preserved; the surfaces are not presented as watertight volumetric segmentations. No organ of Corti, hair cells, nerve branch, compartment labels or internal membrane completeness is asserted.

A new cranial similarity registration uses both temporal bones and the sphenoid as labeled fit surfaces, with the occipital bone held out. It does not reuse an arm/neck transformation and does not fit either cochlea. One uniform scale (1.02913), rotation and translation applies to both source surfaces. No local distortion or manual placement is used.

| Bone reference | Role | Bidirectional RMS |
| --- | --- | ---: |
| Left temporal bone → FJ3281 | Fit | 2.698 mm |
| Right temporal bone → FJ3386 | Fit | 2.660 mm |
| Sphenoid → FJ3394 | Fit | 0.983 mm |
| Occipital → FJ3309 | Holdout | 0.633 mm |

These discrepancies reflect differences between the source skull and the atlas, not a measurement of cochlear accuracy. Temporal errors are material relative to the roughly 6.6 × 8.2 × 10.1 mm cochlear bounding sizes, so the package does not claim submillimeter placement. Within 25 mm of each mapped cochlea, temporal-surface RMS is 3.061 mm left and 3.012 mm right; these local measurements are retained in `quality-registration.json`. Expert local placement review remains necessary before representing this as anatomically validated integration.

## Staged outputs

- `cochlea.json`, `cochlea.bin`, `cochlea.bin.gz`: two-part candidate in the standard extension layout, including `sourceObject`, `sourceObjectType` and `chunks[].gzip`; 259,992 binary bytes, 150,067 gzip bytes, 12,336 total triangles.
- Concept IDs: `atlas:left-cochlea`, `atlas:right-cochlea`. Geometry IDs: `ZA-COCH-L`, `ZA-COCH-R`.
- `cochlea-left/right-base.obj` and `cochlea-left/right-evaluated.obj`: selected source surfaces in original source-world coordinates, retained independently of the display binary.
- `object-provenance.json`, `license-provenance.json`, `ATTRIBUTION.md`, `checksums.json`: identity, attribution limits and artifact fingerprints.
- `work/cochlea-review/export-cochlea.py`: reproducible Blender exporter with pinned blend and atlas hashes, run with `--disable-autoexec`; it writes only candidate/review outputs.
- `work/cochlea-review/left-closeup.png`, `right-closeup.png`, `bilateral-superior.png`, `temporal-context.png`, `left-inner-ear-context.png`: actual source-derived renders inspected during review.

The candidate closes the source-acquisition gap and can be inspected as actual geometry. It should remain distinct from the registered atlas until the intended distribution is compatible with the scoped terms and the fine placement is accepted. The manifest's proposed `/models/extensions/` URLs are not live assets; all files remain in the candidate directory.
