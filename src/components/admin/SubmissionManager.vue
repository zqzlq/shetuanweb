<template>
  <div class="submission-manager">
    <div class="apps-toolbar">
      <div class="status-tabs">
        <button v-for="s in statuses" :key="s.key" class="filter-tab" :class="{ active: activeStatus === s.key }" @click="activeStatus = s.key">{{ s.label }}<span v-if="counts[s.key]" class="tab-count">{{ counts[s.key] }}</span></button>
      </div>
      <button class="btn btn-outline btn-sm" @click="loadSubs">刷新</button>
    </div>

    <div v-if="loading" class="apps-loading">加载中...</div>
    <div v-else-if="filtered.length === 0" class="apps-empty">暂无提交</div>

    <div v-else class="apps-list">
      <div v-for="s in filtered" :key="s.id" class="app-card">
        <div class="app-header">
          <div class="app-info">
            <strong class="app-name">{{ s.title }}</strong>
            <span class="app-group tag tag-accent">{{ s.type === 'award' ? '奖状' : '作品' }}</span>
            <span class="app-status" :class="'status-' + s.status">{{ statusLabel(s.status) }}</span>
          </div>
          <span>{{ s.user_name }}</span>
        </div>
        <div class="app-detail">
          <div class="detail-block" v-if="s.description">
            <span>描述</span>
            <p>{{ s.description }}</p>
          </div>
          <div class="detail-block" v-if="s.image">
            <span>图片</span>
            <img :src="s.image" class="submission-img" />
          </div>
          <div class="app-actions">
            <button v-if="s.status === 'pending'" class="btn btn-primary btn-sm" @click="updateSub(s.id, 'approved')">通过（自动同步）</button>
            <button v-if="s.status === 'pending'" class="btn btn-outline btn-sm btn-reject" @click="updateSub(s.id, 'rejected')">拒绝</button>
            <button v-if="s.status === 'approved'" class="btn btn-outline btn-sm" @click="syncToPage(s.id)">同步到页面</button>
            <button v-if="s.status !== 'pending'" class="btn btn-outline btn-sm" @click="updateSub(s.id, 'pending')">重新审核</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getSubmissions, updateSubmission, syncSubmissionToPage } from '@/services/api'

const subs = ref([])
const loading = ref(false)
const activeStatus = ref('pending')

const statuses = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待审核' },
  { key: 'approved', label: '已通过' },
  { key: 'rejected', label: '已拒绝' },
]

const counts = computed(() => {
  const c = { all: subs.value.length }
  subs.value.forEach(s => { c[s.status] = (c[s.status] || 0) + 1 })
  return c
})

const filtered = computed(() => {
  if (activeStatus.value === 'all') return subs.value
  return subs.value.filter(s => s.status === activeStatus.value)
})

onMounted(loadSubs)

async function loadSubs() {
  loading.value = true
  try { subs.value = await getSubmissions(activeStatus.value) }
  catch (e) { console.error('加载提交失败', e) }
  finally { loading.value = false }
}

async function updateSub(id, status) {
  try {
    await updateSubmission(id, { status })
    await loadSubs()
  } catch (e) { alert('操作失败: ' + e.message) }
}

async function syncToPage(id) {
  try {
    await syncSubmissionToPage(id)
    alert('已同步到对应页面')
  } catch (e) { alert('同步失败: ' + e.message) }
}

function statusLabel(s) {
  const map = { pending: '待审核', approved: '已通过', rejected: '已拒绝' }
  return map[s] || s
}
</script>

<style scoped>
.submission-manager { }
.apps-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.status-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-tab { padding: 6px 16px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 12px; cursor: pointer; }
.filter-tab.active { background: var(--warm-terracotta); color: white; border-color: transparent; }
.tab-count { font-weight: 700; margin-left: 4px; }
.apps-loading, .apps-empty { text-align: center; padding: 48px; color: var(--text-muted); font-size: 14px; }
.apps-list { display: flex; flex-direction: column; gap: 12px; }
.app-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); overflow: hidden; }
.app-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; }
.app-info { display: flex; align-items: center; gap: 10px; }
.app-name { font-family: var(--font-heading); font-size: 14px; }
.app-group { font-size: 11px; }
.app-status { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
.status-pending { background: rgba(212,146,10,0.1); color: var(--warm-amber); }
.status-approved { background: rgba(46,125,50,0.1); color: #2e7d32; }
.status-rejected { background: rgba(198,40,40,0.1); color: #c62828; }
.app-detail { padding: 0 20px 16px; border-top: 1px solid var(--glass-border); }
.detail-block { margin-top: 12px; }
.detail-block span { display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 4px; }
.detail-block p { font-size: 13px; color: var(--text-primary); line-height: 1.7; margin: 0; }
.submission-img { max-width: 240px; border-radius: 8px; border: 1px solid var(--glass-border); }
.app-actions { display: flex; gap: 8px; margin-top: 12px; }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-reject { color: #c62828; border-color: #c62828; }
.btn-reject:hover { background: #c62828; color: white; }
</style>
