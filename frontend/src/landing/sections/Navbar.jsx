import { useEffect, useState } from 'react';
import { Menu, X, Sparkles, User } from 'lucide-react';

import LogoMark from '../../components/LogoMark.jsx';
import AuthModal from '../../components/AuthModal.jsx';
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
  const [authOpen, setAuthOpen] = useState(false);
  const [user, setUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('synaptiq_user') || 'null');
    } catch {
      return null;
    }
  });

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
        >
          <div className="nav__brand-mark">
            <LogoMark size={26} ink="#eef0f5" accent="#3987e5" />
          </div>
          <span className="nav__brand-name">Synapti<span className="brand-q">Q</span></span>
          <span className="nav__brand-badge">
            <span className="nav__brand-dot" aria-hidden="true" />
            v1.0
          </span>
        </button>

        <ul className="nav__links">
          {LINKS.map(link => (
            <li key={link.id}>
              <button
                type="button"
                className="nav__link-btn cursor-target"
                data-cursor-label={link.label}
                onClick={() => handleNavClick(link.id)}
              >
                {link.label}
              </button>
            </li>
          ))}
        </ul>

        <div className="nav__actions">
          <div className="nav__status" title="Local evaluation engine active">
            <span className="nav__status-dot" aria-hidden="true" />
            <span className="nav__status-text">Local-First</span>
          </div>

          <button
            type="button"
            className="nav__link-btn cursor-target"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '6px 14px',
              borderRadius: '8px',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              background: 'rgba(255, 255, 255, 0.04)',
              color: user ? '#38bdf8' : '#e2e8f0',
              fontWeight: 500,
              fontSize: '13px',
              cursor: 'pointer'
            }}
            onClick={() => setAuthOpen(true)}
            data-cursor-label={user ? user.username : 'Account'}
          >
            <User size={14} />
            <span>{user ? user.username : 'Sign In'}</span>
          </button>

          <CtaButton size="sm" onClick={onLaunch} className="cursor-target" data-cursor-label="Dashboard">
            Launch Dashboard
          </CtaButton>

          <button
            type="button"
            className="nav__mobile-toggle"
            onClick={() => setMobileOpen(prev => !prev)}
            aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={mobileOpen}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </nav>

      <AuthModal isOpen={authOpen} onClose={() => setAuthOpen(false)} onAuthSuccess={u => setUser(u)} />

      {mobileOpen && (
        <div className="nav__mobile-menu">
          <ul className="nav__mobile-links">
            {LINKS.map(link => (
              <li key={link.id}>
                <button
                  type="button"
                  className="nav__mobile-link-btn"
                  onClick={() => handleNavClick(link.id)}
                >
                  {link.label}
                </button>
              </li>
            ))}
          </ul>
          <div className="nav__mobile-action">
            <CtaButton
              size="md"
              onClick={() => {
                setMobileOpen(false);
                onLaunch();
              }}
              style={{ width: '100%' }}
            >
              Launch Dashboard →
            </CtaButton>
          </div>
        </div>
      )}
    </header>
  );
}
