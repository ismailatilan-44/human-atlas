import type { StudySession } from './study-session';

export type StudyIdentity = { id: string; datasetId: string; version: string; items: { id: string; conceptId: string }[] };
export type ReviewOutcome = 'correct' | 'wrong' | 'hint' | 'skip';
export type ReviewCard = { due: number; last: number; streak: number; reviews: number };
export type ReviewEvent = { id: string; itemId: string; at: number; outcome: ReviewOutcome };
export type LearnerHistory = {
  schema: 1; identity: string; cards: Record<string, ReviewCard>; events: ReviewEvent[];
  session: StudySession; isolated: boolean; sessionId: string;
  undo?: LearnerHistory;
  completed: { at: number; firstCorrect: number; successful: number; total: number }[];
};
const DAY = 86400000;
const intervals = [DAY, 3 * DAY, 7 * DAY, 14 * DAY, 30 * DAY];
export function studyIdentity(pack: StudyIdentity): string {
  return JSON.stringify(pack);
}
export function newHistory(pack: StudyIdentity, session: StudySession, now: number): LearnerHistory {
  return { schema: 1, identity: studyIdentity(pack), cards: {}, events: [], session, isolated: false,
    sessionId: `${now}-${Math.random().toString(36).slice(2)}`, completed: [] };
}
/** UTC epoch milliseconds; early practice cannot accelerate a scheduled interval. No clinical mastery claim. */
export function review(history: LearnerHistory, event: ReviewEvent): LearnerHistory {
  if (history.events.some(e => e.id === event.id) || !Number.isFinite(event.at) || event.at < 0 || event.at > 8e15) return history;
  const old = history.cards[event.itemId];
  const at = Math.max(event.at, old?.last ?? 0, history.events[history.events.length - 1]?.at ?? 0);
  let card: ReviewCard;
  if (event.outcome === 'skip') card = old ?? { due: at, last: at, streak: 0, reviews: 0 };
  else if (event.outcome !== 'correct') card = { due: at + 600000, last: at, streak: 0, reviews: (old?.reviews ?? 0) + 1 };
  else if (old && at < old.due) card = { ...old, last: at };
  else {
    const streak = Math.min((old?.streak ?? 0) + 1, intervals.length);
    card = { due: at + intervals[streak - 1], last: at, streak, reviews: (old?.reviews ?? 0) + 1 };
  }
  return { ...history, cards: { ...history.cards, [event.itemId]: card }, events: [...history.events, { ...event, at }].slice(-500) };
}
export function dueItems(history: LearnerHistory, pack: StudyIdentity, now: number): number[] {
  return pack.items.flatMap((it, i) => !history.cards[it.id] || history.cards[it.id].due <= now ? [i] : []);
}
export interface StudyStorage { getItem(key: string): string | null; setItem(key: string, value: string): void }
export const studyStorageKey = (pack: StudyIdentity) => `human-atlas.study.v1:${pack.id}`;
export function validateHistory(value: unknown, pack: StudyIdentity): value is LearnerHistory {
  if (!value || typeof value !== 'object') return false;
  if (typeof pack.version !== 'string' || !pack.version) return false;
  const h = value as LearnerHistory, n = pack.items.length, ids = new Set(pack.items.map(i => i.id));
  const index = (i: unknown) => Number.isInteger(i) && Number(i) >= 0 && Number(i) < n;
  const time = (t: unknown) => typeof t === 'number' && Number.isFinite(t) && t >= 0 && t <= 8e15;
  const s = h.session;
  if (h.schema !== 1 || h.identity !== studyIdentity(pack) || !s || !['inspect','recall','feedback','summary'].includes(s.phase)
    || !Array.isArray(s.queue) || !s.queue.length || !s.queue.every(index) || new Set(s.queue).size !== s.queue.length
    || !Number.isInteger(s.index) || s.index < 0 || s.index >= s.queue.length || typeof s.retry !== 'boolean'
    || !s.first || typeof s.first !== 'object' || Array.isArray(s.first) || !Object.entries(s.first).every(([k,v]) => index(Number(k)) && ['correct','wrong','skip'].includes(v))
    || !Array.isArray(s.success) || !s.success.every(index) || new Set(s.success).size !== s.success.length
    || (s.answer !== undefined && s.answer !== null && !pack.items.some(i => i.conceptId === s.answer))
    || (s.hinted !== undefined && typeof s.hinted !== 'boolean')
    || typeof h.sessionId !== 'string' || typeof h.isolated !== 'boolean' || !h.cards || typeof h.cards !== 'object' || Array.isArray(h.cards)
    || !Object.entries(h.cards).every(([id,c]) => ids.has(id) && c && time(c.due) && time(c.last) && Number.isInteger(c.streak) && c.streak >= 0 && c.streak <= 5 && Number.isInteger(c.reviews) && c.reviews >= 0)
    || !Array.isArray(h.events) || h.events.length > 500 || !h.events.every(e => e && typeof e.id === 'string' && ids.has(e.itemId) && time(e.at) && ['correct','wrong','hint','skip'].includes(e.outcome))
    || !Array.isArray(h.completed) || h.completed.length > 50 || !h.completed.every(c => c && time(c.at) && [c.firstCorrect,c.successful,c.total].every(v => Number.isInteger(v) && v >= 0 && v <= n))) return false;
  if (h.undo && (h.undo.undo || !validateHistory(h.undo, pack))) return false;
  return true;
}
export function loadStudy(storage: StudyStorage, pack: StudyIdentity): { history?: LearnerHistory; notice?: string } {
  const key = studyStorageKey(pack);
  try {
    const raw = storage.getItem(key);
    if (raw === null) return {};
    try { const h: unknown = JSON.parse(raw); if (validateHistory(h, pack)) return { history: h }; } catch { /* Try backup. */ }
    const backup = storage.getItem(`${key}:backup`);
    if (backup) try { const h: unknown = JSON.parse(backup); if (validateHistory(h, pack)) return { history: h, notice: 'Bozuk kayıt yerine son sağlam yedek açıldı.' }; } catch { /* Preserve rejected data. */ }
    return { notice: 'Kayıt bozuk, eski içerik sürümüne ait veya kimlikleri değişmiş. Eski veri korunur; yeni oturum açıldı.' };
  } catch { return { notice: 'Yerel depolama kullanılamıyor. Bu oturum bellekte devam ediyor.' }; }
}
export function saveStudy(storage: StudyStorage, pack: StudyIdentity, history: LearnerHistory): boolean {
  const key = studyStorageKey(pack);
  try {
    const previous = storage.getItem(key);
    if (previous) {
      let valid = false;
      try { valid = validateHistory(JSON.parse(previous), pack); } catch { /* Archive corrupt data. */ }
      storage.setItem(valid ? `${key}:backup` : `${key}:recovery`, previous);
    }
    storage.setItem(key, JSON.stringify(history)); return true;
  } catch { return false; }
}
