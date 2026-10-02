import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
const forbidden = ['DEV ONLY', 'atlas-devqa-sandbox', 'dev-qa-panel', 'dev-qa.css', 'devqa', 'Reload + resume', 'Replay scenario'];
function inspect(dir) {
  for (const item of readdirSync(dir, { withFileTypes:true })) {
    const path = join(dir, item.name);
    if (item.isDirectory()) inspect(path);
    else if (/\.(js|css|html|map)$/.test(path)) {
      const contents = readFileSync(path, 'utf8');
      for (const marker of forbidden) if (contents.includes(marker)) throw new Error(`Development QA marker ${marker} leaked into ${path}`);
    }
  }
}
inspect('dist');
console.log('Production QA exclusion: no panel, controls, sandbox namespace or activation flag in dist JS/CSS/HTML/maps.');
