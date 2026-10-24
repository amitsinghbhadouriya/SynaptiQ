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
