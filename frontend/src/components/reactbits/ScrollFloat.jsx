'use client';

import { Children, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

import './ScrollFloat.css';

gsap.registerPlugin(ScrollTrigger);

const useIsomorphicLayoutEffect = typeof window !== 'undefined' ? useLayoutEffect : useEffect;

const clampToScroll = position =>
  typeof position === 'string' && !position.startsWith('clamp(') ? `clamp(${position})` : position;

const clamp01 = value => Math.min(Math.max(value, 0), 1);

const smoothstep = (from, to, value) => {
  const k = clamp01((value - from) / (to - from));
  return k * k * (3 - 2 * k);
};

const random = (index, salt) => {
  const value = Math.sin((index + 1) * 12.9898 + salt * 78.233) * 43758.5453;
  return value - Math.floor(value);
};

const getDelays = (count, order, stagger) => {
  const middle = (count - 1) / 2;
  const ranks = Array.from({ length: count }, (_, index) => {
    if (order === 'end') return count - 1 - index;
    if (order === 'center') return Math.abs(index - middle);
    if (order === 'edges') return middle - Math.abs(index - middle);
    return index;
  });
  if (order === 'random') {
    const shuffled = ranks.map((_, index) => index).sort((a, b) => random(a, 9) - random(b, 9));
    shuffled.forEach((target, rank) => {
      ranks[target] = rank;
    });
  }
  const first = Math.min(...ranks);
  return ranks.map(rank => (rank - first) * Math.max(0, stagger));
};

const ScrollFloat = ({
  children,
  scrollContainerRef,
  containerClassName = '',
  textClassName = '',
  effect = 'float',
  splitBy = 'chars',
  direction = 'up',
  order = 'start',
  fromColor = 'currentColor',
  animationDuration = 1,
  ease = 'back.inOut(2)',
  scrollStart = 'center bottom+=50%',
  scrollEnd = 'bottom bottom-=40%',
  stagger = 0.03,
  distance = 120,
  stretch = 2.3,
  smoothing = 0
}) => {
