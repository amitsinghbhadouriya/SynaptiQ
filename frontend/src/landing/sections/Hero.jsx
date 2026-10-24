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
