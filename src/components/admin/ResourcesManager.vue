<template>
  <div class="resources-manager">
    <!-- 工具栏 -->
    <div class="resources-toolbar">
      <div class="toolbar-left">
        <div class="status-tabs">
          <button v-for="s in statusOptions" :key="s.key" class="filter-tab" :class="{ active: activeStatus === s.key }" @click="activeStatus = s.key; loadResources()">
            {{ s.label }}
          </button>
        </div>
        <div class="category-tabs">
          <button v-for="cat in categoryOptions" :key="cat.key" class="filter-tab cat-filter" :class="{ active: activeCategory === cat.key }" @click="activeCategory = cat.key; loadResources()">
            {{ cat.label }}
          </button>
        </div>
      </div>
      <div class="toolbar-right">
        <button class="btn btn-outline btn-sm" @click="showCategoryMgr = !showCategoryMgr">分类管理</button>
        <button class="btn btn-outline btn-sm" @click="loadResources">刷新</button>
        <button class="btn btn-primary btn-sm" @click="showUpload = true">上传资源</button>
      </div>
    </div>

    <!-- 资源列表 -->
    <div v-if="loading" class="resources-loading">加载中...</div>
    <div v-else-if="resources.length === 0" class="resources-empty">暂无资源</div>

    <div v-else class="resources-table-wrap">
      <table class="resources-table">
        <thead>
          <tr>
            <th>标题</th>
            <th>分类</th>
            <th>文件名</th>
            <th>标签</th>
            <th>大小</th>
            <th>下载</th>
            <th>上传时间</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in resources" :key="r.id" :class="{ expanded: expandedId === r.id }">
            <td class="col-title" @click="toggleExpand(r)">{{ r.title }}</td>
            <td><span class="cat-badge" :class="'cat-' + r.category">{{ categoryLabels[r.category] || r.category }}</span></td>
            <td class="col-filename">{{ r.file_name }}</td>
            <td class="col-tags">
              <span v-for="tag in (r.tags || []).slice(0, 2)" :key="tag" class="tag-mini">{{ tag }}</span>
            </td>
            <td>{{ formatFileSize(r.file_size) }}</td>
            <td>{{ r.download_count }}</td>
            <td>{{ formatDate(r.created_at) }}</td>
            <td><span class="status-badge" :class="'status-' + r.status">{{ statusLabel(r.status) }}</span></td>
            <td class="col-actions">
              <button class="btn-icon" title="编辑" @click="startEdit(r)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
              </button>
              <button v-if="r.status === 'pending'" class="btn-icon" title="通过" style="color: #2e7d32" @click="handleApprove(r)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              </button>
              <button class="btn-icon btn-danger" title="删除" @click="handleDelete(r)">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分类管理 -->
    <div v-if="showCategoryMgr" class="category-mgr">
      <h4>资源分类管理</h4>
      <div v-for="(label, key) in categoryLabels" :key="key" class="cat-row">
        <span class="cat-key">{{ key }}</span>
        <input :value="label" class="cat-input" @input="categoryLabels[$event.target.key] = $event.target.value" />
        <button class="btn-icon btn-danger" @click="removeCategory(key)">&times;</button>
      </div>
      <div class="cat-add-row">
        <input v-model="newCatKey" placeholder="分类key（英文）" class="cat-input" />
        <input v-model="newCatLabel" placeholder="分类名称" class="cat-input" />
        <button class="btn btn-outline btn-sm" @click="addCategory">添加</button>
      </div>
      <p v-if="catMsg" :class="catOk ? 'form-success' : 'form-error'">{{ catMsg }}</p>
    </div>

    <!-- 上传弹窗 -->
    <div v-if="showUpload" class="modal-overlay" @click.self="showUpload = false">
      <div class="modal-card">
        <h3>上传资源</h3>
        <form @submit.prevent="handleUpload">
          <label>
            <span>资源标题 <em>*</em></span>
            <input v-model="uploadForm.title" type="text" placeholder="输入资源标题" required />
          </label>
          <label>
            <span>分类 <em>*</em></span>
            <select v-model="uploadForm.category" required>
              <option value="" disabled>选择分类</option>
              <option v-for="cat in categoryOptions.filter(c => c.key)" :key="cat.key" :value="cat.key">{{ cat.label }}</option>
            </select>
          </label>
          <label>
            <span>描述</span>
            <textarea v-model="uploadForm.description" rows="3" placeholder="资源描述（选填）"></textarea>
          </label>
          <label>
            <span>标签</span>
            <input v-model="uploadForm.tags" type="text" placeholder="多个标签用逗号分隔，如：Vue3,前端,教程" />
          </label>
          <label>
            <span>文件 <em>*</em></span>
            <input type="file" @change="onFileChange" required />
            <small v-if="uploadForm.file" class="file-info">{{ uploadForm.file.name }} ({{ formatFileSize(uploadForm.file.size) }})</small>
          </label>
          <p v-if="uploadError" class="form-error">{{ uploadError }}</p>
          <div class="modal-actions">
            <button type="button" class="btn btn-outline" @click="showUpload = false">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="uploading">{{ uploading ? '上传中...' : '上传' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <div v-if="showEdit" class="modal-overlay" @click.self="showEdit = false">
      <div class="modal-card">
        <h3>编辑资源</h3>
        <form @submit.prevent="handleUpdate">
          <label>
            <span>资源标题 <em>*</em></span>
            <input v-model="editForm.title" type="text" required />
          </label>
          <label>
            <span>分类 <em>*</em></span>
            <select v-model="editForm.category" required>
              <option v-for="cat in categoryOptions.filter(c => c.key)" :key="cat.key" :value="cat.key">{{ cat.label }}</option>
            </select>
          </label>
          <label>
            <span>描述</span>
            <textarea v-model="editForm.description" rows="3"></textarea>
          </label>
          <label>
            <span>标签</span>
            <input v-model="editForm.tags" type="text" placeholder="多个标签用逗号分隔" />
          </label>
          <label>
            <span>状态</span>
            <select v-model="editForm.status">
              <option value="active">正常</option>
              <option value="archived">归档</option>
            </select>
          </label>
          <div class="modal-actions">
            <button type="button" class="btn btn-outline" @click="showEdit = false">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="updating">{{ updating ? '保存中...' : '保存' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAdminResources, createResource, updateResource, deleteResource, getResourceCategories, updateConfigSection } from '@/services/api'

const resources = ref([])
const loading = ref(false)
const activeStatus = ref('all')
const activeCategory = ref('')
const expandedId = ref(null)

const showUpload = ref(false)
const uploading = ref(false)
const uploadError = ref('')
const uploadForm = ref({ title: '', category: '', description: '', tags: '', file: null })

const showEdit = ref(false)
const updating = ref(false)
const editForm = ref({ id: null, title: '', category: '', description: '', tags: '', status: 'active' })

const statusOptions = [
  { key: 'all', label: '全部' },
  { key: 'pending', label: '待审核' },
  { key: 'active', label: '正常' },
  { key: 'archived', label: '已归档' },
]

const categoryOptions = ref([
  { key: '', label: '全部分类' },
  { key: 'literature', label: '文献' },
  { key: 'tutorial', label: '教程' },
  { key: 'tool', label: '工具' },
  { key: 'template', label: '表格模板' },
  { key: 'learning', label: '学习资料' },
])

const categoryLabels = ref({
  literature: '文献',
  tutorial: '教程',
  tool: '工具',
  template: '表格模板',
  learning: '学习资料',
})

onMounted(async () => {
  await loadResources()
  try {
    const data = await getResourceCategories()
    if (data?.categories) {
      categoryLabels.value = data.categories
      categoryOptions.value = [{ key: '', label: '全部分类' }, ...Object.entries(data.categories).map(([k, v]) => ({ key: k, label: v }))]
    }
  } catch { /* use defaults */ }
})

async function loadResources() {
  loading.value = true
  try {
    const data = await getAdminResources({
      status: activeStatus.value,
      category: activeCategory.value,
    })
    resources.value = data.items
  } catch (e) {
    console.error('加载资源失败', e)
  } finally {
    loading.value = false
  }
}

function toggleExpand(r) {
  expandedId.value = expandedId.value === r.id ? null : r.id
}

function onFileChange(e) {
  uploadForm.value.file = e.target.files[0] || null
}

async function handleUpload() {
  if (!uploadForm.value.file) return
  uploading.value = true
  uploadError.value = ''
  try {
    const fd = new FormData()
    fd.append('title', uploadForm.value.title)
    fd.append('category', uploadForm.value.category)
    fd.append('description', uploadForm.value.description)
    fd.append('tags', uploadForm.value.tags)
    fd.append('file', uploadForm.value.file)
    await createResource(fd)
    showUpload.value = false
    uploadForm.value = { title: '', category: '', description: '', tags: '', file: null }
    await loadResources()
  } catch (e) {
    uploadError.value = e.message || '上传失败'
  } finally {
    uploading.value = false
  }
}

function startEdit(r) {
  editForm.value = {
    id: r.id,
    title: r.title,
    category: r.category,
    description: r.description || '',
    tags: (r.tags || []).join(', '),
    status: r.status,
  }
  showEdit.value = true
}

async function handleUpdate() {
  updating.value = true
  try {
    const tags = editForm.value.tags ? editForm.value.tags.split(',').map(t => t.trim()).filter(Boolean) : []
    await updateResource(editForm.value.id, {
      title: editForm.value.title,
      category: editForm.value.category,
      description: editForm.value.description,
      tags,
      status: editForm.value.status,
    })
    showEdit.value = false
    await loadResources()
  } catch (e) {
    alert('更新失败: ' + (e.message || '未知错误'))
  } finally {
    updating.value = false
  }
}

async function handleDelete(r) {
  if (!confirm(`确定删除资源「${r.title}」？此操作不可撤销。`)) return
  try {
    await deleteResource(r.id)
    await loadResources()
  } catch (e) {
    alert('删除失败: ' + (e.message || '未知错误'))
  }
}

async function handleApprove(r) {
  try {
    await updateResource(r.id, { status: 'active' })
    await loadResources()
  } catch (e) {
    alert('审核失败: ' + (e.message || '未知错误'))
  }
}

function statusLabel(status) {
  const labels = { active: '正常', pending: '待审核', archived: '已归档' }
  return labels[status] || status
}

// Category management
const showCategoryMgr = ref(false)
const newCatKey = ref('')
const newCatLabel = ref('')
const catMsg = ref('')
const catOk = ref(false)

function addCategory() {
  const key = newCatKey.value.trim().toLowerCase().replace(/\s+/g, '-')
  const label = newCatLabel.value.trim()
  if (!key || !label) { catMsg.value = '请填写分类key和名称'; catOk.value = false; return }
  if (categoryLabels.value[key]) { catMsg.value = '该分类已存在'; catOk.value = false; return }
  categoryLabels.value[key] = label
  categoryOptions.value.push({ key, label })
  newCatKey.value = ''
  newCatLabel.value = ''
  saveCategories()
}

function removeCategory(key) {
  if (!confirm(`确定删除分类「${categoryLabels.value[key]}」？`)) return
  delete categoryLabels.value[key]
  categoryOptions.value = categoryOptions.value.filter(c => c.key !== key)
  saveCategories()
}

async function saveCategories() {
  catMsg.value = ''
  try {
    await updateConfigSection('resourceCategories', { ...categoryLabels.value })
    catMsg.value = '分类已保存';
    catOk.value = true
  } catch (e) {
    catMsg.value = '保存失败: ' + (e.message || '未知错误')
    catOk.value = false
  }
}

function formatDate(iso) {
  if (!iso) return ''
  return iso.slice(0, 10)
}

function formatFileSize(bytes) {
  if (!bytes) return '-'
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}
</script>

<style scoped>
.resources-toolbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.toolbar-left { display: flex; gap: 8px; flex-wrap: wrap; }
.toolbar-right { display: flex; gap: 8px; }
.status-tabs, .category-tabs { display: flex; gap: 6px; flex-wrap: wrap; }
.filter-tab { padding: 5px 12px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 11px; cursor: pointer; transition: all 0.15s; }
.filter-tab:hover { border-color: var(--glass-border-hover); }
.filter-tab.active { background: var(--warm-terracotta); color: white; border-color: transparent; }
.btn-sm { padding: 6px 14px; font-size: 12px; }

.resources-loading, .resources-empty { text-align: center; padding: 48px; color: var(--text-muted); font-size: 14px; }

.resources-table-wrap { overflow-x: auto; }
.resources-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-sm); }
.resources-table th { padding: 12px 16px; text-align: left; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); background: var(--bg-soft); border-bottom: 1px solid var(--glass-border); white-space: nowrap; }
.resources-table td { padding: 12px 16px; font-size: 13px; border-bottom: 1px solid var(--glass-border); color: var(--text-primary); }
.resources-table tr:hover { background: rgba(192, 96, 64, 0.02); }
.col-title { cursor: pointer; font-weight: 500; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.col-title:hover { color: var(--warm-terracotta); }
.col-filename { max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--text-secondary); font-size: 12px; }
.col-tags { display: flex; gap: 4px; flex-wrap: wrap; }
.tag-mini { font-size: 10px; padding: 1px 6px; background: var(--bg-soft); color: var(--text-muted); border-radius: 999px; white-space: nowrap; }
.col-actions { display: flex; gap: 6px; }

