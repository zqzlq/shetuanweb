<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <p class="eyebrow">{{ page.content.hero.eyebrow }}</p>
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
      </div>

      <div class="groups-grid">
        <PaperCard v-for="g in page.content.groups" :key="g.name" class="reveal" glow="var(--warm-coral)">
          <span class="tag tag-accent">{{ g.tag }}</span>
          <h3>{{ g.name }}</h3>
          <p>{{ g.description }}</p>
          <ul class="req-list"><li v-for="r in g.requirements" :key="r">{{ r }}</li></ul>
        </PaperCard>
      </div>

      <section class="process-section reveal">
        <h2 class="section-title">{{ page.content.sectionTitles.process }}</h2>
        <div class="process-steps">
          <div v-for="(s, i) in page.content.process" :key="s.step" class="process-step">
            <span class="process-num">{{ i + 1 }}</span>
            <strong>{{ s.step }}</strong>
            <p>{{ s.description }}</p>
          </div>
        </div>
      </section>

      <section class="cta-block reveal">
        <h2>{{ page.content.cta.title }}</h2>
        <router-link :to="page.content.cta.buttonLink" class="btn btn-primary">{{ page.content.cta.buttonText }}</router-link>
      </section>
    </div>
  </div>
</template>

<script setup>
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import PaperCard from '@/components/ui/PaperCard.vue'
const store = useSiteConfigStore()
const page = store.getPage('recruitment')
useScrollReveal()
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero { text-align: center; margin-bottom: 48px; padding: 48px 32px; background: rgba(255, 255, 255, 0.6); border: 1px solid var(--glass-border); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); max-width: 560px; margin: 0 auto; }
.groups-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 64px; }
.groups-grid h3 { font-family: var(--font-heading); font-size: 18px; margin: 10px 0 8px; }
.groups-grid p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin: 0 0 12px; }
.req-list { padding-left: 18px; margin: 0; }
.req-list li { font-size: 13px; color: var(--text-secondary); line-height: 1.8; }

.process-section { margin-bottom: 64px; }
.section-title { font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 28px; text-align: center; }
.process-steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.process-step { text-align: center; }
.process-num { display: inline-flex; width: 32px; height: 32px; align-items: center; justify-content: center; background: var(--grad-primary); color: white; border-radius: 50%; font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin-bottom: 12px; }
.process-step strong { display: block; font-size: 15px; margin-bottom: 6px; }
.process-step p { font-size: 13px; color: var(--text-secondary); margin: 0; }

.cta-block { text-align: center; padding: 56px 32px; background: rgba(255, 255, 255, 0.85); border: 1px solid var(--glass-border); border-radius: var(--radius-xl); box-shadow: var(--shadow-lg); position: relative; overflow: hidden; }
.cta-block::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.cta-block h2 { font-size: 1.5rem; margin-bottom: 20px; position: relative; }

@media (max-width: 768px) { .groups-grid { grid-template-columns: 1fr; } .process-steps { grid-template-columns: repeat(2, 1fr); } }
</style>
