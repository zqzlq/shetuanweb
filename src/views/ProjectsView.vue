<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <p class="eyebrow">{{ page.content.hero.eyebrow }}</p>
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
      </div>

      <div class="filter-bar reveal">
        <div class="filter-tabs">
          <button v-for="f in filterOptions" :key="f" class="filter-tab" :class="{ active: activeFilter === f }" @click="activeFilter = f">{{ f }}</button>
        </div>
        <div class="search-box">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M11 11l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          <input v-model="searchQuery" type="text" placeholder="搜索作品..." class="search-input" />
        </div>
      </div>

      <div v-if="visible.length" class="projects-grid">
        <router-link v-for="p in visible" :key="p.slug" :to="p.link || `/project/${p.slug}`" class="reveal project-card-link">
          <div class="project-card" :class="{ featured: p.featured }">
            <div class="card-cover" :class="p.coverImage ? '' : 'cover-' + p.coverClass">
              <img v-if="p.coverImage" :src="p.coverImage" :alt="p.name" class="cover-img" />
              <span class="card-status" :class="p.status">{{ p.status === 'active' ? '进行中' : '开发中' }}</span>
            </div>
            <div class="card-body">
              <span class="tag tag-accent">{{ p.category }}</span>
              <h3>{{ p.name }}</h3>
              <p>{{ p.description }}</p>
              <div class="card-tags"><span v-for="t in p.techStack" :key="t" class="tag">{{ t }}</span></div>
            </div>
          </div>
        </router-link>
      </div>

      <div v-else class="empty-state reveal">
        <p>没有找到匹配的作品</p>
      </div>

      <div v-if="hasMore" class="load-more-wrap reveal">
        <button class="btn btn-outline" @click="loadMore">
          加载更多
          <span class="load-count">({{ filtered.length - visible.length }} 项剩余)</span>
        </button>
      </div>

      <section class="awards-section reveal">
        <div class="section-heading">
          <h2>{{ page.content.awards.title }}</h2>
          <p>{{ page.content.awards.description }}</p>
        </div>
        <div v-for="group in awardGroups" :key="group.year" class="award-year-group">
          <div class="year-header">
            <span class="year-label">{{ group.year }}</span>
            <div class="year-line"></div>
          </div>
          <div class="awards-grid">
            <router-link v-for="a in group.items" :key="a.slug" :to="`/awards/${a.slug}`" class="award-card-link">
              <PaperCard class="award-card" glow="var(--warm-amber)">
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
        <router-link to="/projects/awards" class="view-all-link">查看全部奖项 &rarr;</router-link>
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
import { ref, computed, watch } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import PaperCard from '@/components/ui/PaperCard.vue'

const store = useSiteConfigStore()
const page = store.getPage('projects')
const activeFilter = ref('全部')
const searchQuery = ref('')
const PAGE_SIZE = 6
const showCount = ref(PAGE_SIZE)

useScrollReveal()

// 从首页配置的分类标签动态生成过滤选项
const filterOptions = computed(() => {
  const cats = store.config?.products?.categories || []
  return ['全部', '精选', ...cats.filter(c => c && c !== '精选总览')]
})

