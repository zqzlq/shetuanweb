<template>
  <div class="page-view members-view">
    <div class="container">
      <div class="page-hero">
        <p class="eyebrow">{{ page.content.hero.eyebrow }}</p>
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
      </div>

      <div class="stats-bar reveal">
        <div v-for="s in page.content.stats" :key="s.label" class="stat-item">
          <strong><CountUp :target="s.value" /></strong>
          <span>{{ s.label }}</span>
        </div>
      </div>

      <div class="filter-bar reveal">
        <div class="filter-tabs">
          <button v-for="g in groups" :key="g" class="filter-tab" :class="{ active: activeGroup === g }" @click="activeGroup = g">{{ g }}</button>
        </div>
        <div class="search-box">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M11 11l3 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          <input v-model="searchQuery" type="text" placeholder="搜索成员..." class="search-input" />
        </div>
      </div>

      <div v-if="visible.length" class="members-grid">
        <PaperCard v-for="m in visible" :key="m.name" class="reveal member-card" glow="var(--warm-terracotta)">
          <div class="member-avatar" :style="m.avatar ? {} : { background: avatarColor(m.name) }">
            <img v-if="m.avatar" :src="m.avatar" :alt="m.name" />
            <span v-else>{{ m.name[0] }}</span>
          </div>
          <span class="tag tag-accent">{{ m.group }}</span>
          <h3>{{ m.name }}</h3>
          <p class="member-role">{{ m.role }}</p>
          <p class="member-desc">{{ m.description }}</p>
          <div class="member-skills">
            <span v-for="s in m.skills" :key="s" class="tag">{{ s }}</span>
          </div>
          <div v-if="memberSocialLinks(m).length" class="member-links">
            <a v-for="link in memberSocialLinks(m)" :key="link.platform + link.url" :href="link.url" target="_blank" rel="noopener" :title="link.platform" class="social-icon-link">
              <svg v-if="link.platform === 'github'" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
              <svg v-else-if="link.platform === 'bilibili'" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.995 1.524 2.249 1.56 3.76v7.36c-.036 1.51-.556 2.769-1.56 3.773s-2.262 1.524-3.773 1.56H5.333c-1.51-.036-2.769-.556-3.773-1.56S.036 18.858 0 17.347v-7.36c.036-1.511.556-2.765 1.56-3.76 1.004-.996 2.262-1.52 3.773-1.574h.774l-1.174-1.12a1.234 1.234 0 01-.373-.906c0-.356.124-.658.373-.907l.027-.027c.267-.249.573-.373.92-.373.347 0 .653.124.92.373L9.653 4.44c.071.071.134.142.187.213h4.267a.836.836 0 01.16-.213l2.853-2.747c.267-.249.573-.373.92-.373.347 0 .662.151.929.4.267.249.391.551.391.907 0 .355-.124.657-.373.906zM5.333 7.24c-.746.018-1.373.276-1.88.773-.506.498-.769 1.13-.786 1.894v7.52c.017.764.28 1.395.786 1.893.507.498 1.134.756 1.88.773h13.334c.746-.017 1.373-.275 1.88-.773.506-.498.769-1.129.786-1.893v-7.52c-.017-.765-.28-1.396-.786-1.894-.507-.497-1.134-.755-1.88-.773zM8 11.107c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c0-.373.129-.689.386-.947.258-.257.574-.386.947-.386zm8 0c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373z"/></svg>
              <svg v-else-if="link.platform === 'zhihu'" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M13.444 6.444h2.111v1.584h4.445v1.583h-1.583v7.023H8.555v-1.584H5.027v1.584H3.472v-1.584H2V6.444h3.5v.056h1.028v-.056h2.11v.028h1.056v-.028h3.75zm-5.916 7.023h.556V12.11h-.556zm1.583 0h.556V12.11h-.556zm1.583 0h.556V12.11h-.556zm4.22-5.439H6.528v4.461h8.386z"/></svg>
              <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 12h8M12 8l4 4-4 4"/></svg>
            </a>
          </div>
        </PaperCard>
      </div>

      <div v-else class="empty-state reveal">
        <p>没有找到匹配的成员</p>
      </div>

      <div v-if="hasMore" class="load-more-wrap reveal">
        <button class="btn btn-outline" @click="loadMore">
          加载更多
          <span class="load-count">({{ filtered.length - visible.length }} 位剩余)</span>
        </button>
      </div>

      <section class="cta-block reveal">
        <h2>{{ page.content.joinCta.title }}</h2>
        <p>{{ page.content.joinCta.description }}</p>
        <div class="cta-actions">
          <router-link :to="page.content.joinCta.primaryButton.link" class="btn btn-primary">{{ page.content.joinCta.primaryButton.text }}</router-link>
          <router-link :to="page.content.joinCta.secondaryButton.link" class="btn btn-outline">{{ page.content.joinCta.secondaryButton.text }}</router-link>
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
import CountUp from '@/components/effects/CountUp.vue'

