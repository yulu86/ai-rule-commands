# Frontend Design Examples

Complete working examples demonstrating various design styles and techniques.

---

## Example 1: Luxury Landing Page

**Project**: High-end real estate agency
**Aesthetic**: Luxury/Refined
**Techniques**: Elegant serif typography, generous whitespace, subtle animations

```html
<section class="hero-luxury">
  <div class="content">
    <p class="tag">EST. 1985</p>
    <h1>Beyond</h1>
    <h2>Extraordinary</h2>
    <a href="#properties" class="btn-luxury">Discover More</a>
  </div>
</section>

<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,300;1,600&display=swap');

.hero-luxury {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: #f5f5f0;
  padding: 20vh 5vw;
  position: relative;
  overflow: hidden;
  min-height: 90vh;
  display: flex;
  align-items: center;
}

.content {
  position: relative;
  z-index: 2;
  animation: fadeUp 1s ease forwards;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tag {
  font-family: 'Cormorant Garamond', serif;
  font-size: 0.875rem;
  letter-spacing: 0.3em;
  margin-bottom: 2rem;
  opacity: 0.7;
  font-style: italic;
}

h1 {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(4rem, 10vw, 8rem);
  font-weight: 300;
  font-style: italic;
  line-height: 0.9;
  margin-bottom: 1rem;
}

h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(2rem, 6vw, 4rem);
  font-weight: 600;
  font-style: italic;
  margin-bottom: 4rem;
}

.btn-luxury {
  display: inline-block;
  border: 1px solid rgba(255,255,255,0.3);
  padding: 1.25rem 2.5rem;
  font-size: 0.875rem;
  letter-spacing: 0.2em;
  color: #f5f5f0;
  text-decoration: none;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.btn-luxury::before {
  content: '';
  position: absolute;
  inset: 0;
  background: #c9a96e;
  transform: translateX(-100%);
  transition: transform 0.4s ease;
  z-index: -1;
}

.btn-luxury:hover::before {
  transform: translateX(0);
}

.btn-luxury:hover {
  border-color: #c9a96e;
  color: #1a1a1a;
}

/* Decorative elements */
.hero-luxury::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(201, 169, 110, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.7; }
}
</style>
```

---

## Example 2: Retro-Futuristic Dashboard

**Project**: AI analytics platform
**Aesthetic**: Retro-Futuristic
**Techniques**: Synthwave colors, grid patterns, glow effects, monospace typography

```html
<div class="dashboard-grid">
  <div class="card-glow">
    <h3>SYSTEM STATUS</h3>
    <div class="status-value">OPERATIONAL</div>
    <div class="metrics">
      <div class="metric">
        <span class="metric-label">CPU</span>
        <span class="metric-value">87%</span>
      </div>
      <div class="metric">
        <span class="metric-label">MEM</span>
        <span class="metric-value">4.2GB</span>
      </div>
      <div class="metric">
        <span class="metric-label">UPTIME</span>
        <span class="metric-value">99.9%</span>
      </div>
    </div>
  </div>

  <div class="card-grid">
    <h3>METRICS OVERVIEW</h3>
    <div class="chart-area">
      <div class="bar" style="--height: 60%; --delay: 0.1s"></div>
      <div class="bar" style="--height: 80%; --delay: 0.2s"></div>
      <div class="bar" style="--height: 45%; --delay: 0.3s"></div>
      <div class="bar" style="--height: 90%; --delay: 0.4s"></div>
      <div class="bar" style="--height: 70%; --delay: 0.5s"></div>
    </div>
  </div>

  <div class="card-alerts">
    <h3>RECENT ALERTS</h3>
    <div class="alert-item">
      <span class="alert-time">12:34:56</span>
      <span class="alert-msg">CPU spike detected</span>
    </div>
    <div class="alert-item">
      <span class="alert-time">11:45:23</span>
      <span class="alert-msg">Memory threshold exceeded</span>
    </div>
  </div>
</div>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

:root {
  --neon-blue: #00f0ff;
  --neon-pink: #ff00ff;
  --neon-orange: #ff6b00;
  --bg-dark: #0a0a1a;
  --grid-color: rgba(0, 240, 255, 0.08);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  background: var(--bg-dark);
  padding: 2rem;
  min-height: 100vh;
  background-image:
    linear-gradient(var(--grid-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
  background-size: 50px 50px;
}

.card-glow, .card-grid, .card-alerts {
  background: rgba(10, 10, 26, 0.8);
  border: 1px solid var(--neon-blue);
  padding: 2rem;
  position: relative;
  backdrop-filter: blur(10px);
}

.card-glow::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(45deg, var(--neon-blue), var(--neon-pink), var(--neon-blue));
  z-index: -1;
  filter: blur(8px);
  opacity: 0.6;
  animation: rotate 4s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

h3 {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  color: var(--neon-blue);
  margin-bottom: 1.5rem;
  text-transform: uppercase;
}

.status-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 2.5rem;
  color: var(--neon-pink);
  text-shadow: 0 0 10px var(--neon-pink), 0 0 20px var(--neon-pink);
  margin-bottom: 2rem;
  animation: flicker 3s ease-in-out infinite;
}

@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
  52% { opacity: 1; }
  54% { opacity: 0.85; }
}

.metrics {
  display: grid;
  gap: 1rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(0, 240, 255, 0.2);
}

.metric-label {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.75rem;
  color: var(--neon-blue);
  letter-spacing: 0.1em;
}

.metric-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 1rem;
  color: #fff;
}

.chart-area {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  height: 150px;
}

.bar {
  flex: 1;
  background: linear-gradient(180deg, var(--neon-blue) 0%, var(--neon-pink) 100%);
  height: var(--height);
  border-radius: 2px;
  animation: growUp 0.8s ease forwards;
  animation-delay: var(--delay);
  opacity: 0;
}

@keyframes growUp {
  from {
    opacity: 0;
    transform: scaleY(0);
  }
  to {
    opacity: 1;
    transform: scaleY(1);
  }
}

.alert-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 0, 255, 0.2);
  font-family: 'Orbitron', sans-serif;
  font-size: 0.75rem;
}

.alert-time {
  color: var(--neon-blue);
  letter-spacing: 0.1em;
}

.alert-msg {
  color: #fff;
}
</style>
```

