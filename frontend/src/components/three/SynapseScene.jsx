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
    const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(0x000000, 0);
    host.appendChild(renderer.domElement);
    renderer.domElement.style.display = 'block';
    renderer.domElement.style.width = '100%';
    renderer.domElement.style.height = '100%';

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(52, 1, 0.1, 100);
    camera.position.set(0, 0, 15);
    const world = new THREE.Group();
    scene.add(world);

    // ---- nodes on a noisy fibonacci shell, plus a sparse inner core
    const rand = mulberry32(17);
    const nodes = [];
    for (let i = 0; i < nodeCount; i++) {
      const inner = i % 6 === 0;
      const t = (i + 0.5) / nodeCount;
      const phi = Math.acos(1 - 2 * t);
      const theta = Math.PI * (1 + Math.sqrt(5)) * i;
      const r = inner ? radius * (0.25 + rand() * 0.45) : radius * (0.86 + rand() * 0.28);
      nodes.push(
        new THREE.Vector3(
          r * Math.sin(phi) * Math.cos(theta),
          r * Math.cos(phi) * 0.82,
          r * Math.sin(phi) * Math.sin(theta)
        )
      );
    }
    const nodePositions = new Float32Array(nodes.length * 3);
    const nodeSizes = new Float32Array(nodes.length);
    const nodeGlow = new Float32Array(nodes.length);
    nodes.forEach((p, i) => {
      nodePositions.set([p.x, p.y, p.z], i * 3);
      nodeSizes[i] = 1.4 + rand() * 2.6 + (i % 11 === 0 ? 3 : 0);
      nodeGlow[i] = 0.55 + rand() * 0.45;
    });
    const nodeGeometry = new THREE.BufferGeometry();
    nodeGeometry.setAttribute('position', new THREE.BufferAttribute(nodePositions, 3));
    nodeGeometry.setAttribute('aSize', new THREE.BufferAttribute(nodeSizes, 1));
    nodeGeometry.setAttribute('aGlow', new THREE.BufferAttribute(nodeGlow, 1));
    const nodeMaterial = pointsMaterial(nodeColor, 0.95);
    world.add(new THREE.Points(nodeGeometry, nodeMaterial));

    // ---- links: each node to its 3 nearest neighbours within reach
    const edges = [];
    const seen = new Set();
    nodes.forEach((a, i) => {
      const nearest = nodes
        .map((b, j) => ({ j, d: a.distanceToSquared(b) }))
        .filter(item => item.j !== i)
        .sort((x, y) => x.d - y.d)
        .slice(0, 3);
      nearest.forEach(({ j, d }) => {
        const key = i < j ? `${i}-${j}` : `${j}-${i}`;
        if (d < 7.5 && !seen.has(key)) {
          seen.add(key);
          edges.push([i, j]);
        }
      });
    });
    const adjacency = nodes.map(() => []);
    edges.forEach(([i, j], k) => {
      adjacency[i].push(k);
      adjacency[j].push(k);
    });
    const linkPositions = new Float32Array(edges.length * 6);
    edges.forEach(([i, j], k) => {
      linkPositions.set([nodes[i].x, nodes[i].y, nodes[i].z, nodes[j].x, nodes[j].y, nodes[j].z], k * 6);
    });
    const linkGeometry = new THREE.BufferGeometry();
    linkGeometry.setAttribute('position', new THREE.BufferAttribute(linkPositions, 3));
    const linkMaterial = new THREE.LineBasicMaterial({
      color: linkColor,
      transparent: true,
      opacity: 0.16,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });
    world.add(new THREE.LineSegments(linkGeometry, linkMaterial));

    // ---- pulses travelling along links
    const pulseCount = Math.min(70, edges.length);
    const pulses = Array.from({ length: pulseCount }, () => ({
      edge: Math.floor(rand() * edges.length),
      t: rand(),
      speed: 0.25 + rand() * 0.55,
      forward: rand() > 0.5
    }));
    const pulsePositions = new Float32Array(pulseCount * 3);
    const pulseSizes = new Float32Array(pulseCount).fill(4.2);
    const pulseGlow = new Float32Array(pulseCount).fill(1);
    const pulseGeometry = new THREE.BufferGeometry();
    pulseGeometry.setAttribute('position', new THREE.BufferAttribute(pulsePositions, 3));
    pulseGeometry.setAttribute('aSize', new THREE.BufferAttribute(pulseSizes, 1));
    pulseGeometry.setAttribute('aGlow', new THREE.BufferAttribute(pulseGlow, 1));
    const pulseMaterial = pointsMaterial(pulseColor, 1);
    world.add(new THREE.Points(pulseGeometry, pulseMaterial));

    // ---- orbit rings for depth
    const rings = [];
    [
      { r: radius * 1.42, tilt: [1.15, 0.2, 0], opacity: 0.12 },
      { r: radius * 1.7, tilt: [1.4, -0.5, 0.3], opacity: 0.07 }
    ].forEach(spec => {
      const curve = new THREE.EllipseCurve(0, 0, spec.r, spec.r, 0, Math.PI * 2);
      const geometry = new THREE.BufferGeometry().setFromPoints(curve.getPoints(160));
      const material = new THREE.LineBasicMaterial({ color: linkColor, transparent: true, opacity: spec.opacity });
      const ring = new THREE.LineLoop(geometry, material);
      ring.rotation.set(...spec.tilt);
      world.add(ring);
      rings.push(ring);
    });

    // ---- interaction state
    const pointer = { x: 0, y: 0 };
    const look = { x: 0, y: 0 };
    let scrollFade = 0;
    let visible = true;
    let raf = 0;
    let last = performance.now();

    const resize = () => {
      const width = Math.max(1, host.clientWidth);
      const height = Math.max(1, host.clientHeight);
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.position.z = width < 700 ? 19 : 15;
      camera.updateProjectionMatrix();
    };

    const onPointer = event => {
      pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
      pointer.y = (event.clientY / window.innerHeight) * 2 - 1;
    };
    const onScroll = () => {
      const rect = host.getBoundingClientRect();
      scrollFade = Math.min(1, Math.max(0, -rect.top / Math.max(1, rect.height)));
    };

    const tick = now => {
      raf = 0;
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      const motion = reduced ? 0.15 : 1;

