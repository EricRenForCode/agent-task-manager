from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ==================== Agent Schemas ====================

class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None


class AgentResponse(AgentBase):
    id: UUID
    api_key: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AgentStats(BaseModel):
    total_tasks: int
    todo_count: int
    ongoing_count: int
    done_count: int
    total_tokens_consumed: int
