from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base

if TYPE_CHECKING:
    from src.models.agent import Agent


class HeartbeatLog(Base):
    __tablename__ = "heartbeat_logs"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    agent_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("agents.id"),
        index=True
    )
    
    # 心跳数据
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    status: Mapped[str] = mapped_column(String(50))  # online, busy, idle, error
    
    # 元数据
    meta_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    agent: Mapped["Agent"] = relationship(back_populates="heartbeats")
