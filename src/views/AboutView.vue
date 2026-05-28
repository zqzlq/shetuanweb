<template>
  <div class="page-view about-view">
    <div class="container">
      <div class="page-hero">
        <p class="eyebrow">{{ page.content.hero.eyebrow }}</p>
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
        <div class="badges">
          <span v-for="b in page.content.hero.badges" :key="b.text" class="badge">{{ b.text }}</span>
        </div>
      </div>

      <section class="reveal section-block">
        <div class="section-heading">
          <h2>{{ page.content.values.title }}</h2>
          <p>{{ page.content.values.subtitle }}</p>
        </div>
        <div class="cards-grid cols-3">
          <PaperCard v-for="v in page.content.values.items" :key="v.title" class="reveal" glow="var(--warm-terracotta)">
            <h3>{{ v.title }}</h3>
            <p>{{ v.description }}</p>
          </PaperCard>
        </div>
      </section>

      <section class="reveal section-block">
        <div class="section-heading">
          <h2>{{ page.content.groups.title }}</h2>
          <p>{{ page.content.groups.subtitle }}</p>
        </div>
        <div class="cards-grid cols-2">
          <PaperCard v-for="g in page.content.groups.items" :key="g.name" class="reveal" glow="var(--warm-amber)">
            <span class="tag tag-accent">{{ g.tag }}</span>
            <h3>{{ g.name }}</h3>
            <p>{{ g.description }}</p>
          </PaperCard>
        </div>
      </section>

      <section class="reveal section-block">
        <div class="section-heading">
          <p class="eyebrow">{{ page.content.timeline.eyebrow }}</p>
          <h2>{{ page.content.timeline.title }}</h2>
        </div>
        <div class="timeline">
          <div v-for="t in page.content.timeline.items" :key="t.year" class="timeline-item reveal">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-year">{{ t.year }}</span>
              <h3>{{ t.title }}</h3>
              <p>{{ t.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="cta-block reveal">
        <h2>{{ page.content.cta.title }}</h2>
        <p>{{ page.content.cta.description }}</p>
        <div class="cta-actions">
          <router-link :to="page.content.cta.primaryButton.link" class="btn btn-primary">{{ page.content.cta.primaryButton.text }}</router-link>
          <router-link :to="page.content.cta.secondaryButton.link" class="btn btn-outline">{{ page.content.cta.secondaryButton.text }}</router-link>
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
const page = store.getPage('about')
useScrollReveal()
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero {
  text-align: center;
  margin-bottom: 64px;
  padding: 48px 32px;
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}
.page-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--grad-primary);
}
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); max-width: 560px; margin: 0 auto 20px; }

.badges { display: flex; gap: 12px; justify-content: center; }
.badge { padding: 6px 14px; background: rgba(255, 255, 255, 0.7); border: 1px solid var(--glass-border); border-radius: 999px; font-size: 13px; color: var(--text-secondary); }

.section-block { margin-bottom: 64px; }
.cards-grid { display: grid; gap: 20px; }
.cols-3 { grid-template-columns: repeat(3, 1fr); }
.cols-2 { grid-template-columns: repeat(2, 1fr); }
.cards-grid h3 { font-family: var(--font-heading); font-size: 17px; margin: 12px 0 8px; }
.cards-grid p { font-size: 14px; line-height: 1.7; color: var(--text-secondary); margin: 0; }

.timeline { position: relative; padding-left: 32px; }
.timeline::before { content: ''; position: absolute; top: 0; bottom: 0; left: 7px; width: 2px; background: var(--glass-border); }
.timeline-item { position: relative; padding-bottom: 32px; }
.timeline-dot { position: absolute; left: -32px; top: 4px; width: 16px; height: 16px; background: var(--bg); border: 3px solid var(--warm-terracotta); border-radius: 50%; }
.timeline-year { font-family: var(--font-heading); font-size: 14px; font-weight: 600; color: var(--warm-terracotta); }
.timeline-content h3 { font-family: var(--font-heading); font-size: 17px; margin: 4px 0 6px; }
.timeline-content p { font-size: 14px; color: var(--text-secondary); margin: 0; line-height: 1.7; }

.cta-block {
  text-align: center;
  padding: 56px 32px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}
.cta-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--grad-primary);
}
.cta-block h2 { font-size: 1.5rem; margin-bottom: 12px; position: relative; }
.cta-block p { color: var(--text-secondary); margin-bottom: 24px; position: relative; }
.cta-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; position: relative; }

@media (max-width: 768px) { .cols-3, .cols-2 { grid-template-columns: 1fr; } }
</style>
