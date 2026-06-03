<template>
  <div class="rc-wrapper" v-if="isLoggedIn">
    <!-- 浮动按钮 -->
    <button class="rc-fab" @click="toggleOpen" :class="{ open: isOpen }" title="AI 资源助手">
      <img v-if="!isOpen" :src="logoImg" alt="AI" class="rc-fab-logo" />
      <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>
    </button>

    <!-- 聊天面板 -->
    <Transition name="rc-panel">
      <div v-if="isOpen" class="rc-panel">
        <!-- 标题栏 -->
        <div class="rc-header">
          <div class="rc-header-left">
            <img :src="logoImg" alt="AI" class="rc-header-logo" />
            <span class="rc-header-title">资源助手</span>
            <span v-if="streaming" class="rc-header-status">思考中...</span>
          </div>
          <button class="rc-header-btn" @click="clearChat" title="清空对话">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></svg>
          </button>
        </div>

        <!-- 消息列表 -->
        <div class="rc-messages" ref="messagesRef">
          <!-- 欢迎消息 -->
          <div v-if="messages.length === 0" class="rc-welcome">
            <div class="rc-welcome-icon"><img :src="logoImg" alt="AI" class="rc-welcome-logo" /></div>
            <div class="rc-welcome-text">你好！我是资源助手，可以帮你查找资料、查看统计、推荐资源。</div>
            <div class="rc-quick-questions">
              <button v-for="q in quickQuestions" :key="q" class="rc-quick-btn" @click="sendQuick(q)">{{ q }}</button>
            </div>
          </div>

          <!-- 消息列表 -->
          <div v-for="(msg, i) in messages" :key="i" class="rc-msg" :class="'rc-msg-' + msg.role">
            <div class="rc-msg-avatar" v-if="msg.role === 'assistant'"><img :src="logoImg" alt="AI" class="rc-avatar-img" /></div>
            <div class="rc-msg-body">
              <!-- 文本消息 -->
              <div v-if="msg.type === 'text'" class="rc-msg-text" v-html="renderMarkdown(msg.content)"></div>

              <!-- 资源卡片列表 -->
              <div v-if="msg.type === 'resources'" class="rc-resources">
                <div class="rc-msg-text" v-if="msg.intro" v-html="renderMarkdown(msg.intro)"></div>
                <div v-for="r in msg.items" :key="r.id" class="rc-resource-card">
                  <div class="rc-res-icon">📄</div>
                  <div class="rc-res-info">
                    <div class="rc-res-name">{{ r.name }}</div>
                    <div class="rc-res-meta">
                      <span v-if="r.size">{{ r.size }}</span>
                      <span v-if="r.uploader">{{ r.uploader }}</span>
                      <span v-if="r.folder" class="rc-res-folder">📁 {{ r.folder }}</span>
                    </div>
                    <div v-if="r.tags && r.tags.length" class="rc-res-tags">
                      <span v-for="t in r.tags" :key="t" class="rc-res-tag">{{ t }}</span>
                    </div>
                  </div>
                  <button class="rc-res-dl" @click="downloadRes(r.id)" title="下载">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
                  </button>
                </div>
              </div>

              <!-- 工具调用状态 -->
              <div v-if="msg.type === 'tool'" class="rc-tool-status">
                <span class="rc-tool-spinner"></span>
                <span>{{ msg.content }}</span>
              </div>

              <!-- 加载动画 -->
              <div v-if="msg.type === 'loading'" class="rc-loading">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区 -->
        <div class="rc-input-area">
          <textarea
            v-model="inputText"
            @keydown="handleKeydown"
            placeholder="输入消息... (Enter 发送)"
            class="rc-input"
            rows="1"
            ref="inputRef"
            :disabled="streaming"
          ></textarea>
          <button class="rc-send-btn" @click="sendMessage" :disabled="!inputText.trim() || streaming">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m22 2-7 20-4-9-9-4z"/><path d="m22 2-11 11"/></svg>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, nextTick, watch, onMounted } from 'vue'
import { marked } from 'marked'
import { isUserLoggedIn, getUserToken } from '@/services/api'

const logoImg = 'https://shetuanweb.oss-cn-wulanchabu.aliyuncs.com/images/5ab0547bffef4a0986baac8e245c4401.png'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const isLoggedIn = ref(isUserLoggedIn())
const isOpen = ref(false)
const inputText = ref('')
const messages = ref([])
const streaming = ref(false)
const messagesRef = ref(null)
const inputRef = ref(null)

