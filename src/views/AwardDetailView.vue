<template>
  <div class="page-view" v-if="award">
    <div class="container">
      <router-link to="/projects" class="back-link">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 12L6 8l4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        返回项目列表
      </router-link>

      <div class="award-header reveal">
        <img v-if="award.image" :src="award.image" :alt="award.title" class="award-image" />
        <div class="award-medal">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
            <circle cx="20" cy="16" r="12" fill="var(--warm-amber)" opacity="0.15"/>
            <path d="M20 4l4 9h9l-7 5.5 2.5 9L20 22l-8.5 5.5 2.5-9-7-5.5h9l4-9z" fill="var(--warm-amber)"/>
          </svg>
        </div>
        <span class="tag tag-accent">{{ award.category }}</span>
        <h1>{{ award.title }}</h1>
        <p class="award-desc">{{ award.description }}</p>
      </div>

      <!-- 图片画廊 -->
      <section v-if="award.screenshots?.length" class="screenshots-section reveal">
        <h2>相关图片</h2>
        <div class="screenshots-grid">
          <button v-for="(src, i) in award.screenshots" :key="i" class="screenshot-thumb" @click="openLightbox(i)">
            <img :src="src" :alt="award.title + ' 图片 ' + (i+1)" />
          </button>
        </div>
      </section>

      <!-- Lightbox -->
      <Teleport to="body">
        <div v-if="lightboxIndex >= 0" class="lightbox-overlay" @click.self="closeLightbox">
          <button class="lightbox-close" @click="closeLightbox">&times;</button>
          <button class="lightbox-prev" @click="prevImage">&#8249;</button>
          <img :src="award.screenshots[lightboxIndex]" class="lightbox-img" />
          <button class="lightbox-next" @click="nextImage">&#8250;</button>
          <div class="lightbox-counter">{{ lightboxIndex + 1 }} / {{ award.screenshots.length }}</div>
        </div>
      </Teleport>

      <div class="detail-layout">
        <div class="detail-main">
          <div class="detail-body reveal">
            <h2 class="body-title">详细介绍</h2>
            <MarkdownRenderer :content="award.longDescription" />
          </div>

          <section v-if="award.projectSlug" class="related-project reveal">
            <h2>相关项目</h2>
            <router-link :to="`/project/${award.projectSlug}`" class="project-link-card">
              <div class="project-cover" :class="'cover-' + relatedProject?.coverClass"></div>
              <div class="project-info">
                <span class="tag tag-accent">{{ relatedProject?.category }}</span>
                <h3>{{ relatedProject?.name }}</h3>
                <p>{{ relatedProject?.description }}</p>
              </div>
            </router-link>
          </section>
        </div>

        <aside class="detail-sidebar">
          <div class="sidebar-card">
            <h3>奖项信息</h3>
            <ul class="info-list">
              <li>
                <span class="info-label">级别</span>
                <span class="info-value highlight">{{ award.level }}</span>
              </li>
              <li>
                <span class="info-label">时间</span>
                <span class="info-value">{{ award.date }}</span>
              </li>
              <li>
                <span class="info-label">类别</span>
                <span class="info-value">{{ award.category }}</span>
              </li>
            </ul>
          </div>

          <div class="sidebar-card">
            <h3>参赛成员</h3>
            <div class="participant-list">
              <div v-for="(name, i) in award.participants" :key="name" class="participant">
                <div class="participant-avatar" :style="{ background: avatarColor(name) }">{{ name[0] }}</div>
                <span>{{ name }}</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import MarkdownRenderer from '@/components/ui/MarkdownRenderer.vue'

const route = useRoute()
const store = useSiteConfigStore()
const page = store.getPage('projects')
const award = computed(() => page?.content?.awards?.items?.find((a) => a.slug === route.params.slug))
const relatedProject = computed(() => {
  if (!award.value?.projectSlug) return null
  return page?.content?.projects?.find((p) => p.slug === award.value.projectSlug)
})
useScrollReveal()

const lightboxIndex = ref(-1)
function openLightbox(i) { lightboxIndex.value = i }
function closeLightbox() { lightboxIndex.value = -1 }
function prevImage() { lightboxIndex.value = (lightboxIndex.value - 1 + award.value.screenshots.length) % award.value.screenshots.length }
function nextImage() { lightboxIndex.value = (lightboxIndex.value + 1) % award.value.screenshots.length }

