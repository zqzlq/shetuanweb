<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <p class="eyebrow">{{ page.content.hero.eyebrow }}</p>
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
      </div>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sections.reposTitle }}</h2>
        <div class="repos-grid">
          <a v-for="r in visibleRepos" :key="r.name" :href="r.link" target="_blank" class="repo-card-link">
            <PaperCard class="repo-card" glow="var(--warm-sage)">
              <div class="repo-header">
                <h3>{{ r.name }}</h3>
                <span class="repo-stars">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1l1.8 3.9L13 5.6l-3 2.8.7 4.1L7 10.4l-3.7 2.1.7-4.1-3-2.8 4.2-.7L7 1z" fill="var(--warm-amber)"/></svg>
                  {{ r.stars }}
                </span>
              </div>
              <p>{{ r.description }}</p>
              <span class="tag">{{ r.language }}</span>
            </PaperCard>
          </a>
        </div>
        <div v-if="hasMoreRepos" class="load-more-wrap reveal">
          <button class="btn btn-outline" @click="loadMoreRepos">
            加载更多仓库
            <span class="load-count">({{ repos.length - visibleRepos.length }} 个剩余)</span>
          </button>
        </div>
      </section>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sections.techStackTitle }}</h2>
        <div class="tech-tags"><span v-for="t in page.content.techStack" :key="t" class="tag">{{ t }}</span></div>
      </section>

      <section class="reveal">
        <h2 class="section-title">{{ page.content.sections.contributorsTitle }}</h2>
        <div class="contributors-grid">
          <div v-for="c in visibleContributors" :key="c.name" class="contributor">
            <div class="contributor-avatar" :style="c.avatar ? {} : { background: avatarColor(c.name) }"><img v-if="c.avatar" :src="c.avatar" :alt="c.name" /><span v-else>{{ c.name[0] }}</span></div>
            <strong>{{ c.name }}</strong>
            <span>{{ c.commits }} commits</span>
          </div>
        </div>
        <div v-if="hasMoreContributors" class="load-more-wrap reveal">
          <button class="btn btn-outline" @click="loadMoreContributors">
            查看更多贡献者
            <span class="load-count">({{ contributors.length - visibleContributors.length }} 位剩余)</span>
          </button>
        </div>
      </section>

      <section class="community-block reveal">
        <h2>{{ page.content.community.title }}</h2>
        <p>{{ page.content.community.description }}</p>
        <div class="community-links">
          <a :href="page.content.community.github" target="_blank" class="btn btn-primary">{{ page.content.community.githubText }}</a>
          <a :href="page.content.community.discord" target="_blank" class="btn btn-outline">{{ page.content.community.discordText }}</a>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import PaperCard from '@/components/ui/PaperCard.vue'

const store = useSiteConfigStore()
const page = store.getPage('open-source')
useScrollReveal()

const REPO_SIZE = 3
const showRepos = ref(REPO_SIZE)
const repos = computed(() => page.content.repos || [])
const visibleRepos = computed(() => repos.value.slice(0, showRepos.value))
const hasMoreRepos = computed(() => repos.value.length > showRepos.value)
function loadMoreRepos() { showRepos.value += REPO_SIZE }

const CONTRIB_SIZE = 4
const showContributors = ref(CONTRIB_SIZE)
const contributors = computed(() => page.content.contributors || [])
const visibleContributors = computed(() => contributors.value.slice(0, showContributors.value))
const hasMoreContributors = computed(() => contributors.value.length > showContributors.value)
function loadMoreContributors() { showContributors.value += CONTRIB_SIZE }

const colors = ['var(--warm-terracotta)', 'var(--warm-amber)', 'var(--warm-coral)', 'var(--warm-sage)', 'var(--warm-brown)']
function avatarColor(name) {
  let h = 0
  for (let i = 0; i < name.length; i++) h = name.charCodeAt(i) + ((h << 5) - h)
  return colors[Math.abs(h) % colors.length]
}
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero { text-align: center; margin-bottom: 48px; padding: 48px 32px; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.page-hero::after { content: ''; position: absolute; inset: 0; background-image: radial-gradient(circle at 15% 85%, rgba(192, 96, 64, 0.04) 0%, transparent 40%), radial-gradient(circle at 85% 15%, rgba(212, 146, 10, 0.04) 0%, transparent 40%); pointer-events: none; }
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); }
.section-title { font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 24px; text-align: center; }

/* 仓库 */
.repos-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-bottom: 24px; }
.repo-card-link { text-decoration: none; color: inherit; display: block; }
.repo-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.repo-header h3 { font-family: var(--font-heading); font-size: 16px; margin: 0; }
.repo-stars { font-size: 12px; color: var(--text-muted); display: flex; align-items: center; gap: 4px; }
.repos-grid p { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin: 0 0 10px; }

/* 技术栈 */
.tech-tags { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 48px; }

/* 贡献者 */
.contributors-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 24px; margin-bottom: 24px; }
.contributor { text-align: center; }
.contributor-avatar { width: 52px; height: 52px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: var(--font-heading); font-weight: 700; font-size: 18px; color: #fff; margin: 0 auto 8px; overflow: hidden; }
.contributor-avatar img { width: 100%; height: 100%; object-fit: cover; }
.contributor strong { display: block; font-size: 14px; }
.contributor span { font-size: 12px; color: var(--text-muted); }

.load-more-wrap { text-align: center; margin-bottom: 40px; }
.load-count { font-size: 12px; color: var(--text-muted); font-weight: 400; }

.community-block { text-align: center; padding: 56px 32px; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-xl); box-shadow: var(--shadow-lg); position: relative; overflow: hidden; }
.community-block::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.community-block h2 { font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 12px; position: relative; }
.community-block p { color: var(--text-secondary); margin-bottom: 24px; position: relative; }
.community-links { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

@media (max-width: 768px) { .repos-grid { grid-template-columns: 1fr; } }
</style>
