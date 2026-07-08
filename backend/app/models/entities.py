from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)


class Resume(Base, TimestampMixin):
    __tablename__ = 'resumes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    resume_text: Mapped[str] = mapped_column(Text)
    overall_score: Mapped[int | None]
    ats_score: Mapped[int | None]


class ATSReport(Base, TimestampMixin):
    __tablename__ = 'ats_reports'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    resume_text: Mapped[str] = mapped_column(Text)
    job_description: Mapped[str] = mapped_column(Text)
    match_percent: Mapped[int]


class CoverLetter(Base, TimestampMixin):
    __tablename__ = 'cover_letters'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    company: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(150))
    tone: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)


class Interview(Base, TimestampMixin):
    __tablename__ = 'interviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    company: Mapped[str] = mapped_column(String(150))
    round_type: Mapped[str] = mapped_column(String(50))
    questions: Mapped[str] = mapped_column(Text)


class InterviewEvaluation(Base, TimestampMixin):
    __tablename__ = 'interview_evaluations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    overall_score: Mapped[float] = mapped_column(Float)


class JobApplication(Base, TimestampMixin):
    __tablename__ = 'job_applications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    company: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(50), default='Wishlist', index=True)


class Skill(Base, TimestampMixin):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    target_role: Mapped[str] = mapped_column(String(150))
    current_skills: Mapped[str] = mapped_column(Text)
    analysis: Mapped[str] = mapped_column(Text)


class Roadmap(Base, TimestampMixin):
    __tablename__ = 'roadmaps'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    target_role: Mapped[str] = mapped_column(String(150))
    roadmap: Mapped[str] = mapped_column(Text)


class AIUsage(Base, TimestampMixin):
    __tablename__ = 'ai_usage'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    feature: Mapped[str] = mapped_column(String(100), index=True)
    provider: Mapped[str] = mapped_column(String(50))
    meta: Mapped[str | None] = mapped_column('metadata', Text, nullable=True)


class Setting(Base, TimestampMixin):
    __tablename__ = 'settings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    theme: Mapped[str] = mapped_column(String(20), default='light')


Index('ix_job_user_status', JobApplication.user_id, JobApplication.status)
