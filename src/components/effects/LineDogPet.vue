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
      <div v-if="showMenu && !isRolling" class="dog-menu" :style="menuStyle.pos" @click.stop>
        <div class="dog-menu-arrow" :style="menuStyle.arrow"></div>
        <div class="menu-title">想去哪里逛逛？</div>
        <div class="menu-dice-row">
          <button class="dice-btn" @click="rollDice">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="2" y="2" width="16" height="16" rx="3" stroke="currentColor" stroke-width="1.5"/><circle cx="6" cy="6" r="1.2" fill="currentColor"/><circle cx="10" cy="10" r="1.2" fill="currentColor"/><circle cx="14" cy="14" r="1.2" fill="currentColor"/></svg>
            投骰子
          </button>
          <button v-if="isLoggedIn" class="dice-btn ai-btn" @click="openChat">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 12h8M12 8v8"/></svg>
            资源助手
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

  <!-- AI 聊天面板 -->
  <Teleport to="body">
    <Transition name="chat-panel">
      <div v-if="showChat" class="dog-chat-panel" :style="chatPanelStyle">
        <!-- 头部（可拖动） -->
        <div class="chat-header" @mousedown="startDrag" @touchstart.prevent="startDrag">
          <div class="chat-header-left">
            <img :src="logoImg" alt="AI" class="chat-header-logo" />
            <div class="chat-header-info">
              <span class="chat-header-title">资源助手</span>
              <span v-if="chatStreaming" class="chat-header-status">正在思考</span>
              <span v-else class="chat-header-status online">在线</span>
            </div>
          </div>
          <div class="chat-header-actions">
            <button class="chat-header-btn" @click="clearChat" title="清空对话">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>
            </button>
            <button class="chat-header-btn" @click="showChat=false" title="关闭">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>
            </button>
          </div>
        </div>

        <!-- 消息列表 -->
        <div class="chat-messages" ref="chatMsgRef">
          <!-- 欢迎页 -->
          <div v-if="chatMessages.length === 0" class="chat-welcome">
            <img :src="logoImg" alt="AI" class="chat-welcome-logo" />
            <div class="chat-welcome-title">资源助手</div>
            <div class="chat-welcome-desc">帮你查找资料、查看统计、推荐资源</div>
            <div class="chat-quick-btns">
              <button v-for="q in quickQuestions" :key="q" class="chat-quick-btn" @click="sendQuickChat(q)">
                <span class="chat-quick-icon">Q</span>
                <span>{{ q }}</span>
              </button>
            </div>
          </div>

          <template v-for="(msg, i) in chatMessages" :key="i">
            <!-- 加载动画 -->
            <div v-if="msg.type === 'loading'" class="chat-msg chat-msg-assistant">
              <div class="chat-msg-body chat-loading">
                <span></span><span></span><span></span>
              </div>
            </div>

            <!-- 文本消息 -->
            <div v-if="msg.type === 'text' && msg.content" class="chat-msg" :class="'chat-msg-'+msg.role">
              <div class="chat-msg-body" v-html="renderChatMd(msg.content)"></div>
            </div>

            <!-- 资源卡片 -->
            <div v-if="msg.type === 'resources' && msg.resources?.length" class="chat-msg chat-msg-assistant">
              <div class="chat-card-header">
                <span class="chat-card-title">找到 {{ msg.resources.length }} 个资源</span>
              </div>
              <div class="chat-resources">
                <div v-for="r in msg.resources" :key="r.id" class="chat-res-card" @click="goToResource(r.parent_id)" title="点击定位到资源中心">
                  <div class="chat-res-icon">{{ getFileIcon(r.file_ext) }}</div>
                  <div class="chat-res-info">
                    <div class="chat-res-name">{{ r.original_name || r.name }}</div>
                    <div class="chat-res-meta">
                      <span v-if="r.size">{{ r.size }}</span>
                      <span v-if="r.uploader">{{ r.uploader }}</span>
                      <span class="chat-res-locate">点击定位</span>
                    </div>
                  </div>
                  <div class="chat-res-actions">
                    <button class="chat-res-btn" @click.stop="downloadRes(r.id)" title="下载">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
                    </button>
                    <button class="chat-res-btn" @click.stop="shareResource(r)" title="分享">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 统计卡片 -->
            <div v-if="msg.type === 'stats'" class="chat-msg chat-msg-assistant">
              <div class="chat-stats">
                <div class="chat-stat-item">
                  <div class="chat-stat-val">{{ msg.stats.total_files }}</div>
                  <div class="chat-stat-label">文件</div>
                </div>
                <div class="chat-stat-item">
                  <div class="chat-stat-val">{{ msg.stats.total_folders }}</div>
                  <div class="chat-stat-label">文件夹</div>
                </div>
                <div class="chat-stat-item">
                  <div class="chat-stat-val">{{ msg.stats.total_size }}</div>
                  <div class="chat-stat-label">总大小</div>
                </div>
              </div>
              <div v-if="msg.stats.popular_resources?.length" class="chat-popular">
                <div class="chat-popular-title">热门资源</div>
                <div v-for="(p, j) in msg.stats.popular_resources" :key="j" class="chat-popular-item">
                  <span class="chat-popular-rank">{{ j + 1 }}</span>
                  <span class="chat-popular-name">{{ p.name }}</span>
                  <span class="chat-popular-dl">{{ p.downloads }} 次下载</span>
                </div>
              </div>
            </div>

            <!-- 文件夹列表 -->
            <div v-if="msg.type === 'folders' && msg.folders?.length" class="chat-msg chat-msg-assistant">
              <div class="chat-card-header">
                <span class="chat-card-title">{{ msg.folders.length }} 个文件夹</span>
              </div>
              <div class="chat-folders">
                <button v-for="f in msg.folders.slice(0, 10)" :key="f.id" class="chat-folder-btn" @click="navigateToFolder(f.id)">
                  <span class="chat-folder-icon">{{ f.path.includes('/') ? '📂' : '📁' }}</span>
                  <span class="chat-folder-path">{{ f.path }}</span>
                </button>
                <div v-if="msg.folders.length > 10" class="chat-folders-more">还有 {{ msg.folders.length - 10 }} 个...</div>
              </div>
            </div>
          </template>
        </div>

        <!-- 输入区 -->
        <div class="chat-input-area">
          <textarea
            ref="chatInputRef"
            v-model="chatInput"
            @keydown="chatKeydown"
            @input="autoResize"
            placeholder="输入消息..."
            class="chat-input"
            rows="1"
            :disabled="chatStreaming"
          ></textarea>
          <button class="chat-send" @click="sendChatMsg" :disabled="!chatInput.trim()||chatStreaming">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m22 2-7 20-4-9-9-4z"/></svg>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { marked } from 'marked'
