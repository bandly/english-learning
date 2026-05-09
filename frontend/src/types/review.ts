export interface ReviewSubmit {
  item_type: string
  item_id: number
  score: number  // 0-5
}

export interface ReviewResult {
  next_review_date: string
  interval_days: number
  review_count: number
  status: string
}

export interface ReviewItem {
  id: number
  item_type: string
  item_id: number
  word?: string
  sentence?: string
  meaning?: string
  review_count: number
  interval_days: number
  next_review_date: string
  status: string
}

export interface TodayReviewResponse {
  due_count: number
  new_count: number
  review_items: ReviewItem[]
}

export interface ReviewStats {
  total_words: number
  total_sentences: number
  mastered_count: number
  learning_count: number
  review_count: number
  today_reviews: number
  tomorrow_reviews: number
}