import asyncio
from datetime import date, datetime, timedelta

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import get_settings
from src.database import async_engine, Base, AsyncSessionLocal
from src.routers import agents, tasks, calendar, heartbeat
from src.auth.router import router as auth_router
from src.auth.service import get_current_user
from src.auth.models import User

settings = get_settings()


async def carry_over_tasks():
    from sqlalchemy import and_
    from src.models.task import Task, TaskStatus
    async with AsyncSessionLocal() as db:
        today = date.today()
        await db.execute(
            Task.__table__.update()
            .where(and_(
                Task.task_date < today,
                Task.status.in_([TaskStatus.TODO, TaskStatus.ONGOING])
            ))
            .values(task_date=today)
        )
        await db.commit()


async def seed_default_user():
    from sqlalchemy import select, func
    from src.auth.models import User
    from src.auth.service import hash_password
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(func.count(User.id)))
        if result.scalar() == 0:
            db.add(User(username="admin", hashed_password=hash_password("admin123"), is_active=True, is_superuser=True))
            await db.commit()


async def daily_carryover_loop():
    while True:
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        await asyncio.sleep((next_midnight - now).total_seconds())
        await carry_over_tasks()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.DEBUG:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    await carry_over_tasks()
    await seed_default_user()
    carryover_task = asyncio.create_task(daily_carryover_loop())
    yield
    carryover_task.cancel()
    await async_engine.dispose()


app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION,
    description="智能体每日任务管理系统 API", lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(agents.router, prefix="/api/v1", tags=["agents"])
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])
app.include_router(calendar.router, prefix="/api/v1", tags=["calendar"])
app.include_router(heartbeat.router, prefix="/api/v1", tags=["heartbeat"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/api/v1/protected-test")
async def protected_test(current_user: User = Depends(get_current_user)):
    return {"message": "You are authenticated", "user_id": str(current_user.id), "username": current_user.username}
