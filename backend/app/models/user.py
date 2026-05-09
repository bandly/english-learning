from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)  # Optional password
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    last_login_at = Column(TIMESTAMP, nullable=True)
    settings = Column(JSON, nullable=True)  # User settings (daily goal, etc.)

    # Relationships
    words = relationship("Word", back_populates="user", cascade="all, delete-orphan")
    sentences = relationship("Sentence", back_populates="user", cascade="all, delete-orphan")
    learning_records = relationship("LearningRecord", back_populates="user", cascade="all, delete-orphan")
    review_schedules = relationship("ReviewSchedule", back_populates="user", cascade="all, delete-orphan")
    word_progress = relationship("WordProgress", back_populates="user", cascade="all, delete-orphan")