---

## Example 3: Organic Portfolio

**Project**: Wellness coach portfolio
**Aesthetic**: Organic/Natural
**Techniques**: Soft curves, earth tones, layered transparencies, subtle motion

```html
<section class="hero-organic">
  <div class="floating-shapes">
    <div class="shape shape-1"></div>
    <div class="shape shape-2"></div>
    <div class="shape shape-3"></div>
  </div>

  <div class="content">
    <h1 class="fade-up">Find Your Balance</h1>
    <p class="fade-up">A journey to wellness, one breath at a time</p>
    <a href="#about" class="btn-organic fade-up">Start Your Journey</a>
  </div>
</section>

<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;500;700&display=swap');

:root {
  --sage: #90a955;
  --terracotta: #d4a373;
  --cream: #f5f0e8;
  --brown: #8b7355;
  --soft-pink: #f5e6e6;
}

.hero-organic {
  background: var(--cream);
  padding: 10vh 5vw;
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.floating-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.6;
  filter: blur(40px);
}

.shape-1 {
  width: 400px;
  height: 400px;
  background: var(--sage);
  top: 10%;
  right: 10%;
  animation: float 8s ease-in-out infinite;
}

.shape-2 {
  width: 300px;
  height: 300px;
  background: var(--soft-pink);
  bottom: 20%;
  left: 5%;
  animation: float 10s ease-in-out infinite reverse;
}

.shape-3 {
  width: 250px;
  height: 250px;
  background: var(--terracotta);
  top: 50%;
  left: 50%;
  animation: float 12s ease-in-out infinite;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(30px, -30px) rotate(5deg); }
  50% { transform: translate(-20px, 20px) rotate(-5deg); }
  75% { transform: translate(20px, 10px) rotate(3deg); }
}

.content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 600px;
}

h1 {
  font-family: 'Quicksand', sans-serif;
  font-size: clamp(2.5rem, 6vw, 5rem);
  font-weight: 700;
  color: var(--brown);
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.content p {
  font-family: 'Quicksand', sans-serif;
  font-size: 1.25rem;
  color: var(--brown);
  opacity: 0.8;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.btn-organic {
  display: inline-block;
  background: var(--sage);
  color: var(--cream);
  padding: 1rem 2.5rem;
  border-radius: 2rem;
  font-family: 'Quicksand', sans-serif;
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(144, 169, 85, 0.3);
}

.btn-organic:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(144, 169, 85, 0.4);
}

.fade-up {
  opacity: 0;
  animation: fadeUp 0.8s ease forwards;
}

.fade-up:nth-child(1) { animation-delay: 0.1s; }
.fade-up:nth-child(2) { animation-delay: 0.3s; }
.fade-up:nth-child(3) { animation-delay: 0.5s; }

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
</style>
```

