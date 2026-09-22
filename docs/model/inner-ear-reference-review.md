# Independent inner-ear source reference

`data/model-candidates/inner-ear-reference/inner-ear-reference.json` is a separate dataset with `datasetId: inner-ear-reference`. It contains six actual source surfaces: bilateral `Cochlea`, `Vestibule`, and `Temporal bone` objects from the pinned Z-Anatomy blend. It does not register to or change the main atlas.

## Geometry and identity

The binary preserves original Z-Anatomy world positions in meters: X left, Y posterior, Z superior. The manifest records identity world transform, `atlasRegistration:null`, and `compatibleWithMainAtlas:false`. Consumers must honor that coordinate frame; any display rotation must apply uniformly to every object. No independent object repositioning or main-atlas extension merge is valid.

Part and concept IDs are scoped to this dataset. Each part records its exact `sourceObject`, `sourceObjectType`, source world matrix, parent/collections, base and evaluated geometry counts, authored modifiers and source license scope. `chunks[].url` and `gzip` are paths relative to the manifest. All six base cages and rendered surfaces are additionally preserved as OBJ evidence.

`Vestibule.l/.r` are authored combined surfaces with vestibular and semicircular loop geometry. The named anterior/lateral/posterior semicircular-canal objects in this archive are text labels and two-vertex connectors with zero polygon faces. They are recorded in `excludedCanalLabels`, not exported as independent canal surfaces or assigned fabricated segment boundaries. The package includes no membranes, sensory cells, organ of Corti, nerves or additional inner-ear anatomy.

## Source fidelity and license

The blend is SHA-256 pinned. The exporter never reads the main atlas, fits a skull, recenters a mesh or modifies the source file. It evaluates only authored viewport modifiers; it also supplies original base cages. Mirrored winding correction and float32 packing are documented. Source boundary/nonmanifold edges are measured and retained.

The package keeps a noncommercial restriction for the inner-ear component. Attribution to Dundee's CC BY-NC-SA 4.0 component is an explicit archive-level inference, not an object-level certificate. Temporal bones retain their separate Z-Anatomy CC BY-SA 4.0 declaration and BodyParts3D attribution. See the package's `ATTRIBUTION.md` and `UPSTREAM-LICENSE.txt` for the complete notices and [Dundee's primary provenance source](https://www.dundee.ac.uk/tilt/medical-illustration/anatomy-inner-ear).

## Reproduction and review

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python scripts/export-inner-ear-reference.py -- --render
```

The exporter writes only this candidate directory. `geometry-proof.json` records source preservation and topology; `checksums.json` pins output artifacts. QA views use the exact exported surfaces: `source-temporal-context.png`, `bilateral-inner-ear.png`, `left-ear-context.png`, and `right-ear-context.png`. Cochleae are orange, vestibular complexes green, and original temporal bones translucent blue-gray. Transparency makes internal geometry visible; it does not imply a bony opening or new anatomical segmentation. This is illustrative source anatomy with expert review pending, not a clinical segmentation.

All four views were inspected. The bilateral spirals and canal loops remain distinct within the same-source temporal-bone contexts; no main-atlas registration is involved. `visual-review.json` records the observation and the independent binary checks. The package has 57,684 triangles, 1,213,384 raw bytes and 737,161 gzip bytes. Each cochlea has 3,110 vertices / 6,168 triangles; each vestibular complex has 4,316 / 8,580; each temporal bone has 7,051 / 14,094. Cochleae retain 52 boundary edges each and vestibular complexes 64 each; temporal bones are closed. All six surfaces have zero nonmanifold edges and zero degenerate faces. Gzip roundtrip, index bounds, finite positions, laterality and OBJ/binary coordinate agreement passed. No new test suite was added for this isolated data export.

## Separate viewer package

`python3 scripts/package-inner-ear-reference.py` creates `public/models/inner-ear-reference/atlas.json`, `atlas.bin`, and `atlas.bin.gz` with absolute chunk URLs. This script reads the candidate but never modifies it. The display copy applies the same determinant +1 rotation `(x,y,z) → (x,z,−y)` to all six parts and their normals, recomputes bounds and updates dimension ordering. It introduces no translation, scaling, registration or per-object placement.

`appliedDisplayTransform` records the column-vector matrix, scale 1 and zero translation. `sourceCandidate` records manifest, binary and blend hashes. `packaging-proof.json` verifies that inverse rotation exactly recovers every original float32 vertex, quantized normals undergo the same exact permutation, and every triangle index buffer stays unchanged. This establishes a pure rotation preserving all source distances and relative positions. The display gzip is 736,819 bytes. Dataset IDs remain separate; the similar coordinate axis convention does not make this compatible with the main atlas's anatomy.

The public copy retains component-specific license scopes, source archive/object provenance, attribution, upstream license, source-space QA images and technical review. Its attribution explicitly distinguishes raw source coordinates from the uniform display rotation. No app, registry, source registry or coverage files are edited by either script.
