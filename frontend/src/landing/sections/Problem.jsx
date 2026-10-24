import { useState } from 'react';
import { Search, Sparkles, GitMerge, FileSpreadsheet, ArrowRight, AlertTriangle, CheckCircle } from 'lucide-react';

import ScrollReveal from '../../components/reactbits/ScrollReveal.jsx';
import { FAILURES } from '../content.js';
import { SectionHeading } from '../shared.jsx';

const FAILURE_METRICS = {
  retrieval: {
    icon: Search,
    color: '#0ea5e9',
    badge: 'Retriever Issue',
    query: 'What is the required token overlap for dense contracts?',
    retrieved: 'Chunk #4: "Standard NDA clauses define obligations..." (Score: 0.42 - Missing passage)',
    evidence: 'Chunk #12 (Unretrieved): "Dense contracts require 100-token chunk overlap."',
    output: '"Contracts typically rely on standard indemnification schedules."',
    diagnosis: 'LIKELY_RETRIEVAL_FAILURE',
    fix: 'Increase top-k from 3 to 6 or reduce chunk size with 15% overlap.'
  },
  generation: {
    icon: Sparkles,
    color: '#a855f7',
    badge: 'Generator Hallucination',
    query: 'What was the Q3 operating margin in 2024?',
    retrieved: 'Chunk #1: "Operating income was $42M on $210M revenue, yielding a 20.0% operating margin."',
    evidence: 'Exact span match verified in top chunk #1 at rank 1.',
    output: '"The operating margin in Q3 2024 was approximately 24.5%."',
    diagnosis: 'LIKELY_GENERATION_FAILURE',
    fix: 'Constrain system prompt: "Rely exclusively on extracted numbers in Context."'
  },
  pipeline: {
    icon: GitMerge,
    color: '#f59e0b',
    badge: 'Ordering & Context Break',
    query: 'Compare policy limits between Rider A and Rider B.',
    retrieved: 'Both passages retrieved in chunks #1 and #2, total length 2800 tokens.',
    evidence: 'Context passed exceeds effective attention window; Rider B truncated in prompt.',
    output: '"Rider A limits are $1M. Rider B policy details are not available."',
    diagnosis: 'PIPELINE_INTERACTION_FAILURE',
    fix: 'Optimize context serialization order and summarize intermediate chunks.'
  },
  data: {
    icon: FileSpreadsheet,
    color: '#10b981',
    badge: 'Test Set Noise',
    query: 'What is the renewal grace period?',
    retrieved: 'Passage retrieved accurately, states "30 business days".',
    evidence: 'Reference test key mistakenly entered as "1 calendar month".',
    output: '"30 business days from notice date."',
    diagnosis: 'EVALUATION_DATA_MISMATCH',
    fix: 'Update synthetic benchmark reference or review with subject matter expert.'
  }
};

export default function Problem() {
  const [activeKey, setActiveKey] = useState('retrieval');
  const activeDetail = FAILURE_METRICS[activeKey] || FAILURE_METRICS.retrieval;
  const ActiveIcon = activeDetail.icon;

  return (
    <section className="section" id="problem">
      <div className="section__inner">
        <SectionHeading eyebrow="01 — The problem">A wrong answer has many causes</SectionHeading>
        <ScrollReveal
          containerClassName="lead-reveal"
          textClassName="lead-reveal__text"
          baseOpacity={0.12}
          enableBlur
          blurStrength={4}
          baseRotation={2}
          stagger={0.05}
        >
          A RAG system retrieves passages and writes an answer from them. When that answer fails, a single end-to-end
          score cannot tell you whether the retriever missed the evidence, the generator ignored it, or the pipeline
          coordination broke down.
        </ScrollReveal>

        <div className="failure-grid">
          {FAILURES.map(failure => {
            const isSelected = failure.key === activeKey;
            const meta = FAILURE_METRICS[failure.key];
            const CardIcon = meta.icon;

            return (
              <article
                key={failure.key}
                className={`failure-card cursor-target failure-card--${failure.key}${isSelected ? ' failure-card--active' : ''}`}
                data-cursor-label={failure.tag}
                onClick={() => setActiveKey(failure.key)}
                style={{ '--card-accent': meta.color }}
              >
                <div className="failure-card__header">
                  <div className="failure-card__icon-box">
                    <CardIcon size={20} />
                  </div>
                  <span className="failure-card__tag">{failure.tag}</span>
                </div>
                <h3>{failure.title}</h3>
                <p>{failure.body}</p>
                <div className="failure-card__footer">
                  <span className="failure-card__action">
                    {isSelected ? 'Viewing live autopsy' : 'Inspect anatomy'}
                  </span>
                  <ArrowRight size={14} className="failure-card__arrow" />
                </div>
              </article>
            );
          })}
        </div>

