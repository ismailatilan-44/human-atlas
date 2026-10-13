async (page) => {
  const url=new URL(page.url());
  if(!['localhost','127.0.0.1','[::1]'].includes(url.hostname) || url.searchParams.get('devqa')!=='1') throw new Error('Use a local devqa fixture tab; never real learner storage');
  const results = [];
  const snap = async () => {
    await page.getByRole('button', {name:'Snapshot',exact:true}).click();
    return JSON.parse(await page.getByTestId('qa-snapshot').textContent());
  };
  const direction = c => { const v=c.position.map((n,i)=>n-c.target[i]); const l=Math.hypot(...v); return v.map(n=>n/l); };
  const delta = (a,b) => Math.max(...a.map((n,i)=>Math.abs(n-b[i])));
  for (const size of [{width:1200,height:942,x:535,y:410},{width:390,height:844,x:195,y:285},{width:320,height:568,x:160,y:232}]) {
    await page.reload(); await page.setViewportSize(size);
    await page.getByRole('button',{name:'Kafatası · 22 kemik',exact:true}).click();
    await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption('FMA52734');
    await page.getByRole('button',{name:'DEV ONLY · QA sandbox −',exact:true}).click();
    await page.mouse.move(size.x,size.y); await page.mouse.down();
    await page.mouse.move(size.x+50,size.y+20,{steps:12}); await page.mouse.up();
    await page.waitForTimeout(2400);
    await page.getByRole('button',{name:'DEV ONLY · QA sandbox +',exact:true}).click();
    const initial = await snap(); const steps=[];
    const act = async (name, run) => {
      const before=await snap(); await run(); const after=await snap();
      await page.getByRole('button',{name:'Önceki görünüme dön',exact:true}).click();
      const undo=await snap();
      const undoDelta=Math.max(delta(before.camera.position,undo.camera.position),delta(before.camera.target,undo.camera.target));
      const undoStateMatches=JSON.stringify(before.visibility)===JSON.stringify(undo.visibility) && before.conceptId===undo.conceptId;
      if(undoDelta>1e-5 || !undoStateMatches) throw new Error(`${size.width}: ${name} undo mismatch`);
      await run();
      steps.push({name,before,after,undoDelta,undoStateMatches,directionDelta:delta(direction(before.camera),direction(after.camera))});
    };
    const button = name => page.getByRole('button',{name,exact:true}).click();
    const bone = id => page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption(id);
    await act('change bone in context',()=>bone('FMA53646'));
    await act('separate',()=>button('Seçili kemiği ayır'));
    await act('change bone while separated',()=>bone('FMA53645'));
    await act('isolate',()=>button('Yapıyı yalnız göster'));
    await act('small to large isolated',()=>bone('FMA52734'));
    await act('show context',()=>button('Çevreyi göster'));
    await act('return separated bone',()=>button('Kemiği yerine döndür'));
    await act('whole skull',()=>button('Bütün kafatasını göster'));
    await act('focus',()=>button('Odaklan'));
    const previous=steps.at(-1).before;
    await button('Önceki görünüme dön'); const back=await snap();
    await page.getByRole('button',{name:'DEV ONLY · QA sandbox −',exact:true}).click();
    await page.screenshot({path:`output/playwright/skull-transitions-${size.width}.png`});
    await page.getByRole('button',{name:'Sahneyi kaydet',exact:true}).click();
    const sceneName=`Orbit transition ${size.width}`;
    const oldCopies=page.getByRole('button',{name:`${sceneName} kaydını sil`,exact:true});
    while(await oldCopies.count()) await oldCopies.last().click();
    await page.getByRole('textbox',{name:'Sahne adı',exact:true}).fill(sceneName);
    await page.getByRole('button',{name:'Bu sahneyi kaydet',exact:true}).click();
    await page.reload();
    await page.getByRole('button',{name:'Kayıtlı sahneler',exact:true}).click();
    await page.getByRole('button',{name:`Devam et · ${sceneName}`,exact:true}).last().click();
    const restored=await snap();
    const restorePoseDelta=Math.max(delta(back.camera.position,restored.camera.position),delta(back.camera.target,restored.camera.target));
    await page.getByRole('combobox',{name:'Kafatası bakışı',exact:true}).selectOption('back');
    const explicitView=await snap();
    if(delta(direction(explicitView.camera),[0,0,-1])>1e-5) throw new Error('Explicit back view failed');
    await page.getByRole('button',{name:'Önceki görünüme dön',exact:true}).click();
    const explicitUndo=await snap();
    if(delta(direction(explicitUndo.camera),direction(restored.camera))>1e-5) throw new Error('Explicit view undo failed');
    if(steps.some(s=>s.directionDelta>1e-5) || restorePoseDelta>1e-5) throw new Error(`${size.width}: orbit drift`);
    results.push({size,initial,steps,restorePoseDelta,backPoseDelta:Math.max(delta(previous.camera.position,back.camera.position),delta(previous.camera.target,back.camera.target)),failures:steps.filter(s=>s.directionDelta>1e-5).map(s=>s.name)});
  }
  return results;
}
