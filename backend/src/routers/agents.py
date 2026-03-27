from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Agent, Task, TaskStatus
from src.schemas import AgentCreate, AgentUpdate, AgentResponse, AgentStats

router = APIRouter(prefix="/agents")


@router.get("", response_model=list[AgentResponse])
async def list_agents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """获取智能体列表"""
    result = await db.execute(
        select(Agent)
        .where(Agent.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    agents = result.scalars().all()
    return agents


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建新智能体"""
    # 检查名称是否已存在
    result = await db.execute(
        select(Agent).where(Agent.name == agent_data.name)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Agent with name '{agent_data.name}' already exists"
        )
    
    # 生成 API Key
    api_key = f"atm_{uuid4().hex}"
    
    agent = Agent(
        name=agent_data.name,
        description=agent_data.description,
        avatar_url=agent_data.avatar_url,
        api_key=api_key,
        is_active=agent_data.is_active
    )
    
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """获取智能体详情"""
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id)
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    agent_data: AgentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新智能体"""
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id)
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # 更新字段
    update_data = agent_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    await db.commit()
    await db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """删除智能体 (软删除)"""
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id)
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    agent.is_active = False
    await db.commit()
    return None


@router.get("/{agent_id}/stats", response_model=AgentStats)
async def get_agent_stats(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """获取智能体统计信息"""
    # 检查智能体是否存在
    result = await db.execute(
        select(Agent).where(Agent.id == agent_id)
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # 统计任务
    result = await db.execute(
        select(
            func.count(Task.id).label("total"),
            func.sum(func.case((Task.status == TaskStatus.TODO, 1), else_=0)).label("todo"),
            func.sum(func.case((Task.status == TaskStatus.ONGOING, 1), else_=0)).label("ongoing"),
            func.sum(func.case((Task.status == TaskStatus.DONE, 1), else_=0)).label("done"),
            func.coalesce(func.sum(Task.tokens_consumed), 0).label("tokens")
        ).where(Task.agent_id == agent_id)
    )
    stats = result.one()
    
    return AgentStats(
        total_tasks=stats.total or 0,
        todo_count=stats.todo or 0,
        ongoing_count=stats.ongoing or 0,
        done_count=stats.done or 0,
        total_tokens_consumed=stats.tokens or 0
    )
