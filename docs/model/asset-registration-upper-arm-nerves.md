# Z-Anatomy upper-arm nerve registration — 2026-09-22

Two source musculocutaneous nerve curves are registered to the existing Human Atlas coordinates and exported as a separate extension. This is a measured geometric registration, with anatomical expert review still pending. The main atlas and anatomy knowledge files are unchanged by this export.

## Package and loading

- `public/models/extensions/upper-arm-nerves.json`: same `parts`, `chunks`, `concepts` layout as `atlas.json`.
- `upper-arm-nerves.bin`: 60,912 bytes; `.bin.gz`: 34,652 bytes.
- 2 parts, 1,464 vertices, 2,880 triangles; IDs `ZA-MCN-L` and `ZA-MCN-R`; concept IDs `atlas:left-musculocutaneous-nerve` / `atlas:right-musculocutaneous-nerve`.
- Little-endian Float32 XYZ positions, Int16 normalized XYZ normals, Uint32 triangle indices. Byte offsets align to 4. Bounds are computed from the final Float32 vertices.
- Chunk URLs are absolute under `/models/extensions/`. If concatenating manifests, remap extension-local chunk indexes to the merged chunk list. No further coordinate transform is needed in the viewer.
- `ATTRIBUTION.md` and `UPSTREAM-LICENSE.txt` travel with this package. The package remains separate from the main BodyParts3D CC BY 4.0 asset attribution.

## Registration evidence

Source `Startup.blend` SHA-256 `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`; Blender 5.2.0 LTS with `--disable-autoexec`. The scene declares METRIC, scale length 1.0. Source X is anatomical left, Y posterior, Z superior; target X left, Y superior, Z anterior, both meters.

Axis conversion alone left mean-sized discrepancies of 3.8–15.0 mm RMS across the twelve reference meshes. Six bilateral bone meshes (humerus, radius, scapula) were then fitted by labeled bidirectional nearest-surface similarity ICP. Correspondences never cross anatomical identities. Each direction uses up to 800 evenly spaced vertex indexes per part per iteration. A proper-rotation SVD fit estimates one shared scale, rotation and translation, without warping either side. Six muscle meshes are held out from fitting. Final statistics use all mesh vertices against the opposite triangulated surface in both directions; they are vertex-weighted, not area-weighted. The axis-only baseline uses source vertices against the target surface, so it demonstrates initial discrepancy but is not the same symmetric statistic.

The fit stopped at iteration 56 with coefficient-change sum 7.58e-08 (threshold 1e-7). Uniform scale: **0.9671866615**. Full 4×4 column-vector matrix is in the manifest. Approximately `(x,y,z) → (0.96719x, 0.96719z + 0.05553, -0.96719y + 0.00182)`, with a small additional measured rotation and X offset. Common BP3D origin did not imply identical coordinates.

| Source object | Use | Axis-only RMS mm | Registered RMS mm | Registered p95 mm | Max mm |
|---|---|---:|---:|---:|---:|
| Long head of biceps brachii.l | holdout | 4.964 | 0.975 | 1.805 | 5.632 |
| Short head of biceps brachii.l | holdout | 4.666 | 1.028 | 1.709 | 7.942 |
| Coracobrachialis muscle.l | holdout | 3.845 | 2.259 | 5.848 | 6.606 |
| Scapula.l | fit | 6.760 | 1.845 | 4.249 | 7.608 |
| Radius.l | fit | 14.974 | 0.644 | 1.207 | 1.893 |
| Humerus.l | fit | 8.631 | 0.636 | 1.159 | 1.785 |
| Long head of biceps brachii.r | holdout | 4.964 | 0.929 | 1.717 | 5.675 |
| Short head of biceps brachii.r | holdout | 4.662 | 0.993 | 1.659 | 8.026 |
| Coracobrachialis muscle.r | holdout | 3.845 | 2.267 | 5.874 | 6.615 |
| Scapula.r | fit | 6.760 | 1.846 | 4.306 | 7.663 |
| Radius.r | fit | 14.963 | 0.608 | 1.026 | 4.037 |
| Humerus.r | fit | 8.637 | 0.615 | 1.083 | 1.705 |

Humerus/radius RMS is 0.61–0.64 mm. Independent biceps RMS is 0.93–1.03 mm. Scapula and coracobrachialis retain larger shape differences (RMS 1.85 and 2.26–2.27 mm, local maxima up to 8.03 mm across references). The sources differ and the atlas is simplified; geometry equality is not asserted. These numbers establish coordinate registration, not nerve-path anatomical accuracy or a clinical error bound. A local deformable fit was deliberately not invented to erase genuine source differences.

## Curve conversion and checks

The original one-spline, six-control-point tubes retain their existing bevel radius/settings. Blender converts each into 732 vertices and 1,440 triangles. No decimation, centerline redraw or anatomical path edit is applied. The left source object has a negative world determinant; its triangle winding is reversed before area-weighted normals are recomputed. Normals are then quantized to signed 16-bit. Open source tube ends remain open (`use_fill_caps=false`).

Verified finite positions, nondegenerate triangles, index range, exact Float32 bounds, gzip round trip, consistent face/vertex normal orientation and normalized normals (maximum quantization length error below 0.000022). Binary SHA-256: `626c2958827eeb9bf1e778c39b5d8c4357fd19ff37decc5d4a1702cd08fcb909`.

Front and oblique Blender renders were inspected with the actual atlas bone/muscle chunks and exported nerve binary. Both tubes are continuous, bilaterally placed along the upper arm and terminate near the elbow; there is no gross axis/laterality/scale error visible. Transparent context makes the source path inspectable. This is technical visual QA, not expert anatomical validation.

- `work/open-assets-review/registered-nerves-front.png`
- `work/open-assets-review/registered-nerves-oblique.png`

## Reproduction and provenance limits

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend --python scripts/export-upper-arm-nerves.py
```

The exporter verifies the source blend hash, reads existing curated reference bindings, refits the registration, writes the isolated package and a work report. It never saves the source `.blend` or alters the main atlas.

[Upstream License.txt](https://github.com/Z-Anatomy/Models-of-human-anatomy/blob/master/License.txt) generally declares CC BY-SA 4.0 and separately lists noncommercial inner-ear/kidney references or adaptations. Only the two named nerve curves are selected; no inner-ear/kidney objects are included. Object-specific source/author lineage is not provided upstream. The package preserves upstream attribution and those limitations instead of claiming commercial clearance of the entire archive.
