"""Deterministic 87+32 same-source candidate; writes only beside this script.
Blender --background --disable-autoexec work/open-assets-review/Startup.blend --python data/model-candidates/foot-soft-tissue-source-audit-v1/export.py -- --render
"""
import bpy, gzip, hashlib, json, sys, time
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
SHA='9f08a17ea0115fed80b2a73ecdf0a1bc2ab2f6956f37c593ce23d513ea35afcd'
BASE_SHA='572a92f6c7f630c226e70fd5e02d93db70714c063c8fd493d4eaa4c87472ca56'
BASE_MANIFEST_SHA='a9b76a85da63937bd3c34230c902457d330cec7b75ab6df41c3db9b1cd8154ed'
AXIS=np.array([[1.,0.,0.],[0.,0.,-1.],[0.,1.,0.]])
def build_candidate(output_dir=None, render=False):
    """Append audited32 to pinned87; output defaults here, evidence always stays here.

    The baseline is the immutable local baseline87-atlas.json/baseline87.bin.gz,
    never the mutable published reference. Call only with the pinned blend open.
    """
    START=time.monotonic()
    PACKAGE_OUT=Path(output_dir) if output_dir is not None else OUT
    PACKAGE_OUT.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==SHA
    assert hashlib.sha256((OUT/'baseline87-atlas.json').read_bytes()).hexdigest()==BASE_MANIFEST_SHA
    baseline=json.loads((OUT/'baseline87-atlas.json').read_text())
    base_binary=gzip.decompress((OUT/'baseline87.bin.gz').read_bytes())
    assert len(baseline['parts'])==87 and hashlib.sha256(base_binary).hexdigest()==BASE_SHA
    assert baseline['source']['sha256']==SHA
    assert np.array_equal(AXIS.T@AXIS,np.eye(3)) and np.linalg.det(AXIS)==1
    manifest=json.loads(json.dumps(baseline))
    blob=bytearray(base_binary)
    specs=json.loads((OUT/'new-object-mapping.json').read_text())
    assert len(specs)==32
    inspection={r['sourceObject']:r for r in json.loads((OUT/'evaluated-candidates.json').read_text())['candidates']}
    depsgraph=bpy.context.evaluated_depsgraph_get()
    raw={};checks=[]

    def append(values,dtype):
        while len(blob)%4:blob.append(0)
        offset=len(blob);blob.extend(np.asarray(values,dtype=dtype).tobytes());return offset

    for spec in specs:
        name=spec['sourceObject'];obj=bpy.data.objects[name];assert obj.type=='MESH'
        evaluated=obj.evaluated_get(depsgraph);mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
        world=np.array([list(evaluated.matrix_world@v.co) for v in mesh.vertices],dtype=float)
        indices=np.array([list(t.vertices) for t in mesh.loop_triangles],dtype=np.int64)
        determinant=float(evaluated.matrix_world.to_3x3().determinant())
        if determinant<0:indices=indices[:,[0,2,1]]
        source_hash=hashlib.sha256(world.astype('<f8').tobytes()+indices.astype('<i8').tobytes()).hexdigest()
        assert source_hash==inspection[name]['geometry']['evaluatedWorldGeometrySha256'],name
        metadata=dict(name=name,objectType=obj.type,dataBlock=obj.data.name,
            materials=[m.name for m in obj.data.materials if m],collections=[c.name for c in obj.users_collection],
            parent=obj.parent.name if obj.parent else None,baseVertices=len(obj.data.vertices),basePolygons=len(obj.data.polygons),
            evaluatedVertices=len(world),evaluatedTriangles=len(indices),
            evaluation='evaluated viewport dependency graph; authored visible modifiers preserved',
            worldMatrix=[list(r) for r in evaluated.matrix_world],worldDeterminant=determinant,mirroredWindingCorrected=determinant<0,
            sourceWorldBounds=[world.min(0).tolist(),world.max(0).tolist()],
            modifiers=[dict(name=m.name,type=m.type,showViewport=m.show_viewport,showRender=m.show_render,levels=getattr(m,'levels',None),renderLevels=getattr(m,'render_levels',None)) for m in obj.modifiers],
            topology=inspection[name]['geometry']['topology'],evaluatedWorldGeometrySha256=source_hash)
        evaluated.to_mesh_clear()
        sign=1 if spec['side']=='left' else -1
        assert np.all(sign*world[:,0]>0),name
        reference=world@AXIS;positions=reference.astype('<f4');indices=indices.astype('<u4')
        tri=positions[indices].astype(float);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);area=np.linalg.norm(cross,axis=1)
        assert np.all(area>0) and np.all(np.isfinite(positions)),name
        unit=cross/area[:,None];normals=np.zeros_like(positions,dtype=float)
        for corner in range(3):
            a=tri[:,(corner+1)%3]-tri[:,corner];b=tri[:,(corner+2)%3]-tri[:,corner]
            angles=np.arccos(np.clip(np.sum(a*b,axis=1)/(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1)),-1,1))
            np.add.at(normals,indices[:,corner],unit*angles[:,None])
        lengths=np.linalg.norm(normals,axis=1);used=np.zeros(len(positions),dtype=bool);used[np.unique(indices)]=True
        loose=~used;cancelled=used&(lengths==0)
        for vertex in np.flatnonzero(cancelled):
            incident=np.flatnonzero(np.any(indices==vertex,axis=1));normals[vertex]=unit[incident[np.argmax(area[incident])]];lengths[vertex]=1
        normals[loose]=[0,1,0];lengths[loose]=1;normals/=lengths[:,None]
        encoded=np.rint(normals*32767).astype('<i2');decoded=encoded.astype(float)/32767
        dots=np.sum(decoded[indices].mean(1)*unit,axis=1)
        sorted_faces=np.sort(indices,axis=1);_,face_counts=np.unique(sorted_faces,axis=0,return_counts=True)
        check=dict(partId=spec['partId'],sourceObject=name,nonpositiveInterpolatedFaceNormals=int(np.sum(dots<=0)),
            minFaceNormalDot=float(dots.min()),cancelledVertexNormals=int(np.sum(cancelled)),
            duplicateIndexFaceSets=int(np.sum(face_counts>1)),duplicateFaceExtraCount=int(np.sum(face_counts-1)),
            minDoubleTriangleArea=float(area.min()),maxNormalLengthError=float(np.max(abs(np.linalg.norm(decoded,axis=1)-1))),
            maxFloat32PositionErrorMeters=float(np.max(abs(reference-positions))),**inspection[name]['geometry']['topology'])
        assert check['zeroAreaTriangles']==0 and check['nonManifoldEdges']==0 and check['boundaryEdges']==0,name
        assert check['maxNormalLengthError']<.00003,name
        part=dict(id=spec['partId'],datasetId=baseline['datasetId'],conceptId=spec['conceptId'],name=spec['side'].title()+' '+name[:-2].strip('()').lower(),
            side=spec['side'],system=spec['system'],componentRole=spec['componentRole'],role=spec['role'],chunk=0,
            positions=append(positions,'<f4'),normals=append(encoded,'<i2'),indices=append(indices,'<u4'),
            vertexCount=len(positions),indexCount=int(indices.size),bounds=[positions.min(0).tolist(),positions.max(0).tolist()],
            sourceObject=name,sourceObjectType='MESH',sourceGeometry=metadata,
            normalMethod='angle-weighted face normals quantized to signed 16-bit',looseVertices=int(np.sum(loose)),cancelledVertexNormals=int(np.sum(cancelled)),
            cancelledVertexNormalFallback='Largest incident face normal for source vertices whose angle-weighted normals cancel; faces and positions unchanged',
            sourceScope=spec['scope'],expertReview='pending')
        manifest['parts'].append(part);manifest['concepts'].append(dict(id=part['conceptId'],name=part['name'],elements=[part['id']]))
        checks.append(check);raw[part['id']]=(reference,indices)

    binary=bytes(blob);compressed=gzip.compress(binary,compresslevel=9,mtime=0)
    assert binary[:len(base_binary)]==base_binary
    assert gzip.decompress(compressed)==binary
    assert len(manifest['parts'])==len(manifest['concepts'])==119
    for p in manifest['parts']:
        v=np.frombuffer(binary,dtype='<f4',count=p['vertexCount']*3,offset=p['positions']).reshape(-1,3)
        n=np.frombuffer(binary,dtype='<i2',count=p['vertexCount']*3,offset=p['normals']).reshape(-1,3).astype(float)/32767
        f=np.frombuffer(binary,dtype='<u4',count=p['indexCount'],offset=p['indices']).reshape(-1,3)
        assert np.all(np.isfinite(v)) and f.max()<len(v) and np.max(abs(np.linalg.norm(n,axis=1)-1))<.00003
        assert [v.min(0).tolist(),v.max(0).tolist()]==p['bounds']
        assert all(p[k]%4==0 for k in ['positions','normals','indices'])
        if p['id'] in raw:
            assert np.array_equal(v,raw[p['id']][0].astype('<f4')) and np.array_equal(f,raw[p['id']][1])
    manifest.update(version='Z-Anatomy independent lower-limb and intrinsic-foot reference candidate 3',
        releaseStatus='candidate-integration-and-expert-review-pending',
        scope='Sixteen nerve curves, two fibular artery curves, six ankle ligament surfaces, thirty source-named intrinsic foot muscle objects and sixty-five bone objects including compound sesamoid groups. Compound interosseous/lumbrical/sesamoid objects retain source scope; full innervation/circulation/support detail and expert acceptance remain open.',
        triangles=sum(p['indexCount']//3 for p in manifest['parts']),
        candidateBaseline=dict(manifestSha256=BASE_MANIFEST_SHA,binarySha256=BASE_SHA,parts=87,geometryPreservation='Entire baseline binary prefix and all offsets/arrays unchanged'),
        candidateSourceReview='data/model-candidates/foot-soft-tissue-source-audit-v1/REVIEW.md')
    manifest['chunks']=[dict(url='/models/lower-limb-nerve-reference/anatomy.bin',bytes=len(binary),gzip='/models/lower-limb-nerve-reference/anatomy.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())]
    manifest['inheritedMeshDefects'].extend(c for c in checks if c['nonpositiveInterpolatedFaceNormals'] or c['cancelledVertexNormals'] or c['duplicateFaceExtraCount'] or c['looseVertices'])
    (PACKAGE_OUT/'atlas.json').write_text(json.dumps(manifest,indent=2)+'\n');(PACKAGE_OUT/'anatomy.bin').write_bytes(binary);(PACKAGE_OUT/'anatomy.bin.gz').write_bytes(compressed)
    report=dict(parts=119,newParts=32,newMuscles=30,newSesamoidObjects=2,vertices=sum(p['vertexCount'] for p in manifest['parts']),triangles=manifest['triangles'],
        newVertices=sum(p['vertexCount'] for p in manifest['parts'][87:]),newTriangles=sum(p['indexCount']//3 for p in manifest['parts'][87:]),
        bytes=len(binary),gzipBytes=len(compressed),sourceSha256=SHA,binarySha256=hashlib.sha256(binary).hexdigest(),gzipSha256=hashlib.sha256(compressed).hexdigest(),
        manifestSha256=hashlib.sha256((PACKAGE_OUT/'atlas.json').read_bytes()).hexdigest(),baselinePreservation='PASS: entire 2,643,600-byte original binary prefix preserved; original87 part/concept records unchanged',
        checks=checks)
    assert manifest['parts'][:87]==baseline['parts'] and manifest['concepts'][:87]==baseline['concepts']
    (OUT/'geometry-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    for name in ['ATTRIBUTION.md','UPSTREAM-LICENSE.txt']:
        (PACKAGE_OUT/name).write_bytes((OUT/name).read_bytes())
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2),flush=True)

    if render:
        scene=bpy.data.scenes.new('Intrinsic foot source-decoded QA');bpy.context.window.scene=scene
        scene.world=bpy.data.worlds.new('Foot QA world');scene.world.use_nodes=True
        scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.055,.065,.08,1);scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
        scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.cycles.transparent_max_bounces=32
        scene.render.resolution_x=1400;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
        def material(name,color,alpha):
            m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear()
            out=n.new('ShaderNodeOutputMaterial');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha
            clear=n.new('ShaderNodeBsdfTransparent');surface=n.new('ShaderNodeBsdfPrincipled');surface.inputs['Base Color'].default_value=(*color,1);surface.inputs['Roughness'].default_value=.6
            m.node_tree.links.new(clear.outputs[0],mix.inputs[1]);m.node_tree.links.new(surface.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],out.inputs['Surface']);return m
        mats={'context':material('Bone context',(.8,.85,.9),.14),'muscle':material('Source muscle',(.72,.22,.2),1),'sesamoid':material('Sesamoid context',(.1,.75,.8),1)}
        objects=[]
        for panel,shift in [('source',-.13),('decoded',.13)]:
            for p in manifest['parts']:
                if p['side']!='left':continue
                is_new=p['id'] in raw
                if not is_new and not (p['componentRole']=='bone' and p['bounds'][1][1]<.17):continue
                v=np.frombuffer(binary,dtype='<f4',count=p['vertexCount']*3,offset=p['positions']).reshape(-1,3)
                f=np.frombuffer(binary,dtype='<u4',count=p['indexCount'],offset=p['indices']).reshape(-1,3)
                if panel=='source' and is_new:v,f=raw[p['id']]
                mesh=bpy.data.meshes.new(panel+'-'+p['id']);mesh.from_pydata((v+np.array([shift,0,0])).tolist(),[],f.tolist());mesh.update()
                obj=bpy.data.objects.new(mesh.name,mesh);scene.collection.objects.link(obj)
                key='muscle' if p['componentRole']=='muscle' else 'sesamoid' if is_new else 'context';obj.data.materials.append(mats[key])
                for poly in mesh.polygons:poly.use_smooth=True
                if panel=='decoded':
                    n=np.frombuffer(binary,dtype='<i2',count=p['vertexCount']*3,offset=p['normals']).reshape(-1,3).astype(float)/32767;mesh.normals_split_custom_set_from_vertices(n.tolist())
                objects.append((obj,p,panel))
        for pos in [(.8,-.8,.6),(-.7,.8,-.5)]:
            light=bpy.data.lights.new('Foot QA area','AREA');light.energy=90;light.size=1
            obj=bpy.data.objects.new(light.name,light);scene.collection.objects.link(obj);obj.location=pos;obj.rotation_euler=(Vector((.1,.06,.02))-obj.location).to_track_quat('-Z','Y').to_euler()
        camera=bpy.data.cameras.new('Foot QA camera');camera.type='ORTHO';co=bpy.data.objects.new(camera.name,camera);scene.collection.objects.link(co);scene.camera=co
        def view(filename,direction,include=None):
            for obj,p,panel in objects:
                obj.hide_render=include is not None and p['componentRole']=='muscle' and p['sourceObject'] not in include
            center=Vector((.095,.06,.025));co.location=center+Vector(direction);back=(co.location-center).normalized()
            up=Vector((0,1,0)) if abs(back.y)<.9 else Vector((0,0,1));right=up.cross(back).normalized();co.rotation_euler=Matrix((right,back.cross(right),back)).transposed().to_euler()
            camera.ortho_scale=.49;scene.render.filepath=str(OUT/filename);bpy.ops.render.render(write_still=True)
        view('source-decoded-plantar-all.png',(0,-1,.1))
        view('source-decoded-plantar-deep.png',(0,-1,.1),{p['sourceObject'] for p in manifest['parts'][87:] if p['componentRole']=='muscle' and not p['sourceObject'].startswith(('Abductor','Flexor digitorum brevis','Extensor'))})
        view('source-decoded-dorsal.png',(0,1,.1),{'Extensor digitorum brevis.l','Extensor hallucis brevis.l','Dorsal interossei muscles of foot.l'})
        view('source-decoded-sesamoids.png',(0,-1,.05),{'Medial head of flexor hallucis brevis.l','Lateral head of flexor hallucis brevis.l'})
    (OUT/'latest-run-timing.json').write_text(json.dumps(dict(scriptSeconds=time.monotonic()-START,rendered=render),indent=2)+'\n')

    return report


if __name__ == '__main__':
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    output=Path(args[args.index('--output')+1]) if '--output' in args else None
    build_candidate(output_dir=output,render='--render' in args)
