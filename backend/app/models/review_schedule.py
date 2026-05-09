from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, DECIMAL, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ReviewSchedule(Base):
    __tablename__ = "review_schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(20), nullable=False)  # 'word' or 'sentence'
    next_review_date = Column(TIMESTAMP, nullable=False, index=True)
    review_count = Column(Integer, default=0)
    ease_factor = Column(DECIMAL(3, 2), default=2.5)  # SM-2 algorithm ease factor
    interval_days = Column(Integer, default=0)  # Current interval in days
    last_review_date = Column(TIMESTAMP, nullable=True)
    status = Column(String(20), default="learning")  # 'learning', 'review', 'mastered'
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Foreign keys
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=True)
    sentence_id = Column(Integer, ForeignKey("sentences.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="review_schedules")
    word = relationship("Word", back_populates="review_schedules")
    sentence = relationship("Sentence", back_populates="review_schedules")

    # Composite indexes
    __table_args__ = (
        Index('idx_user_next_review', 'user_id', 'next_review_date'),
        Index('idx_user_item', 'user_id', 'item_type', 'word_id', 'sentence_id'),
    )