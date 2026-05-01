<template>
  <footer class="app-footer">
    <div class="container footer-inner">
      <div class="footer-left">
        <span class="footer-logo">لوحتك</span>
        <p class="footer-copy">Arabic License Plate OCR &copy; {{ year }}</p>
      </div>
      <div class="footer-right">
        <span class="footer-tech">Powered by YOLO + FastAPI + Nuxt</span>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped>
.app-footer {
  border-top: 1px solid var(--bg-card-border);
  padding: var(--space-xl) 0;
  margin-top: auto;
}

.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-md);
}

.footer-left {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.footer-logo {
  font-family: var(--font-heading);
  font-weight: 900;
  font-size: 1.2rem;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-copy {
  font-size: 0.8rem;
  color: var(--text-tertiary);
}

.footer-tech {
  font-size: 0.75rem;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
}

@media (max-width: 768px) {
  .footer-inner {
    flex-direction: column;
    text-align: center;
  }
  .footer-left {
    flex-direction: column;
    gap: var(--space-xs);
  }
}
</style>
