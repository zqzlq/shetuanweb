<template>
  <div class="editor-section">
    <div class="editor-card">
      <h3 class="editor-title">社团简介</h3>
      <div class="field-grid">
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
        <h3 class="editor-title">信息卡片</h3>
        <button class="btn btn-outline btn-xs" @click="addItem">+ 添加</button>
      </div>
      <div v-for="(item, i) in modelValue.items" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">#{{ i + 1 }}</span>
          <button class="btn-icon" @click="removeItem(i)">&times;</button>
        </div>
        <div class="field-grid">
          <label class="field full">
            <span>标题</span>
            <input :value="item.title" @input="updateItem(i, 'title', $event.target.value)" />
          </label>
          <label class="field full">
            <span>描述</span>
            <textarea :value="item.description" @input="updateItem(i, 'description', $event.target.value)" rows="2"></textarea>
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

function updateItem(index, key, value) {
  const items = [...props.modelValue.items]
  items[index] = { ...items[index], [key]: value }
  emit('update:modelValue', { ...props.modelValue, items })
}

function addItem() {
  emit('update:modelValue', { ...props.modelValue, items: [...props.modelValue.items, { title: '', description: '' }] })
}

function removeItem(index) {
  emit('update:modelValue', { ...props.modelValue, items: props.modelValue.items.filter((_, i) => i !== index) })
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
