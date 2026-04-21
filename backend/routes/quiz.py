"""Quiz route'ları."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

XP_QUIZ_CORRECT = 5
XP_QUIZ_WRONG = 1


@router.post("/attempt")
def submit_quiz(
    payload: schemas.QuizSubmit,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = models.QuizAttempt(
        user_id=user.id,
        page_path=payload.page_path,
        quiz_id=payload.quiz_id,
        selected=payload.selected,
        is_correct=payload.is_correct,
    )
    db.add(attempt)
    streak = db.query(models.Streak).filter(models.Streak.user_id == user.id).first()
    if streak:
        streak.total_xp = (streak.total_xp or 0) + (XP_QUIZ_CORRECT if payload.is_correct else XP_QUIZ_WRONG)
    db.commit()
    return {"ok": True, "xp_awarded": XP_QUIZ_CORRECT if payload.is_correct else XP_QUIZ_WRONG}


@router.get("/stats/{page_path:path}", response_model=schemas.QuizStats)
def quiz_stats(
    page_path: str,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempts = db.query(models.QuizAttempt).filter(
        models.QuizAttempt.user_id == user.id,
        models.QuizAttempt.page_path == page_path,
    ).all()
    total = len(attempts)
    correct = sum(1 for a in attempts if a.is_correct)
    return schemas.QuizStats(
        page_path=page_path,
        total_attempts=total,
        correct_count=correct,
        accuracy=(correct / total) if total else 0.0,
    )
