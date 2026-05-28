<template>
  <div class="glass-card" :class="[variant, { 'with-glow': glow }]" :style="glow ? { '--card-accent': glow } : {}">
    <div v-if="glow" class="card-glow" aria-hidden="true"></div>
    <div class="card-wash" aria-hidden="true"></div>
    <slot />
    <div v-if="glow" class="card-accent-line" aria-hidden="true"></div>
  </div>
</template>

<script setup>
defineProps({
  variant: { type: String, default: '' },
  glow: { type: String, default: '' },
})
</script>

<style scoped>
.glass-card {
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 28px;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease, border-color 0.4s ease;
  position: relative;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

/* 暖色光晕渐显 */
.card-wash {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, var(--card-accent, var(--warm-terracotta)), transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.glass-card:hover .card-wash {
  opacity: 0.04;
}

.card-glow {
  position: absolute;
  top: -40%;
  left: 50%;
  transform: translateX(-50%);
  width: 160px;
  height: 160px;
  background: var(--card-accent, var(--warm-terracotta));
  opacity: 0.04;
  border-radius: 50%;
  filter: blur(50px);
  transition: opacity 0.4s, width 0.4s, height 0.4s;
  pointer-events: none;
}

.card-accent-line {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--card-accent, var(--warm-terracotta));
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

/* 默认悬浮 */
.glass-card:hover {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 20px 56px rgba(120, 90, 60, 0.12);
  border-color: var(--glass-border-hover);
}

/* 带光晕的悬浮 */
.glass-card.with-glow:hover {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 24px 64px rgba(120, 90, 60, 0.14);
  border-color: var(--card-accent, var(--warm-terracotta));
}

.glass-card.with-glow:hover .card-glow {
  opacity: 0.15;
  width: 200px;
  height: 200px;
}

.glass-card.with-glow:hover .card-accent-line {
  opacity: 1;
}

.glass-card.stamp {
  border: 2px solid var(--glass-border);
  border-radius: var(--radius-md);
}

.glass-card.stamp:hover {
  border-color: var(--warm-terracotta);
  transform: translateY(-12px) scale(1.03) rotate(-1.5deg);
  box-shadow: 0 24px 64px rgba(120, 90, 60, 0.14);
}
</style>
