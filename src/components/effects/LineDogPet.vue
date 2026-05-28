<template>
  <div
    class="dog-pet"
    :class="{ expanded: showMenu, rolling: isRolling, walking: isWalking, 'face-left': facingLeft, 'at-side': isScrolling && !isWalking }"
    :style="{ left: pos.x + 'px', top: pos.y + 'px' }"
    @click="toggleMenu"
  >
    <!-- 小狗 SVG -->
    <svg class="dog-svg" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- 耳朵 (先画，在头后面) -->
      <!-- 左耳 - 垂耳 -->
      <ellipse cx="38" cy="32" rx="12" ry="18" transform="rotate(-15 38 32)" stroke="#5c4a3a" stroke-width="2" fill="#e8c9a8" class="dog-ear-left"/>
      <ellipse cx="38" cy="32" rx="7" ry="12" transform="rotate(-15 38 32)" fill="#f0d4b8" class="dog-ear-left"/>
      <!-- 右耳 - 垂耳 -->
      <ellipse cx="82" cy="32" rx="12" ry="18" transform="rotate(15 82 32)" stroke="#5c4a3a" stroke-width="2" fill="#e8c9a8" class="dog-ear-right"/>
      <ellipse cx="82" cy="32" rx="7" ry="12" transform="rotate(15 82 32)" fill="#f0d4b8" class="dog-ear-right"/>

      <!-- 身体 -->
      <ellipse cx="60" cy="82" rx="30" ry="24" stroke="#5c4a3a" stroke-width="2" fill="#f5e6d3" class="dog-body"/>
      <!-- 肚皮 -->
      <ellipse cx="60" cy="86" rx="18" ry="16" fill="#faf0e4"/>

      <!-- 头 -->
      <circle cx="60" cy="44" r="28" stroke="#5c4a3a" stroke-width="2" fill="#f5e6d3" class="dog-head"/>
      <!-- 脸部浅色区域 -->
      <ellipse cx="60" cy="50" rx="18" ry="16" fill="#faf0e4"/>

      <!-- 眼睛 - 大圆眼 -->
      <!-- 左眼 -->
      <ellipse cx="49" cy="42" rx="6" ry="6.5" fill="#2c2520" class="dog-eye-left"/>
      <ellipse cx="50.5" cy="40" rx="2.5" ry="2.8" fill="white"/>
      <ellipse cx="47" cy="44" rx="1.2" ry="1.4" fill="white" opacity="0.5"/>
      <!-- 右眼 -->
      <ellipse cx="71" cy="42" rx="6" ry="6.5" fill="#2c2520" class="dog-eye-right"/>
      <ellipse cx="72.5" cy="40" rx="2.5" ry="2.8" fill="white"/>
      <ellipse cx="69" cy="44" rx="1.2" ry="1.4" fill="white" opacity="0.5"/>

      <!-- 腮红 -->
      <ellipse cx="38" cy="52" rx="7" ry="4" fill="#f0a0a0" opacity="0.35"/>
      <ellipse cx="82" cy="52" rx="7" ry="4" fill="#f0a0a0" opacity="0.35"/>

      <!-- 鼻子 -->
      <ellipse cx="60" cy="51" rx="4" ry="3" fill="#5c4a3a"/>
      <ellipse cx="61" cy="50" rx="1.5" ry="1" fill="#8b7355" opacity="0.5"/>

      <!-- 嘴巴 -->
      <path d="M56 54 Q60 58 64 54" stroke="#5c4a3a" stroke-width="1.5" fill="none" stroke-linecap="round"/>

      <!-- 舌头 (开心时显示) -->
      <path v-if="showMenu" d="M58 56 Q60 63 62 56" stroke="#e07070" stroke-width="1.5" fill="#f08080" stroke-linecap="round" class="dog-tongue"/>

      <!-- 项圈 -->
      <path d="M40 68 Q60 74 80 68" stroke="var(--warm-terracotta)" stroke-width="3" fill="none" stroke-linecap="round"/>
      <!-- 项圈铃铛 -->
      <circle cx="60" cy="72" r="4" fill="var(--warm-amber)" stroke="#b8860b" stroke-width="1"/>
      <circle cx="60" cy="72" r="1.5" fill="#daa520"/>

      <!-- 左前腿 -->
      <ellipse cx="46" cy="102" rx="8" ry="6" stroke="#5c4a3a" stroke-width="1.8" fill="#f5e6d3" class="dog-leg-left"/>
      <!-- 右前腿 -->
      <ellipse cx="74" cy="102" rx="8" ry="6" stroke="#5c4a3a" stroke-width="1.8" fill="#f5e6d3" class="dog-leg-right"/>
      <!-- 左爪垫 -->
      <ellipse cx="46" cy="104" rx="4" ry="2.5" fill="#e8c9a8" class="dog-leg-left"/>
      <!-- 右爪垫 -->
      <ellipse cx="74" cy="104" rx="4" ry="2.5" fill="#e8c9a8" class="dog-leg-right"/>

      <!-- 尾巴 -->
      <path d="M88 76 Q102 60 96 72 Q108 58 100 74" stroke="#5c4a3a" stroke-width="2.5" fill="#f5e6d3" stroke-linecap="round" class="dog-tail"/>

      <!-- 头顶呆毛 -->
      <path d="M58 18 Q60 8 64 18" stroke="#5c4a3a" stroke-width="2" fill="#f5e6d3" stroke-linecap="round"/>
    </svg>

    <!-- 骰子 -->
    <div v-if="showDice" class="dice" :class="{ rolling: isRolling }">
      <div class="dice-face">{{ diceResult }}</div>
    </div>

    <!-- 菜单 -->
    <transition name="menu-pop">
      <div v-if="showMenu && !isRolling" class="dog-menu" :class="{ 'menu-left': menuOnLeft, 'menu-below': menuBelow }" @click.stop>
        <div class="menu-title">想去哪里逛逛？</div>
        <div class="menu-dice-row">
          <button class="dice-btn" @click="rollDice">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="2" y="2" width="16" height="16" rx="3" stroke="currentColor" stroke-width="1.5"/><circle cx="6" cy="6" r="1.2" fill="currentColor"/><circle cx="10" cy="10" r="1.2" fill="currentColor"/><circle cx="14" cy="14" r="1.2" fill="currentColor"/></svg>
            投骰子
          </button>
        </div>
        <div class="menu-pages">
          <button v-for="(p, i) in pages" :key="p.path" class="page-btn" @click="goTo(p.path)">
            <span class="page-num">{{ i + 1 }}</span>
            <span>{{ p.name }}</span>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showMenu = ref(false)
