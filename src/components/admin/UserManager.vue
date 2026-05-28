<template>
  <div class="user-manager">
    <div class="apps-toolbar">
      <div class="status-tabs">
        <button v-for="s in statuses" :key="s.key" class="filter-tab" :class="{ active: activeStatus === s.key }" @click="activeStatus = s.key">{{ s.label }}<span v-if="counts[s.key]" class="tab-count">{{ counts[s.key] }}</span></button>
      </div>
      <button class="btn btn-outline btn-sm" @click="loadUsers">刷新</button>
    </div>

    <!-- 批量操作栏 -->
    <div v-if="selectedIds.size > 0" class="batch-bar">
      <span class="batch-info">已选 <strong>{{ selectedIds.size }}</strong> 项</span>
      <button class="btn btn-outline btn-sm btn-reject" @click="batchAction('disable')">批量禁用</button>
      <button class="btn btn-outline btn-sm" @click="batchAction('add-to-members')">批量添加到成员</button>
      <button class="btn btn-outline btn-sm btn-danger" @click="batchAction('delete')">批量删除</button>
      <button class="btn btn-outline btn-sm" @click="selectedIds.clear()">取消选择</button>
    </div>

    <div v-if="loading" class="apps-loading">加载中...</div>
    <div v-else-if="filtered.length === 0" class="apps-empty">暂无用户</div>

    <div v-else class="apps-list">
      <div v-for="u in filtered" :key="u.id" class="app-card" :class="{ selected: selectedIds.has(u.id) }">
        <div class="app-header">
          <div class="app-info">
            <input type="checkbox" :checked="selectedIds.has(u.id)" class="app-check" @click.stop @change="toggleSelect(u.id)" />
            <span class="user-avatar">{{ u.name[0] }}</span>
            <strong class="app-name">{{ u.name }}</strong>
            <span v-if="u.student_id" class="app-group tag tag-accent">{{ u.student_id }}</span>
            <span class="app-status" :class="'status-' + u.status">{{ statusLabel(u.status) }}</span>
          </div>
          <span class="app-date">{{ u.email }}</span>
        </div>
        <div class="app-detail">
          <div class="detail-grid">
            <div class="detail-item"><span>用户名</span><strong>{{ u.username }}</strong></div>
            <div class="detail-item"><span>邮箱</span><strong>{{ u.email }}</strong></div>
            <div class="detail-item"><span>学号</span><strong>{{ u.student_id || '-' }}</strong></div>
            <div class="detail-item"><span>手机</span><strong>{{ u.phone || '-' }}</strong></div>
          </div>
          <div class="app-actions">
            <button v-if="u.status === 'pending'" class="btn btn-primary btn-sm" @click="updateUserStatus(u.id, 'approved')">通过</button>
            <button v-if="u.status === 'pending'" class="btn btn-outline btn-sm btn-reject" @click="updateUserStatus(u.id, 'rejected')">拒绝</button>
            <button v-if="u.status === 'approved'" class="btn btn-outline btn-sm" @click="syncToMember(u.id, u.name)">添加到成员</button>
            <button v-if="u.status === 'approved'" class="btn btn-outline btn-sm btn-reject" @click="updateUserStatus(u.id, 'rejected')">禁用</button>
            <button v-if="u.status === 'rejected'" class="btn btn-primary btn-sm" @click="updateUserStatus(u.id, 'approved')">重新通过</button>
            <button class="btn btn-outline btn-sm btn-danger" @click="deleteSingle(u.id, u.name)">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getUsers, updateUser, deleteUser, batchUpdateUsers, syncUserToMember } from '@/services/api'

const emit = defineEmits(['refresh'])

const users = ref([])
const loading = ref(false)
const activeStatus = ref('pending')
const selectedIds = ref(new Set())

const statuses = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待审核' },
  { key: 'approved', label: '已通过' },
  { key: 'rejected', label: '已拒绝' },
]

const counts = computed(() => {
  const c = { all: users.value.length }
  users.value.forEach(u => { c[u.status] = (c[u.status] || 0) + 1 })
  return c
})

const filtered = computed(() => {
  if (activeStatus.value === 'all') return users.value
  return users.value.filter(u => u.status === activeStatus.value)
})

onMounted(loadUsers)

