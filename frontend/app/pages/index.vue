<template>
  <div class="home-page">
    <!-- Hero -->
    <section class="hero section" id="hero-section">
      <div class="container hero-container">
        <div class="hero-content">
          <div class="hero-badge badge badge-accent animate-fade-in-up">
            🤖 AI-Powered Detection
          </div>
          <h1 class="hero-title animate-fade-in-up delay-1">
            Arabic License Plate
            <span class="gradient-text">Recognition</span>
          </h1>
          <p class="hero-desc animate-fade-in-up delay-2">
            Upload an Egyptian license plate image and instantly detect all
            Arabic characters using advanced YOLO deep learning. Fast, accurate,
            and beautifully simple.
          </p>
          <div class="hero-actions animate-fade-in-up delay-3">
            <NuxtLink to="/detect" class="btn btn-primary btn-lg" id="cta-try-now">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
                <path d="M1 1h6v6H1V1zm0 10h6v6H1v-6zm10-10h6v6h-6V1zm0 10h6v6h-6v-6z"/>
              </svg>
              Try It Now
            </NuxtLink>
            <NuxtLink to="/about" class="btn btn-secondary" id="cta-learn-more">
              Learn More →
            </NuxtLink>
          </div>
        </div>

        <!-- Demo plate preview -->
        <div class="hero-visual animate-fade-in-up delay-4">
          <div class="demo-plate-frame">
            <div class="demo-plate-header">
              <span>EGYPT</span>
              <span style="font-family: var(--font-heading)">مصر</span>
            </div>
            <div class="demo-plate-body">
              <span class="demo-plate-text text-arabic" ref="animatedText">{{ animatedPlate }}</span>
            </div>
          </div>
          <div class="demo-glow"></div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features section" id="features-section">
      <div class="container">
        <h2 class="section-title animate-fade-in-up">
          Why <span class="gradient-text">لوحتك</span>?
        </h2>
        <p class="section-subtitle animate-fade-in-up delay-1">
          Built with cutting-edge technology for accurate Arabic plate recognition
        </p>
        <div class="features-grid">
          <FeatureCard
            v-for="(feat, i) in features"
            :key="i"
            :icon="feat.icon"
            :title="feat.title"
            :description="feat.description"
            :id="`feature-${i}`"
            class="animate-fade-in-up"
            :style="{ animationDelay: `${0.2 + i * 0.1}s` }"
          />
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="how-it-works section" id="how-section">
      <div class="container">
        <h2 class="section-title animate-fade-in-up">How It Works</h2>
        <div class="steps-grid">
          <div v-for="(step, i) in steps" :key="i" class="step-card glass-card animate-fade-in-up" :style="{ animationDelay: `${0.1 + i * 0.12}s` }">
            <div class="step-number">{{ i + 1 }}</div>
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-desc">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section section" id="cta-section">
      <div class="container cta-container">
        <div class="cta-card glass-card">
          <h2 class="cta-title">Ready to detect?</h2>
          <p class="cta-desc">Upload your first plate image and see the AI in action.</p>
          <NuxtLink to="/detect" class="btn btn-primary btn-lg" id="cta-bottom">
            Start Detecting →
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'لوحتك — Arabic License Plate OCR' })

const features = [
  {
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
    title: 'Instant Detection',
    description: 'YOLO-based inference processes your plate in milliseconds, delivering real-time results with bounding boxes and character labels.',
  },
  {
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>',
    title: 'Full Arabic Support',
    description: 'Trained on Egyptian plates with all Arabic numerals (٠-٩) and 18 Arabic letters with precise class mapping.',
  },
  {
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>',
    title: 'Visual Bounding Boxes',
    description: 'See exactly where each character was detected with color-coded bounding boxes drawn directly on your uploaded image.',
  },
  {
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M15 1H9v2h6V1zm-4 13h2V8h-2v6zm8.03-6.61l1.42-1.42c-.43-.51-.9-.99-1.41-1.41l-1.42 1.42A8.962 8.962 0 0012 4c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-2.12-.74-4.07-1.97-5.61zM12 20c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>',
    title: 'Detection History',
    description: 'All your past detections are saved locally. Browse, review, and compare previous plate scans anytime.',
  },
  {
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M19.35 10.04A7.49 7.49 0 0012 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 000 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/></svg>',
    title: 'REST API Ready',
    description: 'Built on FastAPI with OpenAPI docs. Integrate plate detection into any application with a simple HTTP request.',
  },
  {
    icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>',
    title: 'Privacy First',
    description: 'All processing happens on your local machine. No images are sent to external servers or stored in the cloud.',
  },
]

