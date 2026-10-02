import graph from "../data/anatomy/explorer.json";
import { atlasDataset, referenceDataset, referenceConcepts } from "./reference-datasets";
import type { Atlas, Concept, DatasetId } from "./anatomy";
import lowerLimb from "../data/anatomy/lower-limb-reference.json";
import upperLimb from "../data/anatomy/upper-limb-reference.json";

export const knowledgeEntities = new Map(graph.entities.map((entity) => [entity.id, entity]));
export const knowledgeSources = new Map(graph.sources.map((source) => [source.id, source]));
const lowerLimbSources = new Map(lowerLimb.sources.map((source) => [source.id, source]));
const upperLimbSources = new Map(upperLimb.sources.map((source) => [source.id, source]));
export function knowledgeSource(id: string, dataset: DatasetId = "male-body") {
  return dataset === "upper-limb-nerve-reference" ? upperLimbSources.get(id)
    : dataset === "lower-limb-nerve-reference" ? lowerLimbSources.get(id) : knowledgeSources.get(id);
}
export const relationshipNames: Record<string, [string, string]> = {
  attaches_to: ["Bağlandığı kemik", "Bağlanan yapı"],
  articulates_with: ["Eklem yaptığı kemik", "Eklem yaptığı kemik"],
  part_of: ["Parçası olduğu yapı", "İçerdiği yapılar"],
  originates_at: ["Başlangıç yeri", "Buradan başlayan kas"],
  inserts_at: ["Tutunma yeri", "Buraya tutunan kas"],
  innervates: ["Uyardığı kas", "Uyaran sinir"],
  supplies: ["Beslediği yapı", "Besleyen damar"],
  passes_through: ["İçinden geçtiği yapı", "İçinden geçen yapı"],
  branch_of: ["Dalı olduğu sinir", "Sinirin dalları"],
};

export function explorerConcepts(atlas: Atlas): Concept[] {
  if (referenceDataset(atlasDataset(atlas))) return referenceConcepts(atlas);
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

type ExplorerRelation = {
  id: string; subject: string; predicate: string; object: string;
  evidence: { sourceId: string; locator?: string }[];
  viaDivision?: string | null; attachmentNoteTr?: string | null;
  qualifiers?: Record<string, unknown>;
};
export function relationshipsFor(id: string, concepts?: Map<string, Concept>, dataset: DatasetId = "male-body") {
  const relations: ExplorerRelation[] = dataset === "upper-limb-nerve-reference" ? upperLimb.relations : dataset === "lower-limb-nerve-reference"
    ? lowerLimb.relations : dataset === "male-body" ? graph.relations : [];
  return relations
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

/** Preserve source constraints for both students and programmatic consumers. */
export function representationFor(id: string, dataset: DatasetId = "male-body") {
  if (dataset !== "male-body") return undefined;
  return knowledgeEntities.get(id);
}
export function relationshipScopeNotes(qualifiers?: Record<string, unknown>): string[] {
  const names: Record<string, string> = {
    semantics: "İlişkinin anlamı", geometry: "Geometri sınırı", scope: "Kapsam",
    variation: "Varyasyon", coverage: "Kapsam sınırı",
    incompleteEndpointSet: "Uçların tamamı gösterilmiyor",
  };
  return Object.entries(names).flatMap(([key, label]) => {
    const value = qualifiers?.[key];
    if (value === undefined || value === null || value === false) return [];
    return [value === true ? label : `${label}: ${typeof value === "string" ? value : JSON.stringify(value)}`];
  });
}
