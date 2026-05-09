<template>
  <div class="main-layout">
    <el-container>
      <!-- Header -->
      <el-header class="header">
        <div class="logo">英语学习</div>
        <el-menu mode="horizontal" :default-active="activeIndex" router>
          <el-menu-item index="/vocabulary">
            <el-icon><Notebook /></el-icon>
            词汇管理
          </el-menu-item>
          <el-menu-item index="/practice">
            <el-icon><EditPen /></el-icon>
            练习中心
          </el-menu-item>
          <el-menu-item index="/review">
            <el-icon><Calendar /></el-icon>
            复习中心
          </el-menu-item>
        </el-menu>
        <div class="user-info">
          <span>{{ userStore.user?.username }}</span>
          <el-button type="text" @click="handleLogout">退出</el-button>
        </div>
      </el-header>

      <!-- Main Content -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeIndex = computed(() => route.path)

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  margin-right: 40px;
}

.el-menu {
  border-bottom: none;
  flex: 1;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.main-content {
  background: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>