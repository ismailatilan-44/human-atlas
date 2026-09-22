import type { Atlas } from "./anatomy";

// Evidence: data/model-candidates/lung-source-outliers/REVIEW.md.
// BP3D 4.0 assigns renal-region geometry to a pulmonary concept. Preserve
// source membership separately; never infer a replacement renal identity.
const OUTLIERS = new Set(["FJ2041", "FJ2044"]);
const REVIEWED = new Set([
  "FMA8620",
  "FMA8755",
  "FMA13278",
  "FMA50872",
  "FMA66326",
  "FMA68197",
  "FMA7158",
  "FMA7309",
  "FMA7333",
  "FMA7359",
  "FMA9576",
  "FMA45621",
  "FMA45662",
  "FMA45842",
  "FMA67994",
  "FMA85008",
  "FMA85055",
  "FMA259209",
  "FMA265130",
]);
const SOURCE_PREFIX = "atlas:source-membership:";
const UNVERIFIED_PREFIX = "atlas:unverified-source:";

export function selectionVariant(id: string) {
  if (REVIEWED.has(id)) return { id: SOURCE_PREFIX + id, source: true };
  const canonical = sourceSelectionId(id);
  return canonical ? { id: canonical, source: false } : undefined;
}

export function sourceSelectionId(id: string): string | undefined {
  const canonical = id.startsWith(SOURCE_PREFIX) ? id.slice(SOURCE_PREFIX.length) : "";
  return REVIEWED.has(canonical) ? canonical : undefined;
}

export function unverifiedSourcePart(id: string): string | undefined {
  const part = id.startsWith(UNVERIFIED_PREFIX) ? id.slice(UNVERIFIED_PREFIX.length) : "";
  return OUTLIERS.has(part) ? part : undefined;
}

export function selectionReviewNote(id: string): string | undefined {
  if (REVIEWED.has(id))
    return "Kaynakta bu gruba bağlanan, ancak böbrek seviyesinde bulunan iki damar yüzeyi bu seçimden çıkarıldı.";
  if (sourceSelectionId(id))
    return "Ham kaynak seçimi: anatomik eşleşmesi belirsiz FJ2041 ve FJ2044 damar yüzeylerini de içerir. Bu iki yüzey akciğerde değil, böbrek seviyesindedir. Akciğer/toraks incelemesi için incelenmiş seçime dönün.";
  const part = unverifiedSourcePart(id);
  if (part)
    return `${part}: kaynak bu yüzeyi sağ anterior segmental artere (FMA8620) bağlamış, ancak geometri böbrek seviyesindedir. Kesin damar kimliği doğrulanmadı; pulmoner veya renal dal olarak adlandırılmıyor.`;
}

/** Idempotent display adaptation, including when extensions arrive after base preparation. */
export function applyReviewedSelections(atlas: Atlas): Atlas {
  const concepts = new Map(atlas.concepts.map((concept) => [concept.id, concept]));
  for (const id of REVIEWED) {
    const concept = concepts.get(id);
    if (!concept) continue;
    const sourceId = SOURCE_PREFIX + id;
    const previousSource = concepts.get(sourceId);
    const sourceElements = [...new Set([...(previousSource?.elements ?? []), ...concept.elements])];
    if (!sourceElements.some((part) => OUTLIERS.has(part))) continue;
    concepts.set(sourceId, {
      id: sourceId,
      name: concept.name,
      elements: sourceElements,
    });
    concepts.set(id, {
      ...concept,
      elements: sourceElements.filter((part) => !OUTLIERS.has(part)),
    });
  }
  const parts = atlas.parts.map((part) => {
    if (!OUTLIERS.has(part.id)) return part;
    const id = UNVERIFIED_PREFIX + part.id;
    concepts.set(id, { id, name: `Unverified source vessel ${part.id}`, elements: [part.id] });
    return {
      ...part,
      sourceConceptId: part.sourceConceptId ?? part.conceptId,
      conceptId: id,
      name: `Unverified source vessel ${part.id}`,
    };
  });
  return { ...atlas, parts, concepts: [...concepts.values()] };
}
