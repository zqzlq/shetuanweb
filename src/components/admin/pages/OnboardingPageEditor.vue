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
        <h3 class="editor-title">入职流程</h3>
        <button class="btn btn-xs" @click="addStep">+ 添加</button>
      </div>
      <div v-for="(s, i) in c().steps || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ s.title || '新步骤' }}</span>
          <button class="btn-icon" @click="removeStep(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>标题</span><input :value="s.title" @input="updateStep(i, 'title', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="s.description" @input="updateStep(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">资源中心</h3>
        <button class="btn btn-xs" @click="addResource">+ 添加</button>
      </div>
      <div v-for="(r, i) in c().resources || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ r.title || '新资源' }}</span>
          <button class="btn-icon" @click="removeResource(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>标题</span><input :value="r.title" @input="updateResource(i, 'title', $event.target.value)" /></label>
          <label class="field"><span>图标</span><input :value="r.icon" @input="updateResource(i, 'icon', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="r.description" @input="updateResource(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">导师</h3>
        <button class="btn btn-xs" @click="addMentor">+ 添加</button>
      </div>
      <div v-for="(m, i) in c().mentors || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ m.name || '新导师' }}</span>
          <button class="btn-icon" @click="removeMentor(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field"><span>姓名</span><input :value="m.name" @input="updateMentor(i, 'name', $event.target.value)" /></label>
          <label class="field"><span>方向</span><input :value="m.role" @input="updateMentor(i, 'role', $event.target.value)" /></label>
          <label class="field full"><span>描述</span><textarea :value="m.description" @input="updateMentor(i, 'description', $event.target.value)" rows="2"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <div class="card-header">
        <h3 class="editor-title">常见问题</h3>
        <button class="btn btn-xs" @click="addFaq">+ 添加</button>
      </div>
      <div v-for="(f, i) in c().faq || []" :key="i" class="list-item">
        <div class="list-item-header">
          <span class="item-index">{{ f.question || '新问题' }}</span>
          <button class="btn-icon" @click="removeFaq(i)">&#10005;</button>
        </div>
        <div class="field-grid">
          <label class="field full"><span>问题</span><input :value="f.question" @input="updateFaq(i, 'question', $event.target.value)" /></label>
          <label class="field full"><span>回答</span><textarea :value="f.answer" @input="updateFaq(i, 'answer', $event.target.value)" rows="3"></textarea></label>
        </div>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">板块标题</h3>
      <div class="field-grid">
        <label class="field"><span>流程标题</span><input :value="c().sections?.stepsTitle || ''" @input="updateSections('stepsTitle', $event.target.value)" /></label>
        <label class="field"><span>资源标题</span><input :value="c().sections?.resourcesTitle || ''" @input="updateSections('resourcesTitle', $event.target.value)" /></label>
        <label class="field"><span>导师标题</span><input :value="c().sections?.mentorsTitle || ''" @input="updateSections('mentorsTitle', $event.target.value)" /></label>
        <label class="field"><span>FAQ 标题</span><input :value="c().sections?.faqTitle || ''" @input="updateSections('faqTitle', $event.target.value)" /></label>
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
function updateSections(k, v) { up({ ...c(), sections: { ...c().sections, [k]: v } }) }

function updateStep(i, k, v) {
  const arr = [...(c().steps || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), steps: arr })
}
function addStep() { up({ ...c(), steps: [...(c().steps || []), { title: '', description: '' }] }) }
function removeStep(i) { up({ ...c(), steps: (c().steps || []).filter((_, idx) => idx !== i) }) }

function updateResource(i, k, v) {
  const arr = [...(c().resources || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), resources: arr })
}
function addResource() { up({ ...c(), resources: [...(c().resources || []), { title: '', description: '', icon: '' }] }) }
function removeResource(i) { up({ ...c(), resources: (c().resources || []).filter((_, idx) => idx !== i) }) }

function updateMentor(i, k, v) {
  const arr = [...(c().mentors || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), mentors: arr })
}
function addMentor() { up({ ...c(), mentors: [...(c().mentors || []), { name: '', role: '', description: '' }] }) }
function removeMentor(i) { up({ ...c(), mentors: (c().mentors || []).filter((_, idx) => idx !== i) }) }

function updateFaq(i, k, v) {
  const arr = [...(c().faq || [])]
  arr[i] = { ...arr[i], [k]: v }
  up({ ...c(), faq: arr })
}
function addFaq() { up({ ...c(), faq: [...(c().faq || []), { question: '', answer: '' }] }) }
function removeFaq(i) { up({ ...c(), faq: (c().faq || []).filter((_, idx) => idx !== i) }) }
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
</style>
