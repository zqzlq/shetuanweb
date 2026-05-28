<template>
  <div class="image-field">
    <div v-if="modelValue" class="image-preview">
      <img :src="modelValue" alt="预览" />
      <button class="remove-btn" @click.stop="handleRemove" title="删除图片">&times; 删除</button>
    </div>
    <div class="image-actions">
      <label class="btn btn-outline btn-sm upload-btn">
        <input type="file" accept="image/*" @change="handleUpload" hidden />
        {{ uploading ? '上传中...' : '上传图片' }}
      </label>
      <span class="divider">或</span>
      <input
        type="text"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        placeholder="输入图片 URL"
        class="url-input"
      />
    </div>
    <p v-if="error" class="upload-error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { uploadImage, deleteImage } from '@/services/api'

const props = defineProps({ modelValue: { type: String, default: '' } })
const emit = defineEmits(['update:modelValue'])

const uploading = ref(false)
const error = ref('')

async function handleRemove() {
  if (!confirm('确定要删除这张图片吗？')) return
  const url = props.modelValue
  emit('update:modelValue', '')
  if (url) {
    try {
      await deleteImage(url)
    } catch {
      // 静默失败
    }
  }
}

async function handleUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return

  uploading.value = true
  error.value = ''
  try {
    const data = await uploadImage(file)
    emit('update:modelValue', data.url)
  } catch (err) {
    error.value = err.message || '上传失败'
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}
</script>

<style scoped>
.image-field { display: flex; flex-direction: column; gap: 8px; }
.image-preview { position: relative; display: inline-block; max-width: 240px; }
.image-preview img { width: 100%; border-radius: 8px; border: 1px solid var(--glass-border); object-fit: cover; }
.remove-btn { position: absolute; top: 6px; right: 6px; background: rgba(224,80,80,0.85); color: white; border: none; padding: 4px 10px; border-radius: 6px; font-size: 12px; cursor: pointer; display: flex; align-items: center; gap: 2px; white-space: nowrap; z-index: 1; }
.remove-btn:hover { background: #e05050; }
.image-actions { display: flex; align-items: center; gap: 8px; }
.upload-btn { cursor: pointer; }
.divider { font-size: 12px; color: var(--text-muted); }
.url-input { flex: 1; padding: 6px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; }
.url-input:focus { outline: none; border-color: var(--warm-terracotta); }
.upload-error { font-size: 11px; color: #e05050; margin: 0; }

@media (max-width: 768px) {
  .image-actions { flex-wrap: wrap; }
  .image-actions .url-input { width: 100%; flex: auto; }
  .divider { display: none; }
}
</style>
