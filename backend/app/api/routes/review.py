from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User
from app.models.vocabulary import Word
from app.models.sentence import Sentence
from app.models.review_schedule import ReviewSchedule
from app.schemas.review import ReviewSubmit, ReviewResult, ReviewItemResponse, TodayReviewResponse, ReviewStats
from app.api.dependencies import get_current_user
from app.services.review_algorithm import ReviewService

router = APIRouter()


@router.get("/today", response_model=TodayReviewResponse)
async def get_today_review(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get items due for review today"""
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)

    # Get review schedules due today
    result = await db.execute(
        select(ReviewSchedule).where(
            ReviewSchedule.user_id == current_user.id,
            ReviewSchedule.next_review_date <= tomorrow
        ).order_by(ReviewSchedule.next_review_date)
    )
    schedules = result.scalars().all()

    # Build review items
    review_items = []
    for schedule in schedules:
        if schedule.item_type == "word":
            word_result = await db.execute(
                select(Word).where(Word.id == schedule.word_id)
            )
            word = word_result.scalar_one_or_none()
            if word:
                review_items.append(ReviewItemResponse(
                    id=schedule.id,
                    item_type="word",
                    item_id=word.id,
                    word=word.word,
                    meaning=word.meaning,
                    review_count=schedule.review_count,
                    interval_days=schedule.interval_days,
                    next_review_date=schedule.next_review_date,
                    status=schedule.status
                ))
        elif schedule.item_type == "sentence":
            sentence_result = await db.execute(
                select(Sentence).where(Sentence.id == schedule.sentence_id)
            )
            sentence = sentence_result.scalar_one_or_none()
            if sentence:
                review_items.append(ReviewItemResponse(
                    id=schedule.id,
                    item_type="sentence",
                    item_id=sentence.id,
                    sentence=sentence.sentence,
                    meaning=sentence.translation,
                    review_count=schedule.review_count,
                    interval_days=schedule.interval_days,
                    next_review_date=schedule.next_review_date,
                    status=schedule.status
                ))

    # Count statistics
    due_count = len([s for s in schedules if s.next_review_date <= now])
    new_count = len([s for s in schedules if s.next_review_date > now and s.review_count == 0])

    return TodayReviewResponse(
        due_count=due_count,
        new_count=new_count,
        review_items=review_items
    )


@router.post("/submit", response_model=ReviewResult)
async def submit_review(
    review_data: ReviewSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit review result and update schedule"""
    # Get current schedule
    if review_data.item_type == "word":
        result = await db.execute(
            select(ReviewSchedule).where(
                ReviewSchedule.user_id == current_user.id,
                ReviewSchedule.word_id == review_data.item_id
            )
        )
    else:
        result = await db.execute(
            select(ReviewSchedule).where(
                ReviewSchedule.user_id == current_user.id,
                ReviewSchedule.sentence_id == review_data.item_id
            )
        )

    schedule = result.scalar_one_or_none()

    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review schedule not found"
        )

    # Update schedule using algorithm
    review_service = ReviewService()
    current_data = {
        "review_count": schedule.review_count,
        "ease_factor": float(schedule.ease_factor),
        "interval_days": schedule.interval_days
    }

    updated = review_service.update_schedule(current_data, review_data.score)

    # Apply updates
    schedule.next_review_date = updated["next_review_date"]
    schedule.interval_days = updated["interval_days"]
    schedule.review_count = updated["review_count"]
    schedule.ease_factor = updated["ease_factor"]
    schedule.status = updated["status"]
    schedule.last_review_date = updated["last_review_date"]

    await db.commit()

    return ReviewResult(
        next_review_date=schedule.next_review_date,
        interval_days=schedule.interval_days,
        review_count=schedule.review_count,
        status=schedule.status
    )


@router.get("/stats", response_model=ReviewStats)
async def get_review_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get review statistics"""
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    day_after = now + timedelta(days=2)

    # Count total words and sentences
    words_count = await db.execute(
        select(func.count()).select_from(Word).where(Word.user_id == current_user.id)
    )
    total_words = words_count.scalar() or 0

    sentences_count = await db.execute(
        select(func.count()).select_from(Sentence).where(Sentence.user_id == current_user.id)
    )
    total_sentences = sentences_count.scalar() or 0

    # Count by status
    mastered_count = await db.execute(
        select(func.count()).select_from(ReviewSchedule).where(
            ReviewSchedule.user_id == current_user.id,
            ReviewSchedule.status == "mastered"
        )
    )
    mastered = mastered_count.scalar() or 0

    learning_count = await db.execute(
        select(func.count()).select_from(ReviewSchedule).where(
            ReviewSchedule.user_id == current_user.id,
            ReviewSchedule.status == "learning"
        )
    )
    learning = learning_count.scalar() or 0

    review_count = await db.execute(
        select(func.count()).select_from(ReviewSchedule).where(
            ReviewSchedule.user_id == current_user.id,
            ReviewSchedule.status == "review"
        )
    )
    review = review_count.scalar() or 0

    # Count today and tomorrow reviews
    today_reviews = await db.execute(
        select(func.count()).select_from(ReviewSchedule).where(
            ReviewSchedule.user_id == current_user.id,
            ReviewSchedule.next_review_date <= tomorrow
        )
    )
    today = today_reviews.scalar() or 0

    tomorrow_reviews = await db.execute(
        select(func.count()).select_from(ReviewSchedule).where(
            ReviewSchedule.user_id == current_user.id,
            ReviewSchedule.next_review_date > tomorrow,
            ReviewSchedule.next_review_date <= day_after
        )
    )
    tomorrow_count = tomorrow_reviews.scalar() or 0

    return ReviewStats(
        total_words=total_words,
        total_sentences=total_sentences,
        mastered_count=mastered,
        learning_count=learning,
        review_count=review,
        today_reviews=today,
        tomorrow_reviews=tomorrow_count
    )