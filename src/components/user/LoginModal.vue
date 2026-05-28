<template>
  <Teleport to="body">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-card">
        <button class="modal-close" @click="$emit('close')">&times;</button>
        <h2>登录</h2>
        <form @submit.prevent="handleLogin">
          <label>
            <span>用户名</span>
            <input v-model="form.username" type="text" placeholder="用户名" autocomplete="username" />
          </label>
          <label>
            <span>密码</span>
            <input v-model="form.password" type="password" placeholder="密码" autocomplete="current-password" />
          </label>
          <p v-if="error" class="modal-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary modal-btn" :disabled="loading">{{ loading ? '登录中...' : '登录' }}</button>
        </form>
        <p class="modal-switch">还没有账号？<button class="link-btn" @click="$emit('switch')">立即注册</button></p>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { userLogin } from '@/services/api'

defineProps({ show: Boolean })
const emit = defineEmits(['close', 'switch', 'login'])

const form = reactive({ username: '', password: '' })
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const data = await userLogin(form.username, form.password)
    emit('login', data.user)
    emit('close')
  } catch (e) {
    error.value = e.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-card { background: white; border-radius: var(--radius-lg); padding: 32px; width: 100%; max-width: 380px; position: relative; box-shadow: var(--shadow-xl); }
.modal-close { position: absolute; top: 12px; right: 16px; background: none; border: none; font-size: 24px; color: var(--text-muted); cursor: pointer; }
.modal-card h2 { font-family: var(--font-heading); font-size: 18px; margin: 0 0 20px; }
.modal-card label { display: block; margin-bottom: 14px; }
.modal-card label span { display: block; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
.modal-card input { width: 100%; padding: 9px 12px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 14px; background: white; color: var(--text-primary); }
.modal-card input:focus { outline: none; border-color: var(--warm-terracotta); }
.modal-error { color: #e05050; font-size: 13px; margin: 0 0 8px; }
.modal-btn { width: 100%; margin-top: 4px; }
.modal-switch { text-align: center; font-size: 13px; color: var(--text-muted); margin: 16px 0 0; }
.link-btn { background: none; border: none; color: var(--warm-terracotta); cursor: pointer; font-size: 13px; font-weight: 500; padding: 0; }
.link-btn:hover { text-decoration: underline; }
</style>