const steps = [
  { title: 'Upload', desc: 'Drag & drop or browse for a plate image (JPG, PNG, WebP).' },
  { title: 'Detect', desc: 'YOLO model analyzes each character with bounding box precision.' },
  { title: 'Results', desc: 'View detected characters, bounding boxes, and the full plate text.' },
]

// Animated plate demo
const plates = ['٩٨٣دسي', '٣٠٥بطن', '١٢٧اسم', '٤٥٦جهل']
const currentPlateIndex = ref(0)
const animatedPlate = ref(plates[0])

onMounted(() => {
  setInterval(() => {
    currentPlateIndex.value = (currentPlateIndex.value + 1) % plates.length
    animatedPlate.value = plates[currentPlateIndex.value]
  }, 3000)
})
</script>

<style scoped>
/* Hero */
.hero-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3xl);
  align-items: center;
  min-height: calc(100vh - 64px);
  padding-top: 64px;
}

.hero-badge {
  font-size: 0.8rem;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.hero-title {
  font-size: clamp(2.2rem, 5vw, 3.8rem);
  font-weight: 900;
  line-height: 1.1;
}

.hero-desc {
  font-size: 1.1rem;
  max-width: 500px;
}

.hero-actions {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.btn-lg {
  padding: 14px 32px;
  font-size: 1rem;
}

/* Demo visual */
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.demo-plate-frame {
  width: 340px;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: float 4s ease-in-out infinite;
  position: relative;
  z-index: 1;
}

.demo-plate-header {
  background: linear-gradient(135deg, #1a8fbf, #0d6eab);
  padding: 10px 24px;
  display: flex;
  justify-content: space-between;
  color: #fff;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 0.1em;
}

.demo-plate-body {
  background: linear-gradient(to bottom, #f5f0e8, #e8e0d0);
  padding: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.demo-plate-text {
  font-family: var(--font-heading);
  font-size: 3rem;
  font-weight: 900;
  color: #1a1a1a;
  letter-spacing: 0.08em;
  transition: all 0.5s var(--ease-out);
}

.demo-glow {
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(0, 180, 216, 0.15), transparent 70%);
  border-radius: 50%;
  z-index: 0;
  animation: glowPulse 3s ease-in-out infinite;
}

/* Features */
.section-title {
  text-align: center;
  margin-bottom: var(--space-sm);
}

.section-subtitle {
  text-align: center;
  margin-bottom: var(--space-2xl);
  color: var(--text-secondary);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
}

/* Steps */
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
  margin-top: var(--space-2xl);
}

.step-card {
  padding: var(--space-xl);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
}

.step-number {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-gradient);
  color: #fff;
  font-weight: 900;
  font-size: 1.2rem;
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(0, 180, 216, 0.3);
}

.step-title {
  font-size: 1.1rem;
  color: var(--text-primary);
}

.step-desc {
  font-size: 0.875rem;
}

/* CTA */
.cta-card {
  text-align: center;
  padding: var(--space-3xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-lg);
}

.cta-title {
  font-size: 2rem;
}

.cta-desc {
  font-size: 1.05rem;
  max-width: 400px;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-container {
    grid-template-columns: 1fr;
    text-align: center;
    gap: var(--space-2xl);
  }

  .hero-desc { max-width: 100%; }
  .hero-actions { justify-content: center; }
  .features-grid { grid-template-columns: 1fr; }
  .steps-grid { grid-template-columns: 1fr; }
  .demo-plate-frame { width: 280px; }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .features-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
