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
