import apiClient from './client'
import type { PracticeSubmit, PracticeResult, Word } from '@/types'

export const practiceApi = {
  // Get practice words
  async getPracticeWords(count = 10, difficulty?: number): Promise<Word[]> {
    const params: Record<string, unknown> = { count }
    if (difficulty) params.difficulty = difficulty
    return apiClient.get('/practice/words', { params })
  },

  // Submit listening practice
  async submitListening(data: PracticeSubmit): Promise<PracticeResult> {
    return apiClient.post('/practice/listening', data)
  },

  // Submit reading practice
  async submitReading(data: PracticeSubmit): Promise<PracticeResult> {
    return apiClient.post('/practice/reading', data)
  },

  // Submit writing practice
  async submitWriting(data: PracticeSubmit): Promise<PracticeResult> {
    return apiClient.post('/practice/writing', data)
  }
}