// Authentic vector symbols and cards for technologies in the stack.

const esc = value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const wrapName = name => {
  if (name.length <= 12) return [name];
  const words = name.split(' ');
  if (words.length < 2) return [name];
  return [words.slice(0, -1).join(' '), words[words.length - 1]];
};

// Precise vector symbols for each technology
export const TECH_SYMBOLS = {
  Python: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <path d="M11.914 2c-3.102 0-5.18.39-5.18 2.072v1.85h5.18v.518H4.49c-1.79 0-2.49 1.6-2.49 4.533 0 3.03.882 4.542 2.68 4.542h1.565v-2.138c0-2.073 1.8-3.903 3.88-3.903h5.18V8.625c0-1.682-2.078-2.072-5.18-2.072h1.788c.6 0 1.07-.47 1.07-1.07s-.47-1.07-1.07-1.07H11.914zm-2.07 1.554c.432 0 .777.345.777.777s-.345.777-.777.777c-.432 0-.777-.345-.777-.777s.345-.777.777-.777z" fill="#387eb8"/>
      <path d="M12.086 22c3.102 0 5.18-.39 5.18-2.072v-1.85h-5.18v-.518h7.424c1.79 0 2.49-1.6 2.49-4.533 0-3.03-.882-4.542-2.68-4.542h-1.565v2.138c0 2.073-1.8 3.903-3.88 3.903H8.695v.85c0 1.682 2.078 2.072 5.18 2.072h-1.788c-.6 0-1.07.47-1.07 1.07s.47 1.07 1.07 1.07h1.07zm2.07-1.554c-.432 0-.777-.345-.777-.777s.345-.777.777-.777c.432 0 .777.345.777.777s-.345.777-.777.777z" fill="#ffe052"/>
    </svg>
  </g>`,

  Streamlit: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 32 32" fill="none">
      <path d="M16 5l-7 12 4.5 7 2.5-2 2.5 2 4.5-7-7-12z" fill="#FF4B4B"/>
      <path d="M9 17l-6 5.5 10 1.5-4-7z" fill="#FF2B2B"/>
      <path d="M23 17l6 5.5-10 1.5 4-7z" fill="#FF6B6B"/>
    </svg>
  </g>`,

  FastAPI: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="11" fill="#009688"/>
      <path d="M13 3.5L5.5 13H11.5L9.5 20.5L18.5 10.5H12.5L14.5 3.5H13Z" fill="#ffffff"/>
    </svg>
  </g>`,

  PyMuPDF: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <rect x="3" y="2" width="14" height="20" rx="2.5" fill="#ef4444" fill-opacity="0.15" stroke="#ef4444" stroke-width="1.6"/>
      <path d="M13 2v5h5" stroke="#ef4444" stroke-width="1.6" stroke-linecap="round"/>
      <path d="M7 11h6M7 14.5h4" stroke="#ff6b6b" stroke-width="1.5" stroke-linecap="round"/>
      <rect x="5" y="17" width="10" height="4" rx="1" fill="#ef4444"/>
      <text x="10" y="20.2" text-anchor="middle" font-family="Space Grotesk, sans-serif" font-size="3.5" font-weight="700" fill="#ffffff">PDF</text>
    </svg>
  </g>`,

  'python-docx': `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <rect x="4" y="2" width="16" height="20" rx="2.5" fill="#185abd" fill-opacity="0.16" stroke="#3b82f6" stroke-width="1.6"/>
      <rect x="2" y="7" width="10" height="10" rx="1.5" fill="#185abd" stroke="#60a5fa" stroke-width="1.2"/>
      <path d="M4 10l1 4 1.2-3 1.2 3 1-4" stroke="#ffffff" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M14 8h4M14 12h4M14 16h3" stroke="#93c5fd" stroke-width="1.4" stroke-linecap="round"/>
    </svg>
  </g>`,

  'Sentence Transformers': `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" fill="#ffd21e" fill-opacity="0.15" stroke="#ffd21e" stroke-width="1.5"/>
      <circle cx="8.5" cy="10" r="1.5" fill="#ffd21e"/>
      <circle cx="15.5" cy="10" r="1.5" fill="#ffd21e"/>
      <path d="M8 15s1.5 2.5 4 2.5 4-2.5 4-2.5" stroke="#ffd21e" stroke-width="1.8" stroke-linecap="round"/>
      <path d="M4.5 7.5L7 9.5M19.5 7.5L17 9.5" stroke="#38bdf8" stroke-width="1.6" stroke-linecap="round"/>
    </svg>
  </g>`,

  ChromaDB: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10.5" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
      <circle cx="12" cy="4.5" r="2.5" fill="#f43f5e"/>
      <circle cx="17.8" cy="7.2" r="2.5" fill="#fb923c"/>
      <circle cx="19.5" cy="13.2" r="2.5" fill="#facc15"/>
      <circle cx="15.8" cy="18.5" r="2.5" fill="#4ade80"/>
      <circle cx="9.2" cy="18.8" r="2.5" fill="#38bdf8"/>
      <circle cx="4.5" cy="14" r="2.5" fill="#818cf8"/>
      <circle cx="5.8" cy="7.8" r="2.5" fill="#c084fc"/>
    </svg>
  </g>`,

  Ragas: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" stroke="#a855f7" stroke-width="1.6" fill="#a855f7" fill-opacity="0.12"/>
      <circle cx="12" cy="12" r="6" stroke="#c084fc" stroke-width="1.4" stroke-dasharray="2 2"/>
      <circle cx="12" cy="12" r="2.5" fill="#a855f7"/>
      <path d="M12 2v4M12 18v4M2 12h4M18 12h4" stroke="#c084fc" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
  </g>`,

  Pandas: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <rect x="3.5" y="9" width="3.5" height="12" rx="1.2" fill="#38bdf8"/>
      <rect x="8.5" y="4" width="3.5" height="17" rx="1.2" fill="#ff4b4b"/>
      <rect x="13.5" y="11" width="3.5" height="10" rx="1.2" fill="#eab308"/>
      <rect x="18.5" y="6" width="3.5" height="15" rx="1.2" fill="#6366f1"/>
    </svg>
  </g>`,

  Plotly: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <rect x="3" y="13" width="4" height="8" rx="1.5" fill="#1f77b4" fill-opacity="0.6"/>
      <circle cx="5" cy="10" r="2" fill="#38bdf8"/>
      <rect x="10" y="7" width="4" height="14" rx="1.5" fill="#1f77b4"/>
      <circle cx="12" cy="4" r="2" fill="#38bdf8"/>
      <rect x="17" y="10" width="4" height="11" rx="1.5" fill="#1f77b4" fill-opacity="0.6"/>
      <circle cx="19" cy="7" r="2" fill="#38bdf8"/>
      <path d="M2 22h20" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
  </g>`,

  SQLite: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <path d="M4 6c0-2.2 3.6-4 8-4s8 1.8 8 4-3.6 4-8 4-8-1.8-8-4z" fill="#003b57" stroke="#0ea5e9" stroke-width="1.5"/>
      <path d="M4 6v5c0 2.2 3.6 4 8 4s8-1.8 8-4V6" stroke="#0ea5e9" stroke-width="1.5"/>
      <path d="M4 11v5c0 2.2 3.6 4 8 4s8-1.8 8-4v-5" stroke="#0ea5e9" stroke-width="1.5"/>
      <path d="M17 3c-4 5-8 10-6 16" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
    </svg>
  </g>`,

  Pytest: `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <path d="M9 3h6M10 3v5l-5.5 10.5C3.8 20 4.8 22 6.5 22h11c1.7 0 2.7-2 2-3.5L14 8V3" stroke="#0ea5e9" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M6.5 17h11l-2-4H8.5l-2 4z" fill="#0ea5e9" fill-opacity="0.25"/>
      <path d="M9 14l2 2 4-4" stroke="#10b981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </g>`,

  'Standard Python': `<g transform="translate(42, 42)">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
      <rect x="2" y="3" width="20" height="18" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.15)" stroke-width="1.5"/>
      <path d="M6 8l4 4-4 4M12 16h6" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </g>`
};

