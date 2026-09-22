"""Actual base/source outlier QA. Blender --background --disable-autoexec --python this.py"""
import bpy,json,zipfile,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
a=json.loads((ROOT/'public/models/atlas.json').read_text());ps={p['id']:p for p in a['parts']};cs={c['id']:c for c in a['concepts']};chunks=[(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for c in a['chunks']]
def geo(p,chunks):
 b=chunks[p['chunk']];return np.frombuffer(b,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3).astype(float),np.frombuffer(b,'<u4',p['indexCount'],p['indices']).reshape(-1,3)
def target(i):return geo(ps[i],chunks)
def loadzip(path):
 out={}
 with zipfile.ZipFile(path) as z:
  for n in z.namelist():
   if not n.endswith('.obj'):continue
   b=z.read(n);h={};v=[];f=[]
   for l in b.decode().splitlines():
    if l.startswith('# ') and ' : ' in l:k,val=l[2:].split(' : ',1);h[k]=val
    s=l.split()
    if s and s[0]=='v':x,y,z0=map(float,s[1:4]);v.append([x*.001,z0*.001+.0781112,-y*.001-.1])
    elif s and s[0]=='f':
     ids=[int(x.split('/')[0])-1 for x in s[1:]]
     for k in range(1,len(ids)-1):f.append([ids[0],ids[k],ids[k+1]])
   out[h['File ID']]=dict(header=h,member=n,sha256=hashlib.sha256(b).hexdigest(),v=np.array(v),f=np.array(f))
 return out
src=loadzip(D/'live-outlier-objects.zip')
if (D/'comparison-objects.zip').exists():src.update(loadzip(D/'comparison-objects.zip'))
def distance(v,w,f):
 t=BVHTree.FromPolygons(w.tolist(),f.tolist(),all_triangles=True);return np.array([t.find_nearest(Vector(p))[3] for p in v])*1000
m=json.loads((ROOT/'public/models/extensions/lung-bp3d43.json').read_text());mc=[(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for c in m['chunks']]
lungvs=[];lungfs=[];offset=0
for p in m['parts']:
 v,f=geo(p,mc);lungvs.extend(v);lungfs.extend(f+offset);offset+=len(v)
lungv=np.array(lungvs);lungf=np.array(lungfs)
rows=[]
for i in ['FJ2041','FJ2044']:
 v,f=target(i);s=src[i];d=np.concatenate([distance(v,s['v'],s['f']),distance(s['v'],v,f)])
 near=[]
 for p in a['parts']:
  if p['id'] in ['FJ2041','FJ2044']:continue
  if not ('renal' in p['name'].lower() or 'kidney' in p['name'].lower()) or p['bounds'][0][0]>=0:continue
  w,wf=target(p['id']);dv=distance(v,w,wf);near.append(dict(id=p['id'],name=p['name'],minMm=float(dv.min()),medianMm=float(np.median(dv)),maxMm=float(dv.max())))
 dl=distance(v,lungv,lungf)
 rows.append(dict(partId=i,base=ps[i],sourceHeader=s['header'],sourceMember=s['member'],sourceSha256=s['sha256'],sourceVsBaseRmsMm=float(np.sqrt(np.mean(d*d))),sourceVsBaseMaxMm=float(d.max()),minDistanceToLungSurfaceMm=float(dl.min()),medianDistanceToLungSurfaceMm=float(np.median(dl)),nearestRenalContext=sorted(near,key=lambda x:x['minMm'])[:6],allBaseParents=[dict(id=c['id'],name=c['name']) for c in a['concepts'] if i in c['elements']]))
(D/'geometry-evidence.json').write_text(json.dumps(dict(outliers=rows,comparisonObjects=[dict(id=i,header=s['header'],bounds=[s['v'].min(0).tolist(),s['v'].max(0).tolist()]) for i,s in src.items()],method='Actual retained base binary geometry and source OBJ conversion; nearest triangle distance is spatial evidence, not proof of vascular connectivity or anatomical identity.'),indent=2)+'\n')
scene=bpy.data.scenes.new('Outlier actual geometry');bpy.context.window.scene=scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.transparent_max_bounces=32;scene.render.resolution_x=1200;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.07,.09,.12,1)
def mat(name,col,alpha=1):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=.6
 if alpha<1:
  mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;t=n.new('ShaderNodeBsdfTransparent');m.node_tree.links.new(t.outputs[0],mix.inputs[1]);m.node_tree.links.new(p.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],n.get('Material Output').inputs['Surface'])
 return m
def add(name,v,f,m):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(v.tolist(),[],f.tolist());mesh.update();o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);mesh.materials.append(m)
 for p in mesh.polygons:p.use_smooth=True
 return o
orange=mat('Outliers orange',(1,.35,.03));red=mat('Verified named renal context red',(.66,.12,.12));kidney=mat('Right kidney transparent blue',(.2,.55,.75),.15);lungs=mat('Lung source context',(.35,.58,.65),.35)
for i in ['FJ2041','FJ2044']:v,f=target(i);add(i,v,f,orange)
renal=[]
for p in a['parts']:
 if 'renal artery' in p['name'].lower() and 'right' in p['name'].lower():v,f=target(p['id']);renal.append(add(p['id'],v,f,red))
v,f=target('FJ3147');renal.append(add('Base right kidney FJ3147',v,f,kidney))
lo=add('Actual lung source surfaces',lungv,lungf,lungs)
cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));scene.collection.objects.link(cam);scene.camera=cam;cam.data.type='ORTHO'
for name,pos,energy in [('Key',(.2,1.5,.5),8),('Fill',(-.4,1.1,.3),5)]:
 o=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));scene.collection.objects.link(o);o.location=pos;o.data.energy=energy;o.data.size=.6;o.rotation_euler=(Vector((-.05,1.15,0))-o.location).to_track_quat('-Z','Y').to_euler()
for name,center,pos,scale,showlung in [('outliers-lung-and-renal-context',(-.03,1.23,0),(-.03,1.23,.8),.46,True),('outliers-right-renal-close',(-.055,1.10,-.012),(-.055,1.10,.6),.16,False),('outliers-right-renal-oblique',(-.055,1.10,-.012),(-.4,1.18,.5),.17,False)]:
 lo.hide_render=not showlung;center=Vector(center);cam.location=pos;forward=(center-cam.location).normalized();right=forward.cross(Vector((0,1,0))).normalized();up=right.cross(forward).normalized();cam.rotation_euler=Matrix((right,up,-forward)).transposed().to_euler();cam.data.ortho_scale=scale;scene.render.filepath=str(D/(name+'.png'));bpy.ops.render.render(write_still=True)
print('QA_DONE',json.dumps(rows))
