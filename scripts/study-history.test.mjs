import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';
const load = async path => {
 const js=ts.transpileModule(readFileSync(path,'utf8'),{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText;
 return import(`data:text/javascript;base64,${Buffer.from(js).toString('base64')}`);
};
const {newHistory,review,dueItems,validateHistory,loadStudy,saveStudy,studyStorageKey}=await load('app/study-history.ts');
const {startStudy,studyTransition:step}=await load('app/study-session.ts');
const pack={id:'test',datasetId:'ref',version:'v1',items:[{id:'card',conceptId:'bone'}]};
const DAY=86400000, at=Date.parse('2026-03-08T01:30:00Z');
const fresh=()=>newHistory(pack,startStudy(1),at);
const event=(id,outcome,time=at)=>({id,itemId:'card',outcome,at:time});
test('scheduler correct intervals, early practice, mastery, cap and UTC across DST',()=>{
 let h=review(fresh(),event('1','correct'));assert.equal(h.cards.card.due,at+DAY);
 h=review(h,event('early','correct',at+60000));assert.equal(h.cards.card.streak,1);assert.equal(h.cards.card.due,at+DAY);
 h=review(h,event('2','correct',at+DAY));assert.equal(h.cards.card.streak,2);assert.equal(h.cards.card.due,at+4*DAY);
 h=review(h,event('3','correct',at+4*DAY));assert.equal(h.cards.card.streak,3);assert.equal(h.cards.card.due,at+11*DAY);
 for(let i=0;i<10;i++){const now=h.cards.card.due;h=review(h,event('later'+i,'correct',now));assert.ok(h.cards.card.due-now<=30*DAY);}
 assert.equal(h.cards.card.streak,5);
});
test('wrong and hint reset interval, skip preserves, duplicate and bad clock are safe',()=>{
 for(const outcome of ['wrong','hint']) {const h=review(fresh(),event('1',outcome));assert.equal(h.cards.card.streak,0);assert.equal(h.cards.card.due,at+600000);}
 let h=review(fresh(),event('1','correct'));
 assert.equal(review(h,event('1','wrong')),h);
 assert.equal(review(h,event('invalid','correct',NaN)),h);
 const card=h.cards.card;h=review(h,event('skip','skip',at+1000));assert.deepEqual(h.cards.card,card);
 h=review(h,event('backwards','wrong',at-DAY));assert.equal(h.cards.card.last,at+1000);assert.equal(h.cards.card.due,at+601000);
 assert.deepEqual(dueItems(h,pack,at),[]);assert.deepEqual(dueItems(h,pack,at+601000),[0]);
});
test('hint does not become first-attempt success, explicit undo restores score and scheduling atomically',()=>{
 let h=fresh();h.session=step(h.session,{type:'next'});h.session=step(h.session,{type:'hint'});
 const undo=h;h=review(h,event('answer','hint'));h={...h,session:step(h.session,{type:'answer',correct:true,value:'bone'})};
 assert.equal(h.session.first[0],'wrong');assert.deepEqual(h.session.success,[0]);assert.equal(h.cards.card.streak,0);
 h=undo;assert.deepEqual(h.session.first,{});assert.deepEqual(h.cards,{});assert.equal(h.events.length,0);
});
test('storage resumes session and rejects absent versions, stale concepts and invalid state',()=>{
 const h=fresh();h.session=step(h.session,{type:'next'});
 assert.ok(validateHistory(JSON.parse(JSON.stringify(h)),pack));
 assert.ok(!validateHistory(h,{...pack,version:'v2'}));assert.ok(!validateHistory(h,{...pack,version:undefined}));
 assert.ok(!validateHistory(h,{...pack,items:[{id:'card',conceptId:'changed'}]}));
 for(const session of [{...h.session,index:100},{...h.session,queue:[]},{...h.session,queue:[99]},{...h.session,success:[99]},{...h.session,answer:'stale'}]) assert.ok(!validateHistory({...h,session},pack));
 const values=new Map();const storage={getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v)};
 assert.ok(saveStudy(storage,pack,h));assert.deepEqual(loadStudy(storage,pack).history,h);
 assert.ok(saveStudy(storage,pack,{...h,isolated:true}));storage.setItem(studyStorageKey(pack),'broken');
 assert.deepEqual(loadStudy(storage,pack).history,h);assert.match(loadStudy(storage,pack).notice,/yedek/);
 values.clear();storage.setItem(studyStorageKey(pack),'broken');assert.ok(!loadStudy(storage,pack).history);
 assert.ok(saveStudy(storage,pack,h));assert.equal(storage.getItem(studyStorageKey(pack)+':recovery'),'broken');
 const blocked={getItem(){throw Error('disabled')},setItem(){throw Error('quota')}};
 assert.ok(loadStudy(blocked,pack).notice);assert.equal(saveStudy(blocked,pack,h),false);
});

test('bounded audit log continues accepting distinct events beyond 500 reviews',()=>{
 let h=fresh();
 for(let i=0;i<520;i++) h=review(h,event(`unique-${i}`,'wrong',at+i*1000));
 assert.equal(h.events.length,500);assert.equal(h.cards.card.reviews,520);
 assert.equal(h.cards.card.last,at+519000);
});
test('full content identity invalidates changed source evidence and undo survives storage reload',()=>{
 const sourcePack={...pack,items:[{...pack.items[0],sourceObject:'Bone.r',evidence:[{sourceId:'source',locator:'v1'}]}]};
 let h=newHistory(sourcePack,startStudy(1),at);h.session=step(h.session,{type:'next'});
 const before=h;h={...review(h,event('1','wrong')),session:step(h.session,{type:'answer',correct:false,value:null}),undo:before};
 assert.ok(validateHistory(h,sourcePack));
 const values=new Map();const storage={getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v)};
 saveStudy(storage,sourcePack,h);assert.deepEqual(loadStudy(storage,sourcePack).history.undo,before);
 assert.ok(!validateHistory(h,{...sourcePack,items:[{...sourcePack.items[0],evidence:[{sourceId:'source',locator:'changed'}]}]}));
 assert.ok(!validateHistory({...h,undo:{...before,undo:before}},sourcePack));
});