// Compact standalone icon for the list below the bounce cards
export function getTechIconSvg(name) {
  const fullSvg = TECH_SYMBOLS[name] || TECH_SYMBOLS['Standard Python'];
  // Extract the inner svg content and wrap in a clean 24x24 viewBox
  const match = fullSvg.match(/<svg[^>]*>([\s\S]*?)<\/svg>/);
  const inner = match ? match[1] : '';
  return `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">${inner}</svg>`;
}

export function techCard({ name, role, glyph }, index) {
  const lines = wrapName(name);
  const nameY = lines.length > 1 ? 206 : 226;
  const symbol = TECH_SYMBOLS[name] || `<text x="66" y="77" text-anchor="middle" font-family="Space Grotesk, Inter, Segoe UI, sans-serif" font-size="32" font-weight="600" fill="#e9eef8">${esc(glyph || name.slice(0, 2))}</text>`;

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#161922"/><stop offset="1" stop-color="#0d0f15"/></linearGradient>
    <pattern id="p" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#ffffff" stroke-opacity="0.035"/></pattern>
  </defs>
  <rect width="300" height="300" fill="url(#g)"/>
  <rect width="300" height="300" fill="url(#p)"/>
  <rect x="28" y="28" width="76" height="76" rx="18" fill="#3987e5" fill-opacity="0.12" stroke="#3987e5" stroke-opacity="0.55"/>
  ${symbol}
  <text x="272" y="52" text-anchor="end" font-family="ui-monospace, Consolas, monospace" font-size="15" fill="#7d8494">${String(index + 1).padStart(2, '0')}</text>
  ${lines
    .map(
      (line, i) =>
        `<text x="28" y="${nameY + i * 34}" font-family="Space Grotesk, Inter, Segoe UI, sans-serif" font-size="30" font-weight="600" fill="#eef0f5">${esc(line)}</text>`
    )
    .join('')}
  <text x="28" y="268" font-family="Inter, Segoe UI, sans-serif" font-size="17" fill="#9aa1b0">${esc(role)}</text>
</svg>`;
  return { src: `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`, alt: `${name} — ${role}` };
}
