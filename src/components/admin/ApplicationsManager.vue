<template>
  <div class="apps-manager">
    <div class="apps-toolbar">
      <div class="status-tabs">
        <button v-for="s in statuses" :key="s.key" class="filter-tab" :class="{ active: activeStatus === s.key }" @click="activeStatus = s.key">
          {{ s.label }} <span v-if="counts[s.key]" class="tab-count">{{ counts[s.key] }}</span>
        </button>
      </div>
      <button class="btn btn-outline btn-sm" @click="loadApps">刷新</button>
    </div>

    <div v-if="loading" class="apps-loading">加载中...</div>
    <div v-else-if="filteredApps.length === 0" class="apps-empty">暂无申请</div>

    <div v-else class="apps-list">
      <div v-for="app in filteredApps" :key="app.id" class="app-card" :class="{ expanded: expandedId === app.id }">
        <div class="app-header" @click="expandedId = expandedId === app.id ? null : app.id">
          <div class="app-info">
            <strong class="app-name">{{ app.name }}</strong>
            <span class="app-group tag tag-accent">{{ app.group_name }}</span>
            <span class="app-status" :class="'status-' + app.status">{{ statusLabels[app.status] }}</span>
          </div>
          <span class="app-date">{{ formatDate(app.created_at) }}</span>
        </div>

        <div v-if="expandedId === app.id" class="app-detail">
          <div class="detail-grid">
            <div class="detail-item"><span>学号</span><strong>{{ app.student_id }}</strong></div>
            <div class="detail-item"><span>年级专业</span><strong>{{ app.grade_major }}</strong></div>
            <div class="detail-item"><span>手机</span><strong>{{ app.phone }}</strong></div>
            <div class="detail-item"><span>邮箱</span><strong>{{ app.email }}</strong></div>
            <div class="detail-item" v-if="app.github_url"><span>GitHub</span><strong>{{ app.github_url }}</strong></div>
            <div class="detail-item" v-if="app.portfolio_url"><span>作品集</span><strong>{{ app.portfolio_url }}</strong></div>
          </div>
          <div class="detail-block" v-if="app.experience">
            <span>相关经验</span>
            <p>{{ app.experience }}</p>
          </div>
          <div class="detail-block">
            <span>申请动机</span>
            <p>{{ app.motivation }}</p>
          </div>

          <div class="detail-block">
            <span>管理员备注</span>
            <textarea v-model="editingNote" rows="2" placeholder="添加备注..."></textarea>
          </div>

          <div class="app-actions">
            <button v-if="app.status === 'pending'" class="btn btn-outline btn-sm" @click="updateStatus(app.id, 'reviewing')">标记审核中</button>
            <button v-if="app.status !== 'processed'" class="btn btn-primary btn-sm" @click="updateStatus(app.id, 'processed')">通过</button>
            <button v-if="app.status !== 'archived'" class="btn btn-outline btn-sm" @click="updateStatus(app.id, 'archived')">归档</button>
            <button class="btn btn-outline btn-sm btn-danger" @click="deleteApp(app.id)">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getApplications, updateApplication, deleteApplication } from '@/services/api'

const apps = ref([])
const loading = ref(false)
const activeStatus = ref('all')
const expandedId = ref(null)
const editingNote = ref('')

const statuses = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待处理' },
  { key: 'reviewing', label: '审核中' },
  { key: 'processed', label: '已处理' },
  { key: 'archived', label: '已归档' },
]

const statusLabels = { pending: '待处理', reviewing: '审核中', processed: '已处理', archived: '已归档' }

const counts = computed(() => {
  const c = { all: apps.value.length }
  apps.value.forEach((a) => { c[a.status] = (c[a.status] || 0) + 1 })
  return c
})

const filteredApps = computed(() => {
  if (activeStatus.value === 'all') return apps.value
  return apps.value.filter((a) => a.status === activeStatus.value)
})

onMounted(loadApps)

async function loadApps() {
  loading.value = true
  try {
    apps.value = await getApplications()
  } catch (e) {
    console.error('加载申请失败', e)
  } finally {
    loading.value = false
  }
}

async function updateStatus(id, status) {
  try {
    const payload = { status }
    if (editingNote.value) payload.admin_note = editingNote.value
    await updateApplication(id, payload)
    await loadApps()
    editingNote.value = ''
  } catch (e) {
    alert('更新失败: ' + (e.message || '未知错误'))
  }
}

async function deleteApp(id) {
  if (!confirm('确定删除此申请？')) return
  try {
    await deleteApplication(id)
    await loadApps()
  } catch (e) {
    alert('删除失败: ' + (e.message || '未知错误'))
  }
}

function formatDate(iso) {
  if (!iso) return ''
  return iso.slice(0, 10)
}
</script>

<style scoped>
.apps-manager { }
.apps-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.status-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-tab { padding: 6px 16px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 12px; cursor: pointer; transition: all 0.15s; }
.filter-tab:hover { border-color: var(--glass-border-hover); }
.filter-tab.active { background: var(--warm-terracotta); color: white; border-color: transparent; }
.tab-count { font-weight: 700; margin-left: 4px; }

.apps-loading, .apps-empty { text-align: center; padding: 48px; color: var(--text-muted); font-size: 14px; }

.apps-list { display: flex; flex-direction: column; gap: 12px; }
.app-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); overflow: hidden; transition: box-shadow 0.2s; }
.app-card.expanded { box-shadow: var(--shadow-md); }
.app-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; cursor: pointer; }
.app-header:hover { background: var(--bg-soft); }
.app-info { display: flex; align-items: center; gap: 10px; }
.app-name { font-family: var(--font-heading); font-size: 14px; }
.app-group { font-size: 11px; }
.app-status { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
.status-pending { background: rgba(212, 146, 10, 0.1); color: var(--warm-amber); }
.status-reviewing { background: rgba(192, 96, 64, 0.1); color: var(--warm-terracotta); }
.status-processed { background: rgba(122, 154, 106, 0.1); color: var(--warm-sage); }
.status-archived { background: var(--surface); color: var(--text-muted); }
.app-date { font-size: 12px; color: var(--text-muted); }

.app-detail { padding: 0 20px 20px; border-top: 1px solid var(--glass-border); }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }
.detail-item span { display: block; font-size: 11px; color: var(--text-muted); }
.detail-item strong { font-size: 13px; }
.detail-block { margin-top: 16px; }
.detail-block span { display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 4px; }
.detail-block p { font-size: 13px; color: var(--text-primary); line-height: 1.7; margin: 0; }
.detail-block textarea { width: 100%; padding: 8px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; resize: vertical; }
.detail-block textarea:focus { outline: none; border-color: var(--warm-terracotta); }

.app-actions { display: flex; gap: 8px; margin-top: 16px; }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-danger { color: #e05050; border-color: #e05050; }
.btn-danger:hover { background: #e05050; color: white; }

@media (max-width: 768px) {
  .apps-toolbar { flex-direction: column; align-items: stretch; }
  .status-tabs { gap: 6px; }
  .filter-tab { padding: 5px 12px; font-size: 11px; }
  .app-header { padding: 12px 14px; flex-direction: column; align-items: flex-start; gap: 6px; }
  .app-info { flex-wrap: wrap; gap: 6px; }
  .app-detail { padding: 0 14px 14px; }
  .detail-grid { grid-template-columns: 1fr; }
  .app-actions { flex-wrap: wrap; }
}
</style>
