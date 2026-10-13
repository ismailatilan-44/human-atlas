import pack from '../data/study/whole-skull-v1.json';
import type { SceneState, View } from './anatomy';
export const SKULL_GROUP = 'atlas:skull-bones';
export const skullItems = pack.items;
export const skullParts = skullItems.map(item => item.geometryPartId);
export const skullViews: { id: View; label: string }[] = [
  { id: 'three-quarter', label: 'Çapraz' }, { id: 'front', label: 'Önden' },
  { id: 'back', label: 'Arkadan' }, { id: 'side', label: 'Soldan' },
  { id: 'right', label: 'Sağdan' }, { id: 'superior', label: 'Üstten' },
  { id: 'inferior', label: 'Alttan' },
];
export const skullItem = (id?: string) => skullItems.find(item => item.conceptId === id);
export function skullDescription(id?: string): string {
  const item = skullItem(id);
  if (!item) return '8 kranial ve 14 yüz kemiği. Dişler, hyoid ve işitme kemikçikleri bu 22 kemiklik çalışma grubunda değildir.';
  return `${item.description} ${item.boneClass === 'cranial' ? 'Kranial' : 'Yüz'} kemiği · ${item.side === 'left' ? 'bireyin solu' : item.side === 'right' ? 'bireyin sağı' : 'eşleşmemiş tek kemik'}.`;
}
/** One fixed educational displacement, independent of camera/selection; never edits source geometry. */
export function skullOffset(partId: string, separated?: string): [number, number, number] {
  if (partId !== separated) return [0, 0, 0];
  const item = skullItems.find(item => item.geometryPartId === partId);
  return [item?.side === 'right' ? -0.18 : 0.18, 0, 0.12];
}
export function skullStart(state: SceneState): SceneState {
  return { ...state, skull: {}, selected: [...skullParts], visible: ['skeletal'], hidden: [],
    focused: false, isolate: false, explode: 0, ghost: false, rotate: false,
    view: 'three-quarter', reset: state.reset + 1, anchor: undefined, restoreCamera: undefined };
}
