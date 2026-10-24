import ScrollExpand from '../../components/reactbits/ScrollExpand.jsx';
import previewUrl from '../../assets/dashboard-preview.png';
import { MODES } from '../content.js';
import { CtaButton } from '../shared.jsx';

// The dashboard preview expands to full bleed as you scroll; the three test modes are
// revealed on top of it once it fills the screen.
export default function Showcase({ onLaunch }) {
  // change 6: start wider on phones
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;

  return (
    <section className="showcase" id="showcase" aria-label="Dashboard preview">
      <ScrollExpand
        src={previewUrl}
        alt="SynaptiQ analytics dashboard"
        title="One dashboard. Every failure explained."
        scrollHint="Scroll to open the dashboard"
        startWidth={isMobile ? 88 : 46}
        startHeight={isMobile ? 64 : 56}
        startRadius={22}
        mediaZoom={1.3}
        scrollDistance={0}
        holdDistance={0}
        smoothing={0.1}
        overlayScrim={0.78}
        useWindowScroll
        fixedHeight={642}
      >
        <div className="showcase__overlay">
          <p className="showcase__eyebrow">Three tests · one verdict</p>
          <h2 className="showcase__title">Separate the retriever from the generator.</h2>
          <div className="showcase__modes">
            {MODES.map((mode, index) => (
              <div key={mode.title} className="showcase__mode cursor-target" data-cursor-label={`Mode ${index + 1}`}>
                <span className="showcase__mode-index">0{index + 1}</span>
                <h3>{mode.title}</h3>
                <p>{mode.body}</p>
              </div>
            ))}
          </div>
          <CtaButton onClick={onLaunch}>Open the dashboard →</CtaButton>
        </div>
      </ScrollExpand>
    </section>
  );
}
