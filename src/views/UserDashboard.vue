<template>
  <div class="page-view">
    <div class="container" v-if="user">
      <h1>个人中心</h1>
      <p class="page-subtitle">管理你的个人资料、奖状和作品</p>

      <div class="dashboard-tabs">
        <button v-for="t in tabs" :key="t.key" class="filter-tab" :class="{ active: activeTab === t.key }" @click="activeTab = t.key">{{ t.label }}</button>
      </div>

      <!-- 个人资料 -->
      <div v-if="activeTab === 'profile'" class="tab-content">
        <div class="editor-card">
          <h3>基本信息</h3>
          <div class="field-grid">
            <label class="field"><span>用户名（不可修改）</span><input :value="user.username" disabled /></label>
            <label class="field"><span>姓名</span><input v-model="form.name" /></label>
            <label class="field"><span>学号</span><input v-model="form.student_id" /></label>
            <label class="field"><span>手机号</span><input v-model="form.phone" /></label>
            <label class="field"><span>组别</span><select v-model="form.group"><option value="">未选择</option><option v-for="g in groups" :key="g.id" :value="g.name">{{ g.name }}</option></select></label>
            <label class="field"><span>邮箱（不可修改）</span><input :value="user.email" disabled /></label>
            <label class="field full"><span>头像</span><ImageUploadField :modelValue="form.avatar || ''" @update:modelValue="form.avatar = $event" /></label>
            <label class="field full"><span>个人简介</span><textarea v-model="form.bio" rows="3" placeholder="介绍一下自己..."></textarea></label>
          </div>
          <button class="btn btn-primary btn-sm" @click="saveProfile" :disabled="saving">{{ saving ? '保存中...' : '保存资料' }}</button>
        </div>

        <div class="editor-card">
          <h3>修改密码</h3>
          <div class="field-grid">
            <label class="field"><span>旧密码</span><input v-model="pwForm.old" type="password" /></label>
            <label class="field"><span>新密码</span><input v-model="pwForm.newPw" type="password" placeholder="至少6位" /></label>
          </div>
          <p v-if="pwMsg" :class="pwOk ? 'modal-success' : 'modal-error'">{{ pwMsg }}</p>
          <button class="btn btn-outline btn-sm" @click="changePw" :disabled="pwSaving">{{ pwSaving ? '修改中...' : '修改密码' }}</button>
        </div>

        <div class="editor-card">
          <h3>社交链接</h3>
          <div v-for="(link, i) in form.social_links || []" :key="i" class="inline-row">
            <select v-model="link.platform" class="platform-select">
              <option value="github">GitHub</option>
              <option value="bilibili">B站</option>
              <option value="zhihu">知乎</option>
              <option value="blog">博客</option>
              <option value="douyin">抖音</option>
              <option value="weibo">微博</option>
              <option value="other">其他</option>
            </select>
            <input v-model="link.url" placeholder="链接地址" class="flex-1" />
            <button class="btn-icon" @click="removeSocialLink(i)">&times;</button>
          </div>
          <button class="btn btn-outline btn-xs" @click="addSocialLink">+ 添加链接</button>
        </div>
      </div>

      <!-- 我的奖状 -->
      <div v-if="activeTab === 'awards'" class="tab-content">
        <div class="editor-card">
          <div class="card-header"><h3>提交奖状</h3></div>
          <div class="field-grid">
            <label class="field"><span>奖项名称 <em>*</em></span><input v-model="awardForm.title" placeholder="如：程序设计大赛一等奖" /></label>
            <label class="field"><span>Slug</span><input v-model="awardForm.slug" placeholder="唯一标识" /></label>
            <label class="field"><span>级别</span><input v-model="awardForm.level" placeholder="如：省级一等奖" /></label>
            <label class="field"><span>日期</span><input v-model="awardForm.date" type="month" /></label>
            <label class="field"><span>分类</span><input v-model="awardForm.category" placeholder="如：计算机设计" /></label>
            <label class="field"><span>关联项目 Slug</span><input v-model="awardForm.projectSlug" placeholder="选填" /></label>
            <label class="field"><span>参与者（逗号分隔）</span><input :value="awardForm.participants?.join(', ')" @change="awardForm.participants = $event.target.value.split(',').map(s=>s.trim()).filter(Boolean)" /></label>
            <label class="field full"><span>简述</span><textarea v-model="awardForm.shortDesc" rows="2" placeholder="一句话描述"></textarea></label>
            <label class="field full"><span>描述</span><textarea v-model="awardForm.description" rows="3" placeholder="奖项详细描述"></textarea></label>
            <label class="field full"><span>详细介绍（Markdown）</span><textarea v-model="awardForm.longDescription" rows="5" placeholder="支持 Markdown 格式"></textarea></label>
            <label class="field full"><span>主图</span><ImageUploadField :modelValue="awardForm.image || ''" @update:modelValue="awardForm.image = $event" /></label>
            <label class="field full"><span>截图</span><MultiImageUploadField :modelValue="awardForm.screenshots || []" @update:modelValue="awardForm.screenshots = $event" /></label>
          </div>
          <button class="btn btn-primary btn-sm" @click="submitAward" :disabled="saving">{{ saving ? '提交中...' : '提交奖状' }}</button>
        </div>
        <div v-if="submissions.filter(s => s.type === 'award').length" class="submission-list">
          <h3>提交记录</h3>
          <div v-for="s in submissions.filter(s => s.type === 'award')" :key="s.id" class="submission-item">
            <strong>{{ s.title }}</strong>
            <span class="submission-right">
              <span class="submission-status" :class="'status-' + s.status">{{ statusLabel(s.status) }}</span>
              <button class="btn-icon" @click="deleteSubmission(s.id)" title="删除">&#10005;</button>
            </span>
          </div>
        </div>
      </div>

      <!-- 我的作品 -->
      <div v-if="activeTab === 'projects'" class="tab-content">
        <div class="editor-card">
          <div class="card-header"><h3>提交作品</h3></div>
          <div class="field-grid">
            <label class="field"><span>作品名称 <em>*</em></span><input v-model="projectForm.name" /></label>
            <label class="field"><span>Slug</span><input v-model="projectForm.slug" placeholder="唯一标识" /></label>
            <label class="field"><span>分类</span><select v-model="projectForm.category"><option value="" disabled>选择分类</option><option v-for="c in categories" :key="c" :value="c">{{ c }}</option></select></label>
            <label class="field"><span>封面样式</span><input v-model="projectForm.coverClass" placeholder="aurora / meteor / nebula / cosmos / pulse / horizon" /></label>
            <label class="field"><span>GitHub</span><input v-model="projectForm.githubUrl" placeholder="https://github.com/..." /></label>
            <label class="field"><span>链接</span><input v-model="projectForm.link" placeholder="项目链接" /></label>
            <label class="field"><span>技术栈（逗号分隔）</span><input :value="projectForm.techStack?.join(', ')" @change="projectForm.techStack = $event.target.value.split(',').map(s=>s.trim()).filter(Boolean)" /></label>
            <label class="field full"><span>描述</span><textarea v-model="projectForm.description" rows="2" placeholder="简要描述"></textarea></label>
            <label class="field full"><span>详细介绍（Markdown）</span><textarea v-model="projectForm.longDescription" rows="5" placeholder="支持 Markdown 格式"></textarea></label>
            <label class="field full"><span>封面图片</span><ImageUploadField :modelValue="projectForm.coverImage || ''" @update:modelValue="projectForm.coverImage = $event" /></label>
            <label class="field full"><span>截图</span><MultiImageUploadField :modelValue="projectForm.screenshots || []" @update:modelValue="projectForm.screenshots = $event" /></label>
          </div>
          <button class="btn btn-primary btn-sm" @click="submitProject" :disabled="saving">{{ saving ? '提交中...' : '提交作品' }}</button>
        </div>
        <div v-if="submissions.filter(s => s.type === 'project').length" class="submission-list">
          <h3>提交记录</h3>
          <div v-for="s in submissions.filter(s => s.type === 'project')" :key="s.id" class="submission-item">
            <strong>{{ s.title }}</strong>
            <span class="submission-right">
              <span class="submission-status" :class="'status-' + s.status">{{ statusLabel(s.status) }}</span>
              <button class="btn-icon" @click="deleteSubmission(s.id)" title="删除">&#10005;</button>
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="login-prompt">
      <p>请先登录后查看个人中心</p>
      <router-link to="/" class="btn btn-primary">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { isUserLoggedIn, getCurrentMemberUser, updateUserProfile, changePassword, submitUserSubmission, getUserSubmissions, deleteUserSubmission, userLogout } from '@/services/api'
