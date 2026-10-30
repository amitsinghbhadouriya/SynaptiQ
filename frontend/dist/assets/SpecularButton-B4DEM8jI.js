import{r as A,j as b}from"./index-DN7WU2A0.js";/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const He=e=>e==null?void 0:e.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase();/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function Ue(e,t,r=[]){if(t==null)throw new Error("[lucide]: iconNode is required when icon name is used");return{name:He(e),size:24,node:t,...r.length>0?{aliases:r}:{}}}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Xe=e=>{let t="",r=!1;for(const o of e){if(o==="-"||o==="_"||o<=" "){r=t.length>0;continue}t.length===0?t+=o.toLowerCase():t+=r?o.toUpperCase():o,r=!1}return t};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ye=e=>{const t=Xe(e);return t.charAt(0).toUpperCase()+t.slice(1)};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const le=(...e)=>e.filter((t,r,o)=>!!t&&t.trim()!==""&&o.indexOf(t)===r).join(" ").trim();/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const N={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function ae(e){return e!=null}function Oe(e,t={}){var w,u;const r=t.attributeNames??{},o=y=>r[y]??y,m=e.size??e.width??N.width,d=e.size??e.height??N.height,p=((w=e.aliases)==null?void 0:w.filter(y=>typeof y=="string"&&y.trim()!=="").map(y=>`lucide-${y}`))??[],h=[...e.name?[`lucide-${e.name}`]:[],...p],a=((u=t.className)==null?void 0:u.split(" ").filter(Boolean))??[],g=t.includeDefaultClasses===!1?le(...a):le("lucide",...h,...a),_=t.absoluteStrokeWidth?Number(t.strokeWidth??N["stroke-width"])*Number(e.size??e.width??N.width)/Number(t.size??t.width??N.width):t.strokeWidth??N["stroke-width"];return["svg",{...Object.entries(N).reduce((y,[q,j])=>(y[o(q)]=j,y),{}),..."color"in t&&t.color&&{[o("stroke")]:t.color},..."size"in t&&ae(t.size)&&{[o("width")]:t.size,[o("height")]:t.size},..."width"in t&&ae(t.width)&&{[o("width")]:t.width},..."height"in t&&ae(t.height)&&{[o("height")]:t.height},[o("stroke-width")]:_,...g&&{[o("class")]:g},[o("viewBox")]:`0 0 ${m} ${d}`,...t.hasA11yProp===!1?{[o("aria-hidden")]:"true"}:{},..."attributes"in t&&t.attributes},e.node.map(y=>{const[q,j,W]=y,D=t.nonScalingStroke?{[o("vector-effect")]:"non-scaling-stroke",...j}:j;return W?[q,D,W]:[q,D]})]}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function Qe(e,t={}){return Oe(e,{...t,attributeNames:{...t.attributeNames,class:"className","stroke-width":"strokeWidth","stroke-linecap":"strokeLinecap","stroke-linejoin":"strokeLinejoin","vector-effect":"vectorEffect"}})}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ke=e=>{for(const t in e)if(t.startsWith("aria-")||t==="role"||t==="title")return!0;return!1},Ze=A.createContext({}),Je=()=>A.useContext(Ze),et=A.forwardRef(({color:e,size:t,width:r,height:o,strokeWidth:m,absoluteStrokeWidth:d,nonScalingStroke:p,className:h="",children:a,iconNode:g=[],icon:_={node:g,aliases:[],size:24},...M},w)=>{const{size:u=24,strokeWidth:y=2,absoluteStrokeWidth:q=!1,nonScalingStroke:j=!1,color:W="currentColor",className:D=""}=Je()??{},U=!!a||Ke(M),[J,X,ee=[]]=Qe(_,{color:e??W,width:r??t??u,height:o??t??u,strokeWidth:m??y,absoluteStrokeWidth:d??q,nonScalingStroke:p??j,className:le(D,h),hasA11yProp:U,attributes:M});return A.createElement(J,{ref:w,...X},[...ee.map(([te,oe])=>A.createElement(te,oe)),...Array.isArray(a)?a:[a]])});/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function S(e,t=[],r=[]){const o=typeof e=="string"?Ue(e,t,r):e,m=A.forwardRef(({className:d,...p},h)=>A.createElement(et,{ref:h,icon:o,className:d,...p}));return o.name&&(m.displayName=Ye(o.name)),m}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Le={name:"activity",size:24,node:[["path",{d:"M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2",key:"169zse"}]]};Le.node;const ct=S(Le);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Pe={name:"chart-column",size:24,node:[["path",{d:"M3 3v16a2 2 0 0 0 2 2h16",key:"c24i48"}],["path",{d:"M18 17V9",key:"2bz60n"}],["path",{d:"M13 17V5",key:"1frdt8"}],["path",{d:"M8 17v-3",key:"17ska0"}]],aliases:["bar-chart-3"]};Pe.node;const lt=S(Pe);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Re={name:"check",size:24,node:[["path",{d:"M20 6 9 17l-5-5",key:"1gmf2c"}]]};Re.node;const ut=S(Re);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ze={name:"circle-alert",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["line",{x1:"12",x2:"12",y1:"8",y2:"12",key:"1pkeuh"}],["line",{x1:"12",x2:"12.01",y1:"16",y2:"16",key:"4dfq90"}]],aliases:["alert-circle"]};ze.node;const dt=S(ze);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const qe={name:"circle-check",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m16 9-5.5 5.5L8 12",key:"xofnsj"}]],aliases:["check-circle-2"]};qe.node;const ht=S(qe);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const je={name:"database",size:24,node:[["ellipse",{cx:"12",cy:"5",rx:"9",ry:"3",key:"msslwz"}],["path",{d:"M3 5V19A9 3 0 0 0 21 19V5",key:"1wlel7"}],["path",{d:"M3 12A9 3 0 0 0 21 12",key:"mv7ke4"}]]};je.node;const ft=S(je);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ie={name:"info",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"M12 16v-4",key:"1dtifu"}],["path",{d:"M12 8h.01",key:"e9boi3"}]]};Ie.node;const mt=S(Ie);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Be={name:"layers",size:24,node:[["path",{d:"M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z",key:"zw3jo"}],["path",{d:"M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12",key:"1wduqc"}],["path",{d:"M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17",key:"kqbvx6"}]],aliases:["layers-3"]};Be.node;const pt=S(Be);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ne={name:"lightbulb",size:24,node:[["path",{d:"M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5",key:"1gvzjb"}],["path",{d:"M9 18h6",key:"x1upvd"}],["path",{d:"M10 22h4",key:"ceow96"}]]};Ne.node;const xt=S(Ne);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const We={name:"play",size:24,node:[["path",{d:"M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z",key:"10ikf1"}]]};We.node;const yt=S(We);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const De={name:"search",size:24,node:[["path",{d:"m21 21-4.34-4.34",key:"14j7rj"}],["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}]]};De.node;const bt=S(De);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const $e={name:"sparkles",size:24,node:[["path",{d:"M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z",key:"1s2grr"}],["path",{d:"M20 2v4",key:"1rf3ol"}],["path",{d:"M22 4h-4",key:"gwowj6"}],["circle",{cx:"4",cy:"20",r:"2",key:"6kqj1y"}]],aliases:["stars"]};$e.node;const wt=S($e);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Fe={name:"x",size:24,node:[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]};Fe.node;const kt=S(Fe);function vt({size:e=28,ink:t="currentColor",accent:r="#3987e5",className:o=""}){return b.jsxs("svg",{className:`logomark-q ${o}`,width:e,height:e,viewBox:"0 0 100 100","aria-hidden":"true",focusable:"false",children:[b.jsx("defs",{children:b.jsxs("linearGradient",{id:"sqQGrad",x1:"0%",y1:"0%",x2:"100%",y2:"100%",children:[b.jsx("stop",{offset:"0%",stopColor:"#00f5ff"}),b.jsx("stop",{offset:"35%",stopColor:"#38bdf8"}),b.jsx("stop",{offset:"70%",stopColor:"#8b5cf6"}),b.jsx("stop",{offset:"100%",stopColor:"#ec4899"})]})}),b.jsxs("g",{fill:"none",stroke:t,strokeLinecap:"round",children:[b.jsx("circle",{cx:"44",cy:"44",r:"27",strokeWidth:"9"}),b.jsx("path",{d:"M63 63 78 78",stroke:"url(#sqQGrad)",strokeWidth:"9"}),b.jsx("path",{d:"M44 44V28M44 44l-13.8 8M44 44l13.8 8",strokeWidth:"4.5",opacity:"0.55"})]}),b.jsx("circle",{cx:"44",cy:"44",r:"7",fill:r}),b.jsx("circle",{cx:"83",cy:"83",r:"9",fill:"url(#sqQGrad)"})]})}const F=24,tt=Math.PI*2,ot=`#version 300 es
in vec2 aPosition;
void main() {
  gl_Position = vec4(aPosition, 0.0, 1.0);
}`,nt=`#version 300 es
precision highp float;
uniform vec2 uCenter;
uniform vec2 uHalf;
uniform float uRadius;
uniform float uPx;
uniform float uSpot;
uniform vec2 uEntry;
uniform vec3 uLineColor;
uniform vec3 uBaseColor;
uniform float uIntensity;
uniform vec2 uWindow;
uniform float uThickness;
uniform float uGlow;
out vec4 outColor;

float roundedBox(vec2 p, vec2 b, float r) {
  vec2 q = abs(p) - b + r;
  return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
}

float loopPosition(vec2 p, vec2 b, float r) {
  vec2 inner = b - r;
  float arc = 1.5707963 * r;
  float quarter = inner.x + inner.y + arc;
  vec2 a = abs(p);
  vec2 q = a - inner;
  float s = q.x > 0.0 && q.y > 0.0
    ? inner.y + atan(q.y, q.x) * r
    : (q.x > q.y ? min(a.y, inner.y) : inner.y + arc + inner.x - min(a.x, inner.x));
  if (p.x < 0.0) s = p.y >= 0.0 ? 2.0 * quarter - s : 2.0 * quarter + s;
  else if (p.y < 0.0) s = 4.0 * quarter - s;
  return s / max(4.0 * quarter, 0.0001);
}

float lobe(float position, float center) {
  float gap = abs(fract(position - center + 0.5) - 0.5);
  return 1.0 - smoothstep(uWindow.x, uWindow.x + uWindow.y, gap);
}

void main() {
  vec2 p = gl_FragCoord.xy - uCenter;
  float d = roundedBox(p, uHalf, uRadius);
  float position = loopPosition(p, uHalf, uRadius);
  float key = lobe(position, uSpot);
  float back = lobe(position, uSpot + 0.5);
  float streak = key + back * 0.45;
  float width = max(uThickness * uPx * mix(1.0, max(key, back), 0.6), 0.35);
  float band = smoothstep(-width - 0.6, -width + 0.6, d) * (1.0 - smoothstep(-0.6, 0.6, d));
  float hair = smoothstep(-uPx - 0.6, -uPx + 0.6, d) * (1.0 - smoothstep(-0.6, 0.6, d));
  float inside = 1.0 - smoothstep(-0.6, 0.6, d);
  vec2 pool = (p - uEntry) / (uHalf.y * vec2(1.6, 1.1));
  float glow = streak * 0.2 * exp(-abs(d + width * 0.5) / (5.0 * uPx)) + inside * 0.08 * exp(-dot(pool, pool));
  float light = clamp((band * streak + glow * uGlow) * uIntensity, 0.0, 1.0);
  vec4 base = vec4(uBaseColor, 1.0) * hair * 0.6;
  outColor = vec4(uLineColor, 1.0) * light + base * (1.0 - light);
}`,st=["uCenter","uHalf","uRadius","uPx","uSpot","uEntry","uLineColor","uBaseColor","uIntensity","uWindow","uThickness","uGlow"],ce=(e,t,r)=>Math.min(r,Math.max(t,e)),H=e=>e-Math.floor(e),_e=(e,t,r,o,m)=>{const d=r-m,p=o-m,h=Math.PI/2*m,a=d+p+h,g=Math.abs(e),_=Math.abs(t),M=g-d,w=_-p;let u;return M>0&&w>0?u=p+Math.atan2(w,M)*m:M>w?u=Math.min(_,p):u=p+h+d-Math.min(g,d),e<0?u=t>=0?2*a-u:2*a+u:t<0&&(u=4*a-u),H(u/Math.max(4*a,1e-4))},it=(e,t,r,o)=>{const m=t-o,d=r-o,p=Math.PI/2*o,h=m+d+p;let a=H(e)*4*h,g=1,_=1;a>3*h?(a=4*h-a,_=-1):a>2*h?(a-=2*h,g=-1,_=-1):a>h&&(a=2*h-a,g=-1);let M=m-(a-d-p),w=r;if(a<=d)M=t,w=a;else if(a<=d+p){const u=(a-d)/Math.max(o,1e-4);M=m+Math.cos(u)*o,w=d+Math.sin(u)*o}return[M*g,w*_]},Ee=(e,t,r)=>{const o=e.createShader(t);return o?(e.shaderSource(o,r),e.compileShader(o),e.getShaderParameter(o,e.COMPILE_STATUS)?o:(e.deleteShader(o),null)):null},rt=e=>{const t=Ee(e,e.VERTEX_SHADER,ot),r=Ee(e,e.FRAGMENT_SHADER,nt),o=e.createProgram();return!t||!r||!o?null:(e.attachShader(o,t),e.attachShader(o,r),e.bindAttribLocation(o,0,"aPosition"),e.linkProgram(o),e.deleteShader(t),e.deleteShader(r),e.getProgramParameter(o,e.LINK_STATUS)?o:(e.deleteProgram(o),null))},gt=({children:e="Get Started",size:t="lg",radius:r=18,tint:o="#ffffff",tintOpacity:m=.04,blur:d=0,textColor:p="#f5f5f5",lineColor:h="#ffffff",baseColor:a="#525252",intensity:g=1,idleIntensity:_=.35,shineSize:M=10,shineFade:w=34,thickness:u=1.2,glow:y=1,speed:q=.35,followMouse:j=!0,proximity:W=250,autoAnimate:D=!1,disabled:U=!1,onClick:J,className:X="",type:ee="button",style:te,...oe})=>{const ue=A.useRef(null),de=A.useRef(null),T=A.useRef(null),he={radius:Math.max(0,r),lineColor:String(h),baseColor:String(a),intensity:Math.max(0,g),idleIntensity:ce(_,0,1),shineSize:Math.max(0,M),shineFade:Math.max(0,w),thickness:Math.max(0,u),glow:Math.max(0,y),speed:q,followMouse:j,proximity:Math.max(1,W),autoAnimate:D,disabled:U},Y=A.useRef(he);return Y.current=he,A.useEffect(()=>{var Ce;const E=ue.current,P=de.current,s=P==null?void 0:P.getContext("webgl2",{alpha:!0,premultipliedAlpha:!0,antialias:!1,depth:!1,stencil:!1});if(!E||!P||!s)return;const O=rt(s);if(!O)return;const C={};for(const n of st)C[n]=s.getUniformLocation(O,n);const fe=s.createBuffer(),ne=s.createVertexArray();s.bindVertexArray(ne),s.bindBuffer(s.ARRAY_BUFFER,fe),s.bufferData(s.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),s.STATIC_DRAW),s.enableVertexAttribArray(0),s.vertexAttribPointer(0,2,s.FLOAT,!1,0,0),s.bindVertexArray(null);const $=document.createElement("canvas").getContext("2d",{willReadFrequently:!0}),Te=((Ce=window.matchMedia)==null?void 0:Ce.call(window,"(prefers-reduced-motion: reduce)").matches)??!1,se=new Map,f={width:1,height:1,ratio:1},L={x:0,y:0,known:!1},l={spot:0,level:0,press:0,ready:!1};let V=0,G=0,Q=!0;const me=n=>{if(se.has(n))return se.get(n);let i=[1,1,1];if($){$.clearRect(0,0,1,1),$.fillStyle="#000000",$.fillStyle=n,$.fillRect(0,0,1,1);const[c,x,k]=$.getImageData(0,0,1,1).data;i=[c/255,x/255,k/255]}return se.set(n,i),i},pe=n=>Math.min(n.radius,f.width/2,f.height/2),ie=n=>{const i=pe(n),c=i*(1-Math.SQRT1_2);return _e(c-f.width/2,f.height/2-c,f.width/2,f.height/2,i)},Ve=n=>{if(!n.followMouse||n.disabled||!L.known)return null;const i=E.getBoundingClientRect(),c=i.width/f.width||1,x=f.width/2,k=f.height/2,R=(L.x-i.left-i.width/2)/c,v=(i.top+i.height/2-L.y)/c,z=Math.hypot(Math.max(Math.abs(R)-x,0),Math.max(Math.abs(v)-k,0)),B=ce(1-z/n.proximity,0,1),Ae=B*B*(3-2*B),Z=_e(R,v,x,k,pe(n));if(z>0)return{spot:Z,near:Ae};const re=ce(Math.min(x-Math.abs(R),k-Math.abs(v))/(k*.8),0,1),Se=ie(n)-R/x*.06-v/k*.02,Ge=Se-Z-Math.round(Se-Z);return{spot:H(Z+Ge*re*re*(3-2*re)),near:Ae}},xe=n=>{const{width:i,height:c}=f,x=P.width/(i+F*2),k=P.height/(c+F*2);s.viewport(0,0,P.width,P.height),s.clearColor(0,0,0,0),s.clear(s.COLOR_BUFFER_BIT),s.useProgram(O),s.uniform2f(C.uCenter,(F+i/2)*x,(F+c/2)*k),s.uniform2f(C.uHalf,i/2*x,c/2*k),s.uniform1f(C.uRadius,Math.min(n.radius,i/2,c/2)*x),s.uniform1f(C.uPx,f.ratio);const R=Math.min(n.radius,i/2,c/2),[v,z]=it(l.spot,i/2,c/2,R),B=1-Math.min(.35*(c/2),Math.hypot(v,z))/Math.max(Math.hypot(v,z),1e-4);s.uniform1f(C.uSpot,l.spot),s.uniform2f(C.uEntry,v*B*x,z*B*k),s.uniform3fv(C.uLineColor,me(n.lineColor)),s.uniform3fv(C.uBaseColor,me(n.baseColor)),s.uniform1f(C.uIntensity,n.intensity*(l.level+l.press*.8)),s.uniform2f(C.uWindow,n.shineSize/360+l.press*.06,n.shineFade/360+1e-4),s.uniform1f(C.uThickness,n.thickness),s.uniform1f(C.uGlow,n.glow),s.bindVertexArray(ne),s.drawArrays(s.TRIANGLES,0,3),s.bindVertexArray(null)},ye=n=>{if(V=0,!Q)return;const i=Y.current,c=G?Math.min(.05,(n-G)/1e3):1/60;G=n;const x=Ve(i),k=i.autoAnimate&&!Te,R=!!x&&x.near>0;l.ready||(l.spot=ie(i),l.level=i.autoAnimate?1:i.idleIntensity,l.ready=!0);let v=0;k&&!R?l.spot=H(l.spot+i.speed/tt*c):(v=(R?x.spot:ie(i))-l.spot,v-=Math.round(v),l.spot=H(l.spot+v*(1-Math.exp(-c*8))));const z=i.autoAnimate?1:i.idleIntensity+(1-i.idleIntensity)*(x?x.near:0);l.level+=(z-l.level)*(1-Math.exp(-c*7)),l.press*=Math.exp(-c*5),xe(i),Math.abs(v)>2e-4||Math.abs(z-l.level)>.001||l.press>.002||k&&!R?V=requestAnimationFrame(ye):G=0},I=()=>{!V&&Q&&(V=requestAnimationFrame(ye))},be=n=>{var c;const i=(c=n==null?void 0:n.borderBoxSize)==null?void 0:c[0];f.width=Math.max(1,i?i.inlineSize:E.offsetWidth),f.height=Math.max(1,i?i.blockSize:E.offsetHeight),f.ratio=Math.min(window.devicePixelRatio||1,3),P.width=Math.max(1,Math.round((f.width+F*2)*f.ratio)),P.height=Math.max(1,Math.round((f.height+F*2)*f.ratio)),l.ready&&xe(Y.current),I()},we=n=>{L.x=n.clientX,L.y=n.clientY,L.known=!0,I()},ke=n=>{L.x=n.clientX,L.y=n.clientY,L.known=!0,Y.current.disabled||(l.press=1),I()},K=n=>{n.pointerType!=="mouse"&&(L.known=!1,I())},ve=()=>{L.known=!1,I()},ge=new ResizeObserver(n=>be(n[n.length-1]));ge.observe(E);const Me=new IntersectionObserver(n=>{Q=n.some(i=>i.isIntersecting),Q&&(G=0,I())});return Me.observe(E),window.addEventListener("pointermove",we,{passive:!0}),window.addEventListener("pointerup",K,{passive:!0}),window.addEventListener("pointercancel",K,{passive:!0}),document.documentElement.addEventListener("pointerleave",ve),E.addEventListener("pointerdown",ke),be(),T.current=I,()=>{var n;cancelAnimationFrame(V),T.current=null,ge.disconnect(),Me.disconnect(),window.removeEventListener("pointermove",we),window.removeEventListener("pointerup",K),window.removeEventListener("pointercancel",K),document.documentElement.removeEventListener("pointerleave",ve),E.removeEventListener("pointerdown",ke),s.deleteBuffer(fe),s.deleteVertexArray(ne),s.deleteProgram(O),(n=s.getExtension("WEBGL_lose_context"))==null||n.loseContext()}},[]),A.useEffect(()=>{var E;(E=T.current)==null||E.call(T)}),b.jsxs("button",{ref:ue,type:ee,disabled:U,onClick:J,className:`specular-button specular-button--${t}${X?` ${X}`:""}`,style:{"--sb-radius":`${r}px`,"--sb-tint":o,"--sb-tint-opacity":m,"--sb-blur":`${d}px`,"--sb-text-color":p,...te},...oe,children:[b.jsx("canvas",{ref:de,className:"specular-button__light","aria-hidden":"true"}),b.jsx("span",{className:"specular-button__label",children:e})]})};export{ct as A,ut as C,ft as D,mt as I,vt as L,yt as P,gt as S,kt as X,wt as a,pt as b,S as c,ht as d,dt as e,xt as f,lt as g,bt as h};
