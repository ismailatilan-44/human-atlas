# Distal leg nerve metadata candidate

Four source objects receive separate candidate concept labels: bilateral tibial nerve and common fibular nerve. `proposal.json` contains four labels and four anatomical `branch_of` relationships to the existing same-side sciatic nerve. It contains no new root, division, muscle-supply or display-group concepts. These metadata do not authorize activation of the geometry; main-atlas registration was rejected after distal placement review.

## Naming and identifiers

The pinned upstream TA2 table, SHA-256 `0f9092a328b27dcd15d696d9f9a4087deb229a1aad21b75876657622de835974`, establishes the exact unsided pairs:

| Source name | TA2 row | CSV line | Latin |
| --- | --- | --- | --- |
| Tibial nerve | 6582 | 6665 | Nervus tibialis |
| Common fibular nerve | 6571 | 6654 | Nervus fibularis communis |

Source `.l`/`.r` suffixes and manifest concept/part pairs retain laterality. The Latin terms remain unsided, with side stored separately; no unattested Latin compound is generated. Turkish labels are editorial and await anatomical review. Common peroneal nerve is a searchable historical synonym supported by the educational table. The labels refer to the nerve concepts; the associated geometry represents only each named source object.

The `atlas:left/right-tibial-nerve` and `atlas:left/right-common-fibular-nerve` primary IDs are retained. The consulted official BodyParts3D English tables did not yield exact tibial/common-fibular nerve names, and no authoritative lateralized FMA mapping was established. FMA cross-references remain null; this does not assert that FMA lacks those concepts.

## Anatomical hierarchy

[TTUHSC's Hip & Posterior Thigh & Leg table](https://anatomy.ttuhscep.edu/musculoskeletal_system/gluteal_tables.html), verified 2026-10-02, identifies tibial and common fibular as sciatic terminal branches. The individual nerve rows identify sciatic as their source. Exact row/column locators accompany each edge.

Use `branch_of` in the direction child nerve → same-side sciatic nerve. This describes a typical anatomical terminal-branch relationship; it is distinct from source collection membership or a generic `part_of` edge. Do not treat the relationship as transitive, infer innervation from it, or interpret it as proof of geometric continuity or a particular specimen's division level. Existing sciatic motor edges qualified by `viaDivision` remain parent-level functional summaries and are not reassigned.

Suggested relationship labels: outgoing “Dalı olduğu sinir”, incoming “Sinirin dalları”. The consuming parser and view must support the explicit predicate before ingestion.

## Observed source extent and limits

The geometry candidate is `public/models/extensions/distal-leg-nerves.json`; parts are `ZA-TIB-L/R` and `ZA-CFIB-L/R`. Each tibial object contains one 10-point Bezier spline; each common fibular object contains one 8-point Bezier spline. `source-evidence.json` records exact source-world and transformed endpoints, source IDs, hashes, and manifest locators.

With the existing sciatic transform, all proximal endpoints are near atlas Y=0.560 m. Tibial endpoints extend to approximately Y=0.069 m; common fibular endpoints to Y=0.402 m. These coordinates describe source extent only, without asserting a named terminal anatomical landmark. Endpoint coincidence with the sciatic source is a numerical source-model observation, not an anatomical error bound or proof of a fused surface.

Separate deep/superficial fibular, plantar, sural and muscular/digital branch objects are excluded. This candidate does not establish a complete lower-limb nerve network. The final [geometry review](../../../docs/model/asset-registration-distal-leg-nerves.md) rejects main-atlas placement and preserves a separate 14-object matched-source candidate. Metadata validity cannot resolve that spatial concern. The label proposal remains explicitly inactive for male-body integration. A separate-reference release would need dataset-scoped labels and a decision for sciatic relationships: sciatic parent geometry is not included in that reference.

The same pinned Z-Anatomy source as the existing sciatic package is used. Preserve its separate CC BY-SA attribution, underlying BodyParts3D notices, and object-specific provenance limitation; do not replace them with the base atlas license. Geometry export and attribution are owned by the geometry record.

## Review and validation

Candidate validation checks four unique leaf IDs, four same-side `branch_of` edges, verified TA2 pairs, one-to-one manifest part binding and exact recorded source extent. After the final geometry decision, input hashes and the four nerve bindings in the independent reference were checked again; six input hashes now pin the evidence. Application and full-atlas checks belong to integration and are not claimed by this candidate record.

Expert review remains pending for Turkish terminology and anatomical scope. Exact FMA cross-references remain unresolved; main-atlas placement is rejected and source-reference acceptance remains pending. No additional muscle supply, root level, cutaneous territory, or endpoint anatomy is inferred.
