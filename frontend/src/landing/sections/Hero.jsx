import { Layers, Cpu, CheckCircle2, ArrowDown } from 'lucide-react';

import ElectricLogo from '../../components/reactbits/ElectricLogo.jsx';
import TechText from '../../components/reactbits/TechText.jsx';
import SynapseScene from '../../components/three/SynapseScene.jsx';
import markUrl from '../../assets/synaptiq-mark.svg';
import { TAGLINE } from '../content.js';
import { CtaButton, scrollToId } from '../shared.jsx';

const FACTS = [
  {
    value: '3',
    label: 'independent test modes',
    detail: 'Retriever, generator & end-to-end',
    icon: Layers
  },
  {
    value: '7',
    label: 'explainable outcomes',
    detail: 'Deterministic root-cause logic',
    icon: Cpu
  },
  {
    value: '1',
    label: 'click to verify fix',
    detail: 'Fair, identical test benchmarks',
    icon: CheckCircle2
  }
];

export default function Hero({ onLaunch }) {
  return (
    <section className="hero" id="top">
      <SynapseScene className="hero__scene" />
      <div className="hero__vignette" aria-hidden="true" />
      <div className="hero__ambient-glow" aria-hidden="true" />

      <div className="hero__content">
        <div className="hero__badges">
          <p className="hero__eyebrow">
            <span className="hero__eyebrow-dot" aria-hidden="true" />
            RAG evaluation · Root-cause intelligence · Optimization
          </p>
        </div>

        <div className="hero__logo cursor-target" data-cursor-label="SynaptiQ">
          <ElectricLogo
            src={markUrl}
            color="#e9f1ff"
            glowColor="#3987e5"
            scale={0.58}
            strands={4}
            bend={0.55}
            crackle={1.2}
            arcs={0.9}
            speed={2.2}
            glow={0.9}
            interactive
          />
        </div>

        <h1 className="sq-visually-hidden">SynaptiQ</h1>
        <div className="hero__wordmark">
          <TechText
            text="SynaptiQ"
            fontFamily="Space Grotesk Variable"
            fontWeight={600}
            fontSize={176}
            reveal="letter"
            dashLength={4}
            dashGap={2}
            specks={15}
            intro="metrics"
            introDuration={2.2}
            clickKick
            guides={false}
            color="#f1f4fa"
            accentColor="#3987e5"
          />
        </div>

        <p className="hero__tagline">{TAGLINE}</p>
        <p className="hero__sub">
          SynaptiQ isolates your retriever, your generator, and the combined RAG pipeline. It identifies exactly why an
          answer degraded, recommends one targeted parameter change, and verifies whether the fix truly improved performance.
        </p>

        <div className="hero__actions">
          <CtaButton onClick={onLaunch} className="cursor-target" data-cursor-label="Launch">
            Launch Dashboard →
          </CtaButton>
          <CtaButton variant="secondary" onClick={() => scrollToId('loop')} className="cursor-target" data-cursor-label="How it works">
            Explore Architecture
          </CtaButton>
        </div>

        <div className="hero__facts-grid">
          {FACTS.map(fact => {
            const IconComponent = fact.icon;
            return (
              <div key={fact.label} className="hero__fact-card cursor-target" data-cursor-label={fact.label}>
                <div className="hero__fact-top">
                  <div className="hero__fact-icon">
                    <IconComponent size={18} />
                  </div>
                  <span className="hero__fact-val">{fact.value}</span>
                </div>
                <div className="hero__fact-label">{fact.label}</div>
                <div className="hero__fact-detail">{fact.detail}</div>
              </div>
            );
          })}
        </div>
      </div>

      <button
        type="button"
        className="hero__scroll cursor-target"
        data-cursor-label="Scroll"
        onClick={() => scrollToId('problem')}
      >
        <span>Explore Problem</span>
        <ArrowDown size={14} className="hero__scroll-arrow" />
      </button>
    </section>
  );
}
