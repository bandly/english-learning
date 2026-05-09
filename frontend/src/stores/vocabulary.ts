import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { vocabularyApi } from '@/api/vocabulary'
import type { Word, WordCreate, WordUpdate, WordBatchCreate } from '@/types/vocabulary'
import { ElMessage } from 'element-plus'

export const useVocabularyStore = defineStore('vocabulary', () => {
  const words = ref<Word[]>([])
  const total = ref(0)
  const loading = ref(false)
  const currentWord = ref<Word | null>(null)

  // Fetch words
  async function fetchWords(skip = 0, limit = 20, tag?: string) {
    loading.value = true
    try {
      const result = await vocabularyApi.getWords(skip, limit, tag)
      words.value = result.items
      total.value = result.total
    } catch (error) {
      ElMessage.error('获取单词列表失败')
    } finally {
      loading.value = false
    }
  }

  // Create word
  async function createWord(data: WordCreate) {
    loading.value = true
    try {
      const word = await vocabularyApi.createWord(data)
      words.value.unshift(word)
      total.value++
      ElMessage.success('添加成功')
      return word
    } catch (error) {
      ElMessage.error('添加失败')
      return null
    } finally {
      loading.value = false
    }
  }

  // Update word
  async function updateWord(id: number, data: WordUpdate) {
    loading.value = true
    try {
      const word = await vocabularyApi.updateWord(id, data)
      const index = words.value.findIndex(w => w.id === id)
      if (index > -1) {
        words.value[index] = word
      }
      ElMessage.success('更新成功')
      return word
    } catch (error) {
      ElMessage.error('更新失败')
      return null
    } finally {
      loading.value = false
    }
  }

  // Delete word
  async function deleteWord(id: number) {
    loading.value = true
    try {
      await vocabularyApi.deleteWord(id)
      words.value = words.value.filter(w => w.id !== id)
      total.value--
      ElMessage.success('删除成功')
      return true
    } catch (error) {
      ElMessage.error('删除失败')
      return false
    } finally {
      loading.value = false
    }
  }

  // Batch create
  async function batchCreateWords(data: WordBatchCreate) {
    loading.value = true
    try {
      const newWords = await vocabularyApi.batchCreateWords(data)
      words.value = [...newWords, ...words.value]
      total.value += newWords.length
      ElMessage.success(`成功添加 ${newWords.length} 个单词`)
      return newWords
    } catch (error) {
      ElMessage.error('批量添加失败')
      return []
    } finally {
      loading.value = false
    }
  }

  // Get single word
  async function getWord(id: number) {
    loading.value = true
    try {
      currentWord.value = await vocabularyApi.getWord(id)
      return currentWord.value
    } catch (error) {
      ElMessage.error('获取单词失败')
      return null
    } finally {
      loading.value = false
    }
  }

  return {
    words,
    total,
    loading,
    currentWord,
    fetchWords,
    createWord,
    updateWord,
    deleteWord,
    batchCreateWords,
    getWord
  }
})