'use client';

import { Children, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

import './ScrollReveal.css';

gsap.registerPlugin(ScrollTrigger);

const useIsomorphicLayoutEffect = typeof window !== 'undefined' ? useLayoutEffect : useEffect;

const SCRUB_SPAN = 0.5;
const RISE_MASK = 'inset(-1em -1em -0.15em -1em)';

const clampToScroll = position =>
  typeof position === 'string' && !position.startsWith('clamp(') ? `clamp(${position})` : position;

const clamp01 = value => Math.min(Math.max(value, 0), 1);
const smooth = value => value * value * (3 - 2 * value);
const easeOut = value => 1 - Math.pow(1 - value, 3);
const easeBack = (value, overshoot) => {
  const shifted = value - 1;
  return 1 + (overshoot + 1) * shifted * shifted * shifted + overshoot * shifted * shifted;
};
const glowAt = t => (t <= 0 || t >= 1 ? 0 : t < 0.35 ? smooth(t / 0.35) : 1 - smooth((t - 0.35) / 0.65));

const paintPiece = (piece, t, look) => {
  let reveal = t;
  let fadeIn = t;
  let motion = '';
  if (look.effect === 'rise') {
    reveal = easeOut(t);
    fadeIn = clamp01(reveal * 1.25);
    if (reveal < 1) {
      motion = look.masked
        ? `translateY(${((1 - reveal) * 100).toFixed(2)}%) translateY(${((1 - reveal) * 0.2).toFixed(3)}em)`
        : `translateY(${((1 - reveal) * 0.8).toFixed(3)}em)`;
    }
  } else if (look.effect === 'flip') {
    reveal = easeBack(t, 1.2);
    fadeIn = clamp01(t * 2);
    if (t < 1) motion = `perspective(6em) rotateX(${((1 - reveal) * 90).toFixed(2)}deg)`;
  } else if (look.effect === 'scale') {
    reveal = easeBack(t, 1.6);
    fadeIn = clamp01(t * 1.6);
    if (t < 1) motion = `scale(${(0.35 + 0.65 * reveal).toFixed(4)})`;
  }
  if (look.highlightColor) fadeIn = Math.max(fadeIn, clamp01(t / 0.35));
  const settle = clamp01(reveal);
  const lift = look.offset * (1 - settle);
  piece.style.opacity = t >= 1 ? '' : (look.baseOpacity + (1 - look.baseOpacity) * fadeIn).toFixed(3);
  piece.style.transform = [lift ? `translateY(${lift.toFixed(2)}px)` : '', motion].filter(Boolean).join(' ');
  piece.style.filter = look.blur && settle < 1 ? `blur(${(look.blur * (1 - settle)).toFixed(2)}px)` : '';
  if (look.highlightColor) {
    const glow = glowAt(t);
    piece.style.color =
      glow > 0.002 ? `color-mix(in srgb, ${look.highlightColor} ${(glow * 100).toFixed(1)}%, currentColor)` : '';
  }
};

const ScrollReveal = ({
  children,
  scrollContainerRef,
  enableBlur = true,
  baseOpacity = 0.1,
  baseRotation = 3,
  blurStrength = 4,
  baseOffset = 0,
  stagger = 0.05,
  smoothing = 0,
  splitBy = 'words',
  effect = 'fade',
  mode = 'scrub',
  duration = 0.8,
  highlightColor = '',
