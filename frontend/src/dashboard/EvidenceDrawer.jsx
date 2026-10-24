import { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { CircleCheck, CircleX, Lightbulb, X } from 'lucide-react';

import { ms, num, pct, TYPE_LABEL } from './format.js';
import { Badge, Button, DiagnosisBadge } from './widgets.jsx';

function Metric({ label, value, format = num }) {
  return (
    <div className="ev-metric">
      <span>{label}</span>
      <b>{value === null || value === undefined ? '—' : format(value)}</b>
    </div>
  );
}

function Verdict({ passed }) {
  if (passed === null || passed === undefined) return <Badge tone="neutral">not measured</Badge>;
  return passed ? (
    <Badge tone="good" icon={CircleCheck}>
      pass
    </Badge>
  ) : (
    <Badge tone="bad" icon={CircleX}>
      fail
    </Badge>
  );
}

function AnswerBlock({ title, mode }) {
  if (!mode) return null;
  return (
    <section className="ev-section">
      <header className="ev-section__head">
        <h3>{title}</h3>
        <Verdict passed={mode.passed} />
      </header>
      {mode.error ? (
        <p className="ev-error">{mode.error}</p>
      ) : (
        <>
          <p className="ev-answer">{mode.answer}</p>
          <div className="ev-metrics">
            <Metric label="Correctness" value={mode.metrics?.answer_correctness} />
            <Metric label="Faithfulness" value={mode.metrics?.faithfulness} />
            <Metric label="Relevancy" value={mode.metrics?.answer_relevancy} />
            <Metric label="Ragas similarity" value={mode.metrics?.ragas_string_similarity} />
            <Metric label="Latency" value={mode.latency_ms} format={ms} />
          </div>
        </>
      )}
    </section>
  );
}

export default function EvidenceDrawer({ result, onClose, theme, onRunCandidate, runId }) {
  useEffect(() => {
