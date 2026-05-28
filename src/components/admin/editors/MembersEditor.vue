<template>
  <div class="editor-section">
    <div class="editor-card">
      <h3 class="editor-title">人员介绍</h3>
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
      <div class="card-header">
        <h3 class="editor-title">组别</h3>
        <button class="btn btn-outline btn-xs" @click="addGroup">+ 添加</button>
      </div>
      <div v-for="(g, i) in modelValue.groups" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ g.name || '#' + (i + 1) }}</span>
          <button class="btn-icon" @click="removeGroup(i)">&times;</button>
        </div>
        <div class="field-grid">
          <label class="field">
            <span>标签</span>
            <input :value="g.tag" @input="updateGroup(i, 'tag', $event.target.value)" />
          </label>
          <label class="field">
            <span>名称</span>
            <input :value="g.name" @input="updateGroup(i, 'name', $event.target.value)" />
          </label>
          <label class="field full">
            <span>描述</span>
            <textarea :value="g.description" @input="updateGroup(i, 'description', $event.target.value)" rows="2"></textarea>
          </label>
        </div>
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

function updateGroup(index, key, value) {
  const groups = [...props.modelValue.groups]
  groups[index] = { ...groups[index], [key]: value }
  emit('update:modelValue', { ...props.modelValue, groups })
}

function addGroup() {
  emit('update:modelValue', { ...props.modelValue, groups: [...props.modelValue.groups, { tag: '', name: '', description: '' }] })
}

function removeGroup(index) {
  emit('update:modelValue', { ...props.modelValue, groups: props.modelValue.groups.filter((_, i) => i !== index) })
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
.list-item { border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 16px; margin-bottom: 12px; }
.list-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.item-index { font-size: 12px; font-weight: 600; color: var(--text-muted); }
.btn-icon { width: 28px; height: 28px; border: 1px solid var(--glass-border); border-radius: 6px; background: white; color: var(--text-muted); font-size: 16px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-xs { padding: 4px 12px; font-size: 12px; }

@media (max-width: 768px) {
  .editor-card { padding: 16px; }
  .field-grid { grid-template-columns: 1fr; }
}
</style>
