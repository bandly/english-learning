import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api/user'
import type { User, UserCreate, UserLogin, Token } from '@/types/user'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)

  const isLoggedIn = computed(() => !!token.value && !!user.value)

  // Login
  async function login(data: UserLogin) {
    loading.value = true
    try {
      const result: Token = await userApi.login(data)
      token.value = result.access_token
      user.value = result.user
      localStorage.setItem('token', result.access_token)
      localStorage.setItem('user', JSON.stringify(result.user))
      ElMessage.success('登录成功')
      return true
    } catch (error) {
      return false
    } finally {
      loading.value = false
    }
  }

  // Register
  async function register(data: UserCreate) {
    loading.value = true
    try {
      const result: Token = await userApi.register(data)
      token.value = result.access_token
      user.value = result.user
      localStorage.setItem('token', result.access_token)
      localStorage.setItem('user', JSON.stringify(result.user))
      ElMessage.success('注册成功')
      return true
    } catch (error) {
      return false
    } finally {
      loading.value = false
    }
  }

  // Get current user
  async function fetchCurrentUser() {
    if (!token.value) return
    loading.value = true
    try {
      user.value = await userApi.getCurrentUser()
    } catch (error) {
      logout()
    } finally {
      loading.value = false
    }
  }

  // Logout
  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // Initialize from localStorage
  function init() {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = JSON.parse(savedUser)
    }
    if (token.value) {
      fetchCurrentUser()
    }
  }

  return {
    user,
    token,
    loading,
    isLoggedIn,
    login,
    register,
    fetchCurrentUser,
    logout,
    init
  }
})