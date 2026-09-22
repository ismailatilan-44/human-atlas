# Base-system classification review — 2026-09-22

**14 new, clear display-system correction candidates remain. No new bone-class candidate remains after the active skull corrections.** Another **12 pharyngeal muscles** have a respiratory contextual grouping and are kept out of automatic recommendations.

This review scanned all **2,234 base parts** at commit `87e9280e5274b416eec58d82193c383e0a8f2fa1`. It executed the real `prepareAtlas` adapter rather than inspecting only raw manifest systems. The four skull-bone and two subscapularis corrections are recognized as **already done**. Nothing was written outside this candidate folder; no app, geometry, source manifest, graph, coverage or labels changed.

## Evidence and scope

The [official BodyParts3D catalog](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html) publishes the [IS-A relation table](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_inclusion_relation_list.txt), organ-name table and [concept-to-element table](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_element_parts.txt). Fresh snapshots and hashes are retained in this folder. [Official table documentation](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/data-4.html) identifies its parent/child columns.

The evaluated roots are **the exact names in that source**, not invented synonyms:

| Source root | Root name | Matching base parts |
|---|---|---:|
| `FMA5018` | bone organ | 203 |
| `FMA5022` | muscle organ | 323 |
| `FMA10474` | zone of muscle organ | 38 |
| `FMA85453` | head of muscle organ | 42 |

This snapshot does not expose a separate root literally named “skeletal muscle” in the downloaded name list. `FMA5022` reaches named regional muscle organs through head, neck, limb, vertebral-column and trunk classes. The two additional muscle roots ensure named muscle heads/zones are not missed. No keyword-only inference from “muscle” is used. No cardiac-muscle or smooth-muscle structure is reclassified merely because its name contains that word.

The four roots match **606 unique parts**: 574 already aligned, 6 already corrected, 14 new clear correction candidates, 12 contextual-policy cases. **1,628 parts fall outside these checked type roots** and receive no correctness judgment. “All parts scanned” does not mean every system assignment has been anatomically validated.

Every candidate and manual case has both an official IS-A path and an **exact leaf FMA → FJ element mapping**. Full named paths and original line numbers are in [source-paths.md](source-paths.md); the same evidence is machine-readable in [proposals.json](proposals.json). [all-parts-audit.json](all-parts-audit.json) records the outcome for all 2,234 parts.

## New clear corrections — 14 parts

These are named limb/shoulder muscle organs currently displayed in `skeletal` or `connective`, matching the type of issue addressed by the already accepted subscapularis override. The proposed presentation class is `muscular`; geometry, FJ/FMA identity and source relations stay unchanged.

| FJ ID | FMA ID | Source name | Raw → active system | Proposal |
|---|---|---|---|---|
| `FJ1409` | `FMA22554` | Right fibularis brevis | `skeletal` → `skeletal` | `muscular` |
| `FJ1409M` | `FMA22555` | Left fibularis brevis | `skeletal` → `skeletal` | `muscular` |
| `FJ1410` | `FMA22552` | Right fibularis longus | `skeletal` → `skeletal` | `muscular` |
| `FJ1410M` | `FMA22553` | Left fibularis longus | `skeletal` → `skeletal` | `muscular` |
| `FJ1411` | `FMA22550` | Right fibularis tertius | `skeletal` → `skeletal` | `muscular` |
| `FJ1411M` | `FMA22551` | Left fibularis tertius | `skeletal` → `skeletal` | `muscular` |
| `FJ1438` | `FMA22425` | Right tensor fasciae latae | `connective` → `connective` | `muscular` |
| `FJ1438M` | `FMA22426` | Left tensor fasciae latae | `connective` → `connective` | `muscular` |
| `FJ1439` | `FMA22544` | Right tibialis anterior | `skeletal` → `skeletal` | `muscular` |
| `FJ1439M` | `FMA22545` | Left tibialis anterior | `skeletal` → `skeletal` | `muscular` |
| `FJ1440` | `FMA65018` | Right tibialis posterior | `skeletal` → `skeletal` | `muscular` |
| `FJ1440M` | `FMA65019` | Left tibialis posterior | `skeletal` → `skeletal` | `muscular` |
| `FJ1532` | `FMA32540` | Right levator scapulae | `skeletal` → `skeletal` | `muscular` |
| `FJ1532M` | `FMA32541` | Left levator scapulae | `skeletal` → `skeletal` | `muscular` |

