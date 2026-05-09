from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ReviewScheduleBase(BaseModel):
    item_type: str
    next_review_date: datetime
    review_count: int = 0
    ease_factor: float = Field(default=2.5, ge=1.3, le=5.0)
    interval_days: int = 0
    status: str = "learning"


class ReviewSubmit(BaseModel):
    item_type: str
    item_id: int
    score: int = Field(ge=0, le=5)  # User self-rating 0-5


class ReviewResult(BaseModel):
    next_review_date: datetime
    interval_days: int
    review_count: int
    status: str


class ReviewItemResponse(BaseModel):
    id: int
    item_type: str
    item_id: int
    word: Optional[str] = None  # Word text if item_type is 'word'
    sentence: Optional[str] = None  # Sentence text if item_type is 'sentence'
    meaning: Optional[str] = None
    review_count: int
    interval_days: int
    next_review_date: datetime
    status: str

    class Config:
        from_attributes = True


class TodayReviewResponse(BaseModel):
    due_count: int
    new_count: int
    review_items: List[ReviewItemResponse]


class ReviewStats(BaseModel):
    total_words: int
    total_sentences: int
    mastered_count: int
    learning_count: int
    review_count: int
    today_reviews: int
    tomorrow_reviews: int