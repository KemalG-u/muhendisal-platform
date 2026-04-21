"""SQLAlchemy modelleri — users, progress, quiz_attempts, streaks, feedback."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False, index=True)
    nick = Column(String, default="Kemal")
    target = Column(String, default="hepsi")  # "hbv" | "kisisel" | "is" | "hepsi"
    created_at = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, server_default=func.now(), onupdate=func.now())

    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    streak = relationship("Streak", back_populates="user", uselist=False, cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")


class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    page_path = Column(String, nullable=False, index=True)  # "bolum-4/02-chunking"
    status = Column(String, default="started")  # started | completed
    seen_count = Column(Integer, default=1)
    time_spent_sec = Column(Integer, default=0)
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="progress")
    __table_args__ = (UniqueConstraint("user_id", "page_path", name="uq_user_page"),)


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    page_path = Column(String, nullable=False, index=True)
    quiz_id = Column(String, nullable=False)
    selected = Column(String)
    is_correct = Column(Boolean, nullable=False)
    attempted_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="quiz_attempts")


class Streak(Base):
    __tablename__ = "streaks"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_active_date = Column(Date, nullable=True)
    total_xp = Column(Integer, default=0)

    user = relationship("User", back_populates="streak")


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    page_path = Column(String, nullable=True)
    type = Column(String, default="note")  # question | bug | suggestion | note
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="feedback")
