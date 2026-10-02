# Human Atlas repository guidance

Start with `README.md`, the [scope and acceptance plan](docs/model/model-scope-and-acceptance.md), and the [latest recorded delivery handoff](docs/model/progress-report-2026-10-02.md); verify their recorded revisions against the current Git state. The [26 September report](docs/model/progress-report-2026-09-26.md) remains historical evidence. Then read only the task-relevant records under `docs/model/`. Use `.agents/skills/` for anatomy source intake, geometry audits, terminology mapping, benchmarking, imaging, and regional acceptance when the task calls for that workflow.

For authored data, generated outputs, and task-specific checks, follow [source → producer → check routing](docs/model/agent-workflow.md). This file and the six repository skills are versioned guidance: start isolated work from a revision containing them and verify their presence before editing. Older revisions do not inherit untracked files from another checkout; report missing guidance rather than silently working without it. Keep machine-local paths, credentials, and browser session details out of these portable instructions.

- Preserve source object and concept identifiers, reference-body coordinates, component attribution, and separate source licenses.
- Keep observed geometry, inferred anatomy, coverage targets, and pending expert review explicit. Use the versioned regional coverage records when reporting completeness.
- Run the smallest relevant checks from `README.md`: `npm run check`, anatomy knowledge tests, atlas/interaction validators, or `npm run build`, depending on the changed surface. Report only checks actually run.
- Record source and model changes in the owning intake, registration, coverage, or attribution record. Keep instructions and skills for this atlas inside this repository.
- Accept each model package through the relevant search → selection → focus/context → relationship → return journey. Keep source geometry, local interaction, deployed source revision, and anatomical expert acceptance separate.
- At substantial delivery closure, update the existing delivery handoff with the source revision, observed user flow, check environment/results, unresolved targets, and one next package. Link to a newer handoff here when one supersedes the current record; preserve historical reports.
