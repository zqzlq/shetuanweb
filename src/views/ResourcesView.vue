<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <h1>知识库</h1>
        <p class="page-subtitle">实验室学习资源、文档与工具合集</p>
        <button v-if="isLoggedIn" class="btn btn-primary hero-btn" @click="showContribute = true">贡献资源</button>
      </div>

      <!-- 未登录提示 -->
      <div v-if="!isLoggedIn" class="login-prompt reveal">
        <PaperCard>
          <div class="prompt-content">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <h3>仅限登录用户访问</h3>
            <p>知识库为实验室内部功能，请先登录后再访问</p>
            <button class="btn btn-primary" @click="$router.push('/')">返回首页</button>
          </div>
        </PaperCard>
      </div>

      <!-- 已登录：知识库 -->
      <template v-else>
        <div class="kb-layout">
          <!-- 左侧边栏 -->
          <aside class="kb-sidebar">
            <!-- 分类导航 -->
            <div class="sidebar-section">
              <h4 class="sidebar-title">资源分类</h4>
              <nav class="category-nav">
                <button
                  v-for="cat in categoryOptions"
                  :key="cat.key"
                  class="cat-nav-item"
                  :class="{ active: activeCategory === cat.key }"
                  @click="activeCategory = cat.key; loadResources(true)"
                >
                  <span class="cat-label">{{ cat.label }}</span>
                  <span v-if="catCounts[cat.key]" class="cat-count">{{ catCounts[cat.key] }}</span>
                </button>
              </nav>
            </div>

            <!-- 标签云 -->
            <div v-if="tagList.length" class="sidebar-section">
              <h4 class="sidebar-title">热门标签</h4>
              <div class="tag-cloud">
                <button
                  v-for="tag in tagList"
                  :key="tag.name"
                  class="tag-pill"
                  :class="{ active: activeTag === tag.name }"
                  @click="activeTag = activeTag === tag.name ? '' : tag.name; loadResources(true)"
                >
                  {{ tag.name }} ({{ tag.count }})
                </button>
              </div>
            </div>
          </aside>

          <!-- 主内容区 -->
          <main class="kb-main">
            <!-- 工具栏 -->
            <div class="kb-toolbar">
              <div class="search-box">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                <input v-model="searchQuery" type="text" placeholder="搜索资源标题或描述..." @keyup.enter="loadResources(true)" />
                <button v-if="searchQuery" class="clear-btn" @click="searchQuery = ''; loadResources(true)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </button>
              </div>
              <div class="toolbar-right">
                <span class="result-count">{{ total }} 个资源</span>
                <button class="view-toggle" :class="{ active: viewMode === 'card' }" @click="viewMode = 'card'" title="卡片视图">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/></svg>
                </button>
                <button class="view-toggle" :class="{ active: viewMode === 'list' }" @click="viewMode = 'list'" title="列表视图">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/></svg>
                </button>
              </div>
            </div>

            <!-- 活跃标签筛选 -->
            <div v-if="activeTag" class="active-filter">
              <span>标签筛选：</span>
              <span class="filter-tag">{{ activeTag }} <button @click="activeTag = ''; loadResources(true)">&times;</button></span>
            </div>

            <!-- 加载中 -->
            <div v-if="loading && resources.length === 0" class="kb-loading">加载中...</div>

            <!-- 空状态 -->
            <div v-else-if="!loading && resources.length === 0" class="kb-empty">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>
              <p>{{ searchQuery ? '未找到匹配的资源' : '暂无资源' }}</p>
            </div>

            <!-- 卡片视图 -->
            <div v-else-if="viewMode === 'card'" class="resources-grid">
              <PaperCard v-for="r in resources" :key="r.id" class="resource-card" hover>
                <div class="rc-header">
                  <span class="rc-category" :class="'cat-' + r.category">{{ categoryLabels[r.category] || r.category }}</span>
                  <span class="rc-type">{{ r.file_type?.toUpperCase() }}</span>
                </div>
                <h3 class="rc-title" @click="openPreview(r)">{{ r.title }}</h3>
                <p v-if="r.description" class="rc-desc">{{ r.description }}</p>
                <div v-if="r.tags?.length" class="rc-tags">
                  <span v-for="tag in r.tags.slice(0, 3)" :key="tag" class="rc-tag" @click="activeTag = tag; loadResources(true)">{{ tag }}</span>
                </div>
                <div class="rc-meta">
                  <span class="meta-item">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                    {{ r.download_count }}
                  </span>
                  <span class="meta-item">{{ formatFileSize(r.file_size) }}</span>
                </div>
                <div class="rc-actions">
                  <button class="btn btn-outline btn-sm" @click="openPreview(r)">预览</button>
                  <button class="btn btn-primary btn-sm" :disabled="downloadingId === r.id" @click="handleDownload(r)">
                    {{ downloadingId === r.id ? '...' : '下载' }}
                  </button>
                </div>
              </PaperCard>
            </div>

            <!-- 列表视图 -->
            <div v-else class="resources-list">
              <div v-for="r in resources" :key="r.id" class="list-item" @click="openPreview(r)">
                <div class="li-icon" :class="'cat-' + r.category">
                  {{ r.file_type?.toUpperCase().slice(0, 3) }}
                </div>
                <div class="li-body">
                  <div class="li-title">{{ r.title }}</div>
                  <div class="li-meta">
                    <span class="li-cat">{{ categoryLabels[r.category] }}</span>
                    <span>{{ r.file_name }}</span>
                    <span>{{ formatFileSize(r.file_size) }}</span>
                    <span>{{ r.download_count }} 次下载</span>
                  </div>
                </div>
                <div v-if="r.tags?.length" class="li-tags">
                  <span v-for="tag in r.tags.slice(0, 2)" :key="tag" class="rc-tag">{{ tag }}</span>
                </div>
                <div class="li-actions" @click.stop>
                  <button class="btn btn-outline btn-sm" @click="openPreview(r)">预览</button>
                  <button class="btn btn-primary btn-sm" :disabled="downloadingId === r.id" @click="handleDownload(r)">
                    {{ downloadingId === r.id ? '...' : '下载' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- 加载更多 -->
            <div v-if="hasMore" class="load-more">
              <button class="btn btn-outline" :disabled="loading" @click="loadResources(false)">
                {{ loading ? '加载中...' : '加载更多' }}
              </button>
            </div>
          </main>
        </div>

        <!-- 预览弹窗 -->
        <ResourcePreview
          :show="previewVisible"
          :resource="previewResource"
          @close="previewVisible = false"
          @download="onPreviewDownload"
        />

        <!-- 贡献资源弹窗 -->
        <div v-if="showContribute" class="modal-overlay" @click.self="showContribute = false">
          <div class="modal-card">
            <h3>贡献资源</h3>
            <p class="modal-hint">提交资源后需管理员审核，通过后将展示在知识库中</p>
            <form @submit.prevent="handleContribute">
              <label>
                <span>资源标题 <em>*</em></span>
                <input v-model="contributeForm.title" type="text" placeholder="输入资源标题" required />
              </label>
              <label>
                <span>分类 <em>*</em></span>
                <select v-model="contributeForm.category" required>
                  <option value="" disabled>选择分类</option>
                  <option v-for="(label, key) in categories" :key="key" :value="key">{{ label }}</option>
                </select>
              </label>
              <label>
                <span>描述</span>
                <textarea v-model="contributeForm.description" rows="3" placeholder="简要描述资源内容"></textarea>
              </label>
              <label>
                <span>标签</span>
                <input v-model="contributeForm.tags" type="text" placeholder="多个标签用逗号分隔" />
              </label>
              <label>
                <span>文件 <em>*</em></span>
                <input type="file" @change="contributeForm.file = $event.target.files[0]" required />
              </label>
              <p v-if="contributeError" class="form-error">{{ contributeError }}</p>
              <p v-if="contributeSuccess" class="form-success">{{ contributeSuccess }}</p>
              <div class="modal-actions">
                <button type="button" class="btn btn-outline" @click="showContribute = false">取消</button>
                <button type="submit" class="btn btn-primary" :disabled="contributing">{{ contributing ? '提交中...' : '提交' }}</button>
              </div>
            </form>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useScrollReveal } from '@/composables/useScrollReveal'
import { isUserLoggedIn, getResources, downloadResource, getResourceTags, getResourceCategories, contributeResource } from '@/services/api'
import PaperCard from '@/components/ui/PaperCard.vue'
import ResourcePreview from '@/components/ui/ResourcePreview.vue'

useScrollReveal()

const isLoggedIn = ref(isUserLoggedIn())
const loading = ref(false)
const resources = ref([])
const total = ref(0)
const activeCategory = ref('')
const activeTag = ref('')
const searchQuery = ref('')
const currentPage = ref(1)
const hasMore = ref(false)
const viewMode = ref('card')
const downloadingId = ref(null)
const tagList = ref([])
const previewVisible = ref(false)
const previewResource = ref(null)

const showContribute = ref(false)
const contributing = ref(false)
const contributeError = ref('')
const contributeSuccess = ref('')
const contributeForm = ref({ title: '', category: '', description: '', tags: '', file: null })

const categories = ref({})

const catCounts = reactive({})

const categoryOptions = [
  { key: '', label: '全部' },
  { key: 'literature', label: '文献' },
  { key: 'tutorial', label: '教程' },
  { key: 'tool', label: '工具' },
  { key: 'template', label: '表格模板' },
  { key: 'learning', label: '学习资料' },
]

const categoryLabels = {
  literature: '文献',
  tutorial: '教程',
  tool: '工具',
  template: '表格模板',
  learning: '学习资料',
}

function updateCategoryOptions(cats) {
  if (!cats || typeof cats !== 'object') return
  categories.value = cats
  categoryOptions.splice(0, categoryOptions.length, { key: '', label: '全部' })
  Object.entries(cats).forEach(([key, label]) => {
    categoryOptions.push({ key, label })
    categoryLabels[key] = label
  })
}

onMounted(async () => {
  if (isLoggedIn.value) {
    const [cats] = await Promise.all([getResourceCategories().catch(() => null), loadResources(true), loadTags()])
    if (cats?.categories) updateCategoryOptions(cats.categories)
  }
})

async function loadResources(reset = false) {
  if (reset) {
    currentPage.value = 1
    resources.value = []
  }

  loading.value = true
  try {
    const data = await getResources({
      category: activeCategory.value,
      search: searchQuery.value,
      tag: activeTag.value,
      page: currentPage.value,
      per_page: 12,
    })
    if (reset) {
      resources.value = data.items
    } else {
      resources.value.push(...data.items)
    }
    total.value = data.total
    hasMore.value = currentPage.value < data.pages
    currentPage.value++

    // Update category counts
    const allData = await getResources({ per_page: 1 })
    catCounts[''] = allData.total
  } catch (e) {
    if (e.status === 401 || e.status === 422) isLoggedIn.value = false
  } finally {
    loading.value = false
  }
}

async function loadTags() {
  try {
    const data = await getResourceTags()
    tagList.value = data.tags || []
  } catch { /* ignore */ }
}

function openPreview(r) {
  previewResource.value = r
  previewVisible.value = true
}

function onPreviewDownload(result) {
  const r = resources.value.find(x => x.id === previewResource.value?.id)
  if (r) r.download_count = result.download_count
}

async function handleDownload(r) {
  downloadingId.value = r.id
  try {
    const result = await downloadResource(r.id)
    r.download_count = result.download_count
    const a = document.createElement('a')
    a.href = result.file_url
    a.download = result.file_name
    a.target = '_blank'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  } catch (e) {
    alert('下载失败: ' + (e.message || '未知错误'))
  } finally {
    downloadingId.value = null
  }
}

function formatFileSize(bytes) {
  if (!bytes) return ''
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

async function handleContribute() {
  if (!contributeForm.value.file) return
  contributing.value = true
  contributeError.value = ''
  contributeSuccess.value = ''
  try {
    const fd = new FormData()
    fd.append('title', contributeForm.value.title)
    fd.append('category', contributeForm.value.category)
    fd.append('description', contributeForm.value.description)
    fd.append('tags', contributeForm.value.tags)
    fd.append('file', contributeForm.value.file)
    const result = await contributeResource(fd)
    contributeSuccess.value = result.message || '提交成功'
    contributeForm.value = { title: '', category: '', description: '', tags: '', file: null }
  } catch (e) {
    contributeError.value = e.message || '提交失败'
  } finally {
    contributing.value = false
  }
}
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero { text-align: center; margin-bottom: 32px; padding: 40px 32px; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.page-hero::after { content: ''; position: absolute; inset: 0; background-image: radial-gradient(circle at 15% 85%, rgba(192, 96, 64, 0.04) 0%, transparent 40%), radial-gradient(circle at 85% 15%, rgba(212, 146, 10, 0.04) 0%, transparent 40%); pointer-events: none; }
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(1.8rem, 4vw, 2.6rem); margin-bottom: 10px; }
.page-subtitle { font-size: 15px; color: var(--text-secondary); margin: 0 0 16px; }
.hero-btn { margin-top: 4px; }

/* Login prompt */
.login-prompt { max-width: 480px; margin: 0 auto; }
.prompt-content { text-align: center; padding: 40px 20px; color: var(--text-muted); }
.prompt-content svg { margin-bottom: 16px; }
.prompt-content h3 { font-family: var(--font-heading); font-size: 18px; color: var(--text-primary); margin: 0 0 8px; }
.prompt-content p { font-size: 14px; margin: 0 0 24px; }

/* Knowledge base layout */
.kb-layout { display: grid; grid-template-columns: 240px 1fr; gap: 28px; align-items: start; }

/* Sidebar */
.kb-sidebar { position: sticky; top: 100px; }
.sidebar-section { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 20px; margin-bottom: 16px; }
.sidebar-title { font-family: var(--font-heading); font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); margin: 0 0 14px; }
.category-nav { display: flex; flex-direction: column; gap: 2px; }
.cat-nav-item { display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; border: none; background: none; border-radius: 8px; font-size: 13px; color: var(--text-secondary); cursor: pointer; transition: all 0.15s; text-align: left; }
.cat-nav-item:hover { background: var(--bg-soft); color: var(--text-primary); }
.cat-nav-item.active { background: rgba(192, 96, 64, 0.08); color: var(--warm-terracotta); font-weight: 600; }
.cat-count { font-size: 11px; background: var(--bg-soft); padding: 1px 8px; border-radius: 999px; color: var(--text-muted); }
.cat-nav-item.active .cat-count { background: rgba(192, 96, 64, 0.12); color: var(--warm-terracotta); }

.tag-cloud { display: flex; flex-wrap: wrap; gap: 6px; }
.tag-pill { padding: 4px 10px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 11px; cursor: pointer; transition: all 0.15s; color: var(--text-secondary); }
.tag-pill:hover { border-color: var(--warm-terracotta); color: var(--warm-terracotta); }
.tag-pill.active { background: var(--warm-terracotta); color: white; border-color: transparent; }

/* Main content */
.kb-main { min-width: 0; }
.kb-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; gap: 16px; flex-wrap: wrap; }
.search-box { display: flex; align-items: center; gap: 8px; padding: 8px 14px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; flex: 1; min-width: 200px; max-width: 400px; }
.search-box svg { color: var(--text-muted); flex-shrink: 0; }
.search-box input { border: none; outline: none; font-size: 13px; background: transparent; color: var(--text-primary); flex: 1; min-width: 0; }
.clear-btn { background: none; border: none; cursor: pointer; color: var(--text-muted); padding: 2px; display: flex; }

