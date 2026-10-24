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
