'use client';

import { useEffect, useRef } from 'react';

import './StarBorder.css';

const THEMES = {
  dark: {
    surface: '#0c0c0f',
    text: '#fafafa',
    track: 'rgba(255, 255, 255, 0.1)',
    light: '#ffffff'
  },
  light: {
    surface: '#ffffff',
    text: '#18181b',
    track: 'rgba(24, 24, 27, 0.12)',
    light: '#18181b'
  }
};

const HOVERS = ['lap', 'brighten', 'reveal', 'none'];
const BLEED = 48;
const LAP = 0.9;
const TAU = Math.PI * 2;
const WHITE = [255, 255, 255];

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
const wrap = (value, total) => ((value % total) + total) % total;
const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - (2 - 2 * t) ** 3 / 2);
const mix = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const rgba = (rgb, alpha) =>
  `rgba(${Math.round(rgb[0])}, ${Math.round(rgb[1])}, ${Math.round(rgb[2])}, ${clamp(alpha, 0, 1).toFixed(3)})`;

let colorContext = null;

const toRgb = color => {
  colorContext = colorContext ?? document.createElement('canvas').getContext('2d');
  if (!colorContext) return WHITE;
  colorContext.fillStyle = '#000000';
  colorContext.fillStyle = color;
  const value = String(colorContext.fillStyle);
  if (value.startsWith('#')) {
    const hex = parseInt(value.slice(1, 7), 16);
    return [(hex >> 16) & 255, (hex >> 8) & 255, hex & 255];
  }
  const parts = value.match(/[\d.]+/g)?.map(Number) ?? WHITE;
  return [parts[0], parts[1], parts[2]];
};

const outline = (width, height, radius) => {
  const r = Math.max(0, Math.min(radius, width / 2, height / 2));
  const arc = (Math.PI * r) / 2;
  const across = Math.max(0, width - 2 * r);
  const down = Math.max(0, height - 2 * r);
  const segments = [
    { length: across, x: r, y: 0, dx: 1, dy: 0, angle: null },
    { length: arc, x: width - r, y: r, dx: 0, dy: 0, angle: -Math.PI / 2 },
    { length: down, x: width, y: r, dx: 0, dy: 1, angle: null },
    { length: arc, x: width - r, y: height - r, dx: 0, dy: 0, angle: 0 },
    { length: across, x: width - r, y: height, dx: -1, dy: 0, angle: null },
    { length: arc, x: r, y: height - r, dx: 0, dy: 0, angle: Math.PI / 2 },
    { length: down, x: 0, y: height - r, dx: 0, dy: -1, angle: null },
    { length: arc, x: r, y: r, dx: 0, dy: 0, angle: Math.PI }
  ];
  return {
    r,
    segments,
    total: Math.max(
      1,
      segments.reduce((sum, segment) => sum + segment.length, 0)
    )
  };
};

const pointAt = (shape, distance, point) => {
  let s = wrap(distance, shape.total);
  for (const segment of shape.segments) {
    if (segment.length > 0 && s <= segment.length) {
      if (segment.angle === null) {
        point.x = segment.x + segment.dx * s;
        point.y = segment.y + segment.dy * s;
        point.nx = segment.dy;
        point.ny = -segment.dx;
      } else {
        const angle = segment.angle + s / shape.r;
        point.nx = Math.cos(angle);
        point.ny = Math.sin(angle);
        point.x = segment.x + point.nx * shape.r;
        point.y = segment.y + point.ny * shape.r;
      }
      return point;
    }
    s -= segment.length;
  }
  return point;
};

const project = (shape, px, py) => {
  let best = Infinity;
  let found = 0;
  let offset = 0;
  shape.segments.forEach(segment => {
    if (segment.length > 0) {
      let s = 0;
      let x = 0;
      let y = 0;
      if (segment.angle === null) {
        s = clamp((px - segment.x) * segment.dx + (py - segment.y) * segment.dy, 0, segment.length);
        x = segment.x + segment.dx * s;
        y = segment.y + segment.dy * s;
      } else {
        let angle = wrap(Math.atan2(py - segment.y, px - segment.x) - segment.angle, TAU);
        if (angle > Math.PI / 2) angle = angle > Math.PI * 1.25 ? 0 : Math.PI / 2;
        s = angle * shape.r;
        x = segment.x + Math.cos(segment.angle + angle) * shape.r;
        y = segment.y + Math.sin(segment.angle + angle) * shape.r;
      }
      const distance = (px - x) ** 2 + (py - y) ** 2;
      if (distance < best) {
        best = distance;
        found = offset + s;
      }
    }
    offset += segment.length;
  });
  return found;
};

