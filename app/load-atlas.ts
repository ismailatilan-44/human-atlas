import { assetUrl } from "./asset-url";
import type { Atlas, AtlasAnchor } from "./anatomy";
import { prepareAtlas } from "./atlas-metadata";

export function mergeAtlas(base: Atlas, extension: Atlas): Atlas {
  const partIds = new Set(base.parts.map((p) => p.id));
  const conceptIds = new Set(base.concepts.map((c) => c.id));
  if (
    extension.parts.some((p) => partIds.has(p.id)) ||
    extension.concepts.some(
      (c) => conceptIds.has(c.id) && !extension.extendsConceptIds?.includes(c.id),
    )
  ) {
    throw new Error("Ek modelde yinelenen yapı kimliği var.");
  }
  const concepts = new Map(base.concepts.map((c) => [c.id, c]));
  for (const concept of extension.concepts) {
    const previous = concepts.get(concept.id);
    concepts.set(concept.id, {
      ...concept,
      elements: [...new Set([...(previous?.elements ?? []), ...concept.elements])],
    });
  }
  return prepareAtlas({
    ...base,
    parts: [
      ...base.parts,
      ...extension.parts.map((p) => ({
        ...p,
        chunk: p.chunk + base.chunks.length,
        sourceUrl: typeof extension.source === "object" ? extension.source.url : undefined,
      })),
    ],
    concepts: [...concepts.values()],
    chunks: [...base.chunks, ...extension.chunks],
    triangles: base.triangles + extension.triangles,
  });
}

export async function loadAtlas(signal: AbortSignal): Promise<Atlas> {
  async function read<T>(url: string): Promise<T> {
    const response = await fetch(assetUrl(url), { signal });
    if (!response.ok) throw new Error("Anatomi verisi yüklenemedi. Lütfen yeniden deneyin.");
    return response.json() as Promise<T>;
  }
  const [base, registry] = await Promise.all([
    read<Atlas>("/models/atlas.json"),
    read<{ manifests: string[]; landmarks: string[] }>("/models/extensions/index.json"),
  ]);
  const [extensions, landmarks] = await Promise.all([
    Promise.all(registry.manifests.map((url) => read<Atlas>(url))),
    Promise.all(registry.landmarks.map((url) => read<{ anchors: AtlasAnchor[] }>(url))),
  ]);
  return {
    ...extensions.reduce(mergeAtlas, prepareAtlas(base)),
    anchors: landmarks.flatMap((p) => p.anchors),
  };
}
