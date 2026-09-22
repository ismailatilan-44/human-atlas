"""Blender --background --disable-autoexec --python <this file> [-- --render].
Candidate only: actual BP3D source triangles, no fitted transform or surface reconstruction.
"""
import bpy,json,gzip,hashlib,zipfile,sys,re
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
atlas=json.loads((ROOT/'public/models/atlas.json').read_text());ap={p['id']:p for p in atlas['parts']};ac={c['id']:c for c in atlas['concepts']}
chunks=[(ROOT/'public'/c['url'].lstrip('/')).read_bytes() for c in atlas['chunks']]
def target(id):
 p=ap[id];b=chunks[p['chunk']]
 return np.frombuffer(b,dtype='<f4',count=p['vertexCount']*3,offset=p['positions']).reshape(-1,3).astype(float),np.frombuffer(b,dtype='<u4',count=p['indexCount'],offset=p['indices']).reshape(-1,3)
def loadzip(filename):
 result={}
 with zipfile.ZipFile(OUT/filename) as z:
  for member in z.namelist():
   if not member.endswith('.obj'):continue
   text=z.read(member).decode();v=[];f=[];header={}
   for line in text.splitlines():
    if line.startswith('# ') and ' : ' in line: k,value=line[2:].split(' : ',1);header[k]=value
    cs=line.split()
    if not cs:continue
    if cs[0]=='v':
     x,y,z0=map(float,cs[1:4]);v.append([x*.001,z0*.001+.0781112,-y*.001-.1])
    elif cs[0]=='f':
     ids=[int(t.split('/')[0])-1 for t in cs[1:]]
     for i in range(1,len(ids)-1):f.append([ids[0],ids[i],ids[i+1]])
   result[header['File ID']]=dict(member=member,header=header,v=np.array(v,dtype='<f4'),f=np.array(f,dtype='<u4'),sha256=hashlib.sha256(text.encode()).hexdigest())
 return result
sources=loadzip('lung-parenchyma-source.zip');refs=loadzip('thoracic-references.zip')
assert set(sources)=={'FJ'+str(i) for i in range(6595,6613)}
with zipfile.ZipFile(OUT/'bp3d-v43-mapping.zip') as z:mapping=z.read('FMA2Obj.txt').decode()
assert '# Data Version\t4.3' in mapping and '# Objects set\t4.3' in mapping and '# Tree version\tFMA3.0' in mapping
assert all(o['header']['Compatibility version']=='4.3' and o['header']['Build-up logic']=='FMA 3.0 part_of' for o in sources.values())
relations={}
for line in mapping.splitlines():
 if line.startswith('#') or not line.strip():continue
 id,tree,els=line.split('\t');relations[id,tree]=els.split('+')
def distances(v,tv,tf):
 tree=BVHTree.FromPolygons(tv.tolist(),tf.tolist(),all_triangles=True)
 return np.array([tree.find_nearest(Vector(p))[3] for p in v])*1000
metrics=[]
for id,obj in refs.items():
 tv,tf=target(id);sv,sf=obj['v'],obj['f'];d=np.concatenate([distances(sv,tv,tf),distances(tv,sv,sf)])
 metrics.append(dict(partId=id,name=ap[id]['name'],reference='independent_same_id_no_fit',rmsMm=float(np.sqrt(np.mean(d*d))),p95Mm=float(np.percentile(d,95)),maxMm=float(d.max()),sourceSha256=obj['sha256']))
assert max(m['rmsMm'] for m in metrics)<.1, metrics
blob=bytearray();parts=[];quality=[];geometries={}
def append(a,dtype):
 while len(blob)%4:blob.append(0)
 off=len(blob);blob.extend(np.asarray(a,dtype=dtype).tobytes());return off