const quickQuestions = [
  '最近上传了哪些资料？',
  '帮我找找 Python 相关的资源',
  '资源中心有多少文件？',
]

// 检查登录状态
onMounted(() => {
  isLoggedIn.value = isUserLoggedIn()
  // 监听 storage 变化
  window.addEventListener('storage', () => {
    isLoggedIn.value = isUserLoggedIn()
  })
})

function toggleOpen() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    nextTick(() => inputRef.value?.focus())
  }
}

function clearChat() {
  messages.value = []
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

function sendQuick(question) {
  inputText.value = question
  sendMessage()
}

function renderMarkdown(text) {
  if (!text) return ''
  try {
    return marked(text, { breaks: true })
  } catch {
    return text
  }
}

function parseResourceResponse(text) {
  // 尝试从 AI 回复中解析资源列表
  // AI 通常会返回编号列表，我们提取关键信息
  const resourcePattern = /\d+\.\s*[📄📁📝]\s*\*\*(.+?)\*\*/g
  const matches = [...text.matchAll(resourcePattern)]
  if (matches.length > 0) {
    return matches.map(m => ({ name: m[1], id: null }))
  }
  return null
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || streaming.value) return

  inputText.value = ''
  streaming.value = true

  // 添加用户消息
  messages.value.push({ role: 'user', type: 'text', content: text })

  // 添加 AI 加载状态
  const loadingIdx = messages.value.length
  messages.value.push({ role: 'assistant', type: 'loading', content: '' })
  scrollToBottom()

  // 构建历史
  const history = messages.value
    .filter(m => m.type === 'text' && (m.role === 'user' || m.role === 'assistant'))
    .slice(0, -1) // 排除 loading
    .map(m => ({ role: m.role, content: m.content }))

  try {
    const token = getUserToken()
    const res = await fetch(`${API_BASE}/resources/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ message: text, history }),
    })

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}))
      throw new Error(errData.message || '请求失败')
    }

    // 替换 loading 为流式文本
    messages.value[loadingIdx] = { role: 'assistant', type: 'text', content: '' }
    let fullContent = ''
    let toolStatuses = []

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
          const eventType = line.slice(7).trim()
          continue
        }
        if (line.startsWith('data: ')) {
          const dataStr = line.slice(6)
          try {
            const data = JSON.parse(dataStr)

            // 处理不同事件类型
            if (data.content !== undefined) {
              // 文本内容
              fullContent += data.content
              messages.value[loadingIdx] = { role: 'assistant', type: 'text', content: fullContent }
              scrollToBottom()
            } else if (data.name && data.status) {
              // 工具调用状态
              const statusText = data.status === 'calling' ? `正在查询: ${data.name}...` : `✓ ${data.name}`
              // 在消息末尾显示工具状态
              const existingTool = toolStatuses.find(t => t.name === data.name)
              if (existingTool) {
                existingTool.status = data.status
              } else {
                toolStatuses.push({ name: data.name, status: data.status })
              }
            } else if (data.message && data.message.includes('未配置')) {
              fullContent = '⚠️ AI 未配置，请在管理端 → 系统设置中填写 AI API Key。'
              messages.value[loadingIdx] = { role: 'assistant', type: 'text', content: fullContent }
            }
          } catch {
            // 忽略解析错误
          }
        }
      }
    }

    // 流结束后，检查是否包含资源信息
    if (fullContent) {
      // 检查是否有下载链接信息
      const dlPattern = /\/api\/resources\/(\d+)\/download/g
      const dlMatches = [...fullContent.matchAll(dlPattern)]
      if (dlMatches.length > 0) {
        // 提取资源 ID 供下载按钮使用
        // 保持文本显示，下载链接嵌入在文本中
      }
    }

  } catch (err) {
    messages.value[loadingIdx] = {
      role: 'assistant',
      type: 'text',
      content: `❌ ${err.message || '请求失败，请稍后重试'}`,
    }
  } finally {
    streaming.value = false
    scrollToBottom()
  }
}

async function downloadRes(id) {
  if (!id) return
  try {
    const token = getUserToken()
    const res = await fetch(`${API_BASE}/resources/${id}/download`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
    if (!res.ok) throw new Error('下载失败')
    const data = await res.json()
    if (data.url) {
      window.open(data.url, '_blank')
    }
  } catch (err) {
    alert(err.message || '下载失败')
  }
}
</script>

<style scoped>
/* ===== 浮动按钮 ===== */
.rc-wrapper{position:fixed;bottom:24px;right:24px;z-index:150}
.rc-fab{width:52px;height:52px;border-radius:50%;border:none;background:transparent;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .25s;overflow:hidden;padding:0}
.rc-fab:hover{transform:scale(1.1)}
.rc-fab.open{background:rgba(0,0,0,.05);border-radius:14px}
.rc-fab-logo{width:52px;height:52px;object-fit:contain;border-radius:50%}

/* ===== 面板过渡 ===== */
.rc-panel-enter-active{animation:rc-slide-up .25s ease}
.rc-panel-leave-active{animation:rc-slide-up .2s ease reverse}
@keyframes rc-slide-up{from{opacity:0;transform:translateY(16px) scale(.96)}to{opacity:1;transform:translateY(0) scale(1)}}

/* ===== 聊天面板 ===== */
.rc-panel{position:absolute;bottom:68px;right:0;width:400px;height:560px;background:rgba(255,255,255,.97);backdrop-filter:blur(20px);border:1px solid var(--glass-border,rgba(0,0,0,.08));border-radius:var(--radius-xl,20px);box-shadow:var(--shadow-xl,0 20px 60px rgba(0,0,0,.15));display:flex;flex-direction:column;overflow:hidden}

/* ===== 标题栏 ===== */
.rc-header{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid var(--glass-border,rgba(0,0,0,.06));background:rgba(255,255,255,.8)}
.rc-header-left{display:flex;align-items:center;gap:8px}
.rc-header-logo{width:22px;height:22px;object-fit:contain;border-radius:4px}
.rc-header-title{font-size:14px;font-weight:600;color:var(--text-primary,#333)}
.rc-header-status{font-size:11px;color:var(--text-muted,#999);animation:rc-pulse 1.5s infinite}
@keyframes rc-pulse{0%,100%{opacity:1}50%{opacity:.4}}
.rc-header-btn{border:none;background:none;cursor:pointer;color:var(--text-muted,#999);padding:4px;border-radius:6px;display:flex;align-items:center}
.rc-header-btn:hover{background:var(--bg-soft,#f5f5f5);color:var(--text-primary,#333)}

/* ===== 消息列表 ===== */
.rc-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
.rc-messages::-webkit-scrollbar{width:4px}
.rc-messages::-webkit-scrollbar-thumb{background:rgba(0,0,0,.1);border-radius:4px}

/* ===== 欢迎页 ===== */
.rc-welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;text-align:center;gap:12px;padding:20px 0}
.rc-welcome-icon{font-size:40px}
.rc-welcome-logo{width:48px;height:48px;object-fit:contain;border-radius:10px}
.rc-welcome-text{font-size:13px;color:var(--text-secondary,#666);line-height:1.6}
.rc-quick-questions{display:flex;flex-direction:column;gap:6px;width:100%;margin-top:8px}
.rc-quick-btn{border:1px solid var(--glass-border,rgba(0,0,0,.1));background:white;border-radius:var(--radius-md,12px);padding:8px 14px;font-size:12px;color:var(--text-primary,#333);cursor:pointer;text-align:left;transition:all .15s}
.rc-quick-btn:hover{border-color:var(--warm-terracotta,#c06040);color:var(--warm-terracotta,#c06040);background:rgba(192,96,64,.04)}

/* ===== 消息气泡 ===== */
.rc-msg{display:flex;gap:8px;max-width:95%}
.rc-msg-user{align-self:flex-end;flex-direction:row-reverse}
.rc-msg-assistant{align-self:flex-start}
.rc-msg-avatar{width:28px;height:28px;border-radius:50%;background:var(--bg-soft,#f5f5f5);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;overflow:hidden}
.rc-avatar-img{width:20px;height:20px;object-fit:contain}
.rc-msg-body{min-width:0}
.rc-msg-text{font-size:13px;line-height:1.65;color:var(--text-primary,#333);padding:10px 14px;border-radius:var(--radius-md,12px);word-break:break-word}
.rc-msg-user .rc-msg-text{background:var(--warm-terracotta,#c06040);color:white;border-bottom-right-radius:4px}
.rc-msg-assistant .rc-msg-text{background:var(--bg-soft,#f5f5f5);border-bottom-left-radius:4px}

/* markdown 内容样式 */
.rc-msg-text :deep(p){margin:0 0 6px}
.rc-msg-text :deep(p:last-child){margin-bottom:0}
.rc-msg-text :deep(ul),.rc-msg-text :deep(ol){margin:4px 0;padding-left:18px}
.rc-msg-text :deep(code){background:rgba(0,0,0,.06);padding:1px 5px;border-radius:4px;font-size:12px}
.rc-msg-text :deep(pre){background:rgba(0,0,0,.04);padding:8px;border-radius:6px;overflow-x:auto;margin:6px 0}
.rc-msg-text :deep(strong){font-weight:600}

/* ===== 资源卡片 ===== */
.rc-resources{display:flex;flex-direction:column;gap:6px}
.rc-resource-card{display:flex;align-items:center;gap:10px;padding:10px 12px;background:white;border:1px solid var(--glass-border,rgba(0,0,0,.08));border-radius:var(--radius-md,10px);transition:all .15s}
.rc-resource-card:hover{border-color:var(--warm-terracotta,#c06040);box-shadow:0 2px 12px rgba(192,96,64,.1)}
.rc-res-icon{font-size:20px;flex-shrink:0}
.rc-res-info{flex:1;min-width:0}
.rc-res-name{font-size:12px;font-weight:600;color:var(--text-primary,#333);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rc-res-meta{display:flex;gap:8px;font-size:10px;color:var(--text-muted,#999);margin-top:2px;flex-wrap:wrap}
.rc-res-folder{color:var(--warm-terracotta,#c06040)}
.rc-res-tags{display:flex;gap:3px;margin-top:3px;flex-wrap:wrap}
.rc-res-tag{font-size:9px;padding:1px 6px;background:rgba(192,96,64,.08);color:var(--warm-terracotta,#c06040);border-radius:999px}
.rc-res-dl{border:none;background:none;cursor:pointer;color:var(--text-muted,#999);padding:4px;border-radius:6px;display:flex;align-items:center;flex-shrink:0}
.rc-res-dl:hover{color:var(--warm-terracotta,#c06040);background:rgba(192,96,64,.08)}

/* ===== 工具调用状态 ===== */
.rc-tool-status{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text-muted,#999);padding:4px 0}
.rc-tool-spinner{width:12px;height:12px;border:2px solid rgba(192,96,64,.2);border-top-color:var(--warm-terracotta,#c06040);border-radius:50%;animation:rc-spin .6s linear infinite}
@keyframes rc-spin{to{transform:rotate(360deg)}}

/* ===== 加载动画 ===== */
.rc-loading{display:flex;gap:4px;padding:10px 14px}
.rc-loading span{width:6px;height:6px;background:var(--warm-terracotta,#c06040);border-radius:50%;animation:rc-bounce 1.2s infinite}
.rc-loading span:nth-child(2){animation-delay:.2s}
.rc-loading span:nth-child(3){animation-delay:.4s}
@keyframes rc-bounce{0%,80%,100%{transform:scale(0);opacity:.4}40%{transform:scale(1);opacity:1}}

/* ===== 输入区 ===== */
.rc-input-area{display:flex;align-items:flex-end;gap:8px;padding:12px 16px;border-top:1px solid var(--glass-border,rgba(0,0,0,.06));background:rgba(255,255,255,.8)}
.rc-input{flex:1;border:1.5px solid var(--glass-border,rgba(0,0,0,.1));border-radius:var(--radius-md,10px);padding:8px 12px;font-size:13px;font-family:inherit;resize:none;outline:none;background:white;transition:border-color .2s;max-height:80px;line-height:1.4}
.rc-input:focus{border-color:var(--warm-terracotta,#c06040)}
.rc-input:disabled{opacity:.5}
.rc-send-btn{width:36px;height:36px;border-radius:50%;border:none;background:var(--warm-terracotta,#c06040);color:white;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .2s}
.rc-send-btn:hover:not(:disabled){transform:scale(1.05);box-shadow:0 4px 12px rgba(192,96,64,.3)}
.rc-send-btn:disabled{opacity:.4;cursor:not-allowed}

/* ===== 响应式 ===== */
@media(max-width:480px){
  .rc-panel{width:calc(100vw - 32px);right:-8px;height:480px}
}
</style>
