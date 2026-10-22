import type {Part} from './anatomy';
export interface LayoutCell {x:number;y:number;width:number;height:number}
/** Pack only visible source meshes. Every projected bounding box gets its own cell. */
export function createExplosionLayout(parts:Part[],aspect=1){
 const cards=parts.map(p=>({id:p.id,system:p.system,width:Math.max(.035,p.bounds[1][0]-p.bounds[0][0])+.04,height:Math.max(.035,p.bounds[1][1]-p.bounds[0][1])+.04}));
 const area=cards.reduce((n,c)=>n+c.width*c.height,0),maxWidth=Math.max(.3,...cards.map(c=>c.width));
 const targetWidth=Math.max(maxWidth,Math.sqrt(area*Math.max(.5,Math.min(1.5,aspect)))*1.18);
 cards.sort((a,b)=>b.height-a.height||a.id.localeCompare(b.id));
 const cells=new Map<string,LayoutCell>();let x=0,y=0,row=0,usedWidth=0;
 for(const c of cards){if(x>0&&x+c.width>targetWidth){x=0;y+=row;row=0;}cells.set(c.id,{x:x+c.width/2,y:-y-c.height/2,width:c.width,height:c.height});x+=c.width;usedWidth=Math.max(usedWidth,x);row=Math.max(row,c.height);}
 const height=y+row;
 cells.forEach(c=>{c.x-=usedWidth/2;c.y+=height/2;});
 return {cells,width:usedWidth,height};
}

type Triple = [number, number, number];
type VectorLike = readonly number[] | { x: number; y: number; z: number };
const tuple = (v: VectorLike): Triple => 'x' in v ? [v.x, v.y, v.z] : [v[0], v[1], v[2]];
const dot = (a: Triple, b: Triple) => a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
const cross = (a: Triple,b: Triple): Triple => [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const normal = (a: Triple): Triple => {const length=Math.hypot(...a);return length>1e-12 ? a.map(v=>v/length) as Triple : [0,0,1];};
function cameraCards(parts: Part[], viewDirection: VectorLike) {
 const direction=normal(tuple(viewDirection));
 const right=normal(cross(Math.hypot(direction[0],direction[2])<1e-10 ? [0,0,-Math.sign(direction[1])] : [0,1,0],direction));
 const up=cross(direction,right);
 const cards=parts.map(p=>{
  const half=p.bounds[0].map((v,i)=>(p.bounds[1][i]-v)/2);
  const corners: Triple[]=[];
  for(const x of [-half[0],half[0]]) for(const y of [-half[1],half[1]]) for(const z of [-half[2],half[2]]) {
   const corner: Triple=[x,y,z]; corners.push([dot(corner,right),dot(corner,up),dot(corner,direction)]);
  }
  return {id:p.id,corners,width:2*Math.max(...corners.map(c=>c[0]))+.04,height:2*Math.max(...corners.map(c=>c[1]))+.04};
 });
 return {cards,right,up,direction};
}

/** Minimum orbit distance bounding perspective magnification of translated source bounds. */
export function explosionMinimumDistance(parts: Part[], direction: VectorLike, targetOffset: VectorLike=[0,0,0]) {
 const basis=cameraCards(parts,direction);
 return Math.max(.07,8*Math.max(0,...basis.cards.flatMap(c=>c.corners.map(v=>v[2])))+.02-dot(tuple(targetOffset),basis.direction));
}

/**
 * Rigidly translate source meshes onto a camera-facing inventory plane.
 * `direction` points from target toward camera; `targetOffset` is target minus a
 * fixed layout origin, in world coordinates. Returned centers are relative to
 * that origin. Cells are exact perspective bounds (plus padding), expressed in
 * world units on that plane. No source geometry is rotated or scaled.
 *
 * Recompute after zoom/pan, without fitting the camera again. Placement remains
 * anchored to the fixed origin so panning does not get cancelled by recentering.
 * A caller fitting the layout can iterate distance and layout, then use the last
 * layout at its final camera distance. Honor actualDistance if a near pose was
 * clamped to keep the camera outside all translated geometry.
 */
export function createCameraExplosionLayout(parts: Part[], aspect: number, viewDirection: VectorLike, distance: number, targetOffset: VectorLike=[0,0,0]) {
 const {cards,right,up,direction}=cameraCards(parts,viewDirection);
 const target=tuple(targetOffset),px=dot(target,right),py=dot(target,up),pz=dot(target,direction);
 const minimumDistance=Math.max(.07,8*Math.max(0,...cards.flatMap(c=>c.corners.map(v=>v[2])))+.02-pz);
 const actualDistance=Math.max(distance,minimumDistance),depth=actualDistance+pz;
 const area=cards.reduce((sum,c)=>sum+c.width*c.height,0);
 const targetWidth=Math.max(.3,...cards.map(c=>c.width),Math.sqrt(area*Math.max(.5,Math.min(1.5,aspect)))*1.18);
 cards.sort((a,b)=>b.height-a.height||a.id.localeCompare(b.id));
 // Use an orthographic row pass only to anchor the inventory around its origin.
 // Exact perspective rows below may grow, but never overlap or follow the pan.
 let estimateX=0,estimateY=0,estimateRow=0;
 for(const c of cards){if(estimateX>0&&estimateX+c.width>targetWidth){estimateX=0;estimateY+=estimateRow;estimateRow=0;}estimateX+=c.width;estimateRow=Math.max(estimateRow,c.height);}
 const top=(estimateY+estimateRow)/2,left=-targetWidth/2;
 const cells=new Map<string,LayoutCell>(),centers=new Map<string,Triple>();
 let x=left,y=top,row=0,minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity;
 const place=(c: typeof cards[number],cellLeft:number,cellTop:number)=>{
  const gap=Math.max(.02,Math.abs(cellLeft)*1e-12,Math.abs(cellTop)*1e-12);
  // For each corner, solve (translation + corner - pan)/(1-z/depth)
  // against the desired left/top. This accounts for off-axis depth expansion.
  const tx=px+Math.max(...c.corners.map(v=>(cellLeft+gap-px)*(1-v[2]/depth)-v[0]));
  const ty=py+Math.min(...c.corners.map(v=>(cellTop-gap-py)*(1-v[2]/depth)-v[1]));
  const projected=c.corners.map(v=>[(tx+v[0]-px)/(1-v[2]/depth)+px,(ty+v[1]-py)/(1-v[2]/depth)+py]);
  const cellRight=Math.max(...projected.map(v=>v[0]))+gap;
  const cellBottom=Math.min(...projected.map(v=>v[1]))-gap;
  return {tx,ty,cellRight,cellBottom};
 };
 for(const c of cards){
  let placed=place(c,x,y);
  if(x>left&&placed.cellRight>left+targetWidth){x=left;y-=row;row=0;placed=place(c,x,y);}
  const {tx,ty,cellRight,cellBottom}=placed;
  cells.set(c.id,{x:(x+cellRight)/2,y:(y+cellBottom)/2,width:cellRight-x,height:y-cellBottom});
  centers.set(c.id,right.map((v,i)=>v*tx+up[i]*ty) as Triple);
  minX=Math.min(minX,x);maxX=Math.max(maxX,cellRight);minY=Math.min(minY,cellBottom);maxY=Math.max(maxY,y);
  row=Math.max(row,y-cellBottom);x=cellRight;
 }
 return {cells,centers,width:cards.length?2*Math.max(Math.abs(minX),Math.abs(maxX)):0,height:cards.length?2*Math.max(Math.abs(minY),Math.abs(maxY)):0,minimumDistance,actualDistance,right,up,direction};
}
