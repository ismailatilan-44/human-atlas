async (page) => {
  await page.reload();
  await page.setViewportSize({width:1200,height:942});
  await page.getByRole('button',{name:'Kafatası · 22 kemik',exact:true}).click();
  await page.getByRole('button',{name:'Yapıyı yalnız göster',exact:true}).click();
  await page.mouse.move(535,410); await page.mouse.down();
  await page.mouse.move(645,450,{steps:12}); await page.mouse.up();
  await page.waitForTimeout(2200); // Allow OrbitControls damping to settle before comparing poses.

  const snap = async () => {
    await page.getByRole('button', { name: 'Snapshot', exact: true }).click();
    return JSON.parse(await page.getByTestId('qa-snapshot').textContent());
  };
  const direction = camera => { const v = camera.position.map((n,i) => n-camera.target[i]); const l=Math.hypot(...v); return v.map(n=>n/l); };
  const same = (a,b) => Math.max(...a.map((n,i)=>Math.abs(n-b[i]))) < 1e-5;
  const before = await snap();
  await page.mouse.click(540,375);
  const picked = await snap();
  if(picked.conceptId==='atlas:skull-bones') throw new Error('No geometry picked');
  if(!same(before.camera.position,picked.camera.position)||!same(before.camera.target,picked.camera.target)) throw new Error('Canvas pick changed camera');
  await page.screenshot({path:'output/playwright/skull-orbit-pick-after.png'});
  await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption('FMA53646');
  const small = await snap();
  if(!same(direction(before.camera),direction(small.camera))) throw new Error('Small bone refit reset orbit');
  await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption('FMA52734');
  const large = await snap();
  if(!same(direction(before.camera),direction(large.camera))) throw new Error('Large bone refit reset orbit');
  await page.getByRole('combobox',{name:'Kafatası bakışı',exact:true}).selectOption('back');
  const explicit = await snap();
  if(!same(direction(explicit.camera),[0,0,-1])) throw new Error('Explicit view did not change direction');
  await page.getByRole('button',{name:'Önceki görünüme dön',exact:true}).click();
  const back = await snap();
  if(!same(back.camera.position,large.camera.position)||!same(back.camera.target,large.camera.target)) throw new Error('Back failed to restore orbit');
  return {before,picked,small,large,explicit,back};
}
