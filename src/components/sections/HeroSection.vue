<template>
  <section class="hero" ref="heroRef">
    <div class="hero-deco-line" aria-hidden="true"></div>
    <div class="hero-grid-dots" aria-hidden="true"></div>
    <div class="hero-float hero-float-1" aria-hidden="true"></div>
    <div class="hero-float hero-float-2" aria-hidden="true"></div>
    <div class="hero-float hero-float-3" aria-hidden="true"></div>
    <div class="container hero-inner">
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-dot"></span>
          <span>{{ config.hero.eyebrow }}</span>
        </div>
        <h1 class="hero-title">
          <span v-for="(word, i) in titleWords" :key="i" class="title-word">{{ word }}</span>
        </h1>
        <p class="hero-desc">{{ config.hero.description }}</p>
        <div class="hero-actions">
          <router-link to="/projects" class="btn btn-primary">
            <span>查看作品</span>
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </router-link>
          <a href="#about" class="btn btn-outline">了解社团</a>
        </div>
        <ul class="hero-stats">
          <li v-for="(stat, i) in config.hero.stats" :key="i" class="stat-item">
            <strong><CountUp :target="stat.value" /></strong>
            <span>{{ stat.label }}</span>
          </li>
        </ul>
      </div>
      <div class="hero-visual">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="visual-ring"></div>
        <div class="visual-ring visual-ring-2"></div>
        <div class="signal-card">
          <p class="signal-eyebrow">{{ config.hero.signalCard.eyebrow }}</p>
          <strong class="signal-title">{{ config.hero.signalCard.title }}</strong>
          <span class="signal-desc">{{ config.hero.signalCard.description }}</span>
          <div class="signal-bar">
            <div class="signal-bar-fill"></div>
          </div>
        </div>
        <div class="float-card float-card-1">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1l2 5h5l-4 3 1.5 5L8 11l-4.5 3L5 9 1 6h5l2-5z" fill="var(--warm-amber)"/></svg>
          <span>精选项目</span>
        </div>
        <div class="float-card float-card-2">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="var(--warm-sage)" stroke-width="1.5" fill="none"/><path d="M5.5 8l2 2 3.5-3.5" stroke="var(--warm-sage)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span>开源协作</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { useSiteConfigStore } from '@/stores/siteConfig'
import CountUp from '@/components/effects/CountUp.vue'

const { config } = useSiteConfigStore()
const heroRef = ref(null)
let ctx

const titleWords = computed(() => config.hero.title.split(/(?<=[^\s])\s+/))

onMounted(() => {
  if (!heroRef.value) return
  ctx = gsap.context(() => {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })

    tl.from('.hero-badge', { opacity: 0, x: -40, duration: 0.6 })
      .from('.title-word', { opacity: 0, y: 60, rotateX: 15, duration: 0.9, stagger: 0.12 }, '-=0.2')
      .from('.hero-desc', { opacity: 0, y: 30, duration: 0.6 }, '-=0.4')
      .from('.hero-actions .btn', { opacity: 0, y: 20, scale: 0.9, duration: 0.5, stagger: 0.1 }, '-=0.3')
      .from('.stat-item', { opacity: 0, y: 25, duration: 0.5, stagger: 0.08 }, '-=0.3')
      .from('.visual-ring', { scale: 0, opacity: 0, duration: 1, ease: 'back.out(1.5)' }, '-=0.8')
      .from('.signal-card', { opacity: 0, y: 30, scale: 0.9, duration: 0.8, ease: 'back.out(1.3)' }, '-=0.6')
      .from('.float-card', { opacity: 0, scale: 0.8, duration: 0.6, stagger: 0.15 }, '-=0.4')
      .from('.hero-float', { opacity: 0, scale: 0.5, duration: 0.8, stagger: 0.1 }, '-=0.6')
      .from('.hero-deco-line', { scaleX: 0, duration: 1.5, ease: 'power2.inOut' }, '-=1.2')
      .from('.hero-grid-dots', { opacity: 0, duration: 1 }, '-=1')
  }, heroRef.value)
})

onUnmounted(() => { ctx?.revert() })
</script>

<style scoped>
.hero {
  padding: 140px 0 100px;
  position: relative;
  overflow: hidden;
}

.hero-deco-line {
  position: absolute;
  bottom: 0;
  left: 5%;
  right: 5%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(192, 96, 64, 0.15), var(--glass-border), rgba(212, 146, 10, 0.1), transparent);
  transform-origin: center;
}

.hero-grid-dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(192, 96, 64, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 60% 60% at 70% 40%, black, transparent);
  -webkit-mask-image: radial-gradient(ellipse 60% 60% at 70% 40%, black, transparent);
  pointer-events: none;
}

.hero-float {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}

.hero-float-1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: -60px;
  background: radial-gradient(circle, rgba(212, 146, 10, 0.08) 0%, transparent 70%);
  animation: hero-float-anim 12s ease-in-out infinite alternate;
}

.hero-float-2 {
  width: 160px;
  height: 160px;
  bottom: 15%;
  right: -40px;
  background: radial-gradient(circle, rgba(192, 96, 64, 0.1) 0%, transparent 70%);
  animation: hero-float-anim 10s ease-in-out infinite alternate-reverse;
}

