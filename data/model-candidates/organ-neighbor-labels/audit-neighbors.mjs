import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {build} from 'esbuild';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../../..');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'atlas-organ-labels-'));
try {
 const entry=path.join(temp,'entry.ts');
 fs.writeFileSync(entry,`export {relationshipsFor} from ${JSON.stringify(path.join(root,'app/knowledge.ts'))};\nexport {datasetLabel} from ${JSON.stringify(path.join(root,'app/reference-datasets.ts'))};\nexport {mergeAtlas} from ${JSON.stringify(path.join(root,'app/load-atlas.ts'))};`);
 const bundle=path.join(temp,'bundle.mjs');
 await build({entryPoints:[entry],outfile:bundle,bundle:true,platform:'node',format:'esm',logLevel:'silent'});
 const {relationshipsFor,datasetLabel,mergeAtlas}=await import(pathToFileURL(bundle));
 const coverage=JSON.parse(fs.readFileSync(path.join(root,'data/anatomy/coverage.json')));
 const graph=JSON.parse(fs.readFileSync(path.join(root,'data/anatomy/explorer.json')));
 let base=JSON.parse(fs.readFileSync(path.join(root,'public/models/atlas.json')));
 const registry=JSON.parse(fs.readFileSync(path.join(root,'public/models/extensions/index.json')));
 for(const url of registry.manifests)base=mergeAtlas(base,JSON.parse(fs.readFileSync(path.join(root,'public'+url))));
 const labels=JSON.parse(fs.readFileSync(path.join(root,'data/anatomy/labels.json')));
 const reviewedLabels=new Map(labels.entries.flatMap(e=>e.ids.map(id=>[id,e])));
 const entities=new Map(base.concepts.map(e=>[e.id,{...e,geometryPartIds:e.elements}]));
 for(const e of graph.entities)if(!entities.has(e.id))entities.set(e.id,e);
 const conceptMap=new Map([...entities.values()].map(e=>[e.id,{id:e.id,name:e.name,elements:e.geometryPartIds}]));
 const endpoints=new Map(),seeds=[],references=[];
 for(const region of coverage.regions.filter(r=>['thorax','abdomen-pelvis'].includes(r.id)))for(const target of region.targets){
  if(target.separateReference){references.push({targetId:target.id,...target.separateReference,relations:[],reason:'Reference datasets have no male graph relationship panel; no cross-dataset traversal'});}
  for(const binding of target.currentBindings){
   seeds.push({id:binding.conceptId,targetId:target.id,regionId:region.id});
   for(const relation of relationshipsFor(binding.conceptId,conceptMap)){
    const id=relation.otherId,entity=entities.get(id);
    if(!endpoints.has(id))endpoints.set(id,{id,name:entity?.name??relation.name,geometryPartIds:entity?.geometryPartIds??[],current:{},fallback:{},via:[]});
    const row=endpoints.get(id);
    row.via.push({seedId:binding.conceptId,targetId:target.id,regionId:region.id,relationId:relation.id,predicate:relation.predicate,subject:relation.subject,object:relation.object});
    for(const l of ['tr','en','la']){row.current[l]=datasetLabel('male-body',id,row.name,l);row.fallback[l]=datasetLabel('male-body',id,'__MISSING__',l)==='__MISSING__';}
   }
  }
 }
 const entries=[...endpoints.values()];
 for(const e of entries)e.reviewedLabelMissing=Object.fromEntries(['tr','en','la'].map(l=>[l,!reviewedLabels.get(e.id)?.[l]]));
 const reviewedMissingCounts=Object.fromEntries(['tr','en','la'].map(l=>[l,entries.filter(e=>e.reviewedLabelMissing[l]).length]));
 const result={scope:'One relationshipsFor step from thorax/abdomen-pelvis currentBindings; separate datasets do not traverse the male graph. Reviewed-label availability is separate from display fallback: source groups retain their English qualifier when Latin is absent.',seeds,references,endpointCount:entries.length,missingTrOrLa:entries.filter(x=>x.fallback.tr||x.fallback.la).length,reviewedMissingCounts,entries};
 fs.writeFileSync(path.join(here,process.argv.includes('--after') ? 'ui-neighbor-audit-after.json' : 'ui-neighbor-audit.json'),JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({seedCount:seeds.length,endpointCount:result.endpointCount,displayFallbackCount:result.missingTrOrLa,reviewedMissingCounts}));
 for(const e of entries.filter(x=>x.fallback.tr||x.fallback.la))console.log(e.id+' | '+e.name+' | '+e.geometryPartIds.length+' | '+[...new Set(e.via.map(v=>v.targetId))].join(','));
}finally{fs.rmSync(temp,{recursive:true,force:true});}
