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
      <p class="editor-hint">分类与页面管理中的项目分类保持一致，修改后轮播自动同步对应分类下的项目。</p>
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
        <h4 class="sub-title">包含的项目（同步自页面管理 → 项目展示）</h4>
        <p class="sync-hint">此轮播自动展示"{{ slide.tag || '未命名' }}"分类下的所有项目。在页面管理中修改项目分类即可调整归属。</p>
        <div v-if="matchingProjects(slide.tag, si).length === 0" class="empty-hint">{{ si === 0 ? '暂无精选项目' : `暂无"${slide.tag}"分类的项目` }}</div>
        <div v-for="proj in matchingProjects(slide.tag, si)" :key="proj.slug" class="list-item">
          <span class="item-index">{{ proj.name || '未命名项目' }}</span>
          <span v-if="proj.featured" class="tag tag-featured">精选</span>
          <span class="project-slug">{{ proj.slug }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: Object,
  allProjects: { type: Array, default: () => [] }
})
const emit = defineEmits(['update:modelValue'])

function emitVal(val) { emit('update:modelValue', val) }
function update(key, value) { emitVal({ ...props.modelValue, [key]: value }) }

// 根据分类标签匹配项目（精选总览显示所有精选项目）
function matchingProjects(tag, si) {
  if (!tag) return []
  if (si === 0) return (props.allProjects || []).filter(p => p.featured)
  return (props.allProjects || []).filter(p => p.category === tag)
}

// ── 分类与轮播同步 ──

function updateCat(i, value) {
  const categories = [...props.modelValue.categories]
  const oldValue = categories[i]
  categories[i] = value
  const slides = props.modelValue.slides.map(s => ({
    ...s,
    tag: s.tag === oldValue ? value : s.tag,
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

// ── 轮播 ──
</script>

<style scoped>
.editor-section { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 24px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.editor-title { font-family: var(--font-heading); font-size: 15px; font-weight: 600; margin: 0 0 16px; }
.card-header .editor-title { margin: 0; }
.editor-hint { font-size: 12px; color: var(--text-muted); margin: 0 0 12px; line-height: 1.6; }
.sub-title { font-size: 13px; font-weight: 600; color: var(--text-secondary); margin: 0; }
.sync-hint { font-size: 11px; color: var(--text-muted); margin: 4px 0 12px; line-height: 1.5; }
.empty-hint { font-size: 12px; color: var(--text-muted); font-style: italic; padding: 12px 0; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 12px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
.field input, .field textarea { width: 100%; padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 13px; font-family: var(--font-body); background: white; color: var(--text-primary); transition: border-color 0.2s; }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.field input:disabled { background: var(--bg-soft); color: var(--text-muted); cursor: not-allowed; }
.sub-section { margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--glass-border); }
.list-item { border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 10px 14px; margin-bottom: 6px; display: flex; align-items: center; gap: 10px; background: var(--bg-soft); }
.item-index { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.project-slug { font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); margin-left: auto; }
.tag-featured { background: rgba(192, 96, 64, 0.1); color: var(--warm-terracotta); font-size: 10px; padding: 1px 6px; border-radius: 999px; flex-shrink: 0; }
.inline-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.inline-row input { padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 13px; }
.inline-row input:focus { outline: none; border-color: var(--warm-terracotta); }
.w-200 { flex: 1; }
.btn-icon { width: 28px; height: 28px; border: 1px solid var(--glass-border); border-radius: 6px; background: white; color: var(--text-muted); font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-icon:disabled { opacity: 0.3; cursor: not-allowed; }
.btn-xs { padding: 4px 12px; font-size: 12px; }
.cat-lock-hint { font-size: 11px; color: var(--text-muted); font-style: italic; }

@media (max-width: 768px) {
  .editor-card { padding: 16px; }
  .field-grid { grid-template-columns: 1fr; }
}
</style>
