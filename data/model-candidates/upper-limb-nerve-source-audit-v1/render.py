"""Actual source/decoded comparisons and existing-matrix/main-bone previews."""
import bpy,json,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];AXIS=np.array([[1.,0.,0.],[0.,0.,-1.],[0.,1.,0.]])
def run():
 m=json.loads((OUT/'atlas.json').read_text());raw=(OUT/'anatomy.bin').read_bytes();assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==m['source']['sha256']
 reg=json.loads((OUT/'registration-checks.json').read_text());matrix=np.array(reg['matrixColumnVector']);main=json.loads((ROOT/'public/models/atlas.json').read_text());mainParts={p['id']:p for p in main['parts']};buffers={i:(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for i,c in enumerate(main['chunks'])};deps=bpy.context.evaluated_depsgraph_get()
 scene=bpy.data.scenes.new('Upper-limb candidate QA');bpy.context.window.scene=scene;scene.world=bpy.data.worlds.new('QA world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.06,.07,.09,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
 scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.cycles.transparent_max_bounces=32;scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
 def mat(name,color,alpha):
  x=bpy.data.materials.new(name);x.use_nodes=True;n=x.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;clear=n.new('ShaderNodeBsdfTransparent');s=n.new('ShaderNodeBsdfPrincipled');s.inputs['Base Color'].default_value=(*color,1);s.inputs['Roughness'].default_value=.6;x.node_tree.links.new(clear.outputs[0],mix.inputs[1]);x.node_tree.links.new(s.outputs[0],mix.inputs[2]);x.node_tree.links.new(mix.outputs[0],out.inputs['Surface']);return x
 mats={'new':mat('New nerve gold',(1,.65,.07),1),'old':mat('Existing source nerve cyan',(.1,.65,.9),1),'bone':mat('Source bone ivory',(.8,.85,.85),.12),'main':mat('Main bone blue',(.2,.6,.9),.24),'registered-source':mat('Registered source bone ivory',(.85,.8,.6),.17)}
 def mesh(name,v,f,key):
  d=bpy.data.meshes.new(name);d.from_pydata(v.tolist(),[],f.tolist());d.update();o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.data.materials.append(mats[key]);return o
 objects=[]
 for p in m['parts']:
  if p['side']=='right':continue
  v=np.frombuffer(raw,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3).astype(float);f=np.frombuffer(raw,'<u4',p['indexCount'],p['indices']).reshape(-1,3);key='bone' if p['system']=='skeletal' else 'new' if p['role']=='primary' else 'old'
  src=bpy.data.objects[p['sourceObject']].evaluated_get(deps);me=src.to_mesh();me.calc_loop_triangles();sv=np.array([list(src.matrix_world@x.co) for x in me.vertices])@AXIS;sf=np.array([list(t.vertices) for t in me.loop_triangles]);
  if src.matrix_world.to_3x3().determinant()<0:sf=sf[:,[0,2,1]]
  src.to_mesh_clear()
  for panel,pv,pf in [('source',sv,sf),('decoded',v,f)]:objects.append((mesh(panel+':'+p['sourceObject'],pv,pf,key),panel,p))
  rv=(v@AXIS.T)@matrix[:3,:3].T+matrix[:3,3];objects.append((mesh('registered:'+p['sourceObject'],rv,f,'registered-source' if key=='bone' else key),'registered',p))
 for r in reg['measurements']:
  if r['sourceObject'].endswith('.r'):continue
  p=mainParts[r['targetPartId']];b=buffers[p['chunk']];v=np.frombuffer(b,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3);f=np.frombuffer(b,'<u4',p['indexCount'],p['indices']).reshape(-1,3);objects.append((mesh('main:'+r['sourceObject'],v,f,'main'),'registered-main',dict(sourceObject=r['sourceObject'])))
 camera=bpy.data.objects.new('QA camera',bpy.data.cameras.new('QA camera'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.type='ORTHO';camera.data.clip_end=100
 for pos,power,size in [((2,3,4),700,4),((-2,1,1),450,3)]:
  light=bpy.data.objects.new('QA light',bpy.data.lights.new('QA light','AREA'));scene.collection.objects.link(light);light.location=pos;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((.1,1.2,0))-light.location).to_track_quat('-Z','Y').to_euler()
 views=[('source-decoded-whole-arm.png',(.16,1.15,0),(.1,.04,1),1.1,True),('source-decoded-shoulder.png',(.1,1.37,0),(-.35,.12,1),.5,True),('source-decoded-forearm.png',(.24,.99,.02),(.5,.02,1),.48,True),('registered-main-shoulder.png',(.1,1.38,0),(-.4,.1,1),.5,False),('registered-main-forearm.png',(.24,1.01,.02),(.5,.02,1),.52,False)]
 evidence=[]
 for fn,center,direction,scale,pair in views:
  center=Vector(center);direction=Vector(direction).normalized();right=Vector((0,1,0)).cross(direction).normalized();camera.location=center+direction*3;up=direction.cross(right).normalized();camera.rotation_euler=Matrix((right,up,direction)).transposed().to_euler();camera.data.ortho_scale=scale
  for o,panel,p in objects:
   o.hide_render=(panel not in ('source','decoded')) if pair else (panel not in ('registered','registered-main'))
   o.location=right*(-scale*.27 if panel=='source' else scale*.27) if pair and panel in ('source','decoded') else (0,0,0)
  scene.render.filepath=str(OUT/fn);bpy.ops.render.render(write_still=True);evidence.append(dict(file=fn,mode='source-left decoded-right' if pair else 'existing-matrix nerves and ivory source bones over blue main bones',center=list(center),direction=list(direction),orthoScale=scale))
 (OUT/'render-evidence.json').write_text(json.dumps(dict(views=evidence,limits='Representative left-sided views, both sides numerically checked. Pair offsets are render-only. Registered views use old matrix without a new fit and are not acceptance.'),indent=2)+'\n')
if __name__=='__main__':run()
