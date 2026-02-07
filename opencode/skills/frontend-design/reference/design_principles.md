# Design Principles

Core design principles for creating distinctive, production-grade frontend interfaces.

---

## Typography

### Font Selection Rules

1. **Avoid generic fonts**: Inter, Roboto, Arial, system fonts are overused
2. **Choose characterful fonts**: Select fonts with personality and uniqueness
3. **Pair display + body fonts**: One distinctive display font, one refined body font
4. **Consider readability**: Body fonts should be clean and legible at small sizes

### Display Fonts (Headings)

Use for headings and large text. Choose fonts that:
- Have distinctive character shapes
- Support wide letter-spacing for style
- Look good at large sizes (3rem+)

**Recommended Display Fonts:**
- Luxury: Playfair Display, Cormorant Garamond, Lust
- Brutalist: Space Mono, VT323, Roboto Mono
- Retro: Orbitron, Press Start 2P, VT323
- Organic: Quicksand, Poppins, Nunito
- Maximalist: Abril Fatface, Lust, Playfair Display

### Body Fonts (Paragraphs)

Use for body text and interface elements. Choose fonts that:
- Are highly readable at 14-16px
- Have good spacing and legibility
- Support multiple weights

**Recommended Body Fonts:**
- Serif: Lora, Crimson Text, Merriweather
- Sans-serif: DM Sans, IBM Plex Sans, Source Sans Pro
- Monospace: JetBrains Mono, Fira Code

### Typography Hierarchy

```css
/* Hero Title */
.hero-title {
  font-size: clamp(4rem, 15vw, 12rem);
  line-height: 0.9;
  letter-spacing: -0.05em;
  font-weight: 700;
}

/* Section Heading */
.section-heading {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
  font-weight: 600;
}

/* Body Text */
.body-text {
  font-size: 1.125rem;
  line-height: 1.6;
  letter-spacing: 0.01em;
  font-weight: 400;
}

/* Micro Text */
.micro-text {
  font-size: 0.875rem;
  line-height: 1.4;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-weight: 500;
}
```

---

## Color & Theme

### Color Strategy

Use a balanced color palette:

- **Dominant color**: 60-70% of surface area
- **Secondary color**: 20-30% of surface area
- **Accent color**: 5-10% of surface area

### CSS Variables for Consistency

```css
:root {
  /* Brand Colors */
  --color-primary: #1a1a1a;
  --color-secondary: #e0e0e0;
  --color-accent: #ff6b35;

  /* Semantic Colors */
  --color-text: #1a1a1a;
  --color-bg: #fafafa;
  --color-surface: #ffffff;
  --color-border: #e0e0e0;

  /* Functional Colors */
  --color-success: #059669;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-info: #2563eb;
}
```

### Color Harmony Examples

**Monochromatic (Minimalist)**:
```css
:root {
  --color-1: #000000;
  --color-2: #333333;
  --color-3: #666666;
  --color-4: #999999;
  --color-5: #ffffff;
}
```

**Complementary (Brutalist)**:
```css
:root {
  --color-primary: #000000;
  --color-accent: #ff3333;
  --color-contrast: #ffffff;
}
```

**Analogous (Organic)**:
```css
:root {
  --color-1: #556b2f;  /* Olive */
  --color-2: #6b8e23;  /* Olive Drab */
  --color-3: #90a955;  /* Sage */
  --color-4: #b5c689;  /* Light Sage */
}
```

**Triadic (Retro-Futuristic)**:
```css
:root {
  --color-1: #00f0ff;  /* Cyan */
  --color-2: #ff00ff;  /* Magenta */
  --color-3: #ffff00;  /* Yellow */
  --color-bg: #0a0a1a; /* Dark Blue */
}
```

### Theme Variations

**Light Theme**:
```css
:root {
  --color-bg: #ffffff;
  --color-surface: #f5f5f5;
  --color-text: #1a1a1a;
}
```

**Dark Theme**:
```css
:root {
  --color-bg: #1a1a1a;
  --color-surface: #2d2d2d;
  --color-text: #f5f5f0;
}
```

---

## Motion & Animation

### Animation Timing

Use different timings for different purposes:

```css
/* Micro-interactions (hover, focus) */
.duration-fast {
  transition: all 0.2s ease;
}

/* Page transitions */
.duration-medium {
  transition: all 0.4s ease;
}

/* Major animations (page load, modals) */
.duration-slow {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Staggered Reveals

Create orchestration with staggered delays:

```css
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stagger-item {
  animation: fadeUp 0.6s ease forwards;
  opacity: 0;
}

.stagger-item:nth-child(1) { animation-delay: 0.1s; }
.stagger-item:nth-child(2) { animation-delay: 0.2s; }
.stagger-item:nth-child(3) { animation-delay: 0.3s; }
.stagger-item:nth-child(4) { animation-delay: 0.4s; }
```

### Scroll Animations

Use Intersection Observer for scroll-triggered animations:

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});
```

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(50px);
  transition: all 0.6s ease;
}

.animate-on-scroll.animate-in {
  opacity: 1;
  transform: translateY(0);
}
```

### Hover States

Create surprising hover interactions:

```css
.button {
  position: relative;
  overflow: hidden;
  transition: color 0.3s ease;
}

