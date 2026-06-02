from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # 数据库
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/agent_tasks"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # 安全
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    API_KEY_HEADER: str = "X-Agent-Key"
    
    # 应用
    DEBUG: bool = True
    APP_NAME: str = "Agent Task Manager"
    APP_VERSION: str = "0.1.0"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
