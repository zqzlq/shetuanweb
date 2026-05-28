import { onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

/**
 * 子页面滚动入场动画 — 增强版
 */
export function useScrollReveal(selector = '.reveal') {
  let ctx

  onMounted(() => {
    ctx = gsap.context(() => {
      gsap.utils.toArray(selector).forEach((el, i) => {
        gsap.from(el, {
          y: 50,
          opacity: 0,
          duration: 0.7,
          ease: 'power3.out',
          delay: i * 0.04,
          scrollTrigger: {
            trigger: el,
            start: 'top 88%',
            toggleActions: 'play none none none',
          },
        })
      })
    })
  })

  onUnmounted(() => {
    ctx?.revert()
  })
}
