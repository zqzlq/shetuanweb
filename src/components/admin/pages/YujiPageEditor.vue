<template>
  <div class="page-editor">
    <div class="editor-card">
      <h3 class="editor-title">Hero</h3>
      <div class="field-grid">
        <label class="field"><span>版本号</span><input :value="c().hero?.version || ''" @input="updateHero('version', $event.target.value)" /></label>
        <label class="field"><span>标题</span><input :value="c().hero?.title || ''" @input="updateHero('title', $event.target.value)" /></label>
        <label class="field full"><span>副标题</span><textarea :value="c().hero?.subtitle || ''" @input="updateHero('subtitle', $event.target.value)" rows="2"></textarea></label>
      </div>
      <div class="card-header" style="margin-top:16px">
        <h3 class="editor-title" style="font-size:13px">指标数据</h3>
        <button class="btn btn-xs" @click="addMetric">+ 添加</button>
      </div>
      <div v-for="(m, i) in c().hero?.metrics || []" :key="i" class="inline-row">
        <input :value="m.value" @input="updateMetric(i, 'value', $event.target.value)" placeholder="数值" class="inline-input-sm" />
        <input :value="m.label" @input="updateMetric(i, 'label', $event.target.value)" placeholder="标签" class="inline-input" />
        <button class="btn-icon" @click="removeMetric(i)">&#10005;</button>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">功能特性</h3>
        <button class="btn btn-xs" @click="addFeature">+ 添加</button>
      </div>
      <div v-for="(f, i) in c().features || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ f.title || '新特性' }}</span>
          <button class="btn-icon" @click="removeFeature(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>标题</span><input :value="f.title" @input="updateFeature(i, 'title', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="f.description" @input="updateFeature(i, 'description', $event.target.value)" rows="2"></textarea></label>
          <label class="field full"><span>标签（逗号分隔）</span><input :value="(f.tags || []).join(', ')" @change="updateFeature(i, 'tags', $event.target.value.split(',').map(s => s.trim()).filter(Boolean))" /></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">核心亮点</h3>
      <div class="field-grid">
        <label class="field full"><span>亮点（逗号分隔）</span><input :value="(c().highlights || []).join(', ')" @change="up({ ...c(), highlights: $event.target.value.split(',').map(s => s.trim()).filter(Boolean) })" /></label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">CTA</h3>
      <div class="field-grid">
        <label class="field full"><span>标题</span><input :value="c().cta?.title || ''" @input="updateCta('title', $event.target.value)" /></label>
        <label class="field"><span>按钮文字</span><input :value="c().cta?.buttonText || ''" @input="updateCta('buttonText', $event.target.value)" /></label>
        <label class="field"><span>链接</span><input :value="c().cta?.link || ''" @input="updateCta('link', $event.target.value)" /></label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">板块标题</h3>
      <div class="field-grid">
        <label class="field"><span>特性标题</span><input :value="c().sectionTitles?.features || ''" @input="updateSectionTitles('features', $event.target.value)" /></label>
        <label class="field"><span>亮点标题</span><input :value="c().sectionTitles?.highlights || ''" @input="updateSectionTitles('highlights', $event.target.value)" /></label>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ content: Object })
const emit = defineEmits(['update'])
const c = () => props.content
const up = (v) => emit('update', v)

function updateHero(k, v) { up({ ...c(), hero: { ...c().hero, [k]: v } }) }
function updateCta(k, v) { up({ ...c(), cta: { ...c().cta, [k]: v } }) }
function updateSectionTitles(k, v) { up({ ...c(), sectionTitles: { ...c().sectionTitles, [k]: v } }) }

function updateMetric(i, k, v) {
  const arr = [...(c().hero?.metrics || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), hero: { ...c().hero, metrics: arr } })
}
function addMetric() { up({ ...c(), hero: { ...c().hero, metrics: [...(c().hero?.metrics || []), { value: '', label: '' }] } }) }
function removeMetric(i) { up({ ...c(), hero: { ...c().hero, metrics: (c().hero?.metrics || []).filter((_, idx) => idx !== i) } }) }

function updateFeature(i, k, v) {
  const arr = [...(c().features || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), features: arr })
}
function addFeature() { up({ ...c(), features: [...(c().features || []), { title: '', description: '', tags: [] }] }) }
function removeFeature(i) { up({ ...c(), features: (c().features || []).filter((_, idx) => idx !== i) }) }
</script>

<style scoped>
.page-editor { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: var(--bg-soft); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 20px; }
.editor-title { font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin: 0; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.card-header .editor-title { margin: 0; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 11px; font-weight: 500; color: var(--text-muted); margin-bottom: 3px; }
.field input, .field textarea { width: 100%; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.list-item { background: white; border: 1px solid var(--glass-border); border-radius: 8px; padding: 12px; margin-top: 8px; }
.list-item-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.item-index { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.btn-icon { width: 24px; height: 24px; border: none; background: none; font-size: 14px; color: var(--text-muted); cursor: pointer; border-radius: 4px; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { background: var(--bg-soft); color: #e05050; }
.btn-xs { padding: 4px 10px; font-size: 11px; border: 1px solid var(--glass-border); border-radius: 4px; background: white; cursor: pointer; color: var(--text-secondary); }
.btn-xs:hover { border-color: var(--warm-terracotta); color: var(--warm-terracotta); }
.inline-row { display: flex; align-items: center; gap: 8px; margin-top: 8px; }
.inline-input { flex: 1; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.inline-input:focus { outline: none; border-color: var(--warm-terracotta); }
.inline-input-sm { width: 100px; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.inline-input-sm:focus { outline: none; border-color: var(--warm-terracotta); }
</style>
