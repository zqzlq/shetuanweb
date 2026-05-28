<template>
  <div class="page-view">
    <div class="container">
      <div class="page-hero">
        <h1>{{ page.content.hero.title }}</h1>
        <p class="page-subtitle">{{ page.content.hero.subtitle }}</p>
      </div>

      <div class="steps-bar reveal">
        <div v-for="(s, i) in page.content.form.steps" :key="s" class="step" :class="{ active: step === i, done: step > i }">
          <span class="step-num">{{ i + 1 }}</span>
          <span class="step-label">{{ s }}</span>
        </div>
      </div>

      <!-- 第一步：基本信息 -->
      <div v-if="step === 0" class="form-step reveal">
        <PaperCard>
          <div class="form-grid">
            <label :class="{ error: errors.name }">
              <span>姓名 <em>*</em></span>
              <input v-model="form.name" type="text" placeholder="你的姓名" @blur="validateField('name')" />
              <small v-if="errors.name" class="error-msg">{{ errors.name }}</small>
            </label>
            <label :class="{ error: errors.student_id }">
              <span>学号 <em>*</em></span>
              <input v-model="form.student_id" type="text" placeholder="学号" @blur="validateField('student_id')" />
              <small v-if="errors.student_id" class="error-msg">{{ errors.student_id }}</small>
            </label>
            <label :class="{ error: errors.grade_major }">
              <span>年级专业 <em>*</em></span>
              <input v-model="form.grade_major" type="text" placeholder="如：2024级计算机科学" @blur="validateField('grade_major')" />
              <small v-if="errors.grade_major" class="error-msg">{{ errors.grade_major }}</small>
            </label>
            <label :class="{ error: errors.phone }">
              <span>手机 <em>*</em></span>
              <input v-model="form.phone" type="tel" placeholder="手机号" @blur="validateField('phone')" />
              <small v-if="errors.phone" class="error-msg">{{ errors.phone }}</small>
            </label>
            <label class="full" :class="{ error: errors.email }">
              <span>邮箱 <em>*</em></span>
              <input v-model="form.email" type="email" placeholder="邮箱地址" @blur="validateField('email')" />
              <small v-if="errors.email" class="error-msg">{{ errors.email }}</small>
            </label>
          </div>
          <div class="form-actions">
            <button class="btn btn-primary" @click="nextStep0">下一步</button>
          </div>
        </PaperCard>
      </div>

      <!-- 第二步：选择方向 -->
      <div v-if="step === 1" class="form-step reveal">
        <h2 class="form-section-title">{{ page.content.sections.groupsTitle }}</h2>
        <div class="group-selector">
          <div v-for="g in page.content.form.groups" :key="g.id" class="group-option" :class="{ selected: form.group_id === g.id, error: errors.group_id }" @click="selectGroup(g)">
            <span class="tag tag-accent">{{ g.tag }}</span>
            <strong>{{ g.name }}</strong>
          </div>
        </div>
        <small v-if="errors.group_id" class="error-msg error-msg-block">{{ errors.group_id }}</small>

        <PaperCard>
          <div class="form-grid">
            <label><span>GitHub（选填）</span><input v-model="form.github_url" type="url" placeholder="https://github.com/..." /></label>
            <label><span>作品集（选填）</span><input v-model="form.portfolio_url" type="url" placeholder="链接" /></label>
            <label class="full"><span>相关经验（选填）</span><textarea v-model="form.experience" placeholder="简要描述你的相关经验"></textarea></label>
            <label class="full" :class="{ error: errors.motivation }">
              <span>申请动机 <em>*</em></span>
              <textarea v-model="form.motivation" placeholder="为什么想加入星雨作坊？" @blur="validateField('motivation')"></textarea>
              <small v-if="errors.motivation" class="error-msg">{{ errors.motivation }}</small>
            </label>
          </div>
          <div class="form-actions">
            <button class="btn btn-outline" @click="step = 0">上一步</button>
            <button class="btn btn-primary" @click="nextStep1">下一步</button>
          </div>
        </PaperCard>
      </div>

      <!-- 第三步：确认提交 -->
      <div v-if="step === 2" class="form-step reveal">
        <PaperCard>
          <div v-if="submitResult && submitResult.success" class="submit-success">
            <h2>申请已提交</h2>
            <p>{{ submitResult.message }}</p>
          </div>
          <div v-else>
            <h2>确认提交</h2>
            <p>请确认你的信息无误后提交申请。</p>
            <div class="confirm-grid">
              <div class="confirm-item"><span>姓名</span><strong>{{ form.name }}</strong></div>
              <div class="confirm-item"><span>学号</span><strong>{{ form.student_id }}</strong></div>
              <div class="confirm-item"><span>年级专业</span><strong>{{ form.grade_major }}</strong></div>
              <div class="confirm-item"><span>手机</span><strong>{{ form.phone }}</strong></div>
              <div class="confirm-item"><span>邮箱</span><strong>{{ form.email }}</strong></div>
              <div class="confirm-item"><span>意向组别</span><strong>{{ form.group_name }}</strong></div>
              <div class="confirm-item" v-if="form.motivation"><span>申请动机</span><strong>{{ form.motivation }}</strong></div>
            </div>
            <p v-if="submitResult && !submitResult.success" class="submit-error">{{ submitResult.message }}</p>
            <div class="form-actions">
              <button class="btn btn-outline" @click="step = 1">上一步</button>
              <button class="btn btn-primary" :disabled="submitting" @click="submitForm">{{ submitting ? '提交中...' : page.content.applyCta.buttonText }}</button>
            </div>
          </div>
        </PaperCard>
      </div>

      <section class="benefits-section reveal">
        <div class="cards-grid">
          <PaperCard v-for="b in page.content.benefits" :key="b.title" glow="var(--warm-sage)">
            <h3>{{ b.title }}</h3>
            <p>{{ b.description }}</p>
          </PaperCard>
        </div>
      </section>

      <section class="faq-section reveal">
        <h2 class="form-section-title">{{ page.content.sections.faqTitle }}</h2>
        <div v-for="f in page.content.faq" :key="f.question" class="faq-item">
          <button class="faq-q" @click="f.open = !f.open"><span>{{ f.question }}</span><span>{{ f.open ? '−' : '+' }}</span></button>
          <div v-if="f.open" class="faq-a">{{ f.answer }}</div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useSiteConfigStore } from '@/stores/siteConfig'
