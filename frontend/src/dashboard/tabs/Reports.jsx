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
                </select>
              </label>
              <label>
                <span>Candidate</span>
                <select value={candidate} onChange={e => setCandidate(e.target.value)}>
                  {runs.map(run => (
                    <option key={run.run_id} value={run.run_id}>
                      {runName(run)} · {stamp(run.created_at)}
                    </option>
                  ))}
                </select>
              </label>
              <Button
                variant="primary"
                theme={theme}
                icon={GitCompareArrows}
                disabled={!baseline || !candidate || baseline === candidate}
                onClick={() => act.compare(baseline, candidate)}
              >
                Compare
              </Button>
            </div>

            {comparison && (
              <div className="rp-result">
                {comparison.warnings?.length > 0 && (
                  <ul className="rp-warnings">
                    {comparison.warnings.map(w => (
                      <li key={w}>
                        <TriangleAlert size={14} aria-hidden="true" /> {w}
                      </li>
                    ))}
                  </ul>
                )}
                <div className="rp-changes">
                  <span className="d-muted">Changed settings:</span>
                  {Object.keys(comparison.config_changes || {}).length ? (
                    Object.entries(comparison.config_changes).map(([key, change]) => (
                      <Badge key={key} tone="accent">
                        {key}: {String(change.baseline)} → {String(change.candidate)}
                      </Badge>
                    ))
                  ) : (
                    <Badge tone="neutral">none</Badge>
                  )}
                  <span className="d-muted">· {comparison.sample_size} shared questions</span>
                </div>
                <div className="rp-grid">
                  <div className="d-table-wrap">
                    <table className="d-table">
                      <thead>
                        <tr>
                          <th>Metric</th>
                          <th className="num">Baseline</th>
                          <th className="num">Candidate</th>
                          <th className="num">Change</th>
                        </tr>
                      </thead>
                      <tbody>
                        {comparison.metrics.map(row => (
                          <tr key={`${row.metric}`}>
                            <td>{row.metric}</td>
                            <td className="num">{fmt(row.key, row.baseline)}</td>
                            <td className="num">{fmt(row.key, row.candidate)}</td>
                            <td className={`num rp-delta rp-delta--${better(row)}`}>
                              {row.delta === null || row.delta === undefined
                                ? '—'
                                : `${row.delta > 0 ? '+' : ''}${fmt(row.key, row.delta)}`}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <div>
                    <PlotlyChart figure={data.charts.comparison} theme={theme} height={300} />
                    <div className="rp-questions">
                      <Badge tone="good">{comparison.questions.fixed.length} fixed</Badge>
                      <Badge tone="bad">{comparison.questions.regressed.length} regressed</Badge>
                      <Badge tone="neutral">{comparison.questions.still_failing.length} still failing</Badge>
                      <Badge tone="neutral">{comparison.questions.still_passing} still passing</Badge>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </Card>

      <Card title="Run history" icon={History}>
        {runs.length ? (
          <div className="d-table-wrap">
            <table className="d-table d-table--click">
              <thead>
                <tr>
                  <th>Run</th>
                  <th>Document</th>
                  <th>Configuration</th>
                  <th>Embeddings</th>
                  <th className="num">Questions</th>
                  <th className="num">Pass rate</th>
                  <th className="num">Duration</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {data.runs.map(run => (
                  <tr
                    key={run.run_id}
                    className={run.run_id === selected?.run_id ? 'is-selected' : ''}
                    onClick={() => run.status === 'completed' && act.selectRun(run.run_id)}
                  >
                    <td>
                      <span className="d-cell-strong">{runName(run)}</span>
                      <span className="d-cell-sub">{run.run_id}</span>
                    </td>
                    <td className="d-muted">{run.filename}</td>
                    <td className="d-muted">{run.config_short}</td>
                    <td className="d-muted">{run.config.embedding_backend}</td>
                    <td className="num">{run.questions ?? '—'}</td>
                    <td className="num">{run.status === 'completed' ? pct(run.pass_rate) : <Badge tone="bad">{run.status}</Badge>}</td>
                    <td className="num">{ms(run.duration_ms)}</td>
                    <td className="d-muted">{stamp(run.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty icon={FileBarChart} title="No runs recorded yet" />
        )}
      </Card>
    </div>
  );
}
