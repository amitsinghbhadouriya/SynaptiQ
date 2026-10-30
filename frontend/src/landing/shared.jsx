import SpecularButton from '../components/reactbits/SpecularButton.jsx';
import ScrollFloat from '../components/reactbits/ScrollFloat.jsx';

export const scrollToId = id => {
  const target = document.getElementById(id);
  if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

// Landing action buttons rendered as SpecularButton with edge reflections covering the full button length.
export function CtaButton({ variant = 'primary', size = 'md', className = '', children, ...props }) {
  const primary = variant === 'primary';
  return (
    <SpecularButton
      size={size}
      radius={999}
      tint={primary ? '#ffffff' : '#38bdf8'}
      tintOpacity={primary ? 0.96 : 0.06}
      textColor={primary ? '#0b0d12' : '#f1f5f9'}
      lineColor={primary ? '#ffffff' : '#38bdf8'}
      baseColor={primary ? 'rgba(56, 189, 248, 0.5)' : 'rgba(255, 255, 255, 0.18)'}
      intensity={1.3}
      idleIntensity={0.45}
      shineSize={85}
      shineFade={110}
      thickness={1.6}
      glow={1.2}
      followMouse
      proximity={320}
      className={`cta-btn cta-btn--${variant} cta-btn--${size} ${className}`.trim()}
      {...props}
    >
      {children}
    </SpecularButton>
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
