from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WordBase(BaseModel):
    word: str
    phonetic: Optional[str] = None
    meaning: str
    part_of_speech: Optional[str] = None
    example_sentence: Optional[str] = None
    difficulty_level: Optional[int] = Field(default=1, ge=1, le=5)
    tags: Optional[List[str]] = None


class WordCreate(WordBase):
    pass


class WordUpdate(BaseModel):
    word: Optional[str] = None
    phonetic: Optional[str] = None
    meaning: Optional[str] = None
    part_of_speech: Optional[str] = None
    example_sentence: Optional[str] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    tags: Optional[List[str]] = None


class WordResponse(WordBase):
    id: int
    user_id: int
    audio_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WordBatchCreate(BaseModel):
    words: List[WordCreate]


class WordListResponse(BaseModel):
    items: List[WordResponse]
    total: int
    skip: int
    limit: int