<template>
  <header class="admin-header">
    <div class="header-left">
      <button class="sidebar-toggle" @click="$emit('toggle-sidebar')">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      </button>
      <h2 class="header-title">{{ sectionLabels[section] || section }}</h2>
      <span v-if="isDirty" class="dirty-badge">未保存</span>
    </div>
    <div class="header-right">
      <span class="header-user">{{ username }}</span>
      <button class="btn btn-outline btn-sm" @click="$emit('preview')">预览</button>
      <button class="btn btn-primary btn-sm" :disabled="isSaving || !isDirty" @click="$emit('save')">
        {{ isSaving ? '保存中...' : '保存' }}
      </button>
      <div class="data-divider"></div>
      <button class="btn btn-outline btn-sm" @click="$emit('export-data')">导出</button>
      <label class="btn btn-outline btn-sm import-btn">
        <input type="file" accept=".json" @change="$emit('import-data', $event)" hidden />
        导入
      </label>
      <button class="btn btn-outline btn-sm btn-warn" @click="$emit('reset-data')">重置</button>
      <div class="data-divider"></div>
      <button class="btn btn-outline btn-sm" @click="$emit('logout')">退出</button>
    </div>
  </header>
</template>

<script setup>
defineProps({
  section: String,
  isDirty: Boolean,
  isSaving: Boolean,
  username: String,
})
defineEmits(['save', 'preview', 'logout', 'toggle-sidebar', 'export-data', 'import-data', 'reset-data'])

const sectionLabels = {
  hero: 'Hero 区域',
  about: '社团简介',
  members: '人员介绍',
  products: '产品展示',
  openSource: '开源精神',
  footer: '页脚信息',
  pages: '页面管理',
  sections: '模块管理',
  applications: '申请管理',
}
</script>

<style scoped>
.admin-header { height: 56px; background: #fff; border-bottom: 1px solid var(--glass-border); display: flex; align-items: center; justify-content: space-between; padding: 0 24px; flex-shrink: 0; }
.header-left { display: flex; align-items: center; gap: 12px; }
.header-title { font-family: var(--font-heading); font-size: 16px; font-weight: 600; margin: 0; }
.dirty-badge { font-size: 11px; font-weight: 600; color: var(--warm-amber); background: rgba(212, 146, 10, 0.1); padding: 2px 10px; border-radius: 999px; }
.header-right { display: flex; align-items: center; gap: 10px; }
.header-user { font-size: 13px; color: var(--text-muted); }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-warn { color: var(--warm-amber); border-color: var(--warm-amber); }
.btn-warn:hover { background: var(--warm-amber); color: white; }
.import-btn { cursor: pointer; }
.data-divider { width: 1px; height: 20px; background: var(--glass-border); }
.sidebar-toggle { display: none; background: none; border: none; padding: 4px; cursor: pointer; color: var(--text-primary); border-radius: 6px; }
.sidebar-toggle:hover { background: var(--bg-soft); }

@media (max-width: 768px) {
  .sidebar-toggle { display: flex; }
  .admin-header { padding: 0 12px; gap: 8px; }
  .header-user { display: none; }
  .header-title { font-size: 14px; }
  .btn-sm { padding: 5px 10px; font-size: 11px; }
  .data-divider { display: none; }
}
</style>
