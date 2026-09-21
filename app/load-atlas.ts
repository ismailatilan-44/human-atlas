import type { Atlas, AtlasAnchor } from "./anatomy";
import { prepareAtlas } from "./atlas-metadata";

export function mergeAtlas(base: Atlas, extension: Atlas): Atlas {
  const partIds = new Set(base.parts.map((p) => p.id));
  const conceptIds = new Set(base.concepts.map((c) => c.id));
  if (
    extension.parts.some((p) => partIds.has(p.id)) ||
    extension.concepts.some((c) => conceptIds.has(c.id))
  ) {
    throw new Error("Ek modelde yinelenen yapı kimliği var.");
  }
  return prepareAtlas({
    ...base,
    parts: [
      ...base.parts,
      ...extension.parts.map((p) => ({ ...p, chunk: p.chunk + base.chunks.length })),
    ],
    concepts: [...base.concepts, ...extension.concepts],
    chunks: [...base.chunks, ...extension.chunks],
    triangles: base.triangles + extension.triangles,
  });
}

export async function loadAtlas(signal: AbortSignal): Promise<Atlas> {
  const [base, extension] = await Promise.all(
    ["/models/atlas.json", "/models/extensions/upper-arm-nerves.json"].map(async (url) => {
      const response = await fetch(url, { signal });
      if (!response.ok) throw new Error("Anatomi kataloğu yüklenemedi. Lütfen yeniden deneyin.");
      return response.json() as Promise<Atlas>;
    }),
  );
  const response = await fetch("/models/extensions/upper-arm-landmarks.json", { signal });
  if (!response.ok) throw new Error("Anatomik işaretler yüklenemedi.");
  const landmarks = (await response.json()) as { anchors: AtlasAnchor[] };
  return { ...mergeAtlas(base, extension), anchors: landmarks.anchors };
}
