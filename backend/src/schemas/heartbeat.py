from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic import BaseModel, Field

from src.schemas.task import TaskStatus


# ==================== Heartbeat Schemas ====================

class HeartbeatTaskInfo(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus
    task_date: Optional[str] = None  # ISO date string
    tokens_consumed: int = 0


class HeartbeatTasksUpdate(BaseModel):
    completed: Optional[List[str]] = None  # task IDs
    in_progress: Optional[List[str]] = None  # task IDs
    new: Optional[List[HeartbeatTaskInfo]] = None


class HeartbeatRequest(BaseModel):
    agent_name: str
    agent_key: str
    status: str = Field(..., description="online, busy, idle, error")
    tasks: Optional[HeartbeatTasksUpdate] = None
    tokens_consumed: int = Field(default=0, ge=0)
    metadata: Optional[Dict[str, Any]] = None


class HeartbeatResponse(BaseModel):
    success: bool
    server_time: datetime
    tasks_synced: int
    message: Optional[str] = None


class HeartbeatLogResponse(BaseModel):
    id: UUID
    agent_id: UUID
    timestamp: datetime
    status: str
    metadata: Optional[dict]
    
    class Config:
        from_attributes = True
