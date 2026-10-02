---
name: anatomy-regional-acceptance
description: Review whether a body region in a 3D anatomy atlas is ready for medical-student use at a stated detail level. Use for regional QA, coverage reporting, and model release decisions.
---

# Anatomy regional acceptance

Begin with the project's versioned region × structure-family × detail target inventory. Check each required structure at its specified level: D0 location/whole, D1 named selectable structure, D2 subdivision or branch, and D3 fine tissue or functional unit where required. Do not turn a pilot checklist, mesh total, or search result into a whole-body completion percentage.

Inspect the actual product flow: find, select, isolate, hide/show context, follow part/neighbor relationships, and view appropriate labels at close range. Compare geometry and claims with their source records and, where available, medical images. Include left/right, cross-region continuity, reference-body switches, and mobile/web performance when relevant to the release.

Keep technical validation, identity validation, and anatomical expert acceptance as separate statuses. An anatomist or qualified domain reviewer decides contested structure identity, placement, and clinical relevance; record reviewer and evidence. Publish a release report with accepted targets, partial targets, unresolved identity/placement, uninspected families, source versions, and regressions. A missing required target stays visible until resolved or explicitly deferred to another scope version.

Apply the [lightweight source/decision review](../../../docs/model/agent-workflow.md#lightweight-review-before-acceptance) and existing visual QA only to the affected claims and flows. For skull work, use the relevant [research record](../../../docs/model/skull-research/README.md); source-backed content and passing software checks do not close expert acceptance.
