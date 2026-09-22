// Execute the real application adapter, not a duplicate of its override table.
import {createServer} from 'vite';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=new URL('../../../',import.meta.url);
const server=await createServer({root:fileURLToPath(root),configFile:false,optimizeDeps:{noDiscovery:true},server:{middlewareMode:true},appType:'custom'});
try {
 const {prepareAtlas}=await server.ssrLoadModule('/app/atlas-metadata.ts');
 const rawBytes=await readFile(new URL('public/models/atlas.json',root));
 const prepareBytes=await readFile(new URL('app/atlas-metadata.ts',root));
 const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
 const raw=JSON.parse(rawBytes),prepared=prepareAtlas(raw);
 const original=new Map(raw.parts.map(p=>[p.id,p]));
 const evidence={baseManifestSha256:sha(rawBytes),prepareAtlasSha256:sha(prepareBytes),parts:prepared.parts.map(p=>({id:p.id,conceptId:p.conceptId,name:p.name,rawSystem:original.get(p.id).system,activeSystem:p.system}))};
 await writeFile(new URL('active-systems-snapshot.json',import.meta.url),JSON.stringify(evidence,null,2)+'\n');
 console.log(`Snapshotted ${prepared.parts.length} parts using the active prepareAtlas.`);
} finally {await server.close();}
