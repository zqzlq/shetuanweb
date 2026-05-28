<template>
  <div class="page-editor">
    <div class="editor-card">
      <h3 class="editor-title">Hero</h3>
      <div class="field-grid">
        <label class="field"><span>角标</span><input :value="content.hero?.eyebrow" @input="updateHero('eyebrow', $event.target.value)" /></label>
        <label class="field"><span>标题</span><input :value="content.hero?.title" @input="updateHero('title', $event.target.value)" /></label>
        <label class="field full"><span>副标题</span><input :value="content.hero?.subtitle" @input="updateHero('subtitle', $event.target.value)" /></label>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header"><h3 class="editor-title">成员列表</h3><button class="btn btn-outline btn-xs" @click="addMember">+ 添加</button></div>
      <div v-for="(m, i) in content.members || []" :key="i" class="list-item">
        <div class="list-item-header"><span class="item-index">{{ m.name || '#' + (i+1) }}</span><button class="btn-icon" @click="removeMember(i)">&times;</button></div>
        <div class="field-grid">
          <label class="field"><span>姓名</span><input :value="m.name" @input="updateMember(i, 'name', $event.target.value)" /></label>
          <label class="field"><span>角色</span><input :value="m.role" @input="updateMember(i, 'role', $event.target.value)" /></label>
          <label class="field"><span>组别</span><input :value="m.group" @input="updateMember(i, 'group', $event.target.value)" /></label>
          <label class="field"><span>技能（逗号分隔）</span><input :value="m.skills?.join(', ')" @change="updateMember(i, 'skills', $event.target.value.split(',').map(s=>s.trim()).filter(Boolean))" /></label>
          <label class="field full"><span>头像</span><ImageUploadField :modelValue="m.avatar || ''" @update:modelValue="updateMember(i, 'avatar', $event)" /></label>
          <label class="field full"><span>描述</span><textarea :value="m.description" @input="updateMember(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
        <div class="social-links-editor">
          <div class="social-header">
            <span class="sub-title">社交链接</span>
            <button class="btn btn-outline btn-xs" @click="addSocialLink(i)">+ 添加</button>
          </div>
          <div v-for="(link, li) in m.socialLinks || []" :key="li" class="social-row">
            <select :value="link.platform" @change="updateSocialLink(i, li, 'platform', $event.target.value)" class="platform-select">
              <option value="github">GitHub</option>
              <option value="bilibili">B站</option>
              <option value="zhihu">知乎</option>
              <option value="blog">博客</option>
              <option value="douyin">抖音</option>
              <option value="weibo">微博</option>
              <option value="other">其他</option>
            </select>
            <input :value="link.url" @input="updateSocialLink(i, li, 'url', $event.target.value)" placeholder="链接地址" class="social-url" />
            <button class="btn-icon" @click="removeSocialLink(i, li)">&times;</button>
          </div>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header"><h3 class="editor-title">统计数据</h3><button class="btn btn-outline btn-xs" @click="addStat">+ 添加</button></div>
      <div v-for="(s, i) in content.stats || []" :key="i" class="inline-row">
        <input :value="s.value" @input="updateStat(i, 'value', $event.target.value)" placeholder="数值" class="w-100" />
        <input :value="s.label" @input="updateStat(i, 'label', $event.target.value)" placeholder="标签" class="w-200" />
        <button class="btn-icon" @click="removeStat(i)">&times;</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import ImageUploadField from '../ImageUploadField.vue'
const props = defineProps({ content: Object })
const emit = defineEmits(['update'])
const c = () => props.content
const up = (val) => emit('update', val)

function updateHero(k, v) { up({ ...c(), hero: { ...c().hero, [k]: v } }) }

function updateMember(i, k, v) {
  const members = [...(c().members || [])]
  members[i] = { ...members[i], [k]: v }
  up({ ...c(), members })
}
function addMember() { up({ ...c(), members: [...(c().members || []), { name: '', role: '', group: '', avatar: '', description: '', skills: [], socialLinks: [], projects: [] }] }) }

function addSocialLink(mi) {
  const members = [...(c().members || [])]
  members[mi] = { ...members[mi], socialLinks: [...(members[mi].socialLinks || []), { platform: 'github', url: '' }] }
  up({ ...c(), members })
}
function removeSocialLink(mi, li) {
  const members = [...(c().members || [])]
  members[mi] = { ...members[mi], socialLinks: (members[mi].socialLinks || []).filter((_, i) => i !== li) }
  up({ ...c(), members })
}
function updateSocialLink(mi, li, key, value) {
  const members = [...(c().members || [])]
  const links = [...(members[mi].socialLinks || [])]
  links[li] = { ...links[li], [key]: value }
  members[mi] = { ...members[mi], socialLinks: links }
  up({ ...c(), members })
}
function removeMember(i) { up({ ...c(), members: (c().members || []).filter((_, idx) => idx !== i) }) }

function updateStat(i, k, v) {
  const stats = [...(c().stats || [])]
  stats[i] = { ...stats[i], [k]: v }
  up({ ...c(), stats })
}
function addStat() { up({ ...c(), stats: [...(c().stats || []), { value: '', label: '' }] }) }
function removeStat(i) { up({ ...c(), stats: (c().stats || []).filter((_, idx) => idx !== i) }) }
</script>

<style scoped>
.page-editor { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: var(--bg-soft); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 20px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.editor-title { font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin: 0 0 12px; }
.card-header .editor-title { margin: 0; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 11px; font-weight: 500; color: var(--text-muted); margin-bottom: 3px; }
.field input, .field textarea { width: 100%; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.list-item { border: 1px solid var(--glass-border); border-radius: 8px; padding: 12px; margin-top: 8px; background: white; }
.list-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.item-index { font-size: 11px; font-weight: 600; color: var(--text-muted); }
.inline-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.inline-row input { padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; }
.inline-row input:focus { outline: none; border-color: var(--warm-terracotta); }
.w-100 { width: 100px; }
.w-200 { flex: 1; }
.btn-icon { width: 24px; height: 24px; border: 1px solid var(--glass-border); border-radius: 4px; background: white; color: var(--text-muted); font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-xs { padding: 3px 10px; font-size: 11px; }
.social-links-editor { margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--glass-border); }
.social-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.sub-title { font-size: 11px; font-weight: 600; color: var(--text-muted); }
.social-row { display: flex; gap: 8px; align-items: center; margin-bottom: 6px; }
.platform-select { padding: 6px 8px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; width: 90px; }
.social-url { flex: 1; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; }
.social-url:focus { outline: none; border-color: var(--warm-terracotta); }

@media (max-width: 768px) {
  .editor-card { padding: 12px; }
  .field-grid { grid-template-columns: 1fr; }
  .list-item { padding: 10px; }
  .inline-row { flex-wrap: wrap; }
  .inline-row input { flex: 1; min-width: 80px; }
}
</style>
