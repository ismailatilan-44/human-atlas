"""Export separate HRA female pelvis candidate without using the male atlas.
Blender --background --disable-autoexec --python scripts/export-female-pelvis-candidate.py -- --render
Native glTF meter/Y-up coordinates are preserved. No mirroring, fitting or scaling.
"""
import bpy,json,struct,gzip,hashlib,sys
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/model-candidates/female-pelvis'
SOURCES=['uterus-female','ovary-female-left','ovary-female-right','pelvis-female']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_hashes=json.loads((OUT/'source-hashes.json').read_text())
for name,h in source_hashes.items():assert sha(OUT/name)==h,name

def glb(path):
    data=path.read_bytes();magic,version,total=struct.unpack_from('<III',data);assert magic==0x46546c67 and version==2 and total==len(data)
    length,typ=struct.unpack_from('<II',data,12);assert typ==0x4e4f534a;j=json.loads(data[20:20+length]);bl,bt=struct.unpack_from('<II',data,20+length);assert bt==0x004e4942
    return j,data[28+length:28+length+bl]
def access(j,bin,index):
    a=j['accessors'][index];assert 'sparse' not in a
    view=j['bufferViews'][a['bufferView']];dt={5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']];nc={'VEC3':3,'SCALAR':1}[a['type']];item=np.dtype(dt).itemsize;offset=view.get('byteOffset',0)+a.get('byteOffset',0);stride=view.get('byteStride',item*nc)
    return np.ndarray((a['count'],nc),dtype=dt,buffer=bin,offset=offset,strides=(stride,item)).copy()
blob=bytearray();parts=[];concepts=[];source_records=[];render_rows=[];dim_checks=[]
def append(values,dt):
    while len(blob)%4:blob.append(0)
    start=len(blob);blob.extend(np.asarray(values,dtype=dt).tobytes());return start
for source in SOURCES:
    metadata=json.loads((OUT/(source+'-metadata.json')).read_text());graph=json.loads((OUT/(source+'-graph.json')).read_text());primary=graph['data'][0];raw=metadata['was_derived_from'];dist=next(d for d in raw['distributions'] if d['mediaType']=='model/gltf-binary');filename=source+'-'+dist['downloadUrl'].rsplit('/',1)[-1];j,bin=glb(OUT/filename)
    assert primary['organ_owner_sex']=='Female';assert primary['placements'][0]['target']=='https://purl.humanatlas.io/graph/hra-ccf-body#VHFemale'
    vertices=[];sourceparts=[];vertices_by_node={}
    for nodeindex,node in enumerate(j['nodes']):
        # Current selected source files have identity local transforms; fail if source changes.
        assert not any(k in node for k in ['matrix','translation','rotation','scale']),node['name']
        if 'mesh' not in node:continue
        primitives=j['meshes'][node['mesh']]['primitives'];assert len(primitives)==1
        prim=primitives[0];assert prim.get('mode',4)==4
        v=access(j,bin,prim['attributes']['POSITION']).astype('<f4');n=access(j,bin,prim['attributes']['NORMAL']).astype(float);f=access(j,bin,prim['indices']).reshape(-1,3).astype('<u4')
        assert np.isfinite(v).all() and f.max()<len(v);lengths=np.linalg.norm(n,axis=1);
        if np.any(lengths<.5):print('SOURCE_NORMALS',source,node['name'],'short',int(np.sum(lengths<.5)), 'unused',len(v)-len(np.unique(f)), 'min',float(lengths.min()),flush=True)
        degenerateNormalCount=int(np.sum(lengths<1e-10))
        if degenerateNormalCount:
            tri=v[f].astype(float);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])
            for bad in np.flatnonzero(lengths<1e-10):
                incident=np.any(f==bad,axis=1);vectors=cross[incident];areas=np.linalg.norm(vectors,axis=1)
                if len(areas) and areas.max()>1e-25:n[bad]=vectors[np.argmax(areas)]/areas.max()
                else:
                    valid=np.flatnonzero(lengths>.5);near=valid[np.argmin(np.sum((v[valid]-v[bad])**2,axis=1))];n[bad]=n[near]
            lengths=np.linalg.norm(n,axis=1)
        n/=lengths[:,None]
        ex=node.get('extras',{});pid='HRA-FP-'+node['name'];cid='hra-female:'+node['name'];system='skeletal' if source=='pelvis-female' else 'reproductive';name=node['name'].replace('VH_F_','').replace('_',' ')
        part=dict(id=pid,conceptId=cid,name=name,system=system,chunk=0,positions=append(v,'<f4'),normals=append(np.rint(n*32767),'<i2'),indices=append(f,'<u4'),vertexCount=len(v),indexCount=int(f.size),bounds=[v.min(0).tolist(),v.max(0).tolist()],sourceDataset=source,sourceNode=node['name'],sourceNodeIndex=nodeindex,sourceMeshIndex=node['mesh'],sourceOntologyId=ex.get('ontologyid'),sourceLabel=ex.get('label'),sourceNodeType=ex.get('node_type'),sourceSpatialEntity=ex.get('source_spatial_entity'),representation='source_surface',zeroSourceNormalsRecomputed=degenerateNormalCount,expertReview='pending')
        parts.append(part);sourceparts.append(pid);concepts.append(dict(id=cid,name=name,elements=[pid],sourceOntologyId=ex.get('ontologyid')));vertices.append(v);vertices_by_node[nodeindex]=v;render_rows.append((part,v,f))
    subpath=primary['object_reference']['file_subpath'];rootnode=next(i for i,n in enumerate(j['nodes']) if n['name']==subpath)
    selected=[];selected_ids=[]
    def visit(i):
        if i in vertices_by_node:selected.append(vertices_by_node[i]);selected_ids.append('HRA-FP-'+j['nodes'][i]['name'])
        for child in j['nodes'][i].get('children',[]):visit(child)
    visit(rootnode)
    allv=np.concatenate(selected);dims=(allv.max(0)-allv.min(0))*1000;expected=np.array([primary[k+'_dimension'] for k in ['x','y','z']]);delta=np.abs(dims-expected)
    assert delta.max()<.001,(source,dims,expected)
    dim_checks.append(dict(source=source,primarySubpath=subpath,fullFileDimensionsMm=((np.concatenate(vertices).max(0)-np.concatenate(vertices).min(0))*1000).tolist(),geometryDimensionsMm=dims.tolist(),graphDimensionsMm=expected.tolist(),maximumDifferenceMm=float(delta.max())))
    concepts.append(dict(id='hra-female:'+source,name=primary.get('pref_label',primary['label']),elements=selected_ids,sourceOntologyId=primary['representation_of']))
    source_records.append(dict(id=source,dataset=metadata['id'],version=metadata['version'],doi=raw['doi'],citation=raw['citation'],file=filename,url=dist['downloadUrl'],sha256=sha(OUT/filename),license='CC-BY-4.0',sex='Female',donorId=None,donorEvidence='Metadata identifies Visible Human Dataset; no individual donor identifier supplied.',globalPlacement=primary['placements'][0],objectPlacement=primary['object_reference']['placement']))
