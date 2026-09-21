/** Resolve packaged assets for root hosting and repository subpaths. */
export function assetUrl(path: string): string {
  if (!path.startsWith("/")) return path;
  const base = (import.meta as ImportMeta & { env: { BASE_URL: string } }).env.BASE_URL;
  return `${base}${path.slice(1)}`;
}
