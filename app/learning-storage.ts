/** QA sessions never read or write real learner keys. Production folds to native storage. */
export function fixtureMode(): boolean {
  return import.meta.env.DEV && typeof location !== 'undefined'
    && ['localhost', '127.0.0.1', '[::1]'].includes(location.hostname)
    && new URLSearchParams(location.search).get('devqa') === '1';
}
export function learningStorage(): Pick<Storage, 'getItem' | 'setItem'> {
  const storage = window.localStorage;
  if (import.meta.env.DEV && fixtureMode()) return {
    getItem: key => storage.getItem(`atlas-devqa-sandbox:${key}`),
    setItem: (key, value) => storage.setItem(`atlas-devqa-sandbox:${key}`, value),
  };
  return storage;
}

/** Bounded clock offset exists only in the local QA sandbox. */
export function studyNow(): number {
  if (import.meta.env.DEV && fixtureMode()) {
    try { const offset = Number(learningStorage().getItem('clock') ?? 0);
      if (Number.isFinite(offset) && offset >= 0 && offset <= 31 * 86400000) return Date.now() + offset;
    } catch { /* Real clock remains usable without persistence. */ }
  }
  return Date.now();
}
