<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <span class="version-badge">{{ page.content.hero.version }}</span>
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
        <div class="hero-metrics">
          <div v-for="m in page.content.hero.metrics" :key="m.label" class="metric">
            <strong>{{ m.value }}</strong>
            <span>{{ m.label }}</span>
          </div>
        </div>
      </div>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sectionTitles.features }}</h2>
        <div class="features-grid">
          <PaperCard v-for="f in page.content.features" :key="f.title" class="reveal" glow="var(--warm-coral)">
            <h3>{{ f.title }}</h3>
            <p>{{ f.description }}</p>
            <div v-if="f.tags" class="card-tags"><span v-for="t in f.tags" :key="t" class="tag">{{ t }}</span></div>
          </PaperCard>
        </div>
      </section>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sectionTitles.highlights }}</h2>
        <ul class="highlights-list">
          <li v-for="h in page.content.highlights" :key="h">{{ h }}</li>
        </ul>
      </section>

      <section class="cta-block reveal">
        <h2>{{ page.content.cta.title }}</h2>
        <a :href="page.content.cta.link" target="_blank" class="btn btn-primary">{{ page.content.cta.buttonText }}</a>
      </section>
    </div>
  </div>
</template>

<script setup>
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import PaperCard from '@/components/ui/PaperCard.vue'
const store = useSiteConfigStore()
const page = store.getPage('yuji')
useScrollReveal()
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero { text-align: center; margin-bottom: 48px; padding: 48px 32px; background: rgba(255, 255, 255, 0.6); border: 1px solid var(--glass-border); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); margin-bottom: 24px; }
.version-badge { display: inline-block; padding: 4px 12px; background: var(--surface); border: 1px solid var(--glass-border); border-radius: 999px; font-family: var(--font-heading); font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }

.hero-metrics { display: flex; gap: 40px; justify-content: center; }
.metric { text-align: center; }
.metric strong { display: block; font-family: var(--font-heading); font-size: 28px; font-weight: 700; background: var(--grad-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.metric span { font-size: 13px; color: var(--text-muted); }

.section-title { font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 24px; text-align: center; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 48px; }
.features-grid h3 { font-family: var(--font-heading); font-size: 16px; margin: 0 0 8px; }
.features-grid p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin: 0 0 10px; }
.card-tags { display: flex; gap: 6px; flex-wrap: wrap; }

.highlights-list { list-style: none; padding: 0; max-width: 480px; margin: 0 auto 48px; }
.highlights-list li { padding: 12px 0; border-bottom: 1px solid var(--glass-border); font-size: 15px; color: var(--text-primary); position: relative; padding-left: 20px; }
.highlights-list li::before { content: ''; position: absolute; left: 0; top: 50%; width: 6px; height: 6px; background: var(--warm-terracotta); border-radius: 50%; transform: translateY(-50%); }

.cta-block { text-align: center; padding: 56px 32px; background: rgba(255, 255, 255, 0.85); border: 1px solid var(--glass-border); border-radius: var(--radius-xl); box-shadow: var(--shadow-lg); position: relative; overflow: hidden; }
.cta-block::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.cta-block h2 { font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 20px; position: relative; }

@media (max-width: 768px) { .features-grid { grid-template-columns: 1fr; } }
</style>
