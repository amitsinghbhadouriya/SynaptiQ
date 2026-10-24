import { UploadCloud, FileCheck, SplitSquareVertical, Database, Sparkles, UserCheck, Play, HelpCircle, Lightbulb, RefreshCw, BarChart3, Check } from 'lucide-react';

import ScrollReveal from '../../components/reactbits/ScrollReveal.jsx';
import { SectionHeading } from '../shared.jsx';

const PIPELINE_PHASES = [
  {
    phase: 'Phase 01',
    name: 'Ingestion & Vector Indexing',
    color: '#0ea5e9',
    steps: [
      { num: '01', label: 'Upload document', icon: UploadCloud, hint: 'PDF, DOCX, TXT' },
      { num: '02', label: 'Validate type & size', icon: FileCheck, hint: 'Integrity check' },
      { num: '03', label: 'Extract text + metadata', icon: FileCheck, hint: 'PyMuPDF & python-docx' },
      { num: '04', label: 'Chunk & assign IDs', icon: SplitSquareVertical, hint: 'Sentence-aware split' },
      { num: '05', label: 'Embed & index in ChromaDB', icon: Database, hint: 'Sentence Transformers' }
    ]
  },
  {
    phase: 'Phase 02',
    name: 'Test Synthesis & Human Review',
    color: '#a855f7',
    steps: [
      { num: '06', label: 'Generate / import questions', icon: Sparkles, hint: '4 question categories' },
      { num: '07', label: 'Human review & approval', icon: UserCheck, hint: 'Audit synthetic spans' }
    ]
  },
  {
    phase: 'Phase 03',
    name: 'Multi-Mode Evaluation & Root-Cause',
    color: '#f59e0b',
    steps: [
      { num: '08', label: 'Run three test modes', icon: Play, hint: 'Retriever, Gen & E2E' },
      { num: '09', label: 'Diagnose likely cause', icon: HelpCircle, hint: 'Deterministic rules' }
    ]
  },
  {
    phase: 'Phase 04',
    name: 'Remediation & Fair Verification',
    color: '#10b981',
    steps: [
      { num: '10', label: 'Recommend a change', icon: Lightbulb, hint: 'Single-variable tuning' },
      { num: '11', label: 'Re-run the same set', icon: RefreshCw, hint: 'Identical question IDs' },
      { num: '12', label: 'Compare & export', icon: BarChart3, hint: 'Delta, latency & cost' }
    ]
  }
];

export default function Pipeline() {
  return (
    <section className="section" id="pipeline">
      <div className="section__inner">
        <SectionHeading eyebrow="05 — Evaluation pipeline">From upload to verified fix</SectionHeading>
        <ScrollReveal containerClassName="lead-reveal" textClassName="lead-reveal__text" baseOpacity={0.12} baseRotation={2}>
          Every run stores its exact configuration and locks the question IDs. Comparisons between baseline and candidate
          configurations remain completely unbiased, reproducible, and mathematically rigorous.
        </ScrollReveal>

        <div className="pipeline-flow">
          {PIPELINE_PHASES.map((phase) => (
            <div
              key={phase.phase}
              className="pipeline-phase"
              style={{ '--phase-color': phase.color }}
            >
              <div className="pipeline-phase__header">
                <span className="pipeline-phase__tag">{phase.phase}</span>
