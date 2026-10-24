import { useEffect, useMemo, useState } from 'react';
import {
  CircleCheck,
  CircleX,
  Download,
  Eye,
  EyeOff,
  FileUp,
  Gauge as GaugeIcon,
  Lightbulb,
  ListChecks,
  Play,
  Search,
  Server,
  Sparkles,
  Target
} from 'lucide-react';

import MagicBento from '../../components/reactbits/MagicBento.jsx';
import { ago, ms, num, pct, runName } from '../format.js';
import { Badge, Button, CountUp, Delta, Gauge, PlotlyChart, Progress } from '../widgets.jsx';

const FAILURE_COLORS = {
  LIKELY_RETRIEVAL_FAILURE: 'var(--d-series-1)',
  LIKELY_GENERATION_FAILURE: 'var(--d-series-2)',
  LIKELY_COMBINED_FAILURE: 'var(--d-series-3)',
  PIPELINE_INTERACTION_FAILURE: 'var(--d-series-4)',
  CORRECT_BUT_UNGROUNDED: 'var(--d-series-5)',
  UNCERTAIN_REQUIRES_REVIEW: 'var(--d-neutral)'
};

function Head({ icon: Icon, tone = 'plain', title, children }) {
  return (
    <div className="ov-head">
      <span className={`ov-icon ov-icon--${tone}`}>
        <Icon size={15} strokeWidth={2.1} aria-hidden="true" />
      </span>
      <span className="ov-head__title">{title}</span>
      {children && <span className="ov-head__extra">{children}</span>}
    </div>
  );
}

function PixelBars({ runs, selectedId }) {
  const columns = [...runs].reverse().slice(-8);
  return (
    <div className="ov-pixels" aria-hidden="true">
      {columns.map(run => {
        const filled = Math.round((run.pass_rate || 0) * 8);
        return (
          <span key={run.run_id} className={`ov-pixels__col${run.run_id === selectedId ? ' is-selected' : ''}`}>
            {Array.from({ length: 8 }, (_, i) => (
              <span key={i} className={`ov-pixels__cell${i < filled ? ' is-on' : ''}`} />
            ))}
          </span>
        );
      })}
    </div>
  );
}

function HeroCard({ selected, previous, runs, theme, act }) {
  const [hidden, setHidden] = useState(false);
  const delta = previous && selected ? (selected.pass_rate - previous.pass_rate) * 100 : null;
  return (
    <div className="ov-card ov-hero">
      <Head icon={GaugeIcon} title="Overall pass rate">
        <span className="ov-chip">{selected.filename}</span>
        <span className="ov-chip">{runName(selected)}</span>
      </Head>
      <div className="ov-hero__main">
        <div>
          <div className={`ov-big${hidden ? ' is-masked' : ''}`}>
            <CountUp value={(selected.pass_rate || 0) * 100} format={v => v.toFixed(1)} />
            <span className="ov-big__unit">%</span>
            <button type="button" className="ov-eye" onClick={() => setHidden(!hidden)} aria-label={hidden ? 'Show value' : 'Hide value'}>
              {hidden ? <EyeOff size={15} /> : <Eye size={15} />}
            </button>
          </div>
          <p className="ov-sub">
            <Delta value={delta} />
            <span>
              {selected.passed} of {selected.questions} questions passed every check
              {previous ? ` · vs ${runName(previous)}` : ''}
            </span>
          </p>
        </div>
        <PixelBars runs={runs} selectedId={selected.run_id} />
      </div>
      <div className="ov-actions">
        <Button variant="primary" theme={theme} size="sm" icon={FileUp} onClick={act.upload}>
          Upload document
        </Button>
        <Button variant="dark" theme={theme} size="sm" icon={Play} onClick={act.configure}>
          Run evaluation
        </Button>
        <Button variant="ghost" theme={theme} size="sm" icon={Sparkles} onClick={act.generate}>
          Generate tests
        </Button>
      </div>
    </div>
  );
}

