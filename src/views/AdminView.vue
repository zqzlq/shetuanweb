<template>
  <div class="admin-view">
    <!-- 登录 -->
    <div v-if="!isLoggedIn" class="login-wrap">
      <div class="login-card">
        <h1>星雨作坊</h1>
        <p class="login-sub">管理后台</p>
        <form @submit.prevent="handleLogin">
          <label>
            <span>用户名</span>
            <input v-model="loginForm.username" type="text" placeholder="admin" autocomplete="username" />
          </label>
          <label>
            <span>密码</span>
            <input v-model="loginForm.password" type="password" placeholder="密码" autocomplete="current-password" />
          </label>
          <p v-if="loginError" class="login-error">{{ loginError }}</p>
          <button type="submit" class="btn btn-primary login-btn" :disabled="loginLoading">
            {{ loginLoading ? '登录中...' : '登录' }}
          </button>
        </form>
      </div>
    </div>

    <!-- 管理面板 -->
    <div v-else class="admin-layout">
      <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false"></div>
      <AdminSidebar :active-section="activeSection" :open="sidebarOpen" @navigate="activeSection = $event; sidebarOpen = false" />
      <div class="admin-main">
        <AdminHeader
          :section="activeSection"
          :is-dirty="isDirty"
          :is-saving="isSaving"
          :username="currentUser?.username"
          @toggle-sidebar="sidebarOpen = !sidebarOpen"
          @save="handleSave"
          @preview="handlePreview"
          @logout="handleLogout"
          @export-data="handleExport"
          @import-data="handleImport"
          @reset-data="handleReset"
        />
        <div class="admin-content">
          <!-- 首页配置编辑器 -->
          <HeroEditor v-if="activeSection === 'hero' && siteConfig.hero" v-model="siteConfig.hero" @update:modelValue="markDirty" />
          <AboutEditor v-if="activeSection === 'about' && siteConfig.about" v-model="siteConfig.about" @update:modelValue="markDirty" />
          <MembersEditor v-if="activeSection === 'members' && siteConfig.members" v-model="siteConfig.members" @update:modelValue="markDirty" />
          <ProductsEditor v-if="activeSection === 'products' && siteConfig.products" v-model="siteConfig.products" :all-projects="projectsPageProjects" @update:modelValue="markDirty" />
          <OpenSourceEditor v-if="activeSection === 'openSource' && siteConfig.openSource" v-model="siteConfig.openSource" @update:modelValue="markDirty" />
          <FooterEditor v-if="activeSection === 'footer' && siteConfig.footer" v-model="siteConfig.footer" @update:modelValue="markDirty" />
          <SystemSettingsEditor v-if="activeSection === 'system' && siteConfig.system" v-model="siteConfig.system" @update:modelValue="markDirty" />

          <!-- 模块管理 -->
          <div v-if="activeSection === 'sections'" class="sections-editor">
            <div class="editor-card">
              <h3 class="editor-title">首页模块可见性</h3>
              <p class="editor-hint">控制官网首页各模块的显示与隐藏</p>
              <div v-for="s in sectionItems" :key="s.key" class="section-toggle-row">
                <label class="toggle-label">
                  <input type="checkbox" :checked="siteConfig.sections?.[s.key] !== false" @change="toggleSection(s.key, $event.target.checked)" />
                  <span class="toggle-name">{{ s.label }}</span>
                </label>
                <span class="toggle-status" :class="siteConfig.sections?.[s.key] !== false ? 'on' : 'off'">
                  {{ siteConfig.sections?.[s.key] !== false ? '显示' : '隐藏' }}
                </span>
              </div>
            </div>
          </div>

          <!-- 页面管理 -->
          <PagesEditor v-if="activeSection === 'pages'" :pages="pages" @update="handlePageUpdate" @reset="handlePageReset" />

          <!-- 申请管理 -->
          <ApplicationsManager v-if="activeSection === 'applications'" />

          <!-- 用户管理 -->
          <UserManager v-if="activeSection === 'users'" @refresh="loadPages" />

          <!-- 提交审核 -->
          <SubmissionManager v-if="activeSection === 'submissions'" />

          <!-- 留言管理 -->
          <ContactManager v-if="activeSection === 'contactMessages'" />

          <!-- 资源管理 -->
          <ResourcesManager v-if="activeSection === 'resources'" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, provide } from 'vue'
