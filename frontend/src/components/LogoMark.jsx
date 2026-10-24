// Inline SynaptiQ mark for headers: a "Q" ring with a synapse terminal.
export default function LogoMark({ size = 28, ink = 'currentColor', accent = '#3987e5', className = '' }) {
  return (
    <svg className={`logomark-q ${className}`} width={size} height={size} viewBox="0 0 100 100" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="sqQGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#00f5ff" />
          <stop offset="35%" stopColor="#38bdf8" />
          <stop offset="70%" stopColor="#8b5cf6" />
          <stop offset="100%" stopColor="#ec4899" />
        </linearGradient>
      </defs>
      <g fill="none" stroke={ink} strokeLinecap="round">
        <circle cx="44" cy="44" r="27" strokeWidth="9" />
        <path d="M63 63 78 78" stroke="url(#sqQGrad)" strokeWidth="9" />
        <path d="M44 44V28M44 44l-13.8 8M44 44l13.8 8" strokeWidth="4.5" opacity="0.55" />
      </g>
      <circle cx="44" cy="44" r="7" fill={accent} />
      <circle cx="83" cy="83" r="9" fill="url(#sqQGrad)" />
    </svg>
  );
}
