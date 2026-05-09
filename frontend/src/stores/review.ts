import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { reviewApi } from '@/api/review'
import type { ReviewItem, TodayReviewResponse, ReviewStats, ReviewSubmit } from '@/types/review'
import { ElMessage } from 'element-plus'

export const useReviewStore = defineStore('review', () => {
  const todayItems = ref<ReviewItem[]>([])
  const stats = ref<ReviewStats | null>(null)
  const loading = ref(false)

  const dueToday = computed(() => todayItems.value.length)
  const masteredCount = computed(() => stats.value?.mastered_count || 0)

  // Fetch today's review
  async function fetchTodayReview() {
    loading.value = true
    try {
      const result: TodayReviewResponse = await reviewApi.getTodayReview()
      todayItems.value = result.review_items
    } catch (error) {
      ElMessage.error('获取复习列表失败')
    } finally {
      loading.value = false
    }
  }

  // Submit review
  async function submitReview(itemType: string, itemId: number, score: number) {
    loading.value = true
    try {
      const data: ReviewSubmit = {
        item_type: itemType,
        item_id: itemId,
        score
      }
      const result = await reviewApi.submitReview(data)

      // Remove from today's list
      const index = todayItems.value.findIndex(
        item => item.item_type === itemType && item.item_id === itemId
      )
      if (index > -1) {
        todayItems.value.splice(index, 1)
      }

      // Refresh stats
      await fetchStats()

      return result
    } catch (error) {
      ElMessage.error('提交复习结果失败')
      return null
    } finally {
      loading.value = false
    }
  }

  // Fetch stats
  async function fetchStats() {
    loading.value = true
    try {
      stats.value = await reviewApi.getStats()
    } catch (error) {
      ElMessage.error('获取统计数据失败')
    } finally {
      loading.value = false
    }
  }

  return {
    todayItems,
    stats,
    loading,
    dueToday,
    masteredCount,
    fetchTodayReview,
    submitReview,
    fetchStats
  }
})