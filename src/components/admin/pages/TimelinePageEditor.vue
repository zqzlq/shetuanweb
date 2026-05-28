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
        <h3 class="editor-title">即将到来</h3>
        <button class="btn btn-xs" @click="addUpcoming">+ 添加</button>
      </div>
      <div v-for="(upc, i) in c().upcoming || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ upc.title || '新事件' }}</span>
          <button class="btn-icon" @click="removeUpcoming(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>标题</span><input :value="upc.title" @input="updateUpcoming(i, 'title', $event.target.value)" /></label>
          <label class="field"><span>日期</span><input :value="upc.date" @input="updateUpcoming(i, 'date', $event.target.value)" placeholder="YYYY-MM-DD" /></label>
          <label class="field"><span>类型</span><input :value="upc.type" @input="updateUpcoming(i, 'type', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="upc.description" @input="updateUpcoming(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">里程碑</h3>
        <button class="btn btn-xs" @click="addMilestone">+ 添加</button>
      </div>
      <div v-for="(m, i) in c().milestones || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ m.title || '新里程碑' }}</span>
          <button class="btn-icon" @click="removeMilestone(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>年份</span><input :value="m.year" @input="updateMilestone(i, 'year', $event.target.value)" /></label>
          <label class="field"><span>标题</span><input :value="m.title" @input="updateMilestone(i, 'title', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="m.description" @input="updateMilestone(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">板块标题</h3>
      <div class="field-grid">
        <label class="field"><span>即将到来标题</span><input :value="c().sections?.upcomingTitle || ''" @input="updateSections('upcomingTitle', $event.target.value)" /></label>
        <label class="field"><span>里程碑标题</span><input :value="c().sections?.milestonesTitle || ''" @input="updateSections('milestonesTitle', $event.target.value)" /></label>
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
function updateSections(k, v) { up({ ...c(), sections: { ...c().sections, [k]: v } }) }

function updateUpcoming(i, k, v) {
  const arr = [...(c().upcoming || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), upcoming: arr })
}
function addUpcoming() { up({ ...c(), upcoming: [...(c().upcoming || []), { title: '', date: '', type: '', description: '' }] }) }
function removeUpcoming(i) { up({ ...c(), upcoming: (c().upcoming || []).filter((_, idx) => idx !== i) }) }

function updateMilestone(i, k, v) {
  const arr = [...(c().milestones || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), milestones: arr })
}
function addMilestone() { up({ ...c(), milestones: [...(c().milestones || []), { year: '', title: '', description: '' }] }) }
function removeMilestone(i) { up({ ...c(), milestones: (c().milestones || []).filter((_, idx) => idx !== i) }) }
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
