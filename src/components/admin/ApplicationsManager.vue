<template>
  <div class="apps-manager">
    <div class="apps-toolbar">
      <div class="status-tabs">
        <button v-for="s in statuses" :key="s.key" class="filter-tab" :class="{ active: activeStatus === s.key }" @click="activeStatus = s.key">
          {{ s.label }} <span v-if="counts[s.key]" class="tab-count">{{ counts[s.key] }}</span>
        </button>
      </div>
      <div class="toolbar-right">
        <select v-model="activeSession" class="session-select" @change="loadApps">
          <option value="">全部届数</option>
          <option v-for="s in sessions" :key="s" :value="s">{{ s }}</option>
        </select>
        <button class="btn btn-outline btn-sm" @click="loadApps">刷新</button>
      </div>
    </div>

    <!-- 批量操作栏 -->
    <div v-if="selectedIds.size > 0" class="batch-bar">
      <span class="batch-info">已选 <strong>{{ selectedIds.size }}</strong> 项</span>
      <button class="btn btn-primary btn-sm" @click="openBatchDialog('approved')">批量通过</button>
      <button class="btn btn-outline btn-sm btn-reject" @click="confirmBatchReject">批量拒绝</button>
      <button class="btn btn-outline btn-sm" @click="batchUpdateStatus('archived')">批量归档</button>
      <button class="btn btn-outline btn-sm" @click="selectedIds.clear()">取消选择</button>
    </div>

    <div v-if="loading" class="apps-loading">加载中...</div>
    <div v-else-if="filteredApps.length === 0" class="apps-empty">暂无申请</div>

    <div v-else class="apps-list">
      <div v-for="app in filteredApps" :key="app.id" class="app-card" :class="{ expanded: expandedId === app.id, selected: selectedIds.has(app.id) }">
        <div class="app-header" @click="expandedId = expandedId === app.id ? null : app.id">
          <div class="app-info">
            <input type="checkbox" :checked="selectedIds.has(app.id)" class="app-check" @click.stop @change="toggleSelect(app.id)" />
            <strong class="app-name">{{ app.name }}</strong>
            <span v-if="app.session" class="app-group tag tag-accent">{{ app.session }}</span>
            <span class="app-group tag tag-accent">{{ app.group_name }}</span>
            <span class="app-status" :class="'status-' + app.status">{{ statusLabels[app.status] || app.status }}</span>
          </div>
          <span class="app-date">{{ formatDate(app.created_at) }}</span>
        </div>

        <div v-if="expandedId === app.id" class="app-detail">
          <div class="detail-grid">
            <div class="detail-item"><span>学号</span><strong>{{ app.student_id }}</strong></div>
            <div class="detail-item"><span>年级专业</span><strong>{{ app.grade_major }}</strong></div>
            <div class="detail-item"><span>手机</span><strong>{{ app.phone }}</strong></div>
            <div class="detail-item"><span>邮箱</span><strong>{{ app.email }}</strong></div>
            <div class="detail-item" v-if="app.session"><span>届数</span><strong>{{ app.session }}</strong></div>
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

          <div class="detail-block" v-if="app.last_email_type">
            <span>邮件状态</span>
            <p>
              {{ app.last_email_type === 'result_approved' ? '通过通知' : app.last_email_type === 'result_rejected' ? '拒绝通知' : app.last_email_type }}
              <span v-if="app.last_email_sent" class="email-ok">已发送</span>
              <span v-else class="email-fail">发送失败: {{ app.last_email_error }}</span>
              <span v-if="app.last_email_sent_at" class="email-time">{{ formatDate(app.last_email_sent_at) }}</span>
            </p>
          </div>

          <div class="detail-block">
            <span>管理员备注</span>
            <textarea v-model="editingNote" rows="2" placeholder="添加备注..."></textarea>
          </div>

          <div class="app-actions">
            <button v-if="app.status === 'pending'" class="btn btn-outline btn-sm" @click="updateStatus(app.id, 'reviewing')">标记审核中</button>
            <button v-if="app.status === 'pending' || app.status === 'reviewing'" class="btn btn-primary btn-sm" @click="openSingleDialog(app)">通过</button>
            <button v-if="app.status === 'pending' || app.status === 'reviewing'" class="btn btn-outline btn-sm btn-reject" @click="updateStatus(app.id, 'rejected')">拒绝</button>
            <button v-if="app.status !== 'archived'" class="btn btn-outline btn-sm" @click="updateStatus(app.id, 'archived')">归档</button>
            <button class="btn btn-outline btn-sm btn-danger" @click="deleteApp(app.id)">删除</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 通过弹窗 -->
    <div v-if="showDialog" class="dialog-overlay" @click.self="showDialog = false">
      <div class="dialog-card">
        <h3>通过申请{{ dialogIds.length > 1 ? '（批量）' : '' }}</h3>
        <p class="dialog-hint">将{{ dialogIds.length > 1 ? '批量' : '' }}通过 <strong>{{ dialogIds.length }}</strong> 条申请{{ dialogIds.length > 1 ? '' : '：' + dialogAppName }}，并发送通知邮件。</p>
        <div class="dialog-fields">
          <label class="field">
            <span>考核群链接</span>
            <input v-model="dialogGroupLink" type="url" placeholder="https://..." />
          </label>
          <label class="field">
            <span>群二维码图片</span>
            <ImageUploadField :modelValue="dialogQrCode" @update:modelValue="dialogQrCode = $event" />
          </label>
        </div>
        <div class="dialog-actions">
          <button class="btn btn-outline btn-sm" @click="showDialog = false">取消</button>
          <button class="btn btn-primary btn-sm" @click="confirmApprove">确认通过并发送邮件</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getApplications, updateApplication, batchUpdateApplications, deleteApplication } from '@/services/api'
