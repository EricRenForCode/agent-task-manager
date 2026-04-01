from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.task import TaskStatus


# ==================== Task Schemas ====================

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    task_date: date
    tokens_consumed: int = Field(default=0, ge=0)


class TaskCreate(TaskBase):
    agent_id: UUID

    def model_post_init(self, __context: any) -> None:
        object.__setattr__(self, 'original_date', self.task_date)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    task_date: Optional[date] = None
    tokens_consumed: Optional[int] = Field(None, ge=0)


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(TaskBase):
    id: UUID
    agent_id: UUID
    original_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskWithAgent(TaskResponse):
    agent_name: str
    
    class Config:
        from_attributes = True
