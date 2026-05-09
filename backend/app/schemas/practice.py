from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LearningRecordBase(BaseModel):
    item_type: str  # 'word' or 'sentence'
    practice_type: str  # 'listening', 'speaking', 'reading', 'writing'
    score: Optional[int] = None
    is_correct: Optional[bool] = None
    time_spent: Optional[int] = None


class LearningRecordCreate(LearningRecordBase):
    item_id: int  # word_id or sentence_id


class LearningRecordResponse(LearningRecordBase):
    id: int
    user_id: int
    word_id: Optional[int] = None
    sentence_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PracticeSubmit(BaseModel):
    item_type: str
    item_id: int
    user_answer: str
    time_spent: Optional[int] = None


class PracticeResult(BaseModel):
    is_correct: bool
    correct_answer: str
    score: int
    feedback: Optional[str] = None