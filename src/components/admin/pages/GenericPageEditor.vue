<template>
  <div class="generic-editor">
    <p class="hint">此页面暂无专用可视化编辑器，请使用 JSON 模式编辑。</p>
    <div class="preview">
      <pre>{{ JSON.stringify(content, null, 2).slice(0, 2000) }}{{ contentStr.length > 2000 ? '\n...' : '' }}</pre>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ content: Object })
const contentStr = computed(() => JSON.stringify(props.content, null, 2))
</script>

<style scoped>
.generic-editor { padding: 16px 0; }
.hint { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }
.preview { background: var(--bg-soft); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 16px; max-height: 400px; overflow-y: auto; }
.preview pre { font-family: var(--font-mono); font-size: 12px; line-height: 1.6; margin: 0; white-space: pre-wrap; word-break: break-all; color: var(--text-secondary); }

@media (max-width: 768px) {
  .preview { padding: 12px; max-height: 300px; }
  .preview pre { font-size: 11px; }
}
</style>
