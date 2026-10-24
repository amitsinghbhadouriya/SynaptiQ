import { useState } from 'react';
import { createPortal } from 'react-dom';
import { Database, FileText, FileUp, FlaskConical, Layers, LayoutGrid, Play, Search, Sparkles, Table2, Trash2 } from 'lucide-react';

import { ago, pct } from '../format.js';
import { Badge, Button, Card, CountUp, Empty, FilterPills, IconButton, Segmented } from '../widgets.jsx';

const TYPE_TONE = { PDF: 'bad', DOCX: 'accent', TXT: 'neutral' };

function Kpi({ icon: Icon, label, value, note }) {
  return (
    <div className="d-kpi">
      <div className="d-kpi__head">
        <span className="d-kpi__icon">
          <Icon size={14} strokeWidth={2} aria-hidden="true" />
        </span>
        {label}
      </div>
      <div className="d-kpi__value">
        <CountUp value={value} />
      </div>
      <div className="d-kpi__note">{note}</div>
    </div>
  );
}

function FileAvatar({ type }) {
  return <span className={`d-file d-file--${type.toLowerCase()}`}>{type}</span>;
}

export default function Documents({ data, theme, act }) {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const [view, setView] = useState('table');
  const [confirm, setConfirm] = useState(null);
  const docs = data.documents;
  const counts = { all: docs.length, PDF: 0, DOCX: 0, TXT: 0 };
  docs.forEach(d => {
    counts[d.file_type] = (counts[d.file_type] || 0) + 1;
  });
  const shown = docs.filter(
    d => (filter === 'all' || d.file_type === filter) && d.filename.toLowerCase().includes(query.toLowerCase())
  );
  const totals = docs.reduce(
    (acc, d) => ({ chunks: acc.chunks + (d.chunks || 0), questions: acc.questions + d.questions, runs: acc.runs + d.runs }),
    { chunks: 0, questions: 0, runs: 0 }
  );

  const actions = doc => (
    <div className="d-row-actions">
      <IconButton icon={Sparkles} label="Generate test questions" onClick={() => act.generate(doc.document_id)} />
      <IconButton icon={Play} label="Run evaluation" onClick={() => act.configure(doc.document_id)} disabled={!doc.questions} />
      <IconButton icon={Trash2} label="Delete document" onClick={() => setConfirm(doc)} />
    </div>
  );

  return (
    <div className="d-page">
      <div className="d-page__head">
        <div>
          <h1>Documents</h1>
          <p>Everything SynaptiQ has indexed — source files, chunks and their test sets.</p>
        </div>
        <div className="d-page__tools">
          <label className="d-search">
            <Search size={14} aria-hidden="true" />
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search documents" aria-label="Search documents" />
          </label>
          <Segmented
            label="Layout"
            value={view}
            onChange={setView}
            options={[
              { value: 'table', icon: Table2, label: 'Table' },
              { value: 'cards', icon: LayoutGrid, label: 'Cards' }
            ]}
          />
          <Button variant="primary" theme={theme} icon={FileUp} onClick={act.upload}>
            Add document
          </Button>
        </div>
      </div>

      <div className="d-kpis">
        <Kpi icon={FileText} label="Documents" value={docs.length} note="PDF, DOCX and TXT" />
        <Kpi icon={Layers} label="Chunks indexed" value={totals.chunks} note="at the default chunk settings" />
        <Kpi icon={FlaskConical} label="Test questions" value={totals.questions} note="excluding rejected questions" />
        <Kpi icon={Database} label="Evaluation runs" value={totals.runs} note="stored in SQLite history" />
      </div>

      <Card
        title="All documents"
        icon={FileText}
        actions={
          <FilterPills
            label="Filter by type"
            value={filter}
            onChange={setFilter}
            options={[
              { value: 'all', label: 'All', count: counts.all },
              { value: 'PDF', label: 'PDF', count: counts.PDF },
              { value: 'DOCX', label: 'DOCX', count: counts.DOCX },
              { value: 'TXT', label: 'TXT', count: counts.TXT }
            ]}
          />
        }
      >
        {!docs.length ? (
          <Empty
            icon={FileUp}
            title="No documents yet"
            actions={
              <>
                <Button variant="primary" theme={theme} icon={FileUp} onClick={act.upload}>
                  Upload document
                </Button>
                <Button variant="ghost" theme={theme} icon={Sparkles} onClick={act.demo}>
                  Load demo workspace
                </Button>
              </>
            }
          >
            Upload a PDF, DOCX or TXT file (up to {data.status?.limits?.max_upload_mb ?? 20} MB). Scanned PDFs need OCR, which is
            outside the current scope.
          </Empty>
        ) : view === 'table' ? (
          <div className="d-table-wrap">
            <table className="d-table">
              <thead>
                <tr>
                  <th>Document</th>
                  <th>Type</th>
                  <th className="num">Sections</th>
                  <th className="num">Chunks</th>
                  <th>Test set</th>
                  <th className="num">Runs</th>
                  <th className="num">Last pass rate</th>
                  <th>Added</th>
                  <th aria-label="Actions" />
                </tr>
              </thead>
              <tbody>
                {shown.map(doc => (
                  <tr key={doc.document_id}>
                    <td>
                      <span className="d-doc">
                        <FileAvatar type={doc.file_type} />
                        <span>
                          <span className="d-cell-strong">{doc.filename}</span>
                          <span className="d-cell-sub">sha256 {doc.hash}…</span>
                        </span>
                      </span>
                    </td>
                    <td>
                      <Badge tone={TYPE_TONE[doc.file_type]}>{doc.file_type}</Badge>
                    </td>
