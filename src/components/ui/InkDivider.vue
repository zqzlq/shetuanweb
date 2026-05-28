<template>
  <div class="warm-divider"></div>
</template>

<style scoped>
.warm-divider {
  width: 100%;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--glass-border) 20%,
    rgba(192, 96, 64, 0.2) 50%,
    var(--glass-border) 80%,
    transparent 100%
  );
  margin: var(--section-gap) 0;
}
</style>
