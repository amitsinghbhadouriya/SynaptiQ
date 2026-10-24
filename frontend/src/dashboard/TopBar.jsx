import { useEffect, useRef, useState } from 'react';
import {
  BarChart3,
  Bell,
  ChevronDown,
  FileBarChart,
  FileText,
  FlaskConical,
  House,
  LayoutGrid,
  Moon,
  Settings,
  Sparkles,
  Sun,
  Wrench
} from 'lucide-react';

import LogoMark from '../components/LogoMark.jsx';
import { IconButton, Segmented } from './widgets.jsx';

export const TABS = [
  { id: 'overview', label: 'Overview', icon: LayoutGrid },
  { id: 'documents', label: 'Documents', icon: FileText },
  { id: 'evaluations', label: 'Evaluations', icon: FlaskConical },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
  { id: 'reports', label: 'Reports', icon: FileBarChart }
];

function useOutside(ref, onClose) {
  useEffect(() => {
    const handler = event => {
      if (ref.current && !ref.current.contains(event.target)) onClose();
    };
    const key = event => event.key === 'Escape' && onClose();
    document.addEventListener('pointerdown', handler);
    document.addEventListener('keydown', key);
    return () => {
      document.removeEventListener('pointerdown', handler);
      document.removeEventListener('keydown', key);
    };
  }, [ref, onClose]);
}

function Popover({ open, onClose, children, className = '' }) {
  const ref = useRef(null);
  useOutside(ref, onClose);
  if (!open) return null;
  return (
    <div ref={ref} className={`d-popover ${className}`.trim()} role="dialog">
      {children}
    </div>
  );
}

export default function TopBar({ tab, onTab, theme, onTheme, status, failing, onNavigate, onBell, onDemo, mode }) {
  const [menu, setMenu] = useState(null);
  const close = () => setMenu(null);
  const env = status || {};

  return (
    <header className="d-top">
      <button type="button" className="d-top__brand" onClick={() => onNavigate('home')} title="Back to the landing page">
        <LogoMark size={26} ink="currentColor" accent="var(--d-accent)" />
        <span>Synapti<span className="brand-q">Q</span></span>
      </button>

      <nav className="d-tabs" aria-label="Dashboard sections">
        {TABS.map(item => {
          const Icon = item.icon;
          const active = item.id === tab;
          return (
            <button
              key={item.id}
              type="button"
              className={`d-tab${active ? ' is-active' : ''}`}
              aria-current={active ? 'page' : undefined}
              onClick={() => onTab(item.id)}
            >
              {active && <Icon size={14} strokeWidth={2.2} aria-hidden="true" />}
              {item.label}
            </button>
          );
        })}
      </nav>

      <div className="d-top__actions">
        <Segmented
          size="sm"
          label="Colour theme"
          value={theme}
          onChange={(value, event) => onTheme(value, event)}
          options={[
            { value: 'light', icon: Sun, title: 'Light theme' },
            { value: 'dark', icon: Moon, title: 'Dark theme' }
          ]}
        />
        <IconButton icon={Bell} label={failing ? `${failing} failing questions in the selected run` : 'No failing questions'} dot={failing > 0} onClick={onBell} />
        <div className="d-anchor">
