<template>
  <div class="editor-section">
    <div class="editor-card">
      <h3 class="editor-title">产品展示</h3>
      <div class="field-grid">
        <label class="field full">
          <span>标题</span>
          <input :value="modelValue.title" @input="update('title', $event.target.value)" />
        </label>
        <label class="field full">
          <span>描述</span>
          <textarea :value="modelValue.description" @input="update('description', $event.target.value)" rows="2"></textarea>
        </label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">分类标签</h3>
      <div class="inline-row" v-for="(cat, i) in modelValue.categories" :key="i">
        <input :value="cat" @input="updateCat(i, $event.target.value)" class="w-200" />
        <button v-if="i > 0" class="btn-icon" @click="removeCat(i)">&times;</button>
        <span v-else class="cat-lock-hint">精选</span>
      </div>
      <button class="btn btn-outline btn-xs" @click="addCat" style="margin-top:8px">+ 添加分类</button>
    </div>

    <div class="editor-card" v-for="(slide, si) in modelValue.slides" :key="si">
      <div class="card-header">
        <h3 class="editor-title">轮播：{{ slide.tag || '#' + (si + 1) }}</h3>
        <span v-if="si === 0" class="cat-lock-hint">精选总览轮播</span>
      </div>
      <div class="field-grid">
        <label class="field">
          <span>标签</span>
          <input :value="slide.tag" @input="updateSlide(si, 'tag', $event.target.value)" :disabled="si === 0" />
        </label>
        <label class="field">
          <span>标题</span>
          <input :value="slide.title" @input="updateSlide(si, 'title', $event.target.value)" />
        </label>
        <label class="field full">
          <span>描述</span>
          <textarea :value="slide.description" @input="updateSlide(si, 'description', $event.target.value)" rows="2"></textarea>
        </label>
      </div>

      <div class="sub-section">
        <div class="card-header">
          <h4 class="sub-title">项目列表</h4>
          <div class="add-project-wrap">
            <select class="project-select" @change="addProjectFromPool(si, $event)">
              <option value="">从项目库添加...</option>
              <option v-for="p in availableProjects(si)" :key="p.slug" :value="p.slug">{{ p.name }}</option>
            </select>
            <button class="btn btn-outline btn-xs" @click="addProject(si)">+ 手动添加</button>
          </div>
        </div>
        <div v-for="(proj, pi) in slide.projects" :key="pi" class="list-item" :ref="el => { if (!projectRefs.value[si]) projectRefs.value[si] = []; if (el) projectRefs.value[si][pi] = el }">
          <div class="list-item-header">
            <span class="item-index">{{ proj.name || '#' + (pi + 1) }}</span>
            <span class="sort-btns">
              <button class="btn-icon" :disabled="pi === 0" @click="moveProject(si, pi, -1)" title="上移">&#8593;</button>
              <button class="btn-icon" :disabled="pi === slide.projects.length - 1" @click="moveProject(si, pi, 1)" title="下移">&#8595;</button>
              <button class="btn-icon" @click="removeProject(si, pi)">&times;</button>
            </span>
          </div>
          <div class="field-grid">
            <label class="field">
              <span>名称</span>
              <input :value="proj.name" @input="updateProject(si, pi, 'name', $event.target.value)" />
            </label>
            <label class="field">
              <span>Slug</span>
              <input :value="proj.slug" @input="updateProject(si, pi, 'slug', $event.target.value)" />
            </label>
            <label class="field">
              <span>分类</span>
              <input :value="proj.category" @input="updateProject(si, pi, 'category', $event.target.value)" />
            </label>
            <label class="field">
              <span>封面样式</span>
              <input :value="proj.coverClass" @input="updateProject(si, pi, 'coverClass', $event.target.value)" />
            </label>
            <label class="field full">
              <span>描述</span>
              <textarea :value="proj.description" @input="updateProject(si, pi, 'description', $event.target.value)" rows="2"></textarea>
            </label>
            <label class="field full">
              <span>封面图片</span>
              <ImageUploadField :modelValue="proj.coverImage || ''" @update:modelValue="updateProject(si, pi, 'coverImage', $event)" />
            </label>
            <label class="field">
              <span>链接</span>
              <input :value="proj.link" @input="updateProject(si, pi, 'link', $event.target.value)" />
            </label>
            <label class="field">
              <span>技术栈（逗号分隔）</span>
              <input :value="proj.techStack?.join(', ')" @input="updateProject(si, pi, 'techStack', $event.target.value.split(',').map(s => s.trim()).filter(Boolean))" />
            </label>
            <label class="field">
              <span>
                <label class="checkbox-label">
                  <input type="checkbox" :checked="proj.featured" @change="updateProject(si, pi, 'featured', $event.target.checked)" />
                  精选项目
                </label>
              </span>
            </label>
          </div>
          <div class="contributors-editor">
            <div class="contributors-header">
              <span class="sub-title">贡献者</span>
              <button class="btn btn-outline btn-xs" @click="addContributor(si, pi)">+ 添加</button>
            </div>
            <div v-for="(contrib, ci) in proj.contributors || []" :key="ci" class="contrib-row">
              <input :value="contrib.name" @input="updateContributor(si, pi, ci, 'name', $event.target.value)" placeholder="姓名" class="contrib-input" />
              <input :value="contrib.role" @input="updateContributor(si, pi, ci, 'role', $event.target.value)" placeholder="角色" class="contrib-input" />
              <button class="btn-icon btn-icon-sm" @click="removeContributor(si, pi, ci)">&times;</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { nextTick, ref } from 'vue'
