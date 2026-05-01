<template>
  <div class="plate-result" id="plate-result-display">
    <div class="plate-frame">
      <div class="plate-header">
        <span class="plate-country-en">EGYPT</span>
        <span class="plate-country-ar">مصر</span>
      </div>
      <div class="plate-body">
        <span class="plate-text text-arabic">{{ plateText }}</span>
      </div>
    </div>
    <div class="plate-stats">
      <div class="stat">
        <span class="stat-label">Characters</span>
        <span class="stat-value">{{ charCount }}</span>
      </div>
      <div class="stat">
        <span class="stat-label">Time</span>
        <span class="stat-value">{{ processingTime }}ms</span>
      </div>
      <div class="stat">
        <span class="stat-label">Status</span>
        <span class="badge badge-success">Success</span>
      </div>
    </div>
    <button class="btn btn-secondary copy-btn" @click="copyText" id="copy-plate-btn">
      {{ copied ? '✓ Copied!' : '📋 Copy Plate Text' }}
    </button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  plateText: string
  charCount: number
  processingTime: number
}>()

const copied = ref(false)

async function copyText() {
  try {
    await navigator.clipboard.writeText(props.plateText)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  } catch { /* ignore */ }
}
</script>

<style scoped>
.plate-result { display: flex; flex-direction: column; align-items: center; gap: var(--space-lg); }
.plate-frame { width: 100%; max-width: 380px; border-radius: var(--radius-md); overflow: hidden; border: 3px solid rgba(255,255,255,0.15); box-shadow: 0 8px 32px rgba(0,0,0,0.4); animation: fadeInUp 0.5s var(--ease-out) both; }
.plate-header { background: linear-gradient(135deg, #1a8fbf, #0d6eab); padding: 8px 20px; display: flex; align-items: center; justify-content: space-between; }
.plate-country-en { font-family: var(--font-body); font-weight: 700; font-size: 0.9rem; color: #fff; letter-spacing: 0.15em; text-transform: uppercase; }
.plate-country-ar { font-family: var(--font-heading); font-weight: 700; font-size: 1.1rem; color: #fff; }
.plate-body { background: linear-gradient(to bottom, #f5f0e8, #e8e0d0); padding: 20px 24px; display: flex; align-items: center; justify-content: center; min-height: 80px; }
.plate-text { font-family: var(--font-heading); font-size: 2.5rem; font-weight: 900; color: #1a1a1a; letter-spacing: 0.1em; }
.plate-stats { display: flex; gap: var(--space-xl); flex-wrap: wrap; justify-content: center; }
.stat { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.stat-label { font-size: 0.7rem; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.08em; }
.stat-value { font-family: var(--font-mono); font-size: 1.1rem; font-weight: 600; color: var(--text-primary); }
.copy-btn { width: 100%; max-width: 380px; }
</style>
