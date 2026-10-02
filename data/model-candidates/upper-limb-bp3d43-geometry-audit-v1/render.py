"""Source/authored-normal versus decoded candidate and main-bone frame comparison."""
import bpy,json,importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
def run():
 spec=importlib.util.spec_from_file_location('bp43audit',OUT/'build.py');api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
 m=json.loads((OUT/'atlas.json').read_text());raw=(OUT/'anatomy.bin').read_bytes();main=json.loads((ROOT/'public/models/atlas.json').read_text());mp={x['id']:x for x in main['parts']};buffers={i:(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for i,c in enumerate(main['chunks'])}
 scene=bpy.data.scenes.new('BP43 upper-limb source candidate QA');bpy.context.window.scene=scene;scene.world=bpy.data.worlds.new('QA world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.045,.06,.08,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
 scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.transparent_max_bounces=32;scene.render.resolution_x=1600;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
 def material(name,color,alpha):
  mat=bpy.data.materials.new(name);mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;clear=n.new('ShaderNodeBsdfTransparent');s=n.new('ShaderNodeBsdfPrincipled');s.inputs['Base Color'].default_value=(*color,1);s.inputs['Roughness'].default_value=.6;mat.node_tree.links.new(clear.outputs[0],mix.inputs[1]);mat.node_tree.links.new(s.outputs[0],mix.inputs[2]);mat.node_tree.links.new(mix.outputs[0],out.inputs['Surface']);return mat
 mats={'bone':material('Source43 bone ivory',(.8,.83,.85),.14),'main':material('Main40 bone cyan',(.1,.65,.9),.22),'nerve':material('Named nerve gold',(.95,.65,.12),1),'spinal-nerve-trunk':material('Spinal trunks blue',(.15,.45,1),1),'FJ4274':material('Lateral cord orange',(1,.28,.03),1),'FJ4275':material('Medial cord magenta',(.8,.1,.6),1),'FJ4185':material('Second intercostobrachial green',(.15,.8,.5),1),'FJ4223':material('Medial pectoral yellow',(.95,.65,.12),1)}
 objects=[]
 def mesh(name,v,f,n,key):
  d=bpy.data.meshes.new(name);d.from_pydata(v.tolist(),[],f.tolist());d.update()
  for poly in d.polygons:poly.use_smooth=True
  d.normals_split_custom_set_from_vertices(n.tolist());o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.data.materials.append(mats[key]);return o
 for p in m['parts']:
  v=np.frombuffer(raw,'<f4',p['vertexCount']*3,p['positions']).reshape(-1,3).astype(float);f=np.frombuffer(raw,'<u4',p['indexCount'],p['indices']).reshape(-1,3);n=np.frombuffer(raw,'<i2',p['vertexCount']*3,p['normals']).reshape(-1,3).astype(float)/32767
  sv,sn,sf=api.read_obj(ROOT/p['sourcePath']);sv=sv@api.MATRIX[:3,:3].T+api.MATRIX[:3,3];sn=sn@api.ROT.T;sn/=np.linalg.norm(sn,axis=1)[:,None]
  key=p['sourceId'] if p['sourceId'] in mats else p['componentRole'];key=key if key in mats else 'nerve'
  for panel,pv,pf,pn in [('source',sv,sf,sn),('decoded',v,f,n)]:objects.append((mesh(panel+':'+p['sourceId'],pv,pf,pn,key),panel,p))
  if p['componentRole']=='bone':
   q=mp[p['sourceId']];b=buffers[q['chunk']];tv=np.frombuffer(b,'<f4',q['vertexCount']*3,q['positions']).reshape(-1,3);tf=np.frombuffer(b,'<u4',q['indexCount'],q['indices']).reshape(-1,3);tn=np.frombuffer(b,'<i2',q['vertexCount']*3,q['normals']).reshape(-1,3).astype(float)/32767;objects.append((mesh('main:'+p['sourceId'],tv,tf,tn,'main'),'main',p))
 camera=bpy.data.objects.new('QA camera',bpy.data.cameras.new('QA camera'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.type='ORTHO';camera.data.clip_end=100
 for pos,power,size in [((2,3,4),700,4),((-2,1,1),450,3)]:
  light=bpy.data.objects.new('QA light',bpy.data.lights.new('QA light','AREA'));scene.collection.objects.link(light);light.location=pos;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((.1,1.2,0))-light.location).to_track_quat('-Z','Y').to_euler()
 views=[('source-decoded-overview.png',(.13,1.16,0),(.15,.03,1),1.12,'all'),('source-decoded-cords-close.png',(.073,1.425,-.015),(.45,.08,1),.17,'cords'),('source-decoded-collateral-fragments.png',(.105,1.315,.035),(-.25,.08,1),.58,'fragments'),('source-main-bones-overlay.png',(.09,1.3,-.005),(.2,.08,1),.65,'main')]
 records=[]
 for file,center,direction,scale,mode in views:
  center=Vector(center);direction=Vector(direction).normalized();right=Vector((0,1,0)).cross(direction).normalized();up=direction.cross(right).normalized();camera.location=center+direction*3;camera.rotation_euler=Matrix((right,up,direction)).transposed().to_euler();camera.data.ortho_scale=scale
  for o,panel,p in objects:
   selected=True
   if mode=='cords':selected=p['sourceId'] in ['FJ4274','FJ4275','FJ4258'] or p['componentRole']=='bone'
   if mode=='fragments':selected=p['sourceId'] in ['FJ4185','FJ4223'] or p['componentRole']=='bone'
   if mode=='main':selected=p['componentRole']=='bone'
   o.hide_render=not(selected and (panel in ['source','main'] if mode=='main' else panel in ['source','decoded']))
   o.location=right*(-scale*.27 if panel=='source' else scale*.27) if mode!='main' and panel in ['source','decoded'] else (0,0,0)
  scene.render.filepath=str(OUT/file);bpy.ops.render.render(write_still=True);records.append(dict(file=file,mode=mode,panelOrder='source43 left,decoded right' if mode!='main' else 'native-transformed source43 ivory,main40 cyan',center=list(center),direction=list(direction),orthoScale=scale))
 (OUT/'render-evidence.json').write_text(json.dumps(dict(views=records,normalShading='Source authored OBJ normals versus actual decoded Int16 candidate normals; proper common rotation; no smoothing repair',limits='Panel offsets render-only. Morphology and continuous nerve/plexus anatomy unaccepted; blue structures are spinal trunks, not isolated plexus roots.'),indent=2)+'\n')
if __name__=='__main__':run()
