import { useEffect, useRef, useState } from 'react';
import type { Atlas, CameraPose, DatasetId, SceneState } from './anatomy';
import { fixtureMode, learningStorage, studyNow } from './learning-storage';
import { studyPacks, type StudyPack } from './study-packs';
import type { StudyDiagnostics } from './study-panel';
import { startStudy } from './study-session';
import { loadStudy, newHistory, saveStudy } from './study-history';
import { captureScene, loadSceneStore, sceneContentVersion, writeSceneStore, type SavedScene } from './saved-scenes';
import './dev-qa.css';

type State = { liveStudy: StudyDiagnostics | null; atlas: Atlas | null; dataset: DatasetId; state: SceneState; chosenId: string | null;
  language: SavedScene['language']; camera: CameraPose | null; progress: number; error: string;
  studying: boolean; activePack: StudyPack; historySize: number;
  pending: { pack: string | null; scene: string | null; returning: boolean } };
type Controls = { explode: (value: 0 | 1) => void; slowLoad: (value: boolean) => void; study: (pack: StudyPack) => void; reference: (id: DatasetId) => void;
  exit: () => void; select: (id: string) => void; language: (language: SavedScene['language']) => void;
  isolate: () => void; restore: (scene: SavedScene) => void };
type Scenario = 'right' | 'left' | 'upper' | 'scene' | 'race' | 'context-loss' | 'dismiss' | 'exploded' | 'due';
type Entry = { sequence: number; action: string; expected: string; actual: string; result: 'PASS' | 'FAIL' | 'OBSERVE' };
const prefix = 'atlas-devqa-sandbox:';
const journalKey = `${prefix}journal`;
const resumeKey = `${prefix}resume`;
const scenarios: Record<Scenario, string> = { right: 'Right ankle / wrong → undo', left: 'Left ankle / wrong → undo', upper: 'Upper limb / wrong → undo', scene: 'Saved scene / reference restore', race: 'Rapid reference return regression', 'context-loss': 'WebGL loss / study safety', dismiss: 'Dismiss pending module / delayed load', exploded: 'Exploded camera restore', due: 'Due schedule / clock and focus' };
const pause = (ms: number) => new Promise<void>(resolve => window.setTimeout(resolve, ms));
export default function DevQaPanel({ read, controls }: { read: () => State; controls: Controls }) {
  const enabled = import.meta.env.DEV && fixtureMode();
  const current = useRef({ read, controls }); current.current = { read, controls };
  const [open, setOpen] = useState(true), [busy, setBusy] = useState(false);
  const [scenario, setScenario] = useState<Scenario>('upper');
  const [snapshot, setSnapshot] = useState<object>({});
  const [entries, setEntries] = useState<Entry[]>([]);
  const [notice, setNotice] = useState('Fixture storage only. Start and replay preserve the journal; Reset clears only this sandbox.');
  const cancel = useRef(false);
  const version = useRef<{ atlas: Atlas | null; value: string | null }>({ atlas: null, value: null });
  function observe() {
    const s = current.current.read();
    if (s.atlas !== version.current.atlas) version.current = { atlas: s.atlas, value: s.atlas ? sceneContentVersion(s.atlas) : null };
    let persistence: object;
    try {
      const store = learningStorage();
      const loaded = loadStudy(store, s.activePack);
      const live = s.studying && s.liveStudy?.module === s.activePack.id ? s.liveStudy : null;
      const h = live?.history ?? loaded.history;
      const scenes = loadSceneStore(store);
      persistence = { health: live?.persistence ?? loaded.notice ?? scenes.error ?? 'readable', observed: live ? 'live' : 'stored', storedPhase: loaded.history?.session.phase ?? null, sceneCount: scenes.scenes.length,
        phase: s.studying ? h?.session.phase ?? 'initializing' : 'inactive', module: s.studying ? s.activePack.id : null,
        retry: h?.session.retry ?? false, firstAttempt: h?.session.first ?? {}, eventualCorrect: h?.session.success ?? [],
        undo: !!h?.undo, completedRounds: h?.completed.length ?? 0, reviewEvents: h?.events.length ?? 0,
        reviewSchedule: h?.cards ?? {} };
    } catch { persistence = { health: 'unavailable' }; }
    return { reference: s.dataset, loadedReference: s.atlas?.datasetId, sourceVersion: version.current.value,
      conceptId: s.chosenId, camera: s.camera, visibility: { systems: s.state.visible, hidden: s.state.hidden, selected: s.state.selected, isolate: s.state.isolate, ghost: s.state.ghost },
      language: s.language, viewMode: s.state.view, progress: s.progress, error: s.error,
      explorerHistory: s.historySize, pending: s.pending, study: persistence };
  }
  function record(action: string, expected: string, actual: unknown, result: Entry['result'] = 'PASS') {
    const safe = JSON.stringify(actual).slice(0, 1000);
    setEntries(previous => {
      const next = [...previous, { sequence: (previous.at(-1)?.sequence ?? 0) + 1, action, expected, actual: safe, result }].slice(-80);
      try { localStorage.setItem(journalKey, JSON.stringify(next)); } catch { setNotice('Sandbox journal persistence failed.'); }
      return next;
    });
  }
  async function until(label: string, predicate: () => boolean) {
    for (let i = 0; i < 200; i++) {
      if (cancel.current) throw new Error('Cancelled');
      if (predicate()) { await pause(180); return; }
      await pause(100);
    }
    throw new Error(`Timed out: ${label}`);
  }
  const loaded = (id: DatasetId) => { const s = current.current.read(); return s.dataset === id && s.atlas?.datasetId === id && s.progress === 100; };
  function click(label: string) {
    const panel = document.querySelector('[aria-label="Bölgesel çalışma"]');
    const button = [...(panel?.querySelectorAll('button') ?? [])].find(b => b.textContent?.trim() === label);
    if (!button || button.disabled) throw new Error(`Visible study control unavailable: ${label}`);
    button.click();
  }
  function history(pack: StudyPack) { return loadStudy(learningStorage(), pack).history; }
  async function launch(pack: StudyPack) {
    if (current.current.read().studying) { current.current.controls.exit(); await pause(250); }
    current.current.controls.study(pack);
    await until('study model ready', () => loaded(pack.datasetId) && current.current.read().studying);
  }
  async function run(which: Scenario) {
    if (!enabled || busy) return;
    cancel.current = false; setBusy(true);
    record('scenario start', scenarios[which], { scenario: which }, 'OBSERVE');
    try {
      if (which === 'due') {
        if (current.current.read().studying) { current.current.controls.exit(); await pause(250); }
        learningStorage().setItem('clock', '0');
        const pack = studyPacks[2], now = studyNow();
        const h = newHistory(pack, startStudy(pack.items.length), now);
        h.session.phase = 'summary';
        h.session.first = Object.fromEntries(pack.items.map((_, i) => [i, 'wrong']));
        h.cards = Object.fromEntries(pack.items.map(it => [it.id, { due: now + 600000, last: now, streak: 0, reviews: 1 }]));
        if (!saveStudy(learningStorage(), pack, h)) throw new Error('Fixture history write failed');
        await launch(pack);
        const dueButton = () => [...document.querySelectorAll<HTMLButtonElement>('[aria-label="Bölgesel çalışma"] button')].find(b => b.textContent?.startsWith('Zamanı gelenleri çalış'));
        await until('no items initially due', () => !!dueButton()?.disabled);
        learningStorage().setItem('clock', '660000'); window.dispatchEvent(new Event('focus'));
        await pause(500);
        const actual = { label: dueButton()?.textContent, disabled: dueButton()?.disabled };
        record('clock +11 minutes / focus', '5 due items; review button enabled', actual, actual.disabled === false ? 'PASS' : 'FAIL');
        if (actual.disabled !== false) throw new Error('Due button stale after clock/focus');
      } else if (which === 'exploded') {
        if (current.current.read().studying) { current.current.controls.exit(); await pause(250); }
        current.current.controls.reference('upper-limb-nerve-reference');
        await until('upper model ready', () => loaded('upper-limb-nerve-reference'));
        current.current.controls.explode(1); await pause(1800);
        const s = current.current.read();
        const saved = captureScene({ ...s, atlas: s.atlas!, details: false, name: 'DEV exploded fixture' });
        if (!saved.camera) throw new Error('Camera unavailable');
        saved.camera.position[0] += 0.2; saved.camera.target[0] += 0.2;
        current.current.controls.restore(saved); await pause(500);
        current.current.controls.explode(0); await pause(1800);
        current.current.controls.restore(saved); await pause(1800);
        const actual = current.current.read().camera;
        const delta = actual ? Math.max(...actual.position.map((v, i) => Math.abs(v - saved.camera!.position[i])), ...actual.target.map((v, i) => Math.abs(v - saved.camera!.target[i]))) : Infinity;
        record('exploded restore after assembly', 'saved camera retained after animation; delta < 0.001', { expected: saved.camera, actual, delta }, delta < 0.001 ? 'PASS' : 'FAIL');
        if (delta >= 0.001) throw new Error('Animated autofit replaced saved camera');
      } else if (which === 'dismiss') {
        if (current.current.read().studying) { current.current.controls.exit(); await pause(250); }
        current.current.controls.reference('male-body');
        await until('male reference ready', () => loaded('male-body'));
        current.current.controls.slowLoad(true);
        const toggle = [...document.querySelectorAll('button')].find(b => b.textContent === 'Çalışma ve tekrar');
        if (!toggle) throw new Error('Module picker toggle missing');
        toggle.click(); await pause(100);
        const picker = document.querySelector('[aria-label="Çalışma modülleri"]');
        const start = [...(picker?.querySelectorAll('button') ?? [])].find(b => b.textContent?.includes('5 yapı'));
        if (!start) throw new Error('Upper module start missing');
        start.click(); await pause(100); toggle.click();
        await until('delayed load settled', () => loaded('upper-limb-nerve-reference'));
        await pause(300);
        const s = current.current.read();
        record('dismiss pending module', 'picker closed; no study or queued pack', { studying: s.studying, pending: s.pending }, !s.studying && !s.pending.pack ? 'PASS' : 'FAIL');
        if (s.studying || s.pending.pack) throw new Error('Dismissed module launched after delayed load');
      } else if (which === 'context-loss') {
        await launch(studyPacks[2]); click('Yeni çalışma'); await pause(200);
        for (let i = 0; i < studyPacks[2].items.length; i++) { click(i === studyPacks[2].items.length - 1 ? 'Hatırlamayı başlat' : 'Sonraki'); await pause(200); }
        await until('recall before context loss', () => history(studyPacks[2])?.session.phase === 'recall');
        if (document.querySelectorAll('.study-answers button:not(:disabled)').length !== 5) throw new Error('Expected five enabled answers before loss');
        const canvas = document.querySelector('canvas');
        const gl = canvas?.getContext('webgl2') ?? canvas?.getContext('webgl');
        const extension = gl?.getExtension('WEBGL_lose_context');
        if (!extension) throw new Error('WEBGL_lose_context unavailable');
        const before = JSON.stringify(history(studyPacks[2])?.session);
        extension.loseContext();
        await until('context loss reported', () => !!current.current.read().error);
        const alert = document.querySelector('[role="alert"]');
        const activeAnswers = [...document.querySelectorAll('.study-answers button')].filter(b => !b.matches(':disabled')).length;
        record('WebGL context loss observation', 'visible alert and zero enabled answer buttons', { alert: alert?.textContent ?? null, activeAnswers }, alert && activeAnswers === 0 ? 'PASS' : 'FAIL');
        if (!alert || activeAnswers) throw new Error('Study remains answerable without visible rendering failure');
        if (before !== JSON.stringify(history(studyPacks[2])?.session)) throw new Error('Loss changed scoring');
      } else if (which === 'scene' || which === 'race') {
        const pack = studyPacks[1];
        if (current.current.read().studying) { current.current.controls.exit(); await pause(250); }
        current.current.controls.reference(pack.datasetId);
        await until('lower reference', () => loaded(pack.datasetId));
        current.current.controls.select(pack.items[0].conceptId);
        current.current.controls.language('la'); current.current.controls.isolate();
        await pause(500);
        const s = current.current.read();
        const saved = captureScene({ ...s, atlas: s.atlas!, details: true, name: 'DEV QA fixture' });
        const error = writeSceneStore(learningStorage(), [saved]);
        if (error) throw new Error(error);
        record('save visible scene', 'Latin isolated source concept and camera', { concept: saved.chosenId, camera: saved.camera });
        if (which === 'scene') {
          current.current.controls.reference('upper-limb-nerve-reference');
          await until('upper reference', () => loaded('upper-limb-nerve-reference'));
          const restored = loadSceneStore(learningStorage()).scenes[0];
          current.current.controls.restore(restored);
          await until('restore', () => loaded(saved.dataset) && current.current.read().chosenId === saved.chosenId);
          const actual = current.current.read();
          if (actual.language !== 'la' || !actual.state.isolate) throw new Error('Scene visibility/language mismatch');
          await pause(500);
          const pose = current.current.read().camera;
          if (!pose || !saved.camera || Math.max(...pose.position.map((v, i) => Math.abs(v - saved.camera!.position[i])), ...pose.target.map((v, i) => Math.abs(v - saved.camera!.target[i]))) >= 0.001) throw new Error('Restored camera mismatch');
          record('restore through production validator', 'same source concept + LA + isolated', { id: actual.chosenId, language: actual.language, isolated: actual.state.isolate });
        } else {
          await launch(studyPacks[2]);
          // Return initiates an asynchronous lower reference load. A subsequent manual
          // reference choice must cancel the pending snapshot (the PR3 regression).
          current.current.controls.exit(); await pause(30);
          current.current.controls.reference('male-body'); await pause(30);
          current.current.controls.reference(pack.datasetId);
          await until('explicit reference wins', () => loaded(pack.datasetId));
          await pause(500);
          const actual = current.current.read();
          if (actual.chosenId !== null || actual.pending.returning) throw new Error(`Stale return restored ${actual.chosenId}`);
          record('return → male → lower', 'manual choice wins; selection null; pending return false', { id: actual.chosenId, pending: actual.pending });
        }
      } else {
        const pack = studyPacks[which === 'right' ? 0 : which === 'left' ? 1 : 2];
        await launch(pack); click('Yeni çalışma'); await pause(200);
        for (let i = 0; i < pack.items.length; i++) {
          const expected = pack.items[i].conceptId;
          await until('visible inspection identity', () => current.current.read().chosenId === expected);
          record('inspect visible source', expected, current.current.read().chosenId);
          click(i === pack.items.length - 1 ? 'Hatırlamayı başlat' : 'Sonraki'); await pause(200);
        }
        await until('recall', () => history(pack)?.session.phase === 'recall');
        const beforeAnswer = JSON.stringify(history(pack));
        const buttons = document.querySelectorAll<HTMLButtonElement>('.study-answers button');
        // Sorted labels are deliberate: choose a visible answer other than the target.
        const target = pack.items[0].conceptId;
        const { datasetLabel } = await import('./reference-datasets');
        const wrong = [...buttons].find(b => b.textContent !== datasetLabel(pack.datasetId, target, target, current.current.read().language));
        if (!wrong) throw new Error('Wrong-answer button not available');
        wrong.click();
        await until('wrong feedback persisted', () => history(pack)?.session.phase === 'feedback');
        const h = history(pack)!;
        if (h.session.first[0] !== 'wrong' || !h.undo) throw new Error('Expected wrong first attempt and undo');
        record('wrong visible answer', 'feedback / first wrong / undo / review due', { phase: h.session.phase, first: h.session.first, undo: !!h.undo, cards: h.cards });
        click('Son yanıtı geri al');
        await until('atomic undo', () => history(pack)?.session.phase === 'recall');
        if (beforeAnswer !== JSON.stringify(history(pack))) throw new Error('Undo did not restore scoring/schedule/events atomically');
        record('undo', 'exact pre-answer history restored (session/cards/events/undo)', history(pack)?.session.first);
      }
      setSnapshot(observe()); setNotice(`PASS: ${scenarios[which]}. Replay runs the same bounded visible flow.`);
    } catch (error) { record('scenario failure', 'all assertions pass', String(error), 'FAIL'); setNotice(String(error)); }
    finally { current.current.controls.slowLoad(false); setBusy(false); }
  }
  useEffect(() => {
    if (!enabled) return;
    try {
      const stored = JSON.parse(localStorage.getItem(journalKey) ?? '[]');
      if (Array.isArray(stored)) setEntries(stored.filter((e): e is Entry => e && Number.isSafeInteger(e.sequence)
        && ['PASS', 'FAIL', 'OBSERVE'].includes(e.result) && ['action', 'expected', 'actual'].every(k => typeof e[k] === 'string' && e[k].length <= 1000)).slice(-80));
    } catch { setNotice('Sandbox journal unavailable.'); }
    const timer = window.setInterval(() => setSnapshot(observe()), 350);
    try {
      const raw = localStorage.getItem(resumeKey);
      if (raw) {
        localStorage.removeItem(resumeKey);
        const resume = JSON.parse(raw);
        const pack = studyPacks.find(p => p.id === resume.pack);
        if (pack && typeof resume.expected === 'string') {
          setBusy(true);
          void launch(pack).then(() => {
            if (JSON.stringify(history(pack)) !== resume.expected) throw new Error('Reload changed persisted history');
            record('reload resume', 'exact persisted history/phase/first/undo/schedule restored', history(pack)?.session);
            setNotice('PASS: reload resumed the exact saved study history.');
          }).catch(e => record('reload resume', 'module restored', String(e), 'FAIL')).finally(() => setBusy(false));
        }
      }
    } catch { setNotice('Sandbox resume storage unavailable or invalid.'); }
    return () => { cancel.current = true; window.clearInterval(timer); };
  }, [enabled]);
  if (!enabled) return null;
  return <aside className="dev-qa" aria-label="DEV ONLY visual QA">
    <button className="dev-qa-toggle" onClick={() => setOpen(v => !v)}>DEV ONLY · QA sandbox {open ? '−' : '+'}</button>
    {open && <div className="dev-qa-body">
      <p>No real learner storage. Local development only.</p>
      <label>Scenario<select aria-label="QA scenario" value={scenario} disabled={busy} onChange={e => setScenario(e.target.value as Scenario)}>{Object.entries(scenarios).map(([id, label]) => <option key={id} value={id}>{label}</option>)}</select></label>
      <div className="dev-qa-actions"><button disabled={busy} onClick={() => void run(scenario)}>Start scenario</button><button disabled={busy} onClick={() => void run(scenario)}>Replay scenario</button>
        <button onClick={() => setSnapshot(observe())}>Snapshot</button>
        <button disabled={busy || !current.current.read().studying} onClick={() => { try { const pack = current.current.read().activePack; localStorage.setItem(resumeKey, JSON.stringify({ pack: pack.id, expected: JSON.stringify(history(pack)) })); location.reload(); } catch { setNotice('Reload marker could not be saved.'); } }}>Reload + resume</button>
        <button disabled={busy} onClick={() => { try { for (const key of Object.keys(localStorage)) if (key.startsWith(prefix)) localStorage.removeItem(key); location.reload(); } catch { setNotice('Sandbox reset failed.'); } }}>Reset sandbox</button>
      </div>
      <p role="status">{notice}</p>
      <details><summary>Readable state snapshot</summary><pre data-testid="qa-snapshot">{JSON.stringify(snapshot, null, 2)}</pre></details>
      <details open><summary>Event sequence · expected / actual</summary><ol>{entries.map(e => <li key={e.sequence}><strong>{e.sequence}. {e.result} · {e.action}</strong><div>Expected: {e.expected}</div><div>Actual: {e.actual}</div></li>)}</ol></details>
    </div>}
  </aside>;
}
