import { DEFAULT_VISIBLE, type Atlas, type DatasetId, type SceneState } from "./anatomy";
import { anatomyLabel, anatomySearchTerms, type AnatomyLanguage } from "./atlas-metadata";
import {
  femalePelvisConcepts,
  femalePelvisLabel,
  femalePelvisSearchTerms,
} from "./female-pelvis-labels";

export const REFERENCE_DATASETS = {
  "female-pelvis": {
    title: "Kadın pelvis referansı",
    heading: "Pelvis Atlas",
    identity: "Kadın · HRA",
    sex: "female",
    manifest: "/models/female-pelvis/atlas.json",
    scope: "Uterus, iki ovaryum ve pelvis kemikleri. Tam kadın vücudu değildir.",
    description:
      "HRA kadın pelvis referansında yer alan yapı. Bu sahne yalnız mevcut pelvis parçalarını içerir; anatomik ilişki bilgisi eklenmedi.",
    sourceName: "Human Reference Atlas",
    placeholder: "Rahim, ovary, pelvis…",
  },
  "inner-ear-reference": {
    title: "İç kulak referansı",
    heading: "İç Kulak Atlası",
    identity: "İç kulak · ayrı referans",
    sex: "unspecified",
    manifest: "/models/inner-ear-reference/atlas.json",
    scope:
      "İki taraflı koklea, vestibüler kompleks ve temporal kemik bağlamı. Tam kulak modeli değildir; kaynak cinsiyeti belirtilmemiştir.",
    description:
      "Ayrı kaynak referansındaki yapı. Vestibüler kompleks tek kaynak parçasıdır; bağımsız vestibül ve yarım daire kanalı segmentasyonu değildir. Anatomik ilişkiler eklenmedi.",
    sourceName: "Z-Anatomy · iç kulak referansı",
    placeholder: "Koklea, vestibül, temporal…",
  },
} as const;

export function referenceDataset(dataset?: DatasetId) {
  return dataset && dataset !== "male-body" ? REFERENCE_DATASETS[dataset] : undefined;
}
export function referenceDescription(dataset: DatasetId, conceptId?: string): string | undefined {
  if (dataset === "inner-ear-reference" && conceptId?.endsWith("-cochlea"))
    return "Kokleanın dış biçimini gösteren kaynak yüzeyi. İç bölmeler, zarlar ve duyu hücreleri ayrı modellenmemiştir.";
  if (dataset === "inner-ear-reference" && conceptId?.endsWith("-temporal-bone"))
    return "İç kulağın konumunu incelemek için aynı kaynak modelden alınan temporal kemik. Saydamlık, kemik içindeki yapıları görünür kılar.";
  return referenceDataset(dataset)?.description;
}
export function atlasDataset(atlas: Atlas): DatasetId {
  return atlas.datasetId ?? (atlas.sex === "female" ? "female-pelvis" : "male-body");
}
export function referenceConcepts(atlas: Atlas) {
  return atlasDataset(atlas) === "female-pelvis"
    ? femalePelvisConcepts(atlas.concepts)
    : atlas.concepts;
}
export function defaultDatasetScene(
  atlas: Atlas,
): Pick<SceneState, "visible" | "selected" | "ghost"> {
  const innerEar = atlasDataset(atlas) === "inner-ear-reference";
  return {
    visible: [...new Set(atlas.parts.map((p) => p.system))].filter((id) =>
      DEFAULT_VISIBLE.includes(id),
    ),
    selected: innerEar ? atlas.parts.filter((p) => p.system === "sensory").map((p) => p.id) : [],
    ghost: innerEar,
  };
}

const innerEarLabels: Record<string, { tr: string; en: string; la: string; source: string }> = {};
for (const [side, tr, en, suffix] of [
  ["left", "Sol", "Left", "L"],
  ["right", "Sağ", "Right", "R"],
]) {
  innerEarLabels[`inner-ear-reference:${side}-cochlea`] = {
    tr: `${tr} koklea (salyangoz)`,
    en: `${en} cochlea`,
    la: `Cochlea (${suffix})`,
    source: `Cochlea.${suffix.toLowerCase()}`,
  };
  innerEarLabels[`inner-ear-reference:${side}-vestibular-complex`] = {
    tr: `${tr} vestibül / yarım daire kanalı kompleksi`,
    en: `${en} vestibule / semicircular-canal complex`,
    la: `Vestibulum / canales semicirculares (${suffix})`,
    source: `Vestibule.${suffix.toLowerCase()}`,
  };
  innerEarLabels[`inner-ear-reference:${side}-temporal-bone`] = {
    tr: `${tr} temporal kemik (şakak kemiği)`,
    en: `${en} temporal bone`,
    la: `Os temporale (${suffix})`,
    source: `Temporal bone.${suffix.toLowerCase()}`,
  };
}
export function datasetLabel(
  dataset: DatasetId,
  id: string,
  name: string,
  language: AnatomyLanguage,
): string {
  if (dataset === "female-pelvis") return femalePelvisLabel(id, name, language);
  if (dataset === "inner-ear-reference") return innerEarLabels[id]?.[language] ?? name;
  return anatomyLabel(id, name, language);
}
export function datasetSearchTerms(dataset: DatasetId, id: string, name: string): string[] {
  if (dataset === "female-pelvis") return femalePelvisSearchTerms(id, name);
  if (dataset !== "inner-ear-reference") return anatomySearchTerms(id, name);
  const terms = [id, name, ...Object.values(innerEarLabels[id] ?? {})];
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
