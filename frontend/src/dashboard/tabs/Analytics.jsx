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
  const failingTotal = diagnoses.reduce((s, [, n]) => s + n, 0);
  const funnelMax = Math.max(1, ...data.funnel.map(f => f.value));
  const leaderboard = data.runs
    .filter(r => r.status === 'completed' && r.document_id === selected.document_id)
    .sort((a, b) => (b.pass_rate ?? 0) - (a.pass_rate ?? 0))
    .slice(0, 5);

  return (
    <div className="d-page">
      <div className="d-page__head">
        <div>
          <h1>
            Analytics <Info size={15} className="d-title-info" aria-label="Means ignore unmeasured values" />
          </h1>
          <p>
            {runName(selected)} on {selected.filename}
            {previous ? ` · deltas vs ${runName(previous)}` : ' · no earlier run to compare yet'}
          </p>
        </div>
      </div>

      <div className="an-kpis">
        <KpiTile icon={Target} label="Context recall" value={h.context_recall} format={v => v.toFixed(2)} delta={diff(h.context_recall, p.context_recall)} deltaSuffix=" pts" highlight />
        <KpiTile icon={Activity} label="Faithfulness (end-to-end)" value={h.faithfulness} format={v => v.toFixed(2)} delta={diff(h.faithfulness, p.faithfulness)} deltaSuffix=" pts" />
        <KpiTile icon={Trophy} label="Answer correctness (end-to-end)" value={h.answer_correctness} format={v => v.toFixed(2)} delta={diff(h.answer_correctness, p.answer_correctness)} deltaSuffix=" pts" />
        <KpiTile icon={Clock} label="Avg end-to-end latency" value={h.latency_ms_avg} format={v => ms(v)} delta={diff(h.latency_ms_avg, p.latency_ms_avg, 1)} deltaSuffix=" ms" invert />
      </div>

      <div className="an-grid an-grid--2">
        <Card
          title="Score trend"
          icon={BarChart3}
          actions={
            <Segmented
              size="sm"
              label="Metric"
              value={metric}
              onChange={setMetric}
              options={[
                { value: 'pass_rate', label: 'Pass rate' },
                { value: 'hit_at_k', label: 'Hit@k' },
                { value: 'faithfulness', label: 'Faithful' },
                { value: 'answer_correctness', label: 'Correct' }
              ]}
            />
          }
        >
          <PlotlyChart figure={data.charts.trend?.[metric]} theme={theme} height={250} />
        </Card>
        <Card title="Pass rate by test mode" icon={Activity}>
          <PlotlyChart figure={data.charts.modes} theme={theme} height={250} />
        </Card>
      </div>

      <div className="an-grid an-grid--3">
        <Card title="Failure sources" icon={PieChart}>
