<template>
  <div class="app-root">
    <InkBg v-if="!isAdmin" />
    <LineDogPet v-if="!isAdmin" />
    <Navbar v-if="!isAdmin" />
    <main>
      <router-view v-slot="{ Component, route }">
        <transition
          @before-enter="onBeforeEnter"
          @enter="onEnter"
          @leave="onLeave"
          :css="false"
          mode="out-in"
        >
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </main>
    <Footer v-if="!isAdmin" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import InkBg from '@/components/effects/InkBg.vue'
import LineDogPet from '@/components/effects/LineDogPet.vue'
import Navbar from '@/components/layout/Navbar.vue'
import Footer from '@/components/layout/Footer.vue'

gsap.registerPlugin(ScrollTrigger)

const route = useRoute()
const isAdmin = computed(() => route.path.startsWith('/admin'))

const onBeforeEnter = (el) => {
  gsap.set(el, { opacity: 0, y: 24 })
}
const onEnter = (el, done) => {
  gsap.to(el, { opacity: 1, y: 0, duration: 0.45, ease: 'power2.out', onComplete: done })
}
const onLeave = (el, done) => {
  gsap.to(el, { opacity: 0, y: -16, duration: 0.2, ease: 'power2.in', onComplete: done })
}
</script>
