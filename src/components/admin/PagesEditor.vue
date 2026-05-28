<template>
  <div class="pages-editor">
    <div class="pages-list">
      <div class="list-header">
        <h3>页面列表</h3>
      </div>
      <button
        v-for="p in pages"
        :key="p.slug"
        class="page-item"
        :class="{ active: selectedSlug === p.slug }"
        @click="selectPage(p.slug)"
      >
        <span class="page-slug">/{{ p.slug }}</span>
        <span class="page-title">{{ p.title }}</span>
      </button>
    </div>

    <div class="pages-detail" v-if="selectedPage">
      <div class="detail-header">
        <div class="detail-info">
          <h3>{{ selectedPage.title }}</h3>
          <span class="detail-slug">/{{ selectedPage.slug }}</span>
        </div>
        <div class="detail-actions">
          <div class="mode-toggle">
            <button :class="{ active: editMode === 'visual' }" @click="editMode = 'visual'">可视化</button>
            <button :class="{ active: editMode === 'json' }" @click="editMode = 'json'">JSON</button>
          </div>
          <button class="btn btn-outline btn-sm" @click="$emit('reset', selectedPage.slug)">重置默认</button>
          <button class="btn btn-primary btn-sm" :disabled="!pageDirty" @click="savePage">保存</button>
        </div>
      </div>

      <!-- JSON 模式 -->
      <div v-if="editMode === 'json'" class="json-editor">
        <textarea v-model="jsonText" rows="20" class="json-textarea" :class="{ 'json-error': jsonError }"></textarea>
        <p v-if="jsonError" class="json-error-msg">{{ jsonError }}</p>
      </div>

      <!-- 可视化模式 -->
      <div v-else class="visual-editor">
        <component :is="pageEditorComponent" v-if="pageEditorComponent" :content="editContent" @update="onVisualUpdate" />
        <GenericPageEditor v-else :content="editContent" @update="onVisualUpdate" />
      </div>
    </div>

    <div v-else class="pages-empty">
      <p>选择一个页面开始编辑</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import GenericPageEditor from './pages/GenericPageEditor.vue'
import AboutPageEditor from './pages/AboutPageEditor.vue'
import MembersPageEditor from './pages/MembersPageEditor.vue'
import ProjectsPageEditor from './pages/ProjectsPageEditor.vue'
import BlogPageEditor from './pages/BlogPageEditor.vue'
import JoinPageEditor from './pages/JoinPageEditor.vue'

const props = defineProps({ pages: Array })
const emit = defineEmits(['update', 'reset'])

const selectedSlug = ref(null)
const editMode = ref('visual')
const editContent = ref(null)
const jsonText = ref('')
const jsonError = ref('')
const pageDirty = ref(false)

const pageEditors = {
  about: AboutPageEditor,
  members: MembersPageEditor,
  projects: ProjectsPageEditor,
  blog: BlogPageEditor,
  join: JoinPageEditor,
}

const selectedPage = computed(() => props.pages.find((p) => p.slug === selectedSlug.value))
const pageEditorComponent = computed(() => pageEditors[selectedSlug.value] || null)

function selectPage(slug) {
  selectedSlug.value = slug
  const page = props.pages.find((p) => p.slug === slug)
  editContent.value = JSON.parse(JSON.stringify(page?.content || {}))
  jsonText.value = JSON.stringify(editContent.value, null, 2)
  jsonError.value = ''
  pageDirty.value = false
}

watch(editMode, (mode) => {
  if (mode === 'json') {
    jsonText.value = JSON.stringify(editContent.value, null, 2)
    jsonError.value = ''
  }
})

function onVisualUpdate(newContent) {
  editContent.value = newContent
  pageDirty.value = true
}

function savePage() {
  if (editMode.value === 'json') {
    try {
      const parsed = JSON.parse(jsonText.value)
      editContent.value = parsed
      jsonError.value = ''
    } catch (e) {
      jsonError.value = 'JSON 格式错误: ' + e.message
      return
    }
  }
  emit('update', { slug: selectedSlug.value, data: { content: editContent.value } })
  pageDirty.value = false
}
</script>

<style scoped>
.pages-editor { display: flex; gap: 20px; min-height: 600px; }

.pages-list { width: 240px; flex-shrink: 0; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); overflow: hidden; }
.list-header { padding: 16px; border-bottom: 1px solid var(--glass-border); }
.list-header h3 { font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin: 0; }
.page-item { display: block; width: 100%; padding: 12px 16px; border: none; background: none; text-align: left; cursor: pointer; border-bottom: 1px solid var(--glass-border); transition: background 0.15s; }
.page-item:hover { background: var(--bg-soft); }
.page-item.active { background: rgba(192, 96, 64, 0.08); }
.page-slug { display: block; font-size: 12px; font-family: var(--font-mono); color: var(--text-muted); }
.page-title { display: block; font-size: 13px; color: var(--text-primary); margin-top: 2px; }

.pages-detail { flex: 1; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 24px; min-width: 0; }
.detail-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.detail-info h3 { font-family: var(--font-heading); font-size: 16px; margin: 0; }
.detail-slug { font-size: 12px; font-family: var(--font-mono); color: var(--text-muted); }
.detail-actions { display: flex; align-items: center; gap: 8px; }

.mode-toggle { display: flex; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); overflow: hidden; }
.mode-toggle button { padding: 6px 14px; border: none; background: white; font-size: 12px; cursor: pointer; color: var(--text-secondary); transition: all 0.15s; }
.mode-toggle button.active { background: var(--warm-terracotta); color: white; }
.mode-toggle button:not(:last-child) { border-right: 1px solid var(--glass-border); }

.json-textarea { width: 100%; padding: 16px; border: 1px solid var(--glass-border); border-radius: var(--radius-md); font-family: var(--font-mono); font-size: 13px; line-height: 1.6; resize: vertical; background: var(--bg-soft); color: var(--text-primary); }
.json-textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.json-textarea.json-error { border-color: #e05050; }
.json-error-msg { color: #e05050; font-size: 12px; margin-top: 8px; }

.pages-empty { flex: 1; display: flex; align-items: center; justify-content: center; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); color: var(--text-muted); font-size: 14px; }

.btn-sm { padding: 6px 14px; font-size: 12px; }

@media (max-width: 768px) {
  .pages-editor { flex-direction: column; min-height: auto; }
  .pages-list { width: 100%; max-height: 200px; overflow-y: auto; }
  .pages-detail { padding: 16px; }
  .detail-header { flex-direction: column; align-items: flex-start; }
  .detail-actions { width: 100%; flex-wrap: wrap; }
}
</style>
