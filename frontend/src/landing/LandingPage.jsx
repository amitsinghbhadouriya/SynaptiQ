import { useEffect } from 'react';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

import TargetCursor from '../components/reactbits/TargetCursor.jsx';
import CallToAction from './sections/CallToAction.jsx';
import Diagnosis from './sections/Diagnosis.jsx';
import Features from './sections/Features.jsx';
import Hero from './sections/Hero.jsx';
import Loop from './sections/Loop.jsx';
import Navbar from './sections/Navbar.jsx';
import Pipeline from './sections/Pipeline.jsx';
import Problem from './sections/Problem.jsx';
import Showcase from './sections/Showcase.jsx';
import TechStack from './sections/TechStack.jsx';
import './landing.css';

// The landing page is composed of self-contained sections, top to bottom.
export default function LandingPage({ send }) {
  const launch = () => send({ type: 'navigate', page: 'dashboard' });

  useEffect(() => {
    document.documentElement.removeAttribute('data-theme');
    document.title = 'SynaptiQ — RAG evaluation & root-cause intelligence';
    // Fonts and lazy sections change layout after mount; re-measure scroll triggers once settled.