const StarBorder = ({
  as: Component = 'button',
  children,
  className = '',
  style,
  color,
  trailColor,
  duration = 4,
  thickness = 1,
  radius = 12,
  trailLength = 0.3,
  stars = 1,
  glow = 0.6,
  sparkle = false,
  direction = 'clockwise',
  hover = 'lap',
  clickPulse = true,
  theme = 'dark',
  backgroundColor,
  textColor,
  borderColor,
  ...rest
}) => {
  const rootRef = useRef(null);
  const canvasRef = useRef(null);
  const wakeRef = useRef(null);
  const palette = THEMES[theme] ?? THEMES.dark;
  const light = color ?? palette.light;
  const settings = {
    light: theme === 'light',
    color: light,
    trailColor: trailColor ?? light,
    duration: Math.max(0.3, duration),
    thickness: Math.max(0.5, thickness),
    radius: Math.max(0, radius),
    trailLength: clamp(trailLength, 0, 1),
    stars: clamp(Math.round(stars), 1, 6),
    glow: clamp(glow, 0, 1),
    sparkle,
    direction: direction === 'counterclockwise' ? -1 : 1,
    hover: HOVERS.includes(hover) ? hover : 'lap',
    clickPulse
  };
  const settingsRef = useRef(settings);
  settingsRef.current = settings;

  useEffect(() => {
    const root = rootRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext('2d');
    if (!root || !canvas || !ctx) return undefined;

    const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
    const point = { x: 0, y: 0, nx: 0, ny: -1 };
    const state = {
      width: 0,
      height: 0,
      dpr: 1,
      phase: 0,
      velocity: 0,
      motion: 0,
      lap: -1,
      time: 0,
      reveal: 0,
      boost: 0,
      flash: 0,
      emit: 0,
      hovered: false,
      focused: false,
      pointerX: 0,
      pointerY: 0,
      visible: true
    };
    const pulses = [];
    const dust = [];
    const colors = { key: '', head: WHITE, tail: WHITE };
    let raf = 0;
    let last = performance.now();
    let alive = true;

    const measure = () => {
      state.width = root.offsetWidth;
      state.height = root.offsetHeight;
      state.dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.max(1, Math.round((state.width + BLEED * 2) * state.dpr));
      canvas.height = Math.max(1, Math.round((state.height + BLEED * 2) * state.dpr));
      canvas.style.width = `${state.width + BLEED * 2}px`;
      canvas.style.height = `${state.height + BLEED * 2}px`;
      canvas.style.top = `${-BLEED}px`;
      canvas.style.left = `${-BLEED}px`;
      wake();
    };

    const local = event => {
      const rect = root.getBoundingClientRect();
      const scaleX = rect.width ? state.width / rect.width : 1;
      const scaleY = rect.height ? state.height / rect.height : 1;
      return [(event.clientX - rect.left) * scaleX, (event.clientY - rect.top) * scaleY];
    };

    const shapeFor = s =>
      outline(
        Math.max(1, state.width - s.thickness),
        Math.max(1, state.height - s.thickness),
        s.radius - s.thickness / 2
      );

    const stroke = (x1, y1, x2, y2, width, style) => {
      ctx.lineWidth = width;
      ctx.strokeStyle = style;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    };

    const drawTrail = (s, shape, head, length, sign, intensity, tip = true) => {
      if (length < 0.5 || intensity <= 0) return;
      const steps = clamp(Math.ceil(length / 2), 2, 90);
      pointAt(shape, head, point);
      let px = point.x;
      let py = point.y;
      for (let i = 1; i <= steps; i++) {
        pointAt(shape, head - sign * length * (i / steps), point);
        const u = 1 - (i - 0.5) / steps;
        const fade = u * u * intensity;
        let tone = mix(colors.tail, colors.head, u);
        if (!s.light) tone = mix(tone, WHITE, u ** 6 * 0.65);
        ctx.lineCap = tip && i === 1 ? 'round' : 'butt';
        stroke(px, py, point.x, point.y, 2 + 6 * s.glow, rgba(tone, fade * (s.light ? 0.1 : 0.2) * s.glow));
        stroke(px, py, point.x, point.y, s.thickness, rgba(tone, fade));
        px = point.x;
        py = point.y;
      }
    };

    const drawHead = (s, x, y, intensity, twinkle) => {
      if (intensity <= 0) return;
      const tone = colors.head;
      const reach = (12 + 40 * s.glow) * (s.light ? 0.6 : 1);
      const bloom = ctx.createRadialGradient(x, y, 0, x, y, reach);
      const strength = (s.light ? 0.08 : 0.4) * s.glow * intensity;
      bloom.addColorStop(0, rgba(tone, strength));
      bloom.addColorStop(0.2, rgba(tone, strength * 0.4));
      bloom.addColorStop(0.5, rgba(tone, strength * 0.1));
      bloom.addColorStop(1, rgba(tone, 0));
      ctx.fillStyle = bloom;
      ctx.fillRect(x - reach, y - reach, reach * 2, reach * 2);
      if (!s.sparkle) return;

      const size = (1 + s.thickness * 0.6) * (s.light ? 0.85 : 1);
      const core = ctx.createRadialGradient(x, y, 0, x, y, size * 2.2);
      core.addColorStop(0, rgba(s.light ? tone : WHITE, intensity));
      core.addColorStop(s.light ? 0.3 : 0.4, rgba(s.light ? tone : mix(tone, WHITE, 0.5), intensity * 0.9));
      core.addColorStop(s.light ? 0.55 : 1, rgba(tone, s.light ? intensity * 0.12 : 0));
      core.addColorStop(1, rgba(tone, 0));
      ctx.fillStyle = core;
