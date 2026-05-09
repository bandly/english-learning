from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class LearningRecord(Base):
    __tablename__ = "learning_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_type = Column(String(20), nullable=False)  # 'word' or 'sentence'
    practice_type = Column(String(20), nullable=False)  # 'listening', 'speaking', 'reading', 'writing'
    score = Column(Integer, nullable=True)  # 0-100 score
    is_correct = Column(Boolean, nullable=True)
    time_spent = Column(Integer, nullable=True)  # Time spent in seconds
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships - using foreign_keys to specify which FK to use
    user = relationship("User", back_populates="learning_records")
    word = relationship(
        "Word",
        foreign_keys="LearningRecord.word_id",
        back_populates="learning_records"
    )
    sentence = relationship(
        "Sentence",
        foreign_keys="LearningRecord.sentence_id",
        back_populates="learning_records"
    )

    # Foreign keys (conditional based on item_type)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=True)
    sentence_id = Column(Integer, ForeignKey("sentences.id", ondelete="CASCADE"), nullable=True)

    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_user_item_type', 'user_id', 'item_type'),
    )