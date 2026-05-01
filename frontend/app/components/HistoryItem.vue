<template>
  <div class="history-item glass-card" :id="`history-${entry.id}`">
    <div class="history-thumb">
      <img :src="entry.imageDataUrl" :alt="entry.fileName" />
    </div>
    <div class="history-info">
      <div class="history-top">
        <span class="history-plate text-arabic">{{ entry.result.plate_text }}</span>
        <span class="history-chars badge badge-accent">{{ entry.result.labels.length }} chars</span>
      </div>
      <div class="history-bottom">
        <span class="history-file">{{ entry.fileName }}</span>
        <span class="history-time">{{ formatTime(entry.timestamp) }}</span>
      </div>
    </div>
    <button class="btn btn-ghost btn-icon delete-btn" @click.stop="$emit('delete', entry.id)" title="Remove">
      ✕
    </button>
  </div>
</template>

<script setup lang="ts">
import type { HistoryEntry } from '~/composables/useHistory'

defineProps<{ entry: HistoryEntry }>()
defineEmits<{ (e: 'delete', id: string): void }>()

function formatTime(ts: number) {
  const d = new Date(ts)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.history-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  cursor: default;
}

.history-thumb {
  width: 64px;
  height: 44px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  flex-shrink: 0;
  background: #000;
}

.history-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.history-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-top {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.history-plate {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.history-bottom {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.history-file,
.history-time {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
}

.delete-btn {
  opacity: 0;
  transition: opacity var(--transition-fast);
  flex-shrink: 0;
  font-size: 0.8rem;
}

.history-item:hover .delete-btn {
  opacity: 1;
}
</style>
