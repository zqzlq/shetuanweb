<template>
  <div class="editor-section">
    <div class="editor-card">
      <h3 class="editor-title">Hero 区域</h3>
      <div class="field-grid">
        <label class="field full">
          <span>角标文字</span>
          <input :value="modelValue.eyebrow" @input="update('eyebrow', $event.target.value)" />
        </label>
        <label class="field full">
          <span>标题</span>
          <input :value="modelValue.title" @input="update('title', $event.target.value)" />
        </label>
        <label class="field full">
          <span>描述</span>
          <textarea :value="modelValue.description" @input="update('description', $event.target.value)" rows="3"></textarea>
        </label>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">数据统计</h3>
        <button class="btn btn-outline btn-xs" @click="addStat">+ 添加</button>
      </div>
      <div v-for="(s, i) in modelValue.stats" :key="i" class="inline-row">
        <input :value="s.value" @input="updateStat(i, 'value', $event.target.value)" placeholder="数值" class="w-100" />
        <input :value="s.label" @input="updateStat(i, 'label', $event.target.value)" placeholder="标签" class="w-200" />
        <button class="btn-icon" @click="removeStat(i)">&times;</button>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">信号卡片</h3>
      <div class="field-grid">
        <label class="field">
          <span>角标</span>
          <input :value="modelValue.signalCard?.eyebrow" @input="updateNested('signalCard', 'eyebrow', $event.target.value)" />
        </label>
        <label class="field">
          <span>标题</span>
          <input :value="modelValue.signalCard?.title" @input="updateNested('signalCard', 'title', $event.target.value)" />
        </label>
        <label class="field full">
          <span>描述</span>
          <input :value="modelValue.signalCard?.description" @input="updateNested('signalCard', 'description', $event.target.value)" />
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ modelValue: Object })
const emit = defineEmits(['update:modelValue'])

function update(key, value) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}

function updateNested(parent, key, value) {
  emit('update:modelValue', { ...props.modelValue, [parent]: { ...props.modelValue[parent], [key]: value } })
}

function updateStat(index, key, value) {
  const stats = [...props.modelValue.stats]
  stats[index] = { ...stats[index], [key]: value }
  emit('update:modelValue', { ...props.modelValue, stats })
}

function addStat() {
  emit('update:modelValue', { ...props.modelValue, stats: [...props.modelValue.stats, { value: '', label: '' }] })
}

function removeStat(index) {
  const stats = props.modelValue.stats.filter((_, i) => i !== index)
  emit('update:modelValue', { ...props.modelValue, stats })
}
</script>

<style scoped>
.editor-section { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 24px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.editor-title { font-family: var(--font-heading); font-size: 15px; font-weight: 600; margin: 0 0 16px; }
.card-header .editor-title { margin: 0; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 12px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
.field input, .field textarea { width: 100%; padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 13px; font-family: var(--font-body); background: white; color: var(--text-primary); transition: border-color 0.2s; }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.inline-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.inline-row input { padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 13px; }
.inline-row input:focus { outline: none; border-color: var(--warm-terracotta); }
.w-100 { width: 100px; }
.w-200 { flex: 1; }
.btn-icon { width: 28px; height: 28px; border: 1px solid var(--glass-border); border-radius: 6px; background: white; color: var(--text-muted); font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-xs { padding: 4px 12px; font-size: 12px; }

@media (max-width: 768px) {
  .editor-card { padding: 16px; }
  .field-grid { grid-template-columns: 1fr; }
}
</style>
