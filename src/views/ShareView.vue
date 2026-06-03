<template>
  <div class="page-view">
    <div class="container">
      <div v-if="loading" class="share-loading">加载中...</div>
      <div v-else-if="error" class="share-error">
        <h2>链接无效</h2>
        <p>{{ error }}</p>
        <a href="/" class="btn btn-primary btn-sm">返回首页</a>
      </div>
      <template v-else-if="resource">
        <!-- 面包屑（文件夹浏览时） -->
        <div v-if="breadcrumb.length" class="share-breadcrumb">
          <span class="breadcrumb-item" @click="goToTop()">{{ resource.name }}</span>
          <template v-for="item in breadcrumb" :key="item.id">
            <span class="breadcrumb-sep">></span>
            <span class="breadcrumb-item active">{{ item.name }}</span>
          </template>
        </div>

        <!-- 文件预览（图片/PDF） -->
        <template v-if="!resource.is_folder">
          <div v-if="previewing" class="share-preview-card">
            <img v-if="isImage" :src="resource.file_url" class="preview-img" />
            <iframe v-else-if="isPdf" :src="resource.file_url" class="preview-pdf"></iframe>
            <div class="preview-meta">
              <h2 class="share-name">{{ resource.name }}</h2>
              <div class="share-meta-row">
                <span>{{ formatSize(resource.file_size) }}</span>
                <span>{{ (resource.file_ext || '').toUpperCase() }}</span>
                <span>{{ formatDate(resource.created_at) }}</span>
              </div>
            </div>
          </div>
          <div v-else class="share-card">
            <div class="share-icon" v-html="iconSvg(resource.file_ext, 48)"></div>
            <h2 class="share-name">{{ resource.name }}</h2>
            <div class="share-meta-row">
              <span>{{ formatSize(resource.file_size) }}</span>
              <span>{{ (resource.file_ext || '').toUpperCase() }}</span>
              <span>{{ formatDate(resource.created_at) }}</span>
            </div>
            <p v-if="resource.description" class="share-desc">{{ resource.description }}</p>
            <div class="share-actions">
              <button v-if="isImage || isPdf" class="btn btn-outline btn-sm" @click="previewing = true">预览</button>
              <button class="btn btn-primary btn-sm" @click="handleDownload()">下载文件</button>
            </div>
          </div>
        </template>

        <!-- 文件夹内容 -->
        <template v-else>
          <div class="share-card share-folder-card">
            <h2 class="share-folder-title">📁 {{ resource.name }}</h2>
            <p v-if="resource.description" class="share-desc">{{ resource.description }}</p>

            <div v-if="!children.length" class="share-loading">加载中...</div>
            <div v-else class="share-folder-list">
              <div v-for="item in children" :key="item.id" class="share-folder-item" @click="item.is_folder ? navigateTo(item) : openItem(item)">
                <span class="item-icon" v-html="iconSvg(item.is_folder ? 'folder' : item.file_ext, 28)"></span>
                <span class="item-name">{{ item.name }}</span>
                <span class="item-size">{{ item.is_folder ? '-' : formatSize(item.file_size) }}</span>
                <button v-if="!item.is_folder" class="btn btn-primary btn-xs" @click.stop="downloadItem(item)">下载</button>
              </div>
            </div>
          </div>
        </template>

        <p class="share-footer">由星雨作坊资源中心分享</p>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const loading = ref(true)
const error = ref('')
const resource = ref(null)
const children = ref([])
const breadcrumb = ref([])
const previewing = ref(false)

const isImage = computed(() => ['jpg','jpeg','png','gif','webp','svg','bmp','ico'].includes((resource.value?.file_ext || '').toLowerCase()))
const isPdf = computed(() => (resource.value?.file_ext || '').toLowerCase() === 'pdf')

const ICON_COLORS = {
  folder: '#f5a623', pdf: '#e74c3c', doc: '#2b7cd3', docx: '#2b7cd3',
  xls: '#217346', xlsx: '#217346', ppt: '#d04423',
  jpg: '#27ae60', jpeg: '#27ae60', png: '#27ae60', gif: '#27ae60', webp: '#27ae60',
  zip: '#e67e22', rar: '#e67e22', py: '#3572a5', js: '#f1e05a',
  txt: '#6b5e52', md: '#6b5e52', mp4: '#9b59b6',
}

function iconSvg(ext, size = 20) {
  const type = (ext || '').toLowerCase()
  const color = ICON_COLORS[type] || '#8b7355'
  if (type === 'folder') {
    return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none"><path d="M2 6C2 4.9 2.9 4 4 4H9L11 7H20c1.1 0 2 .9 2 2v9c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6Z" fill="${color}"/></svg>`
  }
  const imgExts = ['jpg','jpeg','png','gif','webp','svg']
  let symbol = 'F'
  if (imgExts.includes(type)) symbol = '🖼'
  else if (['zip','rar','7z','tar','gz'].includes(type)) symbol = '📦'
  else if (['xls','xlsx','csv'].includes(type)) symbol = '📊'
  else if (['ppt','pptx'].includes(type)) symbol = '📑'
  else if (['mp4','mp3','wav'].includes(type)) symbol = '▶'
  else if (type === 'pdf') symbol = 'PDF'
  else if (['py','js','ts','html','css','json'].includes(type)) symbol = '</>'
  else symbol = 'A'
  const fs = symbol.length > 2 ? '7' : '10'
  return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none"><rect x="4" y="2" width="16" height="20" rx="2" fill="${color}" opacity="0.15"/><rect x="4" y="2" width="16" height="20" rx="2" stroke="${color}" stroke-width="1.5" fill="none"/><text x="12" y="15" text-anchor="middle" font-size="${fs}" font-weight="600" fill="${color}">${symbol}</text></svg>`
}

