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
