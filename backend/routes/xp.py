"""XP timeline route'lari — gunluk kirilim.

`xp_events` tablosu YOK. Veri kaynaklari:
  - QuizAttempt.attempted_at + is_correct → +5 veya +1
  - Progress.completed_at + status='completed' → +10
Streak daily ping XP'si (20/gun) burada YOKTUR — sadece Streak tablosunda cumulative.
Bu yuzden heatmap "aktivite XP"sini gosterir, toplam XP'den farkli olabilir.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import date, timedelta
from typing import List
from .. import models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/api/xp", tags=["xp"])

XP_QUIZ_CORRECT = 5
XP_QUIZ_WRONG = 1
XP_PAGE_COMPLETE = 10


@router.get("/daily", response_model=List[schemas.DailyXP])
def xp_daily(
    days: int = Query(7, ge=1, le=90),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Son N gun icin gunluk XP kirilimi. Bugun dahil, 0-XP gunler de donulur."""
    today = date.today()
    start = today - timedelta(days=days - 1)

    # Quiz XP: gun bazinda GROUP BY
    quiz_expr = func.sum(
        case((models.QuizAttempt.is_correct == True, XP_QUIZ_CORRECT), else_=XP_QUIZ_WRONG)
    )
    quiz_rows = (
        db.query(
            func.date(models.QuizAttempt.attempted_at).label("d"),
            quiz_expr.label("xp"),
            func.count(models.QuizAttempt.id).label("n"),
        )
        .filter(
            models.QuizAttempt.user_id == user.id,
            func.date(models.QuizAttempt.attempted_at) >= start,
        )
        .group_by("d")
        .all()
    )

    # Progress XP (completed sayfalar)
    prog_rows = (
        db.query(
            func.date(models.Progress.completed_at).label("d"),
            (func.count(models.Progress.id) * XP_PAGE_COMPLETE).label("xp"),
            func.count(models.Progress.id).label("n"),
        )
        .filter(
            models.Progress.user_id == user.id,
            models.Progress.status == "completed",
            func.date(models.Progress.completed_at) >= start,
        )
        .group_by("d")
        .all()
    )

    # Map'e at — tarih → (quiz_xp, quiz_n, prog_xp, prog_n)
    bucket = {}
    for r in quiz_rows:
        if r.d is None:
            continue
        d = r.d if isinstance(r.d, date) else date.fromisoformat(str(r.d))
        b = bucket.setdefault(d, {"quiz_xp": 0, "quiz_n": 0, "prog_xp": 0, "prog_n": 0})
        b["quiz_xp"] = int(r.xp or 0)
        b["quiz_n"] = int(r.n or 0)
    for r in prog_rows:
        if r.d is None:
            continue
        d = r.d if isinstance(r.d, date) else date.fromisoformat(str(r.d))
        b = bucket.setdefault(d, {"quiz_xp": 0, "quiz_n": 0, "prog_xp": 0, "prog_n": 0})
        b["prog_xp"] = int(r.xp or 0)
        b["prog_n"] = int(r.n or 0)

    # Ardisik N gun uretti, bos gunleri 0 ile doldur
    result = []
    for i in range(days):
        d = start + timedelta(days=i)
        b = bucket.get(d, {"quiz_xp": 0, "quiz_n": 0, "prog_xp": 0, "prog_n": 0})
        total = b["quiz_xp"] + b["prog_xp"]
        result.append(
            schemas.DailyXP(
                date=d,
                total_xp=total,
                quiz_xp=b["quiz_xp"],
                quiz_count=b["quiz_n"],
                pages_completed=b["prog_n"],
            )
        )
    return result