---

## Example 4: Brutalist Card Grid

**Project**: Creative agency portfolio
**Aesthetic**: Brutalist/Raw
**Techniques**: Sharp edges, monospace typography, high contrast, grid layout

```html
<section class="brutalist-grid">
  <div class="header">
    <h1>THE COLLECTIVE</h1>
    <p class="subline">WE BREAK RULES. YOU BREAK BARRIERS.</p>
  </div>

  <div class="grid">
    <div class="card">
      <div class="card-number">01</div>
      <h3>Digital</h3>
      <p>We craft digital experiences that challenge conventions and redefine possibilities.</p>
    </div>

    <div class="card card-offset">
      <div class="card-number">02</div>
      <h3>Brand</h3>
      <p>Identities that don't just exist—they dominate conversations.</p>
    </div>

    <div class="card">
      <div class="card-number">03</div>
      <h3>Motion</h3>
      <p>Animation that captures attention and refuses to let go.</p>
    </div>

    <div class="card card-large">
      <div class="card-number">04</div>
      <h3>Strategy</h3>
      <p>Insight-driven approaches that cut through the noise and deliver results that matter.</p>
    </div>
  </div>
</section>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

.brutalist-grid {
  background: #000;
  color: #fff;
  padding: 6rem 4rem;
}

.header {
  margin-bottom: 6rem;
}

h1 {
  font-family: 'Space Mono', monospace;
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 700;
  line-height: 0.9;
  letter-spacing: -0.05em;
  margin-bottom: 1.5rem;
}

.subline {
  font-family: 'Space Mono', monospace;
  font-size: 1.25rem;
  color: #ff3333;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 0;
  border-top: 2px solid #fff;
}

.card {
  border: 2px solid #fff;
  border-top: none;
  padding: 3rem;
  grid-column: span 4;
  position: relative;
}

.card-offset {
  grid-column: 2 / span 6;
  transform: translateY(-2rem);
  z-index: 10;
  border-bottom: 2px solid #ff3333;
}

.card-large {
  grid-column: span 12;
  padding: 4rem;
}

.card-number {
  font-family: 'Space Mono', monospace;
  font-size: 4rem;
  font-weight: 700;
  color: #ff3333;
  margin-bottom: 2rem;
  line-height: 0.9;
}

.card h3 {
  font-family: 'Space Mono', monospace;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  letter-spacing: 0.05em;
}

.card p {
  font-family: 'Space Mono', monospace;
  font-size: 1rem;
  line-height: 1.6;
  opacity: 0.8;
}

.card:hover {
  background: #fff;
  color: #000;
}

.card:hover .card-number {
  color: #ff3333;
}

@media (max-width: 900px) {
  .brutalist-grid {
    padding: 3rem 2rem;
  }

  .card, .card-offset, .card-large {
    grid-column: span 12;
    transform: none;
  }
}
</style>
```

---

## Key Patterns from Examples

### 1. Font Import Pattern

Always import distinctive fonts:
```css
@import url('https://fonts.googleapis.com/css2?family=FontName:wght@...;display=swap');
```

### 2. CSS Variables Pattern

Define theme variables for consistency:
```css
:root {
  --color-primary: #1a1a1a;
  --color-accent: #ff6b35;
  --font-display: 'Font Name', serif;
  --font-body: 'Font Name', sans-serif;
}
```

### 3. Staggered Animation Pattern

Create orchestration with delays:
```css
.stagger-item {
  opacity: 0;
  animation: fadeUp 0.6s ease forwards;
}

.stagger-item:nth-child(1) { animation-delay: 0.1s; }
.stagger-item:nth-child(2) { animation-delay: 0.2s; }
```

### 4. Hover State Pattern

Create surprising interactions:
```css
.button {
  transition: all 0.3s ease;
}

.button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(..., 0.4);
}
```

### 5. Grid Breaking Pattern

Break alignment for visual interest:
```css
.card-standard {
  grid-column: span 4;
}

.card-offset {
  grid-column: 2 / span 6;
  transform: translateY(-2rem);
  z-index: 10;
}

.card-span {
  grid-column: span 12;
}
```

---

## See Also

- [aesthetics.md](./aesthetics.md) - Design style selection guide
- [design_principles.md](./design_principles.md) - Detailed implementation principles