.button::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-accent);
  transform: translateY(100%);
  transition: transform 0.3s ease;
  z-index: -1;
}

.button:hover::after {
  transform: translateY(0);
}

.button:hover {
  color: #fff;
}
```

---

## Spatial Composition

### Layout Principles

1. **Asymmetry over symmetry**: Creates visual interest and movement
2. **Overlap elements**: Adds depth and layering
3. **Diagonal flow**: Creates dynamic energy
4. **Generous whitespace OR controlled density**: Choose one, don't split the difference

### CSS Grid Breaking

Break the grid intentionally for visual impact:

```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
}

/* Standard grid item */
.grid-item-standard {
  grid-column: span 4;
}

/* Offset item - breaks alignment */
.grid-item-offset {
  grid-column: 2 / span 6;  /* Starts at column 2 */
  transform: translateY(-2rem);
}

/* Spanning item - creates emphasis */
.grid-item-span {
  grid-column: span 12;
}

/* Overlap effect */
.grid-item-overlap {
  grid-column: 4 / span 8;
  margin-top: -4rem;
  z-index: 10;
}
```

### Negative Space

Use generous spacing for luxury or minimal aesthetics:

```css
.section-luxury {
  padding: clamp(4rem, 10vw, 8rem) clamp(2rem, 5vw, 4rem);
}

.gap-luxury {
  gap: clamp(2rem, 5vw, 4rem);
}
```

### Controlled Density

Use tight spacing for maximalist or brutalist aesthetics:

```css
.section-dense {
  padding: 1.5rem;
  gap: 0.5rem;
}

.grid-dense {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.25rem;
}
```

---

## Backgrounds & Visual Details

### Gradient Meshes

Create organic color backgrounds:

```css
.gradient-mesh {
  background:
    radial-gradient(at 40% 20%, hsla(262, 75%, 50%, 0.3) 0px, transparent 50%),
    radial-gradient(at 80% 0%, hsla(189, 75%, 50%, 0.3) 0px, transparent 50%),
    radial-gradient(at 0% 50%, hsla(342, 75%, 50%, 0.3) 0px, transparent 50%),
    radial-gradient(at 80% 50%, hsla(262, 75%, 50%, 0.3) 0px, transparent 50%),
    radial-gradient(at 0% 100%, hsla(189, 75%, 50%, 0.3) 0px, transparent 50%),
    radial-gradient(at 80% 100%, hsla(342, 75%, 50%, 0.3) 0px, transparent 50%),
    linear-gradient(135deg, #0a0a1a 0%, #1a0a2a 100%);
}
```

### Noise Textures

Add grain for texture:

```css
.noise-overlay {
  position: relative;
}

.noise-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.05;
  pointer-events: none;
}
```

### Geometric Patterns

Create structured backgrounds:

```css
.grid-pattern {
  background-image:
    linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
}

.dot-pattern {
  background-image: radial-gradient(rgba(255,255,255,0.2) 2px, transparent 2px);
  background-size: 20px 20px;
}
```

### Layered Transparencies

Create depth with multiple semi-transparent layers:

```css
.layered-bg {
  background:
    linear-gradient(180deg, rgba(26, 26, 26, 0.8) 0%, rgba(45, 45, 45, 0.8) 100%),
    radial-gradient(circle at 30% 20%, rgba(255, 107, 53, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 70% 80%, rgba(0, 240, 255, 0.15) 0%, transparent 50%),
    #1a1a1a;
}
```

### Dramatic Shadows

Use deep, colored shadows for impact:

```css
.shadow-dramatic {
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.1),
    0 20px 50px -10px rgba(0,0,0,0.5),
    0 30px 60px -30px rgba(0,240,255,0.3);
}

.shadow-glow {
  box-shadow:
    0 0 0 1px rgba(0,240,255,0.3),
    0 0 20px rgba(0,240,255,0.2),
    0 0 40px rgba(0,240,255,0.1);
}
```

### Decorative Borders

Add styled borders for visual interest:

```css
.border-gradient {
  border: 2px solid transparent;
  background: linear-gradient(#1a1a1a, #1a1a1a) padding-box,
              linear-gradient(135deg, #00f0ff, #ff00ff) border-box;
}

.border-dashed {
  border: 2px dashed rgba(255,255,255,0.3);
  border-radius: 1rem;
}

.border-fancy {
  border: 1px solid;
  border-image: linear-gradient(135deg, #c9a96e, #d4af37, #c9a96e) 1;
}
```

---

## Custom Cursors

Add custom cursors for unique interactions:

```css
body {
  cursor: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='12' cy='12' r='6' fill='%23ff3333'/%3E%3C/svg%3E") 12 12, auto;
}

.interactive {
  cursor: url("data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='12' cy='12' r='8' fill='none' stroke='%2300f0ff' stroke-width='2'/%3E%3C/svg%3E") 12 12, pointer;
}
```

---

## See Also

- [aesthetics.md](./aesthetics.md) - Design style selection guide
- [examples.md](./examples.md) - Complete working examples
