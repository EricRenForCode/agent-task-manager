import asyncio
from datetime import date, datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import get_settings
from src.database import async_engine, Base, AsyncSessionLocal
from src.routers import agents, tasks, calendar, heartbeat

settings = get_settings()


async def carry_over_tasks():
    """将所有未完成任务的 task_date 更新为今天"""
    from sqlalchemy import and_
    from src.models.task import Task, TaskStatus

    async with AsyncSessionLocal() as db:
        today = date.today()
        await db.execute(
            Task.__table__.update()
            .where(
                and_(
                    Task.task_date < today,
                    Task.status.in_([TaskStatus.TODO, TaskStatus.ONGOING])
                )
            )
            .values(task_date=today)
        )
        await db.commit()


async def daily_carryover_loop():
    """在每天午夜执行一次任务滚动"""
    while True:
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        await asyncio.sleep((next_midnight - now).total_seconds())
        await carry_over_tasks()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建表 (开发环境)
    if settings.DEBUG:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    # 启动时立即执行一次滚动，补齐遗漏的天
    await carry_over_tasks()
    # 启动每日定时任务
    carryover_task = asyncio.create_task(daily_carryover_loop())
    yield
    # 关闭时清理
    carryover_task.cancel()
    await async_engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="智能体每日任务管理系统 API",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(agents.router, prefix="/api/v1", tags=["agents"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
app.include_router(calendar.router, prefix="/api/v1", tags=["calendar"])
app.include_router(heartbeat.router, prefix="/api/v1", tags=["heartbeat"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
