import { skullDescription } from './skull';
import type { ReactNode } from 'react';
import { learningStorage, studyNow } from './learning-storage';
import { useEffect, useRef, useState } from 'react';
import type { LearnerHistory, StudyEntry } from './study-history';
export type StudyDiagnostics = { module: string; history: LearnerHistory; persistence: 'pending' | 'saved' | 'failed' };
import { startStudy, studyTransition, type StudyAction } from './study-session';
import { dueItems, loadStudy, newHistory, review, saveStudy, previousResult, hasPreviousResult, restartHistory } from './study-history';
import type { StudyPack } from './study-packs';
import { datasetLabel, referenceDescription } from './reference-datasets';
import { matchesAnatomyQuery } from './search';
import { assetUrl } from './asset-url';
import type { Concept } from './anatomy';
import type { AnatomyLanguage } from './atlas-metadata';

export default function StudyPanel({ pack, concepts, reveal, exit, onDiagnostics, skullControls, overview, entry = 'resume', blocked = false, language = 'tr' }: {
  skullControls?: ReactNode; overview?: () => void; entry?: StudyEntry;
  onDiagnostics?: (value: StudyDiagnostics) => void; blocked?: boolean; pack: StudyPack; concepts: Map<string, Concept>; reveal: (id: string, isolated: boolean) => void; exit: () => void; language?: AnatomyLanguage;
}) {
  const [loaded] = useState(() => { try { return loadStudy(learningStorage(), pack); } catch { return { notice: 'Yerel depolama kullanılamıyor.' }; } });
  const [history, setHistory] = useState(() => {
    const h = loaded.history ?? newHistory(pack, startStudy(pack.items.length), studyNow());
    return entry === 'new' ? restartHistory(h, pack, startStudy(pack.items.length), studyNow()) : h;
  });
  const [viewingResult, setViewingResult] = useState(entry === 'result');
  const [notice, setNotice] = useState(loaded.notice ?? 'İlerleme bu tarayıcıda saklanır.');
  const [persistence, setPersistence] = useState<StudyDiagnostics['persistence']>('pending');
  const [query, setQuery] = useState('');
  const [revision, setRevision] = useState(0);
  const [, refreshClock] = useState(0);
  const revealRef = useRef(reveal); revealRef.current = reveal;
  const heading = useRef<HTMLHeadingElement>(null);
  const result = previousResult(history);
  const session = viewingResult && result ? result.session : history.session;
  const summary = viewingResult || session.phase === 'summary';
  const aggregate = viewingResult && !result ? history.completed.at(-1) : undefined;
  const resultAt = viewingResult ? result?.at ?? aggregate?.at : history.completed.at(-1)?.at;
  const overviewRef = useRef(overview); overviewRef.current = overview;
  const item = pack.items[session.queue[session.index]];
  const recall = session.phase === 'recall';
  const name = (id: string, lang = language) => datasetLabel(pack.datasetId, id, concepts.get(id)?.name ?? id, lang);
  const due = dueItems(history, pack, studyNow());
  const mastered = Object.values(history.cards).filter(c => c.streak >= 3).length;
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;
    const refresh = () => {
      clearTimeout(timer);
      refreshClock(value => value + 1);
      const now = studyNow();
      const upcoming = pack.items.map(it => history.cards[it.id]?.due)
        .filter((at): at is number => at !== undefined && at > now);
      // Wake at the next due boundary; cap the wait to notice wall-clock changes.
      timer = setTimeout(refresh, Math.min(60000, ...upcoming.map(at => at - now)));
    };
    const visible = () => { if (document.visibilityState === 'visible') refresh(); };
    refresh();
    window.addEventListener('focus', refresh);
    document.addEventListener('visibilitychange', visible);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('focus', refresh);
      document.removeEventListener('visibilitychange', visible);
    };
  }, [history.cards, pack]);
  useEffect(() => {
    if (viewingResult) return;
    try {
      const saved = saveStudy(learningStorage(), pack, history);
      setPersistence(saved ? 'saved' : 'failed');
      if (!saved) setNotice('Kayıt yazılamadı; oturum bellekte sürüyor. Depolama alanını kontrol edin.');
    } catch { setPersistence('failed'); setNotice('Yerel depolama kullanılamıyor; oturum bellekte sürüyor.'); }
  }, [history, pack, viewingResult]);
  useEffect(() => {
    if (blocked) return;
    if (summary) { overviewRef.current?.(); heading.current?.focus(); return; }
    if (!concepts.has(item.conceptId)) return;
    revealRef.current(item.conceptId, history.isolated);
    setQuery(''); heading.current?.focus();
  }, [item.conceptId, session.phase, history.isolated, revision, concepts, blocked, summary]);
  useEffect(() => {
    if (import.meta.env.DEV) onDiagnostics?.({ module: pack.id, history, persistence });
  }, [history, persistence, pack, onDiagnostics]);
  const transition = (action: StudyAction) => {
    if (blocked) return;
    setHistory(h => {
      const next = studyTransition(h.session, action);
      const completed = next.phase === 'summary' && h.session.phase !== 'summary'
        ? [...h.completed, { at: studyNow(), firstCorrect: Object.values(next.first).filter(v => v === 'correct').length, successful: next.success.length, total: Object.keys(next.first).length }].slice(-50) : h.completed;
      return { ...h, session: next, completed, lastResult: next.phase === 'summary' ? { session: next, at: completed.at(-1)?.at } : previousResult(h), undo: undefined };
    });
  };
  const answer = (value: string | null) => {
    if (blocked || session.phase !== 'recall') return;
    setHistory(h => {
      if (h.session.phase !== 'recall') return h;
      const correct = value === item.conceptId;
      const updated = review(h, { id: `${h.sessionId}:${studyNow()}:${Math.random().toString(36).slice(2)}`, itemId: item.id, at: studyNow(), outcome: value === null ? 'skip' : h.session.hinted ? 'hint' : correct ? 'correct' : 'wrong' });
      return { ...updated, undo: { ...h, undo: undefined }, session: studyTransition(h.session, { type: 'answer', value, correct }) };
    });
  };
  const restart = (reviewOnly = false) => {
    if (blocked) return;
    const session = startStudy(pack.items.length);
    if (reviewOnly) {
      const currentDue = dueItems(history, pack, studyNow());
      if (!currentDue.length) return;
      session.queue = currentDue; session.phase = 'recall';
    }
    setViewingResult(false);
    setHistory(h => restartHistory(h, pack, session, studyNow())); setRevision(v => v + 1);
  };
  const firstCorrect = aggregate?.firstCorrect ?? Object.values(session.first).filter(v => v === 'correct').length;
  const skipped = Object.values(session.first).filter(v => v === 'skip').length;
  const attempted = aggregate?.total ?? Object.keys(session.first).length;
  return <>
    <div className="study-top"><strong>{pack.title}</strong><button onClick={exit}>{viewingResult ? 'Geri' : 'Kaydet ve Geri'}</button></div>
    <section className="detail-sheet study-panel" aria-label="Bölgesel çalışma">
      <fieldset disabled={blocked} style={{ border: 0, padding: 0, margin: 0, minWidth: 0 }}>
      <h2 ref={heading} tabIndex={-1}>{summary ? (viewingResult ? 'Önceki çalışma sonucu' : 'Çalışma özeti') : `${session.phase === 'inspect' ? 'İncele' : session.retry ? 'Tekrar' : 'Hatırla'} · ${session.index + 1}/${session.queue.length}`}</h2>
      {summary ? <>
        <p>{viewingResult ? 'Bu kayıtlı sonuçtur; yeni bir soru değildir. Görüntülemek ilerlemenizi değiştirmez.' : 'Bu tur tamamlandı.'} {resultAt !== undefined && <time dateTime={new Date(resultAt).toISOString()}>{new Date(resultAt).toLocaleString('tr-TR')}</time>}</p>
        <p>İlk denemede ipucusuz doğru: <strong>{firstCorrect}/{attempted}</strong>{!aggregate && <> · Atlanan: {skipped}</>}</p>
        <p>Tekrarlar dahil doğru: <strong>{aggregate?.successful ?? session.success.length}/{attempted}</strong></p>
        {aggregate ? <p>Bu eski kayıtta yalnız toplam sonuç saklanmış; soru ayrıntıları mevcut değil.</p> : <ul>{pack.items.filter((_, i) => session.first[i] !== undefined).map(it => { const i = pack.items.indexOf(it); return <li key={it.id}>{name(it.conceptId)} — {session.first[i] === 'correct' ? 'İlk denemede doğru' : session.first[i] === 'skip' ? 'Atlandı' : 'İlk denemede yanlış / ipuçlu'}{session.first[i] !== 'correct' && session.success.includes(i) ? ' · Sonradan doğru' : ''}</li>; })}</ul>}
        {!viewingResult && session.success.length < attempted && <button onClick={() => transition({ type: 'retry' })}>Eksikleri tekrar et</button>}
        <button onClick={exit}>Bitir ve keşfe dön</button>
      </> : <>
        {recall ? <>
          <p>Vurgulanan yapının adı nedir?</p>
          {session.hinted && <p role="status">İpucu: {name(item.conceptId)}. Bu yanıt ipucusuz başarı sayılmaz.</p>}
          <input aria-label="Yanıt seçeneklerinde ara" placeholder="Ad veya kaynak kimliği ara…" value={query} onChange={e => setQuery(e.target.value)} />
          <div className="study-answers">{[...pack.items].sort((a,b) => name(a.conceptId).localeCompare(name(b.conceptId),'tr')).filter(it => {
            const concept = concepts.get(it.conceptId);
            return concept && matchesAnatomyQuery(pack.datasetId, concept, query);
          }).map(it => <button key={it.id} onClick={() => answer(it.conceptId)}>{name(it.conceptId)}</button>)}</div>
          <button onClick={() => transition({ type: 'hint' })}>İpucu göster</button><button onClick={() => answer(null)}>Atla</button>
        </> : <>
          {session.phase === 'feedback' && <p role="status">{session.answer === item.conceptId ? session.hinted ? 'İpucuyla doğru.' : 'Doğru.' : session.answer === null ? 'Atlandı. Doğru yanıt:' : `Yanlış: ${name(session.answer!)}. Doğru yanıt:`}</p>}
          <h3>{name(item.conceptId)}</h3><p>{name(item.conceptId, 'en')} · {name(item.conceptId, 'la')}</p>
          <p>{pack.id === 'whole-skull-v1' ? skullDescription(item.conceptId) : referenceDescription(pack.datasetId, item.conceptId)}</p>
          <details><summary>Kaynak ve sınırlar</summary><p>{item.conceptId} · {item.sourceObject}</p>{item.evidence.map(e => <p key={e.sourceId}>{e.sourceId}: {e.locator}</p>)}<p>Kaynak yüzey kusurları korunur; uzman incelemesi bekliyor.</p><a href={assetUrl(pack.attribution)} target="_blank" rel="noreferrer">Kaynak ve lisans kaydı</a></details>
          {session.phase === 'feedback' && history.undo && <button onClick={() => { setHistory(h => h.undo ?? h); }}>Son yanıtı geri al</button>}
          <button onClick={() => transition({ type: 'next' })}>{session.phase === 'inspect' && session.index === pack.items.length - 1 ? 'Hatırlamayı başlat' : 'Sonraki'}</button>
        </>}
        <button onClick={() => setHistory(h => ({ ...h, isolated: !h.isolated }))}>{history.isolated ? 'Bağlamı göster' : 'Yalnız yapıyı göster'}</button>
      </>}
      {!summary && skullControls}
      {viewingResult && history.session.phase !== 'summary' && <button onClick={() => setViewingResult(false)}>Devam et</button>}
      {!viewingResult && hasPreviousResult(history) && <button onClick={() => setViewingResult(true)}>Önceki sonucu gör</button>}
      <button onClick={() => restart()}>Yeni çalışma</button>
      <button disabled={!due.length} onClick={() => restart(true)}>Zamanı gelenleri çalış · {due.length}</button>
      <details><summary>İlerleme ve tekrar planı</summary><p>{history.completed.length} tamamlanan tur (en fazla 50 kayıt). Aralıklı başarı: {mastered}/{pack.items.length} (en az 3 zamanı gelmiş ipucusuz doğru).</p>{history.completed.length > 0 && <ul aria-label="Geçmiş tur sonuçları">{history.completed.map((c, i) => <li key={`${c.at}:${i}`}>{new Date(c.at).toLocaleString('tr-TR')} — İlk deneme: {c.firstCorrect}/{c.total}, tekrarlar dahil: {c.successful}/{c.total}</li>)}</ul>}<p>Doğru: 1, 3, 7, 14, 30 gün. Yanlış/ipucu: 10 dakika. Atla: tarih değişmez. Erken pratik aralığı artırmaz. Tarihler UTC; saat geri alınırsa son kayıt zamanı korunur. Bu bir öğrenme göstergesidir; anatomik yeterlik ölçümü değildir.</p>{pack.items.map(it => <p key={it.id}>{name(it.conceptId)}: {history.cards[it.id] ? new Date(history.cards[it.id].due).toISOString().replace('T',' ').slice(0,16) + ' UTC' : 'Yeni'}</p>)}<p>İçerik sürümü: {pack.version}</p></details>
      </fieldset>
      <p role="status">{notice}</p><p className="study-limit">{pack.scope} {pack.learningGoals.join(' ')} Yenilemeden sonra bu modülü açarak devam edebilirsiniz. Hesap/sunucu yok; tarayıcı verisini silmek kayıtları siler.</p>
    </section>
  </>;
}
