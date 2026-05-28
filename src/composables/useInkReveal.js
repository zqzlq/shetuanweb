import { onMounted, onUnmounted } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

/**
 * 首页 section 滚动入场动画 — 增强版
 */
export function useInkReveal(sectionRef) {
  let ctx

  onMounted(() => {
    if (!sectionRef.value) return

    ctx = gsap.context(() => {
      const section = sectionRef.value
      const glow = section.querySelector('.warm-glow')
      const heading = section.querySelector('.section-heading')
      const cards = section.querySelectorAll('.reveal-card')
      const decoLine = section.querySelector('.section-deco-line')

      // 光晕淡入
      if (glow) {
        gsap.fromTo(glow,
          { opacity: 0 },
          {
            opacity: 1,
            duration: 2,
            ease: 'power2.out',
            scrollTrigger: {
              trigger: section,
              start: 'top 90%',
              once: true,
            },
          }
        )
      }

      // 装饰线展开
      if (decoLine) {
        gsap.fromTo(decoLine,
          { scaleX: 0 },
          {
            scaleX: 1,
            duration: 1.2,
            ease: 'power2.inOut',
            scrollTrigger: {
              trigger: section,
              start: 'top 85%',
              once: true,
            },
          }
        )
      }

      // 标题逐行入场
      if (heading) {
        const eyebrow = heading.querySelector('.eyebrow')
        const h2 = heading.querySelector('h2')
        const desc = heading.querySelector('p:not(.eyebrow)')
        const row = heading.querySelector('.heading-row')
        const tl = gsap.timeline({
          scrollTrigger: {
            trigger: section,
            start: 'top 80%',
            once: true,
          },
        })
        if (eyebrow) tl.fromTo(eyebrow,
          { opacity: 0, x: -30 },
          { opacity: 1, x: 0, duration: 0.6, ease: 'power3.out' }
        )
        if (h2) tl.fromTo(h2,
          { opacity: 0, y: 40, clipPath: 'inset(0 0 100% 0)' },
          { opacity: 1, y: 0, clipPath: 'inset(0 0 0% 0)', duration: 0.8, ease: 'power3.out' },
          '-=0.2'
        )
        if (desc) tl.fromTo(desc,
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration: 0.5 },
          '-=0.3'
        )
      }

      // 卡片依次浮现 — 更有冲击力
      if (cards.length) {
        gsap.fromTo(cards,
          { opacity: 0, y: 80, rotateX: 8 },
          {
            opacity: 1,
            y: 0,
            rotateX: 0,
            duration: 0.8,
            stagger: 0.12,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: section,
              start: 'top 70%',
              once: true,
            },
          }
        )
      }
    }, sectionRef.value)
  })

  onUnmounted(() => {
    ctx?.revert()
  })
}
