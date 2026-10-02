# Intrinsic-foot muscles and sesamoids — source audit and candidate v1

This bounded task adds **32 source objects: 30 intrinsic-foot muscle objects and two compound sesamoid groups**, while preserving the previous 87-object reference. The combined **119-object candidate** is ready for same-source reference integration. Source geometry, compound identity and technical acceptance are recorded; no anatomical expert acceptance, whole-foot completeness or main-body registration is claimed.

Audit baseline: `9e649b6bef0e589a6caa8b7391e10a132a304cea` on `codex/publish-model-explorer`, 2 October 2026. Public integration, labels, relationships, targets and deployment remain the root task's responsibility. This task writes only this candidate directory.

## Source and intake

Actual input: `work/open-assets-review/Startup.blend`, SHA-256 `9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd`, from [Z-Anatomy/Models-of-human-anatomy](https://github.com/Z-Anatomy/Models-of-human-anatomy), `Z-Anatomy/Startup.blend` archive member. Acquisition was 8 September 2026 under the existing [source intake](../../../docs/model/2026-09-08-open-assets-review.md); no new download or upstream-version verification was performed. That intake identifies a male reference; donor-specific information remains unavailable.

Blender 5.2.0 LTS read the pinned file with `--disable-autoexec`, skipped its embedded script and did not save it. The existing unrelated oesophagus/profile dependency-cycle warning recurred without preventing this audit. Source names and collection membership were searched; text/group/marker companions remain distinguishable in `discovery.json`. All exported identities were then checked as real evaluated MESH geometry. A collection name alone did not establish an anatomical surface or verified relationship.

General Z-Anatomy CC BY-SA 4.0 / Gauthier Kervyn attribution and underlying BodyParts3D–DBCLS CC BY-SA 2.1 Japan / Kousaku Okubo notices remain separate in `ATTRIBUTION.md` and the verbatim `UPSTREAM-LICENSE.txt`. Upstream inner-ear/kidney exceptions remain in the notices; those components are not imported here. Object-specific authorship lineage remains unresolved. Private source inspection, derivative export, product inclusion and anatomical acceptance are distinct statuses; this task does not assert new blanket commercial/redistribution clearance.

## Exact selected source scope

Each row below has separate `.l` and `.r` source objects; counts are **per side**. Full exact part/concept/source mappings, systems and roles are in `new-object-mapping.json`. Muscle IDs use `ZA-LLR-{SOURCE-SLUG}-L/R` with `zanatomy:{source-slug}-l/r` concepts, system `muscular`, role `primary`. The sesamoid objects use the same source-preserving pattern, system `skeletal`, role `context`.

| Source base name | Vertices / triangles | Source selection scope |
| --- | ---: | --- |
| (Opponens digiti minimi muscle of foot) | 120 / 236 | Parenthesized source identity; variation/identity expert review pending |
| Abductor digiti minimi of foot | 640 / 1,280 | One named object |
| Abductor hallucis | 844 / 1,688 | One named object; tiny extra defect component retained |
| Dorsal interossei muscles of foot | 975 / 1,946 | Four connected components in one source group; no numbered identities assigned |
| Extensor digitorum brevis | 1,596 / 3,184 | Three connected components in one named object; no inferred heads |
| Extensor hallucis brevis | 561 / 1,118 | One named object |
| Flexor digiti minimi of foot | 230 / 464 | Exact source wording retained |
| Flexor digitorum brevis | 1,610 / 3,224 | One named object |
| Lateral head of flexor hallucis brevis | 481 / 966 | Separate head explicitly named by source |
| Lumbrical muscles of foot | 207 / 418 | Plural source object but one connected component; four separately selectable muscles not demonstrated |
| Medial head of flexor hallucis brevis | 259 / 514 | Separate head explicitly named by source |
| Oblique head of adductor hallucis | 454 / 904 | Separate head explicitly named by source |
| Plantar interossei muscles | 627 / 1,242 | Three connected components in one group; no numbered identities assigned |
| Quadratus plantae muscle | 590 / 1,176 | One named object; no inferred head split |
| Sesamoid bones of foot | 149 / 290 | Two connected components selected together; no medial/lateral identity assigned |
| Transverse head of adductor hallucis | 181 / 366 | Separate head explicitly named by source |

Each side was corroborated by evaluated world-coordinate X sign. Source datablocks, parent, materials, transforms, modifiers, source bounds, component counts and geometry hashes are preserved in the audit/package. The source object types and actual evaluated vertices/triangles establish selectable geometry; source names do not by themselves establish expert identity acceptance.

All objects preserve the existing source frame: original coordinates in meters, X left / Y posterior / Z superior, with the single shared display rotation `(x,y,z) → (x,z,-y)`. There is no scale change, fitting, translation, local deformation, decimation or object-specific movement. The baseline's `compatibleWithMainAtlas:false` and null registration remain. Render-panel offsets exist only in the temporary QA scene.

## Candidate artifacts and validation

`atlas.json`, `anatomy.bin`, `anatomy.bin.gz` form the combined candidate. `baseline87-atlas.json` and `baseline87.bin.gz` pin the previous reference independently of later public changes. All 87 original part/concept records are identical; its **entire 2,643,600-byte binary prefix** is retained. Thus every original position, normal, index array and offset remains unchanged. New geometry appends after that prefix.

| Property | Verified result |
| --- | --- |
| New objects / vertices / triangles | 32 / 19,048 / 38,032 |
| Combined objects / vertices / triangles | 119 / 82,330 / 163,404 |
| Combined binary / gzip bytes | 3,442,880 / 1,931,012 |
| Binary SHA-256 | `038387150768d7c34670bdce332ad4870dc15fbcbb622c0e441ab064cc979350` |
| Gzip SHA-256 | `2a1637fe928cd6cbc93f2804daf27a4c73dee3e45379e519c0e6b9872d225af1` |
| Manifest SHA-256 | `d746e77f27af6b92153dc05930b6af7fde7612c9732ad4ad2c4ce76432d5a4f8` |

Checks passed: pinned source/baseline hashes, exact evaluated source geometry hashes, source side, finite decoded positions, bounds, index ranges, four-byte alignment, decoded Float32 equality to rotated source values, exact decoded source triangles, normalized quantized Int16 normals, nonzero triangle areas, gzip roundtrip and baseline preservation. A render-producing default run and a subsequent numerical `--output` run reproduced **all five package files byte-for-byte**, including attribution/notices. Both scripts passed syntax parsing. See `geometry-checks.json` and `acceptance-evidence.json`.

Source defects are retained explicitly. All 32 additions have zero loose vertices, zero boundary edges, zero zero-area triangles and zero nonmanifold edges under the recorded edge tests. These tests do not establish watertightness or absence of self-intersections. Across 22 muscle objects, **80 triangles** have nonpositive averaged vertex-normal agreement. The worst count per object is ten triangles in each lateral flexor hallucis brevis head. Each abductor hallucis includes a separate three-vertex component consisting of opposing coincident triangles; its three cancelling vertex normals receive a disclosed largest-incident-face normal fallback. No source faces are removed or filled. The sesamoid objects have no normal disagreement/fallback defect. Previous reference defects remain unchanged. Technical D1 source-reference presentation is supported with these limits; fine fascicles, attachment footprints, clinical accuracy and expert anatomy acceptance are not established.

## Opened visual evidence

Four final source/decoded renders were opened and inspected: `source-decoded-plantar-all.png`, `source-decoded-plantar-deep.png`, `source-decoded-dorsal.png`, `source-decoded-sesamoids.png`. Source is left in plantar views and right in the dorsal view because the camera direction reverses. Both panels use matching scale/direction. The source panel uses the actual evaluated new arrays; the decoded panel reads package positions, indices and quantized normals. Bone context uses the previously verified source-frame reference.

No gross source/output course, shape, side, scale or missing-object mismatch was observed. Deep-layer visibility was inspected with superficial muscles hidden; dorsal extensor/interosseous and sesamoid/FHB context were separately shown. Compound selections and coarse source surface detail remain visible. These are technical preservation checks, not a muscle attachment/innervation or anatomical expert review. Browser search → selection → focus/context → relationship → return and deployment acceptance are still integration work.

## Other foot/ankle supports: inventory only

The bounded scan identified **124 evaluated support objects**, including six ankle ligament objects already represented in reference87; 118 have no representation in that specific reference. It searched named ligament, retinaculum, aponeurosis, articular-capsule and tendon-sheath objects whose source bounds lie below 0.30 m superior. This is not a whole-foot syllabus or absence audit of other datasets. `evaluated-candidates.json` records all exact names, matrices, modifiers, bounds, topology and current-reference membership.

Examples per side: `Flexor retinaculum of ankle` (350 vertices / 696 triangles), `Superior extensor retinaculum of ankle` (132 / 260), `Inferior extensor retinaculum of ankle` (160 / 316), `Superior fibular retinaculum` (328 / 652), `Intersesamoid ligament` (30 / 56) and `Long plantar ligament` (1,741 / 3,486). Coarse source surfaces are explicit: plantar aponeurosis has 72 boundary edges; inferior fibular retinaculum has 27. Sixteen support objects start from one source polygon, and each `Dorsal tarsometatarsal ligaments.l/.r` object has four nonmanifold edges. None is included in this 32-object addition. No ligament fascicles, layers or attachments were inferred from source names or proximity.

## Reproduction and integration handoff

Default commands write only this directory:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python data/model-candidates/foot-soft-tissue-source-audit-v1/inspect.py

/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec \
  work/open-assets-review/Startup.blend \
  --python data/model-candidates/foot-soft-tissue-source-audit-v1/export.py -- --render
```

`export.py` also exposes **`build_candidate(output_dir=None, render=False)`**. Importing it with a non-`__main__` module name performs no export. Both baseline inputs are pinned inside this directory, so reproduction does not depend on a mutable public count of 87. The integration owner may call the function with its chosen package directory, or pass `--output PATH`; this writes the three package files plus the reviewed attribution/notices there, while checks/render evidence remain here. The alternate-output behavior was tested only in an owned temporary subdirectory. No public-write option was executed by this task.

Measured wall time from first Blender discovery to verified candidate/reproduction was **853.27 seconds** (about 14.2 minutes), excluding initial instruction reading and final handoff prose; details in `timing.json`. One exporter attempt stopped on a duplicate report-key programming error before writing geometry; it was corrected. No geometry repair or failed source object was substituted. No Git mutations, public edits, app changes or deployment were performed.

Next integration action: use the callable exporter for the 119-object reference, merge the separately reviewed dataset-scoped metadata, and exercise the full muscle/sesamoid product journey. A later bounded support package should inspect the named retinacula and plantar support sheets at their actual source detail rather than declaring the support inventory complete.
