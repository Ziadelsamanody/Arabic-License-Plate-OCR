export interface Detection {
  label: string
  bbox: [number, number, number, number]
}

export interface DetectionResult {
  success: boolean
  labels: string[]
  plate_text: string
  detections: Detection[]
}

export function useDetection() {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase as string

  const result = ref<DetectionResult | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const processingTime = ref(0)

  async function detect(file: File): Promise<DetectionResult | null> {
    loading.value = true
    error.value = null
    result.value = null

    const formData = new FormData()
    formData.append('image', file)

    const start = performance.now()

    try {
      const response = await $fetch<DetectionResult>(`${apiBase}/api/detect`, {
        method: 'POST',
        body: formData,
      })

      processingTime.value = Math.round(performance.now() - start)
      result.value = response
      return response
    } catch (err: any) {
      processingTime.value = Math.round(performance.now() - start)
      error.value = err?.data?.detail || err?.message || 'Detection failed. Is the backend running?'
      return null
    } finally {
      loading.value = false
    }
  }

  function reset() {
    result.value = null
    error.value = null
    loading.value = false
    processingTime.value = 0
  }

  return {
    result,
    loading,
    error,
    processingTime,
    detect,
    reset,
  }
}
