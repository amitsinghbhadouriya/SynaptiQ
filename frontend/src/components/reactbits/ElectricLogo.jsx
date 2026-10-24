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
