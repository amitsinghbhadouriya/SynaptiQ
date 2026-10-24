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
            </CtaButton>
          </div>

          <div className="cta__trust">
            <div className="cta__trust-item">
              <ShieldCheck size={15} className="text-accent" />
              <span>100% Local & Offline First</span>
            </div>
            <div className="cta__trust-dot" />
            <div className="cta__trust-item">
              <span>Zero External Telemetry</span>
            </div>
            <div className="cta__trust-dot" />
            <div className="cta__trust-item">
              <span>Deterministic Rule Audits</span>
            </div>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="footer__grid">
          <div className="footer__col footer__col--brand">
            <div className="footer__brand cursor-target" data-cursor-label="Top" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
              <LogoMark size={26} ink="#eef0f5" accent="#3987e5" />
              <span>Synapti<span className="brand-q">Q</span></span>
            </div>
            <p className="footer__tagline">{TAGLINE}</p>
            <div className="footer__status-badge">
              <span className="footer__status-dot" aria-hidden="true" />
              <span>Diagnostic Core: Operational (Local)</span>
            </div>
          </div>

          <div className="footer__col">
            <h4 className="footer__heading">Architecture</h4>
            <ul className="footer__list">
              <li><button type="button" onClick={() => scrollToId('problem')}>Problem Breakdown</button></li>
              <li><button type="button" onClick={() => scrollToId('loop')}>4-Step Workflow</button></li>
              <li><button type="button" onClick={() => scrollToId('showcase')}>Dashboard Showcase</button></li>
              <li><button type="button" onClick={() => scrollToId('features')}>Key Features</button></li>