for id,obj in sorted(sources.items()):
 v,f=obj['v'],obj['f'];tri=v[f].astype(float);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);nondeg=np.linalg.norm(cross,axis=1)>1e-15
 removed=int(np.sum(~nondeg));f=f[nondeg];cross=cross[nondeg];tri=tri[nondeg]
 # Original positions are retained; zero averaged normals receive a finite fallback.
 unique,inv=np.unique(v,axis=0,return_inverse=True);n=np.zeros_like(unique,dtype=float)
 for corner in range(3):np.add.at(n,inv[f[:,corner]],cross)
 norm=np.linalg.norm(n,axis=1);zero=norm<1e-20;n[~zero]/=norm[~zero,None];n[zero]=[0,1,0];n=n[inv]
 wf=inv[f];edges=np.sort(np.concatenate([wf[:,[0,1]],wf[:,[1,2]],wf[:,[2,0]]]),axis=1);_,counts=np.unique(edges,axis=0,return_counts=True)
 h=obj['header'];concept=h['Concept ID'];assert id in relations.get((concept,'is_a'),[])+relations.get((concept,'part_of'),[])
 q=dict(sourceId=id,rawVertices=len(v),uniquePositions=len(unique),renderTriangles=len(f),removedDegenerateTriangles=removed,unusedOrZeroNormalPositions=int(np.sum(zero)),unusedUniquePositions=int(len(unique)-len(np.unique(inv[f]))),boundaryEdgesAfterExactPositionWeld=int(sum(counts==1)),nonManifoldEdgesAfterExactPositionWeld=int(sum(counts>2)),signedVolumeCm3=float(np.sum(np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])))/6*1e6),bounds=[v.min(0).tolist(),v.max(0).tolist()])
 quality.append(q);geometries[id]=(v,f)
 parts.append(dict(id='BP43-'+id,conceptId=concept,name=h['English name'],system='respiratory',chunk=0,positions=append(v,'<f4'),normals=append(np.rint(n*32767),'<i2'),indices=append(f,'<u4'),vertexCount=len(v),indexCount=int(f.size),bounds=q['bounds'],sourceId=id,sourceConceptId=concept,sourceObject=obj['member'],sourceObjectType='OBJ',sourceSha256=obj['sha256'],sourceHeader=h,quality=q,representation='source_segment_parenchyma_surface',expertReview='pending'))
concepts={}
for p in parts:
 concepts.setdefault(p['conceptId'],dict(id=p['conceptId'],name=p['name'],elements=[]))['elements'].append(p['id'])
groups=[]
for id in ['FMA7333','FMA7383','FMA7337','FMA7370','FMA7371','FMA7309','FMA7310']:
 ids=[x for x in relations[id,'part_of'] if x in sources]
 group=dict(id=id,name=ac[id]['name'],elements=['BP43-'+x for x in ids],sourceMembership='Official 4.3 part_of mapping restricted to these 18 parenchyma surface records')
 concepts[id]=group;groups.append(group)
parentEvidence=json.loads((OUT/'direct-parent-source-evidence.json').read_text())
parentMemberships=[]
for relation in parentEvidence['relations']:
 parent=relation['object'];leaf=relation['subject'];sourceIds=sorted(set(relations[parent,'part_of'])&set(sources));leafIds=sorted(p['sourceId'] for p in parts if p['conceptId']==leaf)
 assert sourceIds==leafIds and sourceIds, (parent,leaf,sourceIds,leafIds)
 assert parent in ac and parent not in concepts
 group=dict(id=parent,name=ac[parent]['name'],elements=['BP43-'+x for x in sourceIds],sourceMembership='Official 4.3/FMA3.0 part_of row restricted to these 18 parenchyma surfaces; corroborated direct source segment parent')
 concepts[parent]=group;groups.append(group)
 parentMemberships.append(dict(parentConceptId=parent,parenchymaConceptId=leaf,sourceIds=sourceIds,relationEvidence=relation['evidence'],qualifiers=relation['qualifiers']))
assert len(parentMemberships)==17
assert sorted(x for g in groups[:5] for x in g['elements'])==sorted(p['id'] for p in parts)
discrepancies=[]
for label,narrow,broad in [('left lung parenchyma vs left lung','FMA27364','FMA7310'),('left upper-lobe parenchyma vs left upper lobe','FMA31242','FMA7370'),('right lung parenchyma vs right lung','FMA27363','FMA7309')]:
 a=set(relations[narrow,'part_of'])&set(sources);b=set(relations[broad,'part_of'])&set(sources)
 discrepancies.append(dict(comparison=label,narrowParenchymaConceptId=narrow,lungOrLobeConceptId=broad,narrowSourceIds=sorted(a),lungOrLobeSourceIds=sorted(b),onlyInLungOrLobe=sorted(b-a),onlyInNarrow=sorted(a-b),resolution='Neither mapping is rewritten. Candidate uses named lung/lobe part_of groups, not the narrower conflicting parenchyma aggregate.'))
