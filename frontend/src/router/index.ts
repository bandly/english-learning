import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/vocabulary'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/vocabulary',
    name: 'Vocabulary',
    component: () => import('@/views/VocabularyView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('@/views/PracticeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/review',
    name: 'Review',
    component: () => import('@/views/ReviewView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/vocabulary')
  } else {
    next()
  }
})

export default router