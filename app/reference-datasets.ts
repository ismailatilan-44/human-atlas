import { DEFAULT_VISIBLE, type Atlas, type DatasetId, type SceneState } from "./anatomy";
import { anatomyLabel, anatomySearchTerms, type AnatomyLanguage } from "./atlas-metadata";
import {
  femalePelvisConcepts,
  femalePelvisLabel,
  femalePelvisSearchTerms,
} from "./female-pelvis-labels";
import lowerLimb from "../data/anatomy/lower-limb-reference.json";

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
  "lower-limb-nerve-reference": {
    title: "Alt ekstremite sinir referansı",
    heading: "Alt Ekstremite Atlası",
    identity: "Alt ekstremite · Z-Anatomy",
    sex: "male",
    manifest: "/models/lower-limb-nerve-reference/atlas.json",
    scope:
      "İki taraflı siyatik, tibial ve ortak fibular sinirler; aynı kaynaktan kemik bağlamı. Tam sinir ağı değildir; uzman incelemesi bekliyor.",
    description:
      "Sinirlerin konumunu incelemek için aynı kaynak modelden alınan kemik bağlamı. Bu ayrı referans ana vücut modeliyle birleştirilmez.",
    sourceName: "Z-Anatomy · alt ekstremite referansı",
    placeholder: "Tibial, fibular, siyatik…",
  },
} as const;

export function referenceDataset(dataset?: DatasetId) {
  return dataset && dataset !== "male-body" ? REFERENCE_DATASETS[dataset] : undefined;
}
export function referenceDescription(dataset: DatasetId, conceptId?: string): string | undefined {
  if (dataset === "lower-limb-nerve-reference" && conceptId?.startsWith("atlas:"))
    return "Kaynakta ayrı adlandırılmış sinir eğrisinin kapsamı. Ayrı distal dallar ve kök kimlikleri bu pakette yoktur; tam alt ekstremite sinir ağı değildir. Siyatik dal bağlantıları kaynakla desteklenir; anatomik uzman incelemesi bekliyor.";
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
  const dataset = atlasDataset(atlas);
  const selectionSystem = dataset === "inner-ear-reference" ? "sensory"
    : dataset === "lower-limb-nerve-reference" ? "nervous" : undefined;
  return {
    visible: [...new Set(atlas.parts.map((p) => p.system))].filter((id) =>
      DEFAULT_VISIBLE.includes(id),
    ),
    selected: selectionSystem ? atlas.parts.filter((p) => p.system === selectionSystem).map((p) => p.id) : [],
    ghost: !!selectionSystem,
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
  if (dataset === "lower-limb-nerve-reference") {
    const entry = lowerLimb.labels.find((label) => label.ids.includes(id));
    const term = entry?.[language] ?? name;
    if (entry?.side !== "left" && entry?.side !== "right") return term;
    if (language === "la") return `${term} (${entry.side === "left" ? "L" : "R"})`;
    return `${language === "tr" ? entry.side === "left" ? "Sol" : "Sağ" : entry.side === "left" ? "Left" : "Right"} ${term}`;
  }
  return anatomyLabel(id, name, language);
}
export function datasetSearchTerms(dataset: DatasetId, id: string, name: string): string[] {
  if (dataset === "female-pelvis") return femalePelvisSearchTerms(id, name);
  if (dataset === "lower-limb-nerve-reference") {
    const entry = lowerLimb.labels.find((label) => label.ids.includes(id));
    const terms = [id, name, ...["tr", "en", "la"].map((language) =>
      datasetLabel(dataset, id, name, language as AnatomyLanguage)), ...(entry?.aliases ?? [])];
    return [...new Set(terms.flatMap((term) => [term, term.normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "").replace(/ı/g, "i")]))];
  }
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