const showDice = ref(false)
const isRolling = ref(false)
const diceResult = ref(1)
const isWalking = ref(false)
const facingLeft = ref(false)

const DOG_SIZE = 80
const MARGIN = 24
const pos = reactive({ x: 0, y: 0 })
const isScrolling = ref(false)
const winW = ref(window.innerWidth)
const winH = ref(window.innerHeight)
let walkTimer = null
let idleTimer = null
let scrollTimer = null
let sideX = 0

const pages = [
  { name: '关于社团', path: '/about' },
  { name: '成员风采', path: '/members' },
  { name: '作品展示', path: '/projects' },
  { name: '博客动态', path: '/blog' },
  { name: '开源仓库', path: '/open-source' },
  { name: '时间线', path: '/timeline' },
  { name: '招新详情', path: '/recruitment' },
  { name: '加入我们', path: '/join' },
]

// 菜单方向：如果小狗在右半边，菜单弹到左边
const menuOnLeft = computed(() => pos.x < winW.value / 2)
// 菜单高度约 280px，判断上下空间
const MENU_H = 300
const menuBelow = computed(() => {
  const spaceAbove = pos.y
  const spaceBelow = winH.value - pos.y - DOG_SIZE
  // 上方空间不够且下方空间够 → 弹下面
  if (spaceAbove < MENU_H && spaceBelow >= MENU_H) return true
  // 下方空间不够且上方空间够 → 弹上面（默认）
  if (spaceBelow < MENU_H && spaceAbove >= MENU_H) return false
  // 都够或都不够 → 默认弹上面
  return false
})

const SIDE_LEFT_X = MARGIN
function getSideRightX() {
  return winW.value - DOG_SIZE - MARGIN
}

function clampPos(x, y) {
  const maxX = winW.value - DOG_SIZE - MARGIN
  const maxY = winH.value - DOG_SIZE - MARGIN
  return {
    x: Math.max(MARGIN, Math.min(x, maxX)),
    y: Math.max(MARGIN, Math.min(y, maxY)),
  }
}