import { login as apiLogin, logout as apiLogout, isLoggedIn as checkLoggedIn, getCurrentUser, getAdminConfig, updateConfig, getAdminPages, updatePage, resetPage, exportAll, importAll, resetAllContent } from '@/services/api'
import AdminSidebar from '@/components/admin/AdminSidebar.vue'
import AdminHeader from '@/components/admin/AdminHeader.vue'
import HeroEditor from '@/components/admin/editors/HeroEditor.vue'
import AboutEditor from '@/components/admin/editors/AboutEditor.vue'
import MembersEditor from '@/components/admin/editors/MembersEditor.vue'
import ProductsEditor from '@/components/admin/editors/ProductsEditor.vue'
import OpenSourceEditor from '@/components/admin/editors/OpenSourceEditor.vue'
import FooterEditor from '@/components/admin/editors/FooterEditor.vue'
import PagesEditor from '@/components/admin/PagesEditor.vue'
import UserManager from '@/components/admin/UserManager.vue'
import SubmissionManager from '@/components/admin/SubmissionManager.vue'
import ApplicationsManager from '@/components/admin/ApplicationsManager.vue'
import ContactManager from '@/components/admin/ContactManager.vue'
import ResourcesManager from '@/components/admin/ResourcesManager.vue'
import SystemSettingsEditor from '@/components/admin/SystemSettingsEditor.vue'

const isLoggedIn = ref(false)
const currentUser = ref(null)
const loginForm = reactive({ username: '', password: '' })
const loginError = ref('')
const loginLoading = ref(false)

const activeSection = ref('hero')
const siteConfig = reactive({})
const pages = ref([])
const isDirty = ref(false)
const isSaving = ref(false)
const sidebarOpen = ref(false)

provide('productCategories', computed(() => siteConfig.products?.categories || []))

const sectionItems = [
  { key: 'hero', label: 'Hero 区域' },
  { key: 'about', label: '社团简介' },
  { key: 'members', label: '人员介绍' },
  { key: 'products', label: '产品展示' },
  { key: 'awards', label: '荣誉展示' },
  { key: 'announcements', label: '公告动态' },
  { key: 'openSource', label: '开源精神' },
]

const projectsPageProjects = computed(() => {
  const projPage = pages.value.find(p => p.slug === 'projects')
  return projPage?.content?.projects || []
})

onMounted(async () => {
  if (checkLoggedIn()) {
    try {
      currentUser.value = await getCurrentUser()
      isLoggedIn.value = true
      await loadData()
    } catch {
      apiLogout()
    }
  }
})

async function loadData() {
  try {
    const config = await getAdminConfig()
    Object.assign(siteConfig, config)
    pages.value = await getAdminPages()
  } catch (e) {
    console.error('加载数据失败', e)
  }
}

async function loadPages() {
  try {
    pages.value = await getAdminPages()
  } catch (e) {
    console.error('加载页面数据失败', e)
  }
}

async function handleLogin() {
  loginError.value = ''
  loginLoading.value = true
  try {
    const data = await apiLogin(loginForm.username, loginForm.password)
    currentUser.value = data.user
    isLoggedIn.value = true
    await loadData()
  } catch (e) {
    loginError.value = e.message || '登录失败'
  } finally {
    loginLoading.value = false
  }
}

function handleLogout() {
  apiLogout()
  isLoggedIn.value = false
  currentUser.value = null
  Object.keys(siteConfig).forEach((k) => delete siteConfig[k])
  pages.value = []
  activeSection.value = 'hero'
  isDirty.value = false
}

function markDirty() {
  isDirty.value = true
}

function toggleSection(key, checked) {
  if (!siteConfig.sections) siteConfig.sections = {}
  siteConfig.sections[key] = checked
  markDirty()
}

async function handleSave() {
  isSaving.value = true
  try {
    if (activeSection.value === 'pages') {
      // 页面编辑器有自己的保存按钮，全局保存时提示用户
      alert('请使用页面编辑器内的"保存"按钮保存页面内容')
      return
    }
    await updateConfig(siteConfig)
    isDirty.value = false
  } catch (e) {
    alert('保存失败: ' + (e.message || '未知错误'))
  } finally {
    isSaving.value = false
  }
}

