<template>
  <div class="md-editor">
    <div class="md-tabs">
      <button :class="{ active: tab === 'edit' }" @click="tab = 'edit'">编辑</button>
      <button :class="{ active: tab === 'preview' }" @click="tab = 'preview'">预览</button>
      <button :class="{ active: tab === 'split' }" @click="tab = 'split'">分屏</button>
    </div>
    <div :class="['md-body', tab]">
      <div class="md-input-wrap" v-if="tab !== 'preview'">
        <textarea :value="modelValue" @input="$emit('update:modelValue', $event.target.value)" rows="6" placeholder="支持 Markdown 格式..." />
      </div>
      <div class="md-preview-wrap" v-if="tab !== 'edit'">
        <div class="md-preview-label">预览</div>
        <MarkdownRenderer :content="modelValue || ''" />
        <div v-if="!modelValue" class="md-empty">暂无内容</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MarkdownRenderer from '../ui/MarkdownRenderer.vue'

defineProps({ modelValue: { type: String, default: '' } })
defineEmits(['update:modelValue'])

const tab = ref('split')
</script>

<style scoped>
.md-editor { border: 1px solid var(--glass-border); border-radius: var(--radius-md); overflow: hidden; }
.md-tabs { display: flex; background: var(--bg-soft); border-bottom: 1px solid var(--glass-border); }
.md-tabs button { padding: 6px 16px; font-size: 12px; border: none; background: none; cursor: pointer; color: var(--text-muted); border-bottom: 2px solid transparent; transition: all 0.2s; }
.md-tabs button.active { color: var(--warm-terracotta); border-bottom-color: var(--warm-terracotta); font-weight: 600; }
.md-tabs button:hover { color: var(--text-primary); }
.md-body { display: flex; min-height: 160px; }
.md-body.edit .md-input-wrap { flex: 1; }
.md-body.preview .md-preview-wrap { flex: 1; }
.md-body.split .md-input-wrap,
.md-body.split .md-preview-wrap { flex: 1; min-width: 0; }
.md-input-wrap { display: flex; }
.md-input-wrap textarea { flex: 1; border: none; padding: 12px; font-size: 13px; font-family: var(--font-body); resize: vertical; outline: none; line-height: 1.6; background: white; color: var(--text-primary); }
.md-preview-wrap { flex: 1; padding: 12px; overflow: auto; border-left: 1px solid var(--glass-border); background: white; }
.md-body.edit .md-preview-wrap,
.md-body.preview .md-input-wrap { display: none; }
.md-body.preview .md-preview-wrap { border-left: none; }
.md-preview-label { font-size: 11px; color: var(--text-muted); margin-bottom: 8px; font-weight: 500; }
.md-empty { color: var(--text-muted); font-size: 13px; font-style: italic; }

@media (max-width: 768px) {
  .md-body.split { flex-direction: column; }
  .md-body.split .md-preview-wrap { border-left: none; border-top: 1px solid var(--glass-border); }
}
</style>
