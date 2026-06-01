<template>
  <div class="contact-manager">
    <div class="contact-toolbar">
      <div class="status-tabs">
        <button v-for="s in statuses" :key="s.key" class="filter-tab" :class="{ active: activeStatus === s.key }" @click="activeStatus = s.key">
          {{ s.label }} <span v-if="counts[s.key]" class="tab-count">{{ counts[s.key] }}</span>
        </button>
      </div>
      <button class="btn btn-outline btn-sm" @click="loadMessages">刷新</button>
    </div>

    <div v-if="loading" class="contact-loading">加载中...</div>
    <div v-else-if="filteredMessages.length === 0" class="contact-empty">暂无留言</div>

    <div v-else class="contact-list">
      <div v-for="msg in filteredMessages" :key="msg.id" class="msg-card" :class="{ expanded: expandedId === msg.id }">
        <div class="msg-header" @click="toggleExpand(msg)">
          <div class="msg-info">
            <strong class="msg-name">{{ msg.name }}</strong>
            <span class="msg-subject">{{ msg.subject }}</span>
            <span class="msg-status" :class="'status-' + msg.status">{{ statusLabels[msg.status] || msg.status }}</span>
          </div>
          <span class="msg-date">{{ formatDate(msg.created_at) }}</span>
        </div>

        <div v-if="expandedId === msg.id" class="msg-detail">
          <div class="detail-grid">
            <div class="detail-item"><span>邮箱</span><strong>{{ msg.email }}</strong></div>
            <div class="detail-item"><span>电话</span><strong>{{ msg.phone || '未填写' }}</strong></div>
            <div class="detail-item"><span>提交时间</span><strong>{{ formatDateTime(msg.created_at) }}</strong></div>
            <div class="detail-item" v-if="msg.read_at"><span>阅读时间</span><strong>{{ formatDateTime(msg.read_at) }}</strong></div>
          </div>
          <div class="detail-block">
            <span>留言内容</span>
            <p>{{ msg.message }}</p>
          </div>

          <div class="detail-block">
            <span>管理员备注</span>
            <textarea v-model="editingNote" rows="2" placeholder="添加备注..."></textarea>
          </div>

          <div class="msg-actions">
            <button v-if="msg.status === 'unread'" class="btn btn-outline btn-sm" @click="updateStatus(msg.id, 'read')">标记已读</button>
            <button v-if="msg.status === 'unread' || msg.status === 'read'" class="btn btn-primary btn-sm" @click="updateStatus(msg.id, 'replied')">标记已回复</button>
            <button v-if="msg.status !== 'archived'" class="btn btn-outline btn-sm" @click="updateStatus(msg.id, 'archived')">归档</button>
            <button class="btn btn-outline btn-sm btn-danger" @click="deleteMsg(msg.id)">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getContactMessages, updateContactMessage, deleteContactMessage } from '@/services/api'

const messages = ref([])
const loading = ref(false)
const activeStatus = ref('all')
const expandedId = ref(null)
const editingNote = ref('')

const statuses = [
  { key: 'all', label: '全部' },
  { key: 'unread', label: '未读' },
  { key: 'read', label: '已读' },
  { key: 'replied', label: '已回复' },
  { key: 'archived', label: '已归档' },
]

const statusLabels = {
  unread: '未读',
  read: '已读',
  replied: '已回复',
  archived: '已归档',
}

const counts = computed(() => {
  const c = { all: messages.value.length }
  messages.value.forEach((m) => { c[m.status] = (c[m.status] || 0) + 1 })
  return c
})

const filteredMessages = computed(() => {
  if (activeStatus.value === 'all') return messages.value
  return messages.value.filter((m) => m.status === activeStatus.value)
})

onMounted(loadMessages)

function toggleExpand(msg) {
  if (expandedId.value === msg.id) {
    expandedId.value = null
    editingNote.value = ''
  } else {
    expandedId.value = msg.id
    editingNote.value = msg.admin_note || ''
    if (msg.status === 'unread') {
      updateStatus(msg.id, 'read', true)
    }
  }
}

