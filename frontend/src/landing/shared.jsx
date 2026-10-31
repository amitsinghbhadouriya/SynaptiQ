import ScrollFloat from '../components/reactbits/ScrollFloat.jsx';

export const scrollToId = id => {
  const target = document.getElementById(id);
  if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

// Landing action buttons styled as clean modern pills.
export function CtaButton({ variant = 'primary', size = 'md', className = '', children, ...props }) {
  return (
    <button
      type="button"
      className={`cta-btn cta-btn--${variant} cta-btn--${size} ${className}`.trim()}
      {...props}
    >
      <span className="cta-btn__content">{children}</span>
    </button>
  );
}

export function SectionHeading({ eyebrow, children, align = 'left' }) {
  return (
    <header className={`section-heading section-heading--${align}`}>
      {eyebrow && <p className="section-heading__eyebrow">{eyebrow}</p>}
      <ScrollFloat
        containerClassName="section-heading__title"
        textClassName="section-heading__text"
        effect="float"
        splitBy="chars"
        animationDuration={0.9}
        ease="power2.out"
        scrollStart="top bottom-=10%"
        scrollEnd="center center+=10%"
        stagger={0.02}
        distance={35}
        stretch={1.05}
      >
        {children}
      </ScrollFloat>
    </header>
  );
}
