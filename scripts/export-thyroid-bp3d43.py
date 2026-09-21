"""Export the separate BodyParts3D 4.3 thyroid reference and actual atlas QA.
Blender --background --disable-autoexec --python scripts/export-thyroid-bp3d43.py -- --render
Source ZIPs and captured official license: data/model-candidates/thyroid-bp3d43.
No ICP/shape correction: use the main atlas's documented BP3D mm-to-m frame.
"""
import bpy, json, gzip, hashlib, zipfile, io, sys
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/model-candidates/thyroid-bp3d43'
OUT=ROOT/'public/models/extensions'
QA=ROOT/'work/thyroid-alternative'
QA.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
SOURCE_HASHES={'bp3d-v43-mapping.zip': '4d4fa81affbbbc8a071f35c72c4be95eefd185e12ef23dabd37d280261f8fe3f', 'thyroid-bp3d43-references.zip': '33b77f86496421dcc0f75390db43a7883289ee47fe2314b05de287ccd8bf6d95', 'thyroid-bp3d43-source.zip': '42026590f461a479b4e35f6b2ac5a2835b34f0b42abec0ffb6d37d51792720bc', 'bp3d-live-license.html': '63d46abcf1b112da9f2d587677d0f4edb7d1654a3c9a8a2bfd1c3d080340512e'}
for filename, expected in SOURCE_HASHES.items(): assert sha(SRC/filename)==expected, filename
ATLAS_HASH='c359f4bcd2cba90b7411d66d5e9fc04dc81294d46cd5c1e8b212c824f2e5bbee'
assert sha(ROOT/'public/models/atlas.json')==ATLAS_HASH
atlas=json.loads((ROOT/'public/models/atlas.json').read_text())
chunks=[(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for c in atlas['chunks']]

def objmesh(text):
    v,f=[],[]
    for line in text.splitlines():
        cols=line.split()
        if not cols:continue
        if cols[0]=='v':
            x,y,z=map(float,cols[1:4]);v.append([x*.001,z*.001+.0781112,-y*.001-.1])
        if cols[0]=='f':
            ids=[int(c.split('/')[0])-1 for c in cols[1:]]
            for k in range(1,len(ids)-1):f.append([ids[0],ids[k],ids[k+1]])
    return np.array(v,dtype='<f4'),np.array(f,dtype='<u4')
def loadzip(path):
    result={}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.endswith('.obj'):result[Path(n).name.split('_')[0]]=(n,*objmesh(z.read(n).decode()),hashlib.sha256(z.read(n)).hexdigest())
    return result
meshes=loadzip(SRC/'thyroid-bp3d43-source.zip')
refs=loadzip(SRC/'thyroid-bp3d43-references.zip')

def target(i):
    p=next(p for p in atlas['parts'] if p['id']==i);b=chunks[p['chunk']]
    return p,np.frombuffer(b,dtype='<f4',count=p['vertexCount']*3,offset=p['positions']).reshape(-1,3),np.frombuffer(b,dtype='<u4',count=p['indexCount'],offset=p['indices']).reshape(-1,3)
def distances(a,b,f):
    tree=BVHTree.FromPolygons(b.tolist(),f.tolist(),all_triangles=True)
    return np.array([tree.find_nearest(Vector(v))[3] for v in a])*1000
metrics=[]
for i,(_,v,f,_) in refs.items():
    p,tv,tf=target(i);d=np.concatenate([distances(v,tv,tf),distances(tv,v,f)])
    metrics.append(dict(sourceId=i,targetId=i,name=p['name'],role='independent_reference_no_fit',rmsMm=float(np.sqrt(np.mean(d*d))),p95Mm=float(np.percentile(d,95)),maxMm=float(d.max())))
assert max(m['rmsMm'] for m in metrics)<.1,metrics
blob=bytearray();parts=[]
def append(a,dtype):
    while len(blob)%4:blob.append(0)
    start=len(blob);blob.extend(np.array(a,dtype=dtype).tobytes());return start
spec=[('FJ3671','FMA13369','Left lobe of thyroid gland'),('FJ3672','FMA13368','Right lobe of thyroid gland'),('FJ3670','FMA49178','Isthmus of thyroid gland')]
for i,c,name in spec:
    member,v,f,sourcehash=meshes[i]
    tris=v[f].astype(float);cross=np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0]);area=np.linalg.norm(cross,axis=1)
    assert np.isfinite(v).all() and np.all(area>1e-15) and f.max()<len(v)
    # Source triangle-soup vertices stay unchanged. Smooth normals by identical position only.
    unique,inverse=np.unique(v,axis=0,return_inverse=True);norm=np.zeros((len(unique),3))
    for k in range(3):np.add.at(norm,inverse[f[:,k]],cross)
    norm/=np.linalg.norm(norm,axis=1)[:,None];norm=norm[inverse]
    volume=float(np.sum(np.einsum('ij,ij->i',tris[:,0],np.cross(tris[:,1],tris[:,2])))/6)*1e6
    wf=inverse[f];edges=np.sort(np.concatenate([wf[:,[0,1]],wf[:,[1,2]],wf[:,[2,0]]]),axis=1)
    _,counts=np.unique(edges,axis=0,return_counts=True)
    quality=dict(rawVertices=len(v),uniquePositions=len(unique),triangles=len(f),signedVolumeCm3=volume,boundaryEdgesAfterExactPositionWeld=int(np.sum(counts==1)),nonManifoldEdgesAfterExactPositionWeld=int(np.sum(counts>2)))
    parts.append(dict(id='BP43-'+i,conceptId=c,name=name,system='endocrine',chunk=0,positions=append(v,'<f4'),normals=append(np.rint(norm*32767),'<i2'),indices=append(f,'<u4'),vertexCount=len(v),indexCount=int(f.size),bounds=[v.min(0).tolist(),v.max(0).tolist()],sourceId=i,sourceConceptId=c,sourceObject=member,sourceObjectType='OBJ',sourceMember=member,sourceSha256=sourcehash,representation='source_anatomical_surface',expertReview='pending',quality=quality))
