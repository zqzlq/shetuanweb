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
          <button v-for="c in page.content.categories" :key="c" class="filter-tab" :class="{ active: activeCat === c }" @click="activeCat = c">{{ c }}</button>
        </div>
        <div class="search-box">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M11 11l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          <input v-model="searchQuery" type="text" placeholder="搜索文章..." class="search-input" />
        </div>
      </div>

      <div v-if="visible.length" class="posts-grid">
        <PaperCard v-for="post in visible" :key="post.title" class="reveal post-card" glow="var(--warm-amber)">
          <span class="tag tag-accent">{{ post.category }}</span>
          <h3>{{ post.title }}</h3>
          <p>{{ post.excerpt }}</p>
          <div class="post-meta">
            <span>{{ post.date }}</span>
            <span>{{ post.readTime }}</span>
          </div>
        </PaperCard>
      </div>

      <div v-else class="empty-state reveal">
        <p>没有找到匹配的文章</p>
      </div>

      <div v-if="hasMore" class="load-more-wrap reveal">
        <button class="btn btn-outline" @click="loadMore">
          加载更多
          <span class="load-count">({{ filtered.length - visible.length }} 篇剩余)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import PaperCard from '@/components/ui/PaperCard.vue'

const store = useSiteConfigStore()
const page = store.getPage('blog')
const activeCat = ref('全部')
const searchQuery = ref('')
const PAGE_SIZE = 6
const showCount = ref(PAGE_SIZE)
useScrollReveal()

const filtered = computed(() => {
  let list = page.content.posts
  if (activeCat.value !== '全部') {
    list = list.filter((p) => p.category === activeCat.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    list = list.filter((p) =>
      p.title.toLowerCase().includes(q) ||
      p.excerpt.toLowerCase().includes(q)
    )
  }
  return list
})

const visible = computed(() => filtered.value.slice(0, showCount.value))
const hasMore = computed(() => filtered.value.length > showCount.value)

watch(activeCat, () => { showCount.value = PAGE_SIZE })
watch(searchQuery, () => { showCount.value = PAGE_SIZE })

function loadMore() { showCount.value += PAGE_SIZE }
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero { text-align: center; margin-bottom: 40px; padding: 48px 32px; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.page-hero::after { content: ''; position: absolute; inset: 0; background-image: radial-gradient(circle at 15% 85%, rgba(192, 96, 64, 0.04) 0%, transparent 40%), radial-gradient(circle at 85% 15%, rgba(212, 146, 10, 0.04) 0%, transparent 40%); pointer-events: none; }
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); }

.filter-bar { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }
.filter-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-tab { padding: 8px 18px; border: 1px solid var(--glass-border); border-radius: 999px; background: transparent; font-size: 13px; color: var(--text-secondary); cursor: pointer; transition: all 0.2s; }
.filter-tab:hover { border-color: var(--glass-border-hover); color: var(--text-primary); background: var(--surface); }
.filter-tab.active { background: var(--grad-primary); color: white; border-color: transparent; }

.search-box { position: relative; flex-shrink: 0; }
.search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); pointer-events: none; }
.search-input { padding: 9px 16px 9px 38px; border: 1px solid var(--glass-border); border-radius: 999px; font-size: 13px; background: #fff; color: var(--text-primary); width: 200px; transition: all 0.2s; outline: none; }
.search-input:focus { border-color: var(--warm-terracotta); box-shadow: 0 0 0 3px rgba(192, 96, 64, 0.1); width: 240px; }
.search-input::placeholder { color: var(--text-muted); }

.posts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-bottom: 32px; }
.post-card h3 { font-family: var(--font-heading); font-size: 17px; margin: 10px 0 8px; }
.post-card p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin: 0 0 12px; }
.post-meta { display: flex; gap: 16px; font-size: 12px; color: var(--text-muted); }

.empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); font-size: 15px; margin-bottom: 32px; }
.load-more-wrap { text-align: center; }
.load-count { font-size: 12px; color: var(--text-muted); font-weight: 400; }

@media (max-width: 640px) { .filter-bar { flex-direction: column; align-items: stretch; } .search-input { width: 100%; } .search-input:focus { width: 100%; } }
</style>
