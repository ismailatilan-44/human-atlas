---
name: anatomy-term-mapping
description: Map anatomical model objects to stable concepts, multilingual labels, laterality, and cited structural relationships. Use when adding or auditing anatomy labels and knowledge-graph entries.
---

# Anatomy term mapping

Treat the anatomical concept, model object, display label, and rendered selection group as different entities. Preserve the project's existing primary IDs; attach FMA, Uberon, TA2/FIPAT, or other external IDs as cross-references only when their meaning matches. Check source version and exact term scope, including whether a name describes a whole structure, branch, region, surface, or parenchyma.

For each proposed mapping verify laterality, parent/part relationship, synonym status, and source evidence. Use official terminology and source tables before fuzzy matching. A name match is a candidate, not proof that the geometry is independently selectable. Do not invent a Latin term, innervation, attachment, or vascular supply when the consulted source does not establish it; leave the field unresolved and say what would resolve it.

Keep relationship types explicit (`part_of`, `branch_of`, `innervates`, `adjacent_to`, etc.) and distinguish directly sourced claims from transitive or visual inferences. Return machine-readable candidate records with evidence and review status, plus a short list of conflicts for an anatomist to decide.
