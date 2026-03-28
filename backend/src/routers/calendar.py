from datetime import date, timedelta
from calendar import monthrange

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import Task, TaskStatus, Agent
from src.schemas import MonthlyCalendarResponse, DailyCalendarResponse, MonthlyDayInfo, DayTaskCount, DailyTaskSummary

router = APIRouter(prefix="/calendar")


@router.get("/monthly", response_model=MonthlyCalendarResponse)
async def get_monthly_calendar(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db)
):
    """获取月度日历数据"""
    # 计算月份的起止日期
    _, last_day = monthrange(year, month)
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)
    
    # 查询该月所有任务
    result = await db.execute(
        select(
            Task.task_date,
            Task.status,
            func.count(Task.id).label("count"),
            func.coalesce(func.sum(Task.tokens_consumed), 0).label("tokens")
        )
        .where(
            and_(
                Task.task_date >= start_date,
                Task.task_date <= end_date
            )
        )
        .group_by(Task.task_date, Task.status)
    )
    
    # 整理数据
    task_data = {}
    for row in result.all():
        task_date = row.task_date
        if task_date not in task_data:
            task_data[task_date] = {
                "todo": 0,
                "ongoing": 0,
                "done": 0,
                "tokens": 0
            }
        task_data[task_date][row.status.value] = row.count
        task_data[task_date]["tokens"] += row.tokens
    
    # 构建每日数据
    days = []
    current_date = start_date
    while current_date <= end_date:
        day_info = task_data.get(current_date, {
            "todo": 0,
            "ongoing": 0,
            "done": 0,
            "tokens": 0
        })
        
        days.append(MonthlyDayInfo(
            date=current_date,
            has_tasks=sum([day_info["todo"], day_info["ongoing"], day_info["done"]]) > 0,
            task_count=DayTaskCount(
                todo=day_info["todo"],
                ongoing=day_info["ongoing"],
                done=day_info["done"]
            ),
            total_tokens=day_info["tokens"]
        ))
        current_date += timedelta(days=1)
    
    return MonthlyCalendarResponse(
        year=year,
        month=month,
        days=days
    )


@router.get("/daily", response_model=DailyCalendarResponse)
async def get_daily_calendar(
    date: date = Query(..., description="Date (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db)
):
    """获取单日详细任务列表"""
    # 查询该日所有任务
    result = await db.execute(
        select(Task).options(joinedload(Task.agent))
        .where(Task.task_date == date)
        .order_by(Task.created_at.desc())
    )
    
    # 按状态分组
    tasks_by_status = {
        "todo": [],
        "ongoing": [],
        "done": []
    }
    
    total_tokens = 0
    agents_involved = set()
    
    for task in result.scalars().all():
        agent_name = task.agent.name

        task_dict = {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "agent_name": agent_name,
            "tokens_consumed": task.tokens_consumed,
            "task_date": task.task_date.isoformat(),
            "original_date": task.original_date.isoformat(),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

        tasks_by_status[task.status.value].append(task_dict)
        total_tokens += task.tokens_consumed
        agents_involved.add(agent_name)
    
    return DailyCalendarResponse(
        date=date,
        tasks=tasks_by_status,
        summary=DailyTaskSummary(
            total_tasks=sum(len(tasks) for tasks in tasks_by_status.values()),
            total_tokens=total_tokens,
            agents_involved=list(agents_involved)
        )
    )
