import { datasetSearchTerms } from "./reference-datasets";
import type { Concept, DatasetId } from "./anatomy";

/** Shared UI/agent matching; fold Turkish I before stripping combining marks. */
export function normalizeAnatomySearch(value: string): string {
  return value.toLocaleLowerCase("tr").normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "").replace(/ı/g, "i").trim();
}
export function matchesAnatomyQuery(dataset: DatasetId, concept: Concept, query: string): boolean {
  const normalized = normalizeAnatomySearch(query);
  return datasetSearchTerms(dataset, concept.id, concept.name)
    .some(term => normalizeAnatomySearch(term).includes(normalized));
}
