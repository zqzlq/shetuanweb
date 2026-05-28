<template>
  <div class="page-view" v-if="award">
    <div class="container">
      <router-link to="/projects" class="back-link">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 12L6 8l4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        返回项目列表
      </router-link>

      <div class="award-header reveal" :class="{ 'has-image': award.image }" @click="award.image ? openImageLightbox(award.image) : null" :style="award.image ? { backgroundImage: 'url(' + award.image + ')' } : {}" :title="award.image ? '点击查看大图' : ''">
        <div class="award-header-overlay"></div>
        <div class="award-header-content">
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
      </div>

      <!-- 截图画廊 - 左右轮播 -->
      <section v-if="award.screenshots?.length" class="screenshots-section reveal">
        <h2>相关图片</h2>
        <div class="carousel-wrap">
          <button class="carousel-btn carousel-btn-left" @click="scrollScreenshots(-1)" :disabled="!canScrollLeft" :class="{ hidden: !canScrollLeft }">&#8249;</button>
          <div class="screenshots-track" ref="trackRef" @scroll="updateCarouselState">
            <button v-for="(src, i) in award.screenshots" :key="i" class="screenshot-thumb" @click="openLightbox(i)">
              <img :src="src" :alt="award.title + ' 图片 ' + (i+1)" />
            </button>
          </div>
          <button class="carousel-btn carousel-btn-right" @click="scrollScreenshots(1)" :disabled="!canScrollRight" :class="{ hidden: !canScrollRight }">&#8250;</button>
        </div>
      </section>

      <!-- Lightbox -->
      <Teleport to="body">
        <div v-if="lightboxIndex >= 0" class="lightbox-overlay" @click.self="closeLightbox">
          <button class="lightbox-close" @click="closeLightbox" aria-label="关闭">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
          </button>
          <div class="lightbox-container">
            <button v-if="lightboxImages.length > 1" class="lightbox-nav lightbox-prev" @click="prevImage" aria-label="上一张">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
            </button>
            <img :src="lightboxImages[lightboxIndex]" class="lightbox-img" alt="大图" />
            <button v-if="lightboxImages.length > 1" class="lightbox-nav lightbox-next" @click="nextImage" aria-label="下一张">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
            </button>
          </div>
          <div class="lightbox-footer">
            <span class="lightbox-counter">{{ lightboxIndex + 1 }} / {{ lightboxImages.length }}</span>
          </div>
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
                <div class="participant-avatar" :style="memberAvatarMap[name] ? {} : { background: avatarColor(name) }"><img v-if="memberAvatarMap[name]" :src="memberAvatarMap[name]" :alt="name" /><span v-else>{{ name[0] }}</span></div>
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
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import MarkdownRenderer from '@/components/ui/MarkdownRenderer.vue'

const route = useRoute()
const store = useSiteConfigStore()
const page = store.getPage('projects')
const membersPage = store.getPage('members')
const award = computed(() => page?.content?.awards?.items?.find((a) => a.slug === route.params.slug))
const relatedProject = computed(() => {
  if (!award.value?.projectSlug) return null
  return page?.content?.projects?.find((p) => p.slug === award.value.projectSlug)
})

const memberAvatarMap = computed(() => {
  const map = {}
  for (const m of membersPage?.content?.members || []) {
    if (m.avatar) map[m.name] = m.avatar
  }
  return map
})
useScrollReveal()

const lightboxIndex = ref(-1)
const lightboxImages = ref([])
const trackRef = ref(null)
const canScrollLeft = ref(false)
const canScrollRight = ref(true)

function openLightbox(i) {
  lightboxImages.value = award.value?.screenshots || []
  lightboxIndex.value = i
}
function openImageLightbox(url) {
  lightboxImages.value = [url, ...(award.value?.screenshots || [])]
  lightboxIndex.value = 0
}
function closeLightbox() { lightboxIndex.value = -1; lightboxImages.value = [] }
function prevImage() { if (lightboxImages.value.length) lightboxIndex.value = (lightboxIndex.value - 1 + lightboxImages.value.length) % lightboxImages.value.length }
function nextImage() { if (lightboxImages.value.length) lightboxIndex.value = (lightboxIndex.value + 1) % lightboxImages.value.length }

