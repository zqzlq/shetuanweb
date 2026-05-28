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
      <div class="card-header"><h3 class="editor-title">文章列表</h3><button class="btn btn-outline btn-xs" @click="addPost">+ 添加</button></div>
      <div v-for="(p, i) in content.posts || []" :key="i" class="list-item">
        <div class="list-item-header"><span class="item-index">{{ p.title || '#' + (i+1) }}</span><button class="btn-icon" @click="removePost(i)">&times;</button></div>
        <div class="field-grid">
          <label class="field"><span>标题</span><input :value="p.title" @input="updatePost(i, 'title', $event.target.value)" /></label>
          <label class="field"><span>分类</span><input :value="p.category" @input="updatePost(i, 'category', $event.target.value)" /></label>
          <label class="field"><span>日期</span><input :value="p.date" @input="updatePost(i, 'date', $event.target.value)" /></label>
          <label class="field"><span>阅读时间</span><input :value="p.readTime" @input="updatePost(i, 'readTime', $event.target.value)" /></label>
          <label class="field full"><span>摘要</span><textarea :value="p.excerpt" @input="updatePost(i, 'excerpt', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header"><h3 class="editor-title">分类</h3><button class="btn btn-outline btn-xs" @click="addCat">+ 添加</button></div>
      <div v-for="(cat, i) in content.categories || []" :key="i" class="inline-row">
        <input :value="cat" @input="updateCat(i, $event.target.value)" class="w-200" />
        <button class="btn-icon" @click="removeCat(i)">&times;</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ content: Object })
const emit = defineEmits(['update'])
const c = () => props.content
const up = (val) => emit('update', val)

function updateHero(k, v) { up({ ...c(), hero: { ...c().hero, [k]: v } }) }

function updatePost(i, k, v) {
  const posts = [...(c().posts || [])]
  posts[i] = { ...posts[i], [k]: v }
  up({ ...c(), posts })
}
function addPost() { up({ ...c(), posts: [...(c().posts || []), { title: '', excerpt: '', category: '', date: '', readTime: '', link: '' }] }) }
function removePost(i) { up({ ...c(), posts: (c().posts || []).filter((_, idx) => idx !== i) }) }

function updateCat(i, v) {
  const categories = [...(c().categories || [])]
  categories[i] = v
  up({ ...c(), categories })
}
function addCat() { up({ ...c(), categories: [...(c().categories || []), ''] }) }
function removeCat(i) { up({ ...c(), categories: (c().categories || []).filter((_, idx) => idx !== i) }) }
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
.w-200 { flex: 1; }
.btn-icon { width: 24px; height: 24px; border: 1px solid var(--glass-border); border-radius: 4px; background: white; color: var(--text-muted); font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-xs { padding: 3px 10px; font-size: 11px; }

@media (max-width: 768px) {
  .editor-card { padding: 12px; }
  .field-grid { grid-template-columns: 1fr; }
  .list-item { padding: 10px; }
}
</style>