import { isUserLoggedIn, getUserToken } from '@/services/api'

const logoImg = 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/5ab0547bffef4a0986baac8e245c4401.png'
const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const router = useRouter()
const isLoggedIn = ref(isUserLoggedIn())
const showMenu = ref(false)
const showDice = ref(false)
const isRolling = ref(false)
const diceResult = ref(1)
const isWalking = ref(false)
const facingLeft = ref(false)

const DOG_SIZE = 80
const MARGIN = 40
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

// 菜单弹出方向：始终朝向屏幕中心，且保证不超出可视区域
const MENU_W = 232  // 220 + padding 12
const MENU_H = 340
const menuStyle = computed(() => {
  const dogCenterX = pos.x + DOG_SIZE / 2
  const halfW = winW.value / 2

  // 水平方向：狗在左边→菜单在右边，狗在右边→菜单在左边
  const goRight = dogCenterX < halfW
  let left
  if (goRight) {
    // 菜单左边对齐狗的左边
    left = 0
    // 不超出右边界
    const menuRight = pos.x + MENU_W
    if (menuRight > winW.value - 12) left = winW.value - 12 - pos.x - MENU_W
  } else {
    // 菜单右边对齐狗的右边
    left = DOG_SIZE - MENU_W
    // 不超出左边界
    if (pos.x + left < 12) left = -pos.x + 12
  }

  // 垂直方向：优先上方，空间不够则下方
  const spaceAbove = pos.y
  const spaceBelow = winH.value - pos.y - DOG_SIZE
  let top
  let arrowOnBottom = true
  if (spaceAbove >= MENU_H + 12) {
    top = -MENU_H - 10
    arrowOnBottom = true
  } else if (spaceBelow >= MENU_H + 12) {
    top = DOG_SIZE + 10
    arrowOnBottom = false
  } else {
    // 都不够，选空间大的一侧
    if (spaceAbove >= spaceBelow) {
      top = -MENU_H - 10
      arrowOnBottom = true
    } else {
      top = DOG_SIZE + 10
      arrowOnBottom = false
    }
  }

  // 箭头水平位置：指向狗的中心
  const arrowLeft = Math.max(16, Math.min(MENU_W - 16, dogCenterX - pos.x - left - 8))

  const posStyle = { position: 'absolute', left: left + 'px', top: top + 'px' }
  const arrowStyle = {
    left: arrowLeft + 'px',
    ...(arrowOnBottom
      ? { bottom: '-8px', borderTop: '8px solid white', borderLeft: '8px solid transparent', borderRight: '8px solid transparent', borderBottom: 'none' }
      : { top: '-8px', borderBottom: '8px solid white', borderLeft: '8px solid transparent', borderRight: '8px solid transparent', borderTop: 'none' })
  }

  return { pos: posStyle, arrow: arrowStyle }
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

// ─── AI 聊天 ───
const showChat = ref(false)
const chatPanelPos = reactive({ x: 0, y: 0 })
const chatPanelInitPos = reactive({ x: 0, y: 0 })
const isDragging = ref(false)
const dragOffset = reactive({ x: 0, y: 0 })
const chatMessages = ref([])
const chatInput = ref('')
const chatStreaming = ref(false)
const chatMsgRef = ref(null)
const chatInputRef = ref(null)
const quickQuestions = ['最近上传了哪些资料？', '帮我找找 Python 相关的资源', '资源中心有多少文件？']

// 节流滚动，避免流式输出时频繁滚动导致卡顿
let scrollRaf = null
function chatScrollBottom() {
  if (scrollRaf) return
  scrollRaf = requestAnimationFrame(() => {
    scrollRaf = null
    if (chatMsgRef.value) chatMsgRef.value.scrollTop = chatMsgRef.value.scrollHeight
  })
}

// 自动调整输入框高度
function autoResize(e) {
  const el = e.target
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 80) + 'px'
}

// 聊天面板样式（支持拖拽定位，默认右下角）
const chatPanelStyle = computed(() => {
  if (chatPanelPos.x === 0 && chatPanelPos.y === 0) {
    return { right: '24px', bottom: '100px' }
  }
  return {
    left: chatPanelPos.x + 'px',
    top: chatPanelPos.y + 'px',
    right: 'auto',
    bottom: 'auto',
  }
})

function openChat() {
  showMenu.value = false
  // 重置位置（默认右下角）
  chatPanelPos.x = 0
  chatPanelPos.y = 0
  showChat.value = true
  stopWalking()
  nextTick(() => {
    if (chatMsgRef.value) chatMsgRef.value.scrollTop = chatMsgRef.value.scrollHeight
    if (chatInputRef.value) chatInputRef.value.focus()
  })
}

// 拖拽逻辑
function startDrag(e) {
  // 如果点击的是按钮，不触发拖拽
  if (e.target.closest('.chat-header-btn')) return

  isDragging.value = true
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY

  // 如果面板还没有用绝对定位，先转换
  if (chatPanelPos.x === 0 && chatPanelPos.y === 0) {
    const panel = document.querySelector('.dog-chat-panel')
    if (panel) {
      const rect = panel.getBoundingClientRect()
      chatPanelPos.x = rect.left
      chatPanelPos.y = rect.top
    }
  }

  dragOffset.x = clientX - chatPanelPos.x
  dragOffset.y = clientY - chatPanelPos.y

  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchmove', onDrag, { passive: false })
  document.addEventListener('touchend', stopDrag)
}

function onDrag(e) {
  if (!isDragging.value) return
  e.preventDefault()
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY

  // 限制在窗口范围内
  const panel = document.querySelector('.dog-chat-panel')
  const w = panel ? panel.offsetWidth : 400
  const h = panel ? panel.offsetHeight : 540

  chatPanelPos.x = Math.max(0, Math.min(clientX - dragOffset.x, winW.value - w))
  chatPanelPos.y = Math.max(0, Math.min(clientY - dragOffset.y, winH.value - h))
}

function stopDrag() {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', stopDrag)
}

function clearChat() { chatMessages.value = [] }

function renderChatMd(text) {
  if (!text) return ''
  try { return marked(text, { breaks: true }) } catch { return text }
}

function chatKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChatMsg() }
}

