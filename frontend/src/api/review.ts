import apiClient from './client'
import type { ReviewSubmit, ReviewResult, TodayReviewResponse, ReviewStats } from '@/types/review'

export const reviewApi = {
  // Get today's review
  async getTodayReview(): Promise<TodayReviewResponse> {
    return apiClient.get('/review/today')
  },

  // Submit review
  async submitReview(data: ReviewSubmit): Promise<ReviewResult> {
    return apiClient.post('/review/submit', data)
  },

  // Get review stats
  async getStats(): Promise<ReviewStats> {
    return apiClient.get('/review/stats')
  }
}