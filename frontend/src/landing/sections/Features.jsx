import { useEffect, useState } from 'react';

import AccordionGallery from '../../components/reactbits/AccordionGallery.jsx';
import { FEATURES } from '../content.js';
import { SectionHeading } from '../shared.jsx';

import ingestImg from '../../assets/features/ingest.jpg';
import chunkImg from '../../assets/features/chunk.jpg';
import testsImg from '../../assets/features/tests.jpg';
import modesImg from '../../assets/features/modes.jpg';
import evidenceImg from '../../assets/features/evidence.jpg';
import diagnoseImg from '../../assets/features/diagnose.jpg';
import recommendImg from '../../assets/features/recommend.jpg';
import compareImg from '../../assets/features/compare.jpg';

const FEATURE_IMAGES = {
  ingest: ingestImg,
  chunk: chunkImg,
  tests: testsImg,
  modes: modesImg,
  evidence: evidenceImg,
  diagnose: diagnoseImg,
  recommend: recommendImg,
  compare: compareImg
};

const useNarrow = () => {
  const [narrow, setNarrow] = useState(() => window.innerWidth < 900);
  useEffect(() => {
    const onResize = () => setNarrow(window.innerWidth < 900);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  return narrow;
};

// React Bits AccordionGallery with dedicated high-resolution visual artwork for each key feature card.
// All animations (GSAP expandRatio, parallax, tilt, duration, and hover triggers) are strictly preserved.
export default function Features() {
  const narrow = useNarrow();
  const items = FEATURES.map((feature, index) => ({
    label: feature.title,
    cursorLabel: feature.short,
    image: FEATURE_IMAGES[feature.key],
    collapsedLabel: (
      <>
        <span className="feature-collapsed__num">0{index + 1}</span> {feature.short}
      </>
    ),
    content: (
      <span className="feature-copy">
        <span className="feature-copy__index">0{index + 1} / 0{FEATURES.length}</span>
        <span className="feature-copy__title">{feature.title}</span>
        <span className="feature-copy__body">{feature.body}</span>
        <span className="feature-copy__points">
          {feature.points.map(point => (
            <span key={point} className="feature-copy__point">
              {point}
            </span>
          ))}
