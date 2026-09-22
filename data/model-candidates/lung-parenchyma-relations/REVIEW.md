# Lung parenchyma navigation candidate

`module-proposal.json` contains **17 source PART-OF edges**, plus **two project display groups and their two separately qualified selection edges**. Only this candidate directory was written; the lung asset candidate and shared anatomy/app files were read-only.

## Anatomical source edges

For every parenchyma concept, the official live BP3D PARTOF endpoint supplies an explicit path:

`parenchyma → bronchopulmonary segment → lobe → right/left lung`

The first relation is `constitutional_part_of` in the source. The module preserves this subtype in `qualifiers.sourceRelation`, uses `directSourceParent:true`, and maps it to the existing canonical `part_of` predicate. The remaining segment→lobe and lobe→lung relations already exist in `knowledge.json`: **22 distinct existing edges are reused**, not duplicated. All 17 paths reach the five existing lobes and two existing lungs. No direct parenchyma→lobe or parenchyma→lung shortcut falsely implies an immediate anatomical parent.

There are eight left parenchyma concepts represented by nine surfaces, and nine right concepts represented by nine surfaces. The left apicoposterior concept has two source objects. For names without an explicit side, laterality comes from the source lung ancestor. Each evidence record contains the exact URL, response SHA-256, JSON path index, named path nodes, object mapping lines and existing graph edge IDs. Source geometry-set inclusion only corroborates the resulting membership; it does not establish any anatomical parent.

## Version pinning matters

The official `get-version.cgi?lng=en` record identifies BP3D 4.3 as FMA3.0, with `md_id=1`, `mv_id=6`, `mr_id=1`, `ci_id=1`, `cb_id=5`. All selected responses explicitly request those IDs and PARTOF `bul_id=4`. A retained `get-partof.cgi` response confirms `model_version:4.3`, `concept_info:FMA`, `concept_build:3.0`, and `cb_id:5`.

During endpoint discovery, `version=4.3` alone returned a newer concept build, `4.12.0-inference`. Those unpinned responses were rejected and are not relationship evidence. `versions.json`, `source-fetch.json` and `source/*.json` retain the correctly pinned provenance. The versioned `FMA2Obj.txt` header and mapping membership agree with the selected paths.

## Project display groups

- `atlas:left-lung-parenchyma-surfaces`: nine selected left surface parts; parent context `FMA7310`.
- `atlas:right-lung-parenchyma-surfaces`: nine selected right surface parts; parent context `FMA7309`.

Both entities have `kind:display_group`, `representationStatus:project_display_group`, and explicit project-derived provenance. Their edges use the requested semantics: **“project display group of source parenchyma surfaces, not complete organ tissue assertion”**. They are selection groups for hiding/showing the surface layer together; they do not create new FMA concepts, claim complete lung tissue, or alter the whole-lung aggregate. Their manifest membership evidence is kept separately from the 17 anatomical source edges in `evidence.json.projectDisplayGroups`.

## Integration and checks

Register the lung extension before or in the same build as this module: its 17 parenchyma concept IDs and 18 geometry parts are required. The module does not redeclare those source entities. It adds only the two collision-free project groups. Register source ID `extension-lung-bp3d43`, retaining the explicit API URL/locator/hash evidence rather than replacing it with a mesh-only attribution.

Canonical `validateKnowledge` passed after an **in-memory** extension registration and module merge. All 17 full navigation paths resolve, no existing edge is duplicated, laterality is consistent, and each display group contains exactly its nine source parts. `validation.json` records the result. Root owns labels, projection and UI integration. This candidate's ownership is released after handoff; no further shared work is pending here.
