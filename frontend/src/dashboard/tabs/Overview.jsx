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
