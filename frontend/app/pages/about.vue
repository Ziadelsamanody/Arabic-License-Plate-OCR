<template>
  <div class="about-page">
    <section class="section">
      <div class="container container-sm" style="padding-top: calc(64px + var(--space-2xl));">
        <div class="page-header animate-fade-in-up">
          <h1 class="page-title">
            About <span class="gradient-text">لوحتك</span>
          </h1>
          <p class="page-subtitle">
            AI-powered Arabic license plate character recognition for Egyptian plates
          </p>
        </div>

        <!-- About sections -->
        <div class="about-content">
          <div class="about-block glass-card animate-fade-in-up delay-1">
            <h2>🧠 How It Works</h2>
            <p>
              لوحتك uses a custom-trained <strong>YOLOv8</strong> deep learning model specifically
              designed for Egyptian license plate characters. The model detects and classifies
              all Arabic numerals (٠ through ٩) and 18 Arabic letters commonly found on Egyptian plates.
            </p>
            <p>
              When you upload an image, it's sent to the FastAPI backend where the YOLO model
              runs inference, identifies each character's position (bounding box), and maps
              the detected classes to their Arabic Unicode equivalents. Characters are sorted
              left-to-right to reconstruct the plate text.
            </p>
          </div>

          <div class="about-block glass-card animate-fade-in-up delay-2">
            <h2>⚙️ Technology Stack</h2>
            <div class="tech-grid">
              <div class="tech-item">
                <span class="tech-label">Model</span>
                <span class="tech-value">YOLOv8 (Ultralytics)</span>
              </div>
              <div class="tech-item">
                <span class="tech-label">Backend</span>
                <span class="tech-value">FastAPI + Python</span>
              </div>
              <div class="tech-item">
                <span class="tech-label">Frontend</span>
                <span class="tech-value">Nuxt 4 + Vue 3</span>
              </div>
              <div class="tech-item">
                <span class="tech-label">Vision</span>
                <span class="tech-value">OpenCV + NumPy</span>
              </div>
              <div class="tech-item">
                <span class="tech-label">Deep Learning</span>
                <span class="tech-value">PyTorch</span>
              </div>
              <div class="tech-item">
                <span class="tech-label">GPU Support</span>
                <span class="tech-value">CUDA (optional)</span>
              </div>
            </div>
          </div>

          <div class="about-block glass-card animate-fade-in-up delay-3">
            <h2>📊 Supported Characters</h2>
            <div class="char-showcase">
              <div class="char-group">
                <h3>Arabic Numerals</h3>
                <div class="char-list">
                  <span v-for="n in numerals" :key="n" class="char-chip text-arabic">{{ n }}</span>
                </div>
              </div>
              <div class="char-group">
                <h3>Arabic Letters</h3>
                <div class="char-list">
                  <span v-for="l in letters" :key="l" class="char-chip text-arabic">{{ l }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="about-block glass-card animate-fade-in-up delay-4">
            <h2>🔒 Privacy</h2>
            <p>
              All image processing happens <strong>locally on your machine</strong>. No images
              are uploaded to external servers. Detection history is stored only in your
              browser's localStorage and never transmitted anywhere.
            </p>
          </div>

          <div class="about-block glass-card animate-fade-in-up delay-5">
            <h2>🚀 API Endpoints</h2>
            <div class="api-list">
              <div class="api-item">
                <span class="badge badge-success">GET</span>
                <code>/api/health</code>
                <span class="api-desc">Check service status and device info</span>
              </div>
              <div class="api-item">
                <span class="badge badge-accent">POST</span>
                <code>/api/detect</code>
                <span class="api-desc">Upload an image and detect plate characters</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'About — لوحتك' })

const numerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
const letters = ['ع', 'ا', 'ب', 'د', 'س', 'ف', 'ج', 'ه', 'ك', 'ل', 'م', 'ن', 'ر', 'ص', 'ط', 'و', 'ي', 'ز']
</script>

<style scoped>
.page-header { text-align: center; margin-bottom: var(--space-2xl); }
.page-title { margin-bottom: var(--space-sm); }

.about-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.about-block {
  padding: var(--space-xl);
}

.about-block h2 {
  font-size: 1.2rem;
  margin-bottom: var(--space-md);
  color: var(--text-primary);
}

.about-block p {
  margin-bottom: var(--space-md);
  line-height: 1.8;
}

.about-block p:last-child { margin-bottom: 0; }

/* Tech grid */
.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-md);
}

.tech-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: var(--space-md);
  background: var(--bg-card);
  border-radius: var(--radius-sm);
  border: 1px solid var(--bg-card-border);
}

.tech-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.tech-value {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

/* Char showcase */
.char-showcase {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.char-group h3 {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-sm);
}

.char-list {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

.char-chip {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-dim);
  color: var(--accent);
  border-radius: var(--radius-sm);
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 1.1rem;
  transition: all var(--transition-fast);
}

.char-chip:hover {
  background: var(--accent-gradient);
  color: #fff;
  transform: scale(1.15);
}

/* API */
.api-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.api-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.api-item code {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--text-primary);
  background: var(--bg-card);
  padding: 4px 10px;
  border-radius: var(--radius-sm);
}

.api-desc {
  font-size: 0.8rem;
  color: var(--text-secondary);
}
</style>
