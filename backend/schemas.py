"""Pydantic schemalar — request/response."""
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, Literal


# ===== User =====

class UserInit(BaseModel):
    """İlk açılışta cihazdan gelen UUID."""
    token: str = Field(..., min_length=8, max_length=128)
    nick: Optional[str] = "Kemal"


class UserUpdate(BaseModel):
    nick: Optional[str] = None
    target: Optional[Literal["hbv", "kisisel", "is", "hepsi"]] = None


class UserOut(BaseModel):
    id: int
    token: str
    nick: str
    target: str
    created_at: datetime
    last_seen: datetime

    class Config:
        from_attributes = True


# ===== Progress =====

class ProgressEvent(BaseModel):
    page_path: str = Field(..., min_length=1, max_length=200)


class ProgressOut(BaseModel):
    page_path: str
    status: str
    seen_count: int
    time_spent_sec: int
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


# ===== Quiz =====

class QuizSubmit(BaseModel):
    page_path: str
    quiz_id: str
    selected: str
    is_correct: bool


class QuizStats(BaseModel):
    page_path: str
    total_attempts: int
    correct_count: int
    accuracy: float


# ===== Streak =====

class StreakOut(BaseModel):
    current_streak: int
    longest_streak: int
    last_active_date: Optional[date]
    total_xp: int

    class Config:
        from_attributes = True


# ===== Feedback =====

class FeedbackIn(BaseModel):
    page_path: Optional[str] = None
    type: Literal["question", "bug", "suggestion", "note"] = "note"
    message: str = Field(..., min_length=1, max_length=5000)


class FeedbackOut(BaseModel):
    id: int
    page_path: Optional[str]
    type: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
