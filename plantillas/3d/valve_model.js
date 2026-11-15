// builds an industrial control valve assembly; returns {group, parts:{id:object3D}, animate(t)}
function buildValve(THREE){
 const G=new THREE.Group();
 const steel=new THREE.MeshStandardMaterial({color:'#AEB6C0',metalness:.9,roughness:.28,emissive:'#000'});
 const dark=new THREE.MeshStandardMaterial({color:'#3B434D',metalness:.75,roughness:.4,emissive:'#000'});
 const orange=new THREE.MeshStandardMaterial({color:'#FF8A3D',metalness:.35,roughness:.45,emissive:'#000'});
 const blue=new THREE.MeshStandardMaterial({color:'#2E6E9E',metalness:.4,roughness:.45,emissive:'#000'});
 const C=(r1,r2,h,m,seg=48)=>new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,seg),m);
 // pipeline
 const pipe=new THREE.Group();
 [-1,1].forEach(s=>{const p=C(.42,.42,3.2,dark.clone());p.rotation.z=Math.PI/2;p.position.x=s*2.35;pipe.add(p);
   const f=C(.78,.78,.18,steel.clone());f.rotation.z=Math.PI/2;f.position.x=s*.82;pipe.add(f);
   for(let k=0;k<8;k++){const a=k/8*Math.PI*2,b=C(.06,.06,.32,steel.clone(),12);b.rotation.z=Math.PI/2;b.position.set(s*.82,Math.cos(a)*.64,Math.sin(a)*.64);pipe.add(b)}});
 G.add(pipe);
 // valve body
 const body=new THREE.Group();
 const bb=new THREE.Mesh(new THREE.SphereGeometry(.82,48,32),blue.clone());bb.scale.set(1,.9,.9);body.add(bb);
 [-1,1].forEach(s=>{const n=C(.5,.6,.5,blue.clone());n.rotation.z=Math.PI/2;n.position.x=s*.55;body.add(n)});
 const bon=C(.42,.55,.6,blue.clone());bon.position.y=.85;body.add(bon);
 G.add(body);
 // yoke + stem
 const yoke=new THREE.Group();
 [-1,1].forEach(s=>{const p=C(.07,.07,1.1,steel.clone(),16);p.position.set(s*.32,1.7,0);yoke.add(p)});
 const stem=C(.05,.05,1.2,steel.clone(),16);stem.position.y=1.6;yoke.add(stem);
 const plate=C(.45,.45,.08,steel.clone());plate.position.y=2.25;yoke.add(plate);
 G.add(yoke);
 // actuator (diaphragm)
 const act=new THREE.Group();
 const low=C(1.25,1.05,.35,orange.clone(),64);low.position.y=2.47;act.add(low);
 const up=C(1.05,1.25,.35,orange.clone(),64);up.position.y=2.82;act.add(up);
 const rim=new THREE.Mesh(new THREE.TorusGeometry(1.27,.05,12,80),steel.clone());rim.rotation.x=Math.PI/2;rim.position.y=2.65;act.add(rim);
 const cap=C(.25,.3,.25,steel.clone());cap.position.y=3.1;act.add(cap);
 G.add(act);
 // positioner
 const pos=new THREE.Group();
 const box=new THREE.Mesh(new THREE.BoxGeometry(.7,.55,.4),new THREE.MeshStandardMaterial({color:'#E8ECEF',metalness:.2,roughness:.5,emissive:'#000'}));box.position.set(.75,1.7,.42);pos.add(box);
 const scr=new THREE.Mesh(new THREE.PlaneGeometry(.42,.18),new THREE.MeshBasicMaterial({color:'#22E6FF'}));scr.position.set(.75,1.78,.625);pos.add(scr);
 const tube=C(.03,.03,.9,steel.clone(),8);tube.position.set(.75,2.2,.42);pos.add(tube);
 G.add(pos);
 // pressure gauge on pipe
 const gauge=new THREE.Group();
 const cv=document.createElement('canvas');cv.width=cv.height=256;const g=cv.getContext('2d');
 function dial(v){g.fillStyle='#fff';g.fillRect(0,0,256,256);g.strokeStyle='#222';g.lineWidth=4;
  for(let i=0;i<=10;i++){const a=Math.PI*.75+i/10*Math.PI*1.5;g.beginPath();g.moveTo(128+Math.cos(a)*100,128+Math.sin(a)*100);g.lineTo(128+Math.cos(a)*(i%5?88:78),128+Math.sin(a)*(i%5?88:78));g.stroke()}
  g.strokeStyle='#d33';g.lineWidth=10;g.beginPath();g.arc(128,128,94,Math.PI*1.95,Math.PI*2.25);g.stroke();
  g.fillStyle='#222';g.font='bold 26px sans-serif';g.textAlign='center';g.fillText('bar',128,190);
  const a=Math.PI*.75+v*Math.PI*1.5;g.strokeStyle='#111';g.lineWidth=7;g.beginPath();g.moveTo(128,128);g.lineTo(128+Math.cos(a)*84,128+Math.sin(a)*84);g.stroke();g.fillStyle='#111';g.beginPath();g.arc(128,128,12,0,7);g.fill()}
 dial(.4);const tex=new THREE.CanvasTexture(cv);tex.colorSpace=THREE.SRGBColorSpace;
 const gs=C(.06,.06,.6,steel.clone(),12);gs.position.set(-2.3,.7,0);gauge.add(gs);
 const gb=C(.48,.48,.22,steel.clone(),48);gb.rotation.x=Math.PI/2;gb.position.set(-2.3,1.35,0);gauge.add(gb);
 const face=new THREE.Mesh(new THREE.CircleGeometry(.42,48),new THREE.MeshBasicMaterial({map:tex}));face.position.set(-2.3,1.35,.115);gauge.add(face);
 G.add(gauge);
 // flow particles inside pipe (visible through nothing -> put just outside as glowing ring markers along pipe top)
 const flow=new THREE.Group();const fm=new THREE.MeshBasicMaterial({color:'#22E6FF',transparent:true,opacity:.9});
 for(let i=0;i<14;i++){const s=new THREE.Mesh(new THREE.SphereGeometry(.05,12,8),fm);flow.add(s)}
 G.add(flow);
 const parts={tuberia:pipe,cuerpo:body,actuador:act,posicionador:pos,manometro:gauge};
 function animate(t){stem.position.y=1.6+Math.sin(t*1.2)*.05;plate.position.y=2.25+Math.sin(t*1.2)*.05;
  dial(.42+.12*Math.sin(t*.9));tex.needsUpdate=true;scr.material.color.setHSL(.52,1,.45+.1*Math.sin(t*4));
  flow.children.forEach((s,i)=>{const u=((t*.35+i/14)%1);s.position.set(-3.9+u*7.8,.46,0);s.material.opacity=.9})}
 return {group:G,parts,animate};
}
