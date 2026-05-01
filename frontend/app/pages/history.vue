<template>
  <div class="history-page">
    <section class="section">
      <div class="container container-sm" style="padding-top: calc(64px + var(--space-2xl));">
        <div class="page-header animate-fade-in-up">
          <h1 class="page-title">
            Detection <span class="gradient-text">History</span>
          </h1>
          <p class="page-subtitle">Your past plate scans, stored locally on your device</p>
        </div>

        <!-- Actions -->
        <div v-if="!isEmpty" class="history-actions animate-fade-in-up delay-1">
          <span class="history-count badge badge-accent">
            {{ history.length }} scan{{ history.length === 1 ? '' : 's' }}
          </span>
          <button class="btn btn-ghost btn-sm" @click="confirmClear" id="clear-history-btn">
            🗑️ Clear All
          </button>
        </div>

        <!-- List -->
        <div v-if="!isEmpty" class="history-list">
          <TransitionGroup name="list" tag="div" class="history-list-inner">
            <HistoryItem
              v-for="entry in history"
              :key="entry.id"
              :entry="entry"
              @delete="removeEntry"
              class="animate-fade-in-up"
            />
          </TransitionGroup>
        </div>

        <!-- Empty state -->
        <div v-else class="empty-state glass-card animate-fade-in-up">
          <div class="empty-icon">🔍</div>
          <h3>No detections yet</h3>
          <p>Upload a plate image to get started. Your scan history will appear here.</p>
          <NuxtLink to="/detect" class="btn btn-primary" id="empty-cta">
            Start Detecting
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'History — لوحتك' })

const { history, isEmpty, removeEntry, clearAll } = useHistory()

function confirmClear() {
  if (confirm('Remove all detection history? This cannot be undone.')) {
    clearAll()
  }
}
</script>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.page-title { margin-bottom: var(--space-sm); }

.history-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-lg);
}

.btn-sm {
  padding: 6px 14px;
  font-size: 0.8rem;
}

.history-list-inner {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

/* Empty */
.empty-state {
  text-align: center;
  padding: var(--space-3xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
}

.empty-icon {
  font-size: 3rem;
}

.empty-state h3 {
  color: var(--text-primary);
}

.empty-state p {
  max-width: 300px;
  font-size: 0.9rem;
}

/* List transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s var(--ease-out);
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
