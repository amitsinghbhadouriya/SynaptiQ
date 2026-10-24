import{a as ae,r as _,j as C}from"./index-B0CXAWtL.js";var ye=ae();/**
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
 */function yt(o){return o!=null}function he(o,e={}){var Z,X;const i=e.attributeNames??{},a=M=>i[M]??M,l=o.size??o.width??Q.width,b=o.size??o.height??Q.height,d=((Z=o.aliases)==null?void 0:Z.filter(M=>typeof M=="string"&&M.trim()!=="").map(M=>`lucide-${M}`))??[],w=[...o.name?[`lucide-${o.name}`]:[],...d],S=((X=e.className)==null?void 0:X.split(" ").filter(Boolean))??[],A=e.includeDefaultClasses===!1?vt(...S):vt("lucide",...w,...S),G=e.absoluteStrokeWidth?Number(e.strokeWidth??Q["stroke-width"])*Number(o.size??o.width??Q.width)/Number(e.size??e.width??Q.width):e.strokeWidth??Q["stroke-width"];return["svg",{...Object.entries(Q).reduce((M,[H,q])=>(M[a(H)]=q,M),{}),..."color"in e&&e.color&&{[a("stroke")]:e.color},..."size"in e&&yt(e.size)&&{[a("width")]:e.size,[a("height")]:e.size},..."width"in e&&yt(e.width)&&{[a("width")]:e.width},..."height"in e&&yt(e.height)&&{[a("height")]:e.height},[a("stroke-width")]:G,...A&&{[a("class")]:A},[a("viewBox")]:`0 0 ${l} ${b}`,...e.hasA11yProp===!1?{[a("aria-hidden")]:"true"}:{},..."attributes"in e&&e.attributes},o.node.map(M=>{const[H,q,J]=M,tt=e.nonScalingStroke?{[a("vector-effect")]:"non-scaling-stroke",...q}:q;return J?[H,tt,J]:[H,tt]})]}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function de(o,e={}){return he(o,{...e,attributeNames:{...e.attributeNames,class:"className","stroke-width":"strokeWidth","stroke-linecap":"strokeLinecap","stroke-linejoin":"strokeLinejoin","vector-effect":"vectorEffect"}})}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const fe=o=>{for(const e in o)if(e.startsWith("aria-")||e==="role"||e==="title")return!0;return!1},ue=_.createContext({}),ge=()=>_.useContext(ue),xe=_.forwardRef(({color:o,size:e,width:i,height:a,strokeWidth:l,absoluteStrokeWidth:b,nonScalingStroke:d,className:w="",children:S,iconNode:A=[],icon:G={node:A,aliases:[],size:24},...P},Z)=>{const{size:X=24,strokeWidth:M=2,absoluteStrokeWidth:H=!1,nonScalingStroke:q=!1,color:J="currentColor",className:tt=""}=ge()??{},xt=!!S||fe(P),[rt,it,lt=[]]=de(G,{color:o??J,width:i??e??X,height:a??e??X,strokeWidth:l??M,absoluteStrokeWidth:b??H,nonScalingStroke:d??q,className:vt(tt,w),hasA11yProp:xt,attributes:P});return _.createElement(rt,{ref:Z,...it},[...lt.map(([O,et])=>_.createElement(O,et)),...Array.isArray(S)?S:[S]])});/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */function R(o,e=[],i=[]){const a=typeof o=="string"?ie(o,e,i):o,l=_.forwardRef(({className:b,...d},w)=>_.createElement(xe,{ref:w,icon:a,className:b,...d}));return a.name&&(l.displayName=ce(a.name)),l}/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ht={name:"activity",size:24,node:[["path",{d:"M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2",key:"169zse"}]]};Ht.node;const Me=R(Ht);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Vt={name:"chart-column",size:24,node:[["path",{d:"M3 3v16a2 2 0 0 0 2 2h16",key:"c24i48"}],["path",{d:"M18 17V9",key:"2bz60n"}],["path",{d:"M13 17V5",key:"1frdt8"}],["path",{d:"M8 17v-3",key:"17ska0"}]],aliases:["bar-chart-3"]};Vt.node;const ve=R(Vt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Xt={name:"check",size:24,node:[["path",{d:"M20 6 9 17l-5-5",key:"1gmf2c"}]]};Xt.node;const be=R(Xt);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const Ot={name:"circle-check",size:24,node:[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m16 9-5.5 5.5L8 12",key:"xofnsj"}]],aliases:["check-circle-2"]};Ot.node;const we=R(Ot);/**
 * @license lucide-react v1.61.0 - ISC
 *
 * This source code is licensed under the ISC license.
