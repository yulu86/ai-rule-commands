---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, artifacts, or applications (websites, landing pages, dashboards, React components, HTML/CSS layouts, or styling/beautifying web UI). Generates creative, polished code avoiding generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

Create distinctive, production-grade frontend interfaces that avoid generic aesthetics.

---

## Quick Start

1. **Choose aesthetic direction** - See [aesthetics.md](reference/aesthetics.md) for style options
2. **Apply principles** - Follow [design_principles.md](reference/design_principles.md) for detailed guidelines
3. **Review examples** - Check [examples.md](reference/examples.md) for complete working patterns

---

## Design Thinking

Before coding, define:

- **Purpose**: What problem does this solve? Who uses it?
- **Tone**: Pick a clear aesthetic (brutalist, retro-futuristic, luxury, organic, maximalist, minimalist)
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose ONE direction and execute with precision. Bold maximalism and refined minimalism both work—the key is intentionality.

---

## Project Type Selection

Choose the right pattern based on project type:

| Project Type | Load Reference |
|--------------|----------------|
| Landing Pages | [landing_page_patterns.md](reference/landing_page_patterns.md) |
| Dashboards | [dashboard_patterns.md](reference/dashboard_patterns.md) |
| Portfolios | [portfolio_patterns.md](reference/portfolio_patterns.md) |
| E-commerce | [ecommerce_patterns.md](reference/ecommerce_patterns.md) |

---

## Reference Files

### Core Design
- [aesthetics.md](reference/aesthetics.md) - Design styles (brutalist, luxury, retro-futuristic, etc.)
- [design_principles.md](reference/design_principles.md) - Typography, color, motion, composition

### Examples & Patterns
- [examples.md](reference/examples.md) - Complete working examples
- [landing_page_patterns.md](reference/landing_page_patterns.md) - Landing page patterns
- [dashboard_patterns.md](reference/dashboard_patterns.md) - Dashboard patterns
- [portfolio_patterns.md](reference/portfolio_patterns.md) - Portfolio patterns
- [ecommerce_patterns.md](reference/ecommerce_patterns.md) - E-commerce patterns

---

## Example: Brutalist Landing Page

**Input**: "Create a landing page for a tech startup"

**Design Direction**: Brutalist/Raw, bold typography, high contrast

```html
<section class="hero">
  <h1>NO FUTURE</h1>
  <p class="subtext">We build what others fear</p>
  <a href="#contact" class="btn-raw">LET'S TALK</a>
</section>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@700&display=swap');

.hero {
  background: #000;
  color: #fff;
  padding: 15vh 5vw;
  text-align: left;
}

h1 {
  font-family: 'Space Mono', monospace;
  font-size: clamp(4rem, 15vw, 12rem);
  line-height: 0.9;
  letter-spacing: -0.05em;
  margin-bottom: 2rem;
}

.subtext {
  font-family: 'Space Mono', monospace;
  font-size: 1.5rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 3rem;
}

.btn-raw {
  display: inline-block;
  border: 2px solid #fff;
  padding: 1.5rem 3rem;
  font-family: 'Space Mono', monospace;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: #fff;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-raw:hover {
  background: #fff;
  color: #000;
}
</style>
```

---

## Key Principles

1. **Avoid generic fonts**: No Inter, Roboto, Arial—choose distinctive fonts
2. **Clear aesthetic direction**: Commit to ONE style and execute consistently
3. **Color strategy**: Dominant color (60-70%), secondary (20-30%), accent (5-10%)
4. **Motion priorities**: One orchestrated page load > scattered micro-interactions
5. **Spatial composition**: Asymmetry, overlap, diagonal flow, grid-breaking
6. **Background depth**: Gradient meshes, noise textures, geometric patterns, dramatic shadows
7. **Match complexity**: Maximalist needs elaborate code; minimalist needs precision

---

## What to Avoid

NEVER use:
- Generic fonts (Inter, Roboto, Arial)
- Cliched color schemes (purple gradients on white)
- Predictable layouts and component patterns
- Cookie-cutter design without context-specific character

Vary between light/dark themes, different fonts, different aesthetics. NEVER converge on common choices across projects.

---

## See Also

- [aesthetics.md](reference/aesthetics.md) - Complete style guide
- [design_principles.md](reference/design_principles.md) - Detailed implementation principles
- [examples.md](reference/examples.md) - Complete working examples
