import { useState } from 'react';
import { Check, CircleCheck, CircleX, FlaskConical, ListChecks, Play, Search, Sparkles, X } from 'lucide-react';

import EvidenceDrawer from '../EvidenceDrawer.jsx';
import { ms, num, runName, TYPE_LABEL } from '../format.js';
import { Badge, Button, Card, CountUp, DiagnosisBadge, Empty, FilterPills, Segmented } from '../widgets.jsx';

function RunSelect({ runs, value, onChange }) {
  return (
    <label className="d-select">
      <span className="sq-visually-hidden">Selected run</span>
      <select value={value || ''} onChange={e => onChange(e.target.value)}>
        {runs.map(run => (
          <option key={run.run_id} value={run.run_id}>
            {runName(run)} — {run.filename}
          </option>
        ))}
      </select>
    </label>
  );
}

function HitCell({ mode }) {
  const hit = mode?.metrics?.hit_at_k;
  if (hit === null || hit === undefined) return <span className="d-muted">n/a</span>;
  const rank = mode.metrics.first_relevant_rank;
  return (
    <span className={`d-hit ${hit ? 'is-hit' : 'is-miss'}`}>
      {hit ? <CircleCheck size={14} aria-hidden="true" /> : <CircleX size={14} aria-hidden="true" />}
      {rank ? `#${rank}` : 'none'}
    </span>
  );
}

function Results({ data, selected, theme, act }) {
  const [filter, setFilter] = useState('all');
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(null);
  const results = data.results;
  const counts = {};
  results.forEach(r => {
    counts[r.diagnosis] = (counts[r.diagnosis] || 0) + 1;
  });
  const filters = [{ value: 'all', label: 'All', count: results.length }].concat(
    Object.entries(counts).map(([code, count]) => ({ value: code, label: data.labels[code], count }))
  );
  const shown = results.filter(
    r => (filter === 'all' || r.diagnosis === filter) && r.question.toLowerCase().includes(query.toLowerCase())
  );
  const retrievalFails = (counts.LIKELY_RETRIEVAL_FAILURE || 0) + (counts.LIKELY_COMBINED_FAILURE || 0) + (counts.CORRECT_BUT_UNGROUNDED || 0);
  const generationFails = (counts.LIKELY_GENERATION_FAILURE || 0) + (counts.PIPELINE_INTERACTION_FAILURE || 0);

  return (
    <>
      <div className="d-kpis d-kpis--compact">
        <div className="d-kpi">
          <div className="d-kpi__head">Questions</div>
          <div className="d-kpi__value"><CountUp value={results.length} /></div>
          <div className="d-kpi__note">{selected.review?.approved ?? 0} approved · {selected.review?.pending ?? 0} pending review</div>
        </div>
        <div className="d-kpi">
          <div className="d-kpi__head">Passed</div>
          <div className="d-kpi__value"><CountUp value={counts.PASS || 0} /></div>
          <div className="d-kpi__note">all three checks passed</div>
        </div>
        <div className="d-kpi">
          <div className="d-kpi__head">Retrieval-side failures</div>
          <div className="d-kpi__value"><CountUp value={retrievalFails} /></div>
          <div className="d-kpi__note">retrieval, combined, ungrounded</div>
        </div>
        <div className="d-kpi">
          <div className="d-kpi__head">Generation-side failures</div>
          <div className="d-kpi__value"><CountUp value={generationFails} /></div>
          <div className="d-kpi__note">generation, pipeline interaction</div>
        </div>
      </div>

      <Card
        title="Per-question results"
        icon={ListChecks}
        actions={
          <label className="d-search d-search--sm">
            <Search size={14} aria-hidden="true" />
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search questions" aria-label="Search questions" />
          </label>
        }
      >
        <FilterPills label="Filter by diagnosis" value={filter} onChange={setFilter} options={filters} />
        <div className="d-table-wrap">
          <table className="d-table d-table--click">
            <thead>
              <tr>
                <th>Question</th>
                <th>Type</th>
                <th>Hit@k</th>
                <th className="num">Recall</th>
                <th className="num">Gen-only</th>
                <th className="num">E2E correct</th>
                <th className="num">Faithful</th>
                <th>Diagnosis</th>
                <th className="num">Latency</th>
              </tr>
            </thead>
            <tbody>
              {shown.map(r => (
                <tr key={r.question_id} onClick={() => setOpen(r)} tabIndex={0} onKeyDown={e => e.key === 'Enter' && setOpen(r)}>
                  <td className="d-q">{r.question}</td>
                  <td><Badge tone="neutral">{TYPE_LABEL[r.type] || r.type}</Badge></td>
                  <td><HitCell mode={r.modes.retriever} /></td>
                  <td className="num">{num(r.modes.retriever?.metrics?.context_recall)}</td>
                  <td className="num">{num(r.modes.generator?.metrics?.answer_correctness)}</td>
                  <td className="num">{num(r.modes.end_to_end?.metrics?.answer_correctness)}</td>
                  <td className="num">{num(r.modes.end_to_end?.metrics?.faithfulness)}</td>
                  <td><DiagnosisBadge code={r.diagnosis} label={r.diagnosis_label} /></td>
                  <td className="num">{ms(r.modes.end_to_end?.latency_ms)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="d-footnote">
          Pass thresholds: evidence coverage ≥ 50% for hit@k, correctness ≥ 0.60 and faithfulness ≥ 0.60 for answers.
          Unanswerable questions pass when the system declines. Click a row to inspect the evidence.
        </p>
      </Card>

      <EvidenceDrawer
        result={open}
        onClose={() => setOpen(null)}
        theme={theme}
        runId={selected.run_id}
        onRunCandidate={selected.top_recommendation ? id => { setOpen(null); act.runCandidate(id); } : null}
      />
    </>
