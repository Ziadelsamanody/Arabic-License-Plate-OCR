<template>
  <div class="feature-card glass-card" :id="id">
    <div class="feature-icon-wrap">
      <span class="feature-icon" v-html="icon"></span>
    </div>
    <h3 class="feature-title">{{ title }}</h3>
    <p class="feature-desc">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  icon: string
  title: string
  description: string
  id?: string
}>()
</script>

<style scoped>
.feature-card {
  padding: var(--space-xl);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-md);
  transition: all var(--transition-normal);
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-glow);
}

.feature-icon-wrap {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-dim);
  border-radius: var(--radius-md);
  color: var(--accent);
  transition: all var(--transition-normal);
}

.feature-card:hover .feature-icon-wrap {
  background: var(--accent-gradient);
  color: #fff;
  box-shadow: 0 4px 15px rgba(0, 180, 216, 0.3);
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.feature-desc {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>
