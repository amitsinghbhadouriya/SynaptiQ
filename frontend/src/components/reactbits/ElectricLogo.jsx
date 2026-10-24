'use client';

import { useEffect, useRef } from 'react';
import { Renderer, Program, Mesh, Triangle, Texture } from 'ogl';

import './ElectricLogo.css';

const BOLT = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><path d="M39 3 12 37h17l-4 24 27-34H35z" fill="#fff"/></svg>'
)}`;
const RASTER = 560;
const CELL = 4;
const FAR = 1e20;
const ARCS = 5;
const PULSES = 3;
const PIXEL_BUDGET = 4e6;

const hexToRgb = hex => {
  let h = String(hex || '').replace('#', '');
  if (h.length === 3) h = h.replace(/./g, c => c + c);
  const n = parseInt(h.slice(0, 6), 16);
  return Number.isNaN(n) ? [1, 1, 1] : [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
};

const transformLine = (f, d, v, z, n) => {
  let k = 0;
  v[0] = 0;
  z[0] = -FAR;
  z[1] = FAR;
  for (let q = 1; q < n; q++) {
    let s = (f[q] + q * q - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
    while (s <= z[k]) {
      k--;
      s = (f[q] + q * q - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
    }
    k++;
    v[k] = q;
    z[k] = s;
    z[k + 1] = FAR;
  }
  k = 0;
  for (let q = 0; q < n; q++) {
    while (z[k + 1] < q) k++;
    d[q] = (q - v[k]) * (q - v[k]) + f[v[k]];
  }
};

const transformGrid = (grid, w, h) => {
  const n = Math.max(w, h);
  const f = new Float64Array(n);
  const d = new Float64Array(n);
  const v = new Int32Array(n);
  const z = new Float64Array(n + 1);
  for (let x = 0; x < w; x++) {
    for (let y = 0; y < h; y++) f[y] = grid[y * w + x];
    transformLine(f, d, v, z, h);
    for (let y = 0; y < h; y++) grid[y * w + x] = d[y];
  }
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) f[x] = grid[y * w + x];
    transformLine(f, d, v, z, w);
    for (let x = 0; x < w; x++) grid[y * w + x] = d[x];
  }
};

const blurLine = (src, dst, offset, stride, n, r) => {
  const scale = 1 / (2 * r + 1);
  let sum = 0;
  for (let i = 0; i <= r && i < n; i++) sum += src[offset + i * stride];
  for (let i = 0; i < n; i++) {
    dst[offset + i * stride] = sum * scale;
    if (i + r + 1 < n) sum += src[offset + (i + r + 1) * stride];
    if (i - r >= 0) sum -= src[offset + (i - r) * stride];
  }
};

const blurGrid = (grid, w, h, r) => {
  const tmp = new Float32Array(w * h);
  for (let pass = 0; pass < 3; pass++) {
    for (let y = 0; y < h; y++) blurLine(grid, tmp, y * w, 1, w, r);
    for (let x = 0; x < w; x++) blurLine(tmp, grid, x, w, h, r);
  }
};

const readCoverage = (data, w, h) => {
  const coverage = new Float32Array(w * h);
  let clear = 0;
  for (let i = 0; i < w * h; i++) if (data[i * 4 + 3] < 250) clear++;
  if (clear > w * h * 0.01) {
    for (let i = 0; i < w * h; i++) coverage[i] = data[i * 4 + 3] / 255;
    return coverage;
  }
  let r = 0;
  let g = 0;
  let b = 0;
  let n = 0;
  const sample = i => {
    r += data[i * 4];
    g += data[i * 4 + 1];
    b += data[i * 4 + 2];
    n++;
  };
  for (let x = 0; x < w; x++) {
    sample(x);
    sample((h - 1) * w + x);
  }
  for (let y = 0; y < h; y++) {
    sample(y * w);
    sample(y * w + w - 1);
  }
  r /= n;
  g /= n;
  b /= n;
  for (let i = 0; i < w * h; i++) {
    const diff = Math.max(Math.abs(data[i * 4] - r), Math.abs(data[i * 4 + 1] - g), Math.abs(data[i * 4 + 2] - b));
    coverage[i] = Math.min(1, Math.max(0, (diff - 24) / 48));
  }
  return coverage;
};

const sampleField = (shape, x, y) => {
  const { field, width, height } = shape;
  const cx = Math.min(Math.max(x, 0.5), width - 0.5);
  const cy = Math.min(Math.max(y, 0.5), height - 0.5);
  const x0 = Math.min(Math.floor(cx - 0.5), width - 2);
  const y0 = Math.min(Math.floor(cy - 0.5), height - 2);
  const tx = cx - 0.5 - x0;
  const ty = cy - 0.5 - y0;
  const i = y0 * width + x0;
  const top = field[i] + (field[i + 1] - field[i]) * tx;
  const bottom = field[i + width] + (field[i + width + 1] - field[i + width]) * tx;
  return top + (bottom - top) * ty + Math.hypot(x - cx, y - cy);
};

const traceShape = image => {
  const iw = image.naturalWidth || image.width;
  const ih = image.naturalHeight || image.height;
  if (!iw || !ih) return null;
  const fit = RASTER / Math.max(iw, ih);
  const w = Math.max(2, Math.round(iw * fit));
  const h = Math.max(2, Math.round(ih * fit));
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  if (!ctx) return null;
  ctx.drawImage(image, 0, 0, w, h);
  const coverage = readCoverage(ctx.getImageData(0, 0, w, h).data, w, h);

  let left = w;
  let top = h;
  let right = -1;
  let bottom = -1;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (coverage[y * w + x] <= 0.01) continue;
      if (x < left) left = x;
      if (x > right) right = x;
      if (y < top) top = y;
      if (y > bottom) bottom = y;
    }
  }
  if (right < 0) return null;

  const logoWidth = right - left + 1;
  const logoHeight = bottom - top + 1;
  const pad = Math.ceil(Math.max(logoWidth, logoHeight) * 0.25) + 2;
  const width = logoWidth + pad * 2;
  const height = logoHeight + pad * 2;
  const outer = new Float32Array(width * height);
  const inner = new Float32Array(width * height);
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const sx = x - pad + left;
      const sy = y - pad + top;
      const a = sx >= 0 && sy >= 0 && sx < w && sy < h ? coverage[sy * w + sx] : 0;
      const i = y * width + x;
      if (a >= 1) {
        outer[i] = 0;
        inner[i] = FAR;
      } else if (a <= 0) {
        outer[i] = FAR;
        inner[i] = 0;
      } else {
        const e = 0.5 - a;
        outer[i] = e > 0 ? e * e : 0;
        inner[i] = e < 0 ? e * e : 0;
      }
    }
  }
  transformGrid(outer, width, height);
  transformGrid(inner, width, height);

  const field = new Float32Array(width * height);
  for (let i = 0; i < width * height; i++) field[i] = Math.sqrt(outer[i]) - Math.sqrt(inner[i]);

  const points = [];
  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      const i = y * width + x;
      const d = field[i];
      if (d > 0) continue;
      if (field[i - 1] <= 0 && field[i + 1] <= 0 && field[i - width] <= 0 && field[i + width] <= 0) continue;
      const gx = field[i + 1] - field[i - 1];
      const gy = field[i + width] - field[i - width];
      const len = Math.hypot(gx, gy) || 1;
      points.push(x + 0.5 - (d * gx) / len, y + 0.5 - (d * gy) / len);
    }
  }
  const stride = Math.max(1, Math.ceil(points.length / 2 / 3000)) * 2;
  const edges = [];
  for (let i = 0; i < points.length; i += stride) edges.push(points[i], points[i + 1]);

  const size = Math.max(logoWidth, logoHeight);
  const glowPad = Math.ceil((size * 0.7) / CELL);
  const glowWidth = Math.ceil(logoWidth / CELL) + glowPad * 2;
  const glowHeight = Math.ceil(logoHeight / CELL) + glowPad * 2;
  const tight = new Float32Array(glowWidth * glowHeight);
  for (let y = 0; y < height; y++) {
    const gy = Math.floor((y - pad) / CELL) + glowPad;
    for (let x = 0; x < width; x++) {
      const gx = Math.floor((x - pad) / CELL) + glowPad;
      tight[gy * glowWidth + gx] += Math.exp(-Math.abs(field[y * width + x]) / 1.5) / (CELL * CELL);
    }
  }
  const wide = tight.slice();
  const tightRadius = Math.max(1, Math.round((size * 0.035) / CELL));
  const wideRadius = Math.max(2, Math.round((size * 0.13) / CELL));
  blurGrid(tight, glowWidth, glowHeight, tightRadius);
  blurGrid(wide, glowWidth, glowHeight, wideRadius);
  const tightNorm = (Math.sqrt(2 * Math.PI * (tightRadius * tightRadius + tightRadius)) * CELL) / 3;
  const wideNorm = (Math.sqrt(2 * Math.PI * (wideRadius * wideRadius + wideRadius)) * CELL) / 3;
  const glow = new Float32Array(glowWidth * glowHeight * 2);
  for (let i = 0; i < glowWidth * glowHeight; i++) {
    glow[i * 2] = tight[i] * tightNorm;
    glow[i * 2 + 1] = wide[i] * wideNorm;
  }

  return {
    field,
    edges,
    width,
    height,
    pad,
    logoWidth,
    logoHeight,
    glow,
    glowWidth,
    glowHeight,
    glowOffset: pad - glowPad * CELL
  };
};

const spawnArc = (shape, time, focus) => {
  const { edges, logoWidth, logoHeight } = shape;
  const count = edges.length / 2;
  if (count < 2) return null;
  const size = Math.max(logoWidth, logoHeight);
  let i = Math.floor(Math.random() * count);
  if (focus) {
    let found = false;
    for (let attempt = 0; attempt < 40 && !found; attempt++) {
      const j = Math.floor(Math.random() * count);
      if (Math.hypot(edges[j * 2] - focus.x, edges[j * 2 + 1] - focus.y) < focus.radius) {
        i = j;
        found = true;
      }
    }
    if (!found) return null;
  }
  const ax = edges[i * 2];
  const ay = edges[i * 2 + 1];
  for (let attempt = 0; attempt < 24; attempt++) {
    const j = Math.floor(Math.random() * count);
    const bx = edges[j * 2];
    const by = edges[j * 2 + 1];
    const len = Math.hypot(bx - ax, by - ay);
    if (len < size * 0.08 || len > size * 0.3) continue;
    const nx = -(by - ay) / len;
    const ny = (bx - ax) / len;
    const bow = len * (0.2 + Math.random() * 0.3);
    const mx = (ax + bx) / 2;
    const my = (ay + by) / 2;
    const left = sampleField(shape, mx + nx * bow, my + ny * bow);
    const right = sampleField(shape, mx - nx * bow, my - ny * bow);
    if (Math.max(left, right) <= 0) continue;
    return {
      ax,
      ay,
      bx,
      by,
      bow: left >= right ? bow : -bow,
      seed: 1 + Math.random() * 60,
      born: time,
      life: 0.35 + Math.random() * 0.45
    };
  }
  return null;
};

const vertex = `#version 300 es
in vec2 position;
in vec2 uv;
out vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position, 0.0, 1.0);
}
`;

const fragment = `#version 300 es
precision highp float;
precision highp int;

