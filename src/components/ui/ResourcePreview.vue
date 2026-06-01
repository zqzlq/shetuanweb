<template>
  <Teleport to="body">
    <div v-if="show" class="preview-overlay" @click.self="close">
      <div class="preview-modal">
        <!-- 顶栏 -->
        <div class="preview-header">
          <div class="preview-info">
            <span class="preview-type" :class="'type-' + (previewData?.type || 'unknown')">
              {{ fileTypeLabel }}
            </span>
            <span class="preview-title">{{ resource?.title }}</span>
            <span class="preview-meta">{{ resource?.file_name }} · {{ formatFileSize(resource?.file_size) }}</span>
          </div>
          <div class="preview-actions">
            <button class="btn btn-outline btn-sm" @click="handleDownload" :disabled="downloading">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
              {{ downloading ? '下载中...' : '下载' }}
            </button>
            <button class="preview-close" @click="close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>
          </div>
        </div>

        <!-- 内容区 -->
        <div class="preview-body">
          <!-- 加载中 -->
          <div v-if="loading" class="preview-loading">
            <div class="spinner"></div>
            <span>加载预览...</span>
          </div>

          <!-- 图片预览 -->
          <div v-else-if="previewData?.type === 'image'" class="preview-image-wrap">
            <img :src="previewData.url" :alt="resource?.title" @load="loading = false" />
          </div>

          <!-- PDF 预览 -->
          <div v-else-if="previewData?.type === 'pdf'" class="preview-pdf-wrap">
            <div class="pdf-toolbar">
              <button :disabled="pdfPage <= 1" @click="pdfPage--; renderPdfPage()">上一页</button>
              <span>{{ pdfPage }} / {{ pdfTotalPages }}</span>
              <button :disabled="pdfPage >= pdfTotalPages" @click="pdfPage++; renderPdfPage()">下一页</button>
            </div>
            <canvas ref="pdfCanvas" class="pdf-canvas"></canvas>
          </div>

          <!-- Markdown 预览 -->
          <div v-else-if="previewData?.type === 'markdown'" class="preview-md-wrap">
            <div v-if="previewData.content" class="md-content markdown-body" v-html="renderedMarkdown"></div>
            <div v-else-if="previewData.url" class="preview-loading">
              <button class="btn btn-outline btn-sm" @click="fetchTextContent(previewData.url)">加载内容</button>
            </div>
          </div>

          <!-- HTML 预览 (DOCX) -->
          <div v-else-if="previewData?.type === 'html'" class="preview-html-wrap">
            <div v-if="previewData.content" class="html-content" v-html="previewData.content"></div>
            <div v-else-if="previewData.url" class="preview-loading">
              <button class="btn btn-outline btn-sm" @click="loadDocx">加载内容</button>
            </div>
          </div>

          <!-- 文本/代码预览 -->
          <div v-else-if="previewData?.type === 'text'" class="preview-text-wrap">
            <pre v-if="previewData.content" class="text-content"><code>{{ previewData.content }}</code></pre>
            <div v-else-if="previewData.url" class="preview-loading">
              <button class="btn btn-outline btn-sm" @click="fetchTextContent(previewData.url)">加载内容</button>
            </div>
          </div>

          <!-- 不支持的格式 -->
          <div v-else class="preview-unsupported">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>
            <h3>暂不支持预览此格式</h3>
            <p>{{ resource?.file_type?.toUpperCase() }} 格式文件请下载后查看</p>
            <button class="btn btn-primary" @click="handleDownload">下载文件</button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { previewResource, downloadResource } from '@/services/api'
import { marked } from 'marked'

const props = defineProps({
  show: Boolean,
  resource: Object,
})
const emit = defineEmits(['close', 'download'])

const loading = ref(false)
const downloading = ref(false)
const previewData = ref(null)
const pdfPage = ref(1)
const pdfTotalPages = ref(0)
const pdfCanvas = ref(null)
let pdfDoc = null

marked.setOptions({ breaks: true })

const renderedMarkdown = computed(() => {
  if (previewData.value?.content) {
    return marked(previewData.value.content)
  }
  return ''
})

const fileTypeLabel = computed(() => {
  const type = previewData.value?.type
  if (type === 'image') return '图片'
  if (type === 'pdf') return 'PDF'
  if (type === 'markdown') return 'Markdown'
  if (type === 'html') return '文档'
  if (type === 'text') return '文本'
  return props.resource?.file_type?.toUpperCase() || '文件'
})

