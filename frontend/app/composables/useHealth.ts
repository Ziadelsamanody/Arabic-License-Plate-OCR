export interface HealthStatus {
  status: string
  device: string
}

export function useHealth() {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase as string

  const isOnline = ref(false)
  const device = ref<string>('unknown')
  const checking = ref(false)

  async function check() {
    checking.value = true
    try {
      const data = await $fetch<HealthStatus>(`${apiBase}/api/health`, {
        timeout: 5000,
      })
      isOnline.value = data.status === 'working'
      device.value = data.device
    } catch {
      isOnline.value = false
      device.value = 'unknown'
    } finally {
      checking.value = false
    }
  }

  let interval: ReturnType<typeof setInterval> | null = null

  function startPolling(ms = 15000) {
    check()
    interval = setInterval(check, ms)
  }

  function stopPolling() {
    if (interval) {
      clearInterval(interval)
      interval = null
    }
  }

  onMounted(() => startPolling())
  onUnmounted(() => stopPolling())

  return {
    isOnline,
    device,
    checking,
    check,
  }
}
