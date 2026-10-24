import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { flushSync } from 'react-dom';
import { CircleAlert, CircleCheck, Info, LoaderCircle, Play, Sparkles, TriangleAlert, X } from 'lucide-react';

import TopBar from './TopBar.jsx';
import Analytics from './tabs/Analytics.jsx';
import Documents from './tabs/Documents.jsx';
import Evaluations from './tabs/Evaluations.jsx';
import Overview from './tabs/Overview.jsx';
import Reports from './tabs/Reports.jsx';
import { Button } from './widgets.jsx';
import './dashboard.css';

const TOAST_ICON = { success: CircleCheck, error: CircleAlert, warning: TriangleAlert, info: Info };

const params = new URLSearchParams(window.location.search);
const TAB_IDS = ['overview', 'documents', 'evaluations', 'analytics', 'reports'];

function readStoredTheme() {
  const requested = params.get('theme');
  if (requested === 'dark' || requested === 'light') return requested;
  try {
    return localStorage.getItem('synaptiq-theme') === 'dark' ? 'dark' : 'light';
  } catch {
    return 'light';
  }
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(',')[1] || '');
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

// ---------------------------------------------------------------- dialogs
function Field({ label, hint, children }) {
  return (
    <label className="d-field">
      <span className="d-field__label">{label}</span>
      {children}
      {hint && <span className="d-field__hint">{hint}</span>}
    </label>
  );
}

function RunDialog({ data, documentId, selected, theme, onClose, onSubmit }) {
  const base = selected?.config || data.defaults.config;
  const eligible = data.documents.filter(d => d.questions > 0);
  const [form, setForm] = useState({
    document_id: eligible.find(d => d.document_id === documentId)?.document_id || eligible[0]?.document_id || '',
    chunk_size: base.chunk_size,
    chunk_overlap: base.chunk_overlap,
    top_k: base.top_k,
    embedding_model: data.defaults.config.embedding_model,
    max_answer_sentences: base.max_answer_sentences,
    abstain_threshold: base.abstain_threshold,
    prompt_version: base.prompt_version,
    label: ''
  });
  const [modes, setModes] = useState({ retriever: true, generator: true, end_to_end: true });
  const offline = data.status?.llm?.provider !== 'anthropic';
  const set = key => event => setForm({ ...form, [key]: event.target.value });
  const submit = event => {
    event.preventDefault();
    onSubmit({
      document_id: form.document_id,
      label: form.label,
      modes: Object.keys(modes).filter(m => modes[m]),
      config: {
        chunk_size: Number(form.chunk_size),
        chunk_overlap: Number(form.chunk_overlap),
        top_k: Number(form.top_k),
        embedding_model: form.embedding_model,
        max_answer_sentences: Number(form.max_answer_sentences),
        abstain_threshold: Number(form.abstain_threshold),
        prompt_version: form.prompt_version,
        label: form.label
      }
    });
  };
  return (
    <div className="d-modal" role="dialog" aria-modal="true" aria-labelledby="run-title">
      <form className="d-modal__panel" onSubmit={submit}>
        <header className="d-modal__head">
          <h2 id="run-title">Run evaluation</h2>
          <button type="button" className="ev-close" onClick={onClose} aria-label="Close">
            <X size={18} />
          </button>
        </header>
        {!eligible.length ? (
          <p className="d-muted">No document has test questions yet. Generate a test set first.</p>
        ) : (
          <>
            <div className="d-form-grid">
              <Field label="Document">
                <select value={form.document_id} onChange={set('document_id')}>
                  {eligible.map(d => (
                    <option key={d.document_id} value={d.document_id}>
                      {d.filename} ({d.questions} questions)
                    </option>
                  ))}
                </select>
              </Field>
              <Field label="Run label" hint="Optional, e.g. “top-k 4”">
                <input value={form.label} onChange={set('label')} maxLength={80} placeholder="Baseline" />
              </Field>
              <Field label="Chunk size" hint="characters">
                <input type="number" min={100} max={4000} step={20} value={form.chunk_size} onChange={set('chunk_size')} />
              </Field>
              <Field label="Chunk overlap" hint="characters">
                <input type="number" min={0} max={1000} step={10} value={form.chunk_overlap} onChange={set('chunk_overlap')} />
              </Field>
              <Field label="Top-k">
                <input type="number" min={1} max={20} value={form.top_k} onChange={set('top_k')} />
              </Field>
              <Field label="Embedding model" hint="Downloaded on first use">
                <select value={form.embedding_model} onChange={set('embedding_model')}>
