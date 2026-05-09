<template>
  <Layout>
    <div class="vocabulary-page">
      <div class="page-header">
        <h2>词汇管理</h2>
        <div class="stats-overview">
          <el-statistic title="总词汇" :value="vocabularyStore.total" />
          <el-statistic title="今日复习" :value="reviewStore.dueToday" />
        </div>
      </div>

      <!-- Add Word Form -->
      <div class="card-container add-word-section">
        <h3>添加单词</h3>
        <el-form :model="wordForm" label-width="80px">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="单词">
                <el-input v-model="wordForm.word" placeholder="输入单词" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="音标">
                <el-input v-model="wordForm.phonetic" placeholder="/.../" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="含义">
                <el-input v-model="wordForm.meaning" placeholder="中文含义" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="词性">
                <el-select v-model="wordForm.part_of_speech" placeholder="词性">
                  <el-option label="名词" value="noun" />
                  <el-option label="动词" value="verb" />
                  <el-option label="形容词" value="adj" />
                  <el-option label="副词" value="adv" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="例句">
                <el-input v-model="wordForm.example_sentence" placeholder="例句" />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="难度">
                <el-select v-model="wordForm.difficulty_level" placeholder="难度">
                  <el-option v-for="n in 5" :key="n" :label="n" :value="n" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="标签">
                <el-input v-model="tagsInput" placeholder="逗号分隔" />
              </el-form-item>
            </el-col>
            <el-col :span="2">
              <el-button type="primary" @click="handleAddWord">添加</el-button>
            </el-col>
          </el-row>
        </el-form>
      </div>

      <!-- Word List -->
      <div class="card-container word-list-section">
        <el-table :data="vocabularyStore.words" v-loading="vocabularyStore.loading" stripe>
          <el-table-column prop="word" label="单词" width="150" />
          <el-table-column prop="phonetic" label="音标" width="120" />
          <el-table-column prop="meaning" label="含义" />
          <el-table-column prop="part_of_speech" label="词性" width="80" />
          <el-table-column prop="difficulty_level" label="难度" width="80">
            <template #default="{ row }">
              <el-rate v-model="row.difficulty_level" disabled :max="5" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="vocabularyStore.total"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
          style="margin-top: 20px; justify-content: center;"
        />
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useVocabularyStore } from '@/stores/vocabulary'
import { useReviewStore } from '@/stores/review'
import { ElMessage, ElMessageBox } from 'element-plus'
import Layout from '@/components/Layout.vue'

const vocabularyStore = useVocabularyStore()
const reviewStore = useReviewStore()

const currentPage = ref(1)
const pageSize = 20

const wordForm = reactive({
  word: '',
  phonetic: '',
  meaning: '',
  part_of_speech: '',
  example_sentence: '',
  difficulty_level: 1,
  tags: []
})

const tagsInput = ref('')

const handleAddWord = async () => {
  if (!wordForm.word || !wordForm.meaning) {
    ElMessage.warning('请输入单词和含义')
    return
  }

  const tags = tagsInput.value.split(',').map(t => t.trim()).filter(t => t)
  await vocabularyStore.createWord({
    ...wordForm,
    tags
  })

  // Reset form
  wordForm.word = ''
  wordForm.phonetic = ''
  wordForm.meaning = ''
  wordForm.part_of_speech = ''
  wordForm.example_sentence = ''
  wordForm.difficulty_level = 1
  tagsInput.value = ''
}

const handleEdit = (word: any) => {
  ElMessage.info('编辑功能待实现')
}

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除该单词？', '提示', { type: 'warning' })
    await vocabularyStore.deleteWord(id)
  } catch {
    // Cancelled
  }
}

const handlePageChange = (page: number) => {
  vocabularyStore.fetchWords((page - 1) * pageSize, pageSize)
}

onMounted(() => {
  vocabularyStore.fetchWords(0, pageSize)
  reviewStore.fetchStats()
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

.add-word-section {
  margin-bottom: 20px;
}

.add-word-section h3 {
  margin: 0 0 20px 0;
}
</style>