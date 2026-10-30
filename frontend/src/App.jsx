import { lazy, Suspense, useCallback, useEffect, useRef, useState } from 'react';

import { createBridge } from './bridge/transport.js';
import GlowCursor from './components/reactbits/GlowCursor.jsx';
import TargetCursor from './components/reactbits/TargetCursor.jsx';

const LandingPage = lazy(() => import('./landing/LandingPage.jsx'));
const DashboardApp = lazy(() => import('./dashboard/DashboardApp.jsx'));

const nonce = () => `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;

function Splash() {
  return (
    <div className="sq-splash" role="status" aria-live="polite">
      <span className="sq-splash__dot" />
      Loading SynaptiQ…
    </div>
  );
}

export default function App() {
  const [props, setProps] = useState(null);
  const bridgeRef = useRef(null);

  useEffect(() => {
    const bridge = createBridge(args => setProps(args));
    bridgeRef.current = bridge;
    return () => bridge.dispose();
  }, []);

  useEffect(() => {
    const onWheel = e => {
      const prev = window.scrollY;
      requestAnimationFrame(() => {
        if (window.scrollY === prev && e.deltaY !== 0) {
          const maxScroll = Math.max(
            document.documentElement.scrollHeight,
            document.body.scrollHeight
          ) - window.innerHeight;
          if ((e.deltaY > 0 && prev < maxScroll - 1) || (e.deltaY < 0 && prev > 1)) {
            window.scrollBy({ top: e.deltaY, behavior: 'auto' });
          }
        }
      });
    };
    window.addEventListener('wheel', onWheel, { passive: true });
    return () => window.removeEventListener('wheel', onWheel);
  }, []);

  const send = useCallback(event => {
    const payload = { ...event, nonce: nonce() };
    bridgeRef.current?.send(payload);
    return payload.nonce;
  }, []);

  const view = props?.view;
  useEffect(() => {
    if (view) window.scrollTo(0, 0);
  }, [view]);

  const cursorNode = (
    <GlowCursor
      color="#3987e5"
      secondaryColor="#6366f1"
      intensity={0.55}
      glow={0.5}
      hotspot={0.25}
      trailWidth={2.2}
      linger={1.0}
      clickBurst
      theme="dark"
      className="glow-cursor--fixed"
    />
  );

  const targetCursorNode = (
    <TargetCursor
      targetSelector="button, [role='button'], a.btn, a.nav__link-btn, .cursor-target, .dash button, .dash a, .dash .d-tab, .dash .d-seg__opt, .dash .d-icon-btn, .dash .d-metric, .dash .d-card"
      hideDefaultCursor={false}
      onlyOnTarget
      spinDuration={2}
      parallaxOn
      cursorColor="#38bdf8"
    />
  );

  if (!props) {
    return (
      <>
        {cursorNode}
        {targetCursorNode}
        <Splash />
      </>
    );
  }

  return (
    <>
      {cursorNode}
      {targetCursorNode}
      <Suspense fallback={<Splash />}>
        {view === 'dashboard' ? (
          <DashboardApp
            data={props.data}
            notice={props.data?.notice ?? props.notice}
            download={props.data?.download ?? props.download}
            apiError={props.api_error}
            mode={bridgeRef.current?.mode}
            send={send}
          />
        ) : (
          <LandingPage send={send} />
        )}
      </Suspense>
    </>
  );
}
