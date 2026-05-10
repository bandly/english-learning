<template>
  <Layout>
    <div class="vocabulary-page">
      <div class="page-header">
        <h2>词库管理</h2>
        <div class="stats-overview">
          <el-statistic title="总词汇" :value="vocabularyStore.total" />
          <el-statistic title="今日复习" :value="reviewStore.todayItems.length" />
          <el-statistic title="已掌握" :value="reviewStore.stats.masteredCount" />
        </div>
      </div>

      <!-- 筛选 -->
      <div class="card-container filter-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-input v-model="searchKeyword" placeholder="搜索单词或含义" clearable>
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </el-col>
          <el-col :span="4">
            <el-select v-model="selectedTag" placeholder="标签筛选" clearable>
              <el-option v-for="tag in vocabularyStore.allTags" :key="tag" :label="tag" :value="tag" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="selectedDifficulty" placeholder="难度筛选" clearable>
              <el-option v-for="n in 5" :key="n" :label="难度 ${n}" :value="n" />
            </el-select>
          </el-col>
        </el-row>
      </div>

      <!-- Word List -->
      <div class="card-container word-list-section">
        <el-table :data="filteredWords" stripe>
          <el-table-column prop="word" label="单词" width="150">
            <template #default="{ row }">
              <span class="word-text">{{ row.word }}</span>
              <el-button size="small" circle @click="playAudio(row.word)" style="margin-left: 8px">
                <el-icon><Headset /></el-icon>
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="phonetic" label="音标" width="120" />
          <el-table-column prop="meaning" label="含义" />
          <el-table-column prop="part_of_speech" label="词性" width="80" />
          <el-table-column prop="difficulty_level" label="难度" width="100">
            <template #default="{ row }">
              <el-rate v-model="row.difficulty_level" disabled :max="5" />
            </template>
          </el-table-column>
          <el-table-column prop="tags" label="标签" width="120">
            <template #default="{ row }">
              <el-tag v-for="tag in row.tags" :key="tag" size="small" style="margin-right: 4px">
                {{ tag }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="example_sentence" label="例句" />
        </el-table>

        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="filteredWords.length"
          layout="total, prev, pager, next"
          style="margin-top: 20px; justify-content: center;"
        />
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useVocabularyStore } from '@/stores/vocabulary'
import { useReviewStore } from '@/stores/review'
import Layout from '@/components/Layout.vue'

const vocabularyStore = useVocabularyStore()
const reviewStore = useReviewStore()

const searchKeyword = ref('')
const selectedTag = ref('')
const selectedDifficulty = ref<number | undefined>()
const currentPage = ref(1)
const pageSize = 20

// 过滤后的单词列表
const filteredWords = computed(() => {
  let words = vocabularyStore.words

  if (searchKeyword.value) {
    words = vocabularyStore.search(searchKeyword.value)
  }

  if (selectedTag.value) {
    words = words.filter(w => w.tags?.includes(selectedTag.value))
  }

  if (selectedDifficulty.value) {
    words = words.filter(w => w.difficulty_level === selectedDifficulty.value)
  }

  return words
})

// 播放音频
const playAudio = (word: string) => {
  const utterance = new SpeechSynthesisUtterance(word)
  utterance.lang = 'en-US'
  speechSynthesis.speak(utterance)
}

onMounted(() => {
  reviewStore.init()
})
</script>

<style scoped>
.vocabulary-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.stats-overview {
  display: flex;
  gap: 40px;
}

.filter-section {
  margin-bottom: 20px;
}

.word-text {
  font-weight: bold;
  font-size: 16px;
}
</style>