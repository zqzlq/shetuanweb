<template>
  <section id="open-source" ref="sectionRef" class="opensource-section">
    <div class="warm-glow" aria-hidden="true"></div>
    <div class="section-deco-line" aria-hidden="true"></div>
    <div class="bg-dots" aria-hidden="true"></div>
    <div class="container">
      <div class="section-heading">
        <p class="eyebrow">OPEN SOURCE</p>
        <h2>{{ config.openSource.title }}</h2>
        <p>{{ config.openSource.description }}</p>
      </div>

      <div class="oss-grid">
        <div v-for="(item, i) in config.openSource.items" :key="i" class="reveal-card oss-card">
          <div class="oss-icon" :style="{ background: dotColors[i] }">
            <svg v-if="i === 0" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2v16M2 10h16" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>
            <svg v-if="i === 1" width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="white" stroke-width="2" fill="none"/><circle cx="10" cy="10" r="2" fill="white"/></svg>
            <svg v-if="i === 2" width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2L3 18h14L10 2z" stroke="white" stroke-width="1.5" fill="none"/></svg>
          </div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <div class="card-bottom-line" :style="{ background: dotColors[i] }"></div>
        </div>
      </div>

      <div class="join-banner reveal-card">
        <div class="banner-glow" aria-hidden="true"></div>
        <div class="banner-pattern" aria-hidden="true"></div>
        <p class="banner-eyebrow">{{ config.openSource.joinBanner.eyebrow }}</p>
        <h3 class="banner-title">{{ config.openSource.joinBanner.title }}</h3>
        <div class="banner-actions">
          <router-link :to="config.openSource.joinBanner.primaryButton.link" class="btn btn-primary">
            {{ config.openSource.joinBanner.primaryButton.text }}
          </router-link>
          <router-link :to="config.openSource.joinBanner.secondaryButton.link" class="btn btn-outline">
            {{ config.openSource.joinBanner.secondaryButton.text }}
          </router-link>
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
const dotColors = ['var(--warm-terracotta)', 'var(--warm-amber)', 'var(--warm-coral)']
useInkReveal(sectionRef)
</script>

<style scoped>
.opensource-section {
  position: relative;
  padding: 100px 0;
  overflow: hidden;
  background: var(--bg-soft);
}

.bg-dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(192, 96, 64, 0.04) 1.5px, transparent 1.5px);
  background-size: 40px 40px;
  pointer-events: none;
}

.warm-glow {
  position: absolute;
  top: 35%;
  right: 8%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(192, 96, 64, 0.06) 0%, transparent 70%);
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

.oss-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  margin-bottom: 56px;
}

.oss-card {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 36px 28px;
  text-align: center;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease, border-color 0.4s ease;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

.oss-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, var(--warm-sage), transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.oss-card:hover {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 24px 64px rgba(120, 90, 60, 0.14);
  border-color: var(--glass-border-hover);
}

.oss-card:hover::after {
  opacity: 0.04;
}

.oss-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.oss-card h3 {
  font-family: var(--font-heading);
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 10px;
  color: var(--text-primary);
}

.oss-card p {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0;
}

.card-bottom-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  opacity: 0.4;
  transition: opacity 0.3s;
}

.oss-card:hover .card-bottom-line {
  opacity: 1;
}

.join-banner {
  text-align: center;
  padding: 64px 40px;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease;
}

.join-banner:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.banner-glow {
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(192, 96, 64, 0.06) 0%, transparent 60%);
  border-radius: 50%;
  filter: blur(40px);
  pointer-events: none;
}

.banner-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(192, 96, 64, 0.02) 1px, transparent 1px);
  background-size: 24px 24px;
  pointer-events: none;
}

.join-banner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--grad-primary);
}

.banner-eyebrow {
  font-family: var(--font-heading);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.15em;
  background: var(--grad-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
  position: relative;
}

.banner-title {
  font-family: var(--font-heading);
  font-size: clamp(1.3rem, 2.5vw, 1.7rem);
  font-weight: 700;
  color: var(--text-primary);
  max-width: 600px;
  margin: 0 auto 28px;
  line-height: 1.4;
  position: relative;
}

.banner-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
  position: relative;
}

@media (max-width: 768px) {
  .oss-grid {
    grid-template-columns: 1fr;
  }
}
</style>
