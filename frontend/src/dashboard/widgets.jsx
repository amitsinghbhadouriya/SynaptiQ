import { useEffect, useRef, useState } from 'react';
import Plotly from 'plotly.js-basic-dist-min';
import { ArrowDownRight, ArrowUpRight, CircleCheck, CircleX, Minus, TriangleAlert } from 'lucide-react';

import SpecularButton from '../components/reactbits/SpecularButton.jsx';
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
export function Button({ variant = 'ghost', theme = 'light', size = 'md', icon: Icon, children, className = '', ...props }) {
  const isDark = theme === 'dark';
  const primary = variant === 'primary';
  const darkVar = variant === 'dark';

  const tint = primary
    ? (isDark ? '#3987e5' : '#2a78d6')
    : (darkVar ? (isDark ? '#eef0f4' : '#15171c') : (isDark ? '#1a1d23' : '#ffffff'));
  const tintOpacity = primary ? 1.0 : (darkVar ? 1.0 : (isDark ? 0.6 : 0.95));
  const textColor = primary
    ? '#ffffff'
    : (darkVar ? (isDark ? '#111318' : '#ffffff') : (isDark ? '#eef0f4' : '#15171c'));
  const lineColor = primary ? '#ffffff' : (isDark ? '#38bdf8' : '#2a78d6');
  const baseColor = primary
    ? 'rgba(255, 255, 255, 0.4)'
    : (isDark ? 'rgba(56, 189, 248, 0.28)' : 'rgba(42, 120, 214, 0.25)');

  return (
    <SpecularButton
      size={size}
      radius={999}
      tint={tint}
      tintOpacity={tintOpacity}
      textColor={textColor}
      lineColor={lineColor}
      baseColor={baseColor}
      intensity={1.25}
      idleIntensity={0.4}
      shineSize={85}
      shineFade={110}
      thickness={1.5}
      glow={1.1}
      followMouse
      proximity={280}
      className={`d-btn d-btn--${size} d-btn--${variant} ${className}`.trim()}
      data-theme={theme}
      {...props}
    >
      {Icon && <Icon size={size === 'sm' ? 14 : 15} strokeWidth={2} aria-hidden="true" />}
      {children}
    </SpecularButton>
  );
}

export function IconButton({ icon: Icon, label, active = false, dot = false, className = '', ...props }) {
  return (
    <button type="button" className={`d-icon-btn${active ? ' is-active' : ''} ${className}`.trim()} aria-label={label} title={label} {...props}>
      <Icon size={16} strokeWidth={1.9} aria-hidden="true" />
      {dot && <span className="d-icon-btn__dot" aria-hidden="true" />}
    </button>
  );
}

// ---------------------------------------------------------------- badges
export function Badge({ tone = 'neutral', children, icon: Icon, className = '' }) {
  return (
    <span className={`d-badge d-badge--${tone} ${className}`.trim()}>
      {Icon && <Icon size={12} strokeWidth={2.2} aria-hidden="true" />}
      {children}
    </span>
  );
}

const TONE_ICON = { good: CircleCheck, bad: CircleX, warn: TriangleAlert, neutral: Minus };

export function DiagnosisBadge({ code, label }) {
  const tone = DIAGNOSIS_TONE[code] || 'neutral';
  return (
    <Badge tone={tone} icon={TONE_ICON[tone]}>
      {label}
    </Badge>
  );
}

export function Delta({ value, suffix = ' pts', invert = false, digits = 1 }) {
  if (value === null || value === undefined || Number.isNaN(value)) return <span className="d-delta d-delta--flat">no comparison</span>;
  const good = invert ? value < 0 : value > 0;
  const flat = Math.abs(value) < 1e-9;
  const Icon = flat ? Minus : value > 0 ? ArrowUpRight : ArrowDownRight;
  return (
    <span className={`d-delta ${flat ? 'd-delta--flat' : good ? 'd-delta--up' : 'd-delta--down'}`}>
      <Icon size={13} strokeWidth={2.4} aria-hidden="true" />
      {value > 0 ? '+' : ''}
      {value.toFixed(digits)}
      {suffix}
    </span>
  );
}

// -------------------------------------------------------- small controls
export function Segmented({ options, value, onChange, label, size = 'md' }) {
  return (
    <div className={`d-seg d-seg--${size}`} role="radiogroup" aria-label={label}>
      {options.map(option => {
        const Icon = option.icon;
        const selected = option.value === value;
        return (
          <button
            key={option.value}
            type="button"
            role="radio"
            aria-checked={selected}
            className={`d-seg__opt${selected ? ' is-selected' : ''}`}
            onClick={event => onChange(option.value, event)}
            title={option.title || option.label}
          >
            {Icon && <Icon size={14} strokeWidth={2} aria-hidden="true" />}
            {option.label && <span>{option.label}</span>}
          </button>
        );
      })}
    </div>
  );
}

