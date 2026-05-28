<template>
  <Teleport to="body">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-card">
        <button class="modal-close" @click="$emit('close')">&times;</button>
        <h2>注册</h2>
        <form @submit.prevent="handleRegister">
          <label><span>用户名 <em>*</em></span><input v-model="form.username" type="text" placeholder="用户名" /></label>
          <label><span>密码 <em>*</em></span><input v-model="form.password" type="password" placeholder="至少6位" /></label>
          <label><span>姓名 <em>*</em></span><input v-model="form.name" type="text" placeholder="真实姓名" /></label>
          <label><span>邮箱 <em>*</em></span><input v-model="form.email" type="email" placeholder="邮箱地址" /></label>
          <label><span>学号</span><input v-model="form.student_id" type="text" placeholder="选填" /></label>
          <label><span>手机号</span><input v-model="form.phone" type="tel" placeholder="选填" /></label>
          <p v-if="success" class="modal-success">{{ success }}</p>
          <p v-if="error" class="modal-error">{{ error }}</p>
          <button v-if="!success" type="submit" class="btn btn-primary modal-btn" :disabled="loading">{{ loading ? '注册中...' : '注册' }}</button>
        </form>
        <p class="modal-switch">已有账号？<button class="link-btn" @click="$emit('switch')">立即登录</button></p>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { userRegister } from '@/services/api'

defineProps({ show: Boolean })
const emit = defineEmits(['close', 'switch'])

const form = reactive({ username: '', password: '', name: '', email: '', student_id: '', phone: '' })
const error = ref('')
const success = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  success.value = ''
  loading.value = true
  try {
    await userRegister({ ...form })
    success.value = '注册成功！请等待管理员审核通过后登录。'
    Object.assign(form, { username: '', password: '', name: '', email: '', student_id: '', phone: '' })
  } catch (e) {
    error.value = e.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-card { background: white; border-radius: var(--radius-lg); padding: 32px; width: 100%; max-width: 400px; position: relative; box-shadow: var(--shadow-xl); max-height: 90vh; overflow-y: auto; }
.modal-close { position: absolute; top: 12px; right: 16px; background: none; border: none; font-size: 24px; color: var(--text-muted); cursor: pointer; }
.modal-card h2 { font-family: var(--font-heading); font-size: 18px; margin: 0 0 20px; }
.modal-card label { display: block; margin-bottom: 12px; }
.modal-card label span { display: block; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 4px; }
.modal-card label span em { color: var(--warm-terracotta); font-style: normal; }
.modal-card input { width: 100%; padding: 9px 12px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 14px; background: white; color: var(--text-primary); }
.modal-card input:focus { outline: none; border-color: var(--warm-terracotta); }
.modal-error { color: #e05050; font-size: 13px; margin: 0 0 8px; }
.modal-success { color: #2e7d32; font-size: 13px; margin: 0 0 8px; background: rgba(46,125,50,0.08); padding: 8px 12px; border-radius: 6px; }
.modal-btn { width: 100%; margin-top: 4px; }
.modal-switch { text-align: center; font-size: 13px; color: var(--text-muted); margin: 16px 0 0; }
.link-btn { background: none; border: none; color: var(--warm-terracotta); cursor: pointer; font-size: 13px; font-weight: 500; padding: 0; }
.link-btn:hover { text-decoration: underline; }
</style>
