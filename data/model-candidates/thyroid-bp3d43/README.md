# Official BodyParts3D 4.3 thyroid source snapshot

Retrieved 2026-09-22 from DBCLS `https://lifesciencedb.jp/bp3d/`. These are original source files, not scraped viewer geometry. License: CC BY-SA 2.1 Japan as stated on the live source's `info_en/license/index.html`; see the captured HTML and `public/models/extensions/THYROID-BP3D43-ATTRIBUTION.md`.

- `thyroid-bp3d43-source.zip`: three original OBJ objects, with source IDs, FMA labels, dimensions and volume estimates in their headers.
- `thyroid-bp3d43-references.zip`: nine original nearby same-ID reference OBJs, used only to validate the existing atlas frame.
- `bp3d-v43-mapping.zip`: official FMA2Obj.txt declaring Data Version 4.3, Objects set 4.3, Tree version FMA3.0.
- `bp3d-live-license.html`: captured live license page.

The source is deliberately separate from Z-Anatomy `thyroid.*`; no active registry was changed.

Re-fetching the source uses a normal public download endpoint. First GET `https://lifesciencedb.jp/bp3d/?lng=en` into a temporary curl cookie jar, then POST form fields to `https://lifesciencedb.jp/bp3d/download.cgi` with that jar and the viewer URL as Referer:

```text
ids=["FJ3670","FJ3671","FJ3672"]
rep_id=["BP21406","BP21433","BP19828"]
filename=thyroid-bp3d43-source
type=art_file
all_downloads=1
```

The original request used BP19819 for the third rep_id based on a third-party inventory; the official response correctly returned BP19828 and FMA13368. All final identities were taken from the official response and official FMA2Obj mapping, not from that inventory. A future re-fetch should use the corrected BP19828. Server-generated ZIP timestamps can change the archive hash; archived member bytes are the reproducibility baseline.

Reference request IDs/representation IDs, in matching order:

```text
FJ3201 BP22977
FJ2808 BP22917
FJ2440 BP22903
FJ2541 BP21463
FJ3161 BP23693
FJ3164 BP23757
FJ3167 BP23524
FJ3170 BP23576
FJ3172 BP23626
```

Regenerate the independent candidate and review renders:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec --python scripts/export-thyroid-bp3d43.py -- --render
```

The exporter pins the source ZIP, reference ZIP, official mapping ZIP, license capture and target atlas hashes. It does not run embedded source scripts or modify shared atlas files. Current output checks and anatomy limitations are in `docs/model/asset-registration-thyroid-bp3d43.md`.
