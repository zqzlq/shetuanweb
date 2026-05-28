<template>
  <span ref="el">{{ displayValue }}</span>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

const props = defineProps({
  target: { type: [Number, String], required: true },
  duration: { type: Number, default: 1.5 },
  trigger: { type: Boolean, default: true },
})

const el = ref(null)
const displayValue = ref('0')

const numericPart = () => {
  const s = String(props.target)
  const match = s.match(/[\d.]+/)
  return match ? parseFloat(match[0]) : 0
}

const suffix = () => {
  const s = String(props.target)
  return s.replace(/[\d.]+/, '')
}

onMounted(() => {
  if (!props.trigger) {
    displayValue.value = String(props.target)
    return
  }

  const num = numericPart()
  const suf = suffix()
  const obj = { val: 0 }

  gsap.to(obj, {
    val: num,
    duration: props.duration,
    ease: 'power2.out',
    scrollTrigger: {
      trigger: el.value,
      start: 'top 90%',
      once: true,
    },
    onUpdate: () => {
      displayValue.value = (num % 1 === 0 ? Math.round(obj.val) : obj.val.toFixed(1)) + suf
    },
    onComplete: () => {
      displayValue.value = String(props.target)
    },
  })
})
</script>
