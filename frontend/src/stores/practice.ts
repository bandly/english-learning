import { defineStore } from 'pinia'
import { ref } from 'vue'
import { practiceApi } from '@/api/practice'
import type { Word, PracticeSubmit, PracticeResult } from '@/types'
import { ElMessage } from 'element-plus'

export const usePracticeStore = defineStore('practice', () => {
  const practiceWords = ref<Word[]>([])
  const currentIndex = ref(0)
  const correctCount = ref(0)
  const loading = ref(false)
  const practiceType = ref<'listening' | 'reading' | 'writing'>('listening')

  // Fetch practice words
  async function fetchPracticeWords(count = 10, difficulty?: number) {
    loading.value = true
    try {
      practiceWords.value = await practiceApi.getPracticeWords(count, difficulty)
      currentIndex.value = 0
      correctCount.value = 0
    } catch (error) {
      ElMessage.error('获取练习内容失败')
    } finally {
      loading.value = false
    }
  }

  // Get current word
  function getCurrentWord(): Word | null {
    if (currentIndex.value < practiceWords.value.length) {
      return practiceWords.value[currentIndex.value]
    }
    return null
  }

  // Submit answer
  async function submitAnswer(userAnswer: string, timeSpent?: number): Promise<PracticeResult | null> {
    const word = getCurrentWord()
    if (!word) return null

    loading.value = true
    try {
      const data: PracticeSubmit = {
        item_type: 'word',
        item_id: word.id,
        user_answer: userAnswer,
        time_spent: timeSpent
      }

      let result: PracticeResult
      if (practiceType.value === 'listening') {
        result = await practiceApi.submitListening(data)
      } else if (practiceType.value === 'reading') {
        result = await practiceApi.submitReading(data)
      } else {
        result = await practiceApi.submitWriting(data)
      }

      if (result.is_correct) {
        correctCount.value++
      }

      return result
    } catch (error) {
      ElMessage.error('提交答案失败')
      return null
    } finally {
      loading.value = false
    }
  }

  // Next word
  function nextWord() {
    currentIndex.value++
  }

  // Reset practice
  function reset() {
    currentIndex.value = 0
    correctCount.value = 0
  }

  // Check if practice complete
  function isComplete(): boolean {
    return currentIndex.value >= practiceWords.value.length
  }

  // Get accuracy rate
  function getAccuracyRate(): number {
    if (currentIndex.value === 0) return 0
    return Math.round((correctCount.value / currentIndex.value) * 100)
  }

  return {
    practiceWords,
    currentIndex,
    correctCount,
    loading,
    practiceType,
    fetchPracticeWords,
    getCurrentWord,
    submitAnswer,
    nextWord,
    reset,
    isComplete,
    getAccuracyRate
  }
})