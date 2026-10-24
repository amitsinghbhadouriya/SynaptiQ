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
