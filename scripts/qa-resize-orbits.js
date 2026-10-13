async page => {
  const url = new URL(page.url());
  if (!['localhost','127.0.0.1','[::1]'].includes(url.hostname) || url.searchParams.get('devqa') !== '1') throw new Error('Local devqa fixture required');
  const cases = [
    ['male-body','skull'],
    ['female-pelvis','Sakrum (sağrı kemiği)'],
    ['inner-ear-reference','Sol koklea (salyangoz)'],
    ['lower-limb-nerve-reference','Sağ Kaval kemiği'],
    ['upper-limb-nerve-reference','Sağ Humerus'],
  ];
  const sizes = [[1000,700],[390,844],[844,390],[390,844],[320,568],[568,320],[320,568],[1200,942]];
  const button = name => page.getByRole('button',{name,exact:true}).click();
  const snap = async () => { await page.waitForTimeout(400); return JSON.parse(await page.getByTestId('qa-snapshot').textContent()); }; // Fixture snapshot refreshes every 350ms, even when landscape sheets overlap its controls.
  const vector = c => c.position.map((n,i)=>n-c.target[i]);
  const distance = c => Math.hypot(...vector(c));
  const direction = c => vector(c).map(n=>n/distance(c));
  const delta = (a,b)=>Math.max(...a.map((n,i)=>Math.abs(n-b[i])));
  const results = [];
  for (const [reference,name] of cases) {
    await page.setViewportSize({width:1200,height:942}); await page.reload();
    await page.getByRole('button',{name:'Kafatası · 22 kemik',exact:true}).waitFor();
    if (reference !== 'male-body') await page.getByRole('combobox',{name:'Anatomi referansı',exact:true}).selectOption(reference);
    if (name === 'skull') {
      await button('Kafatası · 22 kemik');
      await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption('FMA53646');
      await button('Seçili kemiği ayır');
      await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption('FMA53645');
    } else {
      await button('Anatomi ara');
      await page.getByRole('combobox',{name:'Anatomik yapı ara',exact:true}).fill(name);
      await page.getByRole('option',{name:`${name} 1 parça`,exact:true}).click();
    }
    for (const isolated of [false,true]) {
      if (isolated) await button('Yapıyı yalnız göster');
      await button('DEV ONLY · QA sandbox −');
      await page.mouse.move(525,380); await page.mouse.down(); await page.mouse.move(572,400,{steps:12}); await page.mouse.up();
      await page.mouse.wheel(0,-130);
      await page.mouse.move(540,380); await page.mouse.down({button:'right'}); await page.mouse.move(555,390,{steps:6}); await page.mouse.up({button:'right'});
      await page.waitForTimeout(2800);
      await button('DEV ONLY · QA sandbox +');
      const baseline = await snap(), steps = [];
      for (const [width,height] of sizes) {
        await page.setViewportSize({width,height}); await page.waitForTimeout(650);
        const after = await snap();
        const angleDelta = delta(direction(baseline.camera),direction(after.camera));
        const zoomRelativeDelta = Math.abs(distance(after.camera)/distance(baseline.camera)-1);
        const targetRelativeDelta = delta(baseline.camera.target,after.camera.target)/distance(baseline.camera);
        const stateMatches = baseline.reference===after.reference && baseline.conceptId===after.conceptId && JSON.stringify(baseline.visibility)===JSON.stringify(after.visibility);
        const canvas = await page.locator('canvas').boundingBox();
        const offsetValid = !after.camera.viewOffset || (after.camera.viewOffset.fullWidth===canvas.width && after.camera.viewOffset.fullHeight===canvas.height);
        steps.push({width,height,after,angleDelta,zoomRelativeDelta,targetRelativeDelta,stateMatches,offsetValid});
        if (isolated && (width===844 || width===568)) {
          await button('DEV ONLY · QA sandbox −');
          await page.screenshot({path:`output/playwright/resize-${reference}-${width}x${height}.png`});
          await button('DEV ONLY · QA sandbox +');
        }
      }
      results.push({reference,isolated,baseline,steps,passed:steps.every(s=>s.angleDelta<1e-3&&s.zoomRelativeDelta<1e-3&&s.targetRelativeDelta<1e-3&&s.stateMatches&&s.offsetValid)});
    }
  }
  return {passed:results.every(r=>r.passed),results};
}