import ImageUploadField from './ImageUploadField.vue'

const apps = ref([])
const loading = ref(false)
const activeStatus = ref('all')
const activeSession = ref('')
const expandedId = ref(null)
const editingNote = ref('')
const selectedIds = ref(new Set())

// 通过弹窗
const showDialog = ref(false)
const dialogIds = ref([])
const dialogAppName = ref('')
const dialogGroupLink = ref('')
const dialogQrCode = ref('')

const statuses = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待处理' },
  { key: 'reviewing', label: '审核中' },
  { key: 'approved', label: '已通过' },
  { key: 'rejected', label: '已拒绝' },
  { key: 'archived', label: '已归档' },
]

const statusLabels = {
  pending: '待处理',
  reviewing: '审核中',
  approved: '已通过',
  rejected: '已拒绝',
  archived: '已归档',
}

const counts = computed(() => {
  const c = { all: apps.value.length }
  apps.value.forEach((a) => { c[a.status] = (c[a.status] || 0) + 1 })
  return c
})

const sessions = computed(() => {
  const set = new Set()
  apps.value.forEach((a) => { if (a.session) set.add(a.session) })
  return [...set].sort()
})

const filteredApps = computed(() => {
  let result = apps.value
  if (activeStatus.value !== 'all') result = result.filter((a) => a.status === activeStatus.value)
  if (activeSession.value) result = result.filter((a) => a.session === activeSession.value)
  return result
})

onMounted(loadApps)

