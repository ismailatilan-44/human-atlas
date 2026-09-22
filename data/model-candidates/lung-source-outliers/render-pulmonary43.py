import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def read_manifest(path,public=False):
 m=json.loads(path.read_text());chunks=[(ROOT/'public'/c['url'].lstrip('/') if public else path.parent/c['url']).read_bytes() for c in m['chunks']];out={}
 for p in m['parts']:
  b=chunks[p['chunk']];out[p['id']]=(np.frombuffer(b,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3),np.frombuffer(b,'<u4',p['indexCount'],p['indices']).reshape(-1,3))
 return out
base=read_manifest(ROOT/'public/models/atlas.json',True);new=read_manifest(D/'right-anterior-pulmonary-43.json');lung=read_manifest(ROOT/'public/models/extensions/lung-bp3d43.json',True)
s=bpy.data.scenes.new('Pulmonary alternate source representation');bpy.context.window.scene=s;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.cycles.transparent_max_bounces=32;s.render.resolution_x=1100;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('World');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.07,.09,.12,1)
def mat(name,c,alpha=1):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.7
 if alpha<1:
  mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;t=n.new('ShaderNodeBsdfTransparent');m.node_tree.links.new(t.outputs[0],mix.inputs[1]);m.node_tree.links.new(p.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],n.get('Material Output').inputs['Surface'])
 return m
def obj(i,vf,m):
 v,f=vf;mesh=bpy.data.meshes.new(i);mesh.from_pydata(v.tolist(),[],f.tolist());mesh.update();o=bpy.data.objects.new(i,mesh);s.collection.objects.link(o);mesh.materials.append(m)
 for p in mesh.polygons:p.use_smooth=True
 return o
red=mat('Source vessels',(.9,.25,.17));context=mat('Source upper right lobe',(.2,.6,.7),.12)
oldobjs=[obj(i,base[i],red) for i in ['FJ2974','FJ2975','FJ2976','FJ2977','FJ2979','FJ2980','FJ2981']];newobjs=[obj(i,vf,red) for i,vf in new.items()]
for i in ['BP43-FJ6604','BP43-FJ6606','BP43-FJ6607']:obj(i,lung[i],context)
center=Vector((-.065,1.355,.005));cam=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=.165;cam.location=(-.065,1.355,.6);f=(center-cam.location).normalized();r=f.cross(Vector((0,1,0))).normalized();u=r.cross(f).normalized();cam.rotation_euler=Matrix((r,u,-f)).transposed().to_euler()
for name,pos,en in [('Key',(.2,1.7,.6),8),('Fill',(-.5,1.5,.3),6)]:
 o=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));s.collection.objects.link(o);o.location=pos;o.data.energy=en;o.data.size=.5;o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
for name,newvisible in [('pulmonary-existing-seven',False),('pulmonary-source43-seven',True)]:
 for o in newobjs:o.hide_render=not newvisible
 for o in oldobjs:o.hide_render=newvisible
 s.render.filepath=str(D/(name+'.png'));bpy.ops.render.render(write_still=True)
