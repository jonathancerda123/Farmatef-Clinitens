import {boxCorners, fitProjection, slabOf, solidSvg, iso, translateAlong} from '../vendor/anatomy/iso-kit.js';

export const tipos={sliding:['Estante deslizante',140,190,60,7,3],drawers:['Cajonera',120,180,50,3,2],table:['Mesa simple',140,75,60,1,1],board:['Pizarra',180,100,5,1,1],counter:['Mesón de trabajo',560,90,70,1,1],studentTable:['Mesa de alumnos',180,75,90,1,1],entrance:['Entrada',160,200,90,1,1]};
export const escapeHTML=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
export function huella(m){const d=m.fondo_cm+(m.tipo==='studentTable'?90:0);return [90,270].includes(m.orientacion)?[d,m.ancho_cm]:[m.ancho_cm,d]}
export function dentro(m,sala){const [w,d]=huella(m);return m.x_cm>=0&&m.y_cm>=0&&m.x_cm+w<=sala.ancho_cm&&m.y_cm+d<=sala.largo_cm}
export function superpuestos(a,b){const [w,d]=huella(a),[ww,dd]=huella(b);return a.x_cm<b.x_cm+ww&&a.x_cm+w>b.x_cm&&a.y_cm<b.y_cm+dd&&a.y_cm+d>b.y_cm}
export function claves(m){if(m.tipo==='sliding')return ['A','B','F1','F2','F3'].flatMap(c=>Array.from({length:m.filas},(_,i)=>`${c}-${i+1}`));if(m.tipo==='drawers')return Array.from({length:m.filas*m.columnas},(_,i)=>'C'+(i+1));return []}
export function nombreClave(key){if(!key)return 'Selecciona un compartimento';if(key.startsWith('C'))return 'Cajón '+key.slice(1);const [col,row]=key.split('-');return (col.startsWith('F')?'Fondo · columna '+col.slice(1):'Móvil '+col)+' · fila '+row}
export function validarMueble(m,sala){const min=m.tipo==='studentTable'?150:m.tipo==='counter'?180:60;return Object.hasOwn(tipos,m.tipo)&&typeof m.nombre==='string'&&m.nombre.trim().length>0&&m.nombre.trim().length<=80&&['ancho_cm','alto_cm','fondo_cm','x_cm','y_cm','orientacion','filas','columnas'].every(k=>Number.isInteger(m[k]))&&m.ancho_cm>=min&&m.ancho_cm<=720&&m.alto_cm>=50&&m.alto_cm<=220&&m.fondo_cm>=(m.tipo==='board'?5:35)&&m.fondo_cm<=(m.tipo==='board'?15:120)&&[0,90,180,270].includes(m.orientacion)&&m.filas>=1&&m.filas<=12&&m.columnas>=1&&m.columnas<=8&&(m.tipo!=='sliding'||m.columnas===3&&m.alto_cm>=20+6*m.filas)&&(m.tipo!=='drawers'||m.alto_cm>=16+6*m.filas&&m.ancho_cm>=12*m.columnas)&&(claves(m).length>0||m.filas===1&&m.columnas===1)&&dentro(m,sala)}

