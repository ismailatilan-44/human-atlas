import { useEffect, useRef, useState } from 'react';
import pack from '../data/study/right-ankle-v1.json';
import metadata from '../data/anatomy/lower-limb-reference.json';
import { startStudy, studyTransition } from './study-session';
import { datasetLabel } from './reference-datasets';
import { matchesAnatomyQuery } from './search';
import { assetUrl } from './asset-url';
import type { Concept } from './anatomy';

export default function StudyPanel({ concepts, reveal, exit }: {
  concepts: Map<string, Concept>; reveal: (id: string, isolated: boolean) => void; exit: () => void;
}) {
  const [session, setSession] = useState(() => startStudy(pack.items.length));
  const [query, setQuery] = useState('');
  const [isolated, setIsolated] = useState(false);
  const [revision, setRevision] = useState(0);
  const revealRef = useRef(reveal); revealRef.current = reveal;
  const heading = useRef<HTMLHeadingElement>(null);
  const item = pack.items[session.queue[session.index]];
  const recall = session.phase === 'recall';
  const name = (id: string) => datasetLabel('lower-limb-nerve-reference', id, concepts.get(id)?.name ?? id, 'tr');
  useEffect(() => {
    revealRef.current(item.conceptId, isolated);
    setQuery('');
    heading.current?.focus();
  }, [item.conceptId, session.phase, isolated, revision]);
  const answer = (value: string | null) => setSession(s => studyTransition(s, { type: 'answer', value, correct: value === item.conceptId }));
  const firstCorrect = Object.values(session.first).filter(v => v === 'correct').length;
  const skipped = Object.values(session.first).filter(v => v === 'skip').length;
  const entry = metadata.labels.find(l => l.ids.includes(item.conceptId))!;
  return <>
    <div className="study-top"><strong>{pack.title}</strong><button onClick={exit}>Oturumu bitir · Geri</button></div>
    <section className="detail-sheet study-panel" aria-label="Bölgesel çalışma">
      <h2 ref={heading} tabIndex={-1}>{session.phase === 'summary' ? 'Çalışma özeti' : `${session.phase === 'inspect' ? 'İncele' : session.retry ? 'Tekrar' : 'Hatırla'} · ${session.index + 1}/${session.queue.length}`}</h2>
      {session.phase === 'summary' ? <>
        <p>İlk denemede doğru: <strong>{firstCorrect}/{pack.items.length}</strong> · Atlanan: {skipped}</p>
        <p>Tekrarlar dahil doğru: <strong>{session.success.length}/{pack.items.length}</strong></p>
        <p>Henüz doğru yanıtlanmayan: {pack.items.length - session.success.length}</p>
        <ul>{pack.items.map((it, i) => <li key={it.id}>{name(it.conceptId)} — {session.first[i] === 'correct' ? 'İlk denemede doğru' : session.first[i] === 'skip' ? 'Atlandı' : 'İlk denemede yanlış'}{session.first[i] !== 'correct' && session.success.includes(i) ? ' · Tekrarda doğru' : ''}</li>)}</ul>
        {session.success.length < pack.items.length && <button onClick={() => setSession(s => studyTransition(s, { type: 'retry' }))}>Eksikleri tekrar et</button>}
        <button onClick={exit}>Bitir ve keşfe dön</button>
      </> : <>
        {recall ? <>
          <p>Vurgulanan kemiğin adı nedir?</p>
          <input aria-label="Yanıt seçeneklerinde ara" placeholder="Ad veya kaynak kimliği ara…" value={query} onChange={e => setQuery(e.target.value)} />
          <div className="study-answers">{[...pack.items].sort((a,b) => name(a.conceptId).localeCompare(name(b.conceptId),'tr')).filter(it => matchesAnatomyQuery('lower-limb-nerve-reference', concepts.get(it.conceptId)!, query)).map(it => <button key={it.id} onClick={() => answer(it.conceptId)}>{name(it.conceptId)}</button>)}</div>
          <button onClick={() => answer(null)}>Atla</button>
        </> : <>
          {session.phase === 'feedback' && <p role="status">{session.answer === item.conceptId ? 'Doğru.' : session.answer === null ? 'Atlandı. Doğru yanıt:' : `Yanlış: ${name(session.answer!)}. Doğru yanıt:`}</p>}
          <h3>{name(item.conceptId)}</h3><p>{entry.en} · {entry.la}</p>
          <p>Aynı kaynak çerçevesinde ayrı kemik yüzeyi. İnce eklem ayrıntıları bu alıştırmanın kapsamında değildir.</p>
          <details><summary>Kaynak ve sınırlar</summary><p>{item.conceptId} · {item.sourceObject}</p>{item.evidence.map(e => <p key={e.sourceId}>{e.sourceId}: {e.locator}</p>)}<p>Kaynak yüzey kusurları korunur; uzman incelemesi bekliyor.</p><a href={assetUrl(pack.attribution)} target="_blank" rel="noreferrer">Z-Anatomy kaynak ve lisans kaydı</a></details>
          <button onClick={() => setSession(s => studyTransition(s, { type: 'next' }))}>{session.phase === 'inspect' && session.index === pack.items.length - 1 ? 'Hatırlamayı başlat' : 'Sonraki'}</button>
        </>}
        <button onClick={() => setIsolated(v => !v)}>{isolated ? 'Bağlamı göster' : 'Yalnız kemiği göster'}</button>
      </>}
      <button onClick={() => { setSession(startStudy(pack.items.length)); setIsolated(false); setRevision(v => v + 1); }}>Yeniden başlat</button>
      <p className="study-limit">9 kaynak yapısının adını tanıma; tam bölge veya uzman onaylı sınav değildir. İlerleme yalnız bu açık oturumda tutulur; geri dönüş ve sayfa yenileme oturumu sonlandırır.</p>
    </section>
  </>;
}
