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

