import StarBorder from '../components/reactbits/StarBorder.jsx';
import ScrollFloat from '../components/reactbits/ScrollFloat.jsx';

export const scrollToId = id => {
  const target = document.getElementById(id);
  if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

// Landing buttons are React Bits StarBorder buttons in two restrained styles.
export function CtaButton({ variant = 'primary', size = 'md', className = '', children, ...props }) {
  const primary = variant === 'primary';
  return (
    <StarBorder
      theme={primary ? 'light' : 'dark'}
      color={primary ? '#3987e5' : '#ffffff'}
      backgroundColor={primary ? '#eef0f5' : 'rgba(255,255,255,0.03)'}
      textColor={primary ? '#0b0d12' : '#eef0f5'}
      borderColor={primary ? 'rgba(11,13,18,0.08)' : 'rgba(255,255,255,0.14)'}
      radius={999}
      duration={primary ? 4 : 5}
      glow={primary ? 0.5 : 0.6}
      hover="lap"
      className={`cta-btn cta-btn--${variant} cta-btn--${size} ${className}`.trim()}
      {...props}
    >
      {children}
