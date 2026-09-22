/** Audit only direct coverage bindings through the real runtime label dispatcher. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { build } from 'esbuild';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../../..');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'atlas-coverage-labels-'));
const bundle=path.join(temp,'labels.mjs');
try {
 await build({entryPoints:[path.join(root,'app/reference-datasets.ts')],outfile:bundle,bundle:true,platform:'node',format:'esm',logLevel:'silent'});
 const {datasetLabel}=await import(pathToFileURL(bundle).href);
 const coverage=JSON.parse(fs.readFileSync(path.join(root,'data/anatomy/coverage.json')));
 const rows=[];
 for(const region of coverage.regions)for(const target of region.targets){
  const bindings=target.currentBindings.map(b=>({datasetId:'male-body',id:b.conceptId,name:b.sourceName,geometryPartIds:b.geometryPartIds}));
  const ref=target.separateReference;
  if(ref){const atlas=JSON.parse(fs.readFileSync(path.join(root,'public'+ref.manifest)));for(const id of ref.conceptIds??[ref.conceptId]){const c=atlas.concepts.find(c=>c.id===id);if(!c)throw new Error('Unresolved reference '+id);bindings.push({datasetId:ref.datasetId,id,name:c.name,geometryPartIds:c.elements});}}
  for(const binding of bindings){const current={},fallback={};for(const language of ['tr','en','la']){current[language]=datasetLabel(binding.datasetId,binding.id,binding.name,language);fallback[language]=datasetLabel(binding.datasetId,binding.id,'__NO_REVIEWED_LABEL__',language)==='__NO_REVIEWED_LABEL__';}rows.push({...binding,targetId:target.id,regionId:region.id,current,fallback});}
 }
 const result={scope:'65 coverage targets, only direct currentBindings/separateReference concept IDs, no descendant expansion',targets:coverage.regions.reduce((n,r)=>n+r.targets.length,0),uniqueConceptBindings:rows.length,counts:Object.fromEntries(['tr','en','la'].map(l=>[l,rows.filter(r=>r.fallback[l]).length])),entries:rows};
 const output = process.argv[2] ?? 'ui-label-audit-after.json';
 if (path.basename(output) !== output || output === 'ui-label-audit.json') throw new Error('Use a new audit filename; the original snapshot is frozen');
 fs.writeFileSync(path.join(here,output),JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({targets:result.targets,concepts:rows.length,fallbackCounts:result.counts}));
} finally {fs.rmSync(temp,{recursive:true,force:true});}
