"""Export the source spinal cord tissue surface and optional --render review. Blender --background --disable-autoexec --python this.py."""
import bpy, json, gzip, hashlib, zipfile, sys
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/model-candidates/spinal-cord-bp3d43'
OUT=ROOT/'public/models/extensions'
QA=ROOT/'work/spinal-cord-review'
QA.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
SOURCE_HASHES={'spinal-cord-bp3d43-source.zip': '86eeee2718f5ccbb94105f945fd1f050f0355bfaf53ce535f5b44f288c6202bf', 'spinal-cord-bp3d43-references.zip': 'f51b4407797180fb8698aba297e03ed1605e6d7fb704e63ab5d51f2e881f3652', 'bp3d-v43-mapping.zip': '4d4fa81affbbbc8a071f35c72c4be95eefd185e12ef23dabd37d280261f8fe3f', 'bp3d-live-license.html': '63d46abcf1b112da9f2d587677d0f4edb7d1654a3c9a8a2bfd1c3d080340512e'}
for filename,expected in SOURCE_HASHES.items():assert sha(SRC/filename)==expected,filename
atlas=json.loads((ROOT/'public/models/atlas.json').read_text())
chunks=[(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for c in atlas['chunks']]
def objmesh(text):
    v,f=[],[]
    for line in text.splitlines():
        c=line.split()
        if not c:continue
        if c[0]=='v':
            x,y,z=map(float,c[1:4]);v.append([x*.001,z*.001+.0781112,-y*.001-.1])
        if c[0]=='f':
            ids=[int(x.split('/')[0])-1 for x in c[1:]]
            for k in range(1,len(ids)-1):f.append([ids[0],ids[k],ids[k+1]])
    return np.array(v,dtype='<f4'),np.array(f,dtype='<u4')
def loadzip(path):
    out={}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.endswith('.obj'):out[Path(n).name.split('_')[0]]=(n,*objmesh(z.read(n).decode()),hashlib.sha256(z.read(n)).hexdigest())
    return out
meshes=loadzip(SRC/'spinal-cord-bp3d43-source.zip');refs=loadzip(SRC/'spinal-cord-bp3d43-references.zip')
def target(i):
    p=next(p for p in atlas['parts'] if p['id']==i);b=chunks[p['chunk']]
    return p,np.frombuffer(b,dtype='<f4',count=p['vertexCount']*3,offset=p['positions']).reshape(-1,3),np.frombuffer(b,dtype='<u4',count=p['indexCount'],offset=p['indices']).reshape(-1,3)
def distances(a,b,f):
    t=BVHTree.FromPolygons(b.tolist(),f.tolist(),all_triangles=True)
    return np.array([t.find_nearest(Vector(v))[3] for v in a])*1000
metrics=[]
for i,(_,v,f,_) in {**refs,'FJ1737':meshes['FJ1737']}.items():
    p,tv,tf=target(i);d=np.concatenate([distances(v,tv,tf),distances(tv,v,f)])
    metrics.append(dict(sourceId=i,targetId=i,name=p['name'],role='independent_reference_no_fit',rmsMm=float(np.sqrt(np.mean(d*d))),p95Mm=float(np.percentile(d,95)),maxMm=float(d.max())))
assert max(m['rmsMm'] for m in metrics)<.2,metrics
member,v,f,sourcehash=meshes['FJ4426']
tris=v[f].astype(float);cross=np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0]);area=np.linalg.norm(cross,axis=1)
assert np.isfinite(v).all() and f.max()<len(v)
rawVertices=len(v);rawTriangles=len(f);removedDegenerateTriangles=int(np.sum(area<=1e-15))
f=f[area>1e-15];used=np.unique(f);remap=np.full(len(v),-1);remap[used]=np.arange(len(used));v=v[used];f=remap[f]
tris=v[f].astype(float);cross=np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0])
unique,inverse=np.unique(v,axis=0,return_inverse=True);wf=inverse[f]
source_text=next(SRC.glob('FJ4426*.obj')).read_text()
source_normals=[]
for line in source_text.splitlines():
    c=line.split()
    if c and c[0]=='vn':
        x,y,z=map(float,c[1:4]);source_normals.append([x,z,-y])
    if c and c[0]=='f':assert all(x.split('//')[0]==x.split('//')[-1] for x in c[1:])
