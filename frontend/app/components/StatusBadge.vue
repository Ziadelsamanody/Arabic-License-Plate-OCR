<template>
  <span class="status-badge" :class="statusClass" :title="statusTitle" id="health-status-badge">
    <span class="status-dot"></span>
    <span class="status-label hide-mobile">{{ statusLabel }}</span>
  </span>
</template>

<script setup lang="ts">
const { isOnline, device } = useHealth()

const statusClass = computed(() => (isOnline.value ? 'online' : 'offline'))
const statusLabel = computed(() => (isOnline.value ? device.value.toUpperCase() : 'Offline'))
const statusTitle = computed(() =>
  isOnline.value ? `Backend online (${device.value})` : 'Backend is offline'
)
</script>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 600;
  font-family: var(--font-mono);
  letter-spacing: 0.05em;
  transition: all var(--transition-normal);
}

.status-badge.online {
  background: var(--success-dim);
  color: var(--success);
}

.status-badge.offline {
  background: var(--error-dim);
  color: var(--error);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

.online .status-dot {
  background: var(--success);
  box-shadow: 0 0 8px var(--success);
  animation: pulse 2s infinite;
}

.offline .status-dot {
  background: var(--error);
}
</style>
