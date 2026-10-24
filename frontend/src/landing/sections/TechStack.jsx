import { useEffect, useMemo, useRef, useState } from 'react';

import BounceCards from '../../components/reactbits/BounceCards.jsx';
import { STACK } from '../content.js';
import { techCard, getTechIconSvg } from '../techCards.js';
import { SectionHeading } from '../shared.jsx';

const useWidth = ref => {
  const [width, setWidth] = useState(1000);
  useEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    const observer = new ResizeObserver(([entry]) => setWidth(Math.round(entry.contentRect.width)));
    observer.observe(el);
    return () => observer.disconnect();
  }, [ref]);
  return width;
};

// React Bits BounceCards showing every technology SynaptiQ is built with, using authentic tech symbols.
export default function TechStack() {
  const wrapRef = useRef(null);
  const width = useWidth(wrapRef);
  const perRow = width < 560 ? 3 : 6;
  const cardSize = Math.max(96, Math.min(172, Math.floor(width / (perRow * 0.82))));
  // Leave room for the tilt and the hover push so the outer cards stay inside the section.
  const spread = Math.min(cardSize * 1.04, (width - cardSize * 1.25) / Math.max(1, perRow - 1));
  const rows = useMemo(() => {
    const cards = STACK.map((item, index) => techCard(item, index));
    const out = [];
    for (let i = 0; i < cards.length; i += perRow) out.push(cards.slice(i, i + perRow));
    return out;
  }, [perRow]);

  return (
    <section className="section section--alt" id="stack">
      <div className="section__inner">
        <SectionHeading eyebrow="06 — Technology stack">Built on a Python-first stack</SectionHeading>
        <p className="section__hint">Hover a card to bring it forward.</p>
        <div className="stack" ref={wrapRef}>
          {rows.map((row, index) => (
            <BounceCards
              key={`${perRow}-${index}`}
              className="stack__row"
              images={row}
              containerWidth={Math.max(cardSize, width)}
              containerHeight={cardSize + 70}
              cardSize={cardSize}
              spread={spread}
              rotation={7}
              arc={index % 2 ? -10 : 10}
              pushDistance={Math.round(cardSize * 0.45)}
              hoverScale={1.08}
              bounciness={0.55}
              animationDelay={0.2 + index * 0.25}
              animationStagger={0.07}
              borderWidth={3}
              borderColor="#1b1f2a"
              radius={22}
              shadow
            />
          ))}
        </div>
        <ul className="stack__list" aria-label="Technologies and their roles">
          {STACK.map(item => (
            <li key={item.name} className="stack__item cursor-target" data-cursor-label={item.name}>
              <div
                className="stack__icon-badge"
                aria-hidden="true"
                dangerouslySetInnerHTML={{ __html: getTechIconSvg(item.name) }}
              />
              <div className="stack__item-info">
                <strong>{item.name}</strong>
                <span>{item.role}</span>
              </div>
            </li>
          ))}
          <li className="stack__item cursor-target" data-cursor-label="Standard Python">
            <div
              className="stack__icon-badge"
              aria-hidden="true"
              dangerouslySetInnerHTML={{ __html: getTechIconSvg('Standard Python') }}
            />
            <div className="stack__item-info">
              <strong>Standard Python</strong>
              <span>TXT handling & text cleaning</span>
            </div>
          </li>
        </ul>
      </div>
    </section>
  );
}
