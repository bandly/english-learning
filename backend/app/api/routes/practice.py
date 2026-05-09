from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.vocabulary import Word
from app.models.sentence import Sentence
from app.models.learning_record import LearningRecord
from app.models.word_progress import WordProgress
from app.schemas.practice import PracticeSubmit, PracticeResult
from app.schemas.vocabulary import WordResponse
from app.api.dependencies import get_current_user
from datetime import datetime

router = APIRouter()


@router.get("/words", response_model=List[WordResponse])
async def get_practice_words(
    count: int = Query(default=10, ge=1, le=50),
    difficulty: Optional[int] = Query(default=None, ge=1, le=5),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get words for practice"""
    query = select(Word).where(Word.user_id == current_user.id)

    if difficulty:
        query = query.where(Word.difficulty_level == difficulty)

    query = query.limit(count).order_by(Word.created_at.desc())
    result = await db.execute(query)
    words = result.scalars().all()

    return [WordResponse.model_validate(w) for w in words]


@router.post("/listening", response_model=PracticeResult)
async def submit_listening_practice(
    practice_data: PracticeSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit listening practice result"""
    # Get the word/sentence
    if practice_data.item_type == "word":
        result = await db.execute(
            select(Word).where(
                Word.id == practice_data.item_id,
                Word.user_id == current_user.id
            )
        )
        item = result.scalar_one_or_none()
        correct_answer = item.word if item else None
    else:
        result = await db.execute(
            select(Sentence).where(
                Sentence.id == practice_data.item_id,
                Sentence.user_id == current_user.id
            )
        )
        item = result.scalar_one_or_none()
        correct_answer = item.sentence if item else None

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    # Check answer (case-insensitive)
    is_correct = practice_data.user_answer.strip().lower() == correct_answer.strip().lower()
    score = 100 if is_correct else 0

    # Create learning record
    record = LearningRecord(
        user_id=current_user.id,
        item_type=practice_data.item_type,
        word_id=practice_data.item_id if practice_data.item_type == "word" else None,
        sentence_id=practice_data.item_id if practice_data.item_type == "sentence" else None,
        practice_type="listening",
        score=score,
        is_correct=is_correct,
        time_spent=practice_data.time_spent
    )
    db.add(record)

    # Update word progress
    if practice_data.item_type == "word":
        progress_result = await db.execute(
            select(WordProgress).where(
                WordProgress.user_id == current_user.id,
                WordProgress.word_id == practice_data.item_id
            )
        )
        progress = progress_result.scalar_one_or_none()

        if not progress:
            progress = WordProgress(
                user_id=current_user.id,
                word_id=practice_data.item_id
            )
            db.add(progress)

        progress.total_practice_count += 1
        if is_correct:
            progress.correct_count += 1
            progress.listening_correct += 1
        progress.last_practice_at = datetime.utcnow()

    await db.commit()

    return PracticeResult(
        is_correct=is_correct,
        correct_answer=correct_answer,
        score=score,
        feedback="Great!" if is_correct else "Try again!"
    )


@router.post("/reading", response_model=PracticeResult)
async def submit_reading_practice(
    practice_data: PracticeSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit reading practice result (select meaning)"""
    if practice_data.item_type != "word":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reading practice only supports words"
        )

    result = await db.execute(
        select(Word).where(
            Word.id == practice_data.item_id,
            Word.user_id == current_user.id
        )
    )
    word = result.scalar_one_or_none()

    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )

    # Check meaning
    is_correct = practice_data.user_answer.strip() == word.meaning.strip()
    score = 100 if is_correct else 0

    # Create record
    record = LearningRecord(
        user_id=current_user.id,
        item_type="word",
        word_id=word.id,
        practice_type="reading",
        score=score,
        is_correct=is_correct,
        time_spent=practice_data.time_spent
    )
    db.add(record)

    # Update progress
    progress_result = await db.execute(
        select(WordProgress).where(
            WordProgress.user_id == current_user.id,
            WordProgress.word_id == word.id
        )
    )
    progress = progress_result.scalar_one_or_none()

    if not progress:
        progress = WordProgress(
            user_id=current_user.id,
            word_id=word.id
        )
        db.add(progress)

    progress.total_practice_count += 1
    if is_correct:
        progress.correct_count += 1
        progress.reading_correct += 1
    progress.last_practice_at = datetime.utcnow()

    await db.commit()

    return PracticeResult(
        is_correct=is_correct,
        correct_answer=word.meaning,
        score=score
    )


@router.post("/writing", response_model=PracticeResult)
async def submit_writing_practice(
    practice_data: PracticeSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit writing/spelling practice"""
    if practice_data.item_type == "word":
        result = await db.execute(
            select(Word).where(
                Word.id == practice_data.item_id,
                Word.user_id == current_user.id
            )
        )
        item = result.scalar_one_or_none()
        correct_answer = item.word if item else None
    else:
        result = await db.execute(
            select(Sentence).where(
                Sentence.id == practice_data.item_id,
                Sentence.user_id == current_user.id
            )
        )
        item = result.scalar_one_or_none()
        correct_answer = item.sentence if item else None

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    # Check spelling (case-insensitive)
    is_correct = practice_data.user_answer.strip().lower() == correct_answer.strip().lower()
    score = 100 if is_correct else 0

    # Create record
    record = LearningRecord(
        user_id=current_user.id,
        item_type=practice_data.item_type,
        word_id=practice_data.item_id if practice_data.item_type == "word" else None,
        sentence_id=practice_data.item_id if practice_data.item_type == "sentence" else None,
        practice_type="writing",
        score=score,
        is_correct=is_correct,
        time_spent=practice_data.time_spent
    )
    db.add(record)

    # Update progress
    if practice_data.item_type == "word":
        progress_result = await db.execute(
            select(WordProgress).where(
                WordProgress.user_id == current_user.id,
                WordProgress.word_id == practice_data.item_id
            )
        )
        progress = progress_result.scalar_one_or_none()

        if not progress:
            progress = WordProgress(
                user_id=current_user.id,
                word_id=practice_data.item_id
            )
            db.add(progress)

        progress.total_practice_count += 1
        if is_correct:
            progress.correct_count += 1
            progress.writing_correct += 1
        progress.last_practice_at = datetime.utcnow()

    await db.commit()

    return PracticeResult(
        is_correct=is_correct,
        correct_answer=correct_answer,
        score=score,
        feedback="Perfect spelling!" if is_correct else f"Correct spelling: {correct_answer}"
    )