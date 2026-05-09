from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SentenceBase(BaseModel):
    sentence: str
    translation: str
    difficulty_level: Optional[int] = Field(default=1, ge=1, le=5)
    tags: Optional[List[str]] = None


class SentenceCreate(SentenceBase):
    pass


class SentenceUpdate(BaseModel):
    sentence: Optional[str] = None
    translation: Optional[str] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    tags: Optional[List[str]] = None


class SentenceResponse(SentenceBase):
    id: int
    user_id: int
    audio_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SentenceListResponse(BaseModel):
    items: List[SentenceResponse]
    total: int
    skip: int
    limit: int