const filtered = computed(() => {
  let list = page.content.projects || []
  if (activeFilter.value === '精选') {
    list = list.filter((p) => p.featured)
  } else if (activeFilter.value !== '全部') {
    list = list.filter((p) => p.category === activeFilter.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    list = list.filter((p) =>
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.techStack.some((t) => t.toLowerCase().includes(q))
    )
  }
  return list
})

const visible = computed(() => filtered.value.slice(0, showCount.value))
const hasMore = computed(() => filtered.value.length > showCount.value)

const awards = computed(() => page.content.awards.items || [])
const awardGroups = computed(() => {
  const map = new Map()
  for (const a of awards.value) {
    const year = a.date?.slice(0, 4) || '其他'
    if (!map.has(year)) map.set(year, [])
    map.get(year).push(a)
  }
  return Array.from(map.entries())
    .sort(([a], [b]) => b.localeCompare(a))
    .map(([year, items]) => ({ year, items }))
})

watch(activeFilter, () => { showCount.value = PAGE_SIZE })
watch(searchQuery, () => { showCount.value = PAGE_SIZE })

function loadMore() { showCount.value += PAGE_SIZE }
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
.page-subtitle { font-size: 16px; color: var(--text-secondary); max-width: 560px; margin: 0 auto; }

/* 筛选栏 */
.filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-tab { padding: 8px 18px; border: 1px solid var(--glass-border); border-radius: 999px; background: transparent; font-size: 13px; font-weight: 500; color: var(--text-secondary); cursor: pointer; transition: all 0.2s; }
.filter-tab:hover { border-color: var(--glass-border-hover); color: var(--text-primary); background: var(--surface); }
.filter-tab.active { background: var(--grad-primary); color: white; border-color: transparent; }

.search-box {
  position: relative;
  flex-shrink: 0;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  padding: 9px 16px 9px 38px;
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  font-size: 13px;
  background: #fff;
  color: var(--text-primary);
  width: 200px;
  transition: all 0.2s;
  outline: none;
}

.search-input:focus {
  border-color: var(--warm-terracotta);
  box-shadow: 0 0 0 3px rgba(192, 96, 64, 0.1);
  width: 240px;
}

.search-input::placeholder {
  color: var(--text-muted);
}

/* 作品网格 */
.projects-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; margin-bottom: 32px; }
.project-card-link { text-decoration: none; color: inherit; }
.project-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); overflow: hidden; transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease, border-color 0.4s ease; position: relative; }
.project-card::before { content: ''; position: absolute; top: -40%; left: 50%; transform: translateX(-50%); width: 160px; height: 160px; background: var(--warm-coral); opacity: 0; border-radius: 50%; filter: blur(50px); transition: opacity 0.4s, width 0.4s, height 0.4s; pointer-events: none; z-index: 0; }
.project-card:hover { transform: translateY(-12px) scale(1.03); box-shadow: 0 24px 64px rgba(120, 90, 60, 0.14); border-color: var(--warm-coral); }
.project-card:hover::before { opacity: 0.12; width: 200px; height: 200px; }
.card-cover { height: 140px; position: relative; display: flex; align-items: flex-end; padding: 12px; overflow: hidden; }
.cover-img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.cover-aurora { background: linear-gradient(135deg, #c06040, #d4920a); }
.cover-meteor { background: linear-gradient(135deg, #d4920a, #c07080); }
.cover-nebula { background: linear-gradient(135deg, #c06040, #7a9a6a); }
.cover-cosmos { background: linear-gradient(135deg, #7a9a6a, #8b7355); }
.cover-pulse { background: linear-gradient(135deg, #c07080, #e07050); }
.cover-horizon { background: linear-gradient(135deg, #8b7355, #c06040); }
.card-status { font-size: 11px; padding: 3px 8px; border-radius: 999px; color: white; }
.card-status.active { background: rgba(0, 160, 80, 0.75); }
.card-status.wip { background: rgba(180, 130, 0, 0.75); }
.card-body { padding: 20px; }
.card-body h3 { font-family: var(--font-heading); font-size: 17px; margin: 8px 0; }
.card-body p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin: 0 0 12px; }
.card-tags { display: flex; flex-wrap: wrap; gap: 6px; }

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-muted);
  font-size: 15px;
  margin-bottom: 32px;
}

.load-more-wrap { text-align: center; margin-bottom: 40px; }
.load-count { font-size: 12px; color: var(--text-muted); font-weight: 400; }

/* 奖项区域 */
.awards-section { margin-bottom: 64px; }

.award-year-group { margin-bottom: 32px; }

.year-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.year-label {
  font-family: var(--font-heading);
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  flex-shrink: 0;
}

.year-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--glass-border), transparent);
}

.awards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-bottom: 16px; }

.award-card-link { text-decoration: none; color: inherit; display: block; }

.award-badge { margin-bottom: 8px; }
.award-meta { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.award-level { font-size: 12px; font-weight: 600; color: var(--warm-amber); }
.award-card h3 { font-family: var(--font-heading); font-size: 16px; margin-bottom: 8px; }
.award-card p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin: 0 0 12px; }
.award-link-hint { font-size: 12px; font-weight: 600; color: var(--warm-terracotta); opacity: 0; transition: opacity 0.2s; }
.award-card-link:hover .award-link-hint { opacity: 1; }

.view-all-link {
  display: inline-block;
  margin-top: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--warm-terracotta);
  transition: opacity 0.2s;
}

.view-all-link:hover { opacity: 0.7; }

/* CTA */
.cta-block { text-align: center; padding: 56px 32px; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-xl); box-shadow: var(--shadow-lg); position: relative; overflow: hidden; }
.cta-block::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.cta-block h2 { font-size: 1.5rem; margin-bottom: 12px; position: relative; }
.cta-block p { color: var(--text-secondary); margin-bottom: 24px; position: relative; }
.cta-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; position: relative; }

@media (max-width: 640px) {
  .filter-bar { flex-direction: column; align-items: stretch; }
  .search-input { width: 100%; }
  .search-input:focus { width: 100%; }
}
</style>
