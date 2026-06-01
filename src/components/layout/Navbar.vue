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
        <router-link to="/blog" @click="menuOpen = false">动态/公告</router-link>
        <router-link to="/open-source" @click="menuOpen = false">开源</router-link>
        <router-link to="/contact" @click="menuOpen = false">联系我们</router-link>
        <router-link to="/join" class="btn btn-primary btn-sm" @click="menuOpen = false">加入我们</router-link>
        <template v-if="currentUser">
          <div class="user-dropdown">
            <button class="user-avatar-btn" @click="userMenuOpen = !userMenuOpen">
              <span class="user-avatar-sm">{{ currentUser.name[0] }}</span>
            </button>
            <div v-if="userMenuOpen" class="user-dropdown-menu" @click.self="userMenuOpen = false">
              <router-link to="/user" @click="menuOpen = false; userMenuOpen = false">个人中心</router-link>
              <button @click="handleLogout">退出登录</button>
            </div>
          </div>
        </template>
        <template v-else>
          <button class="nav-link-btn" @click="showLogin = true">登录</button>
          <button class="nav-link-btn" @click="showRegister = true">注册</button>
        </template>
      </div>
    </div>

    <LoginModal :show="showLogin" @close="showLogin = false" @switch="switchToRegister" @login="onUserLogin" />
    <RegisterModal :show="showRegister" @close="showRegister = false" @switch="switchToLogin" />
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { isUserLoggedIn, getCurrentMemberUser, userLogout } from '@/services/api'
import logoFallback from '@/assets/logo.png'
import LoginModal from '@/components/user/LoginModal.vue'
import RegisterModal from '@/components/user/RegisterModal.vue'

const { config: siteConfig } = useSiteConfigStore()
const isScrolled = ref(false)
const menuOpen = ref(false)
const userMenuOpen = ref(false)

const currentUser = ref(null)
const showLogin = ref(false)
const showRegister = ref(false)

async function checkLogin() {
  if (isUserLoggedIn()) {
    try { currentUser.value = await getCurrentMemberUser() } catch { userLogout() }
  }
}
checkLogin()

function onUserLogin(user) {
  currentUser.value = user
  showLogin.value = false
}

function handleLogout() {
  userLogout()
  currentUser.value = null
  userMenuOpen.value = false
}

function switchToRegister() { showLogin.value = false; showRegister.value = true }
function switchToLogin() { showRegister.value = false; showLogin.value = true }

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

.nav-link-btn {
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.25s;
  position: relative;
}
.nav-link-btn:hover { color: var(--warm-terracotta); }
.nav-link-btn::after {
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
.nav-link-btn:hover::after { width: 100%; }

.user-dropdown { position: relative; }
.user-avatar-btn {
  width: 32px; height: 32px; border-radius: 50%;
  border: 2px solid var(--warm-terracotta); background: var(--warm-terracotta);
  cursor: pointer; display: flex; align-items: center; justify-content: center;
  transition: transform 0.2s;
}
.user-avatar-btn:hover { transform: scale(1.1); }
.user-avatar-sm { color: white; font-size: 14px; font-weight: 700; font-family: var(--font-heading); }
.user-dropdown-menu {
  position: absolute; top: 40px; right: 0;
  background: white; border: 1px solid var(--glass-border); border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg); padding: 8px 0; min-width: 140px; z-index: 200;
}
.user-dropdown-menu a, .user-dropdown-menu button {
  display: block; width: 100%; padding: 8px 16px; text-align: left;
  font-size: 13px; color: var(--text-primary); background: none; border: none; cursor: pointer; text-decoration: none;
}
.user-dropdown-menu a:hover, .user-dropdown-menu button:hover { background: var(--bg-soft); color: var(--warm-terracotta); }

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
