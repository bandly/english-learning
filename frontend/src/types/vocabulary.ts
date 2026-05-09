export interface Word {
  id: number
  user_id: number
  word: string
  phonetic?: string
  meaning: string
  part_of_speech?: string
  example_sentence?: string
  audio_url?: string
  difficulty_level: number
  tags?: string[]
  created_at: string
  updated_at: string
}

export interface WordCreate {
  word: string
  phonetic?: string
  meaning: string
  part_of_speech?: string
  example_sentence?: string
  difficulty_level?: number
  tags?: string[]
}

export interface WordUpdate {
  word?: string
  phonetic?: string
  meaning?: string
  part_of_speech?: string
  example_sentence?: string
  difficulty_level?: number
  tags?: string[]
}

export interface WordListResponse {
  items: Word[]
  total: number
  skip: number
  limit: number
}

export interface WordBatchCreate {
  words: WordCreate[]
}