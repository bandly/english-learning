from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.vocabulary import Word
from app.models.review_schedule import ReviewSchedule
from app.schemas.vocabulary import WordCreate, WordUpdate, WordResponse, WordBatchCreate, WordListResponse
from app.api.dependencies import get_current_user
from app.services.review_algorithm import ReviewService

router = APIRouter()


@router.post("/", response_model=WordResponse)
async def create_word(
    word_data: WordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new word"""
    # Check if word already exists for this user
    result = await db.execute(
        select(Word).where(
            Word.user_id == current_user.id,
            Word.word == word_data.word
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Word already exists"
        )

    # Create word
    new_word = Word(
        user_id=current_user.id,
        **word_data.model_dump()
    )
    db.add(new_word)
    await db.commit()
    await db.refresh(new_word)

    # Create initial review schedule
    review_service = ReviewService()
    schedule_data = review_service.create_initial_schedule(
        user_id=current_user.id,
        item_type="word"
    )

    review_schedule = ReviewSchedule(
        word_id=new_word.id,
        **schedule_data
    )
    db.add(review_schedule)
    await db.commit()

    return WordResponse.model_validate(new_word)


@router.get("/", response_model=WordListResponse)
async def get_words(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    tag: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's word list with pagination"""
    # Build query
    query = select(Word).where(Word.user_id == current_user.id)

    if tag:
        query = query.where(Word.tags.contains([tag]))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Get items with pagination
    query = query.offset(skip).limit(limit).order_by(Word.created_at.desc())
    result = await db.execute(query)
    words = result.scalars().all()

    return WordListResponse(
        items=[WordResponse.model_validate(w) for w in words],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{word_id}", response_model=WordResponse)
async def get_word(
    word_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single word"""
    result = await db.execute(
        select(Word).where(
            Word.id == word_id,
            Word.user_id == current_user.id
        )
    )
    word = result.scalar_one_or_none()

    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )

    return WordResponse.model_validate(word)


@router.put("/{word_id}", response_model=WordResponse)
async def update_word(
    word_id: int,
    word_data: WordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a word"""
    result = await db.execute(
        select(Word).where(
            Word.id == word_id,
            Word.user_id == current_user.id
        )
    )
    word = result.scalar_one_or_none()

    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )

    # Update fields
    for field, value in word_data.model_dump(exclude_unset=True).items():
        setattr(word, field, value)

    await db.commit()
    await db.refresh(word)

    return WordResponse.model_validate(word)


@router.delete("/{word_id}")
async def delete_word(
    word_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a word"""
    result = await db.execute(
        select(Word).where(
            Word.id == word_id,
            Word.user_id == current_user.id
        )
    )
    word = result.scalar_one_or_none()

    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )

    await db.delete(word)
    await db.commit()

    return {"message": "Word deleted successfully"}


@router.post("/batch", response_model=List[WordResponse])
async def batch_create_words(
    batch_data: WordBatchCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Batch create words"""
    created_words = []

    for word_data in batch_data.words:
        # Check if exists
        result = await db.execute(
            select(Word).where(
                Word.user_id == current_user.id,
                Word.word == word_data.word
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            continue  # Skip existing words

        # Create word
        new_word = Word(
            user_id=current_user.id,
            **word_data.model_dump()
        )
        db.add(new_word)
        await db.flush()  # Flush to get ID

        # Create review schedule
        review_service = ReviewService()
        schedule_data = review_service.create_initial_schedule(
            user_id=current_user.id,
            item_type="word"
        )

        review_schedule = ReviewSchedule(
            word_id=new_word.id,
            **schedule_data
        )
        db.add(review_schedule)

        created_words.append(new_word)

    await db.commit()

    return [WordResponse.model_validate(w) for w in created_words]