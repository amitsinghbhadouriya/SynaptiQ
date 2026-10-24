// Line-art illustrations for the feature explanation panels (no photos).
// Neutral strokes with a single accent, drawn on a 400×600 canvas.

const A = '#3987e5';
const S = 'rgba(255,255,255,0.22)';
const F = 'rgba(255,255,255,0.05)';

function Frame({ children }) {
  return (
    <svg viewBox="0 0 400 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <pattern id="sq-grid" width="24" height="24" patternUnits="userSpaceOnUse">
          <path d="M24 0H0V24" fill="none" stroke="rgba(255,255,255,0.04)" />
        </pattern>
        <radialGradient id="sq-glow" cx="50%" cy="38%" r="60%">
          <stop offset="0" stopColor="rgba(57,135,229,0.22)" />
          <stop offset="1" stopColor="rgba(57,135,229,0)" />
        </radialGradient>
      </defs>
      <rect width="400" height="600" fill="#0d0f15" />
      <rect width="400" height="600" fill="url(#sq-grid)" />
      <rect width="400" height="600" fill="url(#sq-glow)" />
      <g fill="none" stroke={S} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        {children}
      </g>
    </svg>
  );
}

const lines = (x, y, widths, gap = 16) =>
  widths.map((w, i) => <path key={i} d={`M${x} ${y + i * gap}h${w}`} />);

export const ILLUSTRATIONS = {
  ingest: (
    <Frame>
      <rect x="120" y="110" width="150" height="196" rx="12" fill={F} />
      <rect x="140" y="130" width="150" height="196" rx="12" fill="#11141c" />
      {lines(162, 168, [100, 86, 104, 70, 96, 58])}
      <path d="M215 360v70" stroke={A} />
      <path d="M200 415l15 15 15-15" stroke={A} />
      <rect x="150" y="452" width="130" height="34" rx="9" stroke={A} />
      <path d="M168 469h94" stroke={A} />
    </Frame>
  ),
  chunk: (
    <Frame>
      {[0, 1, 2, 3, 4].map(i => (
        <rect key={i} x={110 + (i % 2) * 18} y={120 + i * 66} width="180" height="50" rx="10" fill={i === 2 ? 'rgba(57,135,229,0.12)' : F} stroke={i === 2 ? A : S} />
      ))}
      {[0, 1, 2, 3, 4].map(i => (
        <circle key={i} cx={320} cy={145 + i * 66} r="5" fill={i === 2 ? A : 'none'} stroke={i === 2 ? A : S} />
      ))}
      <path d="M320 150v250" strokeDasharray="3 6" />
    </Frame>
  ),
  tests: (
    <Frame>
      <rect x="96" y="130" width="208" height="92" rx="14" fill={F} />
      <text x="118" y="172" fill="#e9eef8" stroke="none" fontSize="26" fontFamily="Space Grotesk, sans-serif">Q</text>
      {lines(150, 164, [120, 90])}
      <rect x="96" y="246" width="208" height="92" rx="14" fill={F} />
      <text x="118" y="288" fill={A} stroke="none" fontSize="26" fontFamily="Space Grotesk, sans-serif">A</text>
      {lines(150, 280, [110, 130])}
      <rect x="96" y="362" width="208" height="56" rx="14" stroke={A} />
      <path d="M120 390l10 10 20-22" stroke={A} strokeWidth="2.5" />
      {lines(168, 390, [100])}
    </Frame>
  ),
  modes: (
    <Frame>
      {[0, 1, 2].map(i => (
        <g key={i}>
          <rect x={86 + i * 82} y="130" width="64" height="300" rx="12" fill={i === 1 ? 'rgba(57,135,229,0.10)' : F} stroke={i === 1 ? A : S} />
          <circle cx={118 + i * 82} cy={170} r="12" stroke={i === 1 ? A : S} />
          {lines(100 + i * 82, 220, [36, 28, 36, 22], 26)}
        </g>
      ))}
      <path d="M118 460h164" />
      <path d="M200 430v30" stroke={A} />
    </Frame>
  ),
  evidence: (
    <Frame>
      <rect x="90" y="120" width="220" height="330" rx="14" fill={F} />
      {lines(114, 156, [170, 150, 172])}
      <rect x="106" y="222" width="188" height="44" rx="8" fill="rgba(57,135,229,0.14)" stroke={A} />
