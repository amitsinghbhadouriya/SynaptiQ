import{r as _,j as C}from"./index-CI0WOZ92.js";/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const re=o=>o==null?void 0:o.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase();/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function ie(o,e,i=[]){if(e==null)throw new Error("[lucide]: iconNode is required when icon name is used");return{name:re(o),size:24,node:e,...i.length>0?{aliases:i}:{}}}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const le=o=>{let e="",i=!1;for(const a of o){if(a==="-"||a==="_"||a<=" "){i=e.length>0;continue}e.length===0?e+=a.toLowerCase():e+=i?a.toUpperCase():a,i=!1}return e};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ce=o=>{const e=le(o);return e.charAt(0).toUpperCase()+e.slice(1)};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const vt=(...o)=>o.filter((e,i,a)=>!!e&&e.trim()!==""&&a.indexOf(e)===i).join(" ").trim();/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Q={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function mt(o){return o!=null}function he(o,e={}){var Z,X;const i=e.attributeNames??{},a=M=>i[M]??M,l=o.size??o.width??Q.width,b=o.size??o.height??Q.height,d=((Z=o.aliases)==null?void 0:Z.filter(M=>typeof M=="string"&&M.trim()!=="").map(M=>`lucide-${M}`))??[],w=[...o.name?[`lucide-${o.name}`]:[],...d],S=((X=e.className)==null?void 0:X.split(" ").filter(Boolean))??[],P=e.includeDefaultClasses===!1?vt(...S):vt("lucide",...w,...S),G=e.absoluteStrokeWidth?Number(e.strokeWidth??Q["stroke-width"])*Number(o.size??o.width??Q.width)/Number(e.size??e.width??Q.width):e.strokeWidth??Q["stroke-width"];return["svg",{...Object.entries(Q).reduce((M,[H,q])=>(M[a(H)]=q,M),{}),..."color"in e&&e.color&&{[a("stroke")]:e.color},..."size"in e&&mt(e.size)&&{[a("width")]:e.size,[a("height")]:e.size},..."width"in e&&mt(e.width)&&{[a("width")]:e.width},..."height"in e&&mt(e.height)&&{[a("height")]:e.height},[a("stroke-width")]:G,...P&&{[a("class")]:P},[a("viewBox")]:`0 0 ${l} ${b}`,...e.hasA11yProp===!1?{[a("aria-hidden")]:"true"}:{},..."attributes"in e&&e.attributes},o.node.map(M=>{const[H,q,J]=M,tt=e.nonScalingStroke?{[a("vector-effect")]:"non-scaling-stroke",...q}:q;return J?[H,tt,J]:[H,tt]})]}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function de(o,e={}){return he(o,{...e,attributeNames:{...e.attributeNames,class:"className","stroke-width":"strokeWidth","stroke-linecap":"strokeLinecap","stroke-linejoin":"strokeLinejoin","vector-effect":"vectorEffect"}})}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const fe=o=>{for(const e in o)if(e.startsWith("aria-")||e==="role"||e==="title")return!0;return!1},ue=_.createContext({}),ge=()=>_.useContext(ue),xe=_.forwardRef(({color:o,size:e,width:i,height:a,strokeWidth:l,absoluteStrokeWidth:b,nonScalingStroke:d,className:w="",children:S,iconNode:P=[],icon:G={node:P,aliases:[],size:24},...I},Z)=>{const{size:X=24,strokeWidth:M=2,absoluteStrokeWidth:H=!1,nonScalingStroke:q=!1,color:J="currentColor",className:tt=""}=ge()??{},xt=!!S||fe(I),[rt,it,lt=[]]=de(G,{color:o??J,width:i??e??X,height:a??e??X,strokeWidth:l??M,absoluteStrokeWidth:b??H,nonScalingStroke:d??q,className:vt(tt,w),hasA11yProp:xt,attributes:I});return _.createElement(rt,{ref:Z,...it},[...lt.map(([O,et])=>_.createElement(O,et)),...Array.isArray(S)?S:[S]])});/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function A(o,e=[],i=[]){const a=typeof o=="string"?ie(o,e,i):o,l=_.forwardRef(({className:b,...d},w)=>_.createElement(xe,{ref:w,icon:a,className:b,...d}));return a.name&&(l.displayName=ce(a.name)),l}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ht={name:"activity",size:24,node:[["path",{d:"M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2",key:"169zse"}]]};Ht.node;const me=A(Ht);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Vt={name:"chart-column",size:24,node:[["path",{d:"M3 3v16a2 2 0 0 0 2 2h16",key:"c24i48"}],["path",{d:"M18 17V9",key:"2bz60n"}],["path",{d:"M13 17V5",key:"1frdt8"}],["path",{d:"M8 17v-3",key:"17ska0"}]],aliases:["bar-chart-3"]};Vt.node;const Me=A(Vt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Xt={name:"check",size:24,node:[["path",{d:"M20 6 9 17l-5-5",key:"1gmf2c"}]]};Xt.node;const ve=A(Xt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ot={name:"circle-alert",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["line",{x1:"12",x2:"12",y1:"8",y2:"12",key:"1pkeuh"}],["line",{x1:"12",x2:"12.01",y1:"16",y2:"16",key:"4dfq90"}]],aliases:["alert-circle"]};Ot.node;const be=A(Ot);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Yt={name:"circle-check",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m16 9-5.5 5.5L8 12",key:"xofnsj"}]],aliases:["check-circle-2"]};Yt.node;const we=A(Yt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Qt={name:"database",size:24,node:[["ellipse",{cx:"12",cy:"5",rx:"9",ry:"3",key:"msslwz"}],["path",{d:"M3 5V19A9 3 0 0 0 21 19V5",key:"1wlel7"}],["path",{d:"M3 12A9 3 0 0 0 21 12",key:"mv7ke4"}]]};Qt.node;const Ce=A(Qt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ut={name:"info",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"M12 16v-4",key:"1dtifu"}],["path",{d:"M12 8h.01",key:"e9boi3"}]]};Ut.node;const Se=A(Ut);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Kt={name:"layers",size:24,node:[["path",{d:"M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z",key:"zw3jo"}],["path",{d:"M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12",key:"1wduqc"}],["path",{d:"M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17",key:"kqbvx6"}]],aliases:["layers-3"]};Kt.node;const ze=A(Kt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Zt={name:"lightbulb",size:24,node:[["path",{d:"M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5",key:"1gvzjb"}],["path",{d:"M9 18h6",key:"x1upvd"}],["path",{d:"M10 22h4",key:"ceow96"}]]};Zt.node;const Le=A(Zt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Jt={name:"play",size:24,node:[["path",{d:"M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z",key:"10ikf1"}]]};Jt.node;const Ee=A(Jt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const te={name:"search",size:24,node:[["path",{d:"m21 21-4.34-4.34",key:"14j7rj"}],["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}]]};te.node;const $e=A(te);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ee={name:"sparkles",size:24,node:[["path",{d:"M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z",key:"1s2grr"}],["path",{d:"M20 2v4",key:"1rf3ol"}],["path",{d:"M22 4h-4",key:"gwowj6"}],["circle",{cx:"4",cy:"20",r:"2",key:"6kqj1y"}]],aliases:["stars"]};ee.node;const je=A(ee);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const oe={name:"x",size:24,node:[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]};oe.node;const _e=A(oe);function Ae({size:o=28,ink:e="currentColor",accent:i="#3987e5",className:a=""}){return C.jsxs("svg",{className:`logomark-q ${a}`,width:o,height:o,viewBox:"0 0 100 100","aria-hidden":"true",focusable:"false",children:[C.jsx("defs",{children:C.jsxs("linearGradient",{id:"sqQGrad",x1:"0%",y1:"0%",x2:"100%",y2:"100%",children:[C.jsx("stop",{offset:"0%",stopColor:"#00f5ff"}),C.jsx("stop",{offset:"35%",stopColor:"#38bdf8"}),C.jsx("stop",{offset:"70%",stopColor:"#8b5cf6"}),C.jsx("stop",{offset:"100%",stopColor:"#ec4899"})]})}),C.jsxs("g",{fill:"none",stroke:e,strokeLinecap:"round",children:[C.jsx("circle",{cx:"44",cy:"44",r:"27",strokeWidth:"9"}),C.jsx("path",{d:"M63 63 78 78",stroke:"url(#sqQGrad)",strokeWidth:"9"}),C.jsx("path",{d:"M44 44V28M44 44l-13.8 8M44 44l13.8 8",strokeWidth:"4.5",opacity:"0.55"})]}),C.jsx("circle",{cx:"44",cy:"44",r:"7",fill:i}),C.jsx("circle",{cx:"83",cy:"83",r:"9",fill:"url(#sqQGrad)"})]})}const qt={dark:{surface:"#0c0c0f",text:"#fafafa",track:"rgba(255, 255, 255, 0.1)",light:"#ffffff"},light:{surface:"#ffffff",text:"#18181b",track:"rgba(24, 24, 27, 0.12)",light:"#18181b"}},pe=["lap","brighten","reveal","none"],U=48,Mt=.9,gt=Math.PI*2,F=[255,255,255],K=(o,e,i)=>Math.min(i,Math.max(e,o)),bt=(o,e)=>(o%e+e)%e,Tt=o=>o<.5?4*o*o*o:1-(2-2*o)**3/2,ut=(o,e,i)=>[o[0]+(e[0]-o[0])*i,o[1]+(e[1]-o[1])*i,o[2]+(e[2]-o[2])*i],m=(o,e)=>`rgba(${Math.round(o[0])}, ${Math.round(o[1])}, ${Math.round(o[2])}, ${K(e,0,1).toFixed(3)})`;let nt=null;const Ft=o=>{var a;if(nt=nt??document.createElement("canvas").getContext("2d"),!nt)return F;nt.fillStyle="#000000",nt.fillStyle=o;const e=String(nt.fillStyle);if(e.startsWith("#")){const l=parseInt(e.slice(1,7),16);return[l>>16&255,l>>8&255,l&255]}const i=((a=e.match(/[\d.]+/g))==null?void 0:a.map(Number))??F;return[i[0],i[1],i[2]]},ke=(o,e,i)=>{const a=Math.max(0,Math.min(i,o/2,e/2)),l=Math.PI*a/2,b=Math.max(0,o-2*a),d=Math.max(0,e-2*a),w=[{length:b,x:a,y:0,dx:1,dy:0,angle:null},{length:l,x:o-a,y:a,dx:0,dy:0,angle:-Math.PI/2},{length:d,x:o,y:a,dx:0,dy:1,angle:null},{length:l,x:o-a,y:e-a,dx:0,dy:0,angle:0},{length:b,x:o-a,y:e,dx:-1,dy:0,angle:null},{length:l,x:a,y:e-a,dx:0,dy:0,angle:Math.PI/2},{length:d,x:0,y:e-a,dx:0,dy:-1,angle:null},{length:l,x:a,y:a,dx:0,dy:0,angle:Math.PI}];return{r:a,segments:w,total:Math.max(1,w.reduce((S,P)=>S+P.length,0))}},at=(o,e,i)=>{let a=bt(e,o.total);for(const l of o.segments){if(l.length>0&&a<=l.length){if(l.angle===null)i.x=l.x+l.dx*a,i.y=l.y+l.dy*a,i.nx=l.dy,i.ny=-l.dx;else{const b=l.angle+a/o.r;i.nx=Math.cos(b),i.ny=Math.sin(b),i.x=l.x+i.nx*o.r,i.y=l.y+i.ny*o.r}return i}a-=l.length}return i},Gt=(o,e,i)=>{let a=1/0,l=0,b=0;return o.segments.forEach(d=>{if(d.length>0){let w=0,S=0,P=0;if(d.angle===null)w=K((e-d.x)*d.dx+(i-d.y)*d.dy,0,d.length),S=d.x+d.dx*w,P=d.y+d.dy*w;else{let I=bt(Math.atan2(i-d.y,e-d.x)-d.angle,gt);I>Math.PI/2&&(I=I>Math.PI*1.25?0:Math.PI/2),w=I*o.r,S=d.x+Math.cos(d.angle+I)*o.r,P=d.y+Math.sin(d.angle+I)*o.r}const G=(e-S)**2+(i-P)**2;G<a&&(a=G,l=b+w)}b+=d.length}),l},Pe=({as:o="button",children:e,className:i="",style:a,color:l,trailColor:b,duration:d=4,thickness:w=1,radius:S=12,trailLength:P=.3,stars:G=1,glow:I=.6,sparkle:Z=!1,direction:X="clockwise",hover:M="lap",clickPulse:H=!0,theme:q="dark",backgroundColor:J,textColor:tt,borderColor:xt,...rt})=>{const it=_.useRef(null),lt=_.useRef(null),O=_.useRef(null),et=qt[q]??qt.dark,wt=l??et.light,ct={light:q==="light",color:wt,trailColor:b??wt,duration:Math.max(.3,d),thickness:Math.max(.5,w),radius:Math.max(0,S),trailLength:K(P,0,1),stars:K(Math.round(G),1,6),glow:K(I,0,1),sparkle:Z,direction:X==="counterclockwise"?-1:1,hover:pe.includes(M)?M:"lap",clickPulse:H},ot=_.useRef(ct);return ot.current=ct,_.useEffect(()=>{var Dt;const g=it.current,N=lt.current,c=N==null?void 0:N.getContext("2d");if(!g||!N||!c)return;const ht=((Dt=window.matchMedia)==null?void 0:Dt.call(window,"(prefers-reduced-motion: reduce)").matches)??!1,x={x:0,y:0,nx:0,ny:-1},t={width:0,height:0,dpr:1,phase:0,velocity:0,motion:0,lap:-1,time:0,reveal:0,boost:0,flash:0,emit:0,hovered:!1,focused:!1,pointerX:0,pointerY:0,visible:!0},T=[],Y=[],B={key:"",head:F,tail:F};let st=0,pt=performance.now(),kt=!0;const Ct=()=>{t.width=g.offsetWidth,t.height=g.offsetHeight,t.dpr=Math.min(window.devicePixelRatio||1,2),N.width=Math.max(1,Math.round((t.width+U*2)*t.dpr)),N.height=Math.max(1,Math.round((t.height+U*2)*t.dpr)),N.style.width=`${t.width+U*2}px`,N.style.height=`${t.height+U*2}px`,N.style.top=`${-U}px`,N.style.left=`${-U}px`,V()},St=r=>{const s=g.getBoundingClientRect(),n=s.width?t.width/s.width:1,f=s.height?t.height/s.height:1;return[(r.clientX-s.left)*n,(r.clientY-s.top)*f]},yt=r=>ke(Math.max(1,t.width-r.thickness),Math.max(1,t.height-r.thickness),r.radius-r.thickness/2),dt=(r,s,n,f,y,h)=>{c.lineWidth=y,c.strokeStyle=h,c.beginPath(),c.moveTo(r,s),c.lineTo(n,f),c.stroke()},ft=(r,s,n,f,y,h,z=!0)=>{if(f<.5||h<=0)return;const E=K(Math.ceil(f/2),2,90);at(s,n,x);let W=x.x,j=x.y;for(let k=1;k<=E;k++){at(s,n-y*f*(k/E),x);const p=1-(k-.5)/E,D=p*p*h;let $=ut(B.tail,B.head,p);r.light||($=ut($,F,p**6*.65)),c.lineCap=z&&k===1?"round":"butt",dt(W,j,x.x,x.y,2+6*r.glow,m($,D*(r.light?.1:.2)*r.glow)),dt(W,j,x.x,x.y,r.thickness,m($,D)),W=x.x,j=x.y}},zt=(r,s,n,f,y)=>{if(f<=0)return;const h=B.head,z=(12+40*r.glow)*(r.light?.6:1),E=c.createRadialGradient(s,n,0,s,n,z),W=(r.light?.08:.4)*r.glow*f;if(E.addColorStop(0,m(h,W)),E.addColorStop(.2,m(h,W*.4)),E.addColorStop(.5,m(h,W*.1)),E.addColorStop(1,m(h,0)),c.fillStyle=E,c.fillRect(s-z,n-z,z*2,z*2),!r.sparkle)return;const j=(1+r.thickness*.6)*(r.light?.85:1),k=c.createRadialGradient(s,n,0,s,n,j*2.2);k.addColorStop(0,m(r.light?h:F,f)),k.addColorStop(r.light?.3:.4,m(r.light?h:ut(h,F,.5),f*.9)),k.addColorStop(r.light?.55:1,m(h,r.light?f*.12:0)),k.addColorStop(1,m(h,0)),c.fillStyle=k,c.beginPath(),c.arc(s,n,j*2.2,0,gt),c.fill();const p=(3+4*r.glow+r.thickness*1.5)*y,D=r.light?h:F,$=c.createLinearGradient(s-p,n,s+p,n);$.addColorStop(0,m(h,0)),$.addColorStop(.5,m(D,f*.95)),$.addColorStop(1,m(h,0)),dt(s-p,n,s+p,n,r.light?.75:1,$);const u=c.createLinearGradient(s,n-p,s,n+p);u.addColorStop(0,m(h,0)),u.addColorStop(.5,m(D,f*.95)),u.addColorStop(1,m(h,0)),dt(s,n-p,s,n+p,r.light?.75:1,u)},ne=(r,s,n,f,y)=>{if(Y.length>48)return;const h=3+Math.random()*10,z=(Math.random()-.5)*8;Y.push({x:r+n*(Math.random()*3-1),y:s+f*(Math.random()*3-1),vx:n*h-f*z-y*-f*.04,vy:f*h+n*z-y*n*.04,age:0,life:.35+Math.random()*.5,size:.45+Math.random()*.7,seed:Math.random()*gt})},se=(r,s)=>{const n=t.boost>.001?{...r,glow:Math.min(1.5,r.glow+.4*t.boost)}:r;if(c.setTransform(1,0,0,1,0,0),c.clearRect(0,0,N.width,N.height),t.width<2||t.height<2)return;const f=(U+n.thickness/2)*t.dpr;c.setTransform(t.dpr,0,0,t.dpr,f,f),c.globalCompositeOperation=n.light?"source-over":"lighter",c.lineCap="butt";const y=s.total,h=y/n.stars,z=Math.abs(t.motion),E=t.motion>=0?1:-1,W=n.trailLength*n.duration,j=Math.min(z*W,h*.92,y*.6),k=t.reveal*(1+.4*t.boost+.6*t.flash),p=t.flash*(n.light?.18:.32)+t.boost*t.reveal*(n.light?.07:.12);p>.005&&(c.lineWidth=n.thickness+2*n.glow,c.strokeStyle=m(B.head,p),c.beginPath(),c.roundRect(0,0,Math.max(1,t.width-n.thickness),Math.max(1,t.height-n.thickness),Math.max(0,s.r)),c.stroke());const D=K(1-z/Math.max(1,y/n.duration*.6),0,1)*Math.min(1,k),$=(10+14*n.glow+n.thickness*2)*D;for(let u=0;u<n.stars;u++){const R=t.phase+u*h;ft(n,s,R,j,E,Math.min(1,k)),D>.01&&(ft(n,s,R,$,1,D,!1),ft(n,s,R,$,-1,D,!1))}T.forEach(u=>{const v=(1-u.age/.65)**2,L=y/2*(1-(1-Math.min(1,u.age/.5))**2),ae=Math.min(L,y*.16);[1,-1].forEach(Rt=>{const Bt=u.origin+Rt*L;ft(n,s,Bt,ae,Rt,v),at(s,Bt,x),zt(n,x.x,x.y,v*.8,.8)})});for(let u=0;u<n.stars;u++){at(s,t.phase+u*h,x);const R=.82+.18*Math.sin(t.time*6.1+u*2.3)*Math.sin(t.time*2.7+u);zt(n,x.x,x.y,Math.min(1.3,k),R)}Y.forEach(u=>{const R=1-u.age/u.life,v=.45+.55*Math.sin(t.time*20+u.seed),L=R*v*t.reveal*(n.light?.35:.9);L<=.01||(c.fillStyle=m(n.light?B.head:ut(B.tail,F,.6),L),c.beginPath(),c.arc(u.x,u.y,u.size*(.6+.4*R),0,gt),c.fill())})},Lt=r=>{if(st=0,!kt)return;const s=ot.current,n=Math.min(.05,Math.max(.001,(r-pt)/1e3));pt=r,t.time+=n;const f=`${s.color}|${s.trailColor}`;f!==B.key&&(B.key=f,B.head=Ft(s.color),B.tail=Ft(s.trailColor));const y=yt(s),h=y.total,z=h/s.stars,E=t.hovered||t.focused,W=ht?0:s.direction*h/s.duration,j=s.hover==="reveal"&&!E?0:1;t.reveal+=(j-t.reveal)*(1-Math.exp(-n/(j>t.reveal?.16:.45)));const k=s.hover==="brighten"&&E?1:0;t.boost+=(k-t.boost)*(1-Math.exp(-n/(k>t.boost?.18:.5))),t.flash*=Math.exp(-n/.22),t.velocity+=(W-t.velocity)*(1-Math.exp(-n/.45));let p=0;if(t.lap>=0){const v=Tt(Math.min(1,t.lap/Mt));t.lap+=n,p=(Tt(Math.min(1,t.lap/Mt))-v)*h*s.direction,t.lap>=Mt&&(t.lap=-1)}t.motion=t.velocity+p/n,t.phase=bt(t.phase+t.velocity*n+p,h);const D=Math.abs(t.motion)/Math.max(1,Math.abs(h/s.duration));if(s.sparkle&&!ht&&t.reveal>.05)for(t.emit+=n*(2+6*Math.min(2,D))*s.stars;t.emit>1;)t.emit-=1,at(y,t.phase+Math.floor(Math.random()*s.stars)*z,x),ne(x.x,x.y,x.nx,x.ny,t.motion);for(let v=Y.length-1;v>=0;v--){const L=Y[v];L.age+=n,L.x+=L.vx*n,L.y+=L.vy*n,L.vx*=Math.exp(-n*2.2),L.vy*=Math.exp(-n*2.2),L.age>=L.life&&Y.splice(v,1)}for(let v=T.length-1;v>=0;v--)T[v].age+=n,T[v].age>=.65&&T.splice(v,1);se(s,y);const $=Math.abs(j-t.reveal)>.002||Math.abs(k-t.boost)>.002||t.flash>.01||T.length>0||Y.length>0,u=Math.abs(t.motion)>.05||W!==0||t.lap>=0,R=t.reveal>.002||j>0;t.visible&&($||u&&R||t.hovered)&&(st=requestAnimationFrame(Lt))},V=()=>{st||!kt||!t.visible||(pt=performance.now(),st=requestAnimationFrame(Lt))};O.current=V;const Et=r=>{const s=ot.current;[t.pointerX,t.pointerY]=St(r),t.hovered=!0,s.hover==="reveal"&&t.reveal<.15&&(t.phase=Gt(yt(s),t.pointerX-s.thickness/2,t.pointerY-s.thickness/2),t.velocity=0),s.hover==="lap"&&t.lap<0&&!ht&&(t.lap=0),V()},$t=()=>{t.hovered=!1,V()},jt=r=>{ot.current.clickPulse&&(T.push({origin:r,age:0}),T.length>4&&T.shift(),t.flash=1,V())},_t=r=>{if(r.button!==0&&r.pointerType==="mouse")return;const s=ot.current,[n,f]=St(r);jt(Gt(yt(s),n-s.thickness/2,f-s.thickness/2))},At=r=>{r.detail===0&&jt(t.phase)},Pt=()=>{t.focused=g.matches(":focus-visible"),t.focused&&ot.current.hover==="lap"&&t.lap<0&&!ht&&(t.lap=0),V()},It=()=>{t.focused=!1,V()},Nt=new ResizeObserver(Ct);Nt.observe(g);const Wt=new IntersectionObserver(r=>{t.visible=r.some(s=>s.isIntersecting),t.visible&&V()});return Wt.observe(g),g.addEventListener("pointerenter",Et),g.addEventListener("pointerleave",$t),g.addEventListener("pointerdown",_t),g.addEventListener("click",At),g.addEventListener("focus",Pt),g.addEventListener("blur",It),Ct(),()=>{kt=!1,O.current=null,cancelAnimationFrame(st),Nt.disconnect(),Wt.disconnect(),g.removeEventListener("pointerenter",Et),g.removeEventListener("pointerleave",$t),g.removeEventListener("pointerdown",_t),g.removeEventListener("click",At),g.removeEventListener("focus",Pt),g.removeEventListener("blur",It)}},[]),_.useEffect(()=>{var g;(g=O.current)==null||g.call(O)}),C.jsxs(o,{ref:it,className:`star-border${i?` ${i}`:""}`,style:{"--star-border-radius":`${ct.radius}px`,"--star-border-thickness":`${ct.thickness}px`,"--star-border-surface":J??et.surface,"--star-border-text":tt??et.text,"--star-border-track":xt??et.track,...a},...o==="button"&&rt.type===void 0?{type:"button"}:null,...rt,children:[C.jsx("canvas",{ref:lt,className:"star-border__light","aria-hidden":"true"}),C.jsx("span",{className:"star-border__content",children:e})]})};export{me as A,ve as C,Ce as D,Se as I,Ae as L,Ee as P,Pe as S,_e as X,je as a,ze as b,A as c,we as d,be as e,Le as f,Me as g,$e as h};
