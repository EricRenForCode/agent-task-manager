from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import get_settings

settings = get_settings()

# 同步引擎 (用于 Alembic)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 异步引擎 (用于应用)
# 转换 postgresql:// 为 postgresql+asyncpg://
async_database_url = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)
async_engine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
)
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# 依赖注入用
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
