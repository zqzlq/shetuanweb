<template>
  <div class="page-editor">
    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">比赛奖项</h3>
        <button class="btn btn-outline btn-xs" @click="addAward">+ 添加奖项</button>
      </div>
      <div class="field-grid">
        <label class="field full"><span>板块标题</span><input :value="content.awards?.title" @input="updateAwards('title', $event.target.value)" /></label>
        <label class="field full"><span>板块描述</span><input :value="content.awards?.description" @input="updateAwards('description', $event.target.value)" /></label>
      </div>
    </div>

    <div class="year-filter-bar">
      <button v-for="y in yearOptions" :key="y" class="year-tab" :class="{ active: activeYear === y }" @click="activeYear = y">
        {{ y }}<span v-if="y !== '全部'" class="year-count">({{ yearCountMap[y] || 0 }})</span>
      </button>
    </div>

    <div v-for="group in grouped" :key="group.year" class="year-section">
      <div class="year-header">
        <span class="year-label">{{ group.year }}</span>
        <span class="year-count-label">{{ group.items.length }} 项</span>
        <div class="year-line"></div>
      </div>
      <div v-for="item in group.items" :key="item._origIdx" class="list-item" :ref="el => { if (el) itemRefs.value[item._origIdx] = el }">
        <div class="list-item-header">
          <span class="item-index">{{ item.award.title || '#' + (item._origIdx + 1) }}</span>
          <span class="sort-btns">
            <button class="btn-icon" :disabled="item._origIdx === 0" @click="moveAward(item._origIdx, -1)" title="上移">&#8593;</button>
            <button class="btn-icon" :disabled="item._origIdx === totalItems - 1" @click="moveAward(item._origIdx, 1)" title="下移">&#8595;</button>
            <button class="btn-icon" @click="removeAward(item._origIdx)">&times;</button>
          </span>
        </div>
        <div class="field-grid">
          <label class="field"><span>Slug</span><input :value="item.award.slug" @input="updateAwardItem(item._origIdx, 'slug', $event.target.value)" /></label>
          <label class="field"><span>级别</span><input :value="item.award.level" @input="updateAwardItem(item._origIdx, 'level', $event.target.value)" /></label>
          <label class="field"><span>日期</span><input :value="item.award.date" @input="updateAwardItem(item._origIdx, 'date', $event.target.value)" placeholder="2026-05" /></label>
          <label class="field"><span>分类</span><select :value="item.award.category" @change="updateAwardItem(item._origIdx, 'category', $event.target.value)"><option value="" disabled>选择分类</option><option v-for="cat in categoryOptions" :key="cat" :value="cat">{{ cat }}</option></select></label>
          <label class="field full"><span>标题</span><input :value="item.award.title" @input="updateAwardItem(item._origIdx, 'title', $event.target.value)" /></label>
          <label class="field full"><span>简述</span><input :value="item.award.shortDesc" @input="updateAwardItem(item._origIdx, 'shortDesc', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="item.award.description" @input="updateAwardItem(item._origIdx, 'description', $event.target.value)" rows="2"></textarea></label>
          <label class="field full"><span>详细介绍（Markdown）</span><MarkdownEditorField :modelValue="item.award.longDescription || ''" @update:modelValue="updateAwardItem(item._origIdx, 'longDescription', $event)" /></label>
          <label class="field"><span>参赛成员（逗号分隔）</span><input :value="item.award.participants?.join(', ')" @change="updateAwardItem(item._origIdx, 'participants', $event.target.value.split(',').map(s=>s.trim()).filter(Boolean))" /></label>
          <label class="field"><span>关联项目 Slug</span><input :value="item.award.projectSlug" @input="updateAwardItem(item._origIdx, 'projectSlug', $event.target.value)" /></label>
          <label class="field full"><span>主图</span><ImageUploadField :modelValue="item.award.image || ''" @update:modelValue="updateAwardItem(item._origIdx, 'image', $event)" /></label>
          <label class="field full"><span>奖项图片</span><MultiImageUploadField :modelValue="item.award.screenshots || []" @update:modelValue="updateAwardItem(item._origIdx, 'screenshots', $event)" /></label>
        </div>
      </div>
    </div>

    <div v-if="!grouped.length" class="empty-state">
      <p>{{ activeYear === '全部' ? '暂无奖项，点击上方"添加奖项"开始' : activeYear + ' 年暂无奖项' }}</p>
    </div>
  </div>
</template>

<script setup>
import { nextTick, ref, computed, inject } from 'vue'
import ImageUploadField from '../ImageUploadField.vue'
import MultiImageUploadField from '../MultiImageUploadField.vue'
import MarkdownEditorField from '../MarkdownEditorField.vue'

