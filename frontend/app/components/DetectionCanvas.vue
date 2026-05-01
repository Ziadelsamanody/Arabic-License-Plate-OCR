<template>
  <div class="detection-canvas-wrapper" id="detection-canvas">
    <canvas ref="canvasRef" class="detection-canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import type { Detection } from '~/composables/useDetection'

const props = defineProps<{
  imageSrc: string
  detections: Detection[]
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)

function draw() {
  const canvas = canvasRef.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const img = new Image()
  img.onload = () => {
    canvas.width = img.naturalWidth
    canvas.height = img.naturalHeight

    ctx.drawImage(img, 0, 0)

    // Draw bounding boxes
    props.detections.forEach((det, i) => {
      const [x1, y1, x2, y2] = det.bbox
      const w = x2 - x1
      const h = y2 - y1

      // Box
      ctx.strokeStyle = '#00b4d8'
      ctx.lineWidth = Math.max(2, img.naturalWidth * 0.004)
      ctx.shadowColor = 'rgba(0, 180, 216, 0.5)'
      ctx.shadowBlur = 8
      ctx.strokeRect(x1, y1, w, h)
      ctx.shadowBlur = 0

      // Label background
      const fontSize = Math.max(14, img.naturalWidth * 0.03)
      ctx.font = `bold ${fontSize}px Cairo, sans-serif`
      const label = det.label
      const textMetrics = ctx.measureText(label)
      const textW = textMetrics.width + 12
      const textH = fontSize + 8

      ctx.fillStyle = 'rgba(0, 180, 216, 0.9)'
      const labelY = y1 - textH > 0 ? y1 - textH : y1
      ctx.beginPath()
      ctx.roundRect(x1, labelY, textW, textH, 4)
      ctx.fill()

      // Label text
      ctx.fillStyle = '#fff'
      ctx.textBaseline = 'middle'
      ctx.fillText(label, x1 + 6, labelY + textH / 2)
    })
  }
  img.src = props.imageSrc
}

watch(() => [props.imageSrc, props.detections], draw, { immediate: false })

onMounted(() => {
  if (props.imageSrc) draw()
})
</script>

<style scoped>
.detection-canvas-wrapper {
  width: 100%;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--bg-card-border);
  background: #000;
}

.detection-canvas {
  width: 100%;
  height: auto;
  display: block;
}
</style>
