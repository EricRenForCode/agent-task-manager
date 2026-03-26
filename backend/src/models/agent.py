from datetime import datetime, date
from enum import Enum as PyEnum
from typing import Optional, List, TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import String, Text, DateTime, Date, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base

if TYPE_CHECKING:
    from src.models.task import Task
    from src.models.heartbeat import HeartbeatLog


class Agent(Base):
    __tablename__ = "agents"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    api_key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    tasks: Mapped[List["Task"]] = relationship(back_populates="agent", lazy="selectin")
    heartbeats: Mapped[List["HeartbeatLog"]] = relationship(back_populates="agent", lazy="selectin")
