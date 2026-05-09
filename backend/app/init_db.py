"""
Database initialization script
Run this script to create all tables
"""
import asyncio
from app.database import engine, Base
from app.models import User, Word, Sentence, LearningRecord, ReviewSchedule, WordProgress


async def init_db():
    """Create all tables"""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())