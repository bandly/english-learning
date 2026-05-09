import apiClient from './client'
import type { User, UserCreate, UserLogin, Token } from '@/types/user'

export const userApi = {
  // Register
  async register(data: UserCreate): Promise<Token> {
    return apiClient.post('/auth/register', data)
  },

  // Login
  async login(data: UserLogin): Promise<Token> {
    return apiClient.post('/auth/login', data)
  },

  // Get current user
  async getCurrentUser(): Promise<User> {
    return apiClient.get('/auth/me')
  }
}