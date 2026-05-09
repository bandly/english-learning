from sqlalchemy import Column, Integer, Text, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Sentence(Base):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sentence = Column(Text, nullable=False)
    translation = Column(Text, nullable=False)
    audio_url = Column(String(255), nullable=True)
    difficulty_level = Column(Integer, default=1)  # 1-5 difficulty
    tags = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="sentences")
    review_schedules = relationship("ReviewSchedule", back_populates="sentence", cascade="all, delete-orphan")
    learning_records = relationship("LearningRecord", back_populates="sentence", cascade="all, delete-orphan")