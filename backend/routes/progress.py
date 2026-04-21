"""Progress route'ları — sayfa görüldü/tamamlandı + XP."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List
from .. import models, schemas
from ..database import get_db
from ..rate_limit import limiter
from .auth import get_current_user

router = APIRouter(prefix="/api/progress", tags=["progress"])

XP_PAGE_COMPLETE = 10
XP_DAILY_PING = 20
XP_STREAK_7 = 100
XP_STREAK_30 = 500


def _add_xp(db: Session, user_id: int, amount: int):
    """Streak tablosunda total_xp'i artır."""
    streak = db.query(models.Streak).filter(models.Streak.user_id == user_id).first()
    if streak:
        streak.total_xp = (streak.total_xp or 0) + amount


def _update_streak(db: Session, user_id: int):
    """Günlük yoklama: streak'i artır veya sıfırla."""
    streak = db.query(models.Streak).filter(models.Streak.user_id == user_id).first()
    if not streak:
        streak = models.Streak(user_id=user_id)
        db.add(streak)
    today = date.today()
    if streak.last_active_date == today:
        return  # bugün zaten geldi
    if streak.last_active_date and (today - streak.last_active_date).days == 1:
        # Dün de geldi, streak devam
        streak.current_streak = (streak.current_streak or 0) + 1
        bonus = XP_DAILY_PING
        if streak.current_streak == 7:
            bonus += XP_STREAK_7
        elif streak.current_streak == 30:
            bonus += XP_STREAK_30
        streak.total_xp = (streak.total_xp or 0) + bonus
    else:
        # Atlama oldu, streak sıfırla
        streak.current_streak = 1
        streak.total_xp = (streak.total_xp or 0) + XP_DAILY_PING
    streak.last_active_date = today
    if streak.current_streak > (streak.longest_streak or 0):
        streak.longest_streak = streak.current_streak


@router.post("/seen")
@limiter.limit("60/minute")
def mark_seen(
    request: Request,
    payload: schemas.ProgressEvent,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sayfa açıldı, ilk kez görüldüyse kayda al, tekrarsa seen_count++."""
    p = db.query(models.Progress).filter(
        models.Progress.user_id == user.id,
        models.Progress.page_path == payload.page_path,
    ).first()
    if p:
        p.seen_count = (p.seen_count or 1) + 1
    else:
        p = models.Progress(user_id=user.id, page_path=payload.page_path)
        db.add(p)
    _update_streak(db, user.id)
    db.commit()
    return {"ok": True}


@router.post("/complete")
@limiter.limit("30/minute")
def mark_complete(
    request: Request,
    payload: schemas.ProgressEvent,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sayfa tamamlandı, +XP. Idempotent."""
    p = db.query(models.Progress).filter(
        models.Progress.user_id == user.id,
        models.Progress.page_path == payload.page_path,
    ).first()
    if not p:
        p = models.Progress(user_id=user.id, page_path=payload.page_path)
        db.add(p)
    awarded = False
    if p.status != "completed":
        p.status = "completed"
        p.completed_at = datetime.utcnow()
        _add_xp(db, user.id, XP_PAGE_COMPLETE)
        awarded = True
    _update_streak(db, user.id)
    db.commit()
    return {"ok": True, "xp_awarded": XP_PAGE_COMPLETE if awarded else 0}


@router.get("", response_model=List[schemas.ProgressOut])
def list_progress(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(models.Progress).filter(models.Progress.user_id == user.id).all()
