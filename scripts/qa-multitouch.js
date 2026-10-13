async page => {
  const url=new URL(page.url());
  if(!['localhost','127.0.0.1','[::1]'].includes(url.hostname)||url.searchParams.get('devqa')!=='1')throw new Error('Local devqa fixture required');
  const cdp=await page.context().newCDPSession(page);
  await cdp.send('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:5});
  const touch=(type,points)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:points.map(([id,x,y])=>({id,x,y,radiusX:3,radiusY:3,force:1}))});
  const snap=async()=>{await page.waitForTimeout(450);return JSON.parse(await page.getByTestId('qa-snapshot').textContent());};
  const dist=c=>Math.hypot(...c.position.map((n,i)=>n-c.target[i]));
  const dir=c=>c.position.map((n,i)=>(n-c.target[i])/dist(c));
  const delta=(a,b)=>Math.max(...a.map((n,i)=>Math.abs(n-b[i])));
  const sameState=(a,b)=>a.conceptId===b.conceptId&&JSON.stringify(a.visibility)===JSON.stringify(b.visibility)&&a.explorerHistory===b.explorerHistory;
  const poseDelta=(a,b)=>Math.max(delta(a.position,b.position),delta(a.target,b.target))/dist(a);
  const button=name=>page.getByRole('button',{name,exact:true}).click();
  const cases=[['male-body','skull'],['female-pelvis','Sakrum (sağrı kemiği)'],['inner-ear-reference','Sol temporal kemik (şakak kemiği)'],['lower-limb-nerve-reference','Sağ Kaval kemiği'],['upper-limb-nerve-reference','Sağ Humerus']];
  const results=[];
  try {
    for(const [width,height,isolated] of [[390,844,false],[320,568,true],[844,390,true]]) for(const [reference,name] of cases){
      await page.setViewportSize({width,height});await page.reload();
      await page.addStyleTag({content:'.dev-qa{visibility:hidden!important}'});
      if(reference!=='male-body')await page.getByRole('combobox',{name:'Anatomi referansı',exact:true}).selectOption(reference);
      if(name==='skull'){
        await button('Kafatası · 22 kemik');await page.getByRole('combobox',{name:'Kafatası kemiği',exact:true}).selectOption('FMA52734');
      }else{
        await button('Anatomi ara');await page.getByRole('combobox',{name:'Anatomik yapı ara',exact:true}).fill(name);await page.getByRole('option',{name:`${name} 1 parça`,exact:true}).click();
      }
      if(isolated)await button('Yapıyı yalnız göster');
      await page.locator('canvas').evaluate(canvas=>{
        canvas.dataset.touchEvents='[]';
        for(const type of ['pointerdown','pointerup','pointercancel']) canvas.addEventListener(type,event=>{
          const rows=JSON.parse(canvas.dataset.touchEvents);rows.push({type:event.type,pointerType:event.pointerType,id:event.pointerId,trusted:event.isTrusted});canvas.dataset.touchEvents=JSON.stringify(rows.slice(-100));
        });
      });
      const x=width===844?260:width/2,y=width===844?175:width===390?330:225;
      await touch('touchStart',[[1,x-12,y]]);
      for(let i=1;i<=8;i++){await touch('touchMove',[[1,x-12+i*3,y+i]]);await page.waitForTimeout(20);}
      await touch('touchEnd',[]);await page.waitForTimeout(2200);
      const baseline=await snap(), gestures=[];
      const gesture=async(name,r0,r1,dx,dy,reverse=false)=>{
        const before=await snap();
        await touch('touchStart',[[1,x-r0,y]]);await touch('touchStart',[[1,x-r0,y],[2,x+r0,y]]);
        for(let i=1;i<=12;i++){const t=i/12,r=r0+(r1-r0)*t;await touch('touchMove',[[1,x-r+dx*t,y+dy*t],[2,x+r+dx*t,y+dy*t]]);await page.waitForTimeout(20);}
        await page.waitForTimeout(1200);const held=await snap();
        await touch('touchEnd',[[reverse?1:2,reverse?x-r1+dx:x+r1+dx,y+dy]]);await page.waitForTimeout(150);await touch('touchEnd',[]);await page.waitForTimeout(700);const released=await snap();
        const record={name,before,held,released,releasePoseDelta:poseDelta(held.camera,released.camera),angleDelta:delta(dir(before.camera),dir(released.camera)),stateMatches:sameState(before,held)&&sameState(before,released),zoomRatio:dist(released.camera)/dist(before.camera),panRelative:delta(before.camera.target,released.camera.target)/dist(before.camera)};
        gestures.push(record);
      };
      await gesture('pinch zoom out',40,26,0,0);
      await gesture('pinch zoom in',26,40,0,0,true);
      await gesture('two-finger pan',32,32,12,6);
      const beforeTap=await snap();
      // Project the original focused center using the observed camera pose and source viewer FOV34.
      const c=beforeTap.camera,forward=dir(c).map(n=>-n),right=[-forward[2],0,forward[0]];
      const rl=Math.hypot(...right);for(let i=0;i<3;i++)right[i]/=rl;
      const up=[right[1]*forward[2]-right[2]*forward[1],right[2]*forward[0]-right[0]*forward[2],right[0]*forward[1]-right[1]*forward[0]];
      const v=baseline.camera.target.map((n,i)=>n-c.position[i]);const dot=(a,b)=>a.reduce((sum,n,i)=>sum+n*b[i],0);const depth=dot(v,forward),tan=Math.tan(34*Math.PI/360);
      const canvas=await page.locator('canvas').boundingBox();
      const px=canvas.width/2+dot(v,right)/depth/tan*canvas.height/2-(c.viewOffset?.offsetX??0);
      const py=canvas.height/2-dot(v,up)/depth/tan*canvas.height/2-(c.viewOffset?.offsetY??0);
      await page.screenshot({path:`output/playwright/touch-${reference}-${width}-before-tap.png`});
      await touch('touchStart',[[1,px,py]]);await touch('touchEnd',[]);await page.waitForTimeout(900);const tapped=await snap();
      // Empty-space tap must not clear selection or move the camera.
      await touch('touchStart',[[1,22,height===390?180:190]]);await touch('touchEnd',[]);await page.waitForTimeout(500);const empty=await snap();
      const events=JSON.parse(await page.locator('canvas').getAttribute('data-touch-events'));
      const picked=tapped.explorerHistory===beforeTap.explorerHistory+1;
      const passed=gestures.every(g=>g.releasePoseDelta<1e-3&&g.angleDelta<1e-3&&g.stateMatches)&&gestures[0].zoomRatio>1.1&&gestures[1].zoomRatio<0.9&&gestures[2].panRelative>0.001&&picked&&poseDelta(beforeTap.camera,tapped.camera)<1e-3&&JSON.stringify(beforeTap.camera.viewOffset)===JSON.stringify(tapped.camera.viewOffset)&&sameState(tapped,empty)&&poseDelta(tapped.camera,empty.camera)<1e-3&&events.every(e=>e.pointerType==='touch'&&e.trusted);
      results.push({reference,width,height,isolated,baseline,gestures,tap:{px,py,picked,beforeTap,tapped,empty,poseDelta:poseDelta(beforeTap.camera,tapped.camera)},events,passed});
    }
  }catch(error){return {passed:false,error:String(error),results};}finally{await cdp.send('Emulation.setTouchEmulationEnabled',{enabled:false});await cdp.detach();}
  return {passed:results.every(r=>r.passed),results};
}
