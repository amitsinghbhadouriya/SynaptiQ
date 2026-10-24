import { useEffect, useState } from 'react';
import { Menu, X, Sparkles } from 'lucide-react';

import LogoMark from '../../components/LogoMark.jsx';
import { CtaButton, scrollToId } from '../shared.jsx';

const LINKS = [
  { id: 'problem', label: 'Problem' },
  { id: 'loop', label: 'How it works' },
  { id: 'showcase', label: 'Showcase' },
  { id: 'features', label: 'Features' },
  { id: 'diagnosis', label: 'Diagnosis' },
  { id: 'pipeline', label: 'Pipeline' },
  { id: 'stack', label: 'Stack' }
];

export default function Navbar({ onLaunch }) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const handleNavClick = id => {
    setMobileOpen(false);
    scrollToId(id);
  };

  return (
    <header className={`nav-wrapper${scrolled ? ' nav-wrapper--scrolled' : ''}`}>
      <nav className="nav" aria-label="Main Navigation">
        <button
          type="button"
          className="nav__brand cursor-target"
          data-cursor-label="SynaptiQ"
          onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
