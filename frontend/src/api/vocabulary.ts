import apiClient from './client'
import type { Word, WordCreate, WordUpdate, WordListResponse, WordBatchCreate } from '@/types/vocabulary'

export const vocabularyApi = {
  // Create word
  async createWord(data: WordCreate): Promise<Word> {
    return apiClient.post('/words', data)
  },

  // Get word list
  async getWords(skip = 0, limit = 20, tag?: string): Promise<WordListResponse> {
    const params: Record<string, unknown> = { skip, limit }
    if (tag) params.tag = tag
    return apiClient.get('/words', { params })
  },

  // Get single word
  async getWord(id: number): Promise<Word> {
    return apiClient.get(`/words/${id}`)
  },

  // Update word
  async updateWord(id: number, data: WordUpdate): Promise<Word> {
    return apiClient.put(`/words/${id}`, data)
  },

  // Delete word
  async deleteWord(id: number): Promise<void> {
    return apiClient.delete(`/words/${id}`)
  },

  // Batch create words
  async batchCreateWords(data: WordBatchCreate): Promise<Word[]> {
    return apiClient.post('/words/batch', data)
  }
}