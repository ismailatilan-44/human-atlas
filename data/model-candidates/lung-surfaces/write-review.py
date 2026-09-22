"""Rebuild the source/registration review from retained evidence; no public writes."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
m=json.loads((D/'lung-parenchyma.json').read_text());q=json.loads((D/'geometry-proof.json').read_text());v=json.loads((D/'package-validation.json').read_text())
rows='\n'.join('| '+p['sourceId']+' | '+p['sourceConceptId']+' | '+p['name']+' | '+str(p['indexCount']//3)+' |' for p in m['parts'])
metricrows='\n'.join(f"| {p['partId']} | {p['name']} | {p['rmsMm']:.6f} | {p['p95Mm']:.6f} | {p['maxMm']:.6f} |" for p in q['registration'])
groups='\n'.join('| '+g['id']+' | '+g['name']+' | '+', '.join(x.removeprefix('BP43-') for x in g['elements'])+' |' for g in m['surfaceGroups'])
merges='\n'.join(f"| {p['conceptId']} | {p['before']} | {p['added']} | {p['after']} |" for p in v['mergePreview'])
review=f'''# Actual BP3D 4.3 lung surfaces — source and registration review

## Outcome and scope

The base Atlas lung/lobe concepts contain bronchovascular trees, while the official live BodyParts3D 4.3 source contains **18 real segment-parenchyma OBJ surfaces** absent from that base dataset. The source surfaces form bilateral outer lung outlines and five source lobe groups. They are suitable as an additional exploration reference under the recorded quality limits. No envelope was inferred from the trees; no lung geometry was reconstructed or invented. No Z-Anatomy/HRA fallback was required.

The additive package is `/models/extensions/lung-bp3d43.json`, with matching binary/gzip and separate attribution. This review does not assert app registration, UI acceptance, clinical suitability or anatomical expert approval; those are separate decisions. Its 18 part IDs are `BP43-FJ6595` through `BP43-FJ6612`; canonical source FJ and FMA identities remain in each record.

## Evidence that the base representation is incomplete

`geometry-proof.json` records all actual source part IDs/names in the two base lung and five lobe selections. FMA7309 right lung selects 156 existing parts and FMA7310 left lung 124. Their union is 280 bronchial/vascular surfaces, with no overlap with the 18 source parenchyma FJs. Names were used only to find candidates; the base selection's **actual binary positions and triangles** were rendered in `base-lung-groups-front.png`. The visible structure is a branching tube network without an outer lung envelope. The projection crops a low stray branch at the bottom, so it is not presented as a complete anatomical survey. This finding concerns this base Atlas release, not absence from the wider BP3D project.

The actual candidate source geometry was rendered independently in `candidate-lobes-front.png` and `candidate-lobes-posterior.png`, then with the actual base Atlas ribs/sternum/trachea in `candidate-lobes-oblique.png`. These show lung-shaped outer boundaries, lobe grouping and preserved source segment seams. `candidate-source-with-base-trees.png` shows the original source surface/tree relationship with transparent candidate materials; some branch tips lie outside projected boundaries. Neither the image nor low reference residual establishes perfect containment of all vessels.

## Official source and version identity

Source OBJ: https://lifesciencedb.jp/bp3d/download.cgi (recorded requests and returned ZIP retained).

Official mapping: https://lifesciencedb.jp/bp3d/get-info.cgi?version=4.3&cmd=concept-objfiles-list . Extracted `FMA2Obj.txt` explicitly says **Data Version 4.3, Objects set 4.3, Tree version FMA3.0**. All 18 OBJ headers explicitly say **Compatibility version 4.3 / Build-up logic FMA 3.0 part_of**. The geometry membership pipeline does not use an unpinned live parent-relation CGI. Separately reviewed companion direct-parent evidence, retained in `direct-parent-source-evidence.json`, pins cb_id=5, ci_id=1, md_id=1, mv_id=6, mr_id=1 for official 4.3/FMA3.0. The mapping endpoint itself did not supply a numeric concept-build ID. These two evidence mechanisms remain explicit.

The freshly fetched mapping ZIP differs from the earlier archive container hash, but its extracted mapping payload is byte-identical: SHA-256 `c3d16c891016da13447de2fc3241d05d92e8f9dc460e363233c03f420b935d4f`. `source-fetch.json` records both container and payload evidence.

`bp3d-v43-object-catalog.csv` is a retained discovery catalog. Its downloader assigned the first encountered ancestor FMA to an object; it is **not** the canonical leaf concept. Therefore canonical IDs/names are taken from the actual returned OBJ headers and checked against the official FMA2Obj memberships. Request representation IDs and returned header representation IDs are retained separately; no unverified equality is claimed.

### Exact surface identities

| Source FJ | Header FMA | Original source name | Triangles |
|---|---|---|---:|
{rows}

FJ6595 and FJ6597 have distinct source hashes, coordinates and bounds but the same FMA27368 header. They are two genuine source patches of the apicoposterior parenchyma concept. Therefore there are **17 source segment concepts, not 18 distinct anatomical segments**. These are source parenchyma portions, not an assertion that the full bronchopulmonary segment's bronchi/arteries are included in each new leaf selection.

### Lung/lobe/segment source membership and conflicts

| Existing source concept | Original name | New source surface IDs |
|---|---|---|
{groups}

The five lobe memberships partition all 18 objects exactly once. The two lungs divide them 9/9. Names and concept IDs are retained; the generic source name `middle lobe of lung` is not silently renamed in the raw manifest.

**Three source aggregate inconsistencies are preserved, not repaired:**

- FMA27364 (left lung parenchyma) omits FJ6598, unlike FMA7310 (left lung).
- FMA31242 (left upper-lobe parenchyma) omits FJ6598, unlike FMA7370 (left upper lobe).
- FMA27363 (right lung parenchyma) omits FJ6608/FJ6609, unlike FMA7309 (right lung).

`source-mapping-review.json` and the manifest's `sourceAggregateDiscrepancies` contain exact sets and differences. Those three narrower aggregate concepts are **not exported**. The seven exported lung/lobe memberships and 17 existing segment memberships follow their own `part_of` rows. For every segment, the source row intersected with the 18 candidate objects exactly matches the direct-child parenchyma surface set: apicoposterior FMA7372 contains FJ6595+FJ6597; the remaining 16 parents each contain one surface. `directParentMemberships` records the full check plus independently pinned direct-parent evidence. No mismatch was found. No source ontology edge was rewritten, and no left medial-basal or other missing anatomical segment was invented to complete a textbook scheme.

## Coordinate evidence

No fitted registration or deformation was applied. The package uses the same main Atlas BP3D transform:

```text
source mm: X left, Y posterior, Z superior
atlas m:   X left, Y superior, Z anterior
atlas(x,y,z) = (0.001*x, 0.001*z + 0.0781112, -0.001*y - 0.1)
```

Main Atlas manifest SHA-256 at comparison: `{m['registration']['targetManifestSha256']}`.

Nine independent same-ID thoracic objects were downloaded as source references and compared with actual base binary triangles using bidirectional vertex-to-nearest-triangle distances. None was used to fit a transform. RMS is **0.004294–0.081336 mm**; worst sampled maximum is **0.357069 mm**. These are sampled surface distances, not a proof of exact mesh identity or a continuous Hausdorff bound.

| Same-ID reference | Base name | RMS mm | P95 mm | Max mm |
|---|---|---:|---:|---:|
{metricrows}

The oblique render supports gross alignment with actual thoracic context. It does not certify microscopic anatomy, fissure detail or correspondence to every neighboring organ.

## Geometry, quality and license

The package retains **101,493 raw vertices / 68,205 unique positions / 136,376 triangles**. Binary size is **3,463,404 bytes**, gzip **1,878,677 bytes**. Positions are only transformed and float32-packed; every exported position was checked exactly against that source conversion. Indices remain the source triangles; zero degenerate triangles were omitted. No smoothing, remeshing, decimation or positional welding is applied. Exact-position averaging only generates render normals; diagnostic welding is used solely to count topology defects.

All 18 surfaces have zero boundary edges under exact-position-weld diagnostics. FJ6598 has **four non-manifold edges** and **two used unique positions with zero averaged normals**; those normals receive a finite unit-Y fallback. No raw positions are unused. These local source defects are not repaired or disguised. Other 17 surfaces have zero non-manifold edges under the same diagnostic. Diagnostic signed volumes do not establish valid clinical solid volumes. Individual male morphology and visible source segment seams remain; anatomical expert acceptance is pending.

License evidence was freshly checked against the official live-source page https://lifesciencedb.jp/bp3d/info/license/index.html and retained with SHA-256 `63d46abcf1b112da9f2d587677d0f4edb7d1654a3c9a8a2bfd1c3d080340512e`. This source package uses **CC BY-SA 2.1 Japan**, with credit **BodyParts3D, © 2008 Database Center for Life Science (DBCLS)**. A separately versioned archive's BY4 license was not assumed to relicense these live 4.3 files. `ATTRIBUTION.md` and the public `LUNG-BP3D43-ATTRIBUTION.md` state changes, source identity and limits.

## Additive merge contract and checks

The only allowed existing concept extensions are the 24 IDs in `extendsConceptIds`: two lungs, five lobes and 17 bronchopulmonary segments. The package contains 41 concept records in total, including 17 new parenchyma leaf concepts. Merge by union, retaining all original members; never replace the base lung, lobe or segment member list with the new surfaces. `surfaceGroups` separately exposes source-only surface selection if needed.

| Concept | Original members | Added surfaces | After union |
|---|---:|---:|---:|
{merges}

The two lungs become **298 combined members**, preserving all **280 original bronchovascular surfaces**. New part IDs do not collide with base IDs; the 17 leaf IDs do not collide with existing base concepts. This does not resolve any pre-existing broad/ambiguous source bronchovascular group membership.

`package-validation.json` records passing binary length/hash/gzip, finite positions, unit normals, bounds/index range, exact float32 source conversion, source member hashes and non-destructive membership checks. Binary SHA-256: `{v['packageSha256']}`. The exporter also asserts the five lobe memberships partition all 18 surfaces and that each reference RMS is below 0.1 mm.

Reproduce export and optional real-geometry renders with:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --disable-autoexec --python scripts/export-lung-bp3d43.py -- --render
python3 data/model-candidates/lung-surfaces/validate-package.py
```

The exporter validates retained source hashes and main Atlas identity before executing the candidate geometry pipeline. This package work did not edit the app, registry, coverage, base atlas or shared source metadata and did not commit or deploy.
'''
(D/'REVIEW.md').write_text(review)
images=[('base-lung-groups-front.png','Actual base lung groups contain branching tube geometry, no outer envelope visible. Low branch clipped by framing; not a full anatomical inventory image.'),('candidate-lobes-front.png','Actual source surfaces form bilateral outlines; five source lobe colors, visible segment seams.'),('candidate-lobes-oblique.png','Actual base ribs/sternum/trachea context supports gross alignment without fitted/deformed geometry.'),('candidate-lobes-posterior.png','Posterior source view preserves segment seams; not a claim of fissure completeness.'),('candidate-source-with-base-trees.png','Original tree geometry through transparent source surfaces; do not infer complete vessel containment.')]
(D/'visual-review.json').write_text(json.dumps(dict(method='Human-readable model inspection of actual Blender renders using retained source and base binary geometry; no generated anatomy',expertReview='pending',images=[dict(path=n,sha256=hashlib.sha256((D/n).read_bytes()).hexdigest(),observation=o) for n,o in images]),indent=2)+'\n')
print('Wrote REVIEW.md and visual-review.json')
