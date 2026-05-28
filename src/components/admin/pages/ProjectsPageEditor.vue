<template>
  <div class="page-editor">
    <div class="editor-card">
      <h3 class="editor-title">Hero</h3>
      <div class="field-grid">
        <label class="field"><span>角标</span><input :value="content.hero?.eyebrow" @input="updateHero('eyebrow', $event.target.value)" /></label>
        <label class="field"><span>标题</span><input :value="content.hero?.title" @input="updateHero('title', $event.target.value)" /></label>
        <label class="field full"><span>副标题</span><textarea :value="content.hero?.subtitle" @input="updateHero('subtitle', $event.target.value)" rows="2"></textarea></label>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header"><h3 class="editor-title">项目列表</h3><button class="btn btn-outline btn-xs" @click="addProject">+ 添加</button></div>
      <div v-for="(p, i) in content.projects || []" :key="i" class="list-item" :ref="el => { if (el) projectRefs.value[i] = el }">
        <div class="list-item-header">
          <span class="item-index">{{ p.name || '#' + (i+1) }}</span>
          <span class="sort-btns">
            <button class="btn-icon" :disabled="i === 0" @click="moveProject(i, -1)" title="上移">&#8593;</button>
            <button class="btn-icon" :disabled="i === (content.projects?.length || 0) - 1" @click="moveProject(i, 1)" title="下移">&#8595;</button>
            <button class="btn-icon" @click="removeProject(i)">&times;</button>
          </span>
        </div>
        <div class="field-grid">
          <label class="field"><span>名称</span><input :value="p.name" @input="updateProject(i, 'name', $event.target.value)" /></label>
          <label class="field"><span>Slug</span><input :value="p.slug" @input="updateProject(i, 'slug', $event.target.value)" /></label>
          <label class="field"><span>分类</span><input :value="p.category" @input="updateProject(i, 'category', $event.target.value)" /></label>
          <label class="field"><span>封面样式</span><input :value="p.coverClass" @input="updateProject(i, 'coverClass', $event.target.value)" /></label>
          <label class="field"><span>GitHub</span><input :value="p.githubUrl" @input="updateProject(i, 'githubUrl', $event.target.value)" /></label>
          <label class="field"><span>状态</span><input :value="p.status" @input="updateProject(i, 'status', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="p.description" @input="updateProject(i, 'description', $event.target.value)" rows="2"></textarea></label>
          <label class="field full"><span>详细描述（Markdown）</span><MarkdownEditorField :modelValue="p.longDescription || ''" @update:modelValue="updateProject(i, 'longDescription', $event)" /></label>
          <label class="field full"><span>封面图片</span><ImageUploadField :modelValue="p.coverImage || ''" @update:modelValue="updateProject(i, 'coverImage', $event)" /></label>
          <label class="field full"><span>项目截图</span><MultiImageUploadField :modelValue="p.screenshots || []" @update:modelValue="updateProject(i, 'screenshots', $event)" /></label>
          <label class="field"><span>技术栈（逗号分隔）</span><input :value="p.techStack?.join(', ')" @input="updateProject(i, 'techStack', $event.target.value.split(',').map(s=>s.trim()).filter(Boolean))" /></label>
          <label class="field"><span>链接</span><input :value="p.link" @input="updateProject(i, 'link', $event.target.value)" /></label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { nextTick, ref } from 'vue'
import ImageUploadField from '../ImageUploadField.vue'
import MultiImageUploadField from '../MultiImageUploadField.vue'
import MarkdownEditorField from '../MarkdownEditorField.vue'
const props = defineProps({ content: Object })
const emit = defineEmits(['update'])
const c = () => props.content
const up = (val) => emit('update', val)

const projectRefs = ref([])

function updateHero(k, v) { up({ ...c(), hero: { ...c().hero, [k]: v } }) }

function updateProject(i, k, v) {
  const projects = [...(c().projects || [])]
  projects[i] = { ...projects[i], [k]: v }
  up({ ...c(), projects })
}
function addProject() {
  up({ ...c(), projects: [...(c().projects || []), { name: '', slug: '', category: '', description: '', longDescription: '', coverClass: 'aurora', coverImage: '', screenshots: [], githubUrl: '', techStack: [], status: 'wip', featured: false, link: '' }] })
  nextTick(() => { const refs = projectRefs.value; refs[refs.length - 1]?.scrollIntoView({ behavior: 'smooth', block: 'center' }) })
}
function removeProject(i) { up({ ...c(), projects: (c().projects || []).filter((_, idx) => idx !== i) }) }
function moveProject(i, dir) {
  const projects = [...(c().projects || [])]; const j = i + dir
  if (j < 0 || j >= projects.length) return;[projects[i], projects[j]] = [projects[j], projects[i]]
  up({ ...c(), projects })
}
</script>

<style scoped>
.page-editor { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: var(--bg-soft); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 20px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.editor-title { font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin: 0 0 12px; }
.card-header .editor-title { margin: 0; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 11px; font-weight: 500; color: var(--text-muted); margin-bottom: 3px; }
.field input, .field textarea { width: 100%; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.list-item { border: 1px solid var(--glass-border); border-radius: 8px; padding: 12px; margin-top: 8px; background: white; }
.list-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.item-index { font-size: 11px; font-weight: 600; color: var(--text-muted); }
.btn-icon { width: 24px; height: 24px; border: 1px solid var(--glass-border); border-radius: 4px; background: white; color: var(--text-muted); font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-icon:disabled { opacity: 0.3; cursor: not-allowed; }
.sort-btns { display: flex; gap: 4px; }
.btn-xs { padding: 3px 10px; font-size: 11px; }

@media (max-width: 768px) {
  .editor-card { padding: 12px; }
  .field-grid { grid-template-columns: 1fr; }
  .list-item { padding: 10px; }
}
</style>