function PassedCard({ selected, previous }) {
  const delta = previous ? selected.passed - previous.passed : null;
  return (
    <div className="ov-card">
      <Head icon={CircleCheck} tone="good" title="Passed" />
      <div className="ov-value">
        <CountUp value={selected.passed} />
        <span className="ov-value__of">/ {selected.questions}</span>
        {delta !== null && (
          <Badge tone={delta >= 0 ? 'good' : 'bad'}>
            {delta >= 0 ? '+' : ''}
            {delta}
          </Badge>
        )}
      </div>
      <p className="ov-note">Retrieval, generation and end-to-end all passed.</p>
      <div className="ov-split">
        <div>
          <span>Retriever-only</span>
          <strong>{pct(selected.modes?.retriever?.pass_rate)}</strong>
        </div>
        <div>
          <span>Generator-only</span>
          <strong>{pct(selected.modes?.generator?.pass_rate)}</strong>
        </div>
      </div>
    </div>
  );
}

function FailuresCard({ selected, previous, labels }) {
  const entries = Object.entries(selected.diagnoses || {}).filter(([code, n]) => code !== 'PASS' && n > 0);
  const failing = entries.reduce((sum, [, n]) => sum + n, 0);
  const prevFailing = previous ? previous.questions - previous.passed : null;
  return (
    <div className="ov-card">
      <Head icon={CircleX} tone="bad" title="Failing" />
      <div className="ov-value">
        <CountUp value={failing} />
        {prevFailing !== null && (
          <Badge tone={failing <= prevFailing ? 'good' : 'bad'}>
            {failing - prevFailing > 0 ? '+' : ''}
            {failing - prevFailing} vs prev
          </Badge>
        )}
      </div>
      {failing > 0 ? (
        <>
          <div className="ov-stack" role="img" aria-label="Failures by diagnosis">
            {entries.map(([code, n]) => (
              <span key={code} style={{ flexGrow: n, background: FAILURE_COLORS[code] }} title={`${labels[code]}: ${n}`} />
            ))}
          </div>
          <ul className="ov-legend">
            {entries.map(([code, n]) => (
              <li key={code}>
                <i style={{ background: FAILURE_COLORS[code] }} />
                {labels[code]} <b>{n}</b>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p className="ov-note">No failing questions in this run.</p>
      )}
    </div>
  );
}

function QualityCard({ selected }) {
  const h = selected.headline || {};
  const correctness = h.answer_correctness;
  const rows = [
    { label: 'Context recall', value: h.context_recall },
    { label: 'Faithfulness', value: h.faithfulness },
    { label: 'Answer relevancy', value: h.answer_relevancy },
    { label: 'Abstention correct', value: h.abstention_correct }
  ];
  return (
    <div className="ov-card ov-quality">
      <Head icon={Target} title="Quality target" />
      <div className="ov-quality__panel">
        <div className="ov-quality__top">
          <span>End-to-end correctness</span>
          <span className="ov-quality__target">Target 0.80</span>
        </div>
        <div className="ov-quality__gauge">
          <Gauge value={correctness} target={0.8} />
          <div className="ov-quality__value">
            <CountUp value={correctness} format={v => v.toFixed(2)} />
            <small>{correctness !== null && correctness !== undefined && correctness >= 0.8 ? 'on target' : 'below target'}</small>
          </div>
        </div>
      </div>
      <ul className="ov-metrics">
        {rows.map(row => (
          <li key={row.label}>
            <span>{row.label}</span>
            <span className="ov-metrics__num">{num(row.value)}</span>
            <Progress value={row.value} tone={row.value >= 0.8 ? 'good' : row.value >= 0.6 ? 'accent' : 'bad'} />
          </li>
        ))}
      </ul>
    </div>
  );
}

function ChartCard({ charts, theme, runs }) {
  return (
    <div className="ov-card ov-chartcard">
      <Head icon={ListChecks} title="Pass rate by run">
        <span className="ov-chip">last {Math.min(8, runs.length)} runs</span>
      </Head>
      {charts?.runs_bar ? <PlotlyChart figure={charts.runs_bar} theme={theme} height={150} /> : <p className="ov-note">No runs yet.</p>}
    </div>
  );
}

function RecommendationCard({ selected, theme, act }) {
  const rec = selected.top_recommendation;
  return (
    <div className="ov-card ov-rec">
      <div className="ov-rec__top">
        <Badge tone="accent">Diagnose → Recommend</Badge>
        <Lightbulb size={16} aria-hidden="true" className="ov-rec__bulb" />
      </div>
      {rec ? (
        <>
          <h3 className="ov-rec__title">{rec.title}</h3>
          <p className="ov-rec__why">{rec.why}</p>
          <div className="ov-rec__foot">
            <span className="ov-note">
              {rec.votes} of {rec.failing} failing
            </span>
