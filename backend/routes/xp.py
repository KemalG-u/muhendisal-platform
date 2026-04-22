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



def _iso_week_start(d: date) -> date:
    """Verilen tarihin ait oldugu ISO haftasinin Pazartesi'sini dondur."""
    return d - timedelta(days=d.weekday())


@router.get("/weekly", response_model=List[schemas.WeeklyXP])
def xp_weekly(
    weeks: int = Query(8, ge=1, le=52),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Son N hafta icin haftalik XP kirilimi (Pazartesi-Pazar bucketlari).
    Bos haftalar 0-XP ile doldurulur.
    """
    today = date.today()
    current_week_start = _iso_week_start(today)
    start = current_week_start - timedelta(weeks=weeks - 1)

    # Quiz XP — gun bazinda cek, haftaya grupla (SQLite'ta strftime('%W') yerine Python'da bucket)
    quiz_rows = (
        db.query(
            func.date(models.QuizAttempt.attempted_at).label("d"),
            models.QuizAttempt.is_correct.label("c"),
        )
        .filter(
            models.QuizAttempt.user_id == user.id,
            func.date(models.QuizAttempt.attempted_at) >= start,
        )
        .all()
    )

    prog_rows = (
        db.query(func.date(models.Progress.completed_at).label("d"))
        .filter(
            models.Progress.user_id == user.id,
            models.Progress.status == "completed",
            func.date(models.Progress.completed_at) >= start,
        )
        .all()
    )

    # Hafta bucketlari
    bucket = {}
    for i in range(weeks):
        ws = start + timedelta(weeks=i)
        bucket[ws] = {"quiz_xp": 0, "quiz_n": 0, "prog_n": 0}

    for r in quiz_rows:
        if r.d is None:
            continue
        d = r.d if isinstance(r.d, date) else date.fromisoformat(str(r.d))
        ws = _iso_week_start(d)
        if ws in bucket:
            bucket[ws]["quiz_xp"] += XP_QUIZ_CORRECT if r.c else XP_QUIZ_WRONG
            bucket[ws]["quiz_n"] += 1

    for r in prog_rows:
        if r.d is None:
            continue
        d = r.d if isinstance(r.d, date) else date.fromisoformat(str(r.d))
        ws = _iso_week_start(d)
        if ws in bucket:
            bucket[ws]["prog_n"] += 1

    result = []
    for ws in sorted(bucket.keys()):
        b = bucket[ws]
        prog_xp = b["prog_n"] * XP_PAGE_COMPLETE
        result.append(
            schemas.WeeklyXP(
                week_start=ws,
                total_xp=b["quiz_xp"] + prog_xp,
                quiz_xp=b["quiz_xp"],
                quiz_count=b["quiz_n"],
                pages_completed=b["prog_n"],
            )
        )
    return result


@router.get("/me/total", response_model=schemas.XPTotal)
def xp_me_total(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Kullanicinin tum-zamanlar toplam XP'si + breakdown.

    `total_xp` kanonik kaynaktir (Streak.total_xp — streak_feedback.py tarafindan
    quiz/progress/streak_ping olaylarinda guncellenir). Breakdown alanlari tablolardan
    ayri hesaplanir, ters guvenlik (sanity cross-check) icin kullanilabilir.
    """
    streak = db.query(models.Streak).filter(models.Streak.user_id == user.id).one_or_none()

    quiz_agg = (
        db.query(
            func.sum(case((models.QuizAttempt.is_correct == True, XP_QUIZ_CORRECT), else_=XP_QUIZ_WRONG)).label("xp"),
            func.count(models.QuizAttempt.id).label("n"),
        )
        .filter(models.QuizAttempt.user_id == user.id)
        .one()
    )

    prog_n = (
        db.query(func.count(models.Progress.id))
        .filter(models.Progress.user_id == user.id, models.Progress.status == "completed")
        .scalar()
    ) or 0

    return schemas.XPTotal(
        total_xp=int(streak.total_xp) if streak else 0,
        quiz_xp_all_time=int(quiz_agg.xp or 0),
        quiz_count_all_time=int(quiz_agg.n or 0),
        pages_completed_all_time=int(prog_n),
        current_streak=int(streak.current_streak) if streak else 0,
        longest_streak=int(streak.longest_streak) if streak else 0,
    )
