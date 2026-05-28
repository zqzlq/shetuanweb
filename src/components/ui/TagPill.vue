<template>
  <span class="tag" :class="{ 'tag-accent': active, 'tag-clickable': clickable }">
    <slot />
  </span>
</template>

<script setup>
defineProps({
  active: { type: Boolean, default: false },
  clickable: { type: Boolean, default: false },
})
</script>

<style scoped>
.tag-clickable {
  cursor: pointer;
  transition: all 0.2s ease;
}

.tag-clickable:hover {
  background: var(--surface-hover);
  border-color: var(--glass-border-hover);
}

.tag-accent {
  background: var(--grad-primary);
  color: white;
  border-color: transparent;
}
</style>
