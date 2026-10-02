import { useState } from 'react';
import { createPortal } from 'react-dom';
import './saved-scenes.css';
import type { Atlas, CameraPose, DatasetId, SceneState } from './anatomy';
import { captureScene, loadSceneStore, MAX_SAVED_SCENES, writeSceneStore, type SavedScene } from './saved-scenes';

export default function SavedScenesPanel(props: {
  atlas: Atlas; dataset: DatasetId; state: SceneState; camera: () => CameraPose | null;
  chosenId: string | null; details: boolean; language: SavedScene['language'];
  onRestore: (scene: SavedScene) => void; onClose: () => void;
}) {
  const [store, setStore] = useState(() => {
    try { return loadSceneStore(window.localStorage); }
    catch { return { scenes: [] as SavedScene[], error: 'Tarayıcı depolamasına erişilemiyor.', recovered: false }; }
  });
  const [name, setName] = useState('');
  const [message, setMessage] = useState(store.error ?? '');
  function save(scenes: SavedScene[]) {
    let error: string | null;
    try { error = writeSceneStore(window.localStorage, scenes); }
    catch { error = 'Tarayıcı depolamasına erişilemiyor.'; }
    if (error) { setMessage(error); return; }
    setStore({ scenes, error: null, recovered: false });
    setMessage('Kayıt bu tarayıcıda saklandı.');
  }
  return createPortal(<section className="saved-scenes-panel" aria-label="Kayıtlı sahneler">
    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12 }}><h2>Kayıtlı sahneler</h2><button onClick={props.onClose} aria-label="Kayıtlı sahneleri kapat">Kapat</button></div>
    <p style={{ marginBlock: 12 }}>Kamera, seçim, katmanlar, gizlenen yapılar ve etiket dili bu tarayıcıda saklanır. Sayfa yenilendikten sonra Devam et ile açın. En fazla {MAX_SAVED_SCENES} sahne.</p>
    <form onSubmit={e => { e.preventDefault(); if (store.scenes.length >= MAX_SAVED_SCENES) return; save([...store.scenes, captureScene({ ...props, camera: props.camera(), name })]); setName(''); }}>
      <label>Sahne adı<input aria-label="Sahne adı" maxLength={80} value={name} onChange={e => setName(e.target.value)} placeholder="Örneğin sağ ayak bağlamı" style={{ display: 'block', width: '100%', marginBlock: 8, padding: 8, border: '1px solid #aaa', borderRadius: 8 }} /></label>
      <button disabled={store.scenes.length >= MAX_SAVED_SCENES} type="submit">Bu sahneyi kaydet</button>
    </form>
    {message && <p role="status" style={{ marginBlock: 12 }}>{message}</p>}
    <ul style={{ listStyle: 'none', padding: 0 }}>{store.scenes.map(scene => <li key={scene.id} style={{ borderTop: '1px solid #ccc', paddingBlock: 12, overflowWrap: 'anywhere' }}>
      <strong>{scene.name}</strong><p>{scene.dataset} · {new Date(scene.savedAt).toLocaleString()} · {scene.language.toUpperCase()}</p>
      <div style={{ display: 'flex', gap: 20, marginTop: 8 }}><button onClick={() => props.onRestore(scene)}>Devam et · {scene.name}</button><button aria-label={`${scene.name} kaydını sil`} onClick={() => save(store.scenes.filter(s => s.id !== scene.id))}>Sil</button></div>
    </li>)}</ul>
    {!store.scenes.length && <p>Henüz kayıtlı sahne yok.</p>}
    <p style={{ fontSize: 12 }}>Tarayıcı verilerini temizlemek kayıtları siler. Bu kayıtlar öğrenme başarısı veya uzman kabulü değildir.</p>
  </section>, document.body);
}
