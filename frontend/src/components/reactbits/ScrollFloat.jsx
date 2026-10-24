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
  const containerRef = useRef(null);
  const textRef = useRef(null);

  const text = useMemo(() => {
    const parts = Children.toArray(children);
    return parts.every(part => typeof part === 'string' || typeof part === 'number') ? parts.join('') : null;
  }, [children]);

  const shiftColor = fromColor && fromColor !== 'currentColor' ? fromColor : null;
  const shiftStyle = useMemo(
    () =>
      shiftColor
        ? { color: `color-mix(in oklab, ${shiftColor} calc(var(--scroll-float-mix, 0) * 100%), currentColor)` }
        : undefined,
    [shiftColor]
  );

  const splitText = useMemo(() => {
    if (text === null) return null;
    return text.split(/(\s+)/).map((word, wordIndex) =>
      word.trim() === '' ? (
        word
      ) : (
        <span className="scroll-float-word" key={wordIndex}>
          {Array.from(word).map((char, charIndex) => (
            <span className="scroll-float-char" key={charIndex} style={shiftStyle}>
              {char}
            </span>
          ))}
        </span>
      )
    );
  }, [text, shiftStyle]);

  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  useIsomorphicLayoutEffect(() => {
    const el = containerRef.current;
    const textEl = textRef.current;
    if (!el || !textEl) return;
    if (scrollContainerRef && !scrollContainerRef.current) return;

    const scroller = scrollContainerRef?.current || window;
    const pieces = el.querySelectorAll(splitBy === 'words' ? '.scroll-float-word' : '.scroll-float-char');
    const targets = pieces.length ? Array.from(pieces) : [textEl];
    const indexOf = new Map(targets.map((target, index) => [target, index]));
    const at = fn => (_, target) => fn(indexOf.get(target) ?? 0);
    const middle = (targets.length - 1) / 2;
    const edge = index => (middle > 0 ? (index - middle) / middle : 0);
    const delays = getDelays(targets.length, order, stagger);
    const sign = direction === 'down' ? -1 : 1;
    const reach = Math.max(0, Number(distance) || 0) / 120;
    const squeeze = stretch > 0 ? stretch ** -0.43 : 1;
    const baseEase = gsap.parseEase(ease) || (p => p);
    const timing = p => clamp01(baseEase(p));
    const size = () => parseFloat(getComputedStyle(textEl).fontSize) || 16;
    const swell = p => {
      const t = timing(p);
      return 1 - Math.cos(t * Math.PI * 2.5) * Math.pow(1 - t, 2.6);
    };
    const sway = p => {
      const t = timing(p);
