<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <p class="eyebrow">{{ page.content.hero.eyebrow }}</p>
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
      </div>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sections.stepsTitle }}</h2>
        <div class="steps-grid">
          <PaperCard v-for="(s, i) in page.content.steps" :key="s.title" class="reveal" glow="var(--warm-terracotta)">
            <span class="step-num">{{ i + 1 }}</span>
            <h3>{{ s.title }}</h3>
            <p>{{ s.description }}</p>
          </PaperCard>
        </div>
      </section>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sections.resourcesTitle }}</h2>
        <div class="resources-grid">
          <PaperCard v-for="r in page.content.resources" :key="r.title" class="reveal" glow="var(--warm-sage)">
            <h3>{{ r.title }}</h3>
            <p>{{ r.description }}</p>
          </PaperCard>
        </div>
      </section>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sections.mentorsTitle }}</h2>
        <div class="mentors-grid">
          <PaperCard v-for="m in page.content.mentors" :key="m.name" class="reveal mentor-card" glow="var(--warm-amber)">
            <div class="mentor-avatar">{{ m.name[0] }}</div>
            <h3>{{ m.name }}</h3>
            <p class="mentor-role">{{ m.role }}</p>
            <p>{{ m.description }}</p>
          </PaperCard>
        </div>
      </section>

      <section class="faq-section reveal">
        <h2 class="section-title">{{ page.content.sections.faqTitle }}</h2>
        <div v-for="f in page.content.faq" :key="f.question" class="faq-item">
          <button class="faq-q" @click="f.open = !f.open"><span>{{ f.question }}</span><span>{{ f.open ? '−' : '+' }}</span></button>
          <div v-if="f.open" class="faq-a">{{ f.answer }}</div>
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
const page = store.getPage('onboarding')
useScrollReveal()
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero { text-align: center; margin-bottom: 48px; padding: 48px 32px; background: rgba(255, 255, 255, 0.6); border: 1px solid var(--glass-border); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); }
.section-title { font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 24px; text-align: center; }

.steps-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 48px; }
.step-num { display: inline-flex; width: 32px; height: 32px; align-items: center; justify-content: center; background: var(--grad-primary); color: white; border-radius: 50%; font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin-bottom: 12px; }
.steps-grid h3 { font-family: var(--font-heading); font-size: 16px; margin: 0 0 6px; }
.steps-grid p { font-size: 13px; color: var(--text-secondary); margin: 0; }

.resources-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 48px; }
.resources-grid h3 { font-family: var(--font-heading); font-size: 16px; margin: 0 0 6px; }
.resources-grid p { font-size: 13px; color: var(--text-secondary); margin: 0; }

.mentors-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 48px; }
.mentor-card { text-align: center; }
.mentor-avatar { width: 56px; height: 56px; border-radius: 50%; background: var(--surface); border: 1px solid var(--glass-border); display: flex; align-items: center; justify-content: center; font-family: var(--font-heading); font-size: 22px; font-weight: 700; margin: 0 auto 12px; }
.mentor-card h3 { font-family: var(--font-heading); font-size: 16px; margin: 0 0 4px; }
.mentor-role { font-size: 13px; color: var(--warm-terracotta); margin: 0 0 8px; font-weight: 500; }
.mentor-card p:last-child { font-size: 13px; color: var(--text-secondary); margin: 0; }

.faq-item { border-bottom: 1px solid var(--glass-border); }
.faq-q { width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 16px 0; background: none; border: none; font-size: 15px; font-weight: 500; color: var(--text-primary); cursor: pointer; }
.faq-a { padding: 0 0 16px; font-size: 14px; color: var(--text-secondary); line-height: 1.7; }

@media (max-width: 768px) { .steps-grid, .resources-grid { grid-template-columns: repeat(2, 1fr); } .mentors-grid { grid-template-columns: 1fr; } }
</style>