import ImageUploadField from '../ImageUploadField.vue'
const props = defineProps({
  modelValue: Object,
  allProjects: { type: Array, default: () => [] }
})
const emit = defineEmits(['update:modelValue'])

const projectRefs = ref({})

function emitVal(val) { emit('update:modelValue', val) }
function update(key, value) { emitVal({ ...props.modelValue, [key]: value }) }

// ── 分类与轮播同步 ──

function updateCat(i, value) {
  const categories = [...props.modelValue.categories]
  const oldValue = categories[i]
  categories[i] = value
  const slides = props.modelValue.slides.map(s => ({
    ...s,
    tag: s.tag === oldValue ? value : s.tag,
    projects: s.projects.map(p => p.category === oldValue ? { ...p, category: value } : p)
  }))
  emitVal({ ...props.modelValue, categories, slides })
}

function addCat() {
  const categories = [...props.modelValue.categories, '']
  const slides = [...props.modelValue.slides, { tag: '', title: '', description: '', metrics: [], projects: [] }]
  emitVal({ ...props.modelValue, categories, slides })
}

function removeCat(i) {
  if (i === 0) return
  const categories = props.modelValue.categories.filter((_, idx) => idx !== i)
  const slides = props.modelValue.slides.filter((_, idx) => idx !== i)
  emitVal({ ...props.modelValue, categories, slides })
}

// ── 轮播 ──

function updateSlide(si, key, value) {
  const slides = [...props.modelValue.slides]
  slides[si] = { ...slides[si], [key]: value }
  emitVal({ ...props.modelValue, slides })
}

// ── 项目管理 ──

function availableProjects(si) {
  const existingSlugs = new Set((props.modelValue.slides[si]?.projects || []).map(p => p.slug))
  return props.allProjects.filter(p => p.slug && !existingSlugs.has(p.slug))
}

function addProjectFromPool(si, event) {
  const slug = event.target.value
  if (!slug) return
  const source = props.allProjects.find(p => p.slug === slug)
  if (!source) return
  const slides = [...props.modelValue.slides]
  slides[si] = {
    ...slides[si],
    projects: [...slides[si].projects, {
      name: source.name || '',
      slug: source.slug || '',
      category: source.category || '',
      description: source.description || '',
      longDescription: source.longDescription || '',
      link: source.link || '',
      coverClass: source.coverClass || 'aurora',
      coverImage: source.coverImage || '',
      techStack: source.techStack || [],
      githubUrl: source.githubUrl || '',
      demoUrl: source.demoUrl || '',
      status: source.status || 'active',
      featured: source.featured || false,
      screenshots: source.screenshots || [],
      contributors: source.contributors || []
    }]
  }
  emitVal({ ...props.modelValue, slides })
  event.target.value = ''
  nextTick(() => { const refs = projectRefs.value[si]; refs?.[refs.length - 1]?.scrollIntoView({ behavior: 'smooth', block: 'center' }) })
}

function addProject(si) {
  const slides = [...props.modelValue.slides]
  slides[si] = { ...slides[si], projects: [...slides[si].projects, { name: '', slug: '', category: '', description: '', link: '', coverClass: 'aurora', techStack: [], featured: false, contributors: [] }] }
  emitVal({ ...props.modelValue, slides })
  nextTick(() => { const refs = projectRefs.value[si]; refs?.[refs.length - 1]?.scrollIntoView({ behavior: 'smooth', block: 'center' }) })
}

function removeProject(si, pi) {
  const slides = [...props.modelValue.slides]
  slides[si] = { ...slides[si], projects: slides[si].projects.filter((_, i) => i !== pi) }
  emitVal({ ...props.modelValue, slides })
}

