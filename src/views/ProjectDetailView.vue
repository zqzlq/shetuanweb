<template>
  <div class="page-view" v-if="project">
    <div class="container">
      <router-link to="/projects" class="back-link">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M10 12L6 8l4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        返回项目列表
      </router-link>

      <!-- 顶部封面 -->
      <div class="detail-cover" :class="project.coverImage ? '' : 'cover-' + project.coverClass" :style="project.coverImage ? { cursor: 'pointer' } : {}" @click="project.coverImage ? openImageLightbox(project.coverImage) : null">
        <img v-if="project.coverImage" :src="project.coverImage" :alt="project.name" class="cover-img" />
        <div class="cover-pattern"></div>
        <div class="cover-content">
          <span class="tag tag-accent">{{ project.category }}</span>
          <h1>{{ project.name }}</h1>
          <p>{{ project.description }}</p>
        </div>
      </div>

      <div class="detail-layout">
        <!-- 主内容 -->
        <div class="detail-main">
          <div class="detail-body">
            <h2 class="body-title">项目介绍</h2>
            <MarkdownRenderer :content="project.longDescription" />
          </div>

          <!-- 截图画廊 - 左右轮播 -->
          <section v-if="project.screenshots?.length" class="screenshots-section reveal">
            <h2>项目截图</h2>
            <div class="carousel-wrap">
              <button class="carousel-btn carousel-btn-left" @click="scrollScreenshots(-1)" :disabled="!canScrollLeft" :class="{ hidden: !canScrollLeft }">&#8249;</button>
              <div class="screenshots-track" ref="trackRef" @scroll="updateCarouselState">
                <button v-for="(src, i) in project.screenshots" :key="i" class="screenshot-thumb" @click="openLightbox(i)">
                  <img :src="src" :alt="project.name + ' 截图 ' + (i+1)" />
                </button>
              </div>
              <button class="carousel-btn carousel-btn-right" @click="scrollScreenshots(1)" :disabled="!canScrollRight" :class="{ hidden: !canScrollRight }">&#8250;</button>
            </div>
          </section>

          <!-- Lightbox -->
          <Teleport to="body">
            <div v-if="lightboxIndex >= 0" class="lightbox-overlay" @click.self="closeLightbox" @wheel.prevent="onWheel">
              <button class="lightbox-close" @click="closeLightbox" aria-label="关闭">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
              </button>
              <div class="lightbox-container">
                <button v-if="lightboxImages.length > 1" class="lightbox-nav lightbox-prev" @click="prevImage" aria-label="上一张">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
                </button>
                <div class="lightbox-img-wrap" @mousedown="onMouseDown" @mousemove="onMouseMove" @mouseup="onMouseUp" @mouseleave="onMouseUp">
                  <img :src="lightboxImages[lightboxIndex]" class="lightbox-img" alt="大图"
                    :style="{
                      transform: 'scale(' + zoomLevel + ') translate(' + (zoomLevel > 1 ? panX / zoomLevel : 0) + 'px, ' + (zoomLevel > 1 ? panY / zoomLevel : 0) + 'px)',
                      cursor: zoomLevel > 1 ? (isDragging ? 'grabbing' : 'grab') : 'zoom-in'
                    }"
                    @click="toggleZoom" />
                </div>
                <button v-if="lightboxImages.length > 1" class="lightbox-nav lightbox-next" @click="nextImage" aria-label="下一张">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
                </button>
              </div>
              <div class="lightbox-footer">
                <span class="lightbox-counter">{{ lightboxIndex + 1 }} / {{ lightboxImages.length }}</span>
                <span class="lightbox-zoom">{{ Math.round(zoomLevel * 100) }}%</span>
              </div>
            </div>
          </Teleport>

          <!-- 贡献者 -->
          <section v-if="project.contributors.length" class="contributors-section reveal">
            <h2>贡献者</h2>
            <div class="contributors-grid">
              <div v-for="c in project.contributors" :key="c.name" class="contributor">
                <div class="contributor-avatar" :style="c.avatar ? {} : { background: avatarColor(c.name) }"><img v-if="c.avatar" :src="c.avatar" :alt="c.name" /><span v-else>{{ c.name[0] }}</span></div>
                <div class="contributor-info">
                  <strong>{{ c.name }}</strong>
                  <span>{{ c.role }}</span>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- 侧栏 -->
        <aside class="detail-sidebar">
          <div class="sidebar-card">
            <h3>技术栈</h3>
            <div class="tech-list">
              <span v-for="t in project.techStack" :key="t" class="tech-item">{{ t }}</span>
            </div>
          </div>

          <div class="sidebar-card">
            <h3>项目信息</h3>
            <ul class="info-list">
              <li>
                <span class="info-label">状态</span>
                <span class="info-value">
                  <span class="status-dot" :class="project.status"></span>
                  {{ project.status === 'active' ? '进行中' : '开发中' }}
                </span>
              </li>
              <li v-if="project.startDate">
                <span class="info-label">开始时间</span>
                <span class="info-value">{{ project.startDate }}</span>
              </li>
              <li>
                <span class="info-label">分类</span>
                <span class="info-value">{{ project.category }}</span>
              </li>
            </ul>
          </div>

          <div class="sidebar-card" v-if="project.githubUrl || project.demoUrl || project.link">
            <h3>相关链接</h3>
            <div class="link-list">
              <a v-if="project.githubUrl" :href="project.githubUrl" target="_blank" class="link-item">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1C4.15 1 1 4.15 1 8c0 3.1 2 5.7 4.8 6.6.35.07.48-.15.48-.34v-1.2c-1.95.42-2.36-.94-2.36-.94-.32-.81-.78-1.02-.78-1.02-.64-.44.05-.43.05-.43.71.05 1.08.73 1.08.73.63 1.08 1.65.77 2.05.59.06-.46.25-.77.45-.95-1.56-.18-3.2-.78-3.2-3.47 0-.77.28-1.4.73-1.89-.07-.18-.32-.9.07-1.88 0 0 .59-.19 1.94.72a6.76 6.76 0 013.54 0c1.35-.91 1.94-.72 1.94-.72.39.98.14 1.7.07 1.88.45.49.73 1.12.73 1.89 0 2.7-1.64 3.29-3.21 3.46.25.22.48.65.48 1.31v1.94c0 .19.13.42.49.34C13.01 13.7 15 11.1 15 8c0-3.85-3.15-7-7-7z" fill="currentColor"/></svg>
                GitHub
              </a>
              <a v-if="project.demoUrl" :href="project.demoUrl" target="_blank" class="link-item">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6 12l4-4-4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><rect x="1" y="1" width="14" height="14" rx="3" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
                在线演示
              </a>
              <router-link v-if="project.link" :to="project.link" class="link-item">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M6.5 3.5h-3a2 2 0 00-2 2v5a2 2 0 002 2h5a2 2 0 002-2v-3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M9 1l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                访问项目
              </router-link>
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
const project = computed(() => page?.content?.projects?.find((p) => p.slug === route.params.slug))
useScrollReveal()

