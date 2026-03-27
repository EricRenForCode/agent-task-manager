# Agent Task Manager Backend

智能体每日任务管理系统后端服务

## 快速开始

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 访问 API 文档
open http://localhost:8000/docs
```

## API 端点

- `GET /api/v1/agents` - 智能体列表
- `GET /api/v1/tasks` - 任务列表
- `GET /api/v1/calendar/monthly` - 月度日历
- `POST /api/v1/heartbeat` - 智能体心跳上报

## 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行迁移
alembic upgrade head

# 启动开发服务器
uvicorn src.main:app --reload
```
