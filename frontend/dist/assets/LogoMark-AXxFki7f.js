import{r as l,j as c}from"./index-CW8keZlU.js";/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const F=t=>t==null?void 0:t.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase();/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function H(t,e,s=[]){if(e==null)throw new Error("[lucide]: iconNode is required when icon name is used");return{name:F(t),size:24,node:e,...s.length>0?{aliases:s}:{}}}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const U=t=>{let e="",s=!1;for(const o of t){if(o==="-"||o==="_"||o<=" "){s=e.length>0;continue}e.length===0?e+=o.toLowerCase():e+=s?o.toUpperCase():o,s=!1}return e};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const K=t=>{const e=U(t);return e.charAt(0).toUpperCase()+e.slice(1)};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const j=(...t)=>t.filter((e,s,o)=>!!e&&e.trim()!==""&&o.indexOf(e)===s).join(" ").trim();/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const r={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"};/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function z(t){return t!=null}function X(t,e={}){var b,x;const s=e.attributeNames??{},o=n=>s[n]??n,d=t.size??t.width??r.width,k=t.size??t.height??r.height,f=((b=t.aliases)==null?void 0:b.filter(n=>typeof n=="string"&&n.trim()!=="").map(n=>`lucide-${n}`))??[],y=[...t.name?[`lucide-${t.name}`]:[],...f],i=((x=e.className)==null?void 0:x.split(" ").filter(Boolean))??[],p=e.includeDefaultClasses===!1?j(...i):j("lucide",...y,...i),g=e.absoluteStrokeWidth?Number(e.strokeWidth??r["stroke-width"])*Number(t.size??t.width??r.width)/Number(e.size??e.width??r.width):e.strokeWidth??r["stroke-width"];return["svg",{...Object.entries(r).reduce((n,[h,u])=>(n[o(h)]=u,n),{}),..."color"in e&&e.color&&{[o("stroke")]:e.color},..."size"in e&&z(e.size)&&{[o("width")]:e.size,[o("height")]:e.size},..."width"in e&&z(e.width)&&{[o("width")]:e.width},..."height"in e&&z(e.height)&&{[o("height")]:e.height},[o("stroke-width")]:g,...p&&{[o("class")]:p},[o("viewBox")]:`0 0 ${d} ${k}`,...e.hasA11yProp===!1?{[o("aria-hidden")]:"true"}:{},..."attributes"in e&&e.attributes},t.node.map(n=>{const[h,u,w]=n,m=e.nonScalingStroke?{[o("vector-effect")]:"non-scaling-stroke",...u}:u;return w?[h,m,w]:[h,m]})]}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function Z(t,e={}){return X(t,{...e,attributeNames:{...e.attributeNames,class:"className","stroke-width":"strokeWidth","stroke-linecap":"strokeLinecap","stroke-linejoin":"strokeLinejoin","vector-effect":"vectorEffect"}})}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const J=t=>{for(const e in t)if(e.startsWith("aria-")||e==="role"||e==="title")return!0;return!1},O=l.createContext({}),T=()=>l.useContext(O),Y=l.forwardRef(({color:t,size:e,width:s,height:o,strokeWidth:d,absoluteStrokeWidth:k,nonScalingStroke:f,className:y="",children:i,iconNode:p=[],icon:g={node:p,aliases:[],size:24},...C},b)=>{const{size:x=24,strokeWidth:n=2,absoluteStrokeWidth:h=!1,nonScalingStroke:u=!1,color:w="currentColor",className:m=""}=T()??{},E=!!i||J(C),[P,V,G=[]]=Z(g,{color:t??w,width:s??e??x,height:o??e??x,strokeWidth:d??n,absoluteStrokeWidth:k??h,nonScalingStroke:f??u,className:j(m,y),hasA11yProp:E,attributes:C});return l.createElement(P,{ref:b,...V},[...G.map(([R,Q])=>l.createElement(R,Q)),...Array.isArray(i)?i:[i]])});/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function a(t,e=[],s=[]){const o=typeof t=="string"?H(t,e,s):t,d=l.forwardRef(({className:k,...f},y)=>l.createElement(Y,{ref:y,icon:o,className:k,...f}));return o.name&&(d.displayName=K(o.name)),d}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const _={name:"activity",size:24,node:[["path",{d:"M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2",key:"169zse"}]]};_.node;const te=a(_);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const M={name:"chart-column",size:24,node:[["path",{d:"M3 3v16a2 2 0 0 0 2 2h16",key:"c24i48"}],["path",{d:"M18 17V9",key:"2bz60n"}],["path",{d:"M13 17V5",key:"1frdt8"}],["path",{d:"M8 17v-3",key:"17ska0"}]],aliases:["bar-chart-3"]};M.node;const oe=a(M);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const v={name:"check",size:24,node:[["path",{d:"M20 6 9 17l-5-5",key:"1gmf2c"}]]};v.node;const se=a(v);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const A={name:"circle-alert",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["line",{x1:"12",x2:"12",y1:"8",y2:"12",key:"1pkeuh"}],["line",{x1:"12",x2:"12.01",y1:"16",y2:"16",key:"4dfq90"}]],aliases:["alert-circle"]};A.node;const ne=a(A);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const $={name:"circle-check",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m16 9-5.5 5.5L8 12",key:"xofnsj"}]],aliases:["check-circle-2"]};$.node;const ce=a($);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const L={name:"database",size:24,node:[["ellipse",{cx:"12",cy:"5",rx:"9",ry:"3",key:"msslwz"}],["path",{d:"M3 5V19A9 3 0 0 0 21 19V5",key:"1wlel7"}],["path",{d:"M3 12A9 3 0 0 0 21 12",key:"mv7ke4"}]]};L.node;const ae=a(L);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const N={name:"info",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"M12 16v-4",key:"1dtifu"}],["path",{d:"M12 8h.01",key:"e9boi3"}]]};N.node;const ie=a(N);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const S={name:"layers",size:24,node:[["path",{d:"M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z",key:"zw3jo"}],["path",{d:"M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12",key:"1wduqc"}],["path",{d:"M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17",key:"kqbvx6"}]],aliases:["layers-3"]};S.node;const re=a(S);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const D={name:"lightbulb",size:24,node:[["path",{d:"M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5",key:"1gvzjb"}],["path",{d:"M9 18h6",key:"x1upvd"}],["path",{d:"M10 22h4",key:"ceow96"}]]};D.node;const le=a(D);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const W={name:"play",size:24,node:[["path",{d:"M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z",key:"10ikf1"}]]};W.node;const de=a(W);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const q={name:"search",size:24,node:[["path",{d:"m21 21-4.34-4.34",key:"14j7rj"}],["circle",{cx:"11",cy:"11",r:"8",key:"4ej97u"}]]};q.node;const he=a(q);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const B={name:"sparkles",size:24,node:[["path",{d:"M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z",key:"1s2grr"}],["path",{d:"M20 2v4",key:"1rf3ol"}],["path",{d:"M22 4h-4",key:"gwowj6"}],["circle",{cx:"4",cy:"20",r:"2",key:"6kqj1y"}]],aliases:["stars"]};B.node;const ue=a(B);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const I={name:"x",size:24,node:[["path",{d:"M18 6 6 18",key:"1bl5f8"}],["path",{d:"m6 6 12 12",key:"d8bk6v"}]]};I.node;const ke=a(I);function fe({size:t=28,ink:e="currentColor",accent:s="#3987e5",className:o=""}){return c.jsxs("svg",{className:`logomark-q ${o}`,width:t,height:t,viewBox:"0 0 100 100","aria-hidden":"true",focusable:"false",children:[c.jsx("defs",{children:c.jsxs("linearGradient",{id:"sqQGrad",x1:"0%",y1:"0%",x2:"100%",y2:"100%",children:[c.jsx("stop",{offset:"0%",stopColor:"#00f5ff"}),c.jsx("stop",{offset:"35%",stopColor:"#38bdf8"}),c.jsx("stop",{offset:"70%",stopColor:"#8b5cf6"}),c.jsx("stop",{offset:"100%",stopColor:"#ec4899"})]})}),c.jsxs("g",{fill:"none",stroke:e,strokeLinecap:"round",children:[c.jsx("circle",{cx:"44",cy:"44",r:"27",strokeWidth:"9"}),c.jsx("path",{d:"M63 63 78 78",stroke:"url(#sqQGrad)",strokeWidth:"9"}),c.jsx("path",{d:"M44 44V28M44 44l-13.8 8M44 44l13.8 8",strokeWidth:"4.5",opacity:"0.55"})]}),c.jsx("circle",{cx:"44",cy:"44",r:"7",fill:s}),c.jsx("circle",{cx:"83",cy:"83",r:"9",fill:"url(#sqQGrad)"})]})}export{te as A,se as C,ae as D,ie as I,fe as L,de as P,ue as S,ke as X,re as a,ce as b,a as c,ne as d,le as e,oe as f,he as g};