(OUT/'source-mapping-review.json').write_text(json.dumps(dict(groups=groups,sourceAggregateDiscrepancies=discrepancies,directParentMemberships=parentMemberships,leafIdentityBasis='OBJ header specific Concept ID corroborated by official FMA2Obj membership; legacy catalog fma_id is first encountered ancestor, not canonical leaf identity.'),indent=2)+'\n')
binary=bytes(blob);compressed=gzip.compress(binary,compresslevel=9,mtime=0)
(OUT/'lung-parenchyma.bin').write_bytes(binary);(OUT/'lung-parenchyma.bin.gz').write_bytes(compressed)
manifest=dict(version='BodyParts3D 4.3 lung parenchyma candidate 1',status='candidate_not_integrated',sex='male',parts=parts,concepts=list(concepts.values()),extendsConceptIds=[g['id'] for g in groups],chunks=[dict(url='lung-parenchyma.bin',bytes=len(binary),gzip='lung-parenchyma.bin.gz',gzipBytes=len(compressed),sha256=hashlib.sha256(binary).hexdigest())],triangles=sum(p['indexCount']//3 for p in parts),source=dict(id='bodyparts3d-4.3-live',url='https://lifesciencedb.jp/bp3d/?lng=en',license='CC-BY-SA-2.1-JP',attribution='ATTRIBUTION.md',archiveSha256=sha(OUT/'lung-parenchyma-source.zip'),mappingDataVersion='4.3',mappingObjectsSet='4.3',mappingTreeVersion='FMA3.0',objBuildUpLogic='FMA 3.0 part_of',conceptBuildId='not supplied by mapping endpoint; companion direct-parent evidence separately pins cb_id=5 / FMA3.0',mappingSha256=sha(OUT/'bp3d-v43-mapping.zip')),surfaceGroups=groups,sourceAggregateDiscrepancies=discrepancies,directParentMemberships=parentMemberships,registration=dict(method='Unmodified main atlas mm/Z-up to m/Y-up BP3D conversion; nine same-ID thoracic reference measurements, no fitting',matrixColumnVector=[[.001,0,0,0],[0,0,.001,.0781112],[0,-.001,0,-.1],[0,0,0,1]],sourceAxes='X left, Y posterior, Z superior',targetAxes='X left, Y superior, Z anterior',sourceUnits='millimeters',targetUnits='meters',targetManifestSha256=sha(ROOT/'public/models/atlas.json'),measurements=metrics),limitations=['18 source parenchyma surface records in 17 source segment concepts; grouped into five source lobe memberships. Not 18 reconstructed lobes or a clinical segmentation.','Keep existing vessels/bronchi in original lung/lobe and 17 bronchopulmonary segment concepts when merging; use surfaceGroups if a parenchyma-surface-only view is needed.','No fitting, deformation, smoothing, surface inference or replacement of vessels with an envelope.','Exact-position normal averaging and degenerate-face omission affect rendering only; original source ZIP is retained.','FJ6598 has four non-manifold edges after exact-position weld and two used source positions with zero averaged normals; no clinical-volume or watertight-manifold guarantee.', 'Narrow source aggregate FMA27364 and FMA31242 omit FJ6598; FMA27363 omits FJ6608 and FJ6609. These conflicting narrower aggregates are not exported or silently repaired. Named lung/lobe memberships follow their own official part_of mapping.', 'Individual male source reference. Visible segment seams and local source irregularities remain; low registration residual does not certify expert anatomy acceptance or complete vessel containment.', 'See actual quality metrics and renders before deciding anatomical coverage, fissure quality or completeness.'])
(OUT/'lung-parenchyma.json').write_text(json.dumps(manifest,indent=2)+'\n')
base_evidence=[]
for id in ['FMA7309','FMA7310','FMA7333','FMA7337','FMA7370','FMA7371','FMA7383']:
 c=ac[id];base_evidence.append(dict(conceptId=id,name=c['name'],partCount=len(c['elements']),sourcePartNames=[dict(id=p,name=ap[p]['name']) for p in c['elements']],parenchymaSourceOverlap=sorted(set(c['elements'])&set(sources))))
(OUT/'geometry-proof.json').write_text(json.dumps(dict(registration=metrics,quality=quality,baseConceptEvidence=base_evidence,sourceMemberCount=len(sources)),indent=2)+'\n')
print('SUMMARY',json.dumps(dict(parts=len(parts),concepts=len(concepts),triangles=manifest['triangles'],rawBytes=len(binary),gzipBytes=len(compressed),registration=metrics,quality=quality)),flush=True)
if '--render' in sys.argv:
 scene=bpy.data.scenes.new('Actual BP3D lung inspection');bpy.context.window.scene=scene
 scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True;scene.cycles.transparent_max_bounces=32
 scene.render.resolution_x=1400;scene.render.resolution_y=1200;scene.render.resolution_percentage=100
 scene.world=bpy.data.worlds.new('Inspection world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.08,.10,.14,1)
 def mat(name,col,alpha=1):
  m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;surf=n.get('Principled BSDF');surf.inputs['Base Color'].default_value=(*col,1);surf.inputs['Roughness'].default_value=.65
  if alpha<1:
   mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;t=n.new('ShaderNodeBsdfTransparent');m.node_tree.links.new(t.outputs[0],mix.inputs[1]);m.node_tree.links.new(surf.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],n.get('Material Output').inputs['Surface'])
  return m
 def add(name,v,f,m):
  mesh=bpy.data.meshes.new(name);mesh.from_pydata(v.tolist(),[],f.tolist());mesh.update();o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);mesh.materials.append(m)
  for face in mesh.polygons:face.use_smooth=True
  return o
 colors=[(.85,.30,.23),(.93,.60,.17),(.72,.22,.50),(.15,.63,.73),(.25,.40,.82)]
 surfaces=[]
 for group,col in zip(groups[:5],colors):
  material=mat(group['name'],col)
  for id in group['elements']:
   v,f=geometries[id.replace('BP43-','')];surfaces.append(add(id,v,f,material))
 vesselmat=mat('Base atlas vessels',(.70,.27,.24));airmat=mat('Base atlas bronchi',(.86,.83,.68));bonemat=mat('Base ribs and sternum',(.65,.71,.76),.12)
 baseobjs=[];contextobjs=[]
 for id in dict.fromkeys(ac['FMA7309']['elements']+ac['FMA7310']['elements']):
  v,f=target(id);baseobjs.append(add('Base '+id,v,f,airmat if ap[id]['system']=='respiratory' else vesselmat))
 for id in ac['FMA7574']['elements']+ac['FMA7485']['elements']+['FJ2541']:
  v,f=target(id);contextobjs.append(add('Context '+id,v,f,airmat if id=='FJ2541' else bonemat))
 center=Vector((0,1.30,-.01));camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=.44
 for name,pos,energy in [('Key',(.25,1.6,.45),7),('Fill',(-.4,1.35,.15),4)]:
  light=bpy.data.objects.new(name,bpy.data.lights.new(name,'AREA'));scene.collection.objects.link(light);light.data.energy=energy;light.data.size=.6;light.location=pos;light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
 for name,pos,show_source,show_base,show_context in [('base-lung-groups-front',(0,1.30,.8),False,True,False),('candidate-lobes-front',(0,1.30,.8),True,False,False),('candidate-lobes-oblique',(.55,1.35,.6),True,False,True),('candidate-lobes-posterior',(0,1.30,-.8),True,False,False),('candidate-source-with-base-trees',(.55,1.35,.6),True,True,False)]:
  for o in surfaces:o.hide_render=not show_source
  for o in baseobjs:o.hide_render=not show_base
  for o in contextobjs:o.hide_render=not show_context
  # This view exposes tree/surface relationship without changing mesh coordinates.
  if name=='candidate-source-with-base-trees':
   for o in surfaces:
    original=o.data.materials[0];col=original.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value[:3];o.data.materials.clear();o.data.materials.append(mat(o.name+' transparent',col,.15))
  camera.location=pos;forward=(center-camera.location).normalized();right=forward.cross(Vector((0,1,0))).normalized();up=right.cross(forward).normalized();camera.rotation_euler=Matrix((right,up,-forward)).transposed().to_euler();scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