function toggleSelect(id) {
  const next = new Set(selectedIds.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  selectedIds.value = next
}

function openSingleDialog(app) {
  dialogIds.value = [app.id]
  dialogAppName.value = app.name
  dialogGroupLink.value = ''
  dialogQrCode.value = ''
  showDialog.value = true
}

function openBatchDialog(status) {
  dialogIds.value = [...selectedIds.value]
  dialogAppName.value = ''
  dialogGroupLink.value = ''
  dialogQrCode.value = ''
  showDialog.value = true
}

async function confirmApprove() {
  const ids = dialogIds.value
  try {
    if (ids.length === 1) {
      const payload = { status: 'approved' }
      if (editingNote.value) payload.admin_note = editingNote.value
      if (dialogGroupLink.value) payload.group_link = dialogGroupLink.value
      if (dialogQrCode.value) payload.qr_code_url = dialogQrCode.value
      await updateApplication(ids[0], payload)
    } else {
      const payload = { ids, status: 'approved' }
      if (editingNote.value) payload.admin_note = editingNote.value
      if (dialogGroupLink.value) payload.group_link = dialogGroupLink.value
      if (dialogQrCode.value) payload.qr_code_url = dialogQrCode.value
      await batchUpdateApplications(payload)
    }
    showDialog.value = false
    selectedIds.value = new Set()
    editingNote.value = ''
    await loadApps()
  } catch (e) {
    alert('操作失败: ' + (e.message || '未知错误'))
  }
}

async function confirmBatchReject() {
  if (!confirm(`确定拒绝选中的 ${selectedIds.value.size} 条申请吗？`)) return
  await batchUpdateStatus('rejected')
}

async function loadApps() {
  loading.value = true
  try {
    apps.value = await getApplications(activeStatus.value, activeSession.value)
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

async function batchUpdateStatus(status) {
  const ids = [...selectedIds.value]
  if (ids.length === 0) return
  try {
    const payload = { ids, status }
    if (editingNote.value) payload.admin_note = editingNote.value
    await batchUpdateApplications(payload)
    selectedIds.value = new Set()
    editingNote.value = ''
    await loadApps()
  } catch (e) {
    alert('批量更新失败: ' + (e.message || '未知错误'))
  }
}

async function deleteApp(id) {
  if (!confirm('确定删除此申请？')) return
  try {
    await deleteApplication(id)
    selectedIds.value = new Set([...selectedIds.value].filter(x => x !== id))
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
.toolbar-right { display: flex; align-items: center; gap: 8px; }
.session-select { padding: 6px 12px; border: 1px solid var(--glass-border); border-radius: 999px; font-size: 12px; background: white; color: var(--text-primary); cursor: pointer; }
.session-select:focus { outline: none; border-color: var(--warm-terracotta); }
.status-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-tab { padding: 6px 16px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 12px; cursor: pointer; transition: all 0.15s; }
.filter-tab:hover { border-color: var(--glass-border-hover); }
.filter-tab.active { background: var(--warm-terracotta); color: white; border-color: transparent; }
.tab-count { font-weight: 700; margin-left: 4px; }

/* 批量操作栏 */
.batch-bar { display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: rgba(192, 96, 64, 0.06); border: 1px solid rgba(192, 96, 64, 0.2); border-radius: var(--radius-md); margin-bottom: 16px; }
.batch-info { font-size: 13px; color: var(--text-secondary); }
.batch-info strong { color: var(--warm-terracotta); }

.apps-loading, .apps-empty { text-align: center; padding: 48px; color: var(--text-muted); font-size: 14px; }

.apps-list { display: flex; flex-direction: column; gap: 12px; }
.app-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); overflow: hidden; transition: box-shadow 0.2s; }
.app-card.expanded { box-shadow: var(--shadow-md); }
.app-card.selected { border-color: var(--warm-terracotta); background: rgba(192, 96, 64, 0.02); }
.app-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; cursor: pointer; gap: 12px; }
.app-header:hover { background: var(--bg-soft); }
.app-info { display: flex; align-items: center; gap: 10px; flex: 1; min-width: 0; }
.app-check { width: 16px; height: 16px; accent-color: var(--warm-terracotta); cursor: pointer; flex-shrink: 0; }
.app-name { font-family: var(--font-heading); font-size: 14px; white-space: nowrap; }
.app-group { font-size: 11px; }
.app-status { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; white-space: nowrap; }
.status-pending { background: rgba(212, 146, 10, 0.1); color: var(--warm-amber); }
.status-reviewing { background: rgba(192, 96, 64, 0.1); color: var(--warm-terracotta); }
.status-approved { background: rgba(46, 125, 50, 0.1); color: #2e7d32; }
.status-rejected { background: rgba(198, 40, 40, 0.1); color: #c62828; }
.status-archived { background: var(--surface); color: var(--text-muted); }
.app-date { font-size: 12px; color: var(--text-muted); white-space: nowrap; }

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
.btn-reject { color: #c62828; border-color: #c62828; }
.btn-reject:hover { background: #c62828; color: white; }
.email-ok { color: #2e7d32; font-size: 11px; margin-left: 6px; }
.email-fail { color: #c62828; font-size: 11px; margin-left: 6px; }
.email-time { color: var(--text-muted); font-size: 11px; margin-left: 6px; }

/* 通过弹窗 */
.dialog-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 200; }
.dialog-card { background: white; border-radius: var(--radius-lg); padding: 28px; width: 100%; max-width: 480px; box-shadow: var(--shadow-xl); }
.dialog-card h3 { font-family: var(--font-heading); font-size: 16px; margin: 0 0 8px; }
.dialog-hint { font-size: 13px; color: var(--text-secondary); margin: 0 0 20px; }
.dialog-fields { display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; }
.dialog-fields .field span { display: block; font-size: 12px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
.dialog-fields .field input { width: 100%; padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 13px; background: white; color: var(--text-primary); }
.dialog-fields .field input:focus { outline: none; border-color: var(--warm-terracotta); }
.dialog-actions { display: flex; gap: 10px; justify-content: flex-end; }

@media (max-width: 768px) {
  .apps-toolbar { flex-direction: column; align-items: stretch; }
  .status-tabs { gap: 6px; }
  .filter-tab { padding: 5px 12px; font-size: 11px; }
  .batch-bar { flex-wrap: wrap; }
  .app-header { padding: 12px 14px; flex-direction: column; align-items: flex-start; gap: 6px; }
  .app-info { flex-wrap: wrap; gap: 6px; }
  .app-detail { padding: 0 14px 14px; }
  .detail-grid { grid-template-columns: 1fr; }
  .app-actions { flex-wrap: wrap; }
  .dialog-card { margin: 16px; padding: 20px; }
}
</style>
