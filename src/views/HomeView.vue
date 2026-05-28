<template>
  <div class="home-view">
    <HeroSection v-if="showSection('hero')" />
    <AboutSection v-if="showSection('about')" />
    <MembersSection v-if="showSection('members')" />
    <ProductsSection v-if="showSection('products')" />
    <AwardsSection v-if="showSection('awards')" />
    <OpenSourceSection v-if="showSection('openSource')" />
  </div>
</template>

<script setup>
import HeroSection from '@/components/sections/HeroSection.vue'
import AboutSection from '@/components/sections/AboutSection.vue'
import MembersSection from '@/components/sections/MembersSection.vue'
import ProductsSection from '@/components/sections/ProductsSection.vue'
import AwardsSection from '@/components/sections/AwardsSection.vue'
import OpenSourceSection from '@/components/sections/OpenSourceSection.vue'
import { useSiteConfigStore } from '@/stores/siteConfig'

const store = useSiteConfigStore()
const showSection = (key) => store.sections[key] !== false
</script>

<style scoped>
.home-view {
  padding-bottom: 0;
}

@media (max-width: 768px) {
  .home-view {
    padding-bottom: 0;
  }
}
</style>