import { useSiteConfigStore } from '@/stores/siteConfig'
import ImageUploadField from '@/components/admin/ImageUploadField.vue'
import MultiImageUploadField from '@/components/admin/MultiImageUploadField.vue'

const store = useSiteConfigStore()
const categories = computed(() => {
  const cats = store.config?.products?.categories || []
  return cats.filter(c => c && c !== '精选总览')
})
const groups = computed(() => {
  const joinPage = store.getPage('join')
  return joinPage?.content?.form?.groups || []
})

const user = ref(null)
const activeTab = ref('profile')
const saving = ref(false)
const tabs = [
  { key: 'profile', label: '个人资料' },
  { key: 'awards', label: '我的奖状' },
  { key: 'projects', label: '我的作品' },
]

const form = reactive({ name: '', student_id: '', phone: '', group: '', avatar: '', bio: '', social_links: [] })
const pwForm = reactive({ old: '', newPw: '' })
const pwSaving = ref(false)
const pwMsg = ref('')
const pwOk = ref(false)
const submissions = ref([])
const awardForm = reactive({
  title: '', slug: '', level: '', date: '', category: '',
  shortDesc: '', description: '', longDescription: '',
  participants: [], projectSlug: '', image: '', screenshots: [],
})
const projectForm = reactive({
  name: '', slug: '', category: '', coverClass: 'aurora',
  description: '', longDescription: '', coverImage: '', screenshots: [],
  githubUrl: '', link: '', techStack: [],
})