const colors = ['var(--warm-terracotta)', 'var(--warm-amber)', 'var(--warm-coral)', 'var(--warm-sage)', 'var(--warm-brown)']
function avatarColor(name) {
  let h = 0
  for (let i = 0; i < name.length; i++) h = name.charCodeAt(i) + ((h << 5) - h)
  return colors[Math.abs(h) % colors.length]
}
</script>

<style scoped>
.page-view { padding: 120px 0 60px; }

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 28px;
  transition: color 0.2s;
}
.back-link:hover { color: var(--warm-terracotta); }

.award-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 48px 32px;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}

.award-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--grad-primary);
}

.award-medal {
  margin-bottom: 16px;
}
.award-image {
  max-width: 400px;
  width: 100%;
  border-radius: var(--radius-md);
  margin-bottom: 16px;
  object-fit: cover;
}

.award-header h1 {
  font-size: clamp(1.5rem, 3.5vw, 2.2rem);
  margin: 12px 0;
}

.award-desc {
  font-size: 16px;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.8;
}

.detail-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 32px;
  align-items: start;
}

.detail-main { min-width: 0; }

.body-title {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  margin-bottom: 20px;
}

.detail-body {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-sm);
}

.related-project h2 {
  font-family: var(--font-heading);
  font-size: 1.2rem;
  margin-bottom: 16px;
}

.project-link-card {
  display: flex;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
  text-decoration: none;
  color: inherit;
}

.project-link-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--glass-border-hover);
}

.project-cover {
  width: 160px;
  flex-shrink: 0;
}

.cover-aurora { background: linear-gradient(135deg, #c06040, #d4920a); }
.cover-meteor { background: linear-gradient(135deg, #d4920a, #c07080); }
.cover-nebula { background: linear-gradient(135deg, #c06040, #7a9a6a); }
.cover-cosmos { background: linear-gradient(135deg, #7a9a6a, #8b7355); }
.cover-pulse { background: linear-gradient(135deg, #c07080, #e07050); }
.cover-horizon { background: linear-gradient(135deg, #8b7355, #c06040); }

.project-info {
  padding: 20px;
}

.project-info h3 {
  font-family: var(--font-heading);
  font-size: 17px;
  margin: 8px 0;
}

.project-info p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0;
}

.detail-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 100px;
}

.sidebar-card {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.sidebar-card h3 {
  font-family: var(--font-heading);
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--glass-border);
}

.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.info-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.info-label { color: var(--text-muted); }

.info-value {
  font-weight: 600;
  color: var(--text-primary);
}

.info-value.highlight {
  color: var(--warm-terracotta);
  font-weight: 700;
}

.participant-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.participant {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 500;
}

.participant-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 14px;
  color: #fff;
  flex-shrink: 0;
}

/* 图片画廊 */
.screenshots-section {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-sm);
}
.screenshots-section h2 {
  font-family: var(--font-heading);
  font-size: 1.2rem;
  margin-bottom: 20px;
}
.screenshots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}
.screenshot-thumb {
  border: none;
  padding: 0;
  cursor: pointer;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--glass-border);
  transition: transform 0.2s, box-shadow 0.2s;
  background: none;
}
.screenshot-thumb:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
.screenshot-thumb img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

/* Lightbox */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.85);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.lightbox-img {
  max-width: 90vw;
  max-height: 85vh;
  border-radius: 8px;
  object-fit: contain;
}
.lightbox-close {
  position: absolute;
  top: 20px;
  right: 24px;
  background: none;
  border: none;
  color: white;
  font-size: 36px;
  cursor: pointer;
  z-index: 1;
}
.lightbox-prev, .lightbox-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.15);
  border: none;
  color: white;
  font-size: 40px;
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 8px;
  z-index: 1;
}
.lightbox-prev { left: 20px; }
.lightbox-next { right: 20px; }
.lightbox-prev:hover, .lightbox-next:hover { background: rgba(255,255,255,0.3); }
.lightbox-counter {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255,255,255,0.7);
  font-size: 14px;
}

@media (max-width: 900px) {
  .detail-layout {
    grid-template-columns: 1fr;
  }
  .detail-sidebar { position: static; }
  .project-cover { display: none; }
}
</style>
