from datetime import datetime

import os

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pgvector.sqlalchemy import Vector

# ===========================
# Database Configuration
# ===========================

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


# ===========================
# Users
# ===========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    password_hash = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    projects = relationship(
        "Project",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    sessions = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ===========================
# Login Sessions
# ===========================

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    jwt_token = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    expires_at = Column(DateTime)

    user = relationship("User", back_populates="sessions")


# ===========================
# Projects
# ===========================

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String(255), nullable=False)

    description = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="projects")

    conversations = relationship(
        "Conversation",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    goals = relationship(
        "Goal",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    decisions = relationship(
        "Decision",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    reports = relationship(
        "WeeklyReport",
        back_populates="project",
        cascade="all, delete-orphan"
    )


# ===========================
# Conversations
# ===========================

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    title = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship(
        "Project",
        back_populates="conversations"
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


# ===========================
# Messages
# ===========================

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id")
    )

    sender = Column(String(20))      # user / assistant

    content = Column(Text)

    # Semantic Search
    embedding = Column(Vector(1536))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )


# ===========================
# Decisions
# ===========================

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    title = Column(String(255))

    description = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship(
        "Project",
        back_populates="decisions"
    )


# ===========================
# Goals
# ===========================

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    title = Column(String(255))

    description = Column(Text)

    status = Column(String(50), default="pending")

    deadline = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship(
        "Project",
        back_populates="goals"
    )


# ===========================
# Tasks
# ===========================

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    title = Column(String(255))

    description = Column(Text)

    priority = Column(String(20))

    status = Column(String(20), default="pending")

    deadline = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship(
        "Project",
        back_populates="tasks"
    )


# ===========================
# Weekly Reports
# ===========================

class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    execution_score = Column(Integer)

    reflection = Column(Text)

    behavior_pattern = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship(
        "Project",
        back_populates="reports"
    )


# ===========================
# Create Tables
# ===========================

Base.metadata.create_all(engine)