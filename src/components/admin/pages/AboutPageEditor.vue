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
      <div class="card-header"><h3 class="editor-title">价值观</h3><button class="btn btn-outline btn-xs" @click="addValue">+ 添加</button></div>
      <div class="field-grid">
        <label class="field full"><span>标题</span><input :value="content.values?.title" @input="updateValues('title', $event.target.value)" /></label>
        <label class="field full"><span>副标题</span><input :value="content.values?.subtitle" @input="updateValues('subtitle', $event.target.value)" /></label>
      </div>
      <div v-for="(item, i) in content.values?.items || []" :key="i" class="list-item">
        <div class="list-item-header"><span class="item-index">{{ item.title || '#' + (i+1) }}</span><button class="btn-icon" @click="removeValue(i)">&times;</button></div>
        <div class="field-grid">
          <label class="field"><span>图标</span><input :value="item.icon" @input="updateValueItem(i, 'icon', $event.target.value)" /></label>
          <label class="field"><span>标题</span><input :value="item.title" @input="updateValueItem(i, 'title', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="item.description" @input="updateValueItem(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header"><h3 class="editor-title">星系</h3><button class="btn btn-outline btn-xs" @click="addGroup">+ 添加</button></div>
      <div class="field-grid">
        <label class="field full"><span>标题</span><input :value="content.groups?.title" @input="updateGroups('title', $event.target.value)" /></label>
        <label class="field full"><span>副标题</span><input :value="content.groups?.subtitle" @input="updateGroups('subtitle', $event.target.value)" /></label>
      </div>
      <div v-for="(item, i) in content.groups?.items || []" :key="i" class="list-item">
        <div class="list-item-header"><span class="item-index">{{ item.name || '#' + (i+1) }}</span><button class="btn-icon" @click="removeGroup(i)">&times;</button></div>
        <div class="field-grid">
          <label class="field"><span>名称</span><input :value="item.name" @input="updateGroupItem(i, 'name', $event.target.value)" /></label>
          <label class="field"><span>标签</span><input :value="item.tag" @input="updateGroupItem(i, 'tag', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="item.description" @input="updateGroupItem(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header"><h3 class="editor-title">时间线</h3><button class="btn btn-outline btn-xs" @click="addTimeline">+ 添加</button></div>
      <div class="field-grid">
        <label class="field"><span>标题</span><input :value="content.timeline?.title" @input="updateTimeline('title', $event.target.value)" /></label>
        <label class="field"><span>角标</span><input :value="content.timeline?.eyebrow" @input="updateTimeline('eyebrow', $event.target.value)" /></label>
      </div>
      <div v-for="(item, i) in content.timeline?.items || []" :key="i" class="list-item">
        <div class="list-item-header"><span class="item-index">{{ item.year || '#' + (i+1) }}</span><button class="btn-icon" @click="removeTimelineItem(i)">&times;</button></div>
        <div class="field-grid">
          <label class="field"><span>年份</span><input :value="item.year" @input="updateTimelineItem(i, 'year', $event.target.value)" /></label>
          <label class="field"><span>标题</span><input :value="item.title" @input="updateTimelineItem(i, 'title', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="item.description" @input="updateTimelineItem(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ content: Object })
const emit = defineEmits(['update'])
const c = () => props.content
const up = (val) => emit('update', val)

function updateHero(k, v) { up({ ...c(), hero: { ...c().hero, [k]: v } }) }
function updateValues(k, v) { up({ ...c(), values: { ...c().values, [k]: v } }) }
function updateGroups(k, v) { up({ ...c(), groups: { ...c().groups, [k]: v } }) }
function updateTimeline(k, v) { up({ ...c(), timeline: { ...c().timeline, [k]: v } }) }

function updateArrayItem(parent, i, k, v) {
  const arr = [...(c()[parent]?.items || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), [parent]: { ...c()[parent], items: arr } })
}
function addArrayItem(parent, template) {
  up({ ...c(), [parent]: { ...c()[parent], items: [...(c()[parent]?.items || []), template] } })
}
function removeArrayItem(parent, i) {
  up({ ...c(), [parent]: { ...c()[parent], items: (c()[parent]?.items || []).filter((_, idx) => idx !== i) } })
}

const updateValueItem = (i, k, v) => updateArrayItem('values', i, k, v)
const addValue = () => addArrayItem('values', { icon: '', title: '', description: '' })
const removeValue = (i) => removeArrayItem('values', i)
const updateGroupItem = (i, k, v) => updateArrayItem('groups', i, k, v)
const addGroup = () => addArrayItem('groups', { name: '', tag: '', description: '' })
const removeGroup = (i) => removeArrayItem('groups', i)
const updateTimelineItem = (i, k, v) => updateArrayItem('timeline', i, k, v)
const addTimeline = () => addArrayItem('timeline', { year: '', title: '', description: '' })
const removeTimelineItem = (i) => removeArrayItem('timeline', i)
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
.btn-xs { padding: 3px 10px; font-size: 11px; }

@media (max-width: 768px) {
  .editor-card { padding: 12px; }
  .field-grid { grid-template-columns: 1fr; }
  .list-item { padding: 10px; }
}
</style>
