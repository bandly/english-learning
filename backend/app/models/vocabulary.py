from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    word = Column(String(100), nullable=False, index=True)
    phonetic = Column(String(100), nullable=True)  # Phonetic notation
    meaning = Column(Text, nullable=False)  # Chinese meaning
    part_of_speech = Column(String(20), nullable=True)  # noun, verb, adj, etc.
    example_sentence = Column(Text, nullable=True)
    audio_url = Column(String(255), nullable=True)
    difficulty_level = Column(Integer, default=1)  # 1-5 difficulty
    tags = Column(JSON, nullable=True)  # Tags array
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="words")
    progress = relationship("WordProgress", back_populates="word", uselist=False, cascade="all, delete-orphan")
    review_schedules = relationship("ReviewSchedule", back_populates="word", cascade="all, delete-orphan")
    learning_records = relationship("LearningRecord", back_populates="word", cascade="all, delete-orphan")