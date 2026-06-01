<template>
  <aside class="admin-sidebar" :class="{ open: open }">
    <div class="sidebar-brand">
      <span class="brand-icon">星</span>
      <span class="brand-text">管理后台</span>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-group">
        <div class="nav-group-title">首页配置</div>
        <button v-for="s in configSections" :key="s.key" class="nav-item" :class="{ active: activeSection === s.key }" @click="$emit('navigate', s.key)">
          <span class="nav-label">{{ s.label }}</span>
        </button>
      </div>

      <div class="nav-group">
        <div class="nav-group-title">内容管理</div>
        <button class="nav-item" :class="{ active: activeSection === 'pages' }" @click="$emit('navigate', 'pages')">
          <span class="nav-label">页面管理</span>
        </button>
        <button class="nav-item" :class="{ active: activeSection === 'applications' }" @click="$emit('navigate', 'applications')">
          <span class="nav-label">申请管理</span>
        </button>
        <button class="nav-item" :class="{ active: activeSection === 'users' }" @click="$emit('navigate', 'users')">
          <span class="nav-label">用户管理</span>
        </button>
        <button class="nav-item" :class="{ active: activeSection === 'submissions' }" @click="$emit('navigate', 'submissions')">
          <span class="nav-label">提交审核</span>
        </button>
        <button class="nav-item" :class="{ active: activeSection === 'contactMessages' }" @click="$emit('navigate', 'contactMessages')">
          <span class="nav-label">留言管理</span>
        </button>
      </div>
    </nav>
  </aside>
</template>

<script setup>
defineProps({ activeSection: String, open: Boolean })
defineEmits(['navigate'])

const configSections = [
  { key: 'hero', label: 'Hero 区域' },
  { key: 'about', label: '社团简介' },
  { key: 'members', label: '人员介绍' },
  { key: 'products', label: '产品展示' },
  { key: 'openSource', label: '开源精神' },
  { key: 'footer', label: '页脚信息' },
  { key: 'sections', label: '模块管理' },
  { key: 'system', label: '系统设置' },
]
</script>

<style scoped>
.admin-sidebar { width: 240px; background: #fff; border-right: 1px solid var(--glass-border); display: flex; flex-direction: column; flex-shrink: 0; }
.sidebar-brand { display: flex; align-items: center; gap: 10px; padding: 16px 20px; border-bottom: 1px solid var(--glass-border); }
.brand-icon { width: 32px; height: 32px; border-radius: 8px; background: var(--grad-primary); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; }
.brand-text { font-family: var(--font-heading); font-weight: 600; font-size: 15px; color: var(--text-primary); }

.sidebar-nav { flex: 1; overflow-y: auto; padding: 12px 0; }
.nav-group { margin-bottom: 8px; }
.nav-group-title { padding: 8px 20px 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); }
.nav-item { display: flex; align-items: center; gap: 10px; width: 100%; padding: 10px 20px; border: none; background: none; font-size: 14px; color: var(--text-secondary); cursor: pointer; transition: all 0.15s; text-align: left; }
.nav-item:hover { background: var(--bg-soft); color: var(--text-primary); }
.nav-item.active { background: rgba(192, 96, 64, 0.08); color: var(--warm-terracotta); font-weight: 600; }

@media (max-width: 768px) {
  .admin-sidebar { position: fixed; top: 0; left: 0; bottom: 0; z-index: 100; transform: translateX(-100%); transition: transform 0.25s ease; box-shadow: none; }
  .admin-sidebar.open { transform: translateX(0); box-shadow: 4px 0 24px rgba(0,0,0,0.12); }
}
</style>
