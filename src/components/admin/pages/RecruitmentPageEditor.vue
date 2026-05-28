<template>
  <div class="page-editor">
    <div class="editor-card">
      <h3 class="editor-title">Hero</h3>
      <div class="field-grid">
        <label class="field"><span>角标</span><input :value="c().hero?.eyebrow || ''" @input="updateHero('eyebrow', $event.target.value)" /></label>
        <label class="field"><span>标题</span><input :value="c().hero?.title || ''" @input="updateHero('title', $event.target.value)" /></label>
        <label class="field full"><span>副标题</span><textarea :value="c().hero?.subtitle || ''" @input="updateHero('subtitle', $event.target.value)" rows="2"></textarea></label>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">招新组别</h3>
        <button class="btn btn-xs" @click="addGroup">+ 添加</button>
      </div>
      <div v-for="(g, i) in c().groups || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ g.name || '新组别' }}</span>
          <button class="btn-icon" @click="removeGroup(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>名称</span><input :value="g.name" @input="updateGroup(i, 'name', $event.target.value)" /></label>
          <label class="field"><span>标签</span><input :value="g.tag" @input="updateGroup(i, 'tag', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="g.description" @input="updateGroup(i, 'description', $event.target.value)" rows="2"></textarea></label>
          <label class="field full"><span>要求（逗号分隔）</span><input :value="(g.requirements || []).join(', ')" @change="updateGroup(i, 'requirements', $event.target.value.split(',').map(s => s.trim()).filter(Boolean))" /></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">招募流程</h3>
        <button class="btn btn-xs" @click="addProcess">+ 添加</button>
      </div>
      <div v-for="(p, i) in c().process || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ p.step || '新步骤' }}</span>
          <button class="btn-icon" @click="removeProcess(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>步骤名称</span><input :value="p.step" @input="updateProcess(i, 'step', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="p.description" @input="updateProcess(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">CTA 按钮</h3>
      <div class="field-grid">
        <label class="field full"><span>标题</span><input :value="c().cta?.title || ''" @input="updateCta('title', $event.target.value)" /></label>
        <label class="field"><span>按钮文字</span><input :value="c().cta?.buttonText || ''" @input="updateCta('buttonText', $event.target.value)" /></label>
        <label class="field"><span>按钮链接</span><input :value="c().cta?.buttonLink || ''" @input="updateCta('buttonLink', $event.target.value)" /></label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">板块标题</h3>
      <div class="field-grid">
        <label class="field"><span>流程标题</span><input :value="c().sectionTitles?.process || ''" @input="updateSectionTitles('process', $event.target.value)" /></label>
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

function updateGroup(i, k, v) {
  const arr = [...(c().groups || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), groups: arr })
}
function addGroup() { up({ ...c(), groups: [...(c().groups || []), { name: '', tag: '', description: '', requirements: [] }] }) }
function removeGroup(i) { up({ ...c(), groups: (c().groups || []).filter((_, idx) => idx !== i) }) }

function updateProcess(i, k, v) {
  const arr = [...(c().process || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), process: arr })
}
function addProcess() { up({ ...c(), process: [...(c().process || []), { step: '', description: '' }] }) }
function removeProcess(i) { up({ ...c(), process: (c().process || []).filter((_, idx) => idx !== i) }) }
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
</style>
