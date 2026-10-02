import type { Atlas, CameraPose, Concept, DatasetId, SceneState } from './anatomy';

export const SCENE_STORAGE_KEY = 'human-atlas.saved-scenes.v1';
export const MAX_SAVED_SCENES = 12;
// Increment if authored labels/relationships change without manifest changes.
const SEMANTIC_REVISION = 'atlas-content-b877954-2026-10-02';
export interface SavedScene {
  schema: 1; id: string; name: string; savedAt: string;
  dataset: DatasetId; contentVersion: string; chosenId: string | null;
  language: 'tr' | 'en' | 'la'; details: boolean;
  camera: CameraPose | null; state: SceneState;
}
export interface SceneStorage { getItem(key: string): string | null; setItem(key: string, value: string): void }
export interface SceneStoreResult { scenes: SavedScene[]; error: string | null; recovered: boolean }
const datasets = ['male-body', 'female-pelvis', 'inner-ear-reference', 'lower-limb-nerve-reference', 'upper-limb-nerve-reference'];
const systems = ['skeletal', 'muscular', 'arterial', 'venous', 'nervous', 'digestive', 'respiratory', 'urinary', 'reproductive', 'lymphatic', 'endocrine', 'integumentary', 'connective', 'sensory', 'cardiac'];
const record = (v: unknown): v is Record<string, unknown> => !!v && typeof v === 'object' && !Array.isArray(v);
const finite = (v: unknown): v is number => typeof v === 'number' && Number.isFinite(v) && Math.abs(v) < 1e9;
const strings = (v: unknown): v is string[] => Array.isArray(v) && v.length <= 10000 && v.every(x => typeof x === 'string' && x.length < 300) && new Set(v).size === v.length;
const vector = (v: unknown) => Array.isArray(v) && v.length === 3 && v.every(finite);
function cameraValid(v: unknown): boolean {
  if (v === null) return true;
  if (!record(v) || !vector(v.position) || !vector(v.target)) return false;
  if ((v.position as number[]).every((n, i) => n === (v.target as number[])[i])) return false;
  return v.viewOffset === null || (record(v.viewOffset) && ['fullWidth','fullHeight','offsetX','offsetY','width','height'].every(k => finite((v.viewOffset as Record<string, unknown>)[k])) && ['fullWidth','fullHeight','width','height'].every(k => (v.viewOffset as Record<string, number>)[k] > 0));
}
export function isSavedScene(v: unknown): v is SavedScene {
  if (!record(v) || v.schema !== 1 || typeof v.id !== 'string' || !v.id || v.id.length > 100 || typeof v.name !== 'string' || !v.name.trim() || v.name.length > 80 || typeof v.savedAt !== 'string' || !Number.isFinite(Date.parse(v.savedAt)) || !datasets.includes(v.dataset as string) || typeof v.contentVersion !== 'string' || !v.contentVersion || v.contentVersion.length > 200 || (v.chosenId !== null && typeof v.chosenId !== 'string') || !['tr','en','la'].includes(v.language as string) || typeof v.details !== 'boolean' || !cameraValid(v.camera) || !record(v.state)) return false;
  const s = v.state;
  return finite(s.explode) && s.explode >= 0 && s.explode <= 1 && strings(s.visible) && s.visible.every(x => systems.includes(x)) && strings(s.selected) && strings(s.hidden) && ['three-quarter','front','back','side'].includes(s.view as string) && ['isolate','rotate','focused','ghost','concealLabels'].every(k => typeof s[k] === 'boolean') && s.reset === 0 && s.anchor === undefined && s.restoreCamera === undefined;
}
/** Fingerprint the loaded, merged manifest; stable across camera/UI changes. */
export function sceneContentVersion(atlas: Atlas): string {
  const input = JSON.stringify([SEMANTIC_REVISION, atlas.version, atlas.parts, atlas.concepts, atlas.chunks, atlas.anchors]);
  let hash = 2166136261;
  for (let i = 0; i < input.length; i++) hash = Math.imul(hash ^ input.charCodeAt(i), 16777619);
  return `${SEMANTIC_REVISION}:${(hash >>> 0).toString(16)}`;
}
export function captureScene(input: { atlas: Atlas; dataset: DatasetId; state: SceneState; camera: CameraPose | null; chosenId: string | null; details: boolean; language: SavedScene['language']; name: string }, now = new Date(), id = `${Date.now()}-${Math.random().toString(36).slice(2)}`): SavedScene {
  const s = input.state;
  const scene: SavedScene = { schema: 1, id, name: input.name.trim().slice(0,80) || 'Kayıtlı sahne', savedAt: now.toISOString(), dataset: input.dataset, contentVersion: sceneContentVersion(input.atlas), chosenId: input.chosenId, language: input.language, details: input.details, camera: input.camera,
    state: { explode: s.explode, visible: [...s.visible], selected: [...s.selected], hidden: [...(s.hidden ?? [])], isolate: s.isolate, view: s.view, rotate: s.rotate, focused: !!s.focused, ghost: !!s.ghost, concealLabels: !!s.concealLabels, reset: 0 } };
  return JSON.parse(JSON.stringify(scene)) as SavedScene;
}
export function validateScene(scene: SavedScene, atlas: Atlas, concepts: Map<string, Concept>): string | null {
  if (!isSavedScene(scene)) return 'Sahne biçimi geçersiz; kayıt uygulanmadı.';
  const dataset = atlas.datasetId ?? (atlas.sex === 'female' ? 'female-pelvis' : 'male-body');
  if (scene.dataset !== dataset) return 'Sahne başka bir referansa ait.';
  if (scene.contentVersion !== sceneContentVersion(atlas)) return 'Model içerik sürümü değişmiş; eski sahne uygulanmadı. Kaydı silip yeni bir sahne kaydedebilirsiniz.';
  const ids = new Set(atlas.parts.map(p => p.id));
  if ([...scene.state.selected, ...(scene.state.hidden ?? [])].some(id => !ids.has(id)) || (scene.chosenId !== null && !concepts.has(scene.chosenId))) return 'Kayıttaki yapı kimliği artık bulunamıyor; sahne uygulanmadı.';
  return null;
}
function parse(raw: string): SavedScene[] {
  if (raw.length > 2_000_000) throw new Error('oversized');
  const v: unknown = JSON.parse(raw);
  if (!record(v) || v.schema !== 1 || !Array.isArray(v.scenes) || v.scenes.length > MAX_SAVED_SCENES || !v.scenes.every(isSavedScene) || new Set(v.scenes.map(s => s.id)).size !== v.scenes.length) throw new Error('invalid');
  return v.scenes;
}
export function loadSceneStore(storage: SceneStorage): SceneStoreResult {
  try {
    const raw = storage.getItem(SCENE_STORAGE_KEY);
    if (raw === null) return { scenes: [], error: null, recovered: false };
    try { return { scenes: parse(raw), error: null, recovered: false }; }
    catch {
      const backup = storage.getItem(`${SCENE_STORAGE_KEY}.backup`);
      if (backup) { try { return { scenes: parse(backup), recovered: true, error: 'Ana kayıt okunamadı; son sağlam yedek açıldı. Tekrar kaydetmek bu yedeği korur.' }; } catch { /* preserve unreadable data */ } }
      return { scenes: [], recovered: false, error: 'Kayıt okunamadı. Yeni bir sahne kaydetmek önceki bozuk veriyi kurtarma kopyasında korur.' };
    }
  } catch { return { scenes: [], recovered: false, error: 'Tarayıcı depolamasına erişilemiyor. Kayıtlar bu oturumda kaydedilemez.' }; }
}
export function writeSceneStore(storage: SceneStorage, scenes: SavedScene[]): string | null {
  try {
    const serialized = JSON.stringify({ schema: 1, scenes });
    parse(serialized);
    const previous = storage.getItem(SCENE_STORAGE_KEY);
    if (previous !== null) {
      let valid = true; try { parse(previous); } catch { valid = false; }
      storage.setItem(`${SCENE_STORAGE_KEY}.${valid ? 'backup' : 'recovery'}`, previous);
    }
    storage.setItem(SCENE_STORAGE_KEY, serialized);
    return null;
  } catch { return 'Kaydedilemedi: tarayıcı depolaması dolu veya erişim kapalı. Mevcut kayıt korunur; alan açıp tekrar deneyin.'; }
}