uniform sampler2D tFieldFrom;
uniform sampler2D tGlowFrom;
uniform sampler2D tFieldTo;
uniform sampler2D tGlowTo;
uniform vec4 uMapFrom;
uniform vec4 uSizeFrom;
uniform vec4 uMapTo;
uniform vec4 uSizeTo;
uniform float uMorph;
uniform vec2 uResolution;
uniform float uUnit;
uniform float uTime;
uniform float uPresence;
uniform vec3 uHover;
uniform float uHoverRadius;
uniform vec4 uPulses[${PULSES}];
uniform float uPulseBoost;
uniform float uFlash;
uniform vec3 uColor;
uniform vec3 uGlowColor;
uniform float uIntensity;
uniform float uGlow;
uniform float uThickness;
uniform float uStrands;
uniform float uBend;
uniform float uCrackle;
uniform float uFlicker;
uniform float uFill;
uniform float uInk;
uniform vec4 uArcEnds[${ARCS}];
uniform vec4 uArcShape[${ARCS}];

in vec2 vUv;
out vec4 fragColor;

uint scramble(uint x) {
  x ^= x >> 16u;
  x *= 0x7feb352du;
  x ^= x >> 15u;
  x *= 0x846ca68bu;
  x ^= x >> 16u;
  return x;
}

