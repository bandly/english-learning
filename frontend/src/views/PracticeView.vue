<template>
  <Layout>
    <div class="practice-page">
      <div class="page-header">
        <h2>练习中心</h2>
        <el-radio-group v-model="practiceStore.practiceType">
          <el-radio-button value="listening">听力练习</el-radio-button>
          <el-radio-button value="reading">阅读练习</el-radio-button>
          <el-radio-button value="writing">写作练习</el-radio-button>
        </el-radio-group>
      </div>

      <!-- Practice Area -->
      <div class="card-container practice-area" v-if="!practiceStore.isComplete()">
        <div class="practice-header">
          <span>进度: {{ practiceStore.currentIndex + 1 }} / {{ practiceStore.practiceWords.length }}</span>
          <span>正确率: {{ practiceStore.getAccuracyRate() }}%</span>
        </div>

        <!-- Word Display -->
        <div class="word-display" v-if="currentWord">
          <template v-if="practiceStore.practiceType === 'listening'">
            <el-button size="large" circle @click="playAudio">
              <el-icon size="32"><Headset /></el-icon>
            </el-button>
            <p>点击播放，听音拼写</p>
          </template>

          <template v-else-if="practiceStore.practiceType === 'reading'">
            <h2 class="word-text">{{ currentWord.word }}</h2>
            <p v-if="currentWord.phonetic" class="phonetic">{{ currentWord.phonetic }}</p>
            <p>选择正确的含义</p>
          </template>

          <template v-else>
            <h2 class="word-text">{{ currentWord.meaning }}</h2>
            <p>根据含义拼写单词</p>
          </template>
        </div>

        <!-- Answer Input -->
        <div class="answer-section">
          <el-input
            v-model="userAnswer"
            size="large"
            placeholder="输入答案"
            @keyup.enter="submitAnswer"
            style="width: 400px;"
          />
          <el-button type="primary" size="large" @click="submitAnswer" :loading="practiceStore.loading">
            提交
          </el-button>
        </div>

        <!-- Result Feedback -->
        <el-alert
          v-if="lastResult"
          :title="lastResult.is_correct ? '正确!' : '错误'"
          :type="lastResult.is_correct ? 'success' : 'error'"
          :description="`正确答案: ${lastResult.correct_answer}`"
          show-icon
          style="margin-top: 20px;"
        />
      </div>

      <!-- Complete -->
      <div class="card-container complete-section" v-else>
        <el-result icon="success" title="练习完成!" :sub-title="`正确率: ${practiceStore.getAccuracyRate()}%`">
          <template #extra>
            <el-button type="primary" @click="startNewRound">再来一轮</el-button>
            <el-button @click="$router.push('/review')">开始复习</el-button>
          </template>
        </el-result>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { usePracticeStore } from '@/stores/practice'
import Layout from '@/components/Layout.vue'
import type { PracticeResult } from '@/types'

const practiceStore = usePracticeStore()

const userAnswer = ref('')
const lastResult = ref<PracticeResult | null>(null)

const currentWord = computed(() => practiceStore.getCurrentWord())

const playAudio = () => {
  if (currentWord.value?.word) {
    const utterance = new SpeechSynthesisUtterance(currentWord.value.word)
    utterance.lang = 'en-US'
    speechSynthesis.speak(utterance)
  }
}

const submitAnswer = async () => {
  if (!userAnswer.value.trim()) return

  const result = await practiceStore.submitAnswer(userAnswer.value.trim())
  if (result) {
    lastResult.value = result

    setTimeout(() => {
      lastResult.value = null
      userAnswer.value = ''
      practiceStore.nextWord()
    }, 2000)
  }
}

const startNewRound = () => {
  practiceStore.reset()
  practiceStore.fetchPracticeWords(10)
}

onMounted(() => {
  practiceStore.fetchPracticeWords(10)
})
</script>

<style scoped>
.practice-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.practice-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.word-display {
  text-align: center;
  padding: 40px 0;
}

.word-text {
  font-size: 36px;
  margin-bottom: 10px;
}

.phonetic {
  color: #666;
  font-size: 18px;
}

.answer-section {
  display: flex;
  justify-content: center;
  gap: 20px;
}
</style>