import { DEFAULT_VISIBLE, type Atlas, type DatasetId, type SceneState } from "./anatomy";
import { anatomyLabel, anatomySearchTerms, type AnatomyLanguage } from "./atlas-metadata";
import {
  femalePelvisConcepts,
  femalePelvisLabel,
  femalePelvisSearchTerms,
} from "./female-pelvis-labels";
import lowerLimb from "../data/anatomy/lower-limb-reference.json";
import upperLimb from "../data/anatomy/upper-limb-reference.json";

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
    title: "Alt ekstremite referansı",
    heading: "Alt Ekstremite Atlası",
    identity: "Alt ekstremite · Z-Anatomy",
    sex: "male",
    manifest: "/models/lower-limb-nerve-reference/atlas.json",
    scope: "Kısmi sinir/arter seyirleri, seçilmiş bağlar, ayak kasları, sesamoid grupları, retinakulumlar ve plantar aponevroz; aynı kaynaktan kemik bağlamı. Bütün ayak ayrıntıları veya tam ağ değildir; uzman incelemesi bekliyor.",
    description: lowerLimb.descriptionTr,
    sourceName: "Z-Anatomy · alt ekstremite referansı",
    placeholder: "Retinakulum, plantar bağ, ayak kası…",
  },
  "upper-limb-nerve-reference": {
    title: "Üst ekstremite sinir referansı",
    heading: "Üst Ekstremite Sinir Atlası",
    identity: "Üst ekstremite · Z-Anatomy",
    sex: "male",
    manifest: "/models/upper-limb-nerve-reference/atlas.json",
    scope: "Adlandırılmış sinir seyirleri, kas dalı grupları ve aynı kaynaktan kemik bağlamı. Kökler, medial/lateral kordlar ve bütün el dalları bu referansta ayrı modellenmemiştir; uzman incelemesi bekliyor.",
    description: upperLimb.descriptionTr,
    sourceName: "Z-Anatomy · üst ekstremite sinir referansı",
    placeholder: "Ulnar, radial, supraskapular…",
  },
} as const;

export function referenceDataset(dataset?: DatasetId) {
  return dataset && dataset !== "male-body" ? REFERENCE_DATASETS[dataset] : undefined;
}
export function referenceDescription(dataset: DatasetId, conceptId?: string): string | undefined {
  if (dataset === "upper-limb-nerve-reference") {
    const entry = upperLimb.labels.find((label) => label.ids.includes(conceptId ?? ""));
    return [entry?.la === null ? "Latince ad henüz doğrulanmadı; İngilizce gösterim adı korunur." : undefined,
      entry?.scopeNoteTr, upperLimb.descriptionTr].filter(Boolean).join(" ");
  }
  if (dataset === "lower-limb-nerve-reference") {
    const entry = lowerLimb.labels.find((label) => label.ids.includes(conceptId ?? ""));
    const authoredNote = entry && "representationNoteTr" in entry ? entry.representationNoteTr : undefined;
    const scope = authoredNote || (entry?.componentRole === "nerve"
      ? "Adlandırılmış sinirin kaynakta çizilmiş kısmi seyrini gösterir. İnce dallar, kökler ve tam innervasyon kapsamı bu modelden çıkarılamaz; anatomik uzman incelemesi bekliyor."
      : entry?.componentRole === "artery"
        ? "Fibular arterin kaynakta çizilmiş kısmi seyrini gösterir. Tam damar ağı ve besleme alanı bu modelden çıkarılamaz; anatomik uzman incelemesi bekliyor."
        : entry?.componentRole === "ligament"
          ? "Kaynakta ayrı adlandırılmış bağ yüzeyidir. Ayak bileğinin bütün bağları, eklem kapsülü ve tutunma bölgeleri bu seçimle karşılanmaz; anatomik uzman incelemesi bekliyor."
          : entry?.componentRole === "bone_context"
            ? "Aynı kaynak modelden alınmış ayrı kemik yüzeyidir. Eklem ayrıntıları ve bağ tutunmaları ayrıca incelenmelidir; anatomik uzman incelemesi bekliyor."
            : undefined);
    const note = entry?.la === null
      ? "Latince ad henüz doğrulanmadı; Latince modunda İngilizce gösterim adı korunur."
      : undefined;
    return [note, scope || lowerLimb.descriptionTr].filter(Boolean).join(" ");
  }
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
    : dataset === "lower-limb-nerve-reference" || dataset === "upper-limb-nerve-reference" ? "nervous" : undefined;
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
  if (dataset === "lower-limb-nerve-reference" || dataset === "upper-limb-nerve-reference") {
    const entries = dataset === "upper-limb-nerve-reference" ? upperLimb.labels : lowerLimb.labels;
    const entry = entries.find((label) => label.ids.includes(id));
    const term = entry?.[language] ?? entry?.en ?? name;
    if (entry?.side !== "left" && entry?.side !== "right") return term;
    if (language === "la") return `${term} (${entry.side === "left" ? "L" : "R"})`;
    return `${language === "tr" ? entry.side === "left" ? "Sol" : "Sağ" : entry.side === "left" ? "Left" : "Right"} ${term}`;
  }
  return anatomyLabel(id, name, language);
}
export function datasetSearchTerms(dataset: DatasetId, id: string, name: string): string[] {
  if (dataset === "female-pelvis") return femalePelvisSearchTerms(id, name);
  if (dataset === "lower-limb-nerve-reference" || dataset === "upper-limb-nerve-reference") {
    const entries = dataset === "upper-limb-nerve-reference" ? upperLimb.labels : lowerLimb.labels;
    const entry = entries.find((label) => label.ids.includes(id));
    const compactTurkish = entry?.side === "left" || entry?.side === "right"
      ? `${entry.side === "left" ? "Sol" : "Sağ"} ${entry.tr.replace(/^(Ayağın |Ayak bileği )/, "")}`
      : entry?.tr;
    const terms = [id, name, ...["tr", "en", "la"].map((language) =>
      datasetLabel(dataset, id, name, language as AnatomyLanguage)), ...(compactTurkish ? [compactTurkish] : []), ...(entry?.aliases ?? [])];
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
