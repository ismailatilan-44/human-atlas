// Keep the audited source graph intact; ship only fields used by the viewer.
import fs from "node:fs";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
const root = new URL("../", import.meta.url);
const read = (path) => JSON.parse(fs.readFileSync(new URL(path, root), "utf8"));
const graph = read("data/anatomy/knowledge.json");
const baseIds = new Set(read("public/models/atlas.json").concepts.map((c) => c.id));
const catalog = {
  entities: graph.entities
    .filter((e) => !baseIds.has(e.id))
    .map(({ id, name, geometryPartIds }) => ({ id, name, geometryPartIds })),
  sources: graph.sources.map(({ id, title, url }) => ({ id, title, url })),
  relations: graph.relations.map(
    ({ id, subject, predicate, object, status, evidence, qualifiers }) => ({
      id,
      subject,
      predicate,
      object,
      status,
      viaDivision: qualifiers?.viaDivision ?? null,
      evidence: evidence.map(({ sourceId, locator }) => ({ sourceId, locator })),
    }),
  ),
};
const target = new URL("data/anatomy/explorer.json", root);
const output = JSON.stringify(catalog) + "\n";
if (process.argv.includes("--check"))
  assert.equal(
    fs.readFileSync(target, "utf8"),
    output,
    "Regenerate explorer catalog: node scripts/build-explorer-catalog.mjs",
  );
else fs.writeFileSync(target, output);
console.log(
  JSON.stringify({
    entities: catalog.entities.length,
    relations: catalog.relations.length,
    bytes: Buffer.byteLength(output),
    path: fileURLToPath(target),
  }),
);
