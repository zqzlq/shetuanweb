<template>
  <div class="page-editor">
    <div class="editor-card">
      <h3 class="editor-title">Hero</h3>
      <div class="field-grid">
        <label class="field"><span>角标</span><input :value="c().hero?.eyebrow || ''" @input="updateHero('eyebrow', $event.target.value)" /></label>
        <label class="field"><span>标题</span><input :value="c().hero?.title || ''" @input="updateHero('title', $event.target.value)" /></label>
        <label class="field full"><span>副标题</span><textarea :value="c().hero?.subtitle || ''" @input="updateHero('subtitle', $event.target.value)" rows="2"></textarea></label>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">开源仓库</h3>
        <button class="btn btn-xs" @click="addRepo">+ 添加</button>
      </div>
      <div v-for="(r, i) in c().repos || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ r.name || '新仓库' }}</span>
          <button class="btn-icon" @click="removeRepo(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>名称</span><input :value="r.name" @input="updateRepo(i, 'name', $event.target.value)" /></label>
          <label class="field"><span>语言</span><input :value="r.language" @input="updateRepo(i, 'language', $event.target.value)" /></label>
          <label class="field"><span>Star 数</span><input type="number" :value="r.stars" @input="updateRepo(i, 'stars', Number($event.target.value))" /></label>
          <label class="field"><span>链接</span><input :value="r.link" @input="updateRepo(i, 'link', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="r.description" @input="updateRepo(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">核心贡献者</h3>
        <button class="btn btn-xs" @click="addContributor">+ 添加</button>
      </div>
      <div v-for="(c2, i) in c().contributors || []" :key="i" class="inline-row">
        <input :value="c2.name" @input="updateContributor(i, 'name', $event.target.value)" placeholder="姓名" class="inline-input" />
        <input type="number" :value="c2.commits" @input="updateContributor(i, 'commits', Number($event.target.value))" placeholder="提交数" class="inline-input-sm" />
        <button class="btn-icon" @click="removeContributor(i)">&#10005;</button>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">技术栈</h3>
      <div class="field-grid">
        <label class="field full"><span>技术栈（逗号分隔）</span><input :value="(c().techStack || []).join(', ')" @change="up({ ...c(), techStack: $event.target.value.split(',').map(s => s.trim()).filter(Boolean) })" /></label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">社区信息</h3>
      <div class="field-grid">
        <label class="field full"><span>标题</span><input :value="c().community?.title || ''" @input="updateCommunity('title', $event.target.value)" /></label>
        <label class="field full"><span>描述</span><textarea :value="c().community?.description || ''" @input="updateCommunity('description', $event.target.value)" rows="2"></textarea></label>
        <label class="field"><span>Discord 链接</span><input :value="c().community?.discord || ''" @input="updateCommunity('discord', $event.target.value)" /></label>
        <label class="field"><span>Discord 文字</span><input :value="c().community?.discordText || ''" @input="updateCommunity('discordText', $event.target.value)" /></label>
        <label class="field"><span>GitHub 链接</span><input :value="c().community?.github || ''" @input="updateCommunity('github', $event.target.value)" /></label>
        <label class="field"><span>GitHub 文字</span><input :value="c().community?.githubText || ''" @input="updateCommunity('githubText', $event.target.value)" /></label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">板块标题</h3>
      <div class="field-grid">
        <label class="field"><span>仓库标题</span><input :value="c().sections?.reposTitle || ''" @input="updateSections('reposTitle', $event.target.value)" /></label>
        <label class="field"><span>技术栈标题</span><input :value="c().sections?.techStackTitle || ''" @input="updateSections('techStackTitle', $event.target.value)" /></label>
        <label class="field"><span>贡献者标题</span><input :value="c().sections?.contributorsTitle || ''" @input="updateSections('contributorsTitle', $event.target.value)" /></label>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ content: Object })
const emit = defineEmits(['update'])
const c = () => props.content
const up = (v) => emit('update', v)

function updateHero(k, v) { up({ ...c(), hero: { ...c().hero, [k]: v } }) }
function updateCommunity(k, v) { up({ ...c(), community: { ...c().community, [k]: v } }) }
function updateSections(k, v) { up({ ...c(), sections: { ...c().sections, [k]: v } }) }

function updateRepo(i, k, v) {
  const arr = [...(c().repos || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), repos: arr })
}
function addRepo() { up({ ...c(), repos: [...(c().repos || []), { name: '', description: '', stars: 0, language: '', link: '' }] }) }
function removeRepo(i) { up({ ...c(), repos: (c().repos || []).filter((_, idx) => idx !== i) }) }

function updateContributor(i, k, v) {
  const arr = [...(c().contributors || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), contributors: arr })
}
function addContributor() { up({ ...c(), contributors: [...(c().contributors || []), { name: '', commits: 0 }] }) }
function removeContributor(i) { up({ ...c(), contributors: (c().contributors || []).filter((_, idx) => idx !== i) }) }
</script>

<style scoped>
.page-editor { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: var(--bg-soft); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 20px; }
.editor-title { font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin: 0; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.card-header .editor-title { margin: 0; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 11px; font-weight: 500; color: var(--text-muted); margin-bottom: 3px; }
.field input, .field textarea { width: 100%; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.list-item { background: white; border: 1px solid var(--glass-border); border-radius: 8px; padding: 12px; margin-top: 8px; }
.list-item-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.item-index { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.btn-icon { width: 24px; height: 24px; border: none; background: none; font-size: 14px; color: var(--text-muted); cursor: pointer; border-radius: 4px; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { background: var(--bg-soft); color: #e05050; }
.btn-xs { padding: 4px 10px; font-size: 11px; border: 1px solid var(--glass-border); border-radius: 4px; background: white; cursor: pointer; color: var(--text-secondary); }
.btn-xs:hover { border-color: var(--warm-terracotta); color: var(--warm-terracotta); }
.inline-row { display: flex; align-items: center; gap: 8px; margin-top: 8px; }
.inline-input { flex: 1; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.inline-input:focus { outline: none; border-color: var(--warm-terracotta); }
.inline-input-sm { width: 100px; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.inline-input-sm:focus { outline: none; border-color: var(--warm-terracotta); }
</style>