onMounted(async () => {
  if (!isUserLoggedIn()) return
  try {
    user.value = await getCurrentMemberUser()
    Object.assign(form, {
      name: user.value.name || '', student_id: user.value.student_id || '',
      phone: user.value.phone || '', group: user.value.group || '',
      avatar: user.value.avatar || '',
      bio: user.value.bio || '', social_links: user.value.social_links || [],
    })
    submissions.value = await getUserSubmissions()
  } catch { userLogout() }
})

async function changePw() {
  pwMsg.value = ''; pwSaving.value = true
  try {
    await changePassword(pwForm.old, pwForm.newPw)
    pwMsg.value = '密码修改成功'; pwOk.value = true
    pwForm.old = ''; pwForm.newPw = ''
  } catch (e) { pwMsg.value = e.message; pwOk.value = false }
  finally { pwSaving.value = false }
}

async function saveProfile() {
  saving.value = true
  try {
    const updated = await updateUserProfile({ ...form })
    user.value = updated.user
  } catch (e) { alert('保存失败: ' + e.message) }
  finally { saving.value = false }
}

function addSocialLink() {
  form.social_links = [...(form.social_links || []), { platform: 'github', url: '' }]
}
function removeSocialLink(i) {
  form.social_links = (form.social_links || []).filter((_, idx) => idx !== i)
}

async function submitAward() {
  saving.value = true
  try {
    await submitUserSubmission({
      type: 'award',
      title: awardForm.title,
      description: awardForm.shortDesc,
      image: awardForm.image,
      data: { ...awardForm },
    })
    Object.assign(awardForm, {
      title: '', slug: '', level: '', date: '', category: '',
      shortDesc: '', description: '', longDescription: '',
      participants: [], projectSlug: '', image: '', screenshots: [],
    })
    submissions.value = await getUserSubmissions()
    alert('奖状已提交，请等待管理员审核')
  } catch (e) { alert('提交失败: ' + e.message) }
  finally { saving.value = false }
}

