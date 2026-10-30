import { ArrowUp, ShieldCheck, Sparkles } from 'lucide-react';

import MaskedHeading from '../../components/reactbits/MaskedHeading.jsx';
import LogoMark from '../../components/LogoMark.jsx';
import evidenceImg from '../../assets/features/evidence.jpg';
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

          <div className="cta__heading-container">
            <MaskedHeading
              text="Turn RAG Evaluation Into Verifiable Fixes"
              tag="h2"
              mediaType="image"
              src={evidenceImg}
              fillScale={1.3}
              parallax={28}
              drift={14}
              reveal="rise"
              trigger="view"
              spotlight
              spotlightRadius={190}
              outline
              outlineColor="rgba(56, 189, 248, 0.45)"
              outlineWidth={1}
              weight={700}
              textScale={0.068}
              align="center"
              tint="rgba(57, 135, 229, 0.15)"
              className="cta__masked-title"
            />
          </div>

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
            </ul>
          </div>

          <div className="footer__col">
            <h4 className="footer__heading">Diagnostics</h4>
            <ul className="footer__list">
              <li><button type="button" onClick={() => scrollToId('diagnosis')}>Root-Cause Matrix</button></li>
              <li><button type="button" onClick={() => scrollToId('pipeline')}>12-Step Pipeline</button></li>
              <li><button type="button" onClick={() => scrollToId('stack')}>Technology Stack</button></li>
              <li><button type="button" onClick={onLaunch}>Launch App</button></li>
            </ul>
          </div>

          <div className="footer__col">
            <h4 className="footer__heading">Core Stack</h4>
            <ul className="footer__list footer__list--static">
              <li>Python 3.11 Engine</li>
              <li>ChromaDB Vector Store</li>
              <li>Sentence Transformers</li>
              <li>Pytest 100% Verified</li>
            </ul>
          </div>
        </div>

        <div className="footer__bottom">
          <p className="footer__copy">
            © {new Date().getFullYear()} SynaptiQ. Designed for high-reliability, evidence-grounded AI systems.
          </p>
          <button
            type="button"
            className="footer__top-btn cursor-target"
            data-cursor-label="Back to top"
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          >
            <span>Back to top</span>
            <ArrowUp size={14} />
          </button>
        </div>
      </footer>
    </>
  );
}