async function loadMessages() {
  loading.value = true
  try {
    messages.value = await getContactMessages(activeStatus.value)
  } catch (e) {
    console.error('加载留言失败', e)
  } finally {
    loading.value = false
  }
}

async function updateStatus(id, status, silent = false) {
  try {
    const payload = { status }
    if (editingNote.value) payload.admin_note = editingNote.value
    await updateContactMessage(id, payload)
    if (!silent) {
      await loadMessages()
      editingNote.value = ''
    } else {
      const idx = messages.value.findIndex(m => m.id === id)
      if (idx !== -1) messages.value[idx].status = status
    }
  } catch (e) {
    if (!silent) alert('更新失败: ' + (e.message || '未知错误'))
  }
}

async function deleteMsg(id) {
  if (!confirm('确定删除此留言？')) return
  try {
    await deleteContactMessage(id)
    expandedId.value = null
    await loadMessages()
  } catch (e) {
    alert('删除失败: ' + (e.message || '未知错误'))
  }
}

function formatDate(iso) {
  if (!iso) return ''
  return iso.slice(0, 10)
}

function formatDateTime(iso) {
  if (!iso) return ''
  return iso.replace('T', ' ').slice(0, 19)
}
</script>

<style scoped>
.contact-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.status-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-tab { padding: 6px 16px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 12px; cursor: pointer; transition: all 0.15s; }
.filter-tab:hover { border-color: var(--glass-border-hover); }
.filter-tab.active { background: var(--warm-terracotta); color: white; border-color: transparent; }
.tab-count { font-weight: 700; margin-left: 4px; }

.contact-loading, .contact-empty { text-align: center; padding: 48px; color: var(--text-muted); font-size: 14px; }

.contact-list { display: flex; flex-direction: column; gap: 12px; }
.msg-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); overflow: hidden; transition: box-shadow 0.2s; }
.msg-card.expanded { box-shadow: var(--shadow-md); }
.msg-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; cursor: pointer; gap: 12px; }
.msg-header:hover { background: var(--bg-soft); }
.msg-info { display: flex; align-items: center; gap: 10px; flex: 1; min-width: 0; }
.msg-name { font-family: var(--font-heading); font-size: 14px; white-space: nowrap; }
.msg-subject { font-size: 13px; color: var(--text-secondary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.msg-status { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; white-space: nowrap; }
.status-unread { background: rgba(192, 96, 64, 0.1); color: var(--warm-terracotta); }
.status-read { background: rgba(212, 146, 10, 0.1); color: var(--warm-amber); }
.status-replied { background: rgba(46, 125, 50, 0.1); color: #2e7d32; }
.status-archived { background: var(--surface); color: var(--text-muted); }
.msg-date { font-size: 12px; color: var(--text-muted); white-space: nowrap; }

.msg-detail { padding: 0 20px 20px; border-top: 1px solid var(--glass-border); }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; }
.detail-item span { display: block; font-size: 11px; color: var(--text-muted); }
.detail-item strong { font-size: 13px; }
.detail-block { margin-top: 16px; }
.detail-block span { display: block; font-size: 11px; color: var(--text-muted); margin-bottom: 4px; }
.detail-block p { font-size: 13px; color: var(--text-primary); line-height: 1.7; margin: 0; white-space: pre-wrap; }
.detail-block textarea { width: 100%; padding: 8px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; resize: vertical; }
.detail-block textarea:focus { outline: none; border-color: var(--warm-terracotta); }

.msg-actions { display: flex; gap: 8px; margin-top: 16px; }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-danger { color: #e05050; border-color: #e05050; }
.btn-danger:hover { background: #e05050; color: white; }

@media (max-width: 768px) {
  .contact-toolbar { flex-direction: column; align-items: stretch; }
  .status-tabs { gap: 6px; }
  .filter-tab { padding: 5px 12px; font-size: 11px; }
  .msg-header { padding: 12px 14px; flex-direction: column; align-items: flex-start; gap: 6px; }
  .msg-info { flex-wrap: wrap; gap: 6px; }
  .msg-detail { padding: 0 14px 14px; }
  .detail-grid { grid-template-columns: 1fr; }
  .msg-actions { flex-wrap: wrap; }
}
</style>
