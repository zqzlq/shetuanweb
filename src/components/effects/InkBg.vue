<template>
  <div class="warm-bg" aria-hidden="true">
    <div class="bg-grid"></div>
  </div>
</template>

<style scoped>
.warm-bg {
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background:
    radial-gradient(ellipse 700px 600px at 10% 15%, rgba(192, 96, 64, 0.07) 0%, transparent 60%),
    radial-gradient(ellipse 600px 700px at 90% 80%, rgba(212, 146, 10, 0.06) 0%, transparent 60%),
    radial-gradient(ellipse 500px 500px at 55% 25%, rgba(122, 154, 106, 0.05) 0%, transparent 55%),
    var(--bg);
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(192, 96, 64, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(192, 96, 64, 0.03) 1px, transparent 1px);
  background-size: 48px 48px;
}
</style>