function sendQuickChat(q) { chatInput.value = q; sendChatMsg() }

async function sendChatMsg() {
  const text = chatInput.value.trim()
  if (!text || chatStreaming.value) return
  chatInput.value = ''
  // 重置输入框高度
  if (chatInputRef.value) chatInputRef.value.style.height = 'auto'
  chatStreaming.value = true

  // 添加用户消息
  chatMessages.value.push({ role: 'user', type: 'text', content: text })
  // 添加加载动画
  const loadingIdx = chatMessages.value.length
  chatMessages.value.push({ role: 'assistant', type: 'loading' })
  chatScrollBottom()

  // 构建历史（只取文本消息，排除资源卡片等结构化数据，避免重复显示）
  const history = chatMessages.value
    .filter(m => m.type === 'text' && m.content?.trim())
    .slice(-20)
    .map(m => ({ role: m.role, content: m.content }))

  try {
    const token = getUserToken()
    const res = await fetch(`${API_BASE}/resources/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: JSON.stringify({ message: text, history }),
    })
    if (!res.ok) {
      const e = await res.json().catch(() => ({}))
      throw new Error(e.message || '请求失败')
    }

    // 替换加载动画为文本消息
    chatMessages.value[loadingIdx] = { role: 'assistant', type: 'text', content: '' }
    let full = ''
    let currentEvent = 'text'
    // 缓存结构化数据，等文字回复结束后再显示
    const pendingCards = []
    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('event: ')) {
          currentEvent = line.slice(7).trim()
          continue
        }
        if (!line.startsWith('data: ')) continue
        try {
          const d = JSON.parse(line.slice(6))

          if (currentEvent === 'text' && d.content !== undefined) {
            full += d.content
            chatMessages.value[loadingIdx] = { role: 'assistant', type: 'text', content: full }
            chatScrollBottom()
          } else if (currentEvent === 'resources' && d.resources?.length) {
            // 缓存，不立即显示
            pendingCards.push({ role: 'assistant', type: 'resources', resources: d.resources })
          } else if (currentEvent === 'stats') {
            pendingCards.push({ role: 'assistant', type: 'stats', stats: d })
          } else if (currentEvent === 'folders' && d.folders?.length) {
            pendingCards.push({ role: 'assistant', type: 'folders', folders: d.folders })
          } else if (d.message && d.message.includes('未配置')) {
            chatMessages.value[loadingIdx] = { role: 'assistant', type: 'text', content: 'AI 未配置，请在管理端系统设置中填写 API Key。' }
          }
        } catch {}
      }
    }

    // 文字回复结束后，显示缓存的卡片
    if (pendingCards.length > 0) {
      // 等文字渲染完成后再添加卡片
      await nextTick()
      for (const card of pendingCards) {
        chatMessages.value.push(card)
      }
      chatScrollBottom()
    }

    // 如果文本消息为空且没有卡片，移除空消息
    if (!chatMessages.value[loadingIdx]?.content?.trim() && pendingCards.length === 0) {
      chatMessages.value.splice(loadingIdx, 1)
    }
  } catch (err) {
    chatMessages.value[loadingIdx] = { role: 'assistant', type: 'text', content: `请求失败: ${err.message || '未知错误'}` }
  } finally {
    chatStreaming.value = false
    chatScrollBottom()
  }
}

// 文件图标
function getFileIcon(ext) {
  const e = (ext || '').toLowerCase()
  if (['pdf'].includes(e)) return '📄'
  if (['doc', 'docx', 'rtf'].includes(e)) return '📝'
  if (['xls', 'xlsx', 'csv'].includes(e)) return '📊'
  if (['ppt', 'pptx'].includes(e)) return '📑'
  if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(e)) return '🖼'
  if (['zip', 'rar', '7z', 'tar', 'gz'].includes(e)) return '📦'
  if (['py', 'js', 'ts', 'html', 'css', 'json'].includes(e)) return '💻'
  if (['mp4', 'mp3', 'wav'].includes(e)) return '🎬'
  return '📄'
}

// 下载资源
async function downloadRes(id) {
  if (!id) return
  try {
    const token = getUserToken()
    const res = await fetch(`${API_BASE}/resources/${id}/download`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
    if (!res.ok) throw new Error('下载失败')
    const blob = await res.blob()
    const disposition = res.headers.get('Content-Disposition') || ''
    const match = disposition.match(/filename\*=UTF-8''(.+)/i)
    const filename = match ? decodeURIComponent(match[1]) : 'download'
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  } catch (err) {
    alert(err.message || '下载失败')
  }
}

// 跳转到文件夹
function navigateToFolder(folderId) {
  if (!folderId) return
  showChat.value = false
  router.push({ path: '/resources', query: { folder: folderId } })
}

// 点击资源卡片 → 跳转到资源中心该资源所在文件夹（不关闭聊天面板）
function goToResource(parentId) {
  if (parentId) {
    router.push({ path: '/resources', query: { folder: parentId } })
  } else {
    router.push('/resources')
  }
}

// 复制文本到剪贴板（兼容非 HTTPS 环境）
function copyToClipboard(text) {
  // 优先用 Clipboard API
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text)
  }
  // 降级：临时 textarea
  return new Promise((resolve, reject) => {
    const ta = document.createElement('textarea')
    ta.value = text
    ta.style.cssText = 'position:fixed;left:-9999px;top:-9999px'
    document.body.appendChild(ta)
    ta.select()
    try {
      document.execCommand('copy') ? resolve() : reject(new Error('execCommand failed'))
    } catch (e) {
      reject(e)
    } finally {
      document.body.removeChild(ta)
    }
  })
}

// 分享资源（复制分享链接）
async function shareResource(r) {
  if (!r) return
  try {
    const token = getUserToken()
    const res = await fetch(`${API_BASE}/resources/${r.id}/share`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    })
    if (!res.ok) throw new Error('分享失败')
    const data = await res.json()
    const shareUrl = `${window.location.origin}/share/${data.token}`
    await copyToClipboard(shareUrl)
    alert('分享链接已复制到剪贴板')
  } catch (err) {
    alert('分享失败: ' + (err.message || '未知错误'))
  }
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
  window.addEventListener('storage', () => { isLoggedIn.value = isUserLoggedIn() })
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
.dog-pet.expanded {
  z-index: 110;
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
  width: 220px;
  background: #fff;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 16px;
  box-shadow: var(--shadow-xl);
  cursor: default;
  z-index: 1;
}

.dog-menu-arrow {
  position: absolute;
  width: 0;
  height: 0;
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
  display: flex;
  gap: 6px;
}

.dice-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
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
  }
}

/* AI 按钮 */
.ai-btn {
  border-style: solid;
  border-color: var(--warm-terracotta);
  background: var(--warm-terracotta);
  color: white;
}
.ai-btn:hover { background: #a85030; border-color: #a85030; }

/* ─── AI 聊天面板 ─── */
.dog-chat-panel {
  position: fixed;
  bottom: 100px;
  right: 24px;
  width: 400px;
  height: 540px;
  background: rgba(255,253,250,.97);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(0,0,0,.08);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,.12), 0 4px 20px rgba(0,0,0,.06);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 100;
}

.chat-panel-enter-active { animation: chat-slide-up .25s ease; }
.chat-panel-leave-active { animation: chat-slide-up .2s ease reverse; }
@keyframes chat-slide-up { from { opacity: 0; transform: translateY(12px) scale(.96); } to { opacity: 1; transform: translateY(0) scale(1); } }

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid rgba(0,0,0,.06);
  background: linear-gradient(180deg, rgba(255,255,255,.95) 0%, rgba(250,248,245,.95) 100%);
  cursor: move;
  user-select: none;
  -webkit-user-select: none;
}
.chat-header-left { display: flex; align-items: center; gap: 10px; }
.chat-header-logo { width: 28px; height: 28px; object-fit: contain; border-radius: 6px; }
.chat-header-info { display: flex; flex-direction: column; }
.chat-header-title { font-size: 14px; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
.chat-header-status { font-size: 10px; color: var(--text-muted); animation: pulse 1.5s infinite; }
.chat-header-status.online { color: #4ade80; animation: none; }
.chat-header-status.online::before { content: ''; display: inline-block; width: 5px; height: 5px; border-radius: 50%; background: #4ade80; margin-right: 4px; vertical-align: middle; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: .4; } }
.chat-header-actions { display: flex; gap: 2px; }
.chat-header-btn {
  border: none;
  background: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 6px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  transition: all .15s;
}
.chat-header-btn:hover { background: rgba(0,0,0,.05); color: var(--text-primary); }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(0,0,0,.1); border-radius: 4px; }

.chat-welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  text-align: center;
  gap: 8px;
  padding: 20px 0;
}
.chat-welcome-logo { width: 48px; height: 48px; object-fit: contain; border-radius: 12px; margin-bottom: 4px; }
.chat-welcome-title { font-size: 16px; font-weight: 700; color: var(--text-primary); font-family: var(--font-heading); }
.chat-welcome-desc { font-size: 12px; color: var(--text-muted); margin-bottom: 12px; }
.chat-quick-btns { display: flex; flex-direction: column; gap: 6px; width: 100%; padding: 0 4px; }
.chat-quick-btn {
  border: 1px solid rgba(0,0,0,.06);
  background: white;
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 12.5px;
  color: var(--text-primary);
  cursor: pointer;
  text-align: left;
  transition: all .2s;
  display: flex;
  align-items: center;
  gap: 10px;
}
.chat-quick-icon {
  width: 20px; height: 20px; border-radius: 6px;
  background: rgba(192,96,64,.08); color: var(--warm-terracotta);
  font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.chat-quick-btn:hover {
  border-color: var(--warm-terracotta);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(192,96,64,.08);
}
.chat-quick-btn:hover .chat-quick-icon { background: rgba(192,96,64,.15); }

.chat-msg { max-width: 92%; animation: msg-in .3s ease; }
@keyframes msg-in { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.chat-msg-user { align-self: flex-end; }
.chat-msg-assistant { align-self: flex-start; max-width: 95%; }
.chat-msg-body {
  font-size: 13px;
  line-height: 1.75;
  padding: 10px 14px;
  border-radius: 16px;
  word-break: break-word;
}
.chat-msg-user .chat-msg-body {
  background: linear-gradient(135deg, var(--warm-terracotta) 0%, #d4725a 100%);
  color: white;
  border-bottom-right-radius: 4px;
  box-shadow: 0 2px 8px rgba(192,96,64,.2);
}
.chat-msg-assistant .chat-msg-body {
  background: white;
  color: var(--text-primary);
  border-bottom-left-radius: 4px;
  border: 1px solid rgba(0,0,0,.06);
  box-shadow: 0 1px 4px rgba(0,0,0,.04);
}

/* 加载动画 */
.chat-loading {
  display: flex;
  gap: 4px;
  padding: 12px 18px;
  background: white;
  border: 1px solid rgba(0,0,0,.06);
  border-radius: 16px;
  border-bottom-left-radius: 4px;
}
.chat-loading span {
  width: 7px; height: 7px;
  background: var(--warm-terracotta);
  border-radius: 50%;
  animation: loading-bounce 1.4s infinite ease-in-out;
}
.chat-loading span:nth-child(1) { animation-delay: 0s; }
.chat-loading span:nth-child(2) { animation-delay: .2s; }
.chat-loading span:nth-child(3) { animation-delay: .4s; }
@keyframes loading-bounce {
  0%, 80%, 100% { transform: scale(0); opacity: .3; }
  40% { transform: scale(1); opacity: 1; }
}

/* 卡片标题 */
.chat-card-header {
  padding: 6px 14px;
  margin-bottom: 6px;
}
.chat-card-title {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: .5px;
}

/* markdown 渲染样式 */
.chat-msg-body :deep(p) { margin: 0 0 8px; }
.chat-msg-body :deep(p:last-child) { margin-bottom: 0; }
.chat-msg-body :deep(strong) { font-weight: 700; color: var(--text-primary); }
.chat-msg-body :deep(em) { font-style: italic; color: var(--text-secondary); }

/* 标题 */
.chat-msg-body :deep(h1),
.chat-msg-body :deep(h2),
.chat-msg-body :deep(h3) {
  font-family: var(--font-heading);
  font-weight: 700;
  margin: 12px 0 6px;
  line-height: 1.3;
  color: var(--text-primary);
}
.chat-msg-body :deep(h1) { font-size: 15px; }
.chat-msg-body :deep(h2) { font-size: 14px; }
.chat-msg-body :deep(h3) { font-size: 13px; }

/* 列表 */
.chat-msg-body :deep(ul), .chat-msg-body :deep(ol) { margin: 6px 0; padding-left: 20px; }
.chat-msg-body :deep(li) { margin-bottom: 4px; }
.chat-msg-body :deep(li::marker) { color: var(--warm-terracotta); font-weight: 600; }

/* 行内代码 */
.chat-msg-body :deep(code:not(pre code)) {
  background: rgba(192,96,64,.08);
  color: #b35a3a;
  padding: 2px 7px;
  border-radius: 5px;
  font-size: 12px;
  font-family: var(--font-mono, 'JetBrains Mono', monospace);
  border: 1px solid rgba(192,96,64,.1);
}

/* 代码块 */
.chat-msg-body :deep(pre) {
  background: linear-gradient(135deg, #1a1b2e 0%, #1e1e2e 100%);
  color: #cdd6f4;
  padding: 14px 16px;
  border-radius: 10px;
  margin: 10px 0;
  overflow-x: auto;
  font-size: 12px;
  line-height: 1.6;
  border: 1px solid rgba(255,255,255,.06);
  box-shadow: inset 0 1px 3px rgba(0,0,0,.2);
}
.chat-msg-body :deep(pre code) {
  background: none;
  color: inherit;
  padding: 0;
  border: none;
  font-family: var(--font-mono, 'JetBrains Mono', monospace);
}

/* 引用块 */
.chat-msg-body :deep(blockquote) {
  border-left: 3px solid var(--warm-terracotta);
  margin: 10px 0;
  padding: 8px 14px;
  background: linear-gradient(90deg, rgba(192,96,64,.06) 0%, rgba(192,96,64,.02) 100%);
  border-radius: 0 8px 8px 0;
  color: var(--text-secondary);
  font-size: 12.5px;
}

/* 表格 */
.chat-msg-body :deep(table) {
  border-collapse: separate;
  border-spacing: 0;
  margin: 10px 0;
  font-size: 12px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--glass-border);
}
.chat-msg-body :deep(th), .chat-msg-body :deep(td) {
  padding: 8px 12px;
  text-align: left;
  border-bottom: 1px solid var(--glass-border);
}
.chat-msg-body :deep(td) {
  border-right: 1px solid var(--glass-border);
}
.chat-msg-body :deep(td:last-child) { border-right: none; }
.chat-msg-body :deep(th) {
  background: linear-gradient(135deg, rgba(192,96,64,.08) 0%, rgba(192,96,64,.04) 100%);
  font-weight: 600;
  font-size: 11.5px;
  text-transform: uppercase;
  letter-spacing: .3px;
  color: var(--text-secondary);
}
.chat-msg-body :deep(tr:last-child td) { border-bottom: none; }

/* 链接 */
.chat-msg-body :deep(a) {
  color: var(--warm-terracotta);
  text-decoration: none;
  border-bottom: 1px dashed rgba(192,96,64,.4);
  transition: all .15s;
}
.chat-msg-body :deep(a:hover) {
  border-bottom-style: solid;
  color: #a85030;
}

/* 分割线 */
.chat-msg-body :deep(hr) {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
  margin: 12px 0;
}

.chat-input-area {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  padding: 12px 14px;
  border-top: 1px solid rgba(0,0,0,.06);
  background: linear-gradient(180deg, rgba(250,248,245,.95) 0%, rgba(255,255,255,.95) 100%);
}
.chat-input {
  flex: 1;
  border: 1.5px solid var(--glass-border);
  border-radius: var(--radius-md);
  padding: 8px 12px;
  font-size: 13px;
  font-family: inherit;
  resize: none;
  outline: none;
  background: white;
  max-height: 60px;
  line-height: 1.4;
}
.chat-input:focus { border-color: var(--warm-terracotta); }
.chat-input:disabled { opacity: .5; }
.chat-send {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, var(--warm-terracotta) 0%, #d4725a 100%);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all .2s;
  box-shadow: 0 2px 8px rgba(192,96,64,.25);
}
.chat-send:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(192,96,64,.35);
}
.chat-send:disabled { opacity: .4; cursor: not-allowed; box-shadow: none; }

/* ─── 资源卡片 ─── */
.chat-resources {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.chat-res-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: white;
  border: 1px solid rgba(0,0,0,.05);
  border-radius: 12px;
  cursor: pointer;
  transition: all .2s;
}
.chat-res-card:hover {
  border-color: rgba(192,96,64,.25);
  background: rgba(192,96,64,.02);
}
.chat-res-icon { font-size: 22px; flex-shrink: 0; }
.chat-res-info { flex: 1; min-width: 0; }
.chat-res-name {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.chat-res-meta {
  display: flex;
  gap: 8px;
  font-size: 10.5px;
  color: var(--text-muted);
  margin-top: 3px;
}
.chat-res-folder { color: var(--warm-terracotta); }
.chat-res-locate {
  font-size: 10px;
  color: var(--warm-terracotta);
  opacity: 0;
  transition: opacity .2s;
}
.chat-res-card:hover .chat-res-locate { opacity: 1; }
.chat-res-tags { display: flex; gap: 3px; margin-top: 3px; flex-wrap: wrap; }
.chat-res-tag {
  font-size: 9.5px;
  padding: 1px 6px;
  background: rgba(192,96,64,.06);
  color: var(--warm-terracotta);
  border-radius: 999px;
}
.chat-res-actions { display: flex; gap: 4px; flex-shrink: 0; }
.chat-res-btn {
  width: 30px; height: 30px;
  border-radius: 8px;
  border: 1px solid rgba(0,0,0,.06);
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  transition: all .15s;
}
.chat-res-btn:hover {
  color: var(--warm-terracotta);
  border-color: var(--warm-terracotta);
  background: rgba(192,96,64,.04);
}

/* ─── 统计卡片 ─── */
.chat-stats { display: flex; gap: 10px; margin-bottom: 12px; }
.chat-stat-item {
  flex: 1; text-align: center; padding: 12px 8px;
  background: linear-gradient(135deg, rgba(192,96,64,.06) 0%, rgba(192,96,64,.02) 100%);
  border-radius: 12px; border: 1px solid rgba(192,96,64,.08);
}
.chat-stat-val { font-size: 20px; font-weight: 700; color: var(--warm-terracotta); font-family: var(--font-heading); }
.chat-stat-label { font-size: 10px; color: var(--text-muted); margin-top: 2px; }
.chat-popular { margin-top: 4px; }
.chat-popular-title { font-size: 11px; font-weight: 600; color: var(--text-muted); margin-bottom: 8px; }
.chat-popular-item { display: flex; align-items: center; gap: 8px; padding: 6px 0; font-size: 12px; }
.chat-popular-rank {
  width: 20px; height: 20px; border-radius: 50%;
  background: rgba(192,96,64,.1); color: var(--warm-terracotta);
  font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.chat-popular-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.chat-popular-dl { font-size: 10px; color: var(--text-muted); flex-shrink: 0; }

/* ─── 文件夹列表 ─── */
.chat-folders { display: flex; flex-direction: column; gap: 4px; }
.chat-folder-btn {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; border: 1px solid rgba(0,0,0,.05);
  background: white; border-radius: 12px;
  cursor: pointer; font-size: 12px; color: var(--text-primary);
  transition: all .2s; text-align: left;
}
.chat-folder-btn:hover { border-color: rgba(192,96,64,.3); background: rgba(192,96,64,.02); transform: translateX(4px); }
.chat-folder-icon { font-size: 16px; flex-shrink: 0; }
.chat-folder-path { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.chat-folders-more { font-size: 11px; color: var(--text-muted); text-align: center; padding: 6px 0; }

/* ─── 输入区 ─── */
.chat-input-area {
  display: flex; align-items: flex-end; gap: 10px;
  padding: 12px 16px;
  border-top: 1px solid rgba(0,0,0,.06);
  background: linear-gradient(180deg, rgba(250,248,245,.95) 0%, rgba(255,255,255,.95) 100%);
}
.chat-input {
  flex: 1; border: 1.5px solid rgba(0,0,0,.08);
  border-radius: 12px; padding: 10px 14px;
  font-size: 13px; font-family: inherit; resize: none;
  outline: none; background: white; max-height: 80px; line-height: 1.4;
  transition: border-color .2s;
}
.chat-input:focus { border-color: var(--warm-terracotta); }
.chat-input:disabled { opacity: .5; }
.chat-input::placeholder { color: var(--text-muted); }
.chat-send {
  width: 38px; height: 38px; border-radius: 50%; border: none;
  background: linear-gradient(135deg, var(--warm-terracotta) 0%, #d4725a 100%);
  color: white; cursor: pointer; display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; transition: all .2s; box-shadow: 0 2px 8px rgba(192,96,64,.25);
}
.chat-send:hover:not(:disabled) { transform: scale(1.05); box-shadow: 0 4px 12px rgba(192,96,64,.35); }
.chat-send:disabled { opacity: .4; cursor: not-allowed; box-shadow: none; }

@media (max-width: 480px) {
  .dog-chat-panel { width: calc(100vw - 24px); right: 12px; left: 12px !important; height: 70vh; bottom: 80px; }
}
</style>
