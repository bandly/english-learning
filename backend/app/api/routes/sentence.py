from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.sentence import Sentence
from app.models.review_schedule import ReviewSchedule
from app.schemas.sentence import SentenceCreate, SentenceUpdate, SentenceResponse, SentenceListResponse
from app.api.dependencies import get_current_user
from app.services.review_algorithm import ReviewService

router = APIRouter()


@router.post("/", response_model=SentenceResponse)
async def create_sentence(
    sentence_data: SentenceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new sentence"""
    new_sentence = Sentence(
        user_id=current_user.id,
        **sentence_data.model_dump()
    )
    db.add(new_sentence)
    await db.commit()
    await db.refresh(new_sentence)

    # Create initial review schedule
    review_service = ReviewService()
    schedule_data = review_service.create_initial_schedule(
        user_id=current_user.id,
        item_type="sentence"
    )

    review_schedule = ReviewSchedule(
        sentence_id=new_sentence.id,
        **schedule_data
    )
    db.add(review_schedule)
    await db.commit()

    return SentenceResponse.model_validate(new_sentence)


@router.get("/", response_model=SentenceListResponse)
async def get_sentences(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's sentence list"""
    # Get total count
    count_query = select(func.count()).select_from(Sentence).where(
        Sentence.user_id == current_user.id
    )
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Get items
    query = select(Sentence).where(
        Sentence.user_id == current_user.id
    ).offset(skip).limit(limit).order_by(Sentence.created_at.desc())

    result = await db.execute(query)
    sentences = result.scalars().all()

    return SentenceListResponse(
        items=[SentenceResponse.model_validate(s) for s in sentences],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{sentence_id}", response_model=SentenceResponse)
async def get_sentence(
    sentence_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single sentence"""
    result = await db.execute(
        select(Sentence).where(
            Sentence.id == sentence_id,
            Sentence.user_id == current_user.id
        )
    )
    sentence = result.scalar_one_or_none()

    if not sentence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sentence not found"
        )

    return SentenceResponse.model_validate(sentence)


@router.put("/{sentence_id}", response_model=SentenceResponse)
async def update_sentence(
    sentence_id: int,
    sentence_data: SentenceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a sentence"""
    result = await db.execute(
        select(Sentence).where(
            Sentence.id == sentence_id,
            Sentence.user_id == current_user.id
        )
    )
    sentence = result.scalar_one_or_none()

    if not sentence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sentence not found"
        )

    for field, value in sentence_data.model_dump(exclude_unset=True).items():
        setattr(sentence, field, value)

    await db.commit()
    await db.refresh(sentence)

    return SentenceResponse.model_validate(sentence)


@router.delete("/{sentence_id}")
async def delete_sentence(
    sentence_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a sentence"""
    result = await db.execute(
        select(Sentence).where(
            Sentence.id == sentence_id,
            Sentence.user_id == current_user.id
        )
    )
    sentence = result.scalar_one_or_none()

    if not sentence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sentence not found"
        )

    await db.delete(sentence)
    await db.commit()

    return {"message": "Sentence deleted successfully"}