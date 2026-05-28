<template>
  <section id="about" ref="sectionRef" class="about-section">
    <div class="warm-glow" aria-hidden="true"></div>
    <div class="section-deco-line" aria-hidden="true"></div>
    <div class="bg-pattern" aria-hidden="true"></div>
    <div class="container">
      <div class="section-heading">
        <p class="eyebrow">ABOUT</p>
        <div class="heading-row">
          <h2>{{ config.about.title }}</h2>
          <router-link to="/about" class="btn btn-outline btn-sm">了解更多</router-link>
        </div>
        <p>{{ config.about.description }}</p>
      </div>
      <div class="about-grid">
        <div v-for="(item, i) in config.about.items" :key="i" class="reveal-card about-card" :style="{ '--delay': i * 0.1 + 's' }">
          <div class="card-top">
            <span class="card-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <div class="card-icon" :style="{ background: accentColors[i] }">
              <svg v-if="i === 0" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2L12.9 7.6L19 8.5L14.5 12.9L15.7 19L10 16L4.3 19L5.5 12.9L1 8.5L7.1 7.6L10 2Z" fill="white"/></svg>
              <svg v-if="i === 1" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 1C5 1 1 5 1 10s4 9 9 9 9-4 9-9-4-9-9-9zm0 16c-3.9 0-7-3.1-7-7s3.1-7 7-7 7 3.1 7 7-3.1 7-7 7z" fill="white"/><path d="M8 10l2 2 4-4" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <svg v-if="i === 2" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 18.3s-7-4.7-7-9.5C3 5 6.1 2 10 2s7 3 7 6.8c0 4.8-7 9.5-7 9.5z" fill="white"/></svg>
            </div>
          </div>
          <div class="card-accent" :style="{ background: accentColors[i] }"></div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <div class="card-corner" aria-hidden="true"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useInkReveal } from '@/composables/useInkReveal'

const { config } = useSiteConfigStore()
const sectionRef = ref(null)
const accentColors = ['var(--warm-terracotta)', 'var(--warm-amber)', 'var(--warm-coral)']
useInkReveal(sectionRef)
</script>

<style scoped>
.about-section {
  position: relative;
  padding: 100px 0;
  overflow: hidden;
}

.bg-pattern {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 20% 80%, rgba(192, 96, 64, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(212, 146, 10, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

.warm-glow {
  position: absolute;
  top: 35%;
  left: 10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(192, 96, 64, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  filter: blur(40px);
  pointer-events: none;
}

.section-deco-line {
  position: absolute;
  top: 0;
  left: 8%;
  right: 8%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(192, 96, 64, 0.12), var(--glass-border), rgba(212, 146, 10, 0.08), transparent);
  transform-origin: center;
}

.heading-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 13px;
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

.about-card {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 0 28px 28px;
  position: relative;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease, border-color 0.4s ease;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.about-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, var(--warm-terracotta), transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.about-card:hover {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 24px 64px rgba(120, 90, 60, 0.14);
  border-color: var(--glass-border-hover);
}

.about-card:hover::after {
  opacity: 0.04;
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 0 20px;
}

.card-num {
  font-family: var(--font-heading);
  font-size: 48px;
  font-weight: 700;
  color: rgba(192, 96, 64, 0.06);
  line-height: 1;
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.card-corner {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, transparent 50%, rgba(192, 96, 64, 0.04) 50%);
  pointer-events: none;
}

.about-card h3 {
  font-family: var(--font-heading);
  font-size: 19px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.about-card p {
  font-size: 14px;
  line-height: 1.8;
  color: var(--text-secondary);
  margin: 0;
}

@media (max-width: 768px) {
  .about-grid {
    grid-template-columns: 1fr;
  }
}
</style>
