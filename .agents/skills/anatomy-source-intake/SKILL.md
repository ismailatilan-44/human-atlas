---
name: anatomy-source-intake
description: Evaluate a new anatomy model, image dataset, ontology, or licensed asset source for an atlas; record what is actually available, its provenance, and permitted uses. Use before importing third-party anatomy data.
---

# Anatomy source intake

Distinguish an original dataset from an application that repackages it. Inspect the upstream release, source files or manifests, documentation, and the terms that apply to the specific components being considered. A repository's code license does not establish the license of bundled models, images, or text.

For each candidate record the source URL, creator, release/version, access date, file hashes when files were actually obtained, asset type, anatomical region, reference body or donor, coordinate system if known, attribution, component-level license or agreement, and any unresolved provenance. Separate **observed in source**, **claimed by source**, and **inferred** findings. Do not claim mesh quality from screenshots or a README alone.

Record use status separately for private inspection, adaptation, and inclusion in a distributed product. Private access and redistribution are distinct; do not infer either right from the other's availability. When rights or origins are unclear, retain the candidate as unresolved rather than silently promoting it into a release asset. Follow the user's current authorization for acquisition and analysis, and document material source-specific access conditions before using restricted material.

Finish with a compact intake record and the next verification needed: geometry audit, terminology mapping, imaging review, or rights clarification.
