<template>
  <section id="members" ref="sectionRef" class="members-section">
    <div class="warm-glow" aria-hidden="true"></div>
    <div class="section-deco-line" aria-hidden="true"></div>
    <div class="bg-grid" aria-hidden="true"></div>
    <div class="container">
      <div class="section-heading">
        <p class="eyebrow">MEMBERS</p>
        <div class="heading-row">
          <h2>{{ config.members.title }}</h2>
          <router-link to="/members" class="btn btn-outline btn-sm">了解更多</router-link>
        </div>
        <p>{{ config.members.description }}</p>
      </div>
      <div class="members-grid">
        <div v-for="(group, i) in config.members.groups" :key="i" class="reveal-card group-card" :style="{ '--accent': groupColors[i] }">
          <div class="group-glow"></div>
          <div class="group-icon-ring">
            <span class="group-icon-inner" :style="{ background: groupColors[i] }">
              <svg v-if="i === 0" width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M9 1L11.5 6.5L17 7.2L13 11.1L14 17L9 14.2L4 17L5 11.1L1 7.2L6.5 6.5L9 1Z" fill="white"/></svg>
              <svg v-if="i === 1" width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="7" stroke="white" stroke-width="1.5" fill="none"/><path d="M6 9h6M9 6v6" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg>
              <svg v-if="i === 2" width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M9 1v16M1 9h16" stroke="white" stroke-width="1.5" stroke-linecap="round"/><circle cx="9" cy="9" r="3" fill="white"/></svg>
              <svg v-if="i === 3" width="18" height="18" viewBox="0 0 18 18" fill="none"><rect x="2" y="2" width="14" height="14" rx="3" stroke="white" stroke-width="1.5" fill="none"/><path d="M6 9h6" stroke="white" stroke-width="1.5" stroke-linecap="round"/></svg>
            </span>
          </div>
          <span class="group-tag">{{ group.tag }}</span>
          <h3 class="group-name">{{ group.name }}</h3>
          <p class="group-desc">{{ group.description }}</p>
          <div class="group-line" :style="{ background: groupColors[i] }"></div>
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
const groupColors = ['var(--warm-terracotta)', 'var(--warm-coral)', 'var(--warm-amber)', 'var(--warm-sage)']
useInkReveal(sectionRef)
</script>

<style scoped>
.members-section {
  position: relative;
  padding: 100px 0;
  overflow: hidden;
  background: var(--bg-soft);
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(192, 96, 64, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(192, 96, 64, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
}

.warm-glow {
  position: absolute;
  top: 25%;
  right: 5%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(192, 112, 128, 0.08) 0%, transparent 70%);
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

.members-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.group-card {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 40px 24px 32px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease, border-color 0.4s ease;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  box-shadow: var(--shadow-sm);
}

.group-glow {
  position: absolute;
  top: -40%;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 180px;
  background: var(--accent);
  opacity: 0.04;
  border-radius: 50%;
  filter: blur(50px);
  transition: opacity 0.4s, width 0.4s, height 0.4s;
}

.group-card:hover {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 24px 64px rgba(120, 90, 60, 0.14);
  border-color: var(--accent);
}

.group-card:hover .group-glow {
  opacity: 0.15;
  width: 220px;
  height: 220px;
}

.group-icon-ring {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  margin-bottom: 4px;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.group-card:hover .group-icon-ring {
  transform: scale(1.1);
}

.group-icon-inner {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.group-tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
}

.group-name {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.group-desc {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0;
}

.group-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  opacity: 0.4;
  transition: opacity 0.3s;
}

.group-card:hover .group-line {
  opacity: 1;
}

@media (max-width: 900px) {
  .members-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .members-grid {
    grid-template-columns: 1fr;
  }
}
</style>
