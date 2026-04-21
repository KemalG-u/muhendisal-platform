"""Auth/User route'ları."""
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from typing import Optional
from .. import models, schemas
from ..database import get_db
from ..rate_limit import limiter

router = APIRouter(prefix="/api", tags=["auth"])


def get_current_user(
    x_token: Optional[str] = Header(None, alias="X-Token"),
    db: Session = Depends(get_db),
) -> models.User:
    """Header'dan token oku, kullanıcıyı bul. Yoksa 401."""
    if not x_token:
        raise HTTPException(401, "X-Token header eksik")
    user = db.query(models.User).filter(models.User.token == x_token).first()
    if not user:
        raise HTTPException(401, "Geçersiz token, /api/auth/init ile yeni kayıt aç")
    return user


@router.post("/auth/init", response_model=schemas.UserOut)
@limiter.limit("5/minute")
def init_user(
    request: Request,
    payload: schemas.UserInit,
    db: Session = Depends(get_db),
):
    """Cihaz UUID ile ilk kayıt. Token zaten varsa user'ı döner (idempotent)."""
    user = db.query(models.User).filter(models.User.token == payload.token).first()
    if user:
        return user
    user = models.User(token=payload.token, nick=payload.nick or "Kemal")
    db.add(user)
    db.flush()
    streak = models.Streak(user_id=user.id)
    db.add(streak)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=schemas.UserOut)
def get_me(user: models.User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=schemas.UserOut)
@limiter.limit("10/minute")
def update_me(
    request: Request,
    payload: schemas.UserUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.nick is not None:
        user.nick = payload.nick
    if payload.target is not None:
        user.target = payload.target
    db.commit()
    db.refresh(user)
    return user