export function figura(m,key){
 if(m.tipo==='entrance')return {svg:'',P:null,positions:[]};
 const w=m.ancho_cm,h=m.alto_cm,d=m.fondo_cm,student=m.tipo==='studentTable';
 const P=fitProjection(boxCorners({x:-3,y:student?-48:0,w:w+6,d:d+(student?100:26)},0,h+(m.tipo==='counter'?46:26)),460,420,{pad:24,azimuth:86,elevation:9});
 const S=(plan,z,height,cls='')=>solidSvg(slabOf(plan,z,height,P,3,.3),{tone:'lo',crease:'faint',className:cls});
 const rect=(x,y,ww,dd,z,hh,cls='')=>S({x,y,w:ww,d:dd,r:.4},z,hh,cls);
 const link=(clave,body)=>`<a href="#sala-contenido-titulo" class="compartimento${clave===key?' selected':''}" data-key="${clave}" aria-label="${escapeHTML(nombreClave(clave))}">${body}</a>`;
 function table(){let body='';for(const x of [2,w-7])for(const y of [2,d-7])body+=rect(x,y,5,5,0,h-4);return body+rect(0,0,w,d,h-4,4)}
 function chair(x,y,rear){let body='';for(const xx of [x+2,x+32])for(const yy of [y+2,y+32])body+=rect(xx,yy,4,4,0,42,'equipment');return `<g data-chair="">${body+rect(x,y,38,38,42,4,'chair')+rect(x,rear?y:y+34,38,4,46,35,'chair')}</g>`}
 let body='',positions=[0,2];
 if(key?.startsWith('F'))positions=[0,1,2].filter(c=>c!==Number(key[1])-1);
 if(m.tipo==='table')body=table();
 else if(student){for(let i=0;i<3;i++)body+=chair((i+.5)*w/3-19,-45,true);body+=table();for(let i=0;i<3;i++)body+=chair((i+.5)*w/3-19,d+7,false)}
 else if(m.tipo==='board')body=rect(0,0,w,d,0,h)+rect(3,d,w-6,1,3,h-6)+rect(0,d,w,9,0,2);
 else if(m.tipo==='counter'){
  body=rect(0,0,w,d,6,h-10);for(let i=0;i<4;i++)body+=rect(i*w/4+2,d,w/4-4,2,8,h-15)+rect(i*w/4+w*.09,d+2,w*.07,2,h-18,2,'equipment');body+=rect(-2,-2,w+4,d+4,h-4,4);
  const x=w*.16,sy=d*.3;body+=rect(x+12,sy,25,16,h,2,'equipment')+rect(x+22,sy+4,5,5,h+2,9,'equipment')+rect(x,sy+5,50,4,h+11,30,'equipment')+rect(x+2,sy+9,46,.6,h+13,26,'screen')+rect(x,d*.7,50,12,h,2,'equipment');
  body+=rect(w*.53,d*.5,16,16,h,3,'equipment')+rect(w*.53+6,d*.5+5,5,5,h+3,10,'equipment')+rect(w*.53+2,d*.5+4,14,7,h+13,5,'equipment')+rect(w*.73,d*.4,27,25,h,16,'equipment')+rect(w*.73+5,d*.4+25,17,10,h+7,1);
 }else{
  body=rect(0,0,w,d,8,5)+rect(0,0,w,3,13,h-13)+rect(0,0,4,d,13,h-13)+rect(w-4,0,4,d,13,h-13)+rect(0,0,w,d,h,4);
  if(m.tipo==='drawers'){
   const cw=w/m.columnas,rh=(h-16)/m.filas;
   for(let row=m.filas-1;row>=0;row--)for(let col=0;col<m.columnas;col++){
    const x=col*cw+4,z=14+(m.filas-1-row)*rh;body+=link('C'+(row*m.columnas+col+1),rect(x,d-18,cw-8,15,z,2)+rect(x,d-5,cw-8,4,z,rh-3,'front')+rect(x+cw*.25,d-1,cw*.4,3,z+rh*.45,2,'equipment'));
   }
  }else{
   const cw=w/3,rh=(h-20)/m.filas;
   for(let col=0;col<3;col++){let part='';for(let row=m.filas-1;row>=0;row--){const z=14+(m.filas-1-row)*rh;part+=link(`F${col+1}-${row+1}`,rect(col*cw+4,d*.43,cw-8,2,z,rh-3,'rear')+rect(col*cw+4,d*.43,cw-8,d*.32,z,2,'rear'))}body+=`<g data-back="${col}">${part}</g>`}
   for(let i=0;i<2;i++){const letter=i===0?'A':'B';let part=rect(0,d-16,3,20,12,h-12)+rect(cw-3,d-16,3,20,12,h-12)+rect(0,d-16,cw,20,h,3);
    for(let row=m.filas-1;row>=0;row--){const z=14+(m.filas-1-row)*rh;part+=link(`${letter}-${row+1}`,rect(4,d+1,cw-8,2,z,rh-3,'front')+rect(4,d-14,cw-8,17,z,2,'front'))}
    const [tx,ty]=iso([cw/2,d+5,h+9],P);part+=`<a href="#sala-contenido-titulo" class="handle" data-move="${i}" aria-label="Deslizar módulo ${letter}: clic, arrastre o flechas">${rect(cw*.12,d+1,cw*.76,4,h+6,12,'handle')}<text x="${tx}" y="${ty}" text-anchor="middle">↔ ${letter}</text></a>`;
    body+=`<g data-column="${i}" transform="${translateAlong(P,[positions[i]*cw,0,0])}">${part}</g>`;
   }
  }
 }
 return {svg:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 420" role="group" aria-label="${escapeHTML(m.nombre)}, vista frontal">${body}</svg>`,P,positions};
}

export function montarMueble(host,mueble,key,onSelect){
 const built=figura(mueble,key),reduced=matchMedia('(prefers-reduced-motion: reduce)');host.innerHTML=built.svg;
 let positions=built.positions.slice(),values=positions.slice(),selected=key,frame=0,last=0,visible=true,drag=null;
 const columns=[...host.querySelectorAll('[data-column]')],links=[...host.querySelectorAll('[data-key]')];
 function lock(moving){for(const group of host.querySelectorAll('[data-back]')){const hidden=moving||positions.includes(Number(group.dataset.back));group.setAttribute('aria-hidden',String(hidden));group.inert=hidden;for(const a of group.querySelectorAll('[data-key]')){if(hidden)a.removeAttribute('href');else a.setAttribute('href','#sala-contenido-titulo');a.setAttribute('aria-disabled',String(hidden))}}}
 function draw(){columns.forEach((node,i)=>node.setAttribute('transform',translateAlong(built.P,[values[i]*mueble.ancho_cm/3,0,0])))}
 function cancel(){if(frame)cancelAnimationFrame(frame);frame=0;last=0}
 function tick(now){const dt=last?Math.min((now-last)/1000,1/30):1/60;last=now;let active=false;values=values.map((v,i)=>{v+=(positions[i]-v)*(1-Math.exp(-dt/.12));if(Math.abs(v-positions[i])<.001)return positions[i];active=true;return v});draw();if(active&&visible&&!document.hidden)frame=requestAnimationFrame(tick);else{frame=0;last=0;lock(false)}}
 function kick(){if(reduced.matches){cancel();values=positions.slice();draw();lock(false)}else if(!frame&&visible&&!document.hidden&&values.some((v,i)=>Math.abs(v-positions[i])>.001))frame=requestAnimationFrame(tick)}
 function select(clave){selected=clave;links.forEach(a=>a.classList.toggle('selected',a.dataset.key===clave));onSelect(clave)}
 const clamp=(i,v)=>i===0?Math.max(0,Math.min(positions[1]-1,v)):Math.max(positions[0]+1,Math.min(2,v));
 function move(i,value){positions[i]=Math.round(clamp(i,value));if(selected?.startsWith('F')&&positions.includes(Number(selected[1])-1))select(null);lock(true);kick();if(values.every((v,j)=>v===positions[j]))lock(false)}
 links.forEach(a=>a.addEventListener('click',e=>{e.preventDefault();if(a.getAttribute('aria-disabled')!=='true')select(a.dataset.key)}));
 for(const handle of host.querySelectorAll('[data-move]')){const i=Number(handle.dataset.move);let moved=false;
  handle.addEventListener('click',e=>{e.preventDefault();if(moved){moved=false;return}const next=clamp(i,positions[i]+1);move(i,next!==positions[i]?next:positions[i]-1)});
  handle.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();move(i,positions[i]+(e.key==='ArrowLeft'?-1:1))}});
  handle.addEventListener('pointerdown',e=>{if(e.button!==0||drag)return;cancel();moved=false;const origin=iso([0,0,0],built.P),end=iso([mueble.ancho_cm/3,0,0],built.P),ratio=host.querySelector('svg').getBoundingClientRect().width/460;drag={start:e.clientX,original:positions[i],pixels:(end[0]-origin[0])*ratio};handle.setPointerCapture(e.pointerId);lock(true)});
  handle.addEventListener('pointermove',e=>{if(!drag)return;if(Math.abs(e.clientX-drag.start)>4)moved=true;values[i]=clamp(i,drag.original+(e.clientX-drag.start)/drag.pixels);draw()});
  const end=cancelled=>{if(!drag)return;const value=cancelled?drag.original:Math.round(values[i]);drag=null;move(i,value)};handle.addEventListener('pointerup',()=>end(false));handle.addEventListener('pointercancel',()=>end(true));
 }
 const observer=new IntersectionObserver(entries=>{visible=entries.at(-1).isIntersecting;if(visible)kick();else cancel()},{rootMargin:'80px'});observer.observe(host);
 const visibility=()=>{if(document.hidden)cancel();else kick()};document.addEventListener('visibilitychange',visibility);reduced.addEventListener('change',kick);lock(false);
 return ()=>{cancel();observer.disconnect();document.removeEventListener('visibilitychange',visibility);reduced.removeEventListener('change',kick)};
}