async function handlePageUpdate({ slug, data }) {
  try {
    await updatePage(slug, data)
    const idx = pages.value.findIndex((p) => p.slug === slug)
    if (idx !== -1) pages.value[idx] = { ...pages.value[idx], ...data }
  } catch (e) {
    alert('保存失败: ' + (e.message || '未知错误'))
  }
}

async function handlePageReset(slug) {
  if (!confirm(`确定要将 ${slug} 重置为默认内容吗？`)) return
  try {
    await resetPage(slug)
    const updated = await getAdminPages()
    pages.value = updated
  } catch (e) {
    alert('重置失败: ' + (e.message || '未知错误'))
  }
}

function handlePreview() {
  window.open('/', '_blank')
}

async function handleExport() {
  try {
    const data = await exportAll()
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `xingyu-backup-${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    alert('导出失败: ' + (e.message || '未知错误'))
  }
}

async function handleImport(event) {
  const file = event.target.files?.[0]
  if (!file) return
  try {
    const text = await file.text()
    const data = JSON.parse(text)
    if (!data.config && !data.pages) {
      alert('无效的备份文件格式')
      return
    }
    await importAll(data)
    await loadData()
    alert('数据导入成功')
  } catch (e) {
    alert('导入失败: ' + (e.message || '未知错误'))
  }
  event.target.value = ''
}

async function handleReset() {
  if (!confirm('确定要重置所有内容为默认值吗？此操作不可撤销。')) return
  try {
    await resetAllContent()
    await loadData()
    alert('已重置为默认内容')
  } catch (e) {
    alert('重置失败: ' + (e.message || '未知错误'))
  }
}
</script>

<style scoped>
.admin-view { min-height: 100vh; background: var(--bg-soft); }

/* 登录 */
.login-wrap { display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
.login-card { background: #fff; border-radius: var(--radius-xl); padding: 48px 40px; width: 100%; max-width: 380px; box-shadow: var(--shadow-lg); }
.login-card h1 { font-family: var(--font-heading); font-size: 24px; text-align: center; margin-bottom: 4px; }
.login-sub { text-align: center; color: var(--text-muted); font-size: 14px; margin-bottom: 32px; }
.login-card label { display: block; margin-bottom: 16px; }
.login-card label span { display: block; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 6px; }
.login-card input { width: 100%; padding: 10px 14px; border: 1px solid var(--glass-border); border-radius: var(--radius-md); font-size: 14px; background: white; color: var(--text-primary); transition: border-color 0.2s; }
.login-card input:focus { outline: none; border-color: var(--warm-terracotta); box-shadow: 0 0 0 3px rgba(192, 96, 64, 0.1); }
.login-error { color: #e05050; font-size: 13px; margin: 8px 0; }
.login-btn { width: 100%; margin-top: 8px; }

/* 布局 */
.admin-layout { display: flex; min-height: 100vh; }
.admin-main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.admin-content { flex: 1; padding: 24px; overflow-y: auto; }

/* 模块管理 */
.sections-editor { max-width: 600px; }
.sections-editor .editor-card { background: #fff; border-radius: var(--radius-lg); padding: 24px; box-shadow: var(--shadow-sm); }
.editor-title { font-family: var(--font-heading); font-size: 16px; font-weight: 600; margin: 0 0 4px; }
.editor-hint { font-size: 13px; color: var(--text-muted); margin: 0 0 20px; }
.section-toggle-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--glass-border); }
.section-toggle-row:last-child { border-bottom: none; }
.toggle-label { display: flex; align-items: center; gap: 10px; cursor: pointer; }
.toggle-label input[type="checkbox"] { width: 16px; height: 16px; accent-color: var(--warm-terracotta); cursor: pointer; }
.toggle-name { font-size: 14px; font-weight: 500; color: var(--text-primary); }
.toggle-status { font-size: 12px; font-weight: 600; padding: 2px 10px; border-radius: 999px; }
.toggle-status.on { color: #2e7d32; background: rgba(46, 125, 50, 0.1); }
.toggle-status.off { color: #c62828; background: rgba(198, 40, 40, 0.1); }

.sidebar-overlay { display: none; }

@media (max-width: 768px) {
  .sidebar-overlay { display: block; position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 99; }
  .admin-content { padding: 16px; }
}
</style>