const props = defineProps({ content: Object })
const emit = defineEmits(['update'])

const allCategories = inject('productCategories', computed(() => []))
const categoryOptions = computed(() => allCategories.value.filter(c => c !== '精选总览'))
const c = () => props.content
const up = (val) => emit('update', val)

const itemRefs = ref([])
const activeYear = ref('全部')

const items = computed(() => c().awards?.items || [])
const totalItems = computed(() => items.value.length)

const yearCountMap = computed(() => {
  const map = {}
  for (const a of items.value) {
    const y = a.date?.slice(0, 4) || '其他'
    map[y] = (map[y] || 0) + 1
  }
  return map
})

const yearOptions = computed(() => {
  const years = [...new Set(items.value.map(a => a.date?.slice(0, 4) || '其他'))].sort((a, b) => b.localeCompare(a))
  return ['全部', ...years]
})

const grouped = computed(() => {
  const list = items.value.map((award, i) => ({ award, _origIdx: i }))
  const filtered = activeYear.value === '全部' ? list : list.filter(item => (item.award.date?.slice(0, 4) || '其他') === activeYear.value)
  const map = new Map()
  for (const item of filtered) {
    const year = item.award.date?.slice(0, 4) || '其他'
    if (!map.has(year)) map.set(year, [])
    map.get(year).push(item)
  }
  return Array.from(map.entries())
    .sort(([a], [b]) => b.localeCompare(a))
    .map(([year, items]) => ({ year, items }))
})

function updateAwards(k, v) { up({ ...c(), awards: { ...c().awards, [k]: v } }) }

function updateAwardItem(i, k, v) {
  const items = [...(c().awards?.items || [])]
  items[i] = { ...items[i], [k]: v }
  up({ ...c(), awards: { ...c().awards, items } })
}

function addAward() {
  const now = new Date()
  const defaultDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  const newItem = { slug: '', title: '', shortDesc: '', description: '', longDescription: '', image: '', screenshots: [], level: '', date: defaultDate, category: '', participants: [], projectSlug: '' }
  up({ ...c(), awards: { ...c().awards, items: [...(c().awards?.items || []), newItem] } })
  nextTick(() => { const refs = itemRefs.value; refs[refs.length - 1]?.scrollIntoView({ behavior: 'smooth', block: 'center' }) })
}

function removeAward(i) {
  up({ ...c(), awards: { ...c().awards, items: (c().awards?.items || []).filter((_, idx) => idx !== i) } })
}

function moveAward(i, dir) {
  const items = [...(c().awards?.items || [])]; const j = i + dir
  if (j < 0 || j >= items.length) return
  ;[items[i], items[j]] = [items[j], items[i]]
  up({ ...c(), awards: { ...c().awards, items } })
}
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
.field input, .field textarea, .field select { width: 100%; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.field input:focus, .field textarea:focus, .field select:focus { outline: none; border-color: var(--warm-terracotta); }
.list-item { border: 1px solid var(--glass-border); border-radius: 8px; padding: 12px; margin-top: 8px; background: white; }
.list-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.item-index { font-size: 11px; font-weight: 600; color: var(--text-muted); }
.btn-icon { width: 24px; height: 24px; border: 1px solid var(--glass-border); border-radius: 4px; background: white; color: var(--text-muted); font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-icon:disabled { opacity: 0.3; cursor: not-allowed; }
.sort-btns { display: flex; gap: 4px; }
.btn-xs { padding: 3px 10px; font-size: 11px; }

.year-filter-bar { display: flex; gap: 6px; flex-wrap: wrap; }
.year-tab { padding: 6px 14px; border: 1px solid var(--glass-border); border-radius: 999px; background: white; font-size: 12px; font-weight: 500; color: var(--text-secondary); cursor: pointer; transition: all 0.15s; }
.year-tab:hover { border-color: var(--warm-terracotta); color: var(--text-primary); }
.year-tab.active { background: var(--warm-terracotta); color: white; border-color: var(--warm-terracotta); }
.year-count { font-size: 11px; margin-left: 3px; opacity: 0.7; }

.year-section { margin-top: 8px; }
.year-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; margin-top: 8px; }
.year-label { font-family: var(--font-heading); font-size: 18px; font-weight: 700; color: var(--text-primary); flex-shrink: 0; }
.year-count-label { font-size: 12px; color: var(--text-muted); flex-shrink: 0; }
.year-line { flex: 1; height: 1px; background: linear-gradient(90deg, var(--glass-border), transparent); }

.empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); font-size: 13px; }

@media (max-width: 768px) {
  .editor-card { padding: 12px; }
  .field-grid { grid-template-columns: 1fr; }
  .list-item { padding: 10px; }
}
</style>