function toggleSelect(id) {
  const next = new Set(selectedIds.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  selectedIds.value = next
}

async function loadUsers() {
  loading.value = true
  try { users.value = await getUsers('all') }
  catch (e) { console.error('加载用户失败', e) }
  finally { loading.value = false }
}

async function updateUserStatus(id, status) {
  try {
    await updateUser(id, { status })
    await loadUsers()
  } catch (e) { alert('操作失败: ' + e.message) }
}

async function syncToMember(id, name) {
  if (!confirm(`确定将 ${name} 添加到官网成员展示页吗？`)) return
  try {
    await syncUserToMember(id)
    alert(`${name} 已添加到成员页面`)
    emit('refresh')
  } catch (e) { alert('操作失败: ' + e.message) }
}

async function deleteSingle(id, name) {
  if (!confirm(`确定删除用户 ${name} 吗？其提交记录也将被删除，已在成员展示中的记录将被移除。`)) return
  try {
    await deleteUser(id)
    selectedIds.value = new Set([...selectedIds.value].filter(x => x !== id))
    await loadUsers()
    emit('refresh')
  } catch (e) { alert('删除失败: ' + e.message) }
}

async function batchAction(action) {
  const ids = [...selectedIds.value]
  const label = { disable: '批量禁用', 'add-to-members': '批量添加到成员', delete: '批量删除' }[action]
  if (!confirm(`确定${label}选中的 ${ids.length} 个用户吗？`)) return
  try {
    await batchUpdateUsers({ ids, action })
    selectedIds.value = new Set()
    await loadUsers()
    if (action === 'add-to-members') emit('refresh')
    alert(`${label}完成`)
  } catch (e) { alert('操作失败: ' + e.message) }
}

function statusLabel(s) {
  const map = { pending: '待审核', approved: '已通过', rejected: '已拒绝' }
  return map[s] || s
}
</script>

<style scoped>
.user-manager { }
.apps-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.status-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
.filter-tab { padding: 6px 16px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 12px; cursor: pointer; transition: all 0.15s; }
.filter-tab.active { background: var(--warm-terracotta); color: white; border-color: transparent; }
.tab-count { font-weight: 700; margin-left: 4px; }
.batch-bar { display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: rgba(192,96,64,0.06); border: 1px solid rgba(192,96,64,0.2); border-radius: var(--radius-md); margin-bottom: 16px; }
.batch-info { font-size: 13px; color: var(--text-secondary); }
.batch-info strong { color: var(--warm-terracotta); }
.apps-loading, .apps-empty { text-align: center; padding: 48px; color: var(--text-muted); font-size: 14px; }
.apps-list { display: flex; flex-direction: column; gap: 12px; }
.app-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); overflow: hidden; }
.app-card.selected { border-color: var(--warm-terracotta); background: rgba(192,96,64,0.02); }
.app-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; gap: 12px; }
.app-info { display: flex; align-items: center; gap: 10px; flex: 1; min-width: 0; }
.app-check { width: 16px; height: 16px; accent-color: var(--warm-terracotta); cursor: pointer; flex-shrink: 0; }
.user-avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--warm-terracotta); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
.app-name { font-family: var(--font-heading); font-size: 14px; white-space: nowrap; }
.app-group { font-size: 11px; }
.app-status { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; white-space: nowrap; }
.status-pending { background: rgba(212,146,10,0.1); color: var(--warm-amber); }
.status-approved { background: rgba(46,125,50,0.1); color: #2e7d32; }
.status-rejected { background: rgba(198,40,40,0.1); color: #c62828; }
.app-date { font-size: 12px; color: var(--text-muted); white-space: nowrap; }
.app-detail { padding: 0 20px 16px; border-top: 1px solid var(--glass-border); display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px; }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px; flex: 1; }
.detail-item span { display: block; font-size: 11px; color: var(--text-muted); }
.detail-item strong { font-size: 13px; }
.app-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-reject { color: #c62828; border-color: #c62828; }
.btn-reject:hover { background: #c62828; color: white; }
.btn-danger { color: #e05050; border-color: #e05050; }
.btn-danger:hover { background: #e05050; color: white; }
@media (max-width: 768px) { .app-detail { flex-direction: column; } .detail-grid { grid-template-columns: 1fr; } .batch-bar { flex-wrap: wrap; } }
</style>
