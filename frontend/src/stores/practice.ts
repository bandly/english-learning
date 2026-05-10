import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useVocabularyStore, type Word } from './vocabulary'
import sentencesData from '@/data/sentences.json'

export interface Sentence {
  id: number
  sentence: string
  translation: string
  difficulty_level: number
  tags?: string[]
}

export interface PracticeResult {
  is_correct: boolean
  correct_answer: string
  score: number
  feedback?: string
}

export const usePracticeStore = defineStore('practice', () => {
  const vocabularyStore = useVocabularyStore()

  const practiceWords = ref<Word[]>([])
  const practiceSentences = ref<Sentence[]>(sentencesData as Sentence[])
  const currentIndex = ref(0)
  const correctCount = ref(0)
  const loading = ref(false)
  const practiceType = ref<'listening' | 'reading' | 'writing'>('listening')
  const lastResult = ref<PracticeResult | null>(null)

  // 获取练习单词
  function fetchPracticeWords(count = 10, difficulty?: number) {
    let words = vocabularyStore.words
    if (difficulty) {
      words = words.filter(w => w.difficulty_level === difficulty)
    }
    // 随机选取
    practiceWords.value = shuffleArray(words).slice(0, count)
    currentIndex.value = 0
    correctCount.value = 0
    lastResult.value = null
  }

  // 获取当前单词
  function getCurrentWord(): Word | null {
    if (currentIndex.value < practiceWords.value.length) {
      return practiceWords.value[currentIndex.value]
    }
    return null
  }

  // 提交答案
  function submitAnswer(userAnswer: string): PracticeResult | null {
    const word = getCurrentWord()
    if (!word) return null

    let correctAnswer = ''
    let isCorrect = false

    if (practiceType.value === 'listening') {
      correctAnswer = word.word
      isCorrect = userAnswer.trim().toLowerCase() === correctAnswer.toLowerCase()
    } else if (practiceType.value === 'reading') {
      correctAnswer = word.meaning
      isCorrect = userAnswer.trim() === correctAnswer.trim()
    } else {
      correctAnswer = word.word
      isCorrect = userAnswer.trim().toLowerCase() === correctAnswer.toLowerCase()
    }

    const score = isCorrect ? 100 : 0

    if (isCorrect) {
      correctCount.value++
    }

    lastResult.value = {
      is_correct: isCorrect,
      correct_answer: correctAnswer,
      score,
      feedback: isCorrect ? '正确!' : `正确答案: ${correctAnswer}`
    }

    return lastResult.value
  }

  // 下一个单词
  function nextWord() {
    currentIndex.value++
    lastResult.value = null
  }

  // 重置
  function reset() {
    currentIndex.value = 0
    correctCount.value = 0
    lastResult.value = null
  }

  // 是否完成
  function isComplete(): boolean {
    return currentIndex.value >= practiceWords.value.length
  }

  // 正确率
  function getAccuracyRate(): number {
    if (currentIndex.value === 0) return 0
    return Math.round((correctCount.value / currentIndex.value) * 100)
  }

  // 随机数组
  function shuffleArray<T>(array: T[]): T[] {
    const shuffled = [...array]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    return shuffled
  }

  return {
    practiceWords,
    currentIndex,
    correctCount,
    loading,
    practiceType,
    lastResult,
    fetchPracticeWords,
    getCurrentWord,
    submitAnswer,
    nextWord,
    reset,
    isComplete,
    getAccuracyRate
  }
})