const lightboxIndex = ref(-1)
const lightboxImages = ref([])
const zoomLevel = ref(1)
const panX = ref(0)
const panY = ref(0)
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const trackRef = ref(null)
const canScrollLeft = ref(false)
const canScrollRight = ref(true)

function openLightbox(i) {
  lightboxImages.value = project.value?.screenshots || []
  lightboxIndex.value = i
  resetView()
}
function openImageLightbox(url) {
  lightboxImages.value = [url, ...(project.value?.screenshots || [])]
  lightboxIndex.value = 0
  resetView()
}
function closeLightbox() { lightboxIndex.value = -1; lightboxImages.value = []; resetView() }
function resetView() { zoomLevel.value = 1; panX.value = 0; panY.value = 0 }
function prevImage() { if (lightboxImages.value.length) { lightboxIndex.value = (lightboxIndex.value - 1 + lightboxImages.value.length) % lightboxImages.value.length; resetView() } }
function nextImage() { if (lightboxImages.value.length) { lightboxIndex.value = (lightboxIndex.value + 1) % lightboxImages.value.length; resetView() } }

function toggleZoom(e) {
  if (zoomLevel.value === 1) zoomLevel.value = 2
  else if (zoomLevel.value === 2) zoomLevel.value = 3
  else resetView()
}
function onWheel(e) {
  if (lightboxIndex.value < 0) return
  e.preventDefault()
  zoomLevel.value = Math.max(0.5, Math.min(5, zoomLevel.value + (e.deltaY > 0 ? -0.25 : 0.25)))
  if (zoomLevel.value === 1) { panX.value = 0; panY.value = 0 }
}

function onMouseDown(e) {
  if (zoomLevel.value <= 1) return
  isDragging.value = true
  dragStart.value = { x: e.clientX - panX.value, y: e.clientY - panY.value }
  e.preventDefault()
}
function onMouseMove(e) {
  if (!isDragging.value) return
  panX.value = e.clientX - dragStart.value.x
  panY.value = e.clientY - dragStart.value.y
}
function onMouseUp() { isDragging.value = false }

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

function onKeydown(e) {
  if (lightboxIndex.value < 0) return
  if (e.key === 'Escape') closeLightbox()
  if (e.key === 'ArrowLeft') { if (zoomLevel.value > 1) { panX.value += 60; e.preventDefault() } else { prevImage() } }
  if (e.key === 'ArrowRight') { if (zoomLevel.value > 1) { panX.value -= 60; e.preventDefault() } else { nextImage() } }
  if (e.key === 'ArrowUp' && zoomLevel.value > 1) { panY.value += 60; e.preventDefault() }
  if (e.key === 'ArrowDown' && zoomLevel.value > 1) { panY.value -= 60; e.preventDefault() }
}
onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))

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

