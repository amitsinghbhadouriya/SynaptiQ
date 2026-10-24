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
