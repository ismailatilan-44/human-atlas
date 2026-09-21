# Upper-arm attachment anchors — 2026-09-22

Six real source attachment surfaces now supply representative reference points for bilateral coracoid, supraglenoid and radial-tuberosity landmarks. The two coracobrachialis humeral insertion targets remain explicitly unresolved. These are separate landmark markers, not new whole-bone geometry bindings or segmented landmark meshes.

## Package

Endpoint: `/models/extensions/upper-arm-landmarks.json`.

- `anchors`: 6 records with `conceptId`, `position:[x,y,z]`, `contextPartIds`, `sourceObject`, `method`, `status`, detailed source/evidence/quality/limitations.
- `unresolved`: 2 humerus-medial-midshaft records, `position:null`, with the reason no coordinate was produced.
- Coordinates already use Human Atlas meters / X left / Y superior / Z anterior. The source hash and registration matrix are copied from the nerve extension; consumers must not reapply the transform.
- `contextPartIds` identifies the supporting bone for camera/context use. It does not assert that the whole bone is the landmark.

## How the points were derived

The source surfaces belong to `2: Muscular insertions` and are parented to the expected side-specific scapula or radius. Each point is the area-weighted centroid of the authored triangle surface, projected back onto that same attachment surface, then transformed by the existing six-bone registration. Surface normals and a bone bounding box were not used to guess an anatomical site. `Solidify` and `Subdivision` display modifiers are recorded but not applied: the authored base attachment patch supplies the location, without artificial display thickness.

The JSON retains the original source-space point, method, source object type/name, triangle count, source bone distance and registered target-bone distance. The exported position is not silently snapped to the target bone. The nearest target-bone point is stored separately for review.

| Target concept | Source attachment surface | Context part | Source bone gap mm | Target atlas bone gap mm |
|---|---|---|---:|---:|
| atlas:left-coracoid-process | Coracobrachialis muscle.ol | FJ3279 | 0.000 | 0.478 |
| atlas:left-supraglenoid-tubercle | Long head of biceps brachii.ol | FJ3279 | 0.000 | 0.335 |
| atlas:left-radial-tuberosity | Biceps brachii muscle.el | FJ3277 | 0.158 | 1.240 |
| atlas:right-coracoid-process | Coracobrachialis muscle.or | FJ3384 | 0.000 | 0.457 |
| atlas:right-supraglenoid-tubercle | Long head of biceps brachii.or | FJ3384 | 0.000 | 0.305 |
| atlas:right-radial-tuberosity | Biceps brachii muscle.er | FJ3349 | 0.158 | 2.194 |

Coracoid anchors use the coracobrachialis origin patch as a representative point for the shared coracoid origin region; they do not delimit the entire coracoid or claim both muscle footprints coincide exactly. Supraglenoid anchors use the long-head biceps origin patch. Radial anchors use the biceps distal insertion patch. Their anatomical identity follows the already curated origin/insertion relationships in `data/anatomy/upper-arm.json`; the source patches add spatial evidence, not a new literature claim.

## Rejected or unresolved source candidates

The source contains named two-vertex label connectors for coracoid process, supraglenoid tubercle and radial tuberosity. Left `.i` connectors and `.s` text objects have identity cached world transforms in a direct headless read. Reconstructing the parent hierarchy locates them near the skeleton, but the left coracoid/supraglenoid connector offsets are not mirrored to the actual left attachment footprint. Neither cached origin coordinates nor a hand-mirrored repair was exported. Dedicated attachment surfaces provide bilateral spatial evidence instead.

`Short head of biceps brachii.ol` is parented to `Scapula.r` and has negative-X coordinates despite its suffix. It was not treated as a left origin. The properly parented bilateral coracobrachialis origin patches were used for the shared coracoid reference.

No dedicated coracobrachialis humeral insertion patch or named medial-midshaft attachment marker was found. Both humeri have only Bone/Cartilage material slots and no vertex groups. Coracobrachialis `.ol/.or` patches attach to scapula and cannot represent humeral insertion. Both `atlas:*‑humerus-medial-midshaft` records remain unresolved; no whole-bone center or guessed distal muscle point fills that gap.

## Verification and limits

The exporter checks source SHA-256, attachment parent/collection, finite coordinates, laterality and bounded distances to the source and target bone surfaces. The six source bone gaps are at most 0.158 mm; atlas gaps are 0.305–2.194 mm. These are proximity measurements, not localization accuracy estimates.

Source and target renders use the actual selected bone/patch meshes and exported anchor coordinates. Gold spheres represent reference points and red surfaces represent source attachment patches. The source render displays registered Z-Anatomy bones; the target render displays existing atlas binary bones. Inspect the paired images:

- [Registered source bones and attachment anchors](../../public/models/extensions/landmark-proof-source.png)
- [Existing atlas bones and the same anchors](../../public/models/extensions/landmark-proof-target.png)

The paired renders were visually inspected: source patches and gold points occupy the corresponding bilateral local attachment regions, and the registered source/target scenes show no gross placement or laterality mismatch. The radial target patches retain the measured 1.24–2.19 mm discrepancy. Expert anatomical review remains pending. No clinical localization claim is made.

## Reproduce

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend --python scripts/export-upper-arm-landmarks.py -- --render
```

Omit `-- --render` to export JSON only. The source blend is never saved. Attribution and upstream mixed-source limitations remain in `public/models/extensions/ATTRIBUTION.md` and `UPSTREAM-LICENSE.txt`; this addition selects attachment patches only and does not relicense the full source archive.