.toolbar-right { display: flex; align-items: center; gap: 10px; }
.result-count { font-size: 12px; color: var(--text-muted); }
.view-toggle { width: 32px; height: 32px; border: 1px solid var(--glass-border); background: white; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: var(--text-muted); transition: all 0.15s; }
.view-toggle:hover { border-color: var(--warm-terracotta); color: var(--warm-terracotta); }
.view-toggle.active { background: rgba(192, 96, 64, 0.08); border-color: var(--warm-terracotta); color: var(--warm-terracotta); }

.active-filter { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; font-size: 13px; color: var(--text-secondary); }
.filter-tag { display: inline-flex; align-items: center; gap: 6px; padding: 3px 12px; background: var(--warm-terracotta); color: white; border-radius: 999px; font-size: 12px; }
.filter-tag button { background: none; border: none; color: white; cursor: pointer; font-size: 14px; line-height: 1; }

/* States */
.kb-loading, .kb-empty { text-align: center; padding: 60px 20px; color: var(--text-muted); font-size: 14px; }
.kb-empty svg { margin-bottom: 12px; }

/* Card view */
.resources-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.resource-card { display: flex; flex-direction: column; }
.rc-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.rc-category { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
.cat-literature { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.cat-tutorial { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.cat-tool { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.cat-template { background: rgba(168, 85, 247, 0.1); color: #a855f7; }
.cat-learning { background: rgba(236, 72, 153, 0.1); color: #ec4899; }
.rc-type { font-size: 10px; font-weight: 700; color: var(--text-muted); background: var(--bg-soft); padding: 2px 6px; border-radius: 4px; letter-spacing: 0.03em; }

.rc-title { font-family: var(--font-heading); font-size: 15px; font-weight: 600; margin: 0 0 6px; color: var(--text-primary); cursor: pointer; transition: color 0.2s; }
.rc-title:hover { color: var(--warm-terracotta); }
.rc-desc { font-size: 12px; color: var(--text-secondary); margin: 0 0 10px; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; flex: 1; }

.rc-tags { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 10px; }
.rc-tag { font-size: 10px; padding: 2px 8px; background: var(--bg-soft); color: var(--text-muted); border-radius: 999px; cursor: pointer; transition: all 0.15s; }
.rc-tag:hover { background: rgba(192, 96, 64, 0.08); color: var(--warm-terracotta); }

.rc-meta { display: flex; gap: 12px; margin-bottom: 12px; }
.meta-item { display: flex; align-items: center; gap: 4px; font-size: 11px; color: var(--text-muted); }

.rc-actions { display: flex; gap: 8px; justify-content: flex-end; }
.btn-sm { padding: 5px 16px; font-size: 12px; }

/* List view */
.resources-list { display: flex; flex-direction: column; gap: 8px; }
.list-item { display: flex; align-items: center; gap: 14px; padding: 14px 18px; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); cursor: pointer; transition: all 0.2s; }
.list-item:hover { border-color: var(--warm-terracotta); box-shadow: var(--shadow-sm); }

.li-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; flex-shrink: 0; background: var(--bg-soft); color: var(--text-muted); }
.list-item .cat-literature .li-icon, .li-icon.cat-literature { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.li-icon.cat-tutorial { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.li-icon.cat-tool { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.li-icon.cat-template { background: rgba(168, 85, 247, 0.1); color: #a855f7; }
.li-icon.cat-learning { background: rgba(236, 72, 153, 0.1); color: #ec4899; }

.li-body { flex: 1; min-width: 0; }
.li-title { font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin-bottom: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.li-meta { display: flex; flex-wrap: wrap; gap: 10px; font-size: 11px; color: var(--text-muted); }
.li-cat { font-weight: 600; color: var(--text-secondary); }

.li-tags { display: flex; gap: 4px; flex-shrink: 0; }
.li-actions { display: flex; gap: 6px; flex-shrink: 0; }

/* Load more */
.load-more { text-align: center; margin-top: 28px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 20px; backdrop-filter: blur(4px); }
.modal-card { background: #fff; border-radius: var(--radius-xl); padding: 32px; width: 100%; max-width: 480px; box-shadow: var(--shadow-lg); max-height: 90vh; overflow-y: auto; }
.modal-card h3 { font-family: var(--font-heading); font-size: 18px; margin: 0 0 4px; }
.modal-hint { font-size: 13px; color: var(--text-muted); margin: 0 0 20px; }
.modal-card label { display: block; margin-bottom: 14px; }
.modal-card label span { display: block; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 5px; }
.modal-card label span em { color: var(--warm-terracotta); font-style: normal; }
.modal-card input, .modal-card select, .modal-card textarea { width: 100%; padding: 9px 12px; border: 1px solid var(--glass-border); border-radius: var(--radius-md); font-size: 13px; background: white; color: var(--text-primary); transition: border-color 0.2s; font-family: inherit; box-sizing: border-box; }
.modal-card input:focus, .modal-card select:focus, .modal-card textarea:focus { outline: none; border-color: var(--warm-terracotta); box-shadow: 0 0 0 3px rgba(192, 96, 64, 0.1); }
.modal-card textarea { resize: vertical; }
.form-error { color: #e05050; font-size: 12px; margin: 4px 0; }
.form-success { color: #2e7d32; font-size: 12px; margin: 4px 0; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; }

@media (max-width: 768px) {
  .kb-layout { grid-template-columns: 1fr; }
  .kb-sidebar { position: static; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .sidebar-section { padding: 14px; margin-bottom: 0; }
  .search-box { max-width: none; }
  .resources-grid { grid-template-columns: 1fr; }
  .list-item { flex-wrap: wrap; }
  .li-tags { display: none; }
}

@media (max-width: 480px) {
  .kb-sidebar { grid-template-columns: 1fr; }
}
</style>
