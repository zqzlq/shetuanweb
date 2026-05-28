<template>
  <div class="page-editor">
    <div class="editor-card">
      <h3 class="editor-title">Hero</h3>
      <div class="field-grid">
        <label class="field full"><span>标题</span><input :value="content.hero?.title" @input="updateHero('title', $event.target.value)" /></label>
        <label class="field full"><span>副标题</span><input :value="content.hero?.subtitle" @input="updateHero('subtitle', $event.target.value)" /></label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">表单配置</h3>
      <div class="field-grid">
        <label class="field full"><span>步骤（逗号分隔）</span><input :value="content.form?.steps?.join(', ')" @input="updateFormSteps($event.target.value)" /></label>
      </div>
      <div class="sub-section">
        <div class="card-header"><h4 class="sub-title">组别</h4><button class="btn btn-outline btn-xs" @click="addGroup">+ 添加</button></div>
        <div v-for="(g, i) in content.form?.groups || []" :key="i" class="inline-row">
          <input :value="g.id" @input="updateGroup(i, 'id', $event.target.value)" placeholder="ID" class="w-100" />
          <input :value="g.name" @input="updateGroup(i, 'name', $event.target.value)" placeholder="名称" class="w-150" />
          <input :value="g.tag" @input="updateGroup(i, 'tag', $event.target.value)" placeholder="标签" class="w-150" />
          <button class="btn-icon" @click="removeGroup(i)">&times;</button>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header"><h3 class="editor-title">福利</h3><button class="btn btn-outline btn-xs" @click="addBenefit">+ 添加</button></div>
      <div v-for="(b, i) in content.benefits || []" :key="i" class="list-item">
        <div class="list-item-header"><span class="item-index">{{ b.title || '#' + (i+1) }}</span><button class="btn-icon" @click="removeBenefit(i)">&times;</button></div>
        <div class="field-grid">
          <label class="field full"><span>标题</span><input :value="b.title" @input="updateBenefit(i, 'title', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="b.description" @input="updateBenefit(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header"><h3 class="editor-title">FAQ</h3><button class="btn btn-outline btn-xs" @click="addFaq">+ 添加</button></div>
      <div v-for="(f, i) in content.faq || []" :key="i" class="list-item">
        <div class="list-item-header"><span class="item-index">#{{ i+1 }}</span><button class="btn-icon" @click="removeFaq(i)">&times;</button></div>
        <div class="field-grid">
          <label class="field full"><span>问题</span><input :value="f.question" @input="updateFaq(i, 'question', $event.target.value)" /></label>
          <label class="field full"><span>回答</span><textarea :value="f.answer" @input="updateFaq(i, 'answer', $event.target.value)" rows="2"></textarea></label>
        </div>
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

function updateFormSteps(val) {
  const steps = val.split(',').map(s => s.trim()).filter(Boolean)
  up({ ...c(), form: { ...c().form, steps } })
}

function updateGroup(i, k, v) {
  const groups = [...(c().form?.groups || [])]
  groups[i] = { ...groups[i], [k]: v }
  up({ ...c(), form: { ...c().form, groups } })
}
function addGroup() { up({ ...c(), form: { ...c().form, groups: [...(c().form?.groups || []), { id: '', name: '', tag: '' }] } }) }
function removeGroup(i) { up({ ...c(), form: { ...c().form, groups: (c().form?.groups || []).filter((_, idx) => idx !== i) } }) }

function updateBenefit(i, k, v) {
  const benefits = [...(c().benefits || [])]
  benefits[i] = { ...benefits[i], [k]: v }
  up({ ...c(), benefits })
}
function addBenefit() { up({ ...c(), benefits: [...(c().benefits || []), { title: '', description: '' }] }) }
function removeBenefit(i) { up({ ...c(), benefits: (c().benefits || []).filter((_, idx) => idx !== i) }) }

function updateFaq(i, k, v) {
  const faq = [...(c().faq || [])]
  faq[i] = { ...faq[i], [k]: v }
  up({ ...c(), faq })
}
function addFaq() { up({ ...c(), faq: [...(c().faq || []), { question: '', answer: '' }] }) }
function removeFaq(i) { up({ ...c(), faq: (c().faq || []).filter((_, idx) => idx !== i) }) }
</script>

<style scoped>
.page-editor { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: var(--bg-soft); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 20px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.editor-title { font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin: 0 0 12px; }
.card-header .editor-title, .sub-title { margin: 0; }
.sub-title { font-size: 13px; font-weight: 600; color: var(--text-secondary); }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 11px; font-weight: 500; color: var(--text-muted); margin-bottom: 3px; }
.field input, .field textarea { width: 100%; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.field input:focus, .field textarea:focus { outline: none; border-color: var(--warm-terracotta); }
.sub-section { margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--glass-border); }
.list-item { border: 1px solid var(--glass-border); border-radius: 8px; padding: 12px; margin-top: 8px; background: white; }
.list-item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.item-index { font-size: 11px; font-weight: 600; color: var(--text-muted); }
.inline-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.inline-row input { padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; }
.inline-row input:focus { outline: none; border-color: var(--warm-terracotta); }
.w-100 { width: 100px; }
.w-150 { width: 150px; }
.btn-icon { width: 24px; height: 24px; border: 1px solid var(--glass-border); border-radius: 4px; background: white; color: var(--text-muted); font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon:hover { color: #e05050; border-color: #e05050; }
.btn-xs { padding: 3px 10px; font-size: 11px; }

@media (max-width: 768px) {
  .editor-card { padding: 12px; }
  .field-grid { grid-template-columns: 1fr; }
  .inline-row { flex-wrap: wrap; }
  .inline-row input { flex: 1; min-width: 60px; }
  .w-100, .w-150 { width: auto; }
}
</style>
