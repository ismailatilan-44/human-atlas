# Female pelvis — standalone source and viewer candidate

`female-pelvis.json` + `female-pelvis.bin` + `female-pelvis.bin.gz` form a standalone dataset in the project's Atlas-style binary layout. The chunk URLs and attribution path are relative to this folder. Serve the folder together or resolve these URLs against the manifest URL. **Do not merge into the male atlas**: coordinate frame, dataset identity and sex are separate.

The selected files contain 27 source surfaces: 11 in the uterus file (including a separate cervicovaginal junction context surface), left and right ovaries, and 14 pelvic bone/tissue surfaces. The `hra-female:uterus-female` aggregate includes the source `VH_F_uterus` hierarchy; it intentionally excludes the separate cervicovaginal-junction root. Per-node concept IDs retain distinct structures even when the source ontology label is missing or names generic tissue.

Original official GLBs, metadata JSON, graph JSON and crosswalk CSV are preserved. `release-inventory.json` records the official latest endpoint resolutions and old GitHub inventory. `source-hashes.json` pins input bytes. `validation.json` records independent checks. `*.gltf.json` files are readable GLB JSON headers extracted without modifying the original files. `uterus-v1.1-metadata.json` is historical comparison evidence and is not the selected organ version.

Original sex, provenance, placement objects, global female-body target, citations, licenses and file hashes are carried in `female-pelvis.json`. Explicit donor IDs were not supplied. Graph object-placement rotations refer to HRA placement processing; the candidate already uses native glTF metre/Y-up coordinates, so it does **not** reapply those rotations or recenter organs independently.

Regenerate from the pinned original files:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec --python scripts/export-female-pelvis-candidate.py -- --render
```

Review images: `female-pelvis-front.png`, `female-pelvis-oblique.png`, `female-pelvis-organs-close.png`. Attribution and all selected source citations are in `ATTRIBUTION.md`; detailed review is `docs/model/female-pelvis-source-review.md`.

No app, registry, shared anatomy sources, graph, coverage or male model changes are part of this candidate.
