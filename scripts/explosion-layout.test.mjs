import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import ts from 'typescript';
import {PerspectiveCamera,Vector3} from 'three';
const js=ts.transpileModule(readFileSync('app/explosion-layout.ts','utf8'),{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText;
const {createExplosionLayout,createCameraExplosionLayout,explosionMinimumDistance}=await import(`data:text/javascript;base64,${Buffer.from(js).toString('base64')}`);
const parts=Array.from({length:35},(_,i)=>({id:`p${i}`,system:'skeletal',bounds:[[i*.01,-.1,-.3],[i*.01+.02+(i%5)*.12,.02+(i%3)*.23,.05+(i%7)*.19]]}));
function checkProjection(group,direction,distance,pan,aspect=1){
 const layout=createCameraExplosionLayout(group,aspect,direction,distance,pan);
 const target=new Vector3(...pan),camera=new PerspectiveCamera(34,aspect,.005,10000);
 camera.position.copy(target).addScaledVector(new Vector3(...direction).normalize(),layout.actualDistance);
 camera.lookAt(target);camera.updateMatrixWorld();
 const rectangles=[];
 for(const p of group){
  const center=p.bounds[0].map((v,i)=>(v+p.bounds[1][i])/2),destination=layout.centers.get(p.id);
  const points=[];
  for(const x of [p.bounds[0][0],p.bounds[1][0]])for(const y of [p.bounds[0][1],p.bounds[1][1]])for(const z of [p.bounds[0][2],p.bounds[1][2]]){
   const world=new Vector3(x-center[0]+destination[0],y-center[1]+destination[1],z-center[2]+destination[2]);
   const point=world.project(camera);assert(Number.isFinite(point.x)&&Number.isFinite(point.y));assert(point.z>=-1&&point.z<=1,'corner crosses clipping plane');points.push(point);
  }
  rectangles.push({id:p.id,left:Math.min(...points.map(p=>p.x)),right:Math.max(...points.map(p=>p.x)),top:Math.max(...points.map(p=>p.y)),bottom:Math.min(...points.map(p=>p.y))});
 }
 for(let i=0;i<rectangles.length;i++)for(let j=i+1;j<rectangles.length;j++){
  const a=rectangles[i],b=rectangles[j];
  assert(a.right<=b.left+1e-9||b.right<=a.left+1e-9||a.top<=b.bottom+1e-9||b.top<=a.bottom+1e-9,`${a.id} overlaps ${b.id}: ${JSON.stringify({direction,distance,pan,a,b})}`);
 }
 return {layout,rectangles};
}
test('camera-facing packing prevents actual perspective overlap across angles, zoom and pan',()=>{
 for(const direction of [[0,0,1],[0,0,-1],[1,0,0],[-1,0,0],[.7,.4,-.5],[.0001,1,.0001],[0,-1,.001]])
 for(const distance of [.15,1.5,8,30])for(const pan of [[0,0,0],[2,-1,.3],[-4,3,-.7]])for(const aspect of [.46,1.7])
  checkProjection(parts,direction,distance,pan,aspect);
});
test('packing does not cancel a lateral pan and preserves stable source identities',()=>{
 const one=[parts[0]],before=checkProjection(one,[0,0,1],8,[0,0,0]),after=checkProjection(one,[0,0,1],8,[1,0,0]);
 assert(after.rectangles[0].right<before.rectangles[0].left,'inventory should move left when camera pans right');
 assert.deepEqual([...before.layout.centers.keys()],['p0']);
 const clone=structuredClone(parts);createCameraExplosionLayout(parts,1,[.7,.3,1],8);assert.deepEqual(parts,clone);
});
test('legacy cell packing and empty camera layout remain supported',()=>{
 assert.equal(createExplosionLayout(parts,1).cells.size,parts.length);
 const empty=createCameraExplosionLayout([],1,[0,0,1],4);assert.equal(empty.width,0);assert.equal(empty.height,0);assert.equal(empty.centers.size,0);
 assert(explosionMinimumDistance(parts,[0,0,1])>.3);
});
test('real atlas depth-heavy bounds stay separated at fitted, close and panned poses',()=>{
 const atlas=JSON.parse(readFileSync('public/models/atlas.json','utf8'));
 for(const direction of [[.7,.3,1],[1,0,0],[0,1,.001]]){
  const group=atlas.parts.filter(p=>p.system==='skeletal');
  for(const [distance,pan] of [[20,[0,0,0]],[2,[.5,-.4,0]]])checkProjection(group,direction,distance,pan,.46);
 }
});
