import { useEffect, useState } from 'react';
import { Lock, LogOut, Mail, ShieldCheck, User, X, AlertCircle, CheckCircle2 } from 'lucide-react';
import './AuthModal.css';

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [mode, setMode] = useState('login');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('synaptiq_user') || 'null');
    } catch {
      return null;
    }
  });

  useEffect(() => {
    if (isOpen) {
      setError('');
      setSuccess('');
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('synaptiq_token');
      if (token) {
        await fetch('api/v1/auth/logout', {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` }
        }).catch(() => {});
      }
    } finally {
      localStorage.removeItem('synaptiq_user');
      localStorage.removeItem('synaptiq_token');
      setCurrentUser(null);
      setSuccess('Logged out successfully.');
      onAuthSuccess?.(null);
    }
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (mode === 'register' && password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      const endpoint = mode === 'login' ? 'api/v1/auth/login' : 'api/v1/auth/register';
      const body =
        mode === 'login'
          ? { username_or_email: username, password }
          : { username, email, password };

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await res.json();
      if (!res.ok) {
        if (res.status === 429) {
          throw new Error('Rate limit exceeded: maximum 30 requests per minute. Please wait a moment.');
        }
        throw new Error(data.detail || 'Authentication failed');
      }

      localStorage.setItem('synaptiq_user', JSON.stringify(data.user));
      const token = data.access_token || data.token;
      if (token) localStorage.setItem('synaptiq_token', token);
      setCurrentUser(data.user);
      setSuccess(`Signed in as ${data.user.username}`);
      onAuthSuccess?.(data.user);
      setTimeout(() => onClose(), 800);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sq-modal-overlay" onClick={onClose} role="dialog" aria-modal="true">
      <div className="sq-auth-card" onClick={e => e.stopPropagation()}>
        <button className="sq-auth-close" onClick={onClose} aria-label="Close dialog">
          <X size={18} />
        </button>

        <div className="sq-auth-header">
          <div className="sq-auth-badge">
            <ShieldCheck size={14} className="sq-auth-badge-icon" />
            <span>30 req/min rate limit active</span>
          </div>
          <h2 className="sq-auth-title">
            Synapti<span>Q</span> Access
          </h2>
          <p className="sq-auth-subtitle">
            {currentUser ? 'Manage your active evaluation session' : 'Sign in or create your evaluation account'}
          </p>
        </div>

        {currentUser ? (
          <div className="sq-auth-logged-in">
            <div className="sq-auth-avatar">
              <User size={28} />
            </div>
            <div className="sq-auth-user-info">
              <div className="sq-auth-username">{currentUser.username}</div>
              <div className="sq-auth-email">{currentUser.email || 'Local User'}</div>
              <div className="sq-auth-role">Role: {currentUser.role || 'user'}</div>
            </div>
            <button className="sq-auth-btn sq-auth-btn--danger" onClick={handleLogout}>
              <LogOut size={16} />
              Sign Out
            </button>
          </div>
        ) : (
          <>
            <div className="sq-auth-tabs">
              <button
                type="button"
                className={`sq-auth-tab ${mode === 'login' ? 'active' : ''}`}
                onClick={() => {
                  setMode('login');
                  setError('');
                }}
              >
                Sign In
              </button>
              <button
                type="button"
                className={`sq-auth-tab ${mode === 'register' ? 'active' : ''}`}
                onClick={() => {
                  setMode('register');
                  setError('');
                }}
              >
                Create Account
              </button>
            </div>

            {error && (
              <div className="sq-auth-alert sq-auth-alert--error">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}
            {success && (
              <div className="sq-auth-alert sq-auth-alert--success">
                <CheckCircle2 size={16} />
                <span>{success}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="sq-auth-form">
              <div className="sq-auth-field">
                <label className="sq-auth-label">
                  <User size={14} />
                  <span>{mode === 'login' ? 'Username or Email' : 'Username'}</span>
                </label>
                <input
                  type="text"
                  required
                  className="sq-auth-input"
                  placeholder={mode === 'login' ? 'e.g. admin or admin@synaptiq.ai' : 'at least 3 characters'}
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                />
              </div>

              {mode === 'register' && (
                <div className="sq-auth-field">
                  <label className="sq-auth-label">
                    <Mail size={14} />
                    <span>Email Address</span>
                  </label>
                  <input
                    type="email"
                    required
                    className="sq-auth-input"
                    placeholder="alex@company.com"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                  />
                </div>
              )}

              <div className="sq-auth-field">
                <label className="sq-auth-label">
                  <Lock size={14} />
                  <span>Password</span>
                </label>
                <input
                  type="password"
                  required
                  className="sq-auth-input"
                  placeholder="••••••••"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                />
              </div>

              {mode === 'register' && (
                <div className="sq-auth-field">
                  <label className="sq-auth-label">
                    <Lock size={14} />
                    <span>Confirm Password</span>
                  </label>
                  <input
                    type="password"
                    required
                    className="sq-auth-input"
                    placeholder="repeat your password"
                    value={confirmPassword}
                    onChange={e => setConfirmPassword(e.target.value)}
                  />
                </div>
              )}

              <button type="submit" disabled={loading} className="sq-auth-btn sq-auth-btn--primary">
                {loading ? 'Authenticating…' : mode === 'login' ? 'Sign In →' : 'Register Account →'}
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}

