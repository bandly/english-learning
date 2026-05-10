import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useVocabularyStore, type Word } from './vocabulary'
import type { Sentence } from './practice'

// 复习记录存储在localStorage
interface ReviewRecord {
  wordId: number
  itemType: 'word' | 'sentence'
  reviewCount: number
  easeFactor: number
  intervalDays: number
  nextReviewDate: string
  lastReviewDate: string
  status: 'learning' | 'review' | 'mastered'
}

export const useReviewStore = defineStore('review', () => {
  const vocabularyStore = useVocabularyStore()

  // 从localStorage读取复习记录
  const reviewRecords = ref<ReviewRecord[]>([])

  // 初始化 - 从localStorage加载
  function init() {
    const saved = localStorage.getItem('reviewRecords')
    if (saved) {
      reviewRecords.value = JSON.parse(saved)
    } else {
      // 为所有单词创建初始复习计划
      vocabularyStore.words.forEach(word => {
        reviewRecords.value.push({
          wordId: word.id,
          itemType: 'word',
          reviewCount: 0,
          easeFactor: 2.5,
          intervalDays: 1,
          nextReviewDate: new Date().toISOString(),
          lastReviewDate: '',
          status: 'learning'
        })
      })
      saveToLocalStorage()
    }
  }

  // 保存到localStorage
  function saveToLocalStorage() {
    localStorage.setItem('reviewRecords', JSON.stringify(reviewRecords.value))
  }

  // 今日复习列表
  const todayItems = computed(() => {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)

    return reviewRecords.value
      .filter(r => new Date(r.nextReviewDate) <= tomorrow)
      .map(record => {
        const word = vocabularyStore.words.find(w => w.id === record.wordId)
        return {
          id: record.wordId,
          word: word?.word || '',
          meaning: word?.meaning || '',
          phonetic: word?.phonetic || '',
          reviewCount: record.reviewCount,
          intervalDays: record.intervalDays,
          nextReviewDate: record.nextReviewDate,
          status: record.status
        }
      })
  })

  // 统计
  const stats = computed(() => {
    const mastered = reviewRecords.value.filter(r => r.status === 'mastered').length
    const learning = reviewRecords.value.filter(r => r.status === 'learning').length
    const review = reviewRecords.value.filter(r => r.status === 'review').length

    return {
      totalWords: vocabularyStore.total,
      masteredCount: mastered,
      learningCount: learning,
      reviewCount: review,
      todayReviews: todayItems.value.length
    }
  })

  // 提交复习 (SM-2算法)
  function submitReview(wordId: number, quality: number) {
    const record = reviewRecords.value.find(r => r.wordId === wordId)
    if (!record) return

    // SM-2算法计算下次复习时间
    let newEaseFactor = record.easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    newEaseFactor = Math.max(1.3, newEaseFactor)

    let intervalDays = 0
    if (quality < 3) {
      intervalDays = 1
      record.reviewCount = 0
      newEaseFactor = 2.5
    } else {
      if (record.reviewCount === 0) {
        intervalDays = 1
      } else if (record.reviewCount === 1) {
        intervalDays = 2
      } else {
        intervalDays = Math.ceil(record.intervalDays * newEaseFactor)
      }
      record.reviewCount++
    }

    // 更新状态
    let status = 'learning'
    if (intervalDays >= 30) {
      status = 'mastered'
    } else if (record.reviewCount > 0) {
      status = 'review'
    }

    // 计算下次复习日期
    const nextReviewDate = new Date()
    nextReviewDate.setDate(nextReviewDate.getDate() + intervalDays)

    // 更新记录
    record.easeFactor = newEaseFactor
    record.intervalDays = intervalDays
    record.nextReviewDate = nextReviewDate.toISOString()
    record.lastReviewDate = new Date().toISOString()
    record.status = status

    saveToLocalStorage()
  }

  // 清除复习记录（重新开始）
  function clearRecords() {
    localStorage.removeItem('reviewRecords')
    reviewRecords.value = []
    init()
  }

  return {
    reviewRecords,
    todayItems,
    stats,
    init,
    submitReview,
    clearRecords
  }
})