function formatSize(bytes) {
  if (!bytes) return '-'
  const units = ['B', 'KB', 'MB', 'GB']
  let i = 0
  while (bytes >= 1024 && i < units.length - 1) { bytes /= 1024; i++ }
  return `${bytes.toFixed(i > 0 ? 1 : 0)} ${units[i]}`
}

function formatDate(iso){if(!iso)return'-';const d=new Date(iso+'Z');const p=n=>String(n).padStart(2,'0');return`${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`}

async function loadSharedFile() {
  const token = route.params.token
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || '/api'
    const res = await fetch(`${API_BASE}/share/${token}`)
    if (!res.ok) {
      error.value = '链接无效或已过期'
      return
    }
    const data = await res.json()
    resource.value = data
    if (data.is_folder) {
      children.value = data.children || []
    }
  } catch {
    error.value = '网络错误，请稍后重试'
  } finally {
    loading.value = false
  }
}

async function loadFolderContents(folderId, name) {
  const token = route.params.token
  try {
    const API_BASE = import.meta.env.VITE_API_BASE || '/api'
    const res = await fetch(`${API_BASE}/share/${folderId}/items?token=${token}`)
    if (!res.ok) throw new Error()
    const data = await res.json()
    children.value = data.items || []
    breadcrumb.value.push({ id: folderId, name: name || data.name })
  } catch {
    alert('加载失败')
  }
}

function navigateTo(item) {
  if (item.share_token) {
    window.location.href = `/share/${item.share_token}`
    return
  }
  loadFolderContents(item.id, item.name)
}

function goToTop() {
  breadcrumb.value = []
  loadSharedFile()
}

function handleDownload() {
  if (!resource.value?.file_url) return
  const a = document.createElement('a')
  a.href = resource.value.file_url
  a.download = resource.value.name
  a.click()
}

function downloadItem(item) {
  if (!item.file_url) return
  const a = document.createElement('a')
  a.href = item.file_url
  a.download = item.name
  a.click()
}

function openItem(item) {
  const ext = (item.file_ext || '').toLowerCase()
  const imgExts = ['jpg','jpeg','png','gif','webp','svg']
  if (imgExts.includes(ext) || ext === 'pdf') {
    resource.value = { ...item, is_folder: false }
    previewing.value = true
  } else {
    downloadItem(item)
  }
}

onMounted(loadSharedFile)
</script>

<style scoped>
.page-view { padding: 80px 0 60px; min-height: 100vh; display: flex; align-items: flex-start; justify-content: center; }
.container { width: 100%; max-width: 640px; margin: 0 auto; padding: 0 24px; }

.share-loading { color: var(--text-muted); padding: 48px 0; text-align: center; }
.share-error { padding: 48px 0; text-align: center; }
.share-error h2 { font-family: var(--font-heading); font-size: 20px; margin-bottom: 8px; }
.share-error p { color: var(--text-muted); margin-bottom: 20px; }

/* 面包屑 */
.share-breadcrumb { display: flex; align-items: center; gap: 6px; margin-bottom: 16px; font-size: 13px; }
.breadcrumb-item { color: var(--text-muted); cursor: pointer; }
.breadcrumb-item:hover { color: var(--warm-terracotta); }
.breadcrumb-item.active { color: var(--text-primary); font-weight: 500; }
.breadcrumb-sep { color: var(--text-muted); font-size: 11px; }

/* 文件卡片 */
.share-card { background: white; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 32px; box-shadow: var(--shadow-md); text-align: center; }
.share-icon { margin-bottom: 16px; }
.share-name { font-family: var(--font-heading); font-size: 20px; margin: 0 0 12px; word-break: break-all; }
.share-meta-row { display: flex; justify-content: center; gap: 16px; font-size: 13px; color: var(--text-muted); margin-bottom: 16px; flex-wrap: wrap; }
.share-desc { font-size: 14px; color: var(--text-secondary); line-height: 1.6; margin-bottom: 20px; text-align: left; }
.share-actions { display: flex; justify-content: center; gap: 8px; }

/* 预览 */
.share-preview-card { background: white; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-md); }
.preview-img { width: 100%; max-height: 60vh; object-fit: contain; display: block; background: #1a1a1a; }
.preview-pdf { width: 100%; height: 60vh; border: none; }
.preview-meta { padding: 20px; text-align: center; }

/* 文件夹 */
.share-folder-card { text-align: left; }
.share-folder-title { font-family: var(--font-heading); font-size: 20px; margin: 0 0 12px; }
.share-folder-list { display: flex; flex-direction: column; gap: 6px; margin-top: 16px; }
.share-folder-item { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border: 1px solid var(--glass-border); border-radius: var(--radius-md); cursor: pointer; transition: all 0.15s; }
.share-folder-item:hover { background: var(--bg-soft); border-color: var(--warm-terracotta); }
.item-icon { flex-shrink: 0; }
.item-name { flex: 1; font-size: 13px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.item-size { font-size: 11px; color: var(--text-muted); }

/* 页脚 */
.share-footer { font-size: 12px; color: var(--text-muted); margin-top: 20px; text-align: center; }

/* 按钮 */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px; padding: 8px 20px; border-radius: 999px; font-size: 13px; font-weight: 600; cursor: pointer; border: none; transition: all 0.2s; }
.btn-primary { background: var(--grad-primary); color: white; }
.btn-primary:hover { opacity: 0.9; }
.btn-outline { background: transparent; border: 1.5px solid var(--glass-border); color: var(--text-primary); }
.btn-outline:hover { border-color: var(--warm-terracotta); color: var(--warm-terracotta); }
.btn-sm { padding: 6px 14px; font-size: 12px; }
.btn-xs { padding: 4px 10px; font-size: 11px; }
</style>