function getRandomTarget() {
  const maxX = winW.value - DOG_SIZE - MARGIN
  const maxY = winH.value - DOG_SIZE - MARGIN
  return {
    x: MARGIN + Math.random() * (maxX - MARGIN),
    y: MARGIN + Math.random() * (maxY - MARGIN),
  }
}

function moveToTarget(targetX, targetY, onDone) {
  const dx = targetX - pos.x
  const dy = targetY - pos.y
  const dist = Math.sqrt(dx * dx + dy * dy)

  if (dist < 10) {
    if (onDone) onDone()
    return
  }

  facingLeft.value = dx < 0
  const speed = 400 + Math.random() * 300
  const duration = (dist / speed) * 1000

  isWalking.value = true
  const startX = pos.x
  const startY = pos.y
  const startTime = performance.now()

  function step(now) {
    const elapsed = now - startTime
    const t = Math.min(elapsed / duration, 1)
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t

    pos.x = startX + dx * ease
    pos.y = startY + dy * ease

    if (t < 1) {
      walkTimer = requestAnimationFrame(step)
    } else {
      isWalking.value = false
      if (onDone) onDone()
    }
  }

  walkTimer = requestAnimationFrame(step)
}

function goToSide(onDone) {
  // 移动到最近的侧边
  const leftDist = pos.x - SIDE_LEFT_X
  const rightDist = getSideRightX() - pos.x
  sideX = leftDist <= rightDist ? SIDE_LEFT_X : getSideRightX()
  // y 随机调整一点
  const maxY = winH.value - DOG_SIZE - MARGIN
  const targetY = MARGIN + Math.random() * (maxY - MARGIN)
  moveToTarget(sideX, targetY, onDone)
}

function startWalking() {
  if (showMenu.value || isRolling.value || isScrolling.value) return

  // 正常随机走动
  const target = getRandomTarget()
  const dx = target.x - pos.x
  const dy = target.y - pos.y
  const dist = Math.sqrt(dx * dx + dy * dy)

  if (dist < 60) {
    scheduleNext()
    return
  }

  moveToTarget(target.x, target.y, () => scheduleNext())
}

function scheduleNext() {
  // 滚动中不安排下一次走动
  if (isScrolling.value) return
  // 走完后休息 2~6 秒
  const wait = 2000 + Math.random() * 4000
  idleTimer = setTimeout(() => {
    startWalking()
  }, wait)
}

function stopWalking() {
  if (walkTimer) {
    cancelAnimationFrame(walkTimer)
    walkTimer = null
  }
  if (idleTimer) {
    clearTimeout(idleTimer)
    idleTimer = null
  }
  isWalking.value = false
}

function toggleMenu() {
  if (isRolling.value) return
  showMenu.value = !showMenu.value
  if (showMenu.value) {
    stopWalking()
  } else {
    scheduleNext()
  }
}

function goTo(path) {
  showMenu.value = false
  router.push(path)
  scheduleNext()
}

function rollDice() {
  if (isRolling.value) return
  isRolling.value = true
  showDice.value = true
  showMenu.value = false

  let count = 0
  const total = 15
  const interval = setInterval(() => {
    diceResult.value = Math.floor(Math.random() * pages.length) + 1
    count++
    if (count >= total) {
      clearInterval(interval)
      const finalIndex = diceResult.value - 1
      setTimeout(() => {
        isRolling.value = false
        showDice.value = false
        router.push(pages[finalIndex].path)
        scheduleNext()
      }, 600)
    }
  }, 80)
}

// 滚动时靠边
let hasMovedToSide = false

function onScroll() {
  if (showMenu.value || isRolling.value) return

  // 清除之前的 debounce
  if (scrollTimer) clearTimeout(scrollTimer)

  // 只在滚动开始时移动一次到侧边
  if (!hasMovedToSide) {
    hasMovedToSide = true
    isScrolling.value = true
    stopWalking()
    goToSide()
  }

  // 滚动停止 2 秒后恢复随机走动
  scrollTimer = setTimeout(() => {
    hasMovedToSide = false
    isScrolling.value = false
    scheduleNext()
  }, 2000)
}

