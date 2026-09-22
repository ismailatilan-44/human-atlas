# Concept-selection review — 2026-09-22

**Finding: the 43-piece `FMA46565 / skull` selection is inherited from the official BodyParts3D 4.0 PART-OF compound mapping. It is not a group expansion introduced by the checked-in converter or viewer.** All 43 IDs match the official source **in the same order**. The original source group is too broad for the intended “skull bones” selection: 22 skull bone surfaces + 19 ocular/lacrimal surfaces + 2 hyoid surfaces.

No application, source manifest, graph, labels, coverage or geometry was modified. This is an ID, name, relation and code-path review; no image or anatomical surface correctness approval is claimed.

## Official source evidence

- [BodyParts3D download catalog](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html) explicitly describes element-parts tables as definitions of compound organs and publishes IS-A and PART-OF variants.
- [PART-OF compound elements](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_element_parts.txt), saved as `partof_element_parts.txt`, lines **10845–10887**, lists precisely the current 43 `FMA46565` elements.
- [PART-OF inclusion relations](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_inclusion_relation_list.txt) connect skull → viscerocranium → left/right orbit → ocular/lacrimal structures; skull → viscerocranium → hyoid bone is another explicit source path. Individual shortest paths are retained in the proposal JSON.
- [IS-A inclusion relations](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_inclusion_relation_list.txt) establish the proposed parts' source concepts as descendants of `FMA5018 / bone organ`. Source skull ∩ bone-organ descendants gives 24 surfaces; excluding the two `FMA52749 / hyoid bone` surfaces gives 22.
- The intended conventional 22-bone scope, including mandible but excluding associated hyoid and ear ossicles, follows [OpenStax, Divisions of the Skeletal System](https://openstax.org/books/anatomy-and-physiology-2e/pages/7-1-divisions-of-the-skeletal-system) and [The Skull](https://openstax.org/books/anatomy-and-physiology/pages/7-2-the-skull).

Fresh source downloads, URLs and SHA-256 values are in `source-fetch.json`. The exact source/base comparison and reviewed code hashes are in `selection-pipeline-evidence.json`. Base manifest SHA-256: `c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee`.

## Importer and selection path

`scripts/convert-anatomy.py` copies each incoming metadata concept's `id`, `name` and `elements` without expanding the list. It reads mesh geometry separately. `scripts/optimize-anatomy.mjs` simplifies geometry and changes binary offsets but retains concept memberships. The historical external CONCEPT_MAP input itself is not present in this repo, so this report does not invent its generation history; equality of the final 43-element list with the official published mapping settles the observed mismatch.

`app/knowledge.ts::explorerConcepts` keeps existing atlas concepts before adding graph-only concepts. `app/coverage-panel.tsx` resolves the target's concept ID, and `app/page.tsx::choose` uses `selected: c.elements`. `app/scene.tsx` honors that set; selected parts can remain visible even if their system layer is hidden. Therefore switching to the skeletal layer does not correct a 43-member selected source group.

Nor should a proposed skull-bones composite be implemented by `system === 'skeletal'`: this would retain both hyoid surfaces while losing the inferior nasal conchae (`respiratory`) and lacrimal bones (`sensory`). Those four bone memberships are established by source IS-A identities, not current UI system buckets.

## Recommended minimal integration (candidate only)

Add a **separate display composite** `atlas:skull-bones` / **Kafatası kemikleri**, referencing the 22 existing FJ IDs below. Keep `FMA46565` and all 43 original source elements unchanged. Label the original group **Kafatası (kaynak grubu)** and show that it also includes eye/lacrimal and hyoid surfaces. Point the skull-bones coverage action to the display composite.

This preserves FMA source semantics, raw provenance and every mesh ID. No geometry import, binary rewrite, inferred source relation or deformation is needed. The source group and display composite will both remain searchable; their distinct names and scope notes are necessary to avoid presenting them as equivalent. Do not add a false FMA equivalence for the new display composite. A regression should assert exactly these 22 IDs, no ocular/hyoid IDs, continued availability of original `FMA46565`, and no accidental filter by system.

The proposed 22 surfaces correspond by source name to 8 cranial and 14 facial bones. This count is a **selection contract**, not a claim that every surface detail, suture or variation has been visually/anatomically validated.

| Existing part ID | Existing source concept ID | Source name | Current UI system |
|---|---|---|---|
| `FJ3199` | `FMA52740` | Ethmoid | skeletal |
| `FJ3200` | `FMA52734` | Frontal bone | skeletal |
| `FJ3263` | `FMA54738` | Left inferior nasal concha | respiratory |
| `FJ3265` | `FMA53646` | Left lacrimal bone | sensory |
| `FJ3269` | `FMA53650` | Left maxilla | skeletal |
| `FJ3272` | `FMA53648` | Left nasal bone | skeletal |
| `FJ3273` | `FMA53656` | Left palatine bone | skeletal |
| `FJ3274` | `FMA52789` | Left parietal bone | skeletal |
| `FJ3281` | `FMA52739` | Left temporal bone | skeletal |
| `FJ3287` | `FMA52893` | Left zygomatic bone | skeletal |
| `FJ3289` | `FMA52748` | Mandible | skeletal |
| `FJ3309` | `FMA52735` | Occipital bone | skeletal |
| `FJ3369` | `FMA54737` | Right inferior nasal concha | respiratory |
| `FJ3371` | `FMA53645` | Right lacrimal bone | sensory |
| `FJ3375` | `FMA53649` | Right maxilla | skeletal |
| `FJ3378` | `FMA53647` | Right nasal bone | skeletal |
| `FJ3379` | `FMA53655` | Right palatine bone | skeletal |
| `FJ3380` | `FMA52788` | Right parietal bone | skeletal |
| `FJ3386` | `FMA52738` | Right temporal bone | skeletal |
| `FJ3392` | `FMA52892` | Right zygomatic bone | skeletal |
| `FJ3394` | `FMA52736` | Sphenoid bone | skeletal |
| `FJ3395` | `FMA9710` | Vomer | skeletal |

Machine-readable integration candidate: `skull-bones-proposal.json` (`elements`, `sourceConceptIds`, per-part source paths and original 43 elements retained).

### Original source members excluded from the new display composite

| Part ID | Source concept ID | Source name |
|---|---|---|
| `FJ1282` | `FMA58082` | Anterior chamber of left eyeball |
| `FJ1285` | `FMA58300` | Left choroid |
| `FJ1286` | `FMA58300` | Left choroid |
| `FJ1289` | `FMA58240` | Left cornea |
| `FJ1297` | `FMA58237` | Left iris |
| `FJ1299` | `FMA59103` | Left lacrimal gland |
| `FJ1305` | `FMA58243` | Left lens |
| `FJ1317` | `FMA58272` | Left sclera |
| `FJ1320` | `FMA58840` | Suspensory ligament of left lens |
| `FJ1331` | `FMA58829` | Left vitreous body |
| `FJ1336` | `FMA58299` | Right choroid |
| `FJ1337` | `FMA58299` | Right choroid |
| `FJ1340` | `FMA58239` | Right cornea |
| `FJ1348` | `FMA58236` | Right iris |
| `FJ1350` | `FMA59102` | Right lacrimal gland |
| `FJ1356` | `FMA58242` | Right lens |
| `FJ1368` | `FMA58271` | Right sclera |
| `FJ1371` | `FMA58839` | Suspensory ligament of right lens |
| `FJ1382` | `FMA58828` | Right vitreous body |
| `FJ2772` | `FMA52749` | Hyoid bone |
| `FJ3201` | `FMA52749` | Hyoid bone |

The two hyoid IDs are two source surface records; this review does not assume they are byte-identical duplicate meshes.

## Bounded scan: first 65 coverage targets

Reviewed exactly **65 target rows** in current stored region/target order, containing **78 bindings**. Of these, **53 bindings refer to base-manifest concepts**, and **all 53 base selections exactly match an official IS-A, PART-OF or union element set**. Current extension additions were kept distinct from this base comparison (for example, spinal cord now adds a separately sourced neural-tissue surface). Separate regional references and zero-geometry landmarks were not conflated with male base geometry.

**No second unequivocal extraneous-structure case comparable to skull was established by this bounded ID/name/source review.** The following broad selections merit explicit scope descriptions, but their internal structures must not be deleted merely because a different organ silhouette might be expected:

| Target | Observed membership | Assessment |
|---|---|---|
| Brain | 59 pieces, including four ventricular cavity surfaces and cerebral aqueduct | Source includes internal cavities; no out-of-brain structure established here. Existing raw system mislabels are a separate metadata issue. |
| Heart | 83 pieces including chambers, valves, papillary muscles and coronary vessels | Internal/coronary context, not a proven foreign organ selection. Whether the selected pieces form a full wall surface is outside this membership review. |
| Lungs | Left 124 and right 156 pieces; source names describe bronchial and segmental vessel trees | Representation-scope warning: the lists alone do not establish lung parenchyma/pleural outer surfaces. This is not an overreach finding; requires its own morphology/scope review if needed. |
| Liver | 60 pieces including hepatic segments, arteries, portal/hepatic veins and biliary branches | Broad intrahepatic/hilar context; do not apply a blanket digestive-system filter or remove vessels without an explicitly different selection contract. |
| Pancreas | 4 surfaces named pancreas, parenchyma, pancreatic duct and duct tree | Source organ/duct grouping, not an established foreign inclusion. |
| Small / large intestine | Both include `FJ2599 / ileocecal junction` | Shared junction is a boundary membership, not sufficient evidence of a grouping error. |

`coverage-first-65-review.json` contains all 65 rows, current selected part names/IDs, source-set comparison results and the limited finding assigned to each. An absence of another obvious name-level issue does **not** certify the groups' anatomical completeness or correctness.

## Reproduction

After the six official TSV snapshots are present:

```sh
python3 data/model-candidates/concept-selection-review/review.py
```

This writes only the candidate JSON evidence beside the script. The downloaded official tables are retained for reproducibility; `LATEST` URL contents may change, so the recorded hashes identify the reviewed snapshot.

## Entegrasyon kaydı

22 Eylül: Kök görev bu adayın incelenen verilerini etkin etiket/bilgi grafiği/görüntüleme katmanına uyguladı. Bu klasörün aday snapshotı korunur; güncel ürün durumu docs/model/2026-09-20-delivery-plan.md içinde izlenir.
