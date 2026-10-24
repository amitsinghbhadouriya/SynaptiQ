import { useEffect, useState } from 'react';
import { Download, FileBarChart, GitCompareArrows, History, TriangleAlert } from 'lucide-react';

import { ms, num, pct, runName, stamp } from '../format.js';
import { Badge, Button, Card, Empty, PlotlyChart } from '../widgets.jsx';

const fmt = (key, value) => {
  if (value === null || value === undefined) return '—';
  if (key === 'latency_ms_avg') return ms(value);
  if (key === 'cost_total') return `$${Number(value).toFixed(4)}`;
  return num(value);
};

export default function Reports({ data, selected, theme, act }) {
  const runs = data.runs.filter(r => r.status === 'completed');
  const comparison = data.comparison && !data.comparison.error ? data.comparison : null;
  const [baseline, setBaseline] = useState(comparison?.baseline_run_id || runs[1]?.run_id || '');
  const [candidate, setCandidate] = useState(comparison?.candidate_run_id || runs[0]?.run_id || '');

  useEffect(() => {
    if (comparison) {
      setBaseline(comparison.baseline_run_id);
      setCandidate(comparison.candidate_run_id);
    }
  }, [comparison?.baseline_run_id, comparison?.candidate_run_id]);

  const better = (row) => {
    if (row.delta === null || row.delta === undefined || Math.abs(row.delta) < 1e-9) return 'flat';
    const invert = row.key === 'latency_ms_avg' || row.key === 'cost_total';
    return (row.delta > 0) !== invert ? 'up' : 'down';
  };

  return (
    <div className="d-page">
      <div className="d-page__head">
        <div>
          <h1>Reports</h1>
          <p>Before/after comparisons on the same test set, exports and the full run history.</p>
        </div>
        {selected && (
          <div className="d-page__tools">
            <Button variant="ghost" theme={theme} icon={Download} onClick={() => act.export(selected.run_id, 'csv')}>
              Export CSV
            </Button>
            <Button variant="ghost" theme={theme} icon={Download} onClick={() => act.export(selected.run_id, 'json')}>
              Export JSON
            </Button>
          </div>
        )}
      </div>

      <Card title="Compare two runs" icon={GitCompareArrows}>
        {runs.length < 2 ? (
          <Empty icon={GitCompareArrows} title="Two completed runs are needed">
            Run a candidate configuration (for example the recommended change) to compare it with the baseline.
          </Empty>
        ) : (
          <>
            <div className="rp-pick">
              <label>
                <span>Baseline</span>
                <select value={baseline} onChange={e => setBaseline(e.target.value)}>
                  {runs.map(run => (
                    <option key={run.run_id} value={run.run_id}>
                      {runName(run)} · {stamp(run.created_at)}
                    </option>
                  ))}
