from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class WordProgress(Base):
    __tablename__ = "word_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    mastery_level = Column(Integer, default=0)  # 0-100 mastery level
    total_practice_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    listening_correct = Column(Integer, default=0)
    speaking_correct = Column(Integer, default=0)
    reading_correct = Column(Integer, default=0)
    writing_correct = Column(Integer, default=0)
    last_practice_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="word_progress")
    word = relationship("Word", back_populates="progress")

    # Unique constraint per user per word
    __table_args__ = (
        Index('idx_user_word_unique', 'user_id', 'word_id', unique=True),
    )