binary=bytes(blob);compressed=gzip.compress(binary,compresslevel=9,mtime=0)
(OUT/'thyroid-bp3d43.bin').write_bytes(binary);(OUT/'thyroid-bp3d43.bin.gz').write_bytes(compressed)
manifest=dict(version='BodyParts3D 4.3 thyroid candidate 1',status='registered_source_reference',sex='male',source=dict(id='bodyparts3d-4.3-live',url='https://lifesciencedb.jp/bp3d/?lng=en',downloadUrl='https://lifesciencedb.jp/bp3d/download.cgi',license='CC-BY-SA-2.1-JP',attribution='/models/extensions/THYROID-BP3D43-ATTRIBUTION.md',archiveSha256=sha(SRC/'thyroid-bp3d43-source.zip'),officialMappingSha256=sha(SRC/'bp3d-v43-mapping.zip'),licenseEvidenceSha256=sha(SRC/'bp3d-live-license.html')),parts=parts,chunks=[dict(url='/models/extensions/thyroid-bp3d43.bin',bytes=len(binary),gzip='/models/extensions/thyroid-bp3d43.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())],triangles=sum(p['indexCount']//3 for p in parts),concepts=[dict(id=c,name=n,elements=['BP43-'+i]) for i,c,n in spec]+[dict(id='FMA9603',name='Thyroid gland',elements=[p['id'] for p in parts])],registration=dict(method='Unmodified main atlas BP3D coordinate conversion; nine independent same-ID neck references, no fitted transform',matrixColumnVector=[[.001,0,0,0],[0,0,.001,.0781112],[0,-.001,0,-.1],[0,0,0,1]],targetManifestSha256=ATLAS_HASH,measurements=metrics),limitations=['Three source surfaces, separate left/right lobes and isthmus; no added smoothing, decimation or anatomical remodeling.','No blood vessels, nerves, fascia, parathyroids or pyramidal lobe included.','Individual male reference morphology, not a universal normal thyroid or clinical segmentation.','Exact-position-weld diagnostics find boundary edges in all three source surfaces; no watertight/manifold solid or clinical volume claim.','Source reference integrated for exploration; anatomical expert acceptance remains pending.'])
(OUT/'thyroid-bp3d43.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(parts=parts,registration=metrics,bytes=len(binary),gzipBytes=len(compressed)),indent=2))
if '--render' in sys.argv:
    scene=bpy.data.scenes.new('BP3D43 thyroid QA');bpy.context.window.scene=scene
    scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.transparent_max_bounces=32
    scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
    scene.world=bpy.data.worlds.new('QA world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.09,.105,.13,1)
    scene.view_settings.view_transform='AgX'
    def mat(name,col,alpha=1):
        m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;s=n.get('Principled BSDF');s.inputs['Base Color'].default_value=(*col,1);s.inputs['Roughness'].default_value=.55
        if alpha<1:
            mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;t=n.new('ShaderNodeBsdfTransparent');m.node_tree.links.new(t.outputs[0],mix.inputs[1]);m.node_tree.links.new(s.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],n.get('Material Output').inputs['Surface'])
        return m
    def add(name,v,f,m):
        v,remap=np.unique(v,axis=0,return_inverse=True);f=remap[f]
        mesh=bpy.data.meshes.new(name);mesh.from_pydata(v.tolist(),[],f.tolist());mesh.update();o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);mesh.materials.append(m)
        for p in mesh.polygons:p.use_smooth=True
        return o
    contexts=[]
    for i in refs:
        p,v,f=target(i);m=mat(p['name'],(.53,.70,.75),.7 if i in ['FJ2440','FJ2808','FJ2541'] else .2);contexts.append(add(p['name'],v,f,m))
    for (i,_,name),col in zip(spec,[(.78,.24,.12),(.94,.46,.16),(.96,.72,.20)]):
        _,v,f,_=meshes[i];add(name,v,f,mat(name,col))
    camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=.14
    light=bpy.data.objects.new('Key',bpy.data.lights.new('Key','AREA'));scene.collection.objects.link(light);light.data.energy=2;light.data.size=.35;light.location=(.08,1.58,.4);light.rotation_euler=(Vector((0,1.465,0))-light.location).to_track_quat('-Z','Y').to_euler()
    for view,location in [('front',(0,1.465,.6)),('oblique',(.45,1.49,.5)),('posterior',(0,1.465,-.6)),('isolated',(0,1.465,.6))]:
        for o in contexts:o.hide_render=view=='isolated'
        camera.location=location;back=(camera.location-Vector((0,1.465,0))).normalized();right=Vector((0,1,0)).cross(back).normalized();up=back.cross(right);camera.rotation_euler=Matrix((right,up,back)).transposed().to_euler();scene.render.filepath=str(QA/('thyroid-bp3d43-'+view+'.png'));bpy.ops.render.render(write_still=True)