function moveProject(si, pi, dir) {
  const slides = props.modelValue.slides.map(s => ({ ...s, projects: [...s.projects] }))
  const pj = pi + dir
  if (pj < 0 || pj >= slides[si].projects.length) return
  ;[slides[si].projects[pi], slides[si].projects[pj]] = [slides[si].projects[pj], slides[si].projects[pi]]
  emitVal({ ...props.modelValue, slides })
}

function updateProject(si, pi, key, value) {
  let slides = props.modelValue.slides.map(s => ({ ...s, projects: [...s.projects] }))
  slides[si].projects[pi] = { ...slides[si].projects[pi], [key]: value }

  // 精选状态跨分类同步：同一 slug 的项目在所有分类下保持一致
  if (key === 'featured') {
    const slug = slides[si].projects[pi].slug
    if (slug) {
      slides = slides.map(s => ({
        ...s,
        projects: s.projects.map(p => p.slug === slug ? { ...p, featured: value } : p)
      }))
    }
  }

  emitVal({ ...props.modelValue, slides })
}

function addContributor(si, pi) {
  const slides = props.modelValue.slides.map(s => ({ ...s, projects: [...s.projects] }))
  const proj = slides[si].projects[pi]
  slides[si].projects[pi] = { ...proj, contributors: [...(proj.contributors || []), { name: '', role: '', avatar: '' }] }
  emitVal({ ...props.modelValue, slides })
}

function removeContributor(si, pi, ci) {
  const slides = props.modelValue.slides.map(s => ({ ...s, projects: [...s.projects] }))
  const proj = slides[si].projects[pi]
  slides[si].projects[pi] = { ...proj, contributors: (proj.contributors || []).filter((_, i) => i !== ci) }
  emitVal({ ...props.modelValue, slides })
}

function updateContributor(si, pi, ci, key, value) {
  const slides = props.modelValue.slides.map(s => ({ ...s, projects: [...s.projects] }))
  const contribs = [...(slides[si].projects[pi].contributors || [])]
  contribs[ci] = { ...contribs[ci], [key]: value }
  slides[si].projects[pi] = { ...slides[si].projects[pi], contributors: contribs }
  emitVal({ ...props.modelValue, slides })
}
</script>

<style scoped>
.editor-section { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 24px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.editor-title { font-family: var(--font-heading); font-size: 15px; font-weight: 600; margin: 0 0 16px; }
.card-header .editor-title, .card-header .sub-title { margin: 0; }
.sub-title { font-size: 13px; font-weight: 600; color: var(--text-secondary); }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 12px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
.field input, .field textarea { width: 100%; padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 13px; font-family: var(--font-body); background: white; color: var(--text-primary); transition: border-color 0.2s; }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.field input:disabled { background: var(--bg-soft); color: var(--text-muted); cursor: not-allowed; }
.sub-section { margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--glass-border); }
.list-item { border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 16px; margin-bottom: 12px; }
.list-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.item-index { font-size: 12px; font-weight: 600; color: var(--text-muted); }
.inline-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.inline-row input { padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 13px; }
.inline-row input:focus { outline: none; border-color: var(--warm-terracotta); }
.w-200 { flex: 1; }
.btn-icon { width: 28px; height: 28px; border: 1px solid var(--glass-border); border-radius: 6px; background: white; color: var(--text-muted); font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-icon:disabled { opacity: 0.3; cursor: not-allowed; }
.sort-btns { display: flex; gap: 4px; }
.btn-xs { padding: 4px 12px; font-size: 12px; }
.cat-lock-hint { font-size: 11px; color: var(--text-muted); font-style: italic; }
.checkbox-label { display: flex; align-items: center; gap: 6px; cursor: pointer; font-size: 12px; }
.checkbox-label input { width: auto; }
.add-project-wrap { display: flex; gap: 8px; align-items: center; }
.project-select { padding: 4px 8px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 12px; background: white; color: var(--text-primary); max-width: 180px; }
.contributors-editor { margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--glass-border); }
.contributors-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.contrib-row { display: flex; gap: 8px; align-items: center; margin-bottom: 6px; }
.contrib-input { flex: 1; padding: 6px 10px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 12px; background: white; color: var(--text-primary); }
.contrib-input:focus { outline: none; border-color: var(--warm-terracotta); }
.btn-icon-sm { width: 22px; height: 22px; font-size: 13px; }

@media (max-width: 768px) {
  .editor-card { padding: 16px; }
  .field-grid { grid-template-columns: 1fr; }
  .list-item { padding: 12px; }
  .add-project-wrap { flex-wrap: wrap; }
  .project-select { max-width: 100%; }
}
</style>
