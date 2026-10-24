import { lazy, Suspense, useCallback, useEffect, useRef, useState } from 'react';

import { createBridge } from './bridge/transport.js';

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

  if (!props) return <Splash />;

  return (
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
  );
}
