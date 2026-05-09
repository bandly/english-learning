export interface PracticeSubmit {
  item_type: string
  item_id: number
  user_answer: string
  time_spent?: number
}

export interface PracticeResult {
  is_correct: boolean
  correct_answer: string
  score: number
  feedback?: string
}

export interface Sentence {
  id: number
  user_id: number
  sentence: string
  translation: string
  audio_url?: string
  difficulty_level: number
  tags?: string[]
  created_at: string
  updated_at: string
}