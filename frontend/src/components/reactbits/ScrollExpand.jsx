'use client';

import { useCallback, useEffect, useRef } from 'react';

import './ScrollExpand.css';

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);

const smoothstep = (edge0, edge1, x) => {
  const t = clamp((x - edge0) / (edge1 - edge0 || 1e-6), 0, 1);
  return t * t * (3 - 2 * t);
};

const ScrollExpand = ({
  src = '',
  mediaType = 'image',
  poster = '',
  alt = '',
  title = '',
  scrollHint = '',
  startWidth = 42,
  startHeight = 58,
  startRadius = 24,
  endRadius = 0,
  mediaZoom = 1.35,
  scrollDistance = 1.2,
  holdDistance = 0.35,
  smoothing = 0.1,
  overlayScrim = 0.45,
  useWindowScroll = false,
  enabled = true,
  fixedHeight,
  children,
  className = '',
  style,
  ...rest
}) => {
  const rootRef = useRef(null);
  const trackRef = useRef(null);
  const stageRef = useRef(null);
  const frameRef = useRef(null);
  const mediaRef = useRef(null);
  const titleRef = useRef(null);
  const overlayRef = useRef(null);
  const scrimRef = useRef(null);
  const hintRef = useRef(null);

  const propsRef = useRef({});
  propsRef.current = {
    startWidth,
    startHeight,
    startRadius,
    endRadius,
    mediaZoom,
    scrollDistance,
    holdDistance,
    smoothing,
    overlayScrim,
    useWindowScroll,
    enabled,
    fixedHeight
  };

  const applyProgress = useCallback((p, exit = 0) => {
    const frame = frameRef.current;
    const media = mediaRef.current;
    if (!frame || !media) return;
    const c = propsRef.current;

    const e = smoothstep(0, 1, p);

    const w = c.startWidth + (100 - c.startWidth) * e;
    const h = c.startHeight + (100 - c.startHeight) * e;
    const ix = Math.max(0, (100 - w) / 2);
    const iy = Math.max(0, (100 - h) / 2);
    const r = c.startRadius + (c.endRadius - c.startRadius) * e;

    if (e >= 0.99) {
      frame.style.clipPath = 'none';
    } else {
      frame.style.clipPath = `inset(${iy}% ${ix}% ${iy}% ${ix}% round ${r}px)`;
    }

    media.style.transform = `scale(${c.mediaZoom + (1 - c.mediaZoom) * e})`;
    // change 1: darkens the image + adds blur
    media.style.filter = e > 0.05 ? `blur(${(e * 6).toFixed(1)}px)` : 'none';

    if (scrimRef.current) scrimRef.current.style.opacity = `${c.overlayScrim * e}`;

    // title fades out between 40% and 88%
    if (titleRef.current) {
      const out = smoothstep(0.4, 0.88, p);
      titleRef.current.style.opacity = `${1 - out}`;
      titleRef.current.style.transform = `translate3d(0, ${-28 * out}px, 0) scale(${1 + 0.06 * out})`;
    }

    if (hintRef.current) {
      const gone = smoothstep(0, 0.15, p);
      hintRef.current.style.opacity = `${1 - gone}`;
      hintRef.current.style.transform = `translate3d(0, ${8 * gone}px, 0)`;
    }

    // overlay fades in from 68% — change 3: fades out smoothly at end of hold for smooth handoff
    if (overlayRef.current) {
      const enter = smoothstep(0.68, 1, p);
      const exitFade = exit > 0 ? smoothstep(0.65, 1, exit) : 0;
      const opacity = enter * (1 - exitFade);
      overlayRef.current.style.opacity = `${opacity}`;
      overlayRef.current.style.transform = `translate3d(0, ${(18 * (1 - enter) - 20 * exitFade).toFixed(1)}px, 0)`;
      overlayRef.current.style.pointerEvents = opacity > 0.2 ? 'auto' : 'none';
    }
  }, []);

  useEffect(() => {
    const root = rootRef.current;
    const track = trackRef.current;
    const stage = stageRef.current;
    if (!root || !track || !stage) return;

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let raf = 0;
    let current = { p: 0, exit: 0 };
    let target = { p: 0, exit: 0 };
    let stageH = 0;
    let running = false;

    const measure = () => {
      const c = propsRef.current;
      stageH = c.fixedHeight ? c.fixedHeight : (c.useWindowScroll ? window.innerHeight : root.clientHeight);
      if (stageH <= 0) return;
      stage.style.height = `${stageH}px`;
      if (c.fixedHeight) {
        track.style.height = `${c.fixedHeight}px`;
      } else {
        track.style.height = `${stageH * (1 + Math.max(0, c.scrollDistance) + Math.max(0, c.holdDistance))}px`;
      }

      const w = root.clientWidth || stageH;
      stage.style.setProperty('--se-title-size', `${clamp(w * 0.075, 20, 84)}px`);
      try {
        if (typeof window !== 'undefined' && window.ScrollTrigger) {
          window.ScrollTrigger.refresh();
        }
      } catch {}
    };

    const readProgress = () => {
      const c = propsRef.current;
      if (!c.enabled) return { p: 1, exit: 0 };
      if (c.fixedHeight) {
        const rect = track.getBoundingClientRect();
        const vh = window.innerHeight || c.fixedHeight;
        // As the section scrolls from entering the screen to reaching top, expand smoothly
        const p = clamp((vh - rect.top) / (vh * 0.65), 0, 1);
        return { p, exit: 0 };
      }
      const span = stageH * Math.max(0.01, c.scrollDistance);
      const hold = stageH * Math.max(0.01, c.holdDistance);
      if (c.useWindowScroll) {
        const top = track.getBoundingClientRect().top;
        const p = clamp(-top / span, 0, 1);
        const exit = clamp((-top - span) / hold, 0, 1);
        return { p, exit };
      }
      const p = clamp(root.scrollTop / span, 0, 1);
      const exit = clamp((root.scrollTop - span) / hold, 0, 1);
      return { p, exit };
    };

    const tick = () => {
      const c = propsRef.current;
      const k = c.smoothing <= 0 ? 1 : 1 - Math.exp(-1 / (60 * c.smoothing));
      current.p += (target.p - current.p) * k;
      current.exit += (target.exit - current.exit) * k;
      if (Math.abs(target.p - current.p) < 0.0004 && Math.abs(target.exit - current.exit) < 0.0004) {
        current.p = target.p;
        current.exit = target.exit;
        running = false;
      }
      applyProgress(current.p, current.exit);
      raf = running ? requestAnimationFrame(tick) : 0;
    };

    const kick = () => {
      if (running) return;
      running = true;
      if (!raf) raf = requestAnimationFrame(tick);
    };

    const onScroll = () => {
      target = readProgress();
      if (propsRef.current.smoothing <= 0 || reduceMotion) {
        current = { ...target };
        applyProgress(current.p, current.exit);
        return;
      }
      kick();
    };

    const onResize = () => {
      measure();
      target = readProgress();
      current = { ...target };
      applyProgress(current.p, current.exit);
    };

    measure();
    target = readProgress();
    current = { ...target };
    applyProgress(current.p, current.exit);

    const scroller = useWindowScroll ? window : root;
    scroller.addEventListener('scroll', onScroll, { passive: true });
    if (useWindowScroll) {
      document.addEventListener('scroll', onScroll, { passive: true });
    }
    window.addEventListener('resize', onResize);
    const ro = new ResizeObserver(onResize);
    ro.observe(root);

    return () => {
      if (raf) cancelAnimationFrame(raf);
      scroller.removeEventListener('scroll', onScroll);
      if (useWindowScroll) {
        document.removeEventListener('scroll', onScroll);
      }
      window.removeEventListener('resize', onResize);
      ro.disconnect();
    };
  }, [applyProgress, useWindowScroll]);

  const media =
    mediaType === 'video' ? (
      <video
        ref={mediaRef}
        className="scroll-expand__media"
        src={src}
        poster={poster}
        autoPlay
        muted
        loop
        playsInline
      />
    ) : (
      <img ref={mediaRef} className="scroll-expand__media" src={src} alt={alt} draggable={false} />
    );

  return (
    <div
      ref={rootRef}
      className={`scroll-expand ${useWindowScroll ? '' : 'scroll-expand--scroller'} ${className}`.trim()}
      style={style}
      {...rest}
    >
      <div ref={trackRef} className="scroll-expand__track">
        <div ref={stageRef} className="scroll-expand__stage">
          <div ref={frameRef} className="scroll-expand__frame">
            {media}
            <div ref={scrimRef} className="scroll-expand__scrim" />
            {children ? (
              <div ref={overlayRef} className="scroll-expand__overlay">
                {children}
              </div>
            ) : null}
          </div>
          {title ? (
            <div ref={titleRef} className="scroll-expand__title">
              {title}
            </div>
          ) : null}
          {scrollHint ? (
            <div ref={hintRef} className="scroll-expand__hint">
              {scrollHint}
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default ScrollExpand;
