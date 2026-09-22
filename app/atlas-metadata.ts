import type { Atlas } from "./anatomy";
import labels from "../data/anatomy/labels.json";
import brachialPlexus from "../data/anatomy/brachial-plexus.json";

export type AnatomyLanguage = "tr" | "en" | "la";

const BRACHIAL_PLEXUS_IDS = new Set(brachialPlexus.labels.flatMap((entry) => entry.ids));

// Reviewed in docs/model/2026-09-08-audit.md (M-01). Keep the source manifest intact.
const NERVOUS_PARTS = new Set(["FJ1730", "FJ1731", "FJ1752", "FJ1767", "FJ1814"]);
// The source IS-A hierarchy identifies both lacrimal bones and inferior nasal conchae as bones.
const SKULL_BONE_PARTS = new Set(["FJ3263", "FJ3265", "FJ3369", "FJ3371"]);
// Reviewed IS-A muscle organs use the muscle display layer, including pharyngeal muscles.
// Anatomical region and source PART-OF context remain independent of the primary layer.
const MUSCLE_PARTS = new Set([
  "FJ1504",
  "FJ1504M",
  "FJ1409",
  "FJ1409M",
  "FJ1410",
  "FJ1410M",
  "FJ1411",
  "FJ1411M",
  "FJ1438",
  "FJ1438M",
  "FJ1439",
  "FJ1439M",
  "FJ1440",
  "FJ1440M",
  "FJ1532",
  "FJ1532M",
  "FJ2740",
  "FJ2742",
  "FJ2743",
  "FJ2745",
  "FJ2746",
  "FJ2747",
  "FJ2752",
  "FJ2754",
  "FJ2755",
  "FJ2757",
  "FJ2758",
  "FJ2759",
]);
// These are hepatic organ-segment surfaces, not venous vessels (source IS-A FMA86140).
const HEPATIC_SEGMENT_PARTS = new Set([
  "FJ1858",
  "FJ2409",
  "FJ2818",
  "FJ2819",
  "FJ2820",
  "FJ2821",
  "FJ2822",
  "FJ2823",
  "FJ2824",
]);

/** Apply reviewed display metadata without mutating source data or geometry identities. */
export function prepareAtlas(atlas: Atlas): Atlas {
  return {
    ...atlas,
    parts: atlas.parts.map((part) => {
      const system = NERVOUS_PARTS.has(part.id)
        ? "nervous"
        : SKULL_BONE_PARTS.has(part.id)
          ? "skeletal"
          : MUSCLE_PARTS.has(part.id)
            ? "muscular"
            : HEPATIC_SEGMENT_PARTS.has(part.id)
              ? "digestive"
              : part.system;
      return system === part.system ? part : { ...part, system };
    }),
  };
}

/** A missing note does not establish that a structure is fully represented. */
export function getRepresentationNote(conceptId: string): string | undefined {
  if (conceptId === "atlas:skull-bones") {
    return "Mandibula dahil 22 kafatası kemiği yüzeyi. Göz yapıları, hyoid ve orta kulak kemikçikleri bu seçime dahil değildir.";
  }
  if (conceptId === "FMA46565") {
    return "BodyParts3D kaynak grubu, kafatası kemikleri yanında göz ve gözyaşı bezi yapıları ile hyoid yüzeylerini de içerir. Yalnız kemikler için Kafatası kemikleri seçimini kullanın.";
  }
  if (BRACHIAL_PLEXUS_IDS.has(conceptId)) return brachialPlexus.representationNoteTr;
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
  const label = LABELS_BY_ID.get(conceptId);
  return label && "representationNoteTr" in label ? label.representationNoteTr : undefined;
}

const LABELS_BY_ID = new Map(
  [...labels.entries, ...brachialPlexus.labels].flatMap((entry) =>
    entry.ids.map((id) => [id, entry] as const),
  ),
);

/** Outside reviewed label sets, retain the supplied source label. */
export function anatomyLabel(id: string, fallback: string, language: AnatomyLanguage): string {
  const entry = LABELS_BY_ID.get(id);
  // A missing Latin term must not remove a reviewed source-group qualifier.
  const label =
    entry?.[language] ||
    (entry && "sourceGroupLabel" in entry && entry.sourceGroupLabel ? entry.en : undefined);
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

/** Include all reviewed languages and source names, regardless of display language. */
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
