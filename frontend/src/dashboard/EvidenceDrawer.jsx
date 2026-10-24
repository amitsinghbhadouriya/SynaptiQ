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
    const onKey = event => event.key === 'Escape' && onClose();
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [onClose]);

  if (!result) return null;
  const retriever = result.modes.retriever;
  // Portal to <body>: animated ancestors would otherwise become the containing block of this fixed overlay.
  return createPortal(
    <div className="ev-backdrop" onClick={onClose}>
      <aside
        className="ev-drawer"
        role="dialog"
        aria-modal="true"
        aria-labelledby="ev-title"
        onClick={event => event.stopPropagation()}
      >
        <header className="ev-drawer__head">
          <div className="ev-drawer__tags">
            <Badge tone="neutral">{TYPE_LABEL[result.type] || result.type}</Badge>
            <DiagnosisBadge code={result.diagnosis} label={result.diagnosis_label} />
          </div>
          <button type="button" className="ev-close" onClick={onClose} aria-label="Close">
            <X size={18} />
          </button>
        </header>
        <h2 id="ev-title" className="ev-question">
          {result.question}
        </h2>

        <section className="ev-section ev-diagnosis">
          <h3>Why this diagnosis</h3>
          <p>{result.diagnosis_reason}</p>
          {result.notes?.length > 0 && (
            <ul className="ev-notes">
              {result.notes.map(note => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          )}
          {result.recommendation && (
            <div className="ev-rec">
              <Lightbulb size={15} aria-hidden="true" />
              <div>
                <b>{result.recommendation.title}</b>
                <span>{result.recommendation.why}</span>
              </div>
              {onRunCandidate && (
                <Button variant="primary" theme={theme} size="sm" onClick={() => onRunCandidate(runId)}>
                  Test run’s top fix
                </Button>
              )}
            </div>
          )}
        </section>

        <section className="ev-section">