// 窗口大小变化时修正位置
function onResize() {
  winW.value = window.innerWidth
  winH.value = window.innerHeight
  const clamped = clampPos(pos.x, pos.y)
  pos.x = clamped.x
  pos.y = clamped.y
  // 如果正在靠边，更新 sideX
  if (isScrolling.value) {
    sideX = pos.x
  }
}

onMounted(() => {
  // 初始位置：右下角
  const clamped = clampPos(
    winW.value - DOG_SIZE - MARGIN,
    winH.value - DOG_SIZE - MARGIN
  )
  pos.x = clamped.x
  pos.y = clamped.y
  sideX = pos.x

  window.addEventListener('resize', onResize)
  window.addEventListener('scroll', onScroll, { passive: true })
  // 3 秒后开始随机走动
  idleTimer = setTimeout(startWalking, 3000)
})

onBeforeUnmount(() => {
  stopWalking()
  if (scrollTimer) clearTimeout(scrollTimer)
  window.removeEventListener('resize', onResize)
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.dog-pet {
  position: fixed;
  z-index: 99;
  cursor: pointer;
  user-select: none;
  -webkit-user-select: none;
  transition: none;
}

/* 面朝左时翻转 */
.dog-pet.face-left .dog-svg {
  transform: scaleX(-1);
}

.dog-svg {
  width: 80px;
  height: 80px;
  filter: drop-shadow(0 4px 12px rgba(120, 90, 60, 0.15));
  transition: transform 0.3s ease;
  animation: dog-idle 3s ease-in-out infinite;
}

.dog-pet:hover .dog-svg {
  transform: scale(1.08);
}

.dog-pet.face-left:hover .dog-svg {
  transform: scaleX(-1) scale(1.08);
}

.dog-pet.expanded .dog-svg {
  animation: dog-bounce 0.4s ease;
}

.dog-pet.expanded.face-left .dog-svg {
  animation: dog-bounce-left 0.4s ease;
}

/* 待机动画 */
@keyframes dog-idle {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

@keyframes dog-bounce {
  0% { transform: scale(1); }
  40% { transform: scale(1.15); }
  70% { transform: scale(0.95); }
  100% { transform: scale(1); }
}

@keyframes dog-bounce-left {
  0% { transform: scaleX(-1) scale(1); }
  40% { transform: scaleX(-1) scale(1.15); }
  70% { transform: scaleX(-1) scale(0.95); }
  100% { transform: scaleX(-1) scale(1); }
}

/* 行走动画 */
.dog-pet.walking .dog-svg {
  animation: dog-walk 0.35s ease-in-out infinite;
}

.dog-pet.walking.face-left .dog-svg {
  animation: dog-walk-left 0.35s ease-in-out infinite;
}

@keyframes dog-walk {
  0%, 100% { transform: translateY(0) rotate(0); }
  25% { transform: translateY(-5px) rotate(2deg); }
  75% { transform: translateY(-5px) rotate(-2deg); }
}

@keyframes dog-walk-left {
  0%, 100% { transform: scaleX(-1) translateY(0) rotate(0); }
  25% { transform: scaleX(-1) translateY(-5px) rotate(2deg); }
  75% { transform: scaleX(-1) translateY(-5px) rotate(-2deg); }
}

/* 行走时腿部抖动 */
.dog-pet.walking .dog-leg-left {
  animation: leg-step 0.35s ease-in-out infinite;
}

.dog-pet.walking .dog-leg-right {
  animation: leg-step 0.35s ease-in-out infinite 0.175s;
}

@keyframes leg-step {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

/* 行走时尾巴更欢快 */
.dog-pet.walking .dog-tail {
  animation-duration: 0.2s;
}

/* 尾巴摇摆 */
.dog-tail {
  transform-origin: 88px 76px;
  animation: tail-wag 0.6s ease-in-out infinite alternate;
}

@keyframes tail-wag {
  0% { transform: rotate(-10deg); }
  100% { transform: rotate(15deg); }
}

.dog-pet:hover .dog-tail {
  animation-duration: 0.25s;
}

/* 眨眼 */
.dog-eye-left, .dog-eye-right {
  animation: blink 4s ease-in-out infinite;
}

@keyframes blink {
  0%, 42%, 46%, 100% { ry: 2.5; }
  44% { ry: 0.3; }
}

/* 耳朵抖动 */
.dog-ear-left {
  transform-origin: 38px 20px;
  animation: ear-twitch 5s ease-in-out infinite;
}

.dog-ear-right {
  transform-origin: 82px 20px;
  animation: ear-twitch 5s ease-in-out infinite 0.3s;
}

@keyframes ear-twitch {
  0%, 90%, 100% { transform: rotate(0); }
  93% { transform: rotate(-8deg); }
  96% { transform: rotate(3deg); }
}

/* 骰子 */
.dice {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background: #fff;
  border: 2px solid var(--warm-terracotta);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
  animation: dice-appear 0.3s ease;
}

.dice.rolling {
  animation: dice-shake 0.08s linear infinite;
}

.dice-face {
  font-family: var(--font-heading);
  font-size: 20px;
  font-weight: 700;
  color: var(--warm-terracotta);
}

@keyframes dice-appear {
  from { transform: translateX(-50%) scale(0) rotate(-180deg); }
  to { transform: translateX(-50%) scale(1) rotate(0); }
}

@keyframes dice-shake {
  0% { transform: translateX(-50%) rotate(-10deg); }
  25% { transform: translateX(-50%) rotate(10deg); }
  50% { transform: translateX(-50%) rotate(-8deg); }
  75% { transform: translateX(-50%) rotate(8deg); }
  100% { transform: translateX(-50%) rotate(-10deg); }
}

/* 菜单 */
.dog-menu {
  position: absolute;
  bottom: 90px;
  right: 0;
  width: 220px;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 16px;
  box-shadow: var(--shadow-xl);
  cursor: default;
}

.dog-menu.menu-left {
  right: auto;
  left: 0;
}

.dog-menu.menu-left::after {
  right: auto;
  left: 28px;
}

/* 菜单弹到下面 */
.dog-menu.menu-below {
  bottom: auto;
  top: 90px;
}

.dog-menu.menu-below::after {
  bottom: auto;
  top: -8px;
  border-right: none;
  border-bottom: none;
  border-left: 1px solid var(--glass-border);
  border-top: 1px solid var(--glass-border);
}

.dog-menu::after {
  content: '';
  position: absolute;
  bottom: -8px;
  right: 28px;
  width: 16px;
  height: 16px;
  background: #fff;
  border-right: 1px solid var(--glass-border);
  border-bottom: 1px solid var(--glass-border);
  transform: rotate(45deg);
}

.menu-title {
  font-family: var(--font-heading);
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
  text-align: center;
}

.menu-dice-row {
  margin-bottom: 12px;
}

.dice-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  border: 2px dashed var(--warm-terracotta);
  border-radius: var(--radius-md);
  background: rgba(192, 96, 64, 0.04);
  color: var(--warm-terracotta);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.dice-btn:hover {
  background: rgba(192, 96, 64, 0.1);
  transform: scale(1.02);
}

.menu-pages {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.page-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-sm);
  background: #fff;
  font-size: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover {
  background: var(--bg-soft);
  border-color: var(--warm-terracotta);
  color: var(--warm-terracotta);
}

.page-num {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  flex-shrink: 0;
}

.page-btn:hover .page-num {
  background: var(--warm-terracotta);
  color: #fff;
}

/* 靠边待机 - 更安静 */
.dog-pet.at-side .dog-svg {
  animation: dog-idle 4s ease-in-out infinite;
  opacity: 0.85;
  transform: scale(0.9);
}

.dog-pet.at-side.face-left .dog-svg {
  transform: scaleX(-1) scale(0.9);
}

.dog-pet.at-side:hover .dog-svg {
  opacity: 1;
  transform: scaleX(-1) scale(1.08);
}

.dog-pet.at-side .dog-tail {
  animation-duration: 1.2s;
}

/* 菜单弹出动画 */
.menu-pop-enter-active {
  animation: menu-pop-in 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.menu-pop-leave-active {
  animation: menu-pop-in 0.2s ease reverse;
}

@keyframes menu-pop-in {
  from { opacity: 0; transform: translateY(12px) scale(0.9); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@media (max-width: 640px) {
  .dog-svg {
    width: 64px;
    height: 64px;
  }
  .dog-menu {
    width: 200px;
    right: -8px;
  }
  .dog-menu.menu-left {
    right: auto;
    left: -8px;
  }
}
</style>
