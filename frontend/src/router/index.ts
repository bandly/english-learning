import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/vocabulary'
  },
  {
    path: '/vocabulary',
    name: 'Vocabulary',
    component: () => import('@/views/VocabularyView.vue')
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('@/views/PracticeView.vue')
  },
  {
    path: '/review',
    name: 'Review',
    component: () => import('@/views/ReviewView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router