import { Activity, Cpu, Sliders, ShieldCheck, ArrowRight, Sparkles } from 'lucide-react';

import OrbitImages from '../../components/reactbits/OrbitImages.jsx';
import ScrollReveal from '../../components/reactbits/ScrollReveal.jsx';
import { LOOP } from '../content.js';
import { SectionHeading } from '../shared.jsx';

import ingestImg from '../../assets/features/ingest.jpg';
import chunkImg from '../../assets/features/chunk.jpg';
import testsImg from '../../assets/features/tests.jpg';
import modesImg from '../../assets/features/modes.jpg';
import evidenceImg from '../../assets/features/evidence.jpg';
import diagnoseImg from '../../assets/features/diagnose.jpg';
import recommendImg from '../../assets/features/recommend.jpg';
import compareImg from '../../assets/features/compare.jpg';

const ORBIT_MODULES = [
  { src: ingestImg, alt: 'Ingestion & Vector Indexing' },
  { src: chunkImg, alt: 'Token Overlap & Chunking' },
  { src: testsImg, alt: 'Synthetic Test Synthesis' },
  { src: modesImg, alt: 'Multi-Mode Evaluation' },
  { src: evidenceImg, alt: 'Ground-Truth Evidence Verification' },
  { src: diagnoseImg, alt: 'Deterministic Root-Cause Logic' },
  { src: recommendImg, alt: 'Remediation Tuning' },
  { src: compareImg, alt: 'Verifiable Benchmark Comparison' }
];

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
        </ScrollReveal>

        <div className="loop-orbit-wrapper">
          <OrbitImages
            images={ORBIT_MODULES}
            shape="ellipse"
            radiusX={460}
            radiusY={120}
            rotation={-5}
            duration={28}
            itemSize={88}
            itemRadius={16}
            depth={0.65}
            showPath
            pathColor="rgba(56, 189, 248, 0.25)"
            pathWidth={1.5}
            pathDash={6}
            shadow={0.5}
            hoverScale={1.14}
            hoverSpeed={0.2}
            draggable
            clickToFront
            centerContent={
              <div className="loop-orbit-center">
                <span className="loop-orbit-center__pulse" aria-hidden="true" />
                <div className="loop-orbit-center__badge">
                  <span className="loop-orbit-center__eyebrow">
                    <Sparkles size={11} style={{ display: 'inline', verticalAlign: '-1px', marginRight: '4px' }} />
                    CONTINUOUS AUDIT LOOP
                  </span>
                  <span className="loop-orbit-center__title">Interactive Diagnostics</span>
                  <span className="loop-orbit-center__hint">Drag to fling · Click to bring to front</span>
                </div>
              </div>
            }
          />
        </div>

        <div className="loop-container">
          <ol className="loop">
            {LOOP.map((item, index) => {
              const meta = STEP_META[index] || STEP_META[0];
              const StepIcon = meta.icon;

              return (
                <li
                  key={item.step}
                  className="loop__step cursor-target"
                  data-cursor-label={item.title}
                >
                  <div className="loop__step-top">
                    <span className="loop__num">{item.step}</span>
                    <div className="loop__step-icon">
                      <StepIcon size={18} />
                    </div>
                  </div>

                  <span className="loop__badge">{meta.badge}</span>
                  <h3>{item.title}</h3>
                  <p>{item.body}</p>

                  <div className="loop__footer">
                    <span className="loop__highlight">{meta.highlight}</span>
                  </div>

                  {index < LOOP.length - 1 && (
                    <div className="loop__connector" aria-hidden="true">
                      <ArrowRight size={14} />
                    </div>
                  )}
                </li>
              );
            })}
          </ol>
        </div>
      </div>
    </section>
  );
}
