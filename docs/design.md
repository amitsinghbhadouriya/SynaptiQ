# Design System & UI/UX

This document explains the visual design system, user experience choices, typography, color palette, and interactive animations used throughout **SynaptiQ**.

---

## 1. Design Philosophy

SynaptiQ is built with a **cybernetic, high-precision aesthetic** inspired by mission-critical developer tools and futuristic diagnostic stations:
- **Restrained & Professional**: The interface relies on dark, deep charcoal neutrals so that high-priority metrics and pass/fail states immediately pop out.
- **Glassmorphism & Depth**: Subtle glass borders, blurred backdrops (`backdrop-filter: blur(12px)`), and radial ambient glow orbs create visual hierarchy without clutter.
- **Dynamic Micro-Interactions**: Rather than feeling like a static document, the interface feels alive with responsive hover states, smooth scroll-triggered reveals, and 3D scenes.
- **Accessible & Contrast-Compliant**: Every text color passes WCAG AA contrast standards. Green is reserved strictly for passing benchmarks, and red/rose is reserved strictly for failures.

---

## 2. Color Palette

All colors are controlled using CSS custom properties (`tokens`) defined in `frontend/src/styles/global.css`:

| Token | Hex / Value | Usage |
|---|---|---|
| `--l-bg` | `#07080b` | Main deep background (near black) |
| `--l-bg-2` | `#0b0d12` | Secondary panel and footer background |
| `--l-surface` | `#0f1117` | Card surfaces and containers |
| `--l-surface-2` | `#151822` | Hovered cards and active navigation pills |
| `--l-border` | `rgba(255, 255, 255, 0.08)` | Subtle container borders |
| `--l-border-strong`| `rgba(255, 255, 255, 0.16)` | Active card borders and badge outlines |
| `--l-ink` | `#eef0f5` | Primary high-contrast headings and body text |
| `--l-ink-2` | `#b4b9c5` | Secondary text, descriptions, and metadata |
| `--l-muted` | `#7d8494` | Footnotes, timestamps, and inactive labels |
| `--l-accent` | `#3987e5` | SynaptiQ signature radiant blue accent |
| `--l-good` | `#10b981` | Passing evaluations, verified fixes, and success indicators |
| `--l-warning` | `#f59e0b` | Potential regressions, warnings, and missing reference data |
| `--l-bad` | `#f43f5e` | Failed evaluations, hallucinations, and unretrieved evidence |
| `--l-purple` | `#a855f7` | End-to-end mode indicators and diagnostic highlights |
| `--l-cyan` | `#0ea5e9` | Retriever mode indicators |

### The SynaptiQ "Q" Multi-Stop Gradient
The signature **"Q"** in SynaptiQ features an electric gradient with dynamic keyframe animation:
- **Gradient Stops**: `#00f5ff` (Electric Cyan) $\to$ `#38bdf8` (Sky Neon) $\to$ `#6366f1` (Indigo Pulse) $\to$ `#a855f7` (Violet) $\to$ `#ec4899` (Rose Neon).
- **Animation**: Continuous 4.5s gradient sweep with a gentle 2.4s breathing drop-shadow pulse that scales on hover.

---

## 3. Typography

SynaptiQ uses high-performance modern web typography loaded via fontsource:

1. **Display & Headings**: `Space Grotesk Variable`
   - Geometric, modern, and technical.
   - Used for the hero wordmark, section headings (`h1` through `h4`), metric numbers, and brand logos.
2. **Body & Interface**: `Inter Variable`
   - Highly legible at small and standard font sizes.
   - Used for paragraphs, explanations, table data, buttons, and badges.
3. **Code & Data**: `ui-monospace, Menlo, Consolas, monospace`
   - Used for character offsets, chunk IDs, file paths, JSON previews, and token counts.

---

## 4. Key Interactive Components

| Component | Location | What It Does |
|---|---|---|
| **TechText** | `frontend/src/components/reactbits/TechText.jsx` | Renders the interactive "SynaptiQ" wordmark on HTML5 canvas with a metrics intro, draggable letter physics, and custom gradient glow on the letter Q. |
| **ElectricLogo** | `frontend/src/components/reactbits/ElectricLogo.jsx` | Renders a WebGL interactive brand logo with animated electric arcs and lightning crackles. |
| **SynapseScene** | `frontend/src/components/three/SynapseScene.jsx` | 3D Three.js particle scene depicting a neural synapse network that rotates with mouse parallax. |
| **ScrollFloat** | `frontend/src/components/reactbits/ScrollFloat.jsx` | Section titles float upwards and fade into view smoothly as the user scrolls down. |
| **ScrollReveal** | `frontend/src/components/reactbits/ScrollReveal.jsx` | Words illuminate one by one based on scroll progress. |
| **ScrollExpand** | `frontend/src/components/reactbits/ScrollExpand.jsx` | The showcase dashboard expands to full width with a smooth pinned scroll interaction. |
| **StarBorder** | `frontend/src/components/reactbits/StarBorder.jsx` | Buttons feature an animated luminous shooting-star border effect. |
| **TargetCursor** | `frontend/src/components/reactbits/TargetCursor.jsx` | Custom cybernetic bracket cursor that snaps onto interactive targets. |
| **MagicBento** | `frontend/src/components/reactbits/MagicBento.jsx` | High-tech bento grid cards in the dashboard with spotlight mouse hover glow and ripple effects. |
| **BounceCards** | `frontend/src/components/reactbits/BounceCards.jsx` | Interactive technology cards that tilt and bounce on hover. |

---

## 5. Visual Hierarchy & Spacing

- **Desktop Layout**: Standard max content width is bounded at `1280px` to maintain comfortable readability.
- **Fluid Typography**: Uses CSS `clamp()` functions (e.g., `font-size: clamp(2rem, 5vw, 3.8rem)`) to scale effortlessly across mobile phones, tablets, laptops, and ultra-wide desktop monitors.
- **Consistent Section Cadence**: Each section on the landing page is separated by standard vertical padding (`clamp(80px, 10vw, 140px)`).

---

## 6. Accessibility (a11y) & Performance

- **Reduced Motion Support**: If a user has `prefers-reduced-motion` enabled in their operating system, all continuous animations and transitions gracefully collapse to zero-duration.
- **Screen Reader Support**: Visually hidden headings (`.sq-visually-hidden`) are provided for assistive readers.
- **Hardware Acceleration**: Canvas and Three.js layers utilize GPU compositing (`will-change: transform`), ensuring 60 FPS performance even on low-power devices.
- **Theme Adaptability**: The dashboard supports both dark and light modes, controlled cleanly via `data-theme` on the root HTML tag.