import { useScrollReveal } from '@/composables/useScrollReveal'
import { submitApplication } from '@/services/api'
import PaperCard from '@/components/ui/PaperCard.vue'

const store = useSiteConfigStore()
const page = store.getPage('join')
useScrollReveal()

const step = ref(0)
const submitting = ref(false)
const submitResult = ref(null)
const form = reactive({
  name: '', student_id: '', grade_major: '', phone: '', email: '',
  group_id: '', group_name: '', github_url: '', portfolio_url: '',
  experience: '', motivation: '',
})

const errors = reactive({
  name: '', student_id: '', grade_major: '', phone: '', email: '',
  group_id: '', motivation: '',
})

const rules = {
  name: [
    { test: (v) => v.trim(), msg: '请填写姓名' },
    { test: (v) => v.trim().length >= 2, msg: '姓名至少 2 个字符' },
  ],
  student_id: [
    { test: (v) => v.trim(), msg: '请填写学号' },
    { test: (v) => /^\d{6,12}$/.test(v.trim()), msg: '学号应为 6-12 位数字' },
  ],
  grade_major: [
    { test: (v) => v.trim(), msg: '请填写年级专业' },
  ],
  phone: [
    { test: (v) => v.trim(), msg: '请填写手机号' },
    { test: (v) => /^1\d{10}$/.test(v.trim()), msg: '请输入 11 位手机号' },
  ],
  email: [
    { test: (v) => v.trim(), msg: '请填写邮箱' },
    { test: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()), msg: '请输入正确的邮箱格式' },
  ],
  group_id: [
    { test: (v) => v, msg: '请选择一个组别' },
  ],
  motivation: [
    { test: (v) => v.trim(), msg: '请填写申请动机' },
    { test: (v) => v.trim().length >= 10, msg: '申请动机至少 10 个字' },
  ],
}

function validateField(field) {
  const fieldRules = rules[field]
  if (!fieldRules) return true
  const value = field === 'group_id' ? form.group_id : form[field]
  for (const rule of fieldRules) {
    if (!rule.test(value)) {
      errors[field] = rule.msg
      return false
    }
  }
  errors[field] = ''
  return true
}

function validateStep0() {
  const fields = ['name', 'student_id', 'grade_major', 'phone', 'email']
  let ok = true
  for (const f of fields) {
    if (!validateField(f)) ok = false
  }
  return ok
}

function validateStep1() {
  const fields = ['group_id', 'motivation']
  let ok = true
  for (const f of fields) {
    if (!validateField(f)) ok = false
  }
  return ok
}

function nextStep0() {
  if (validateStep0()) step.value = 1
}

function nextStep1() {
  if (validateStep1()) step.value = 2
}

function selectGroup(g) {
  form.group_id = g.id
  form.group_name = g.name
  errors.group_id = ''
}

