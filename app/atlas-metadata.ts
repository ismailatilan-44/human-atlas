import type { Atlas } from "./anatomy";
import labels from "../data/anatomy/labels.json";

export type AnatomyLanguage = "tr" | "en" | "la";

// Reviewed in docs/model/2026-09-08-audit.md (M-01). Keep the source manifest intact.
const NERVOUS_PARTS = new Set(["FJ1730", "FJ1731", "FJ1752", "FJ1767", "FJ1814"]);

/** Apply reviewed display metadata without mutating source data or geometry identities. */
export function prepareAtlas(atlas: Atlas): Atlas {
  return {
    ...atlas,
    parts: atlas.parts.map((part) =>
      NERVOUS_PARTS.has(part.id) && part.system !== "nervous"
        ? { ...part, system: "nervous" }
        : part,
    ),
  };
}

/** A missing note does not establish that a structure is fully represented. */
export function getRepresentationNote(conceptId: string): string | undefined {
  if (conceptId === "atlas:left-median-nerve" || conceptId === "atlas:right-median-nerve") {
    return "Bu model ana sinir gövdesini gösterir; ayrı kas, palmar ve dijital dal modelleri henüz eklenmedi.";
  }
  if (conceptId === "atlas:left-sciatic-nerve" || conceptId === "atlas:right-sciatic-nerve") {
    return "Bu model pelvis ve uyluktaki ana sinir gövdelerini gösterir; ayrı tibial ve ortak fibular devamlar henüz eklenmedi.";
  }
  if (conceptId === "FMA9603") {
    return "Bu kaynak model sağ ve sol tiroid lobları ile isthmusu içerir. Paratiroidler ve piramidal lob bu pakete dahil değildir.";
  }
  if (conceptId === "FMA7647") {
    return "Omuriliğin uzunlamasına sinir dokusu ve mevcut merkez kanal parçası birlikte gösteriliyor. Kökler, zarlar ve ayrı segment modelleri bu pakete dahil değildir.";
  }
  return undefined;
}

const LABELS_BY_ID = new Map(
  labels.entries.flatMap((entry) => entry.ids.map((id) => [id, entry] as const)),
);

/** Outside the reviewed pilot, retain the supplied source label. */
export function anatomyLabel(id: string, fallback: string, language: AnatomyLanguage): string {
  const entry = LABELS_BY_ID.get(id);
  const label = entry?.[language];
  if (!entry || !label) return fallback;
  if (!entry.side) return label;
  // Retain the exact TA2 Latin term; L/R are side markers, not invented Latin declensions.
  if (language === "la") return `${label} (${entry.side === "left" ? "L" : "R"})`;
  const side =
    language === "tr"
      ? entry.side === "left"
        ? "Sol"
        : "Sağ"
      : entry.side === "left"
        ? "Left"
        : "Right";
  return `${side} ${label.toLocaleLowerCase(language)}`;
}

/** Include all pilot languages and source names, regardless of display language. */
export function anatomySearchTerms(id: string, fallback: string): string[] {
  const entry = LABELS_BY_ID.get(id);
  const terms = [id, fallback];
  if (entry) {
    terms.push(
      ...(["tr", "en", "la"] as const).map((language) => anatomyLabel(id, fallback, language)),
      ...entry.aliases,
    );
  }
  // Permit an ASCII keyboard to find Turkish labels while retaining readable terms.
  return [
    ...new Set(
      terms.flatMap((term) => [
        term,
        term
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .replace(/ı/g, "i"),
      ]),
    ),
  ];
}
