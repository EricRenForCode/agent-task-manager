from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Task, TaskStatus
from src.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate, TaskWithAgent

router = APIRouter(prefix="/tasks")


@router.get("", response_model=list[TaskWithAgent])
async def list_tasks(
    date: Optional[date] = Query(None, description="Filter by date (YYYY-MM-DD)"),
    agent_id: Optional[UUID] = Query(None, description="Filter by agent ID"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """获取任务列表，支持多种过滤条件"""
    query = select(Task).join(Task.agent)
    
    # 应用过滤条件
    filters = []
    if date:
        filters.append(Task.task_date == date)
    if agent_id:
        filters.append(Task.agent_id == agent_id)
    if status:
        filters.append(Task.status == status)
    
    if filters:
        query = query.where(and_(*filters))
    
    query = query.order_by(Task.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    # 转换为包含 agent_name 的响应
    return [
        TaskWithAgent(
            **task.__dict__,
            agent_name=task.agent.name
        )
        for task in tasks
    ]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建新任务"""
    from src.models import Agent
    
    # 检查智能体是否存在
    result = await db.execute(
        select(Agent).where(Agent.id == task_data.agent_id)
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agent not found"
        )
    
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        agent_id=task_data.agent_id,
        task_date=task_data.task_date,
        tokens_consumed=task_data.tokens_consumed
    )
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskWithAgent)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """获取任务详情"""
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskWithAgent(
        **task.__dict__,
        agent_name=task.agent.name
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新任务"""
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # 更新字段
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    await db.commit()
    await db.refresh(task)
    return task


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: UUID,
    status_update: TaskStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新任务状态"""
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    task.status = status_update.status
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """删除任务"""
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    await db.delete(task)
    await db.commit()
    return None
