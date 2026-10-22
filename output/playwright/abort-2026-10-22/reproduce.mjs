import http from 'node:http';
const html=`<!doctype html><meta charset="utf-8"><title>Abort tanısı</title><h1>Bağımsız fetch iptal testi</h1><button id="headers">Yanıt gelmeden iptal</button><button id="body">Gövde okunurken iptal</button><pre id="report">Hazır</pre><script>
const origins=new WeakMap();const then=Promise.prototype.then;Promise.prototype.then=function(...args){const next=Reflect.apply(then,this,args);origins.set(next,new Error('Promise branch created').stack);return next;};
const rows=[];const show=()=>document.querySelector('#report').textContent=JSON.stringify(rows,null,2);
addEventListener('unhandledrejection',e=>{rows.push({unhandled:e.reason?.name,message:e.reason?.message,stack:e.reason?.stack,origin:origins.get(e.promise)||null});show();});
async function run(path){const a=new AbortController();setTimeout(()=>a.abort(),200);try{const r=await fetch(path,{signal:a.signal});rows.push({headers:true});show();await r.arrayBuffer();rows.push({success:true});}catch(e){rows.push({caught:e.name});}show();}
document.querySelector('#headers').onclick=()=>{void run('/headers')};document.querySelector('#body').onclick=()=>{void run('/body')};
</script>`;
http.createServer((req,res)=>{if(req.url==='/'){res.setHeader('Content-Type','text/html');res.end(html);return;}if(req.url==='/headers'){const t=setTimeout(()=>res.end('hello'),1000);res.on('close',()=>clearTimeout(t));return;}res.writeHead(200,{'Content-Type':'application/octet-stream','Content-Length':'1000000'});res.write(Buffer.alloc(10000));const t=setInterval(()=>res.write(Buffer.alloc(10000)),100);res.on('close',()=>clearInterval(t));}).listen(3020,'127.0.0.1',()=>console.log('http://127.0.0.1:3020'));
