<template>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <img :src="siteConfig.footer.logo || logoFallback" alt="星雨作坊" class="footer-logo-img" />
          <div>
            <div class="footer-name">{{ siteConfig.footer.brand }}</div>
            <div class="footer-slogan">{{ siteConfig.footer.slogan }}</div>
          </div>
        </div>
        <div class="footer-links">
          <router-link to="/about">关于</router-link>
          <router-link to="/members">成员</router-link>
          <router-link to="/projects">项目</router-link>
          <router-link to="/blog">动态/公告</router-link>
          <router-link to="/contact">联系我们</router-link>
          <router-link to="/join">加入</router-link>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; {{ new Date().getFullYear() }} {{ siteConfig.footer.brand }}</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useSiteConfigStore } from '@/stores/siteConfig'
import logoFallback from '@/assets/logo.png'
const { config: siteConfig } = useSiteConfigStore()
</script>

<style scoped>
.site-footer {
  padding: 48px 0 32px;
  border-top: 1px solid var(--glass-border);
  margin-top: var(--section-gap);
}

.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.footer-logo-img {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
}

.footer-name {
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 15px;
  color: var(--text-primary);
}

.footer-slogan {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 2px;
}

.footer-links {
  display: flex;
  gap: 24px;
}

.footer-links a {
  font-size: 13px;
  color: var(--text-muted);
  transition: color 0.2s;
}

.footer-links a:hover {
  color: var(--text-primary);
}

.footer-bottom {
  padding-top: 20px;
  border-top: 1px solid var(--glass-border);
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
}

@media (max-width: 640px) {
  .footer-inner {
    flex-direction: column;
    gap: 24px;
    text-align: center;
  }

  .footer-brand {
    flex-direction: column;
  }

  .footer-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 16px;
  }
}
</style>