const store = useSiteConfigStore()
const page = store.getPage('members')
const activeGroup = ref('全部')
const searchQuery = ref('')
const PAGE_SIZE = 6
const showCount = ref(PAGE_SIZE)
useScrollReveal()

const members = computed(() => page.content.members || [])

// 兼容旧 links 格式和新 socialLinks 格式
function memberSocialLinks(m) {
  if (m.socialLinks?.length) return m.socialLinks.filter(l => l.url)
  // 向后兼容旧的 links 格式
  const legacy = []
  if (m.links?.github) legacy.push({ platform: 'github', url: m.links.github })
  if (m.links?.portfolio) legacy.push({ platform: 'blog', url: m.links.portfolio })
  return legacy
}

const groups = computed(() => {
  const gs = [...new Set(members.value.map((m) => m.group))]
  return ['全部', ...gs]
})

const filtered = computed(() => {
  let list = members.value
  if (activeGroup.value !== '全部') {
    list = list.filter((m) => m.group === activeGroup.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase()
    list = list.filter((m) =>
      m.name.toLowerCase().includes(q) ||
      m.role.toLowerCase().includes(q) ||
      m.description.toLowerCase().includes(q) ||
      m.skills.some((s) => s.toLowerCase().includes(q))
    )
  }
  return list
})

const visible = computed(() => filtered.value.slice(0, showCount.value))
const hasMore = computed(() => filtered.value.length > showCount.value)

watch(activeGroup, () => { showCount.value = PAGE_SIZE })
watch(searchQuery, () => { showCount.value = PAGE_SIZE })

function loadMore() { showCount.value += PAGE_SIZE }

const colors = ['var(--warm-terracotta)', 'var(--warm-amber)', 'var(--warm-coral)', 'var(--warm-sage)', 'var(--warm-brown)']
function avatarColor(name) {
  let h = 0
  for (let i = 0; i < name.length; i++) h = name.charCodeAt(i) + ((h << 5) - h)
  return colors[Math.abs(h) % colors.length]
}
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
.page-subtitle { font-size: 16px; color: var(--text-secondary); max-width: 640px; margin: 0 auto; }

.stats-bar { display: flex; justify-content: center; gap: 48px; padding: 28px 0; margin-bottom: 40px; border-top: 1px solid var(--glass-border); border-bottom: 1px solid var(--glass-border); background: #fff; border-radius: var(--radius-lg); }
.stat-item { text-align: center; }
.stat-item strong { display: block; font-family: var(--font-heading); font-size: 28px; font-weight: 700; background: var(--grad-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.stat-item span { font-size: 13px; color: var(--text-muted); }

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

.search-box { position: relative; flex-shrink: 0; }
.search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); pointer-events: none; }
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
.search-input:focus { border-color: var(--warm-terracotta); box-shadow: 0 0 0 3px rgba(192, 96, 64, 0.1); width: 240px; }
.search-input::placeholder { color: var(--text-muted); }

/* 成员网格 */
.members-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-bottom: 32px; }
.member-card { text-align: center; }
.member-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin: 0 auto 12px;
  overflow: hidden;
}
.member-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.member-card h3 { font-family: var(--font-heading); font-size: 18px; margin: 8px 0 4px; }
.member-role { font-size: 13px; color: var(--warm-terracotta); margin: 0 0 8px; font-weight: 500; }
.member-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin: 0 0 12px; }
.member-skills { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; }
.member-links { display: flex; gap: 10px; justify-content: center; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--glass-border); }
.social-icon-link { color: var(--text-muted); transition: color 0.2s, transform 0.2s; display: flex; }
.social-icon-link:hover { color: var(--warm-terracotta); transform: translateY(-2px); }

.empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); font-size: 15px; margin-bottom: 32px; }

.load-more-wrap { text-align: center; margin-bottom: 40px; }
.load-count { font-size: 12px; color: var(--text-muted); font-weight: 400; }

.cta-block { text-align: center; padding: 56px 32px; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-xl); box-shadow: var(--shadow-lg); position: relative; overflow: hidden; }
.cta-block::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.cta-block h2 { font-size: 1.5rem; margin-bottom: 12px; position: relative; }
.cta-block p { color: var(--text-secondary); margin-bottom: 24px; position: relative; }
.cta-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; position: relative; }

@media (max-width: 640px) {
  .filter-bar { flex-direction: column; align-items: stretch; }
  .search-input { width: 100%; }
  .search-input:focus { width: 100%; }
  .stats-bar { gap: 24px; }
}
</style>
