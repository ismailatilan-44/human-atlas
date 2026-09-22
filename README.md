# Human Atlas

An interactive 3D anatomy explorer built with React, Three.js, and shadcn/ui. Take the BodyParts3D adult male reference apart into **2,234 individually selectable meshes**, explore **15 anatomical systems**, and search **3,432 named concepts**.

**[Working model explorer](https://ismailatilan-44.github.io/human-atlas/)**

**[Original upstream demo](https://human-atlas-seven.vercel.app)** — the local model-explorer changes below are not yet published there.

## Model explorer work

This branch adds registered Z-Anatomy musculocutaneous, median and sciatic nerves plus bilateral menisci and cruciate ligaments and BodyParts3D 4.3 thyroid lobes/isthmus and spinal cord tissue and 20 partial brachial-plexus source components plus 18 BodyParts3D 4.3 lung tissue surfaces (2,290 total meshes), six source-derived attachment markers, regional Turkish/English/Latin labels, and source-backed relationship navigation. Selection supports context transparency, hiding, focus and back navigation. A regional coverage panel exposes 65 first-release target groups; it is not a comprehensive anatomy syllabus. Their 83 directly bound concepts have Turkish and English labels; four Latin labels remain intentionally unavailable. A separate skull-bones selection contains 22 existing bone surfaces while preserving the broader original source group. Rotator cuff muscles have 26 sourced attachment/innervation links, with named regions and explicit missing nerve geometry.

Run locally to inspect the work. Read [delivery status](docs/model/2026-09-20-delivery-plan.md), [regional coverage](docs/model/regional-coverage.md), [nerve registration](docs/model/asset-registration-upper-arm-nerves.md), and [attachment markers](docs/model/landmark-registration.md). Two humeral attachment locations remain unresolved; nerve branches, brachial-plexus roots and medial/lateral cords, detailed spinal segments/roots and broader female anatomy remain open. Anatomical expert review is pending. The low-detail Z-Anatomy thyroid candidate is deliberately excluded from the active model registry after visual review.

Lung exploration now retains the original bronchovascular pieces while adding segment tissue to 24 existing lung, lobe and segment selections. Two tissue-only groups let students hide nine surfaces on either side together. Seventeen source relationships connect tissue to its segment and the existing lobe/lung hierarchy. Regional labels total 271 records; this is not a full atlas translation. Source-group scope notes remain visible even when Latin terms are unavailable. Another 26 muscle and nine hepatic tissue surfaces use corrected display layers. See the [lung source review](data/model-candidates/lung-surfaces/REVIEW.md) and [component attribution](public/models/extensions/LUNG-BP3D43-ATTRIBUTION.md). Two legacy source surfaces carry pulmonary IDs but lie at renal level. Reviewed pulmonary/thoracic selections exclude them, while a visible toggle retains raw source membership. Direct selection marks their identity unverified; no renal reassignment or geometry change is made. Right lung is163 reviewed /165 source pieces. See the [source discrepancy review](data/model-candidates/lung-source-outliers/REVIEW.md).

The extensions have separate [arm/median attribution](public/models/extensions/ATTRIBUTION.md), [knee attribution](public/models/extensions/KNEE-ATTRIBUTION.md), and [sciatic attribution](public/models/extensions/SCIATIC-ATTRIBUTION.md), and [BodyParts3D 4.3 thyroid attribution](public/models/extensions/THYROID-BP3D43-ATTRIBUTION.md), and [spinal cord attribution](public/models/extensions/SPINAL-CORD-BP3D43-ATTRIBUTION.md). The [brachial-plexus attribution](public/models/extensions/BRACHIAL-PLEXUS-ATTRIBUTION.md) records its missing roots/cords and regional registration limits. Extension licenses must not be replaced by the base atlas license.

## Separate female pelvis reference

The reference selector opens 27 HRA surfaces covering the uterus, two ovaries and pelvic bones in their original shared female coordinate frame. It loads separately from the male body. Turkish, English and Latin display labels preserve source identifiers; duplicated ovary aliases appear once in search. Switching references clears selection, view history and camera state. This is a regional reference, not a complete female body.

See [source review](docs/model/female-pelvis-source-review.md) and [CC BY 4.0 attribution](public/models/female-pelvis/ATTRIBUTION.md). `python3 scripts/package-female-pelvis.py` reproduces the public package from the pinned candidate without changing geometry.

## Separate inner-ear reference

A second regional reference contains six Z-Anatomy surfaces: two cochleae, two combined vestibular/semicircular surfaces, and their original temporal-bone context. All positions receive one uniform display-axis rotation; no fitting to a different skull is applied. The source does not identify a sex. Inner-ear components retain noncommercial/share-alike terms separately from temporal-bone attribution. See [source review](docs/model/inner-ear-reference-review.md) and [component attribution](public/models/inner-ear-reference/ATTRIBUTION.md).

The source canal labels are not independent surfaces. Internal membranes, sensory cells and detailed cochlear compartments are not modeled. Turkish/English/Latin search and the shared selection controls work independently of the male atlas.

## Explore

- Orbit, zoom, and select structures directly on the body.
- Toggle individual systems or use skeleton and organ presets.
- Move from assembled anatomy to a spaced inventory of every visible piece.
- Search anatomical names and source identifiers.
- Isolate a selected structure and read its details.
- Use compact controls and detail panels on mobile.

## Run locally

Requires Node.js 22.13 or newer. No API keys or accounts are needed.

```sh
npm ci
npm run dev
```

Open http://localhost:3016. To build the static site, run `npm run build`; the output is in `dist/`.

## Validate

```sh
npm run check
node --test scripts/anatomy-knowledge.test.mjs
node scripts/validate-atlas.mjs
node scripts/validate-interactions.mjs
npm run build
```

Validation covers mesh buffers, names and concept membership, nonoverlapping exploded layouts at desktop and mobile aspect ratios, search and inspection contracts, and tap-versus-drag handling. Browser interaction checks have exercised selection, system controls, search, isolation, rotation, and 390×844, 320×568, and 844×390 layouts. Phone controls stay clear of the exploded inventory, and isolated structures fit the space above or beside the detail panel. Physical-device performance and real multitouch hardware have not been tested.

## Anatomy data

The current viewer uses **BodyParts3D 4.0**, an adult male reference anatomy, licensed **CC BY 4.0**. It does not represent every human structure or variation. Individual source meshes are distinct from named concepts, which may group multiple meshes. Descriptions distinguish general system context from individual organ explanations.

Geometry is simplified for browser performance while retaining every source mesh. The packaged model contains 2,288,268 triangles and downloads approximately 33 MB of compressed geometry. Full credits, source links, and adaptation details are in [ATTRIBUTION.md](public/ATTRIBUTION.md).

This is an educational explorer, not a diagnostic or surgical tool.

## How it works

Geometry is merged into batches. Per-structure GPU textures control translation, visibility, and selection, while component geometry supports accurate picking. Exploded layouts pack only the visible pieces. Rendering updates when the scene changes; orbit controls remain responsive without thousands of separate draw calls.

The optional WebMCP tools expose anatomy search and inspection in compatible browsers. The visible interface works without them.

## Rebuilding geometry

The repository includes browser-ready geometry. Rebuilding it is optional: obtain the official BodyParts3D OBJ archive and English metadata tables, prepare the joined concepts and display-system mappings, run `scripts/convert-anatomy.py`, then `node scripts/optimize-anatomy.mjs` and `node scripts/compress-models.mjs`. Simplification uses a 0.2% relative error limit per structure.

## Deploy

GitHub Pages serves the `gh-pages` branch. After committing and pushing source changes to the `fork` remote, run `npm run deploy:pages`. This builds for the repository subpath, commits only static output to a temporary checkout, and pushes without force. The GitHub Pages repository setting must select `gh-pages` at `/`. This avoids requiring OAuth workflow-file permission. To inspect the build locally: `npm run build -- --base=/human-atlas/` then `npx vite preview --base=/human-atlas/`.

Import this repository into Vercel as a Vite project. The included `vercel.json` configures `npm ci`, `npm run build`, and the `dist` output directory. It can also be served by a static host.

## License

Original application code is released under the [MIT License](LICENSE). **The base anatomy data is CC BY 4.0; the Z-Anatomy extension has separate attribution and licensing**; preserve the attribution when redistributing it. Third-party dependencies retain their respective licenses.

Issues and pull requests are welcome. Please include reproduction steps and browser/device details for interaction problems.
