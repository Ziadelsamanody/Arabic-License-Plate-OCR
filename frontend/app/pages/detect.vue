<template>
  <div class="detect-page">
    <LoadingOverlay :visible="loading" text="Detecting characters..." />

    <section class="section detect-section">
      <div class="container container-sm">
        <!-- Header -->
        <div class="page-header animate-fade-in-up">
          <h1 class="page-title">
            <span class="gradient-text">Detect</span> Plate Characters
          </h1>
          <p class="page-subtitle">
            Upload an Egyptian license plate image to identify all Arabic characters
          </p>
        </div>

        <!-- Upload -->
        <div class="upload-area animate-fade-in-up delay-1">
          <DropZone ref="dropZoneRef" @file-selected="onFileSelected" @file-cleared="onFileCleared" />

          <!-- Action buttons -->
          <div class="action-row" v-if="selectedFile">
            <button
              class="btn btn-primary btn-lg detect-btn"
              :disabled="loading || !selectedFile"
              @click="runDetection"
              id="detect-btn"
            >
              <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
                <path d="M1 1h6v6H1V1zm0 10h6v6H1v-6zm10-10h6v6h-6V1zm0 10h6v6h-6v-6z"/>
              </svg>
              Detect Characters
            </button>
            <button class="btn btn-ghost" @click="resetAll" id="reset-btn">Reset</button>
          </div>
        </div>

        <!-- Error -->
        <div v-if="error" class="error-banner glass-card animate-fade-in-up" id="error-banner">
          <span class="error-icon">⚠️</span>
          <div class="error-content">
            <strong>Detection Failed</strong>
            <p>{{ error }}</p>
          </div>
        </div>

        <!-- Results -->
        <Transition name="results">
          <div v-if="result" class="results-area" id="results-section">
            <!-- Annotated image -->
            <div class="result-block animate-fade-in-up">
              <h2 class="result-heading">Detected Characters</h2>
              <DetectionCanvas
                :image-src="imageDataUrl"
                :detections="result.detections"
              />
            </div>

            <!-- Character cards -->
            <div class="result-block animate-fade-in-up delay-1">
              <h3 class="result-subheading">Individual Characters</h3>
              <div class="char-cards-row">
                <CharacterCard
                  v-for="(label, i) in result.labels"
                  :key="i"
                  :label="label"
                  :index="i"
                />
              </div>
            </div>

            <!-- Plate result -->
            <div class="result-block animate-fade-in-up delay-2">
              <h3 class="result-subheading">Plate Output</h3>
              <PlateResult
                :plate-text="result.plate_text"
                :char-count="result.labels.length"
                :processing-time="processingTime"
              />
            </div>

            <hr class="divider" />

            <!-- Try again -->
            <div class="try-again animate-fade-in-up delay-3">
              <button class="btn btn-secondary" @click="resetAll" id="try-again-btn">
                ← Upload Another Image
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'Detect — لوحتك' })

const { result, loading, error, processingTime, detect, reset } = useDetection()
const { addEntry } = useHistory()

const dropZoneRef = ref<InstanceType<typeof DropZone> | null>(null) as any
const selectedFile = ref<File | null>(null)
const imageDataUrl = ref('')

function onFileSelected(file: File, dataUrl: string) {
  selectedFile.value = file
  imageDataUrl.value = dataUrl
  reset()
}

function onFileCleared() {
  selectedFile.value = null
  imageDataUrl.value = ''
  reset()
}

async function runDetection() {
  if (!selectedFile.value) return
  const res = await detect(selectedFile.value)
  if (res && selectedFile.value) {
    addEntry(selectedFile.value.name, imageDataUrl.value, res)
  }
}

function resetAll() {
  reset()
  selectedFile.value = null
  imageDataUrl.value = ''
  dropZoneRef.value?.clearFile?.()
}
</script>

<style scoped>
.detect-section {
  padding-top: calc(64px + var(--space-2xl));
}

.page-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.page-title {
  margin-bottom: var(--space-sm);
}

.page-subtitle {
  font-size: 1.05rem;
}

/* Upload area */
.upload-area {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.action-row {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
}

.detect-btn {
  flex: 1;
  max-width: 300px;
}

/* Error */
.error-banner {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  padding: var(--space-lg);
  margin-top: var(--space-lg);
  border: 1px solid rgba(248, 113, 113, 0.2);
  background: var(--error-dim);
}

.error-icon { font-size: 1.4rem; }
.error-content strong { color: var(--error); font-size: 0.9rem; }
.error-content p { font-size: 0.85rem; color: var(--text-secondary); margin-top: 4px; }

/* Results */
.results-area {
  margin-top: var(--space-2xl);
  display: flex;
  flex-direction: column;
  gap: var(--space-2xl);
}

.result-block {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.result-heading {
  font-size: 1.3rem;
}

.result-subheading {
  font-size: 1rem;
  color: var(--text-secondary);
}

.char-cards-row {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
  justify-content: center;
}

.try-again {
  display: flex;
  justify-content: center;
}

/* Transition */
.results-enter-active {
  transition: all 0.5s var(--ease-out);
}

.results-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
</style>
