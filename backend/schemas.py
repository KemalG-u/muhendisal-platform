"""Pydantic schemalar — request/response."""
import re
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional, Literal


# ===== Güvenlik yardımcıları =====

# HTML tag'leri ve tehlikeli şemaları reddet — XSS server-side savunması.
# Frontend bu veriyi textContent ile basmalı; bu katman ikinci savunma hattı.
_HTML_TAG_RE = re.compile(r"<\s*/?\s*([a-zA-Z][a-zA-Z0-9]*)", re.IGNORECASE)
_DANGEROUS_SCHEMES_RE = re.compile(r"(javascript|data|vbscript)\s*:", re.IGNORECASE)
_BLOCKED_TAGS = {"script", "iframe", "object", "embed", "svg", "img", "link",
                 "style", "meta", "base", "form", "input", "button", "video",
                 "audio", "source", "track", "frame", "frameset", "applet"}


def _strip_dangerous_html(value: str) -> str:
    """Tehlikeli HTML etiketlerini ve şemaları reddet.

    Yasak etiket bulursa ValueError — kullanıcıya validation hatası döner.
    Masum HTML-benzeri metin (ör. '3 < 5') geçer; sadece yapısal etiketler
    ve javascript: benzeri şemalar engellenir.
    """
    for match in _HTML_TAG_RE.finditer(value):
        tag = match.group(1).lower()
        if tag in _BLOCKED_TAGS:
            raise ValueError(f"HTML etiketi yasak: <{tag}>")
    if _DANGEROUS_SCHEMES_RE.search(value):
        raise ValueError("javascript: / data: / vbscript: şeması yasak")
    return value


# ===== User =====

class UserInit(BaseModel):
    """İlk açılışta cihazdan gelen UUID."""
    token: str = Field(..., min_length=8, max_length=128)
    nick: Optional[str] = "Kemal"

    @field_validator("nick")
    @classmethod
    def _clean_nick(cls, v):
        if v is None:
            return v
        if len(v) > 64:
            raise ValueError("nick 64 karakterden uzun olamaz")
        return _strip_dangerous_html(v)


class UserUpdate(BaseModel):
    nick: Optional[str] = Field(None, max_length=64)
    target: Optional[Literal["hbv", "kisisel", "is", "hepsi", "baslangic"]] = None

    @field_validator("nick")
    @classmethod
    def _clean_nick(cls, v):
        return _strip_dangerous_html(v) if v else v


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

    @field_validator("page_path")
    @classmethod
    def _clean_path(cls, v):
        # Sayfa yolu sade ASCII + - _ / . olmalı; path traversal engelle
        if ".." in v or v.startswith("/"):
            raise ValueError("page_path geçersiz")
        if not re.match(r"^[a-zA-Z0-9\-_./]+$", v):
            raise ValueError("page_path sadece a-z, 0-9, - _ / . içerebilir")
        return v


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
    page_path: str = Field(..., max_length=200)
    quiz_id: str = Field(..., max_length=80)
    selected: str = Field(..., max_length=500)
    is_correct: bool

    @field_validator("page_path", "quiz_id")
    @classmethod
    def _clean_id(cls, v):
        return _strip_dangerous_html(v)

    @field_validator("selected")
    @classmethod
    def _clean_selected(cls, v):
        return _strip_dangerous_html(v)


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
    page_path: Optional[str] = Field(None, max_length=200)
    type: Literal["question", "bug", "suggestion", "note", "proje_teslim"] = "note"
    message: str = Field(..., min_length=1, max_length=5000)

    @field_validator("message")
    @classmethod
    def _clean_message(cls, v):
        return _strip_dangerous_html(v)

    @field_validator("page_path")
    @classmethod
    def _clean_path(cls, v):
        if v is None:
            return v
        return _strip_dangerous_html(v)


class FeedbackOut(BaseModel):
    id: int
    page_path: Optional[str]
    type: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


# ===== Quiz attempt (son denemeler listesi) =====

class QuizAttemptOut(BaseModel):
    id: int
    page_path: str
    quiz_id: str
    selected: Optional[str]
    is_correct: bool
    attempted_at: datetime

    class Config:
        from_attributes = True


# ===== XP timeline (F10) =====

class DailyXP(BaseModel):
    date: date
    total_xp: int
    quiz_xp: int
    quiz_count: int
    pages_completed: int
