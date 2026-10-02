---
name: anatomy-asset-audit
description: Inspect, compare, and export anatomical Blender, FBX, OBJ, or glTF assets while preserving individual structure identities and spatial context. Use for model-source audits and web asset preparation.
---

# Anatomy asset audit

Start from the source file and its intake record. For unfamiliar `.blend` files, use Blender background Python with automatic script execution disabled unless the specific source scripts have been reviewed. Inspect object types separately: nonempty mesh, curve, text, empty/landmark, and collection membership. An object count is not a count of anatomical structures.

Map source object IDs to persistent anatomy concepts before conversion. Preserve curves such as peripheral nerves by recording spline geometry and testing their rendered/exported representation; a mesh-only exporter can omit them. Record transform, units, bounds, laterality, source hash, mesh/material references, and whether multiple objects form one structure or one object covers multiple structures.

Export a bounded regional sample before bulk conversion. Compare source and output object identities, count, transforms, geometry, labels, and representative rendered views. Validate glTF/GLB with the Khronos validator. Use glTF Transform or mesh simplification only after checking that joining, flattening, or decimation does not erase selectable structure boundaries or important landmarks.

Report verified geometry, partial representation, name-only markers, and unresolved objects separately. A plausible render or matching name does not prove anatomical correctness; send uncertain placements and identity claims to regional review.
