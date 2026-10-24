export const pct = (value, digits = 0) =>
  value === null || value === undefined || Number.isNaN(value) ? '—' : `${(value * 100).toFixed(digits)}%`;

export const num = (value, digits = 2) =>
  value === null || value === undefined || Number.isNaN(value) ? '—' : Number(value).toFixed(digits);

export const ms = value => (value === null || value === undefined ? '—' : value >= 1000 ? `${(value / 1000).toFixed(1)} s` : `${Math.round(value)} ms`);

export const usd = value => (value === null || value === undefined ? 'not measured' : `$${Number(value).toFixed(4)}`);

export function ago(iso) {
  if (!iso) return '—';
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return iso;
  const seconds = Math.max(0, (Date.now() - then) / 1000);
  if (seconds < 60) return 'just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  if (seconds < 86400 * 7) return `${Math.floor(seconds / 86400)}d ago`;
  return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

export const stamp = iso =>
  iso ? new Date(iso).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—';

export const DIAGNOSIS_TONE = {
  PASS: 'good',
  LIKELY_RETRIEVAL_FAILURE: 'bad',
  LIKELY_GENERATION_FAILURE: 'bad',
  LIKELY_COMBINED_FAILURE: 'bad',
  PIPELINE_INTERACTION_FAILURE: 'warn',
  CORRECT_BUT_UNGROUNDED: 'warn',
  UNCERTAIN_REQUIRES_REVIEW: 'neutral'
};

export const TYPE_LABEL = { factual: 'Factual', numerical: 'Numerical', multi_hop: 'Multi-hop', unanswerable: 'Unanswerable' };

export const runName = run => (run ? run.label || run.config_short : '—');
