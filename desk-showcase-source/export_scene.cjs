const fs=require('fs'); const THREE=require('./three.min.js');
let source=fs.readFileSync(__dirname+'/source-index.html','utf8');
let begin=source.indexOf('  const M = {'), end=source.indexOf('  // Labels');
let body=source.slice(begin,end);
body=body.replace('  const M = {','  const M = {');
body=body.replace('  // Units: cm.',"  for(const [name,mat] of Object.entries(M)) mat.userData.name=name;\n  // Units: cm.");
const scene=new THREE.Scene();function woodTex(){return null;}
eval(body);
scene.updateMatrixWorld(true);
const output=[];
scene.traverse(obj=>{
 if(!obj.isMesh)return;
 let geo=obj.geometry.clone(); if(geo.index)geo=geo.toNonIndexed();geo.applyMatrix4(obj.matrixWorld);
 const p=geo.getAttribute('position'),n=geo.getAttribute('normal'),uv=geo.getAttribute('uv');
 const mat=obj.material;const e=mat.emissive?mat.emissive.clone().multiplyScalar(mat.emissiveIntensity??1):new THREE.Color(0);
 output.push({positions:Array.from(p.array),normals:Array.from(n.array),uv:uv?Array.from(uv.array):null,color:[mat.color.r,mat.color.g,mat.color.b],emissive:[e.r,e.g,e.b],name:mat.userData.name||'',opacity:mat.opacity,roughness:mat.roughness??.5,shadow:obj.castShadow});
});
fs.writeFileSync(__dirname+'/scene.json',JSON.stringify(output));console.log('Exported',output.length,'meshes');