norm=np.array(source_normals)[used];assert np.isfinite(norm).all() and np.all(np.linalg.norm(norm,axis=1)>0)
norm/=np.linalg.norm(norm,axis=1)[:,None]
edges=np.sort(np.concatenate([wf[:,[0,1]],wf[:,[1,2]],wf[:,[2,0]]]),axis=1)
_,counts=np.unique(edges,axis=0,return_counts=True)
parent=list(range(len(unique)))
def find(i):
    while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
    return i
for a,b in edges:
    a,b=find(int(a)),find(int(b))
    if a!=b:parent[a]=b
components={}
for i in range(len(unique)):components.setdefault(find(i),[]).append(i)
component_info=[dict(vertices=len(ids),boundsM=[unique[ids].min(0).tolist(),unique[ids].max(0).tolist()]) for ids in sorted(components.values(),key=len,reverse=True)]
quality=dict(rawVertices=rawVertices,rawTriangles=rawTriangles,removedDegenerateTriangles=removedDegenerateTriangles,exportedVertices=len(v),uniquePositions=len(unique),triangles=len(f),signedVolumeCm3=float(np.sum(np.einsum('ij,ij->i',tris[:,0],np.cross(tris[:,1],tris[:,2])))/6)*1e6,boundaryEdgesAfterExactPositionWeld=int(np.sum(counts==1)),nonManifoldEdgesAfterExactPositionWeld=int(np.sum(counts>2)),componentsAfterExactPositionWeld=component_info)
blob=bytearray()
def append(a,dtype):
    while len(blob)%4:blob.append(0)
    start=len(blob);blob.extend(np.array(a,dtype=dtype).tobytes());return start
