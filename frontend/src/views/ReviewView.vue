<template>
  <Layout>
    <div class="review-page">
      <div class="page-header">
        <h2>复习中心</h2>
        <div class="stats-overview">
          <el-statistic title="今日待复习" :value="reviewStore.dueToday" />
          <el-statistic title="已掌握" :value="reviewStore.masteredCount" />
          <el-statistic title="学习中" :value="reviewStore.stats?.learning_count || 0" />
        </div>
      </div>

      <!-- Review List -->
      <div class="card-container">
        <el-table :data="reviewStore.todayItems" v-loading="reviewStore.loading" stripe>
          <el-table-column prop="word" label="单词" width="150">
            <template #default="{ row }">
              {{ row.word || row.sentence }}
            </template>
          </el-table-column>
          <el-table-column prop="meaning" label="含义" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'mastered' ? 'success' : row.status === 'review' ? 'warning' : 'info'">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="review_count" label="复习次数" width="100" />
          <el-table-column label="评分" width="300">
            <template #default="{ row }">
              <el-rate
                v-model="row.tempScore"
                :max="5"
                show-text
                :texts="['完全忘记', '记得一点', '有些犹豫', '比较轻松', '很清楚', '完美']"
              />
              <el-button
                size="small"
                type="primary"
                @click="submitReview(row)"
                :disabled="row.tempScore === undefined"
                style="margin-left: 10px;"
              >
                提交
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-empty v-if="reviewStore.todayItems.length === 0" description="今日暂无复习内容" />
      </div>

      <!-- Stats Chart Placeholder -->
      <div class="card-container stats-chart">
        <h3>学习统计</h3>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card shadow="hover">
              <el-statistic title="总词汇量" :value="reviewStore.stats?.total_words || 0" />
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <el-statistic title="已掌握" :value="reviewStore.stats?.mastered_count || 0" />
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <el-statistic title="明日复习" :value="reviewStore.stats?.tomorrow_reviews || 0" />
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card shadow="hover">
              <el-statistic title="学习中" :value="reviewStore.stats?.learning_count || 0" />
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useReviewStore } from '@/stores/review'
import { ElMessage } from 'element-plus'
import Layout from '@/components/Layout.vue'

const reviewStore = useReviewStore()

const submitReview = async (item: any) => {
  if (item.tempScore === undefined) return

  await reviewStore.submitReview(item.item_type, item.item_id, item.tempScore)
  ElMessage.success('复习已提交')
}

onMounted(() => {
  reviewStore.fetchTodayReview()
  reviewStore.fetchStats()
})
</script>

<style scoped>
.review-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.stats-overview {
  display: flex;
  gap: 40px;
}

.stats-chart {
  margin-top: 20px;
}

.stats-chart h3 {
  margin: 0 0 20px 0;
}

.el-card {
  text-align: center;
}
</style>