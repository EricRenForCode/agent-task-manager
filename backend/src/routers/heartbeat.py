from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.config import get_settings
from src.models import Agent, Task, TaskStatus, HeartbeatLog
from src.schemas import HeartbeatRequest, HeartbeatResponse

router = APIRouter(prefix="/heartbeat")
settings = get_settings()


async def verify_agent_key(
    agent_name: str,
    agent_key: str,
    db: AsyncSession
) -> Optional[Agent]:
    """验证智能体 API Key"""
    result = await db.execute(
        select(Agent).where(
            and_(
                Agent.name == agent_name,
                Agent.api_key == agent_key,
                Agent.is_active == True
            )
        )
    )
    return result.scalar_one_or_none()


@router.post("", response_model=HeartbeatResponse)
async def receive_heartbeat(
    heartbeat: HeartbeatRequest,
    db: AsyncSession = Depends(get_db)
):
    """接收智能体心跳上报"""
    from sqlalchemy import and_
    
    # 验证智能体
    agent = await verify_agent_key(
        heartbeat.agent_name,
        heartbeat.agent_key,
        db
    )
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid agent name or key"
        )
    
    tasks_synced = 0
    
    # 处理任务更新
    if heartbeat.tasks:
        # 标记完成的任务
        if heartbeat.tasks.completed:
            for task_id in heartbeat.tasks.completed:
                result = await db.execute(
                    select(Task).where(
                        and_(
                            Task.id == task_id,
                            Task.agent_id == agent.id
                        )
                    )
                )
                task = result.scalar_one_or_none()
                if task:
                    task.status = TaskStatus.DONE
                    tasks_synced += 1
        
        # 标记进行中的任务
        if heartbeat.tasks.in_progress:
            for task_id in heartbeat.tasks.in_progress:
                result = await db.execute(
                    select(Task).where(
                        and_(
                            Task.id == task_id,
                            Task.agent_id == agent.id
                        )
                    )
                )
                task = result.scalar_one_or_none()
                if task:
                    task.status = TaskStatus.ONGOING
                    tasks_synced += 1
        
        # 创建新任务
        if heartbeat.tasks.new:
            from datetime import date as date_module
            today = date_module.today()
            
            for task_info in heartbeat.tasks.new:
                task = Task(
                    title=task_info.title,
                    description=task_info.description,
                    status=task_info.status,
                    agent_id=agent.id,
                    task_date=task_info.task_date or today,
                    tokens_consumed=task_info.tokens_consumed
                )
                db.add(task)
                tasks_synced += 1
    
    # 记录心跳日志
    heartbeat_log = HeartbeatLog(
        agent_id=agent.id,
        status=heartbeat.status,
        metadata=heartbeat.metadata
    )
    db.add(heartbeat_log)
    
    await db.commit()
    
    return HeartbeatResponse(
        success=True,
        server_time=datetime.utcnow(),
        tasks_synced=tasks_synced,
        message=f"Heartbeat received from {agent.name}"
    )