part=dict(id='BP43-FJ4426',conceptId='FMA242005',name='Neural tissue of spinal cord',system='nervous',chunk=0,positions=append(v,'<f4'),normals=append(np.rint(norm*32767),'<i2'),indices=append(f,'<u4'),vertexCount=len(v),indexCount=int(f.size),bounds=[v.min(0).tolist(),v.max(0).tolist()],sourceObject=member,sourceObjectType='OBJ',sourceId='FJ4426',sourceConceptId='FMA242005',sourceMember=member,sourceSha256=sourcehash,representation='source_anatomical_surface',expertReview='pending',quality=quality)
binary=bytes(blob);compressed=gzip.compress(binary,compresslevel=9,mtime=0)
(OUT/'spinal-cord-bp3d43.bin').write_bytes(binary);(OUT/'spinal-cord-bp3d43.bin.gz').write_bytes(compressed)
manifest=dict(version='BodyParts3D 4.3 spinal cord candidate 1',status='registered_source_reference',extendsConceptIds=['FMA7647'],sex='male',scope='Longitudinal neural tissue surface of spinal cord; source FMA7647 combines this with central canal FJ1737',source=dict(id='bodyparts3d-4.3-live',url='https://lifesciencedb.jp/bp3d/?lng=en',downloadUrl='https://lifesciencedb.jp/bp3d/download.cgi',license='CC-BY-SA-2.1-JP',attribution='/models/extensions/SPINAL-CORD-BP3D43-ATTRIBUTION.md',archiveSha256=sha(SRC/'spinal-cord-bp3d43-source.zip'),officialMappingSha256=sha(SRC/'bp3d-v43-mapping.zip'),licenseEvidenceSha256=sha(SRC/'bp3d-live-license.html')),parts=[part],chunks=[dict(url='/models/extensions/spinal-cord-bp3d43.bin',bytes=len(binary),gzip='/models/extensions/spinal-cord-bp3d43.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())],triangles=len(f),concepts=[dict(id='FMA242005',name='Neural tissue of spinal cord',elements=['BP43-FJ4426']),dict(id='FMA7647',name='Spinal cord',elements=['BP43-FJ4426'])],registration=dict(method='Unmodified base-atlas BP3D mm-to-m axis conversion; five same-ID references spanning cervical to lumbar levels and central canal, no fitting or deformation',matrixColumnVector=[[.001,0,0,0],[0,0,.001,.0781112],[0,-.001,0,-.1],[0,0,0,1]],targetManifestSha256=sha(ROOT/'public/models/atlas.json'),measurements=metrics),limitations=['Degenerate source faces and unused vertices are omitted from the display export; original OBJ retained unchanged.','Source neural tissue of spinal cord surface; no separate spinal gray/white matter, segment parcels, roots or meninges included.','FMA7647 source aggregation also includes the existing central canal FJ1737; the extension should merge by concept ID and preserve that part.','Individual reference morphology; anatomical expert review pending.','Registered source reference; additional root, meningeal and segment detail remains outside this package.'])
(OUT/'spinal-cord-bp3d43.json').write_text(json.dumps(manifest,indent=2)+'\n')
(QA/'quality-registration.json').write_text(json.dumps(dict(quality=quality,registration=metrics,bytes=len(binary),gzipBytes=len(compressed)),indent=2)+'\n')
print(json.dumps(dict(quality=quality,registration=metrics,bytes=len(binary),gzipBytes=len(compressed)),indent=2))
if '--render' in sys.argv:
    scene=bpy.data.scenes.new('Spinal cord source review');bpy.context.window.scene=scene
    scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.transparent_max_bounces=24
    scene.render.resolution_x=900;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
    scene.world=bpy.data.worlds.new('QA world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.1,.12,.15,1)
    scene.view_settings.view_transform='AgX'
    def mat(name,col,alpha=1):
        m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;s=n.get('Principled BSDF');s.inputs['Base Color'].default_value=(*col,1);s.inputs['Roughness'].default_value=.6
        if alpha<1:
            mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;t=n.new('ShaderNodeBsdfTransparent');m.node_tree.links.new(t.outputs[0],mix.inputs[1]);m.node_tree.links.new(s.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],n.get('Material Output').inputs['Surface'])
        return m
    def add(name,v,f,m):
        v,remap=np.unique(v,axis=0,return_inverse=True);f=remap[f];mesh=bpy.data.meshes.new(name);mesh.from_pydata(v.tolist(),[],f.tolist());mesh.update();o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);mesh.materials.append(m)
        for p in mesh.polygons:p.use_smooth=True
        return o
    cord=add('FJ4426 neural tissue',v,f,mat('Cord ivory',(.87,.72,.46)))
    _,cv,cf,_=meshes['FJ1737'];canal=add('Existing central canal FJ1737',cv,cf,mat('Canal red',(.8,.12,.08)))
    contexts=[]
    for p in atlas['parts']:
        if 'vertebra' in p['name'].lower() and 'sacral' not in p['name'].lower() and 'coccy' not in p['name'].lower():
            _,tv,tf=target(p['id']);contexts.append(add(p['name'],tv,tf,mat(p['id'],(.30,.53,.69),.12)))
    camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=.55
    center=Vector((0,1.33,-.055))
    for name,loc,energy in [('Key',(.3,1.5,.5),10),('Fill',(-.3,1.1,-.4),5)]:
        light=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));scene.collection.objects.link(light);light.data.energy=energy;light.data.size=.6;light.location=loc;light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
    for view,loc in [('isolated-front',(0,1.33,.7)),('isolated-lateral',(.7,1.33,-.055)),('vertebral-context',(.55,1.33,-.7)),('canal-comparison',(0,1.33,.7))]:
        for o in contexts:o.hide_render=view!='vertebral-context'
        canal.hide_render=view!='canal-comparison'
        camera.location=loc;back=(camera.location-center).normalized();right=Vector((0,1,0)).cross(back).normalized();up=back.cross(right);camera.rotation_euler=Matrix((right,up,back)).transposed().to_euler();scene.render.filepath=str(QA/(view+'.png'));bpy.ops.render.render(write_still=True)
