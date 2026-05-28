<template>
  <div class="multi-image-field">
    <div v-if="modelValue?.length" class="image-grid">
      <div v-for="(url, i) in modelValue" :key="i" class="image-thumb">
        <img :src="url" alt="图片" />
        <button class="remove-btn" @click.stop="removeAt(i)" title="删除图片">&times;</button>
      </div>
    </div>
    <div class="add-row">
      <label class="btn btn-outline btn-sm upload-btn">
        <input type="file" accept="image/*" @change="handleUpload" hidden />
        {{ uploading ? '上传中...' : '上传图片' }}
      </label>
      <span class="divider">或</span>
      <div class="url-add">
        <input v-model="urlInput" type="text" placeholder="输入图片 URL" class="url-input" @keydown.enter.prevent="addUrl" />
        <button class="btn btn-outline btn-sm" :disabled="!urlInput.trim()" @click="addUrl">添加</button>
      </div>
    </div>
    <p v-if="error" class="upload-error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { uploadImage, deleteImage } from '@/services/api'

const props = defineProps({ modelValue: { type: Array, default: () => [] } })
const emit = defineEmits(['update:modelValue'])

const uploading = ref(false)
const error = ref('')
const urlInput = ref('')

function update(list) {
  emit('update:modelValue', list)
}

async function removeAt(i) {
  if (!confirm('确定要删除这张图片吗？')) return
  const url = props.modelValue[i]
  // 从列表中移除
  update(props.modelValue.filter((_, idx) => idx !== i))
  // 从 OSS 删除
  if (url) {
    try {
      await deleteImage(url)
    } catch {
      // 静默失败，不影响 UI
    }
  }
}

function addUrl() {
  const url = urlInput.value.trim()
  if (!url) return
  update([...props.modelValue, url])
  urlInput.value = ''
}

async function handleUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  uploading.value = true
  error.value = ''
  try {
    const data = await uploadImage(file)
    update([...props.modelValue, data.url])
  } catch (err) {
    error.value = err.message || '上传失败'
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}
</script>

<style scoped>
.multi-image-field { display: flex; flex-direction: column; gap: 8px; }
.image-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.image-thumb { position: relative; width: 100px; height: 100px; border-radius: 8px; overflow: hidden; border: 1px solid var(--glass-border); }
.image-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.remove-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  background: rgba(0,0,0,0.6);
  color: white;
  border: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  padding: 0;
  transition: background 0.15s;
}
.remove-btn:hover { background: rgba(224,80,80,0.9); }
.add-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.upload-btn { cursor: pointer; }
.divider { font-size: 12px; color: var(--text-muted); }
.url-add { display: flex; gap: 6px; flex: 1; min-width: 200px; }
.url-input { flex: 1; padding: 6px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; }
.url-input:focus { outline: none; border-color: var(--warm-terracotta); }
.upload-error { font-size: 11px; color: #e05050; margin: 0; }
</style>
