<template>
  <div class="markdown-body" v-html="rendered"></div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  content: { type: String, default: '' },
})

const rendered = computed(() => {
  if (!props.content) return ''
  return marked(props.content, { breaks: true })
})
</script>

<style scoped>
.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  font-family: var(--font-heading);
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.markdown-body :deep(p) {
  margin: 0.8em 0;
  line-height: 1.8;
}

.markdown-body :deep(code) {
  background: var(--surface);
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 0.9em;
}

.markdown-body :deep(pre) {
  background: var(--bg-soft);
  color: var(--text-primary);
  padding: 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  overflow-x: auto;
}

.markdown-body :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid var(--warm-terracotta);
  padding-left: 16px;
  margin: 1em 0;
  color: var(--text-secondary);
}

.markdown-body :deep(img) {
  max-width: 100%;
  border-radius: var(--radius-md);
}

.markdown-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  border: 1px solid var(--glass-border);
  padding: 8px 12px;
  text-align: left;
}

.markdown-body :deep(th) {
  background: var(--surface);
  font-weight: 600;
}
</style>
