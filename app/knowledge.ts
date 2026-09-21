import graph from "../data/anatomy/explorer.json";
import { femalePelvisConcepts } from "./female-pelvis-labels";
import type { Atlas, Concept } from "./anatomy";

export const knowledgeEntities = new Map(graph.entities.map((entity) => [entity.id, entity]));
export const knowledgeSources = new Map(graph.sources.map((source) => [source.id, source]));
export const relationshipNames: Record<string, [string, string]> = {
  attaches_to: ["Bağlandığı kemik", "Bağlanan yapı"],
  part_of: ["Parçası olduğu yapı", "İçerdiği yapılar"],
  originates_at: ["Başlangıç yeri", "Buradan başlayan kas"],
  inserts_at: ["Tutunma yeri", "Buraya tutunan kas"],
  innervates: ["Uyardığı kas", "Uyaran sinir"],
  supplies: ["Beslediği yapı", "Besleyen damar"],
  passes_through: ["İçinden geçtiği yapı", "İçinden geçen yapı"],
};

export function explorerConcepts(atlas: Atlas): Concept[] {
  if (atlas.datasetId === "female-pelvis" || atlas.sex === "female")
    return femalePelvisConcepts(atlas.concepts);
  const concepts = new Map(atlas.concepts.map((c) => [c.id, c]));
  for (const entity of graph.entities) {
    if (!concepts.has(entity.id))
      concepts.set(entity.id, {
        id: entity.id,
        name: entity.name,
        elements: entity.geometryPartIds,
      });
  }
  return [...concepts.values()];
}

export function relationshipsFor(id: string, concepts?: Map<string, Concept>) {
  return graph.relations
    .filter((r) => r.subject === id || r.object === id)
    .map((relation) => {
      const outgoing = relation.subject === id;
      const otherId = outgoing ? relation.object : relation.subject;
      return {
        ...relation,
        otherId,
        divisionLabel:
          relation.viaDivision === "tibial"
            ? "Tibial bölüm üzerinden"
            : relation.viaDivision === "common_fibular"
              ? "Ortak fibular bölüm üzerinden"
              : undefined,
        label: relationshipNames[relation.predicate][outgoing ? 0 : 1],
        name: concepts?.get(otherId)?.name ?? knowledgeEntities.get(otherId)?.name ?? otherId,
      };
    })
    .sort(
      (a, b) =>
        Number(a.predicate === "part_of") - Number(b.predicate === "part_of") ||
        a.name.localeCompare(b.name),
    );
}
