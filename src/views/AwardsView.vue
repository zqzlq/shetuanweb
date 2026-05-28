<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <h1>比赛奖项</h1>
        <p class="page-subtitle">社团成员在各类比赛中获得的荣誉与成果。</p>
      </div>

      <div class="filter-bar reveal">
        <div class="filter-tabs">
          <button v-for="c in categories" :key="c" class="filter-tab" :class="{ active: activeCat === c }" @click="activeCat = c">{{ c }}</button>
        </div>
      </div>

      <div v-for="group in grouped" :key="group.year" class="year-group reveal">
        <div class="year-header">
          <span class="year-label">{{ group.year }}</span>
          <span class="year-count">{{ group.items.length }} 项</span>
          <div class="year-line"></div>
        </div>
        <div class="awards-grid">
          <router-link v-for="a in group.items" :key="a.slug" :to="`/awards/${a.slug}`" class="award-card-link">
            <PaperCard class="award-card" glow="var(--warm-amber)">
              <img v-if="a.image" :src="a.image" :alt="a.title" class="award-image" />
              <div class="award-badge" aria-hidden="true">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2l2.5 5.5L18 8.2l-4 3.8 1 5.5L10 14.8l-5 2.7 1-5.5-4-3.8 5.5-.7L10 2z" fill="var(--warm-amber)"/></svg>
              </div>
              <div class="award-meta">
                <span class="tag tag-accent">{{ a.category }}</span>
                <span class="award-level">{{ a.level }}</span>
              </div>
              <h3>{{ a.title }}</h3>
              <p>{{ a.shortDesc || a.description }}</p>
              <span class="award-link-hint">查看详情 &rarr;</span>
            </PaperCard>
          </router-link>
        </div>
      </div>

      <div v-if="!grouped.length" class="empty-state reveal">
        <p>该分类暂无奖项记录</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import PaperCard from '@/components/ui/PaperCard.vue'

const store = useSiteConfigStore()
const page = store.getPage('projects')
const activeCat = ref('全部')
useScrollReveal()

const awards = computed(() => page?.content?.awards?.items || [])

const categories = computed(() => {
  const cats = [...new Set(awards.value.map((a) => a.category))]
  return ['全部', ...cats]
})

const filtered = computed(() => {
  if (activeCat.value === '全部') return awards.value
  return awards.value.filter((a) => a.category === activeCat.value)
})

const grouped = computed(() => {
  const map = new Map()
  for (const a of filtered.value) {
    const year = a.date?.slice(0, 4) || '其他'
    if (!map.has(year)) map.set(year, [])
    map.get(year).push(a)
  }
  return Array.from(map.entries())
    .sort(([a], [b]) => b.localeCompare(a))
    .map(([year, items]) => ({ year, items }))
})
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero {
  text-align: center;
  margin-bottom: 40px;
  padding: 48px 32px;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}

.page-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 15% 85%, rgba(192, 96, 64, 0.04) 0%, transparent 40%),
    radial-gradient(circle at 85% 15%, rgba(212, 146, 10, 0.04) 0%, transparent 40%);
  pointer-events: none;
}
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); }

.filter-bar {
  margin-bottom: 40px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

.filter-tab {
  padding: 8px 18px;
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  background: transparent;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab:hover { border-color: var(--glass-border-hover); color: var(--text-primary); background: var(--surface); }
.filter-tab.active { background: var(--grad-primary); color: white; border-color: transparent; }

/* 年份分组 */
.year-group {
  margin-bottom: 48px;
}

.year-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.year-label {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  flex-shrink: 0;
}

.year-count {
  font-size: 13px;
  color: var(--text-muted);
  flex-shrink: 0;
}

.year-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--glass-border), transparent);
}

.awards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.award-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.award-badge { margin-bottom: 8px; }
.award-image { width: 100%; height: 120px; object-fit: cover; border-radius: var(--radius-sm); margin-bottom: 8px; }

.award-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.award-level {
  font-size: 12px;
  font-weight: 600;
  color: var(--warm-amber);
}

.award-card h3 { font-family: var(--font-heading); font-size: 16px; margin-bottom: 8px; }
.award-card p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin: 0 0 12px; }

.award-link-hint {
  font-size: 12px;
  font-weight: 600;
  color: var(--warm-terracotta);
  opacity: 0;
  transition: opacity 0.2s;
}

.award-card-link:hover .award-link-hint { opacity: 1; }

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
  font-size: 15px;
}

@media (max-width: 768px) {
  .page-hero { padding: 32px 20px; }
  .year-label { font-size: 22px; }
  .awards-grid { grid-template-columns: 1fr; }
}

@media (max-width: 480px) {
  .page-hero { padding: 24px 16px; }
  .page-hero h1 { font-size: 1.5rem; }
}
</style>