float fieldAt(sampler2D tex, vec4 map, vec4 size, vec2 p) {
  vec2 f = (p - map.xy) / map.z;
  vec2 c = clamp(f, vec2(0.5), size.xy - 0.5);
  return (textureLod(tex, c / size.xy, 0.0).r + length(f - c)) * map.z;
}

vec2 glowAt(sampler2D tex, vec4 map, vec4 size, vec2 p) {
  vec2 f = (p - map.xy) / map.z - map.w;
  return textureLod(tex, f / (size.zw * ${CELL}.0), 0.0).rg;
}

float shape(vec2 p, float k) {
  float to = fieldAt(tFieldTo, uMapTo, uSizeTo, p);
  if (k >= 1.0) return to;
  return mix(fieldAt(tFieldFrom, uMapFrom, uSizeFrom, p), to, k);
}

vec2 aura(vec2 p, float k) {
  vec2 to = glowAt(tGlowTo, uMapTo, uSizeTo, p);
  if (k >= 1.0) return to;
  return mix(glowAt(tGlowFrom, uMapFrom, uSizeFrom, p), to, k);
}

vec4 corner(ivec2 c, uint seed) {
  uint h = scramble(uint(c.x) * 0x8da6b343u + uint(c.y) * 0xd8163841u + seed * 0xcb1ab31fu);
  return vec4(uvec4(h, h >> 8u, h >> 16u, h >> 24u) & 255u) / 127.5 - 1.0;
}

vec2 drift(vec2 p, uint seed, out mat2 jac) {
  vec2 i = floor(p);
  vec2 f = p - i;
  vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
  vec2 du = 30.0 * f * f * (f * (f - 2.0) + 1.0);
  ivec2 c = ivec2(i);
  vec4 ga = corner(c, seed);
  vec4 gb = corner(c + ivec2(1, 0), seed);
  vec4 gc = corner(c + ivec2(0, 1), seed);
  vec4 gd = corner(c + ivec2(1, 1), seed);
  vec2 fb = f - vec2(1.0, 0.0);
  vec2 fc = f - vec2(0.0, 1.0);
  vec2 fd = f - vec2(1.0);
  vec2 va = vec2(dot(ga.xy, f), dot(ga.zw, f));
  vec2 vb = vec2(dot(gb.xy, fb), dot(gb.zw, fb));
  vec2 vc = vec2(dot(gc.xy, fc), dot(gc.zw, fc));
  vec2 vd = vec2(dot(gd.xy, fd), dot(gd.zw, fd));
