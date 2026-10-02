import { learningStorage, studyNow } from './learning-storage';
import { useEffect, useRef, useState } from 'react';
import type { LearnerHistory } from './study-history';
export type StudyDiagnostics = { module: string; history: LearnerHistory; persistence: 'pending' | 'saved' | 'failed' };
import { startStudy, studyTransition, type StudyAction } from './study-session';
import { dueItems, loadStudy, newHistory, review, saveStudy } from './study-history';
import type { StudyPack } from './study-packs';
import { datasetLabel, referenceDescription } from './reference-datasets';
import { matchesAnatomyQuery } from './search';
import { assetUrl } from './asset-url';
import type { Concept } from './anatomy';
import type { AnatomyLanguage } from './atlas-metadata';

export default function StudyPanel({ pack, concepts, reveal, exit, onDiagnostics, blocked = false, language = 'tr' }: {
  onDiagnostics?: (value: StudyDiagnostics) => void; blocked?: boolean; pack: StudyPack; concepts: Map<string, Concept>; reveal: (id: string, isolated: boolean) => void; exit: () => void; language?: AnatomyLanguage;
}) {
  const [loaded] = useState(() => { try { return loadStudy(learningStorage(), pack); } catch { return { notice: 'Yerel depolama kullanılamıyor.' }; } });
  const [history, setHistory] = useState(() => loaded.history ?? newHistory(pack, startStudy(pack.items.length), studyNow()));
  const [notice, setNotice] = useState(loaded.notice ?? 'İlerleme bu tarayıcıda saklanır.');
  const [persistence, setPersistence] = useState<StudyDiagnostics['persistence']>('pending');
  const [query, setQuery] = useState('');
  const [revision, setRevision] = useState(0);
  const revealRef = useRef(reveal); revealRef.current = reveal;
  const heading = useRef<HTMLHeadingElement>(null);
  const session = history.session;
  const item = pack.items[session.queue[session.index]];
  const recall = session.phase === 'recall';
  const name = (id: string, lang = language) => datasetLabel(pack.datasetId, id, concepts.get(id)?.name ?? id, lang);
  const due = dueItems(history, pack, studyNow());
  const mastered = Object.values(history.cards).filter(c => c.streak >= 3).length;
  useEffect(() => {
    try {
      const saved = saveStudy(learningStorage(), pack, history);
      setPersistence(saved ? 'saved' : 'failed');
      if (!saved) setNotice('Kayıt yazılamadı; oturum bellekte sürüyor. Depolama alanını kontrol edin.');
    } catch { setPersistence('failed'); setNotice('Yerel depolama kullanılamıyor; oturum bellekte sürüyor.'); }
  }, [history, pack]);
  useEffect(() => {
    revealRef.current(item.conceptId, history.isolated);
    setQuery(''); heading.current?.focus();
  }, [item.conceptId, session.phase, history.isolated, revision]);
  useEffect(() => {
    if (import.meta.env.DEV) onDiagnostics?.({ module: pack.id, history, persistence });
  }, [history, persistence, pack, onDiagnostics]);
  const transition = (action: StudyAction) => {
    if (blocked) return;
    setHistory(h => {
      const next = studyTransition(h.session, action);
      const completed = next.phase === 'summary' && h.session.phase !== 'summary'
        ? [...h.completed, { at: studyNow(), firstCorrect: Object.values(next.first).filter(v => v === 'correct').length, successful: next.success.length, total: Object.keys(next.first).length }].slice(-50) : h.completed;
      return { ...h, session: next, completed, undo: undefined };
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
    if (reviewOnly) { if (!due.length) return; session.queue = due; session.phase = 'recall'; }
    setHistory(h => ({ ...h, undo: undefined, session, isolated: false, sessionId: newHistory(pack, session, studyNow()).sessionId })); setRevision(v => v + 1);
  };
  const firstCorrect = Object.values(session.first).filter(v => v === 'correct').length;
  const skipped = Object.values(session.first).filter(v => v === 'skip').length;
  const attempted = Object.keys(session.first).length;
  return <>
    <div className="study-top"><strong>{pack.title}</strong><button onClick={exit}>Kaydet ve Geri</button></div>
    <section className="detail-sheet study-panel" aria-label="Bölgesel çalışma">
      <fieldset disabled={blocked} style={{ border: 0, padding: 0, margin: 0, minWidth: 0 }}>
      <h2 ref={heading} tabIndex={-1}>{session.phase === 'summary' ? 'Çalışma özeti' : `${session.phase === 'inspect' ? 'İncele' : session.retry ? 'Tekrar' : 'Hatırla'} · ${session.index + 1}/${session.queue.length}`}</h2>
      {session.phase === 'summary' ? <>
        <p>İlk denemede ipucusuz doğru: <strong>{firstCorrect}/{attempted}</strong> · Atlanan: {skipped}</p>
        <p>Tekrarlar dahil doğru: <strong>{session.success.length}/{attempted}</strong></p>
        <ul>{pack.items.filter((_, i) => session.first[i] !== undefined).map(it => { const i = pack.items.indexOf(it); return <li key={it.id}>{name(it.conceptId)} — {session.first[i] === 'correct' ? 'İlk denemede doğru' : session.first[i] === 'skip' ? 'Atlandı' : 'İlk denemede yanlış / ipuçlu'}{session.first[i] !== 'correct' && session.success.includes(i) ? ' · Sonradan doğru' : ''}</li>; })}</ul>
        {session.success.length < attempted && <button onClick={() => transition({ type: 'retry' })}>Eksikleri tekrar et</button>}
        <button onClick={exit}>Bitir ve keşfe dön</button>
      </> : <>
        {recall ? <>
          <p>Vurgulanan yapının adı nedir?</p>
          {session.hinted && <p role="status">İpucu: {name(item.conceptId)}. Bu yanıt ipucusuz başarı sayılmaz.</p>}
          <input aria-label="Yanıt seçeneklerinde ara" placeholder="Ad veya kaynak kimliği ara…" value={query} onChange={e => setQuery(e.target.value)} />
          <div className="study-answers">{[...pack.items].sort((a,b) => name(a.conceptId).localeCompare(name(b.conceptId),'tr')).filter(it => matchesAnatomyQuery(pack.datasetId, concepts.get(it.conceptId)!, query)).map(it => <button key={it.id} onClick={() => answer(it.conceptId)}>{name(it.conceptId)}</button>)}</div>
          <button onClick={() => transition({ type: 'hint' })}>İpucu göster</button><button onClick={() => answer(null)}>Atla</button>
        </> : <>
          {session.phase === 'feedback' && <p role="status">{session.answer === item.conceptId ? session.hinted ? 'İpucuyla doğru.' : 'Doğru.' : session.answer === null ? 'Atlandı. Doğru yanıt:' : `Yanlış: ${name(session.answer!)}. Doğru yanıt:`}</p>}
          <h3>{name(item.conceptId)}</h3><p>{name(item.conceptId, 'en')} · {name(item.conceptId, 'la')}</p>
          <p>{referenceDescription(pack.datasetId, item.conceptId)}</p>
          <details><summary>Kaynak ve sınırlar</summary><p>{item.conceptId} · {item.sourceObject}</p>{item.evidence.map(e => <p key={e.sourceId}>{e.sourceId}: {e.locator}</p>)}<p>Kaynak yüzey kusurları korunur; uzman incelemesi bekliyor.</p><a href={assetUrl(pack.attribution)} target="_blank" rel="noreferrer">Kaynak ve lisans kaydı</a></details>
          {session.phase === 'feedback' && history.undo && <button onClick={() => { setHistory(h => h.undo ?? h); }}>Son yanıtı geri al</button>}
          <button onClick={() => transition({ type: 'next' })}>{session.phase === 'inspect' && session.index === pack.items.length - 1 ? 'Hatırlamayı başlat' : 'Sonraki'}</button>
        </>}
        <button onClick={() => setHistory(h => ({ ...h, isolated: !h.isolated }))}>{history.isolated ? 'Bağlamı göster' : 'Yalnız yapıyı göster'}</button>
      </>}
      <button onClick={() => restart()}>Yeni çalışma</button>
      <button disabled={!due.length} onClick={() => restart(true)}>Zamanı gelenleri çalış · {due.length}</button>
      <details><summary>İlerleme ve tekrar planı</summary><p>{history.completed.length} tamamlanan tur (en fazla 50 kayıt). Aralıklı başarı: {mastered}/{pack.items.length} (en az 3 zamanı gelmiş ipucusuz doğru).</p><p>Doğru: 1, 3, 7, 14, 30 gün. Yanlış/ipucu: 10 dakika. Atla: tarih değişmez. Erken pratik aralığı artırmaz. Tarihler UTC; saat geri alınırsa son kayıt zamanı korunur. Bu bir öğrenme göstergesidir; anatomik yeterlik ölçümü değildir.</p>{pack.items.map(it => <p key={it.id}>{name(it.conceptId)}: {history.cards[it.id] ? new Date(history.cards[it.id].due).toISOString().replace('T',' ').slice(0,16) + ' UTC' : 'Yeni'}</p>)}<p>İçerik sürümü: {pack.version}</p></details>
      </fieldset>
      <p role="status">{notice}</p><p className="study-limit">{pack.scope} {pack.learningGoals.join(' ')} Yenilemeden sonra bu modülü açarak devam edebilirsiniz. Hesap/sunucu yok; tarayıcı verisini silmek kayıtları siler.</p>
    </section>
  </>;
}
