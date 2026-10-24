import { useEffect, useRef, useState } from 'react';
import Plotly from 'plotly.js-basic-dist-min';
import { ArrowDownRight, ArrowUpRight, CircleCheck, CircleX, Minus, TriangleAlert } from 'lucide-react';

import StarBorder from '../components/reactbits/StarBorder.jsx';
import { DIAGNOSIS_TONE } from './format.js';

// ------------------------------------------------------------- count-up
export function useCountUp(target, duration = 1100) {
  const [value, setValue] = useState(0);
  const fromRef = useRef(0);
  useEffect(() => {
    if (target === null || target === undefined || Number.isNaN(target)) {
      setValue(target);
      return undefined;
    }
    const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    if (reduce) {
      setValue(target);
      return undefined;
    }
    const from = 0;
    const start = performance.now();
    let raf = 0;
    const step = now => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      setValue(from + (target - from) * eased);
      if (t < 1) raf = requestAnimationFrame(step);
      else fromRef.current = target;
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [target, duration]);
  return value;
}

export function CountUp({ value, format = v => Math.round(v).toLocaleString(), className = '' }) {
  const current = useCountUp(value);
  return <span className={className}>{current === null || current === undefined ? '—' : format(current)}</span>;
}

// --------------------------------------------------------------- buttons
// Every dashboard button is a React Bits StarBorder, styled per variant and theme.
const VARIANTS = {
  primary: { light: ['#2a78d6', '#ffffff', 'rgba(42,120,214,0.35)', '#ffffff'], dark: ['#3987e5', '#ffffff', 'rgba(57,135,229,0.45)', '#ffffff'] },
  dark: { light: ['#15171c', '#ffffff', 'rgba(21,23,28,0.2)', '#9cc2f3'], dark: ['#eef0f4', '#111318', 'rgba(255,255,255,0.2)', '#2a78d6'] },
  ghost: { light: ['#ffffff', '#15171c', '#e3e5ea', '#2a78d6'], dark: ['#1a1d23', '#eef0f4', 'rgba(255,255,255,0.1)', '#9cc2f3'] }
};

export function Button({ variant = 'ghost', theme = 'light', size = 'md', icon: Icon, children, className = '', ...props }) {
  const [bg, fg, border, star] = VARIANTS[variant][theme === 'dark' ? 'dark' : 'light'];
  const lightSurface = (variant === 'ghost' && theme !== 'dark') || (variant === 'dark' && theme === 'dark');
  return (
    <StarBorder
      theme={lightSurface ? 'light' : 'dark'}
      color={star}
      backgroundColor={bg}
      textColor={fg}
      borderColor={border}
      radius={999}
      glow={0.5}
      duration={variant === 'primary' ? 3.5 : 5}
      hover="lap"
      className={`d-btn d-btn--${size} d-btn--${variant} ${className}`.trim()}
      {...props}
    >
      {Icon && <Icon size={size === 'sm' ? 14 : 15} strokeWidth={2} aria-hidden="true" />}
      {children}
    </StarBorder>
  );
