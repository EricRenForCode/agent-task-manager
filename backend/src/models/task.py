from datetime import datetime, date
from enum import Enum as PyEnum
from typing import Optional, TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import String, Text, DateTime, Date, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base

if TYPE_CHECKING:
    from src.models.agent import Agent


class TaskStatus(str, PyEnum):
    TODO = "todo"
    ONGOING = "ongoing"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.TODO,
        index=True
    )
    
    # 关联
    agent_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agents.id"),
        index=True
    )
    
    # 日期
    task_date: Mapped[date] = mapped_column(Date, index=True)
    
    # Token 消耗
    tokens_consumed: Mapped[int] = mapped_column(Integer, default=0)
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    agent: Mapped["Agent"] = relationship(back_populates="tasks")
