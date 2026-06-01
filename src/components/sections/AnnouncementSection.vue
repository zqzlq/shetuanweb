<template>
  <section id="announcements" ref="sectionRef" class="announcements-section">
    <div class="warm-glow" aria-hidden="true"></div>
    <div class="section-deco-line" aria-hidden="true"></div>
    <div class="bg-dots" aria-hidden="true"></div>
    <div class="container">
      <div class="section-heading">
        <p class="eyebrow">ANNOUNCEMENTS</p>
        <div class="heading-row">
          <h2>公告通知</h2>
          <router-link to="/blog" class="btn btn-outline btn-sm">查看全部</router-link>
        </div>
        <p>了解实验室最新动态和重要通知</p>
      </div>

      <div class="announce-grid">
        <router-link
          v-for="item in items"
          :key="item.title"
          to="/blog"
          class="announce-link"
        >
          <div class="announce-card" :class="{ pinned: item.pinned }">
            <div class="announce-top">
              <span v-if="item.pinned" class="pin-badge">置顶</span>
              <span class="tag tag-accent">{{ item.category }}</span>
              <span class="announce-date">{{ item.date }}</span>
            </div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.excerpt }}</p>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'

const store = useSiteConfigStore()
const page = store.getPage('blog')

const items = computed(() => {
  const list = page?.content?.posts || []
  return [...list]
    .filter((p) => p.category === '公告' || p.pinned)
    .sort((a, b) => {
      if (a.pinned && !b.pinned) return -1
      if (!a.pinned && b.pinned) return 1
      return b.date.localeCompare(a.date)
    })
    .slice(0, 3)
    .map((p) => ({
      title: p.title,
      excerpt: p.excerpt,
      category: p.category,
      date: p.date,
      pinned: p.pinned,
    }))
})
</script>

<style scoped>
.announcements-section {
  position: relative;
  padding: 100px 0;
  overflow: hidden;
  background: var(--bg-soft);
}

.bg-dots {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(192, 96, 64, 0.04) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
}

.warm-glow {
  position: absolute;
  top: 30%;
  left: 10%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(192, 96, 64, 0.06) 0%, transparent 70%);
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
}

.heading-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 13px;
}

.announce-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.announce-link {
  text-decoration: none;
  color: inherit;
}

.announce-card {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 28px;
  transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
  position: relative;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.announce-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--grad-primary);
  opacity: 0;
  transition: opacity 0.3s;
}

.announce-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: var(--warm-terracotta);
}

.announce-card:hover::before {
  opacity: 1;
}

.announce-card.pinned {
  border-left: 3px solid var(--warm-terracotta);
}

.announce-top {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}

.pin-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--warm-terracotta);
  color: white;
}

.announce-date {
  font-size: 12px;
  color: var(--text-muted);
  margin-left: auto;
}

.announce-card h3 {
  font-family: var(--font-heading);
  font-size: 17px;
  margin: 0 0 10px;
  color: var(--text-primary);
}

.announce-card p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

@media (max-width: 768px) {
  .announcements-section { padding: 60px 0; }
  .announce-grid { grid-template-columns: 1fr; }
}
</style>
