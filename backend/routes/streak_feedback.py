"""Streak ve feedback route'ları."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/api", tags=["streak", "feedback"])


@router.get("/streak", response_model=schemas.StreakOut)
def get_streak(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    streak = db.query(models.Streak).filter(models.Streak.user_id == user.id).first()
    if not streak:
        streak = models.Streak(user_id=user.id)
        db.add(streak)
        db.commit()
        db.refresh(streak)
    return streak


@router.post("/feedback", response_model=schemas.FeedbackOut)
def post_feedback(
    payload: schemas.FeedbackIn,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    fb = models.Feedback(
        user_id=user.id,
        page_path=payload.page_path,
        type=payload.type,
        message=payload.message,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


@router.get("/feedback", response_model=List[schemas.FeedbackOut])
def list_feedback(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(models.Feedback).filter(
        models.Feedback.user_id == user.id
    ).order_by(models.Feedback.created_at.desc()).all()