async function submitForm() {
  submitting.value = true
  submitResult.value = null
  try {
    const result = await submitApplication(form)
    submitResult.value = { success: true, message: result.message || '申请已提交' }
  } catch (e) {
    submitResult.value = { success: false, message: e.message || '提交失败，请稍后重试' }
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page-view { padding: 120px 0 40px; }
.page-hero { text-align: center; margin-bottom: 40px; padding: 48px 32px; background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.page-hero::after { content: ''; position: absolute; inset: 0; background-image: radial-gradient(circle at 15% 85%, rgba(192, 96, 64, 0.04) 0%, transparent 40%), radial-gradient(circle at 85% 15%, rgba(212, 146, 10, 0.04) 0%, transparent 40%); pointer-events: none; }
.page-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--grad-primary); }
.page-hero h1 { font-size: clamp(2rem, 4vw, 3rem); margin-bottom: 12px; }
.page-subtitle { font-size: 16px; color: var(--text-secondary); }

.steps-bar { display: flex; justify-content: center; gap: 32px; margin-bottom: 40px; }
.step { display: flex; align-items: center; gap: 8px; color: var(--text-muted); }
.step.active { color: var(--warm-terracotta); }
.step.done { color: var(--text-primary); }
.step-num { width: 28px; height: 28px; border-radius: 50%; border: 2px solid currentColor; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 600; }
.step.active .step-num { background: var(--warm-terracotta); color: white; border-color: var(--warm-terracotta); }
.step.done .step-num { background: var(--warm-terracotta); color: white; border-color: var(--warm-terracotta); }
.step-label { font-size: 14px; font-weight: 500; }

.form-step { margin-bottom: 32px; }
.form-section-title { font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 20px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
.form-grid .full { grid-column: 1 / -1; }
.form-grid label span { display: block; font-size: 13px; font-weight: 500; color: var(--text-secondary); margin-bottom: 6px; }
.form-grid label span em { color: var(--warm-terracotta); font-style: normal; }
.form-grid input, .form-grid textarea { width: 100%; padding: 10px 14px; border: 1px solid var(--glass-border); border-radius: var(--radius-md); font-size: 14px; font-family: var(--font-body); background: white; color: var(--text-primary); transition: border-color 0.2s, box-shadow 0.2s; }
.form-grid input:focus, .form-grid textarea:focus { outline: none; border-color: var(--warm-terracotta); box-shadow: 0 0 0 3px rgba(192, 96, 64, 0.1); }
.form-grid textarea { min-height: 80px; resize: vertical; }

/* 错误状态 */
.form-grid label.error input,
.form-grid label.error textarea {
  border-color: #e05050;
  box-shadow: 0 0 0 3px rgba(224, 80, 80, 0.08);
}

.error-msg {
  display: block;
  font-size: 12px;
  color: #e05050;
  margin-top: 4px;
}

.error-msg-block {
  display: block;
  font-size: 12px;
  color: #e05050;
  margin: -16px 0 16px;
}

.form-actions { display: flex; gap: 12px; justify-content: flex-end; }

.group-selector { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 8px; }
.group-option { border: 2px solid var(--glass-border); border-radius: var(--radius-lg); padding: 20px 16px; text-align: center; cursor: pointer; transition: all 0.2s; }
.group-option:hover { border-color: var(--glass-border-hover); background: var(--surface); }
.group-option.selected { border-color: var(--warm-terracotta); background: rgba(192, 96, 64, 0.06); }
.group-option.error { border-color: #e05050; }
.group-option strong { display: block; margin-top: 8px; font-family: var(--font-heading); }

/* 确认页 */
.confirm-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 24px 0; }
.confirm-item { padding: 12px 16px; background: var(--bg); border-radius: var(--radius-md); }
.confirm-item span { display: block; font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }
.confirm-item strong { font-size: 14px; color: var(--text-primary); word-break: break-all; }

.benefits-section { margin: 48px 0; }
.cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.cards-grid h3 { font-family: var(--font-heading); font-size: 16px; margin-bottom: 8px; }
.cards-grid p { font-size: 13px; color: var(--text-secondary); margin: 0; line-height: 1.7; }

/* 提交结果 */
.submit-success { text-align: center; padding: 32px 0; }
.submit-success h2 { font-family: var(--font-heading); color: var(--warm-sage); margin-bottom: 12px; }
.submit-success p { color: var(--text-secondary); font-size: 15px; }
.submit-error { color: #e05050; font-size: 13px; margin: 8px 0; text-align: right; }

.faq-section { margin-top: 48px; }
.faq-item { border-bottom: 1px solid var(--glass-border); }
.faq-q { width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 16px 0; background: none; border: none; font-size: 15px; font-weight: 500; color: var(--text-primary); cursor: pointer; }
.faq-a { padding: 0 0 16px; font-size: 14px; color: var(--text-secondary); line-height: 1.7; }

@media (max-width: 768px) { .form-grid { grid-template-columns: 1fr; } .group-selector { grid-template-columns: repeat(2, 1fr); } .cards-grid { grid-template-columns: 1fr; } .confirm-grid { grid-template-columns: 1fr; } }
</style>