.cat-badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; white-space: nowrap; }
.cat-literature { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.cat-tutorial { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.cat-tool { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.cat-template { background: rgba(168, 85, 247, 0.1); color: #a855f7; }
.cat-learning { background: rgba(236, 72, 153, 0.1); color: #ec4899; }

.status-badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
.status-active { background: rgba(46, 125, 50, 0.1); color: #2e7d32; }
.status-pending { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.status-archived { background: var(--surface); color: var(--text-muted); }

.btn-icon { width: 28px; height: 28px; border: none; background: none; cursor: pointer; display: flex; align-items: center; justify-content: center; border-radius: 6px; color: var(--text-secondary); transition: all 0.15s; }
.btn-icon:hover { background: var(--bg-soft); color: var(--text-primary); }
.btn-icon.btn-danger:hover { background: rgba(224, 80, 80, 0.1); color: #e05050; }

/* 弹窗 */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 20px; }
.modal-card { background: #fff; border-radius: var(--radius-xl); padding: 32px; width: 100%; max-width: 480px; box-shadow: var(--shadow-lg); max-height: 90vh; overflow-y: auto; }
.modal-card h3 { font-family: var(--font-heading); font-size: 18px; margin: 0 0 24px; }
.modal-card label { display: block; margin-bottom: 16px; }
.modal-card label span { display: block; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 6px; }
.modal-card label span em { color: var(--warm-terracotta); font-style: normal; }
.modal-card input, .modal-card select, .modal-card textarea { width: 100%; padding: 10px 14px; border: 1px solid var(--glass-border); border-radius: var(--radius-md); font-size: 14px; background: white; color: var(--text-primary); transition: border-color 0.2s; font-family: inherit; box-sizing: border-box; }
.modal-card input:focus, .modal-card select:focus, .modal-card textarea:focus { outline: none; border-color: var(--warm-terracotta); box-shadow: 0 0 0 3px rgba(192, 96, 64, 0.1); }
.modal-card textarea { resize: vertical; }
.file-info { display: block; margin-top: 6px; font-size: 12px; color: var(--text-muted); }
.form-error { color: #e05050; font-size: 13px; margin: 8px 0; }
.modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 24px; }

/* Category management */
.category-mgr { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 20px; margin-top: 20px; }
.category-mgr h4 { font-family: var(--font-heading); font-size: 14px; margin: 0 0 16px; }
.cat-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.cat-key { font-size: 12px; color: var(--text-muted); width: 80px; flex-shrink: 0; font-family: monospace; }
.cat-input { flex: 1; padding: 6px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 13px; }
.cat-input:focus { outline: none; border-color: var(--warm-terracotta); }
.cat-add-row { display: flex; gap: 10px; margin-top: 12px; }
.form-success { color: #2e7d32; font-size: 12px; margin: 8px 0 0; }

@media (max-width: 768px) {
  .resources-toolbar { flex-direction: column; align-items: stretch; }
  .toolbar-left, .toolbar-right { flex-wrap: wrap; }
  .resources-table { font-size: 12px; }
  .resources-table th, .resources-table td { padding: 8px 10px; }
}
</style>
