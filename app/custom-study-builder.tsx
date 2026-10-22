import { useState } from 'react';
import type { StudyPack } from './study-packs';
import type { StudyEntry } from './study-history';
import { hasPreviousResult, loadStudy } from './study-history';
import { learningStorage } from './learning-storage';
import { datasetLabel } from './reference-datasets';
import {
  buildCustomStudyPack, loadCustomStudyLibrary, makeCustomStudyPreset,
  MAX_SAVED_CUSTOM_STUDIES, MIN_CUSTOM_ITEMS, resolveCustomStudyPreset,
  saveCustomStudyLibrary, type CustomStudyPreset,
} from './custom-study';
import './custom-study.css';

export default function CustomStudyBuilder({ packs, onStart, disabled = false }: {
  packs: StudyPack[];
  onStart: (pack: StudyPack, entry: StudyEntry) => void;
  disabled?: boolean;
}) {
  const [library, setLibrary] = useState(() => {
    if (typeof window === 'undefined') return { presets: [] as CustomStudyPreset[], writable: false };
    return loadCustomStudyLibrary(learningStorage(), packs);
  });
  const [baseId, setBaseId] = useState(packs[0]?.id ?? '');
  const [selectedIds, setSelectedIds] = useState<string[]>(() => packs[0]?.items.map(it => it.id) ?? []);
  const [search, setSearch] = useState('');
  const [notice, setNotice] = useState(library.notice ?? '');
  const base = packs.find(p => p.id === baseId);
  const chosenPack = base && buildCustomStudyPack(base, selectedIds);
  const chooseBase = (id: string) => {
    const next = packs.find(p => p.id === id);
    if (!next) return;
    setBaseId(id);
    setSelectedIds(next.items.map(it => it.id));
    setSearch('');
    setNotice('');
  };
  const toggleItem = (id: string) => {
    setSelectedIds(ids => ids.includes(id) ? ids.filter(v => v !== id) : [...ids, id]);
  };
  const label = (pack: StudyPack, conceptId: string) =>
    datasetLabel(pack.datasetId, conceptId, conceptId, 'tr');
  const persist = (next: CustomStudyPreset[]) => {
    if (!library.writable || !saveCustomStudyLibrary(learningStorage(), packs, next)) {
      setNotice('Tarayıcı kaydı yazılamadı veya eski kayıt korunuyor. Mevcut çalışma verileri değiştirilmedi.');
      return false;
    }
    setLibrary({ presets: next, writable: true });
    setNotice('Özel çalışma seti bu tarayıcıya kaydedildi.');
    return true;
  };
  const createAndStart = () => {
    if (!base || !chosenPack || disabled) return;
    const preset = makeCustomStudyPreset(base, selectedIds);
    if (!preset) return;
    if (library.writable) {
      const next = [
        preset,
        ...library.presets.filter(other => resolveCustomStudyPreset(other, packs)?.id !== chosenPack.id),
      ].slice(0, MAX_SAVED_CUSTOM_STUDIES);
      persist(next);
    } else setNotice(library.notice ?? 'Kayıt kullanılamıyor; bu set geçici olarak açıldı.');
    onStart(chosenPack, 'new');
  };
  const remove = (preset: CustomStudyPreset) => {
    const target = resolveCustomStudyPreset(preset, packs)?.id;
    persist(library.presets.filter(p => resolveCustomStudyPreset(p, packs)?.id !== target));
  };
  const edit = (preset: CustomStudyPreset) => {
    const next = packs.find(p => p.id === preset.sourcePackId);
    if (!next) return;
    setBaseId(next.id);
    setSelectedIds([...preset.itemIds]);
    setSearch('');
    setNotice('Set seçimleri düzenlemeye açıldı. Kaydet ve başlat ile uygulayın.');
  };
  return <section className="custom-study-builder" aria-label="Özel çalışma oluştur">
    <h3>Özel 3B çalışma seti</h3>
    <p>Kenhub tarzı seçim: mevcut kaynaklı yapılardan kendi çalışma setini oluştur, kaydet ve tekrar et. Yalnız aynı referans içindeki yapılar birlikte çalışılır.</p>
    <label className="custom-study-label" htmlFor="custom-study-region">Bölge</label>
    <select id="custom-study-region" value={baseId} onChange={e => chooseBase(e.target.value)} disabled={disabled}>
      {packs.map(pack => <option key={pack.id} value={pack.id}>{pack.title} · {pack.items.length} yapı</option>)}
    </select>
    {base && <>
      <div className="custom-study-actions">
        <button type="button" onClick={() => setSelectedIds(base.items.map(it => it.id))} disabled={disabled}>Tümünü seç</button>
        <button type="button" onClick={() => setSelectedIds([])} disabled={disabled}>Seçimi temizle</button>
      </div>
      <input type="search" aria-label="Çalışma yapılarında ara" value={search}
        placeholder="Yapı ara…" onChange={e => setSearch(e.target.value)} />
      <fieldset className="custom-study-structures" disabled={disabled}>
        <legend>Yapılar · {selectedIds.length}/{base.items.length} seçili</legend>
        {base.items.filter(it => label(base, it.conceptId).toLocaleLowerCase('tr').includes(search.toLocaleLowerCase('tr')))
          .map(it => <label key={it.id} className="custom-study-item">
            <input type="checkbox" checked={selectedIds.includes(it.id)} onChange={() => toggleItem(it.id)} />
            <span>{label(base, it.conceptId)}</span>
          </label>)}
      </fieldset>
      <p className="custom-study-note">En az {MIN_CUSTOM_ITEMS} yapı seç. Her setin kendi çalışma geçmişi vardır; hazır modüllerin eski kayıtları değişmez.</p>
      <button type="button" className="custom-study-primary" disabled={!chosenPack || disabled} onClick={createAndStart}>
        Seti kaydet ve başlat · {selectedIds.length} yapı
      </button>
    </>}
    {notice && <p role="status">{notice}</p>}
    {library.presets.length > 0 && <div className="custom-study-saved">
      <h3>Kaydedilen özel setler ({library.presets.length}/{MAX_SAVED_CUSTOM_STUDIES})</h3>
      {library.presets.map(preset => {
        const pack = resolveCustomStudyPreset(preset, packs);
        if (!pack) return null;
        let saved;
        try { saved = loadStudy(learningStorage(), pack).history; } catch { /* Unsaved practice is still available. */ }
        return <div key={pack.id} role="group" aria-label={pack.title + ' · ' + pack.items.length + ' yapı'}>
          <strong>{packs.find(p => p.id === preset.sourcePackId)?.title} · {pack.items.length} yapı</strong>
          <div>
            <button type="button" disabled={disabled} onClick={() => onStart(pack, 'new')}>Yeni çalışma</button>
            {saved && saved.session.phase !== 'summary' && <button type="button" disabled={disabled} onClick={() => onStart(pack, 'resume')}>Devam et</button>}
            {saved && hasPreviousResult(saved) && <button type="button" disabled={disabled} onClick={() => onStart(pack, 'result')}>Önceki sonucu gör</button>}
            <button type="button" disabled={disabled} onClick={() => edit(preset)}>Düzenle</button>
            <button type="button" disabled={disabled || !library.writable} onClick={() => remove(preset)}>Listeden kaldır</button>
          </div>
        </div>;
      })}
      <p>Listeden kaldırmak, çalışma geçmişini silmez. Setler yalnız bu tarayıcıda saklanır.</p>
    </div>}
  </section>;
}
