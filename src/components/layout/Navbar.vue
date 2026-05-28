<template>
  <nav class="navbar" :class="{ scrolled: isScrolled }">
    <div class="navbar-inner container">
      <router-link to="/" class="navbar-brand">
        <span class="brand-icon">
          <img :src="siteConfig.footer.logo || logoFallback" alt="星雨作坊" class="brand-logo-img" />
        </span>
        <span class="brand-text">星雨作坊</span>
      </router-link>

      <button class="navbar-toggle" @click="menuOpen = !menuOpen" aria-label="菜单">
        <span :class="{ open: menuOpen }"></span>
      </button>

      <div class="navbar-links" :class="{ open: menuOpen }">
        <router-link to="/#about" @click="menuOpen = false">关于</router-link>
        <router-link to="/members" @click="menuOpen = false">成员</router-link>
        <router-link to="/projects" @click="menuOpen = false">项目</router-link>
        <router-link to="/blog" @click="menuOpen = false">动态</router-link>
        <router-link to="/open-source" @click="menuOpen = false">开源</router-link>
        <router-link to="/join" class="btn btn-primary btn-sm" @click="menuOpen = false">加入我们</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import logoFallback from '@/assets/logo.png'

const { config: siteConfig } = useSiteConfigStore()
const isScrolled = ref(false)
const menuOpen = ref(false)

const onScroll = () => {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 16px 0;
  transition: all 0.35s ease;
}

.navbar.scrolled {
  background: rgba(250, 247, 242, 0.92);
  border-bottom: 1px solid var(--glass-border);
  padding: 10px 0;
  box-shadow: 0 2px 20px rgba(120, 90, 60, 0.06);
}

.navbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 17px;
  color: var(--text-primary);
}

.brand-icon {
  display: flex;
  transition: transform 0.3s ease;
}

.brand-logo-img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.navbar-brand:hover .brand-icon {
  transform: rotate(15deg) scale(1.1);
}

.brand-text {
  letter-spacing: 0.02em;
  transition: color 0.3s;
}

.navbar-brand:hover .brand-text {
  color: var(--warm-terracotta);
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 28px;
}

.navbar-links a:not(.btn) {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: color 0.25s;
  position: relative;
  padding: 4px 0;
}

.navbar-links a:not(.btn):hover {
  color: var(--warm-terracotta);
}

.navbar-links a:not(.btn)::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--grad-primary);
  border-radius: 1px;
  transition: width 0.3s ease;
}

.navbar-links a:not(.btn):hover::after {
  width: 100%;
}

.btn-sm {
  padding: 8px 20px;
  font-size: 13px;
}

.navbar-toggle {
  display: none;
  background: none;
  border: none;
  width: 28px;
  height: 20px;
  position: relative;
  cursor: pointer;
}

.navbar-toggle span,
.navbar-toggle span::before,
.navbar-toggle span::after {
  display: block;
  width: 100%;
  height: 2px;
  background: var(--text-primary);
  position: absolute;
  transition: all 0.3s;
}

.navbar-toggle span {
  top: 50%;
  transform: translateY(-50%);
}

.navbar-toggle span::before {
  content: '';
  top: -8px;
}

.navbar-toggle span::after {
  content: '';
  bottom: -8px;
}

.navbar-toggle span.open {
  background: transparent;
}

.navbar-toggle span.open::before {
  top: 0;
  transform: rotate(45deg);
}

.navbar-toggle span.open::after {
  bottom: 0;
  transform: rotate(-45deg);
}

@media (max-width: 768px) {
  .navbar-toggle {
    display: block;
  }

  .navbar-links {
    position: fixed;
    top: 0;
    right: -100%;
    width: 280px;
    height: 100vh;
    background: rgba(250, 247, 242, 0.98);
    flex-direction: column;
    align-items: flex-start;
    padding: 80px 32px 32px;
    gap: 20px;
    border-left: 1px solid var(--glass-border);
    transition: right 0.3s ease;
  }

  .navbar-links.open {
    right: 0;
  }

  .navbar-links a:not(.btn) {
    font-size: 16px;
  }
}
</style>