binary=bytes(blob);compressed=gzip.compress(binary,compresslevel=9,mtime=0);(OUT/'female-pelvis.bin').write_bytes(binary);(OUT/'female-pelvis.bin.gz').write_bytes(compressed)
allv=np.concatenate([row[1] for row in render_rows]);manifest=dict(version='HRA female pelvis standalone candidate 1',datasetId='female-pelvis',title='Kadın pelvis referansı',scope='Uterus, iki ovaryum ve kemik pelvis; ayrı HRA kadın referansı',sex='female',status='standalone_candidate_not_integrated',source=dict(id='hra-female-pelvis',name='Human Reference Atlas — female pelvis',url='https://humanatlas.io/3d-reference-library',license='CC-BY-4.0',attribution='ATTRIBUTION.md',records=source_records),parts=parts,concepts=concepts,chunks=[dict(url='female-pelvis.bin',bytes=len(binary),gzipUrl='female-pelvis.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())],triangles=sum(p['indexCount']//3 for p in parts),bounds=[allv.min(0).tolist(),allv.max(0).tolist()],coordinateFrame=dict(id='HRA-native-VHFemaleOrgans-glTF',units='meter',up='Y',method='Native GLB positions and identity node transforms retained; no per-organ recentering or graph local-placement reapplied.',sourceSpatialEntity='#VHFemaleOrgans',graphGlobalTarget='https://purl.humanatlas.io/graph/hra-ccf-body#VHFemale',maleAtlasCompatible=False,dimensionChecks=dim_checks),limitations=['Separate female reference assembly, not a male-atlas extension or a whole female body.','Visible Human Dataset provenance; individual donor identity and all four organs being from one subject are not established by the supplied metadata.','Pelvis is 14 bone/tissue surfaces; uterus file contains 11 anatomical surface regions. Whole organ closure or clinical volume not asserted.','No vagina, uterine tubes, ligaments, vessels, urinary bladder or pelvic floor added to the selected scope.','Latest versions are independently numbered by organ: uterus v1.2; ovaries and pelvis v1.3.','Ontology labels are preserved as supplied, including missing values and broad tissue labels; node-scoped concept IDs prevent false equivalence.'])
(OUT/'female-pelvis.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(dict(parts=len(parts),triangles=manifest['triangles'],bounds=manifest['bounds'],dimensions=dim_checks,bytes=len(binary),gzip=len(compressed)),indent=2))
if '--render' in sys.argv:
    scene=bpy.data.scenes.new('Female pelvis candidate');bpy.context.window.scene=scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.transparent_max_bounces=32;scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.08,.10,.13,1)
    def mat(name,col,alpha):
        m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;s=n.get('Principled BSDF');s.inputs['Base Color'].default_value=(*col,1);s.inputs['Roughness'].default_value=.65
        if alpha<1:
            mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;t=n.new('ShaderNodeBsdfTransparent');m.node_tree.links.new(t.outputs[0],mix.inputs[1]);m.node_tree.links.new(s.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],n.get('Material Output').inputs['Surface'])
        return m
    mats={'pelvis-female':mat('Pelvis',(.75,.81,.86),.16),'uterus-female':mat('Uterus',(.82,.29,.30),1),'ovary-female-left':mat('Left ovary',(.98,.70,.17),1),'ovary-female-right':mat('Right ovary',(.32,.75,.70),1)}
    for part,v,f in render_rows:
        mesh=bpy.data.meshes.new(part['name']);mesh.from_pydata(v.tolist(),[],f.tolist());mesh.update();o=bpy.data.objects.new(part['name'],mesh);scene.collection.objects.link(o);mesh.materials.append(mats[part['sourceDataset']]);
        for p in mesh.polygons:p.use_smooth=True
    camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.type='ORTHO'
    target=Vector((-.013,.065,-.075))
    light=bpy.data.objects.new('Key',bpy.data.lights.new('Key','AREA'));scene.collection.objects.link(light);light.data.energy=18;light.data.size=.5;light.location=(.05,.35,.5);light.rotation_euler=(target-light.location).to_track_quat('-Z','Y').to_euler()
    for view,delta,scale in [('front',(0,0,.8),.37),('oblique',(.55,.18,.65),.37),('organs-close',(0,.08,.8),.17)]:
        camera.location=target+Vector(delta);camera.data.ortho_scale=scale;back=(camera.location-target).normalized();right=Vector((0,1,0)).cross(back).normalized();up=back.cross(right);camera.rotation_euler=Matrix((right,up,back)).transposed().to_euler();scene.render.filepath=str(OUT/('female-pelvis-'+view+'.png'));bpy.ops.render.render(write_still=True)
