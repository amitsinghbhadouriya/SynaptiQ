import { useEffect, useRef } from 'react';
import * as THREE from 'three';

// A slowly rotating 3D "synapse" network: nodes on a noisy shell, nearest-neighbour links,
// signal pulses travelling along links, and two orbit rings. Follows the pointer with a
// gentle parallax and recedes as the page scrolls. Pauses when off-screen.

const POINT_VERTEX = /* glsl */ `
  attribute float aSize;
  attribute float aGlow;
  uniform float uPixelRatio;
  varying float vAlpha;
  void main() {
    vec4 mv = modelViewMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * mv;
    gl_PointSize = aSize * uPixelRatio * (30.0 / -mv.z);
    vAlpha = aGlow * smoothstep(30.0, 9.0, -mv.z);
  }
`;

const POINT_FRAGMENT = /* glsl */ `
  uniform vec3 uColor;
  uniform float uOpacity;
  varying float vAlpha;
  void main() {
    float d = length(gl_PointCoord - 0.5);
    float a = pow(smoothstep(0.5, 0.0, d), 1.6);
    gl_FragColor = vec4(uColor, a * vAlpha * uOpacity);
  }
`;

const pointsMaterial = (color, opacity) =>
  new THREE.ShaderMaterial({
    uniforms: {
      uColor: { value: new THREE.Color(color) },
      uOpacity: { value: opacity },
      uPixelRatio: { value: Math.min(window.devicePixelRatio || 1, 2) }
    },
    vertexShader: POINT_VERTEX,
    fragmentShader: POINT_FRAGMENT,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending
  });

function mulberry32(seed) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export default function SynapseScene({
  className = '',
  nodeCount = 240,
  radius = 6.2,
  nodeColor = '#dfe8f7',
  linkColor = '#6f9fe6',
  pulseColor = '#5aa2ff'
}) {
  const hostRef = useRef(null);

  useEffect(() => {
    const host = hostRef.current;
    if (!host) return undefined;
    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    } catch {
      return undefined; // no WebGL: the hero still works without the scene
    }
