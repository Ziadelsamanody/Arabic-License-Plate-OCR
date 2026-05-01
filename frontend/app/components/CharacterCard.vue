<template>
  <div class="char-card glass-card" :style="{ animationDelay: `${index * 0.08}s` }">
    <span class="char-glyph text-arabic">{{ label }}</span>
    <div class="char-meta">
      <span class="char-index">#{{ index + 1 }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  index: number
}>()
</script>

<style scoped>
.char-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-lg);
  min-width: 70px;
  animation: fadeInUp 0.4s var(--ease-out) both;
  text-align: center;
}

.char-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-glow);
}

.char-glyph {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 900;
  color: var(--accent);
  line-height: 1;
}

.char-meta {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.char-index {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--text-tertiary);
}
</style>
