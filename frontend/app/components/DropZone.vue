<template>
  <div
    class="dropzone"
    :class="{ active: isDragging, 'has-file': !!previewUrl }"
    @dragenter.prevent="onDragEnter"
    @dragover.prevent
    @dragleave.prevent="onDragLeave"
    @drop.prevent="onDrop"
    @click="openPicker"
    id="image-drop-zone"
  >
    <input
      ref="fileInput"
      type="file"
      accept="image/jpeg,image/png,image/webp"
      class="file-input"
      @change="onFileChange"
      id="image-file-input"
    />

    <!-- Preview -->
    <div v-if="previewUrl" class="preview-container">
      <img :src="previewUrl" alt="Uploaded plate" class="preview-image" />
      <div class="preview-overlay">
        <button class="btn btn-secondary btn-sm" @click.stop="clearFile" id="clear-image-btn">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="currentColor">
            <path d="M1.7 1.7a1 1 0 011.4 0L7 5.6l3.9-3.9a1 1 0 111.4 1.4L8.4 7l3.9 3.9a1 1 0 01-1.4 1.4L7 8.4l-3.9 3.9a1 1 0 01-1.4-1.4L5.6 7 1.7 3.1a1 1 0 010-1.4z"/>
          </svg>
          Remove
        </button>
        <span class="file-name">{{ fileName }}</span>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="dropzone-content">
      <div class="dropzone-icon" :class="{ bounce: isDragging }">
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="6" y="12" width="36" height="24" rx="4" stroke="currentColor" stroke-width="2"/>
          <path d="M18 30l4-6 3 3 5-7 6 10H12l6-0z" fill="currentColor" opacity="0.2"/>
          <circle cx="17" cy="20" r="3" stroke="currentColor" stroke-width="2"/>
          <path d="M24 6v6m-3-3h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      <p class="dropzone-title">
        {{ isDragging ? 'Drop it here!' : 'Drop your plate image' }}
      </p>
      <p class="dropzone-subtitle">or click to browse · JPG, PNG, WebP</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (e: 'file-selected', file: File, dataUrl: string): void
  (e: 'file-cleared'): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const previewUrl = ref<string | null>(null)
const fileName = ref('')
let dragCounter = 0

function openPicker() {
  if (!previewUrl.value) {
    fileInput.value?.click()
  }
}

function onDragEnter() {
  dragCounter++
  isDragging.value = true
}

function onDragLeave() {
  dragCounter--
  if (dragCounter <= 0) {
    isDragging.value = false
    dragCounter = 0
  }
}

function onDrop(e: DragEvent) {
  isDragging.value = false
  dragCounter = 0
  const file = e.dataTransfer?.files?.[0]
  if (file && file.type.startsWith('image/')) {
    handleFile(file)
  }
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    handleFile(file)
  }
}

function handleFile(file: File) {
  fileName.value = file.name
  const reader = new FileReader()
  reader.onload = (e) => {
    const dataUrl = e.target?.result as string
    previewUrl.value = dataUrl
    emit('file-selected', file, dataUrl)
  }
  reader.readAsDataURL(file)
}

function clearFile() {
  previewUrl.value = null
  fileName.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  emit('file-cleared')
}

// Expose for parent reset
defineExpose({ clearFile })
</script>

<style scoped>
.dropzone {
  position: relative;
  border: 2px dashed rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-lg);
  padding: var(--space-3xl) var(--space-xl);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  background: var(--bg-card);
  overflow: hidden;
}

.dropzone:hover {
  border-color: rgba(255, 255, 255, 0.15);
  background: var(--bg-card-hover);
}

.dropzone.active {
  border-color: var(--accent);
  background: var(--accent-dim);
  box-shadow: inset 0 0 30px rgba(0, 180, 216, 0.05);
}

.dropzone.has-file {
  padding: 0;
  border-style: solid;
  border-color: var(--bg-card-border);
  cursor: default;
}

.file-input {
  display: none;
}

/* Empty state */
.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
}

.dropzone-icon {
  color: var(--text-tertiary);
  transition: all var(--transition-normal);
}

.dropzone:hover .dropzone-icon {
  color: var(--accent);
  transform: translateY(-4px);
}

.dropzone-icon.bounce {
  animation: float 1s ease-in-out infinite;
  color: var(--accent);
}

.dropzone-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.dropzone-subtitle {
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

/* Preview */
.preview-container {
  position: relative;
  width: 100%;
}

.preview-image {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  display: block;
  border-radius: calc(var(--radius-lg) - 2px);
  background: #000;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md);
  background: linear-gradient(to bottom, rgba(0,0,0,0.6), transparent);
  border-radius: calc(var(--radius-lg) - 2px) calc(var(--radius-lg) - 2px) 0 0;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.preview-container:hover .preview-overlay {
  opacity: 1;
}

.file-name {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.7);
  font-family: var(--font-mono);
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-sm {
  padding: 6px 14px;
  font-size: 0.8rem;
}
</style>