/* 封面 */
.detail-cover {
  height: 280px;
  border-radius: var(--radius-xl);
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 40px;
  margin-bottom: 40px;
  overflow: hidden;
}
.cover-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle at 30% 40%, rgba(255,255,255,0.15) 0%, transparent 50%),
                     radial-gradient(circle at 70% 60%, rgba(255,255,255,0.1) 0%, transparent 40%);
  pointer-events: none;
}

.cover-content {
  position: relative;
  z-index: 1;
}

.cover-content h1 {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  color: #fff;
  margin: 12px 0 8px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.cover-content p {
  color: rgba(255,255,255,0.85);
  font-size: 15px;
  max-width: 500px;
}

.cover-aurora { background: linear-gradient(135deg, #c06040, #d4920a); }
.cover-meteor { background: linear-gradient(135deg, #d4920a, #c07080); }
.cover-nebula { background: linear-gradient(135deg, #c06040, #7a9a6a); }
.cover-cosmos { background: linear-gradient(135deg, #7a9a6a, #8b7355); }
.cover-pulse { background: linear-gradient(135deg, #c07080, #e07050); }
.cover-horizon { background: linear-gradient(135deg, #8b7355, #c06040); }

/* 双栏布局 */
.detail-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 32px;
  align-items: start;
}

.detail-main {
  min-width: 0;
}

.body-title {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.detail-body {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-sm);
}

/* 贡献者 */
.contributors-section {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 32px;
  box-shadow: var(--shadow-sm);
}

.contributors-section h2 {
  font-family: var(--font-heading);
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.contributors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.contributor {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: var(--radius-md);
  background: var(--bg);
  transition: background 0.2s;
}

.contributor:hover {
  background: var(--bg-soft);
}

.contributor-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 16px;
  color: #fff;
  flex-shrink: 0;
  overflow: hidden;
}
.contributor-avatar img { width: 100%; height: 100%; object-fit: cover;
}

.contributor-info strong {
  display: block;
  font-size: 14px;
}

.contributor-info span {
  font-size: 12px;
  color: var(--text-muted);
}

/* 侧栏 */
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
  color: var(--text-primary);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--glass-border);
}

.tech-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-item {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: var(--bg-soft);
  color: var(--text-secondary);
  border: 1px solid var(--glass-border);
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

.info-label {
  color: var(--text-muted);
}

.info-value {
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.active { background: #00a050; }
.status-dot.wip { background: #b48200; }

.link-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.link-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  background: var(--bg);
  border: 1px solid var(--glass-border);
  transition: all 0.2s;
}

.link-item:hover {
  background: var(--bg-soft);
  border-color: var(--warm-terracotta);
  color: var(--warm-terracotta);
}

/* 截图画廊 */
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
.carousel-wrap { position: relative; display: flex; align-items: center; }
.screenshots-track {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none;
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
  width: 36px; height: 36px;
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
  position: absolute; top: 20px; right: 24px;
  background: rgba(255,255,255,0.1); border: none; color: white;
  width: 44px; height: 44px; border-radius: 50%;
  cursor: pointer; z-index: 10;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.2s;
}
.lightbox-close:hover { background: rgba(255,255,255,0.25); }
.lightbox-container {
  position: relative; display: flex; align-items: center;
  gap: 12px; width: 100vw; height: 100vh; justify-content: center;
}
.lightbox-img-wrap {
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
  width: 100vw; height: 100vh;
}
.lightbox-img {
  width: 100vw; height: 100vh;
  object-fit: contain;
  transition: transform 0.25s ease;
  user-select: none;
  display: block;
  padding: 20px;
}
.lightbox-nav {
  flex-shrink: 0; width: 48px; height: 48px; border-radius: 50%;
  background: rgba(255,255,255,0.12); border: none; color: white;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: background 0.2s, transform 0.2s;
}
.lightbox-nav:hover { background: rgba(255,255,255,0.25); transform: scale(1.1); }
.lightbox-footer {
  position: absolute; bottom: 28px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 10px; align-items: center;
}
.lightbox-counter, .lightbox-zoom {
  color: rgba(255,255,255,0.6); font-size: 14px;
  background: rgba(0,0,0,0.4); padding: 4px 16px; border-radius: 999px;
  font-variant-numeric: tabular-nums;
}
.lightbox-zoom { background: rgba(192,96,64,0.3); color: rgba(255,255,255,0.85); }
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
  .detail-sidebar {
    position: static;
  }
  .detail-cover {
    height: 200px;
    padding: 28px;
  }
}
</style>