export function FilterPills({ options, value, onChange, label }) {
  return (
    <div className="d-pills" role="tablist" aria-label={label}>
      {options.map(option => (
        <button
          key={option.value}
          type="button"
          role="tab"
          aria-selected={option.value === value}
          className={`d-pill${option.value === value ? ' is-selected' : ''}`}
          onClick={() => onChange(option.value)}
        >
          {option.label}
          <span className="d-pill__count">{option.count}</span>
        </button>
      ))}
    </div>
  );
}

export function Progress({ value, tone = 'accent' }) {
  const width = Math.max(0, Math.min(1, value || 0)) * 100;
  return (
    <span className="d-progress" role="presentation">
      <span className={`d-progress__fill d-progress__fill--${tone}`} style={{ width: `${width}%` }} />
    </span>
  );
}

export function Empty({ icon: Icon, title, children, actions }) {
  return (
    <div className="d-empty">
      {Icon && (
        <span className="d-empty__icon">
          <Icon size={20} strokeWidth={1.8} aria-hidden="true" />
        </span>
      )}
      <h3>{title}</h3>
      {children && <p>{children}</p>}
      {actions && <div className="d-empty__actions">{actions}</div>}
    </div>
  );
}

export function Card({ title, icon: Icon, actions, children, className = '', style }) {
  return (
    <section className={`d-card ${className}`.trim()} style={style}>
      {(title || actions) && (
        <header className="d-card__head">
          {Icon && (
            <span className="d-card__icon">
              <Icon size={15} strokeWidth={2} aria-hidden="true" />
            </span>
          )}
          {title && <h2 className="d-card__title">{title}</h2>}
          {actions && <div className="d-card__actions">{actions}</div>}
        </header>
      )}
      {children}
    </section>
  );
}

// ------------------------------------------------------------- gauge
export function Gauge({ value, target = 0.8, size = 168 }) {
  const animated = useCountUp(value ?? 0, 1300);
  const r = 64;
  const length = Math.PI * r;
  const clamp = v => Math.max(0, Math.min(1, v || 0));
  const targetAngle = Math.PI * (1 - clamp(target));
  const tx = 80 + r * Math.cos(targetAngle);
  const ty = 84 - r * Math.sin(targetAngle);
  return (
    <svg className="d-gauge" width={size} height={size * 0.62} viewBox="0 0 160 98" aria-hidden="true">
      <path d="M16 84a64 64 0 0 1 128 0" className="d-gauge__track" />
      <path
        d="M16 84a64 64 0 0 1 128 0"
        className="d-gauge__value"
        strokeDasharray={`${length * clamp(animated)} ${length}`}
      />
      <circle cx={tx} cy={ty} r="5" className="d-gauge__target" />
    </svg>
  );
}

// ----------------------------------------------------------- plotly chart
const DARK_SWAP = {
  '#2a78d6': '#3987e5',
  '#eb6834': '#d95926',
  '#1baf7a': '#199e70',
  '#eda100': '#c98500',
  '#e87ba4': '#d55181',
  '#b8bcc6': '#4a4d57',
  '#9a9ca5': '#6e717b',
  '#d7e4f6': '#26364f',
  '#ffffff': '#14161b',
  '#ececf0': '#24272e',
  'rgba(42,120,214,0.10)': 'rgba(57,135,229,0.16)'
};

function themed(figure, theme) {
  let text = JSON.stringify(figure);
  if (theme === 'dark') {
    for (const [from, to] of Object.entries(DARK_SWAP)) text = text.split(from).join(to);
  }
  const out = JSON.parse(text);
  const ink = theme === 'dark' ? '#8b909c' : '#898781';
  out.layout = {
    ...out.layout,
    autosize: true,
    font: { ...(out.layout?.font || {}), color: ink },
    hoverlabel: theme === 'dark'
      ? { bgcolor: '#2a2d35', bordercolor: '#2a2d35', font: { color: '#f4f5f8', size: 12 } }
      : out.layout?.hoverlabel
  };
  delete out.layout.template;
  return out;
}

export function PlotlyChart({ figure, theme, height = 260, className = '' }) {
  const ref = useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el || !figure) return undefined;
    const fig = themed(figure, theme);
    Plotly.react(el, fig.data, { ...fig.layout, height: fig.layout.height || height }, {
      displayModeBar: false,
      responsive: true,
      displaylogo: false
    });
    const observer = new ResizeObserver(() => Plotly.Plots.resize(el));
    observer.observe(el);
    return () => observer.disconnect();
  }, [figure, theme, height]);
  useEffect(() => {
    const el = ref.current;
    return () => {
      if (el) Plotly.purge(el);
    };
  }, []);
  if (!figure) return null;
  return <div ref={ref} className={`d-plot ${className}`.trim()} style={{ minHeight: height }} />;
}
