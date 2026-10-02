import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';
const js = ts.transpileModule(readFileSync('app/saved-scenes.ts','utf8'), { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }).outputText;
const api = await import(`data:text/javascript;base64,${Buffer.from(js).toString('base64')}`);
const atlas = { datasetId:'male-body', version:'4.0', parts:[{id:'p1',bounds:[[0,0,0],[1,1,1]]}],concepts:[{id:'c1',elements:['p1']}],chunks:[] };
const concepts = new Map([['c1',atlas.concepts[0]]]);
const state = { explode:0.25, visible:['skeletal'],selected:['p1'],hidden:[],isolate:true,view:'front',rotate:false,focused:true,ghost:true,concealLabels:true,reset:9 };
const camera = {position:[1,2,3],target:[0,0,0],viewOffset:{fullWidth:390,fullHeight:844,width:390,height:844,offsetX:0,offsetY:120}};
const create = () => api.captureScene({atlas,dataset:'male-body',state,camera,chosenId:'c1',details:true,language:'la',name:' Test '},new Date('2026-10-02T10:00:00Z'),'one');
function storage() { const data=new Map(); return {data,getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,v)}; }
test('scene roundtrip preserves camera, stable IDs, visibility and label language without transient resets',()=>{
 const scene=create(), store=storage();
 assert.equal(api.writeSceneStore(store,[scene]),null);
 const saved=api.loadSceneStore(store).scenes[0];
 assert.deepEqual(saved,scene); assert.equal(saved.name,'Test');assert.equal(saved.state.reset,0);
 assert.deepEqual(saved.camera,camera); assert.equal(saved.language,'la');assert.equal(saved.state.concealLabels,true);
 assert.equal(api.validateScene(saved,atlas,concepts),null);
 state.visible.push('nervous');assert.deepEqual(saved.state.visible,['skeletal']);state.visible.pop();
});
test('content and identity changes never silently restore a stale scene',()=>{
 const scene=create();
 assert.match(api.validateScene({...scene,contentVersion:''},atlas,concepts),/geçersiz/);
 assert.match(api.validateScene(scene,{...atlas,version:'next'},concepts),/sürümü/);
 assert.match(api.validateScene(scene,{...atlas,parts:[{...atlas.parts[0],bounds:[[0,0,0],[2,2,2]]}]},concepts),/sürümü/);
 assert.match(api.validateScene({...scene,dataset:'female-pelvis'},atlas,concepts),/referansa/);
 assert.match(api.validateScene({...scene,chosenId:'missing'},atlas,concepts),/kimliği/);
 assert.match(api.validateScene({...scene,state:{...scene.state,hidden:['missing']}},atlas,concepts),/kimliği/);
});
test('malformed schema, invalid numeric camera, selection duplicates and missing fields are rejected',()=>{
 const scene=create();
 for(const broken of [{...scene,schema:2},{...scene,state:{...scene.state,explode:2}},{...scene,camera:{...camera,position:[0,0,0]}},{...scene,camera:{...camera,position:[NaN,2,3]}},{...scene,camera:{...camera,viewOffset:{...camera.viewOffset,width:0}}},{...scene,state:{...scene.state,visible:['unknown']}},{...scene,state:{...scene.state,selected:['p1','p1']}},{...scene,state:{...scene.state,hidden:undefined}}]) assert.equal(api.isSavedScene(broken),false);
});
test('corrupt data can recover previous good backup and unreadable original is retained on repair',()=>{
 const store=storage(), scene=create();
 api.writeSceneStore(store,[scene]);api.writeSceneStore(store,[]);
 store.setItem(api.SCENE_STORAGE_KEY,'{broken');
 assert.deepEqual(api.loadSceneStore(store).scenes,[scene]);assert.equal(api.loadSceneStore(store).recovered,true);
 assert.equal(api.writeSceneStore(store,[scene]),null);
 assert.equal(store.getItem(`${api.SCENE_STORAGE_KEY}.recovery`),'{broken');
 assert.equal(api.loadSceneStore(store).error,null);
});
test('quota or denied storage reports failure while last valid primary survives',()=>{
 const store=storage(), scene=create();api.writeSceneStore(store,[scene]);
 const original=store.getItem(api.SCENE_STORAGE_KEY);
 const quota={getItem:store.getItem,setItem(){throw new Error('quota')}};
 assert.match(api.writeSceneStore(quota,[]),/Kaydedilemedi/);assert.equal(store.getItem(api.SCENE_STORAGE_KEY),original);
 assert.match(api.loadSceneStore({getItem(){throw new Error('denied')}}).error,/erişilemiyor/);
});
test('storage bounds reject missing versions, duplicate slots and overlarge arrays',()=>{
 const store=storage(), scene=create();
 for(const scenes of [[scene,scene],Array.from({length:13},(_,i)=>({...scene,id:String(i)})),[{...scene,contentVersion:undefined}]]) assert.ok(api.writeSceneStore(store,scenes));
 assert.equal(store.getItem(api.SCENE_STORAGE_KEY),null);
});
