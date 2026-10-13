async page => {
  if(new URL(page.url()).searchParams.get('devqa')!=='1') throw new Error('Fixture required');
  await page.setViewportSize({width:1200,height:942}); await page.reload();
  const button=name=>page.getByRole('button',{name,exact:true}).click();
  const snap=async()=>{await page.waitForTimeout(450);return JSON.parse(await page.getByTestId('qa-snapshot').textContent());};
  const delta=(a,b)=>Math.max(...a.map((n,i)=>Math.abs(n-b[i])));
  const distance=c=>Math.hypot(...c.position.map((n,i)=>n-c.target[i]));
  const checks=[];
  const resizeCheck=async name=>{
    const before=await snap();
    for(const [width,height] of [[844,390],[390,844],[1200,942]]){
      await page.setViewportSize({width,height});await page.waitForTimeout(700);const after=await snap();
      const poseDelta=Math.max(delta(before.camera.position,after.camera.position),delta(before.camera.target,after.camera.target))/distance(before.camera);
      const stateMatches=before.conceptId===after.conceptId&&JSON.stringify(before.visibility)===JSON.stringify(after.visibility);
      if(poseDelta>1e-3||!stateMatches)throw new Error(JSON.stringify({name,width,before,after,poseDelta,stateMatches}));
      checks.push({name,width,height,poseDelta,stateMatches});
    }
  };
  await page.getByRole('combobox',{name:'Anatomi referansı',exact:true}).selectOption('female-pelvis');
  await page.getByRole('button',{name:'Kayıtlı sahneler',exact:true}).click();await button('Kayıtlı sahneleri kapat');
  await button('DEV ONLY · QA sandbox −');
  await page.mouse.move(535,380);await page.mouse.down();await page.mouse.move(595,410,{steps:12});await page.mouse.up();await page.mouse.wheel(0,-100);await page.waitForTimeout(2600);
  await button('DEV ONLY · QA sandbox +');await resizeCheck('unfocused scene');
  await page.getByRole('slider',{name:'Explode anatomy',exact:true}).press('End');await page.waitForTimeout(2200);
  await button('DEV ONLY · QA sandbox −');await page.mouse.move(520,390);await page.mouse.down();await page.mouse.move(540,405,{steps:6});await page.mouse.up();await page.mouse.wheel(0,-80);await page.waitForTimeout(2600);await button('DEV ONLY · QA sandbox +');
  await resizeCheck('settled exploded grid');
  await button('Görünümü ve katmanları sıfırla');await page.waitForTimeout(1800);
  await button('Anatomi ara');await page.getByRole('option',{name:'Sakrum (sağrı kemiği) 1 parça',exact:true}).click();await button('Yapıyı yalnız göster');
  await button('DEV ONLY · QA sandbox −');await page.mouse.move(520,390);await page.mouse.down();await page.mouse.move(570,410,{steps:8});await page.mouse.up();await page.mouse.wheel(0,-120);await page.waitForTimeout(2600);await button('DEV ONLY · QA sandbox +');
  await button('Sahneyi kaydet');
  const sceneName='Resize fixture';const old=page.getByRole('button',{name:`${sceneName} kaydını sil`,exact:true});while(await old.count())await old.last().click();
  await page.getByRole('textbox',{name:'Sahne adı',exact:true}).fill(sceneName);await button('Bu sahneyi kaydet');await button(`Devam et · ${sceneName}`);await page.waitForTimeout(450);
  await resizeCheck('restored isolated scene');
  const beforeFocus=await snap();await button('Odaklan');const focused=await snap();
  if(Math.abs(distance(beforeFocus.camera)-distance(focused.camera))<1e-4)throw new Error('Focus did not release resize preservation');
  await button('Önceki görünüme dön');const undo=await snap();
  if(delta(beforeFocus.camera.position,undo.camera.position)>1e-5 || delta(beforeFocus.camera.target,undo.camera.target)>1e-5)throw new Error(JSON.stringify({name:'Focus undo failed',beforeFocus,undo}));
  await page.getByRole('button',{name:'back view',exact:true}).click();const back=await snap();
  if(Math.abs((back.camera.position[2]-back.camera.target[2])/distance(back.camera)+1)>1e-5)throw new Error('Named view blocked');
  return {passed:true,checks,beforeFocus,focused,undo,back};
}
