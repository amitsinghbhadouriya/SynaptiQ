import { ArrowUp, ShieldCheck, Sparkles } from 'lucide-react';

import ScrollReveal from '../../components/reactbits/ScrollReveal.jsx';
import LogoMark from '../../components/LogoMark.jsx';
import { TAGLINE } from '../content.js';
import { CtaButton, scrollToId } from '../shared.jsx';

export default function CallToAction({ onLaunch }) {
  return (
    <>
      <section className="section cta" id="cta">
        <div className="cta__glow" aria-hidden="true" />
        <div className="section__inner cta__inner">
          <div className="cta__badge">
            <Sparkles size={14} className="text-accent" />
            <span>Deterministic RAG Intelligence</span>
          </div>

          <ScrollReveal
            containerClassName="cta__reveal"
            textClassName="cta__text"
            baseOpacity={0.1}
            enableBlur
            blurStrength={5}
            baseRotation={3}
            highlightColor="#3987e5"
          >
            SynaptiQ turns RAG evaluation from a score report into an evidence-backed improvement workflow.
          </ScrollReveal>

          <p className="cta__sub">
            Test your retriever and generator in isolation. Uncover the exact cause of hallucinations and retrieval misses.
            Tune chunking and prompts with fair, verifiable before-and-after benchmarks.
          </p>

          <div className="cta__actions">
            <CtaButton onClick={onLaunch} className="cursor-target" data-cursor-label="Dashboard">
              Launch Dashboard →
            </CtaButton>
            <CtaButton variant="secondary" onClick={() => scrollToId('top')} className="cursor-target" data-cursor-label="Top">
              Back to Top ↑
