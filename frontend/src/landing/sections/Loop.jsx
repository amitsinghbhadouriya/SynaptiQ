import { Activity, Cpu, Sliders, ShieldCheck, ArrowRight } from 'lucide-react';

import ScrollReveal from '../../components/reactbits/ScrollReveal.jsx';
import { LOOP } from '../content.js';
import { SectionHeading } from '../shared.jsx';

const STEP_META = [
  {
    icon: Activity,
    badge: 'Multi-Mode Benchmarks',
    highlight: 'Tests retriever, generator & pipeline independently'
  },
  {
    icon: Cpu,
    badge: 'Evidence Classification',
    highlight: 'Maps results to 7 deterministic root-cause rules'
  },
  {
    icon: Sliders,
    badge: 'Targeted Remediation',
    highlight: 'Prescribes 1 isolated tuning parameter change'
  },
  {
    icon: ShieldCheck,
    badge: 'Fair Benchmark Verification',
    highlight: 'Re-runs exact same questions to confirm lift'
  }
];

export default function Loop() {
  return (
    <section className="section section--alt" id="loop">
      <div className="section__inner">
        <SectionHeading eyebrow="02 — Our solution">Evaluate. Diagnose. Recommend. Verify.</SectionHeading>
        <ScrollReveal
          containerClassName="lead-reveal"
          textClassName="lead-reveal__text"
          baseOpacity={0.12}
          baseRotation={2}
        >
          SynaptiQ is not a black-box document chatbot. It is a precision diagnostics engine that pinpoints what failed,
          explains why it failed, and measures whether your targeted change produced a verifiable improvement.
