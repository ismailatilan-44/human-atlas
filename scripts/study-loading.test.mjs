import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createServer } from 'vite';
import react from '@vitejs/plugin-react';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

test('a recall session renders safely while retry clears the atlas, then retains its question', async () => {
  const server = await createServer({
    configFile: false, plugins: [react()],
    optimizeDeps: { noDiscovery: true, include: [] },
    server: { middlewareMode: true, hmr: false, watch: null }, appType: 'custom',
  });
  try {
    const { default: StudyPanel } = await server.ssrLoadModule('/app/study-panel.tsx');
    const { newHistory, saveStudy } = await server.ssrLoadModule('/app/study-history.ts');
    const { startStudy } = await server.ssrLoadModule('/app/study-session.ts');
    const { studyPacks } = await server.ssrLoadModule('/app/study-packs.ts');
    const pack = studyPacks.find(pack => pack.id === 'right-ankle-v1');
    const session = { ...startStudy(pack.items.length), phase: 'recall', index: 3 };
    const history = newHistory(pack, session, Date.now());
    const values = new Map();
    const storage = { getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value) };
    globalThis.window = { localStorage: storage };
    assert.ok(saveStudy(storage, pack, history));
    const before = [...values];
    const render = (concepts, blocked) => renderToStaticMarkup(createElement(StudyPanel, {
      pack, concepts, blocked, reveal() {}, exit() {},
    }));
    const loading = render(new Map(), true);
    assert.match(loading, /Hatırla · 4\/9/);
    assert.match(loading, /<fieldset disabled/);
    assert.match(loading, /class="study-answers"><\/div>/);
    const atlas = JSON.parse(readFileSync('public/models/lower-limb-nerve-reference/atlas.json', 'utf8'));
    const restored = render(new Map(atlas.concepts.map(concept => [concept.id, concept])), false);
    assert.match(restored, /Hatırla · 4\/9/);
    assert.doesNotMatch(restored, /<fieldset disabled/);
    assert.match(restored, /class="study-answers"><button/);
    assert.deepEqual([...values], before, 'rendering does not alter saved answers or scheduling');
  } finally {
    delete globalThis.window;
    await server.close();
  }
});

test('all study packs preserve legacy results and ongoing answers across explicit entries', async (t) => {
 const server=await createServer({configFile:false,plugins:[react()],optimizeDeps:{noDiscovery:true,include:[]},server:{middlewareMode:true,hmr:false,watch:null},appType:'custom'});
 try {
  const {default:Panel}=await server.ssrLoadModule('/app/study-panel.tsx');
  const {newHistory,restartHistory,saveStudy}=await server.ssrLoadModule('/app/study-history.ts');
  const {startStudy}=await server.ssrLoadModule('/app/study-session.ts');
  const {studyPacks}=await server.ssrLoadModule('/app/study-packs.ts');
  for (const pack of studyPacks) await t.test(pack.id, () => {
  const n=pack.items.length;
  let h=newHistory(pack,startStudy(n),1);
  h.session={...h.session,phase:'summary',index:n-1,first:Object.fromEntries(pack.items.map((_,i)=>[i,i === 1 ? 'skip' : 'correct'])),success:pack.items.map((_,i)=>i)};
  h.completed=[{at:1,firstCorrect:n-1,successful:n,total:n}]; h.isolated=true;
  const values=new Map(),storage={getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v)};
  globalThis.window={localStorage:storage};saveStudy(storage,pack,h);
  const render=entry=>renderToStaticMarkup(createElement(Panel,{pack,entry,concepts:new Map(),reveal(){},exit(){}}));
  const before=[...values];
  assert.ok(render('new').includes(`İncele · 1/${n}`));assert.doesNotMatch(render('new'),/Çalışma özeti/);
  assert.match(render('result'),/Önceki çalışma sonucu/);assert.ok(render('result').includes(`${n}/${n}`));assert.ok(render('result').includes(`${n-1}/${n}`));assert.match(render('result'),/Atlandı · Sonradan doğru/);
  assert.deepEqual([...values],before);
  h=restartHistory(h,pack,{...startStudy(n),phase:'recall',index:1,first:{0:'correct'},success:[0]},2);
  saveStudy(storage,pack,h);
  assert.ok(render('resume').includes(`Hatırla · 2/${n}`));
  assert.match(render('result'),/Önceki çalışma sonucu/);assert.match(render('result'),/>Devam et</);
  h.lastResult=undefined;saveStudy(storage,pack,h);
  assert.match(render('result'),/yalnız toplam sonuç/);assert.ok(render('result').includes(`${n}/${n}`));
  });
 } finally {delete globalThis.window;await server.close();}
});
