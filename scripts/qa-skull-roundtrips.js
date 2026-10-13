async (page) => {
  const url=new URL(page.url());
  if(!['localhost','127.0.0.1','[::1]'].includes(url.hostname)||url.searchParams.get('devqa')!=='1') throw new Error('Local devqa fixture required');
  const results=[];
  const snap=async()=>{await page.getByRole('button',{name:'Snapshot',exact:true}).click();return JSON.parse(await page.getByTestId('qa-snapshot').textContent());};
  const delta=(a,b)=>Math.max(...a.map((n,i)=>Math.abs(n-b[i])));
  const direction=c=>{const v=c.position.map((n,i)=>n-c.target[i]);const l=Math.hypot(...v);return v.map(n=>n/l);};
  const check=(name,before,after)=>{
    const poseDelta=Math.max(delta(before.camera.position,after.camera.position),delta(before.camera.target,after.camera.target));
    const matches=before.reference===after.reference&&before.conceptId===after.conceptId&&before.viewMode===after.viewMode&&JSON.stringify(before.camera.viewOffset)===JSON.stringify(after.camera.viewOffset)&&JSON.stringify(before.visibility)===JSON.stringify(after.visibility);
    if(!matches||poseDelta>1e-5) throw new Error(JSON.stringify({name,before,after,poseDelta,matches}));
    return {name,before,after,poseDelta,matches};
  };
  for(const size of [{width:1200,height:942,x:535,y:410},{width:390,height:844,x:195,y:285},{width:320,height:568,x:160,y:232}]){
    await page.reload();await page.setViewportSize(size);
    await page.getByRole('button',{name:'Kafatası · 22 kemik',exact:true}).click();
    await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption('FMA53646');
    await page.getByRole('button',{name:'Seçili kemiği ayır',exact:true}).click();
    await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption('FMA53645');
    if(size.width===390) await page.getByRole('button',{name:'Yapıyı yalnız göster',exact:true}).click();
    await page.getByRole('button',{name:'DEV ONLY · QA sandbox −',exact:true}).click();
    await page.mouse.move(size.x,size.y);await page.mouse.down();await page.mouse.move(size.x+55,size.y+20,{steps:12});await page.mouse.up();await page.waitForTimeout(2400);
    await page.getByRole('button',{name:'DEV ONLY · QA sandbox +',exact:true}).click();
    let baseline=await snap();
    for(let settle=0,stable=0;settle<60&&stable<3;settle++){
      await page.waitForTimeout(100); const next=await snap();
      stable=delta(baseline.camera.position,next.camera.position)<1e-7 ? stable+1 : 0;
      baseline=next;
      if(settle===59&&stable<3)throw new Error('Orbit inertia did not settle');
    }
    await page.getByRole('button',{name:'Çalışma',exact:true}).click();
    await page.getByRole('region',{name:'Bölgesel çalışma',exact:true}).waitFor();
    const entered=await snap();
    const entryAngleDelta=delta(direction(baseline.camera),direction(entered.camera));
    if(entryAngleDelta>1e-3||JSON.stringify(entered.visibility.skull)!==JSON.stringify(baseline.visibility.skull)) throw new Error(JSON.stringify({name:'study entry',baseline,entered,entryAngleDelta}));
    await page.getByRole('button',{name:'Yeni çalışma',exact:true}).click();
    await page.getByRole('button',{name:'Yalnız yapıyı göster',exact:true}).click();
    await page.getByRole('combobox',{name:'Kafatası bakışı',exact:true}).selectOption('back');
    await page.getByRole('button',{name:'Kemiği yerine döndür',exact:true}).click();
    await page.getByRole('button',{name:'Sonraki',exact:true}).click();
    await page.getByRole('button',{name:'Kaydet ve Geri',exact:true}).click();
    await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).waitFor();
    await page.waitForTimeout(250);
    const study=check('skull study return',baseline,await snap());
    await page.getByRole('button',{name:'Sahneyi kaydet',exact:true}).click();
    const sceneName=`Orbit roundtrip ${size.width}`;
    const copies=page.getByRole('button',{name:`${sceneName} kaydını sil`,exact:true});while(await copies.count())await copies.last().click();
    await page.getByRole('textbox',{name:'Sahne adı',exact:true}).fill(sceneName);
    await page.getByRole('button',{name:'Bu sahneyi kaydet',exact:true}).click();
    await page.getByRole('button',{name:'Kayıtlı sahneleri kapat',exact:true}).click();
    await page.getByRole('combobox',{name:'Anatomi referansı',exact:true}).selectOption('inner-ear-reference');
    for(let load=0;load<200&&!await page.getByRole('button',{name:'Kayıtlı sahneler',exact:true}).isEnabled();load++) await page.waitForTimeout(100);
    const other=await snap();if(other.loadedReference!=='inner-ear-reference'||other.progress!==100)throw new Error('Other reference not loaded');
    await page.getByRole('button',{name:'Kayıtlı sahneler',exact:true}).click();
    await page.getByRole('button',{name:`Devam et · ${sceneName}`,exact:true}).click();
    await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).waitFor();await page.waitForTimeout(250);
    const reference=check('reference then saved scene',baseline,await snap());
    await page.reload();await page.getByRole('button',{name:'Kayıtlı sahneler',exact:true}).click();
    await page.getByRole('button',{name:`Devam et · ${sceneName}`,exact:true}).click();
    await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).waitFor();await page.waitForTimeout(250);
    const reload=check('reload then saved scene',baseline,await snap());
    await page.getByRole('button',{name:'Bildirimi kapat',exact:true}).click();
    await page.getByRole('button',{name:'DEV ONLY · QA sandbox −',exact:true}).click();
    await page.screenshot({path:`output/playwright/skull-roundtrip-${size.width}.png`});
    results.push({size,baseline,entryAngleDelta,study,other,reference,reload});
  }
  return results;
}
