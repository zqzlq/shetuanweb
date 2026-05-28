<template>
  <section id="awards" ref="sectionRef" class="awards-section">
    <div class="warm-glow" aria-hidden="true"></div>
    <div class="section-deco-line" aria-hidden="true"></div>
    <div class="bg-dots" aria-hidden="true"></div>
    <div class="container">
      <div class="section-heading">
        <p class="eyebrow">AWARDS</p>
        <div class="heading-row">
          <h2>{{ page.content.awards.title }}</h2>
          <router-link to="/projects/awards" class="btn btn-outline btn-sm">查看全部</router-link>
        </div>
        <p>{{ page.content.awards.description }}</p>
      </div>

      <div class="awards-grid">
        <router-link
          v-for="a in awards"
          :key="a.slug"
          :to="`/awards/${a.slug}`"
          class="award-card-link"
        >
          <div class="award-card">
            <div class="award-glow" aria-hidden="true"></div>
            <img v-if="a.image" :src="a.image" :alt="a.title" class="award-image" />
            <div class="award-icon">
              <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                <path d="M14 2l3.5 7.7L26 10.8l-5.5 5.4L22 24l-8-4.2L6 24l1.5-7.8L2 10.8l8.5-1.1L14 2z" fill="var(--warm-amber)" stroke="var(--warm-amber)" stroke-width="1" stroke-linejoin="round"/>
              </svg>
            </div>
            <span class="tag tag-accent">{{ a.category }}</span>
            <span class="award-level">{{ a.level }}</span>
            <h3>{{ a.title }}</h3>
            <p>{{ a.shortDesc }}</p>
            <div class="award-meta">
              <span class="award-date">{{ a.date }}</span>
              <span class="award-participants">{{ a.participants.join('、') }}</span>
            </div>
            <div class="award-accent-line" aria-hidden="true"></div>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useInkReveal } from '@/composables/useInkReveal'

const store = useSiteConfigStore()
const page = store.getPage('projects')
const sectionRef = ref(null)
useInkReveal(sectionRef)

const awards = computed(() => (page?.content?.awards?.items || []).slice(0, 3))
</script>

<style scoped>
.awards-section {
  position: relative;
  padding: 100px 0;
  overflow: hidden;
  background: var(--bg-soft);
}

.bg-dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(192, 96, 64, 0.04) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
}

.warm-glow {
  position: absolute;
  top: 30%;
  right: 10%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(212, 146, 10, 0.08) 0%, transparent 70%);
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

.awards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.award-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.award-card {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 32px 24px 24px;
  position: relative;
  overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease, border-color 0.4s ease;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 240px;
}

.award-glow {
  position: absolute;
  top: -30%;
  left: 50%;
  transform: translateX(-50%);
  width: 140px;
  height: 140px;
  background: var(--warm-amber);
  opacity: 0.04;
  border-radius: 50%;
  filter: blur(40px);
  transition: opacity 0.4s, width 0.4s, height 0.4s;
  pointer-events: none;
}

.award-card-link:hover .award-card {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 24px 64px rgba(120, 90, 60, 0.14);
  border-color: var(--warm-amber);
}

.award-card-link:hover .award-glow {
  opacity: 0.15;
  width: 180px;
  height: 180px;
}

.award-icon {
  margin-bottom: 4px;
}
.award-image {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  margin-bottom: 8px;
}

.award-level {
  font-size: 13px;
  font-weight: 700;
  color: var(--warm-amber);
}

.award-card h3 {
  font-family: var(--font-heading);
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.5;
}

.award-card p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0;
}

.award-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: var(--text-muted);
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--glass-border);
}

.award-accent-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--warm-amber);
  opacity: 0;
  transition: opacity 0.3s;
}

.award-card-link:hover .award-accent-line {
  opacity: 1;
}

@media (max-width: 900px) {
  .awards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .awards-grid {
    grid-template-columns: 1fr;
  }
}
</style>
