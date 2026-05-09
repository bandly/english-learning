export interface User {
  id: number
  username: string
  created_at: string
  last_login_at?: string
  settings?: Record<string, unknown>
}

export interface UserCreate {
  username: string
  password?: string
}

export interface UserLogin {
  username: string
  password?: string
}

export interface Token {
  access_token: string
  token_type: string
  user: User
}