// 键盘导航
function onKeydown(e) {
  if (lightboxIndex.value < 0) return
  if (e.key === 'Escape') closeLightbox()
  if (e.key === 'ArrowLeft') prevImage()
  if (e.key === 'ArrowRight') nextImage()
}
onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))

function scrollScreenshots(dir) {
  const el = trackRef.value
  if (!el) return
  el.scrollBy({ left: el.clientWidth * 0.6 * dir, behavior: 'smooth' })
}

function updateCarouselState() {
  const el = trackRef.value
  if (!el) return
  canScrollLeft.value = el.scrollLeft > 10
  canScrollRight.value = el.scrollLeft < el.scrollWidth - el.clientWidth - 10
}

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
  padding: 0;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
}

.award-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--grad-primary);
  z-index: 2;
}

.award-header.has-image { border-color: transparent; }

.award-header-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1;
}

.award-header.has-image .award-header-overlay {
  background: rgba(0,0,0,0.55);
}

.award-header-content {
  position: relative;
  z-index: 2;
  padding: 48px 32px;
  max-width: 700px;
}

.award-medal {
  margin-bottom: 16px;
}

.award-header h1 {
  font-size: clamp(1.5rem, 3.5vw, 2.2rem);
  margin: 12px 0;
}

.award-header.has-image h1,
.award-header.has-image .award-desc {
  color: #fff;
  text-shadow: 0 1px 4px rgba(0,0,0,0.3);
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
  overflow: hidden;
}
.participant-avatar img { width: 100%; height: 100%; object-fit: cover; }

/* 截图轮播 */
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
.carousel-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.screenshots-track {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none;
  padding-bottom: 4px;
  flex: 1;
}
.screenshots-track::-webkit-scrollbar { display: none; }
.screenshot-thumb {
  border: none;
  padding: 0;
  cursor: pointer;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--glass-border);
  transition: transform 0.2s, box-shadow 0.2s;
  background: none;
  flex-shrink: 0;
  width: 220px;
}
.screenshot-thumb:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
.screenshot-thumb img {
  width: 220px;
  height: 160px;
  object-fit: cover;
  display: block;
}
.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: rgba(0,0,0,0.5);
  color: white;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: opacity 0.2s, background 0.2s;
}
.carousel-btn:hover { background: rgba(0,0,0,0.75); }
.carousel-btn:disabled { opacity: 0; pointer-events: none; }
.carousel-btn.hidden { display: none; }
.carousel-btn-left { left: -18px; }
.carousel-btn-right { right: -18px; }

/* Lightbox */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.88);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(8px);
  animation: lbFadeIn 0.2s ease;
}
@keyframes lbFadeIn { from { opacity: 0; } to { opacity: 1; } }
.lightbox-close {
  position: absolute;
  top: 20px;
  right: 24px;
  background: rgba(255,255,255,0.1);
  border: none;
  color: white;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.lightbox-close:hover { background: rgba(255,255,255,0.25); }
.lightbox-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  max-width: 92vw;
}
.lightbox-img {
  max-width: 85vw;
  max-height: 82vh;
  border-radius: 12px;
  object-fit: contain;
  box-shadow: 0 8px 40px rgba(0,0,0,0.5);
  user-select: none;
}
.lightbox-nav {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255,255,255,0.12);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, transform 0.2s;
}
.lightbox-nav:hover { background: rgba(255,255,255,0.25); transform: scale(1.1); }
.lightbox-footer {
  position: absolute;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
}
.lightbox-counter {
  color: rgba(255,255,255,0.6);
  font-size: 14px;
  background: rgba(0,0,0,0.4);
  padding: 4px 16px;
  border-radius: 999px;
  font-variant-numeric: tabular-nums;
}

@media (max-width: 900px) {
  .detail-layout {
    grid-template-columns: 1fr;
  }
  .detail-sidebar { position: static; }
  .project-cover { display: none; }
}
</style>