watch(() => props.show, async (val) => {
  if (val && props.resource) {
    await loadPreview()
  } else {
    previewData.value = null
    pdfDoc = null
    pdfPage.value = 1
    pdfTotalPages.value = 0
  }
})

async function loadPreview() {
  loading.value = true
  previewData.value = null
  try {
    const data = await previewResource(props.resource.id)
    previewData.value = data

    if (data.type === 'pdf' && data.url) {
      await nextTick()
      await loadPdf(data.url)
    }
  } catch (e) {
    console.error('预览加载失败', e)
    previewData.value = { type: 'unsupported' }
  } finally {
    loading.value = false
  }
}

async function loadPdf(url) {
  try {
    const pdfjsLib = await import('pdfjs-dist')
    pdfjsLib.GlobalWorkerOptions.workerSrc = new URL('pdfjs-dist/build/pdf.worker.min.mjs', import.meta.url).href

    const loadingTask = pdfjsLib.getDocument(url)
    pdfDoc = await loadingTask.promise
    pdfTotalPages.value = pdfDoc.numPages
    pdfPage.value = 1
    await renderPdfPage()
  } catch (e) {
    console.error('PDF 加载失败', e)
    previewData.value = { type: 'unsupported' }
  }
}

async function renderPdfPage() {
  if (!pdfDoc || !pdfCanvas.value) return
  const page = await pdfDoc.getPage(pdfPage.value)
  const scale = 1.5
  const viewport = page.getViewport({ scale })

  const canvas = pdfCanvas.value
  const context = canvas.getContext('2d')
  canvas.height = viewport.height
  canvas.width = viewport.width

  await page.render({ canvasContext: context, viewport }).promise
}

async function fetchTextContent(url) {
  try {
    const res = await fetch(url)
    const text = await res.text()
    if (previewData.value) {
      previewData.value = { ...previewData.value, content: text.slice(0, 50000) }
    }
  } catch (e) {
    console.error('内容加载失败', e)
  }
}

async function loadDocx() {
  try {
    const mammoth = await import('mammoth')
    const res = await fetch(props.resource.file_url)
    const arrayBuffer = await res.arrayBuffer()
    const result = await mammoth.convertToHtml({ arrayBuffer })
    if (previewData.value) {
      previewData.value = { ...previewData.value, content: result.value }
    }
  } catch (e) {
    console.error('DOCX 加载失败', e)
  }
}

async function handleDownload() {
  downloading.value = true
  try {
    const result = await downloadResource(props.resource.id)
    const a = document.createElement('a')
    a.href = result.file_url
    a.download = result.file_name
    a.target = '_blank'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    emit('download', result)
  } catch (e) {
    alert('下载失败: ' + (e.message || '未知错误'))
  } finally {
    downloading.value = false
  }
}

function close() {
  emit('close')
}

function formatFileSize(bytes) {
  if (!bytes) return ''
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}
</script>

<style scoped>
.preview-overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0, 0, 0, 0.6);
  display: flex; align-items: center; justify-content: center;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.preview-modal {
  background: #fff; border-radius: var(--radius-xl);
  width: 100%; max-width: 960px; max-height: 90vh;
  display: flex; flex-direction: column;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.preview-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 24px; border-bottom: 1px solid var(--glass-border);
  flex-shrink: 0;
}

