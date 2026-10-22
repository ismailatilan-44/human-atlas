import type { StudyPack } from './study-packs';
import type { StudyStorage } from './study-history';

export const CUSTOM_STUDY_KEY = 'human-atlas.custom-study.v1';
export const MIN_CUSTOM_ITEMS = 4;
export const MAX_SAVED_CUSTOM_STUDIES = 12;

export type CustomStudyPreset = {
  sourcePackId: string;
  sourceVersion: string;
  itemIds: string[];
};
export type CustomStudyLibrary = {
  presets: CustomStudyPreset[];
  writable: boolean;
  notice?: string;
};

/** A deterministic subset of an existing reviewed pack. No new anatomy is authored. */
export function buildCustomStudyPack(base: StudyPack, ids: readonly string[]): StudyPack | undefined {
  if (!Array.isArray(ids) || ids.length < MIN_CUSTOM_ITEMS || ids.length > base.items.length ||
    ids.some(id => typeof id !== 'string') || new Set(ids).size !== ids.length) return;
  const requested = new Set(ids);
  const items = base.items.filter(it => requested.has(it.id));
  if (items.length !== ids.length) return;
  const positions = base.items.flatMap((it, i) => requested.has(it.id) ? [i] : []);
  return {
    ...base,
    id: 'custom.' + base.id + '.' + positions.join('-'),
    title: 'Özel çalışma · ' + base.title,
    scope: base.scope + ' Seçilen ' + items.length + ' mevcut kaynaklı tanıma maddesiyle sınırlıdır.',
    items,
  };
}

export function makeCustomStudyPreset(base: StudyPack, ids: readonly string[]): CustomStudyPreset | undefined {
  const custom = buildCustomStudyPack(base, ids);
  if (!custom) return;
  return { sourcePackId: base.id, sourceVersion: base.version, itemIds: custom.items.map(it => it.id) };
}

export function resolveCustomStudyPreset(preset: CustomStudyPreset, bases: readonly StudyPack[]): StudyPack | undefined {
  const base = bases.find(b => b.id === preset.sourcePackId && b.version === preset.sourceVersion);
  return base ? buildCustomStudyPack(base, preset.itemIds) : undefined;
}

export function loadCustomStudyLibrary(storage: StudyStorage, bases: readonly StudyPack[]): CustomStudyLibrary {
  try {
    const raw = storage.getItem(CUSTOM_STUDY_KEY);
    if (raw === null) return { presets: [], writable: true };
    if (raw.length > 32768) return { presets: [], writable: false, notice: 'Özel set kaydı beklenenden büyük; eski veri korunuyor.' };
    const data: unknown = JSON.parse(raw);
    if (!data || typeof data !== 'object' || Array.isArray(data)) throw Error('shape');
    const value = data as { schema?: unknown; presets?: unknown };
    if (value.schema !== 1 || !Array.isArray(value.presets) || value.presets.length > MAX_SAVED_CUSTOM_STUDIES) throw Error('schema');
    const presets: CustomStudyPreset[] = [];
    for (const entry of value.presets) {
      if (!entry || typeof entry !== 'object' || Array.isArray(entry)) throw Error('entry');
      const p = entry as CustomStudyPreset;
      if (typeof p.sourcePackId !== 'string' || typeof p.sourceVersion !== 'string' ||
        !Array.isArray(p.itemIds) || !p.itemIds.every(id => typeof id === 'string') ||
        !resolveCustomStudyPreset(p, bases)) {
        return { presets: [], writable: false, notice: 'Bazı özel setler eski içerik sürümüne ait veya bozuk. Kayıt değiştirilmedi.' };
      }
      presets.push(p);
    }
    const keys = presets.map(p => resolveCustomStudyPreset(p, bases)?.id);
    if (new Set(keys).size !== keys.length) throw Error('duplicate');
    return { presets, writable: true };
  } catch {
    return { presets: [], writable: false, notice: 'Özel çalışma kaydı okunamadı. Eski veri korunuyor; yeni çalışma geçici yapılabilir.' };
  }
}

export function saveCustomStudyLibrary(storage: StudyStorage, bases: readonly StudyPack[], presets: readonly CustomStudyPreset[]): boolean {
  if (presets.length > MAX_SAVED_CUSTOM_STUDIES || new Set(presets.map(p => resolveCustomStudyPreset(p, bases)?.id)).size !== presets.length ||
    presets.some(p => !resolveCustomStudyPreset(p, bases))) return false;
  try {
    storage.setItem(CUSTOM_STUDY_KEY, JSON.stringify({ schema: 1, presets }));
    return true;
  } catch { return false; }
}
