import { useState } from 'react';
import { Activity, BarChart3, Clock, Filter, Info, PieChart, Target, Trophy } from 'lucide-react';

import { ms, num, pct, runName } from '../format.js';
import { Card, CountUp, Delta, Empty, Progress, Segmented, PlotlyChart } from '../widgets.jsx';

const DONUT_COLORS = {
  LIKELY_RETRIEVAL_FAILURE: 'var(--d-series-1)',
  LIKELY_GENERATION_FAILURE: 'var(--d-series-2)',
  LIKELY_COMBINED_FAILURE: 'var(--d-series-3)',
  PIPELINE_INTERACTION_FAILURE: 'var(--d-series-4)',
  CORRECT_BUT_UNGROUNDED: 'var(--d-series-5)',
  UNCERTAIN_REQUIRES_REVIEW: 'var(--d-neutral)'
};
const FUNNEL_SHADES = ['var(--d-ord-1)', 'var(--d-ord-2)', 'var(--d-ord-3)', 'var(--d-ord-4)'];

function KpiTile({ icon: Icon, label, value, format, delta, deltaSuffix, invert, highlight }) {
  return (
    <div className={`an-kpi${highlight ? ' an-kpi--hl' : ''}`}>
      <div className="an-kpi__top">
        <span className="an-kpi__icon">
          <Icon size={14} strokeWidth={2.1} aria-hidden="true" />
        </span>
        <Delta value={delta} suffix={deltaSuffix} invert={invert} digits={deltaSuffix === ' ms' ? 0 : 1} />
      </div>
      <div className="an-kpi__value">
        <CountUp value={value} format={format} />
      </div>
      <div className="an-kpi__label">{label}</div>
      {highlight && <span className="an-kpi__swoosh" aria-hidden="true" />}
    </div>
  );
}

export default function Analytics({ data, selected, previous, theme }) {
  const [metric, setMetric] = useState('pass_rate');
  if (!selected) {
    return (
      <div className="d-page">
        <div className="d-page__head">
          <div>
            <h1>Analytics</h1>
            <p>How your RAG pipeline is performing across runs.</p>
          </div>
        </div>
        <Card>
          <Empty icon={BarChart3} title="Run an evaluation to see analytics" />
        </Card>
      </div>
    );
  }

  const h = selected.headline || {};
  const p = previous?.headline || {};
  const diff = (a, b, scale = 100) => (a !== null && a !== undefined && b !== null && b !== undefined ? (a - b) * scale : null);
  const diagnoses = Object.entries(selected.diagnoses || {}).filter(([code, n]) => code !== 'PASS' && n > 0);
