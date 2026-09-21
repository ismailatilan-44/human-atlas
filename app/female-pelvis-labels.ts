import type { Concept } from "./anatomy";
import type { AnatomyLanguage } from "./atlas-metadata";

type Labels = Record<AnatomyLanguage, string>;
// Dataset-scoped display translations, never an ontology or geometry remapping.
// Latin anatomical terms checked against FIPAT; composed source-region labels
// (junction, lower segment, bone tissue) are descriptive display labels.
// https://ifaa.unifr.ch/Public/EntryPage/TA98%20Tree/TA98%20EN/09.1.03%20TA98%20EN.htm
// https://fipat.library.dal.ca/wp-content/uploads/2021/08/FIPAT-TA2-Errata.pdf
const labels: Record<string, Labels> = {};
function add(key: string, tr: string, en: string, la: string) {
  labels[`hra-female:${key}`] = { tr, en, la };
}
add(
  "VH_F_cervicovaginal_junction",
  "Rahim ağzı–vajina birleşimi",
  "Cervicovaginal junction",
  "Junctio cervicovaginalis",
);
add(
  "VH_F_abdominal_ostium_of_uterine_tube",
  "Rahim tüpünün karın ağzı",
  "Abdominal ostium of uterine tube",
  "Ostium abdominale tubae uterinae",
);
add("VH_F_body_of_uterus", "Rahim gövdesi", "Body of uterus", "Corpus uteri");
add("VH_F_fundus_of_uterus", "Rahim fundusu", "Fundus of uterus", "Fundus uteri");
// The source does not identify a side or separate the two cornua/ostia.
add("VH_F_cornua", "Boynuzlar (cornua; kaynak adı)", "Cornua (source name)", "Cornua");
add(
  "VH_F_lower_uterine_segment",
  "Rahmin alt segmenti",
  "Lower uterine segment",
  "Segmentum inferius uteri",
);
add(
  "VH_F_posterior_wall_of_uterus",
  "Rahmin arka duvarı",
  "Posterior wall of uterus",
  "Paries posterior uteri",
);
add(
  "VH_F_anterior_wall_of_uterus",
  "Rahmin ön duvarı",
  "Anterior wall of uterus",
  "Paries anterior uteri",
);
add("VH_F_cervix", "Rahim ağzı (serviks)", "Cervix", "Cervix uteri");
add(
  "VH_F_internal_cervical_os",
  "Rahim ağzının iç açıklığı",
  "Internal cervical os",
  "Ostium internum uteri",
);
add(
  "VH_F_external_cervical_os",
  "Rahim ağzının dış açıklığı",
  "External cervical os",
  "Ostium externum uteri",
);
add("VH_F_left_ovary", "Sol yumurtalık", "Left ovary", "Ovarium sinistrum");
add("VH_F_right_ovary", "Sağ yumurtalık", "Right ovary", "Ovarium dextrum");
add("VH_F_sacrum", "Sakrum (sağrı kemiği)", "Sacrum", "Os sacrum");
add("VH_F_coccyx", "Koksiks (kuyruk sokumu kemiği)", "Coccyx", "Os coccygis");
for (const [bone, tr, la] of [
  ["pubis", "Pubis", "Os pubis"],
  ["ilium", "İlium", "Os ilium"],
  ["ischium", "İskiyum", "Os ischii"],
]) {
  for (const [side, trSide, enSide] of [
    ["L", "Sol", "Left"],
    ["R", "Sağ", "Right"],
  ]) {
    for (const [tissue, trTissue, laTissue] of [
      ["spongy", "süngerimsi kemik", "substantia spongiosa"],
      ["compact", "kompakt kemik", "substantia compacta"],
    ]) {
      add(
        `VH_F_${bone}_${tissue}_bone_${side}`,
        `${trSide} ${tr.toLocaleLowerCase("tr")} — ${trTissue}`,
        `${enSide} ${bone} — ${tissue} bone`,
        `${la} (${side}) — ${laTissue}`,
      );
    }
  }
}
add("uterus-female", "Rahim", "Uterus", "Uterus");
add("pelvis-female", "Kemik pelvis", "Bony pelvis", "Pelvis ossea");
labels["hra-female:ovary-female-left"] = labels["hra-female:VH_F_left_ovary"];
labels["hra-female:ovary-female-right"] = labels["hra-female:VH_F_right_ovary"];

export function femalePelvisLabel(id: string, fallback: string, language: AnatomyLanguage): string {
  return labels[id]?.[language] ?? fallback;
}

export function femalePelvisSearchTerms(id: string, sourceName: string): string[] {
  const entry = labels[id];
  const terms = [id, sourceName, ...Object.values(entry ?? {})];
  // Keep both original IDs searchable when an ovary alias is deduplicated.
  if (id === "hra-female:VH_F_left_ovary") terms.push("hra-female:ovary-female-left", "FMA:7214");
  if (id === "hra-female:VH_F_right_ovary") terms.push("hra-female:ovary-female-right", "FMA:7213");
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

/** Same exact surface set: prefer its FMA-tagged source node, keeping its ID. */
export function femalePelvisConcepts(concepts: Concept[]): Concept[] {
  const surfaces = new Map<string, Concept>();
  const isFma = (concept: Concept) =>
    /^FMA[:_]?\d+$/i.test(
      (concept as Concept & { sourceOntologyId?: string }).sourceOntologyId ?? "",
    );
  for (const concept of concepts) {
    const key = concept.elements.length ? [...concept.elements].sort().join("\u0000") : concept.id;
    const previous = surfaces.get(key);
    if (!previous || (isFma(concept) && !isFma(previous))) surfaces.set(key, concept);
  }
  return [...surfaces.values()];
}