.hero-float-3 {
  width: 120px;
  height: 120px;
  top: 60%;
  left: 40%;
  background: radial-gradient(circle, rgba(122, 154, 106, 0.07) 0%, transparent 70%);
  animation: hero-float-anim 14s ease-in-out infinite alternate;
}

@keyframes hero-float-anim {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(20px, -15px) scale(1.1); }
}

.hero-inner {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 60px;
  align-items: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  background: rgba(192, 96, 64, 0.08);
  border: 1px solid rgba(192, 96, 64, 0.12);
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: var(--warm-terracotta);
  margin-bottom: 24px;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--warm-terracotta);
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.4); }
}

.hero-title {
  font-size: clamp(2.4rem, 5.5vw, 3.8rem);
  line-height: 1.12;
  margin-bottom: 24px;
  color: var(--text-primary);
  letter-spacing: -0.025em;
  display: flex;
  flex-wrap: wrap;
  gap: 0 14px;
}

.title-word {
  display: inline-block;
  perspective: 400px;
}

.hero-desc {
  font-size: 17px;
  line-height: 1.8;
  color: var(--text-secondary);
  max-width: 540px;
  margin-bottom: 36px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  margin-bottom: 56px;
}

.hero-actions .btn svg {
  transition: transform 0.3s;
}

.hero-actions .btn:hover svg {
  transform: translateX(3px);
}

.hero-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  position: relative;
}

.stat-item:not(:last-child)::after {
  content: '';
  position: absolute;
  right: -20px;
  top: 4px;
  bottom: 4px;
  width: 1px;
  background: var(--glass-border);
}

.stat-item strong {
  font-family: var(--font-heading);
  font-size: 32px;
  font-weight: 700;
  background: var(--grad-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-item span {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
}

.hero-visual {
  position: relative;
  height: 400px;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  will-change: transform;
  animation: orb-float 10s ease-in-out infinite alternate;
}

.orb-1 {
  width: 200px;
  height: 200px;
  top: -20px;
  right: -20px;
  background: rgba(192, 96, 64, 0.15);
  filter: blur(50px);
}

.orb-2 {
  width: 150px;
  height: 150px;
  bottom: 0;
  left: 0;
  background: rgba(212, 146, 10, 0.12);
  filter: blur(45px);
  animation-delay: 3s;
}

@keyframes orb-float {
  0% { transform: translate(0, 0); }
  100% { transform: translate(8px, -10px); }
}

.visual-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 280px;
  height: 280px;
  border-radius: 50%;
  border: 1px solid rgba(192, 96, 64, 0.12);
  animation: ring-rotate 20s linear infinite;
}

.visual-ring::before {
  content: '';
  position: absolute;
  top: -5px;
  left: 50%;
  width: 10px;
  height: 10px;
  background: var(--warm-terracotta);
  border-radius: 50%;
  transform: translateX(-50%);
}

.visual-ring-2 {
  width: 340px;
  height: 340px;
  border-color: rgba(212, 146, 10, 0.08);
  animation-direction: reverse;
  animation-duration: 30s;
}

.visual-ring-2::before {
  background: var(--warm-amber);
  width: 8px;
  height: 8px;
  top: -4px;
}

@keyframes ring-rotate {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

.signal-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 270px;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  padding: 32px;
  box-shadow: var(--shadow-xl);
  z-index: 1;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease;
}

.signal-card:hover {
  transform: translate(-50%, -50%) scale(1.04);
  box-shadow: 0 24px 72px rgba(120, 90, 60, 0.18);
}

.signal-card::before {
  content: '';
  position: absolute;
  top: -1px;
  left: 24px;
  right: 24px;
  height: 3px;
  background: var(--grad-primary);
  border-radius: 0 0 3px 3px;
}

.signal-eyebrow {
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  background: var(--grad-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 14px;
}

.signal-title {
  display: block;
  font-family: var(--font-heading);
  font-size: 26px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.signal-desc {
  font-size: 13px;
  color: var(--text-secondary);
  display: block;
  margin-bottom: 16px;
}

.signal-bar {
  height: 4px;
  background: var(--surface);
  border-radius: 2px;
  overflow: hidden;
}

.signal-bar-fill {
  height: 100%;
  width: 0;
  background: var(--grad-primary);
  border-radius: 2px;
  animation: bar-fill 2.5s 1.5s ease-out forwards;
}

@keyframes bar-fill {
  0% { width: 0; }
  100% { width: 72%; }
}

.float-card {
  position: absolute;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  box-shadow: var(--shadow-md);
  z-index: 2;
  animation: float-bob 4s ease-in-out infinite alternate;
}

.float-card-1 {
  top: 10%;
  right: -10px;
  animation-delay: 0s;
}

.float-card-2 {
  bottom: 15%;
  left: -10px;
  animation-delay: 2s;
}

@keyframes float-bob {
  0% { transform: translateY(0); }
  100% { transform: translateY(-10px); }
}

@media (max-width: 900px) {
  .hero-inner {
    grid-template-columns: 1fr;
  }
  .hero-visual {
    display: none;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 100px 0 60px;
  }
  .hero-stats {
    gap: 24px;
  }
  .stat-item:not(:last-child)::after {
    display: none;
  }
  .hero-actions {
    flex-direction: column;
  }
}
</style>
