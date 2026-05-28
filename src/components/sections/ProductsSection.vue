<template>
  <section id="products" ref="sectionRef" class="products-section">
    <div class="warm-glow" aria-hidden="true"></div>
    <div class="section-deco-line" aria-hidden="true"></div>
    <div class="container">
      <div class="section-heading">
        <p class="eyebrow">PRODUCTS</p>
        <div class="heading-row">
          <h2>{{ config.products.title }}</h2>
          <router-link to="/projects" class="btn btn-outline btn-sm">查看全部</router-link>
        </div>
        <p>{{ config.products.description }}</p>
      </div>

      <div class="filter-tabs">
        <button
          v-for="cat in config.products.categories"
          :key="cat"
          class="filter-tab"
          :class="{ active: activeCat === cat }"
          @click="activeCat = cat"
        >
          {{ cat }}
        </button>
      </div>

      <div class="carousel-wrap">
        <button class="carousel-arrow carousel-arrow-left" @click="scrollBy(-1)" :class="{ disabled: !canScrollLeft }" aria-label="上一页">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M11 4L6 9l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div class="carousel-track" ref="trackRef" @scroll="updateScrollState">
          <router-link
            v-for="project in filteredProjects"
            :key="project.slug"
            :to="`/project/${project.slug}`"
            class="product-card-link"
          >
            <div class="product-card">
              <div class="card-cover" :class="project.coverImage ? '' : 'cover-' + project.coverClass">
                <img v-if="project.coverImage" :src="project.coverImage" :alt="project.name" class="cover-img" />
                <span class="card-category">{{ project.category }}</span>
                <div class="cover-pattern"></div>
              </div>
              <div class="card-body">
                <h3>{{ project.name }}</h3>
                <p>{{ project.description }}</p>
                <div class="card-tags">
                  <span v-for="t in project.techStack" :key="t" class="tag">{{ t }}</span>
                </div>
              </div>
            </div>
          </router-link>
        </div>
        <button class="carousel-arrow carousel-arrow-right" @click="scrollBy(1)" :class="{ disabled: !canScrollRight }" aria-label="下一页">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M7 4l5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useInkReveal } from '@/composables/useInkReveal'

const { config } = useSiteConfigStore()
const sectionRef = ref(null)
const trackRef = ref(null)
const activeCat = ref('精选总览')
const canScrollLeft = ref(false)
const canScrollRight = ref(true)

useInkReveal(sectionRef)

const allProjects = computed(() => {
  const seen = new Set()
  return config.products.slides.flatMap((s) => s.projects).filter((p) => {
    if (seen.has(p.slug)) return false
    seen.add(p.slug)
    return true
  })
})

const filteredProjects = computed(() => {
  if (activeCat.value === '精选总览') {
    return allProjects.value.filter((p) => p.featured)
  }
  return allProjects.value.filter((p) => p.category === activeCat.value)
})

function updateScrollState() {
  const el = trackRef.value
  if (!el) return
  canScrollLeft.value = el.scrollLeft > 10
  canScrollRight.value = el.scrollLeft < el.scrollWidth - el.clientWidth - 10
}

function scrollBy(dir) {
  const el = trackRef.value
  if (!el) return
  const cardWidth = el.querySelector('.product-card')?.offsetWidth || 320
  el.scrollBy({ left: dir * (cardWidth + 24), behavior: 'smooth' })
}

onMounted(() => { nextTick(updateScrollState) })
</script>

<style scoped>
.products-section {
  position: relative;
  padding: 100px 0;
  overflow: hidden;
}

.warm-glow {
  position: absolute;
  top: 20%;
  left: 50%;
  width: 400px;
  height: 400px;
  margin: -200px 0 0 -200px;
  background: radial-gradient(circle, rgba(212, 146, 10, 0.06) 0%, transparent 70%);
  border-radius: 50%;
  filter: blur(40px);
  pointer-events: none;
}

.section-deco-line {
  position: absolute;
  top: 0;
  left: 8%;
  right: 8%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(192, 96, 64, 0.12), var(--glass-border), rgba(212, 146, 10, 0.08), transparent);
  transform-origin: center;
}

.heading-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 13px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-tab {
  padding: 8px 20px;
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab:hover {
  border-color: var(--glass-border-hover);
  color: var(--text-primary);
  background: #fff;
}

.filter-tab.active {
  background: var(--grad-primary);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 16px rgba(192, 96, 64, 0.2);
}

/* 轮播 */
.carousel-wrap {
  position: relative;
}

.carousel-track {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  padding: 4px 4px 20px 4px;
  scrollbar-width: none;
}

.carousel-track::-webkit-scrollbar {
  display: none;
}

.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--glass-border);
  background: #fff;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 2;
  box-shadow: var(--shadow-md);
  transition: all 0.2s;
}

.carousel-arrow:hover {
  background: var(--grad-primary);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 4px 20px rgba(192, 96, 64, 0.3);
}

.carousel-arrow.disabled {
  opacity: 0.3;
  pointer-events: none;
}

.carousel-arrow-left {
  left: -16px;
}

.carousel-arrow-right {
  right: -16px;
}

/* 卡片链接 */
.product-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  flex: 0 0 300px;
  scroll-snap-align: start;
}

/* 卡片 */
.product-card {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease, border-color 0.4s ease;
  box-shadow: var(--shadow-sm);
}

.product-card-link:hover .product-card {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 24px 64px rgba(120, 90, 60, 0.14);
  border-color: var(--glass-border-hover);
}

.card-cover {
  height: 180px;
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 16px;
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

.cover-aurora { background: linear-gradient(135deg, #c06040 0%, #d4920a 100%); }
.cover-meteor { background: linear-gradient(135deg, #d4920a 0%, #c07080 100%); }
.cover-nebula { background: linear-gradient(135deg, #c06040 0%, #7a9a6a 100%); }
.cover-cosmos { background: linear-gradient(135deg, #7a9a6a 0%, #8b7355 100%); }
.cover-pulse { background: linear-gradient(135deg, #c07080 0%, #e07050 100%); }
.cover-horizon { background: linear-gradient(135deg, #8b7355 0%, #c06040 100%); }

.card-category {
  font-size: 12px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  background: rgba(0, 0, 0, 0.2);
  padding: 4px 14px;
  border-radius: 999px;
  position: relative;
  z-index: 1;
}

.card-body {
  padding: 20px;
}

.card-body h3 {
  font-family: var(--font-heading);
  font-size: 17px;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--text-primary);
}

.card-body p {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0 0 14px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

@media (max-width: 768px) {
  .product-card-link {
    flex: 0 0 260px;
  }
  .carousel-arrow {
    display: none;
  }
}
</style>
