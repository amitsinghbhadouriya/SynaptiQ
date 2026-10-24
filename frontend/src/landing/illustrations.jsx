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
