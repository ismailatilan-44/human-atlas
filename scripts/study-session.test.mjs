import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import ts from 'typescript';
const js = ts.transpileModule(readFileSync('app/study-session.ts', 'utf8'), { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }).outputText;
const { startStudy, studyTransition: step } = await import(`data:text/javascript;base64,${Buffer.from(js).toString('base64')}`);
const json = p => JSON.parse(readFileSync(p, 'utf8'));
test('every scored item has one same-side source surface and exact verified label evidence', () => {
 const pack = json('data/study/right-ankle-v1.json');
 const atlas = json('public/models/lower-limb-nerve-reference/atlas.json');
 const metadata = json('data/anatomy/lower-limb-reference.json');
 assert.equal(pack.items.length, 9); assert.equal(new Set(pack.items.map(i => i.id)).size, 9);
 for (const item of pack.items) {
  const concept = atlas.concepts.find(c => c.id === item.conceptId);
  assert.equal(concept.elements.length, 1);
  const label = metadata.labels.find(l => l.ids.includes(item.conceptId));
  assert.equal(label.side, 'right'); assert.equal(label.componentRole, 'bone_context');
  assert.equal(label.terminologyStatus, 'verified_against_pinned_table'); assert.ok(label.la);
  assert.equal(item.sourceObject, label.sourceObject); assert.deepEqual(item.evidence, label.evidence);
 }
});
test('wrong, skipped and repeated submissions preserve first attempt through repeated retry rounds', () => {
 let s = startStudy(3);
 assert.equal(step(s, {type:'answer',value:'x',correct:true}), s);
 for(let i=0;i<3;i++) s=step(s,{type:'next'});
 s=step(s,{type:'answer',value:'wrong',correct:false});
 assert.equal(step(s,{type:'answer',value:'correct',correct:true}),s);
 s=step(s,{type:'next'}); s=step(s,{type:'answer',value:null,correct:false});
 s=step(s,{type:'next'}); s=step(s,{type:'answer',value:'correct',correct:true});
 s=step(s,{type:'next'}); assert.equal(s.phase,'summary');
 const first={...s.first}; assert.deepEqual(first,{0:'wrong',1:'skip',2:'correct'});
 s=step(s,{type:'retry'}); assert.deepEqual(s.queue,[0,1]);
 s=step(s,{type:'answer',value:'correct',correct:true});s=step(s,{type:'next'});
 s=step(s,{type:'answer',value:null,correct:false});s=step(s,{type:'next'});
 s=step(s,{type:'retry'});assert.deepEqual(s.queue,[1]);
 s=step(s,{type:'answer',value:'correct',correct:true});s=step(s,{type:'next'});
 assert.deepEqual(s.first,first);assert.equal(s.success.length,3);assert.equal(step(s,{type:'retry'}),s);
 assert.deepEqual(startStudy(3).first,{});
});
