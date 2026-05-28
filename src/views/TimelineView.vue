<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <p class="eyebrow">{{ page.content.hero.eyebrow }}</p>
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
      </div>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sections.upcomingTitle }}</h2>
        <div class="upcoming-grid">
          <PaperCard v-for="e in page.content.upcoming" :key="e.title" class="reveal" glow="var(--warm-terracotta)">
            <span class="tag tag-accent">{{ e.type }}</span>
            <h3>{{ e.title }}</h3>
            <p>{{ e.description }}</p>
            <span class="event-date">{{ e.date }}</span>
          </PaperCard>
        </div>
      </section>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sections.milestonesTitle }}</h2>
        <div class="timeline">
          <div v-for="m in page.content.milestones" :key="m.year" class="timeline-item reveal">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-year">{{ m.year }}</span>
              <h3>{{ m.title }}</h3>
              <p>{{ m.description }}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import PaperCard from '@/components/ui/PaperCard.vue'
const store = useSiteConfigStore()
const page = store.getPage('timeline')
useScrollReveal()
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero { text-align: center; margin-bottom: 48px; padding: 48px 32px; background: rgba(255, 255, 255, 0.6); border: 1px solid var(--glass-border); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); }
.section-title { font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 24px; text-align: center; }

.upcoming-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 64px; }
.upcoming-grid h3 { font-family: var(--font-heading); font-size: 16px; margin: 10px 0 6px; }
.upcoming-grid p { font-size: 13px; color: var(--text-secondary); margin: 0 0 8px; line-height: 1.7; }
.event-date { font-size: 12px; color: var(--text-muted); }

.timeline { position: relative; padding-left: 32px; }
.timeline::before { content: ''; position: absolute; top: 0; bottom: 0; left: 7px; width: 2px; background: var(--glass-border); }
.timeline-item { position: relative; padding-bottom: 32px; }
.timeline-dot { position: absolute; left: -32px; top: 4px; width: 16px; height: 16px; background: var(--bg); border: 3px solid var(--warm-terracotta); border-radius: 50%; }
.timeline-year { font-family: var(--font-heading); font-size: 14px; font-weight: 600; color: var(--warm-terracotta); }
.timeline-content h3 { font-family: var(--font-heading); font-size: 17px; margin: 4px 0 6px; }
.timeline-content p { font-size: 14px; color: var(--text-secondary); margin: 0; line-height: 1.7; }

@media (max-width: 768px) { .upcoming-grid { grid-template-columns: 1fr; } }
</style>
