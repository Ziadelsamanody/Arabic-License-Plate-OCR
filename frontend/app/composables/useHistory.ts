import type { DetectionResult } from './useDetection'

export interface HistoryEntry {
  id: string
  timestamp: number
  fileName: string
  imageDataUrl: string
  result: DetectionResult
}

const STORAGE_KEY = 'plate-ocr-history'

function loadFromStorage(): HistoryEntry[] {
  if (typeof window === 'undefined') return []
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function saveToStorage(entries: HistoryEntry[]) {
  if (typeof window === 'undefined') return
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries))
}

const history = ref<HistoryEntry[]>([])

export function useHistory() {
  // Initialize on first use (client-side only)
  if (import.meta.client && history.value.length === 0) {
    history.value = loadFromStorage()
  }

  function addEntry(fileName: string, imageDataUrl: string, result: DetectionResult) {
    const entry: HistoryEntry = {
      id: crypto.randomUUID(),
      timestamp: Date.now(),
      fileName,
      imageDataUrl,
      result,
    }
    history.value.unshift(entry)
    // Keep last 50 entries
    if (history.value.length > 50) {
      history.value = history.value.slice(0, 50)
    }
    saveToStorage(history.value)
  }

  function removeEntry(id: string) {
    history.value = history.value.filter((e) => e.id !== id)
    saveToStorage(history.value)
  }

  function clearAll() {
    history.value = []
    saveToStorage([])
  }

  const isEmpty = computed(() => history.value.length === 0)

  return {
    history,
    isEmpty,
    addEntry,
    removeEntry,
    clearAll,
  }
}
