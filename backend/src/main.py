from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import get_settings
from src.database import async_engine, Base
from src.routers import agents, tasks, calendar, heartbeat

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建表 (开发环境)
    if settings.DEBUG:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭时清理
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
