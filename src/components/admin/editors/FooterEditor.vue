<template>
  <div class="editor-section">
    <div class="editor-card">
      <h3 class="editor-title">页脚信息</h3>
      <div class="field-grid">
        <label class="field full">
          <span>品牌名称</span>
          <input :value="modelValue.brand" @input="update('brand', $event.target.value)" />
        </label>
        <label class="field full">
          <span>Logo 图片</span>
          <ImageUploadField :modelValue="modelValue.logo || ''" @update:modelValue="update('logo', $event)" />
        </label>
        <label class="field full">
          <span>标语</span>
          <input :value="modelValue.slogan" @input="update('slogan', $event.target.value)" />
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import ImageUploadField from '../ImageUploadField.vue'
const props = defineProps({ modelValue: Object })
const emit = defineEmits(['update:modelValue'])

function update(key, value) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}
</script>

<style scoped>
.editor-section { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 24px; }
.editor-title { font-family: var(--font-heading); font-size: 15px; font-weight: 600; margin: 0 0 16px; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 12px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
.field input { width: 100%; padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: var(--radius-sm); font-size: 13px; font-family: var(--font-body); background: white; color: var(--text-primary); transition: border-color 0.2s; }
.field input:focus { outline: none; border-color: var(--warm-terracotta); }

@media (max-width: 768px) {
  .editor-card { padding: 16px; }
  .field-grid { grid-template-columns: 1fr; }
}
</style>
