import { defineStore } from 'pinia'
import { ref } from 'vue'
import vocabularyData from '@/data/vocabulary.json'

export interface Word {
  id: number
  word: string
  phonetic?: string
  meaning: string
  part_of_speech?: string
  example_sentence?: string
  difficulty_level: number
  tags?: string[]
  abbreviation_of?: string[]  // 缩写由哪些单词组成
  related_abbreviations?: string[]  // 单词关联哪些缩写
}

export const useVocabularyStore = defineStore('vocabulary', () => {
  const words = ref<Word[]>(vocabularyData as Word[])
  const loading = ref(false)

  // 过滤
  function filterByTag(tag: string) {
    return words.value.filter(w => w.tags?.includes(tag))
  }

  function filterByDifficulty(level: number) {
    return words.value.filter(w => w.difficulty_level === level)
  }

  // 搜索
  function search(keyword: string) {
    const lower = keyword.toLowerCase()
    return words.value.filter(w =>
      w.word.toLowerCase().includes(lower) ||
      w.meaning.toLowerCase().includes(lower)
    )
  }

  // 获取总数
  const total = words.value.length

  // 获取所有标签
  const allTags = Array.from(new Set(words.value.flatMap(w => w.tags || [])))

  return {
    words,
    total,
    loading,
    filterByTag,
    filterByDifficulty,
    search,
    allTags
  }
})