async function submitProject() {
  saving.value = true
  try {
    await submitUserSubmission({
      type: 'project',
      title: projectForm.name,
      description: projectForm.description,
      image: projectForm.coverImage,
      data: { ...projectForm },
    })
    Object.assign(projectForm, {
      name: '', slug: '', category: '', coverClass: 'aurora',
      description: '', longDescription: '', coverImage: '', screenshots: [],
      githubUrl: '', link: '', techStack: [],
    })
    submissions.value = await getUserSubmissions()
    alert('作品已提交，请等待管理员审核')
  } catch (e) { alert('提交失败: ' + e.message) }
  finally { saving.value = false }
}

function statusLabel(s) {
  const map = { pending: '审核中', approved: '已通过', rejected: '已拒绝' }
  return map[s] || s
}

async function deleteSubmission(id) {
  if (!confirm('确定删除此提交记录吗？')) return
  try {
    await deleteUserSubmission(id)
    submissions.value = await getUserSubmissions()
  } catch (e) { alert('删除失败: ' + e.message) }
}
</script>

<style scoped>
.page-view { padding: 120px 0 60px; min-height: 100vh; }
.page-view h1 { font-family: var(--font-heading); font-size: 1.8rem; margin-bottom: 4px; }
.page-subtitle { font-size: 15px; color: var(--text-muted); margin-bottom: 32px; }
.dashboard-tabs { display: flex; gap: 8px; margin-bottom: 24px; }
.filter-tab { padding: 6px 18px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 13px; cursor: pointer; transition: all 0.15s; }
.filter-tab.active { background: var(--warm-terracotta); color: white; border-color: transparent; }
.tab-content { max-width: 680px; }
.editor-card { background: #fff; border: 1px solid var(--glass-border); border-radius: var(--radius-lg); padding: 24px; margin-bottom: 20px; }
.editor-card h3 { font-family: var(--font-heading); font-size: 15px; margin: 0 0 16px; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.card-header h3 { margin: 0; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.field.full { grid-column: 1/-1; }
.field span { display: block; font-size: 12px; font-weight: 500; color: var(--text-secondary); margin-bottom: 3px; }
.field input, .field textarea { width: 100%; padding: 8px 12px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 13px; background: white; color: var(--text-primary); }
.field input:disabled { background: var(--bg-soft); color: var(--text-muted); }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.inline-row { display: flex; gap: 8px; align-items: center; margin-bottom: 8px; }
.platform-select { padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; width: 110px; }
.flex-1 { flex: 1; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; }
.flex-1:focus { outline: none; border-color: var(--warm-terracotta); }
.btn-icon { width: 28px; height: 28px; border: 1px solid var(--glass-border); border-radius: 6px; background: white; color: var(--text-muted); cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-xs { padding: 4px 12px; font-size: 11px; margin-top: 4px; }
.submission-list { margin-top: 16px; }
.submission-list h3 { font-size: 14px; margin-bottom: 12px; }
.submission-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; border: 1px solid var(--glass-border); border-radius: 8px; margin-bottom: 6px; background: var(--bg-soft); font-size: 13px; }
.submission-right { display: flex; align-items: center; gap: 8px; }
.submission-status { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 999px; }
.status-pending { background: rgba(212,146,10,0.1); color: var(--warm-amber); }
.status-approved { background: rgba(46,125,50,0.1); color: #2e7d32; }
.status-rejected { background: rgba(198,40,40,0.1); color: #c62828; }
.login-prompt { text-align: center; padding: 160px 20px; }
.login-prompt p { font-size: 16px; color: var(--text-muted); margin-bottom: 20px; }
@media (max-width: 768px) { .field-grid { grid-template-columns: 1fr; } .editor-card { padding: 16px; } }
</style>