The pairwise groups are fibularis brevis/longus/tertius (6), tensor fasciae latae (2), tibialis anterior/posterior (4), and levator scapulae (2). The JSON `safeDisplayOverrideProposal` is an explicit 14-ID candidate map; it is **not applied automatically** by this review.

## Manual policy review — 12 parts, no automatic override

All 12 are unambiguously muscle organs in the source IS-A table, but their current primary UI class is `respiratory`. The difference could reflect a pharyngeal/organ-context grouping rather than confusion with bone or fascia. IS-A tissue/organ type is not an exclusive physiological-system-membership assertion. The source type is not uncertain; the desired **primary presentation policy** is. Preserve `respiratory` pending that policy decision, or support muscle as a secondary layer/tag. If a future policy explicitly puts every skeletal muscle under `muscular`, review these together rather than silently applying a rule in this audit.

| FJ ID | FMA ID | Source name | Raw → active system | Proposal |
|---|---|---|---|---|
| `FJ2740` | `FMA46636` | Left inferior pharyngeal constrictor | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2742` | `FMA46633` | Right middle pharyngeal constrictor | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2743` | `FMA46672` | Left palatopharyngeus | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2745` | `FMA46670` | Left salpingopharyngeus | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2746` | `FMA46668` | Left stylopharyngeus | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2747` | `FMA46632` | Left superior pharyngeal constrictor | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2752` | `FMA46635` | Right inferior pharyngeal constrictor | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2754` | `FMA46634` | Left middle pharyngeal constrictor | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2755` | `FMA46671` | Right palatopharyngeus | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2757` | `FMA46669` | Right salpingopharyngeus | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2758` | `FMA46667` | Right stylopharyngeus | `respiratory` → `respiratory` | Manual policy review; no automatic override |
| `FJ2759` | `FMA46631` | Right superior pharyngeal constrictor | `respiratory` → `respiratory` | Manual policy review; no automatic override |

No actual respiratory membership is asserted merely from their source names here; the current application class is observed, and organ-context intent remains to be confirmed.

## Already corrected — 6, excluded from new candidates

| FJ ID | FMA ID | Source name | Raw → active system | Proposal |
|---|---|---|---|---|
| `FJ1504` | `FMA13414` | Right subscapularis | `skeletal` → `muscular` | `muscular` |
| `FJ1504M` | `FMA13415` | Left subscapularis | `skeletal` → `muscular` | `muscular` |
| `FJ3263` | `FMA54738` | Left inferior nasal concha | `respiratory` → `skeletal` | `skeletal` |
| `FJ3265` | `FMA53646` | Left lacrimal bone | `sensory` → `skeletal` | `skeletal` |
| `FJ3369` | `FMA54737` | Right inferior nasal concha | `respiratory` → `skeletal` | `skeletal` |
| `FJ3371` | `FMA53645` | Right lacrimal bone | `sensory` → `skeletal` | `skeletal` |

All 203 source bone-organ surfaces now have active `skeletal`. The active adapter's five older nervous-system corrections are also captured in the audit summary but lie outside these bone/muscle type rules and are not counted as new work. Muscle zones (38) and heads (42) already use `muscular`.

## Minimal implementation proposal

If accepted, append only the 14 explicit FJ IDs to the existing reviewed muscular-display overrides. Do not overwrite `public/models/atlas.json`, replace FMA identities, rewrite IS-A/PART-OF semantics or mass-convert every muscle-class descendant. Confirm that these 14 active classes become `muscular`, the previously corrected 6 remain correct, and the 12 manual cases remain unchanged until separately decided. No geometry regeneration or mesh test is required for the metadata-only change.

This is metadata/type evidence, not a visual mesh, physiological completeness, or expert anatomical validation.

## Reproduction

```sh
node data/model-candidates/system-classification-review/snapshot-active.mjs
python3 data/model-candidates/system-classification-review/review.py
```

Both commands write only inside this candidate directory. The Python review refuses to combine a stale active snapshot with a changed source manifest or adapter. New source downloads should update `source-fetch.json`; preserved hashes identify this review even if the official `LATEST` endpoint later changes.

- Base manifest SHA-256: `c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee`
- Active adapter SHA-256: `b67ba5600ba6d3d33909f3dc6f50b9d6670d92c6584cc5f90aba6d36dcebb30d`
- IS-A relation SHA-256: `26e7d818e03a8c909fe09c561f38d0d513423c87681f9450a803bc38f5b07564`
- Element mapping SHA-256: `a3de74423f943b0d724ae8f59b3a817f87c423a544f8db98113b1980817cbeaf`