.preview-info { display: flex; align-items: center; gap: 12px; min-width: 0; }
.preview-type {
  font-size: 11px; font-weight: 700; padding: 3px 10px;
  border-radius: 999px; white-space: nowrap;
  background: rgba(192, 96, 64, 0.1); color: var(--warm-terracotta);
}
.type-image { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
.type-pdf { background: rgba(239, 68, 68, 0.1); color: #ef4444; }
.type-markdown { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.type-html { background: rgba(168, 85, 247, 0.1); color: #a855f7; }
.type-text { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }

.preview-title {
  font-family: var(--font-heading); font-weight: 600; font-size: 15px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.preview-meta { font-size: 12px; color: var(--text-muted); white-space: nowrap; }

.preview-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.preview-close {
  width: 32px; height: 32px; border: none; background: none;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  border-radius: 8px; color: var(--text-secondary); transition: all 0.15s;
}
.preview-close:hover { background: var(--bg-soft); color: var(--text-primary); }
.btn-sm { padding: 6px 14px; font-size: 12px; }

.preview-body {
  flex: 1; overflow: auto; min-height: 0;
}

/* Loading */
.preview-loading {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 12px; padding: 60px 20px;
  color: var(--text-muted); font-size: 14px;
}
.spinner {
  width: 32px; height: 32px; border: 3px solid var(--glass-border);
  border-top-color: var(--warm-terracotta); border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Image */
.preview-image-wrap {
  display: flex; align-items: center; justify-content: center;
  padding: 20px; min-height: 300px; background: #f8f8f8;
}
.preview-image-wrap img {
  max-width: 100%; max-height: calc(90vh - 120px);
  object-fit: contain; border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* PDF */
.preview-pdf-wrap { display: flex; flex-direction: column; align-items: center; }
.pdf-toolbar {
  display: flex; align-items: center; gap: 16px;
  padding: 12px 20px; border-bottom: 1px solid var(--glass-border);
  width: 100%;
}
.pdf-toolbar button {
  padding: 4px 12px; border: 1px solid var(--glass-border);
  border-radius: 6px; background: white; font-size: 12px;
  cursor: pointer; transition: all 0.15s;
}
.pdf-toolbar button:hover:not(:disabled) { border-color: var(--warm-terracotta); }
.pdf-toolbar button:disabled { opacity: 0.4; cursor: not-allowed; }
.pdf-toolbar span { font-size: 13px; color: var(--text-secondary); }
.pdf-canvas {
  max-width: 100%; padding: 20px;
}

/* Markdown */
.preview-md-wrap { padding: 24px; }
.md-content { font-size: 14px; line-height: 1.8; }
.md-content :deep(h1) { font-size: 1.8em; margin: 0.8em 0 0.4em; }
.md-content :deep(h2) { font-size: 1.4em; margin: 0.8em 0 0.4em; }
.md-content :deep(h3) { font-size: 1.2em; margin: 0.6em 0 0.3em; }
.md-content :deep(p) { margin: 0.5em 0; }
.md-content :deep(code) {
  background: var(--bg-soft); padding: 2px 6px; border-radius: 4px;
  font-size: 0.9em; font-family: monospace;
}
.md-content :deep(pre) {
  background: #1e1e2e; color: #cdd6f4; padding: 16px;
  border-radius: 8px; overflow-x: auto; margin: 12px 0;
}
.md-content :deep(pre code) { background: none; padding: 0; color: inherit; }
.md-content :deep(blockquote) {
  border-left: 3px solid var(--warm-terracotta);
  padding-left: 16px; margin: 12px 0; color: var(--text-secondary);
}
.md-content :deep(img) { max-width: 100%; border-radius: 8px; }
.md-content :deep(table) { border-collapse: collapse; width: 100%; margin: 12px 0; }
.md-content :deep(th), .md-content :deep(td) {
  padding: 8px 12px; border: 1px solid var(--glass-border); text-align: left;
}

/* HTML (DOCX) */
.preview-html-wrap { padding: 24px; }
.html-content { font-size: 14px; line-height: 1.8; }
.html-content :deep(img) { max-width: 100%; height: auto; }
.html-content :deep(table) { border-collapse: collapse; width: 100%; }
.html-content :deep(th), .html-content :deep(td) {
  padding: 8px 12px; border: 1px solid var(--glass-border);
}

/* Text/Code */
.preview-text-wrap { padding: 0; }
.text-content {
  margin: 0; padding: 24px; font-size: 13px; line-height: 1.7;
  font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
  background: #1e1e2e; color: #cdd6f4;
  overflow: auto; max-height: calc(90vh - 120px);
  white-space: pre-wrap; word-break: break-all;
}

/* Unsupported */
.preview-unsupported {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 12px; padding: 80px 20px;
  color: var(--text-muted);
}
.preview-unsupported svg { color: var(--glass-border); }
.preview-unsupported h3 { font-family: var(--font-heading); font-size: 16px; color: var(--text-primary); margin: 0; }
.preview-unsupported p { font-size: 13px; margin: 0 0 16px; }

@media (max-width: 768px) {
  .preview-overlay { padding: 10px; }
  .preview-modal { max-width: 100%; max-height: 95vh; }
  .preview-header { padding: 12px 16px; flex-wrap: wrap; gap: 8px; }
  .preview-info { flex-wrap: wrap; gap: 8px; }
  .preview-meta { display: none; }
}
</style>
