# Agent Task Manager - Backend Service Design

## 项目概述
智能体每日任务管理系统后端服务，用于监控 OpenClaw 各智能体的任务状态和 token 消耗。

## 技术栈
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **Cache**: Redis (可选，用于实时状态)
- **ORM**: SQLAlchemy 2.0 + Alembic
- **Validation**: Pydantic v2
- **Deployment**: Docker + Docker Compose

## 项目结构

```
agent-task-manager/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic.ini
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── task.py
│   │   └── heartbeat.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── task.py
│   │   └── heartbeat.py
│   ├── routers/                # API routes
│   │   ├── __init__.py
│   │   ├── agents.py
│   │   ├── tasks.py
│   │   ├── calendar.py
│   │   └── heartbeat.py
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── agent_service.py
│   │   ├── task_service.py
│   │   └── heartbeat_service.py
│   └── utils/
│       └── __init__.py
├── migrations/                 # Alembic migrations
└── tests/
    └── __init__.py
```

## 数据库模型

### Agent (智能体)
```python
class Agent(Base):
    __tablename__ = "agents"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # Relationships
    tasks: Mapped[list["Task"]] = relationship(back_populates="agent")
    heartbeats: Mapped[list["HeartbeatLog"]] = relationship(back_populates="agent")
```

### Task (任务)
```python
class TaskStatus(str, Enum):
    TODO = "todo"
    ONGOING = "ongoing"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        default=TaskStatus.TODO,
        index=True
    )
    
    # 关联
    agent_id: Mapped[UUID] = mapped_column(
        ForeignKey("agents.id"),
        index=True
    )
    
    # 日期相关
    task_date: Mapped[date] = mapped_column(index=True)
    
    # Token 消耗
    tokens_consumed: Mapped[int] = mapped_column(default=0)
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    # Relationships
    agent: Mapped["Agent"] = relationship(back_populates="tasks")
```

### HeartbeatLog (心跳日志)
```python
class HeartbeatLog(Base):
    __tablename__ = "heartbeat_logs"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    agent_id: Mapped[UUID] = mapped_column(ForeignKey("agents.id"), index=True)
    
    # 心跳数据
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    status: Mapped[str] = mapped_column(String(50))  # online, busy, idle, error
    
    # 元数据 (JSON)
    metadata: Mapped[dict | None] = mapped_column(JSON)
    # 例如: {"tasks_completed": 5, "current_task": "...", "memory_usage": "..."}
    
    # Relationships
    agent: Mapped["Agent"] = relationship(back_populates="heartbeats")
```

## API 端点设计

### 1. 智能体管理 (/api/v1/agents)

```yaml
GET    /agents              # 列出所有智能体
POST   /agents              # 创建智能体
GET    /agents/{id}         # 获取智能体详情
PUT    /agents/{id}         # 更新智能体
DELETE /agents/{id}         # 删除智能体
GET    /agents/{id}/stats   # 获取智能体统计 (token消耗等)
```

### 2. 任务管理 (/api/v1/tasks)

```yaml
GET    /tasks                    # 列出任务 (支持过滤)
POST   /tasks                    # 创建任务
GET    /tasks/{id}               # 获取任务详情
PUT    /tasks/{id}               # 更新任务
DELETE /tasks/{id}               # 删除任务
PATCH  /tasks/{id}/status        # 更新任务状态

# 查询参数
GET /tasks?date=2024-03-26       # 按日期筛选
GET /tasks?agent_id=xxx          # 按智能体筛选
GET /tasks?status=ongoing        # 按状态筛选
GET /tasks?start_date=...&end_date=...  # 日期范围
```

### 3. 日历视图 (/api/v1/calendar)

```yaml
GET /calendar/monthly?year=2024&month=3
# 返回某月的所有日期及其任务统计

Response:
{
  "year": 2024,
  "month": 3,
  "days": [
    {
      "date": "2024-03-01",
      "has_tasks": true,
      "task_count": {
        "todo": 2,
        "ongoing": 1,
        "done": 3
      },
      "total_tokens": 1500
    }
  ]
}

GET /calendar/daily?date=2024-03-26
# 返回某天的详细任务列表

Response:
{
  "date": "2024-03-26",
  "tasks": {
    "todo": [...],
    "ongoing": [...],
    "done": [...]
  },
  "summary": {
    "total_tasks": 10,
    "total_tokens": 2500,
    "agents_involved": ["agent1", "agent2"]
  }
}
```

### 4. 心跳上报 (/api/v1/heartbeat)

```yaml
POST /heartbeat
# 智能体通过 heartbeat 上报状态

Request Body:
{
  "agent_name": "my-agent",      # 或 agent_id
  "agent_key": "secret-key",     # 认证密钥
  "status": "online",            # online, busy, idle, error
  "tasks": {
    "completed": ["task-id-1"],
    "in_progress": ["task-id-2"],
    "new": [
      {
        "title": "新任务",
        "description": "任务描述",
        "status": "todo"
      }
    ]
  },
  "tokens_consumed": 500,
  "metadata": {
    "memory_usage": "...",
    "current_operation": "..."
  }
}

Response:
{
  "success": true,
  "server_time": "2024-03-26T10:00:00Z",
  "tasks_synced": 3
}
```

### 5. 统计与报表 (/api/v1/stats)

```yaml
GET /stats/overview              # 总体统计
GET /stats/agents                # 各智能体统计
GET /stats/daily?start=...&end=...  # 每日统计
GET /stats/tokens?agent_id=...   # Token 消耗统计
```

## 认证方案

### 方案1: API Key (推荐用于 Agent Heartbeat)
```python
# 每个智能体有唯一的 API Key
# Header: X-Agent-Key: <secret-key>
```

### 方案2: JWT (用于 Web UI 用户)
```python
# 管理员登录后获得 JWT
# Header: Authorization: Bearer <token>
```

## Docker Compose 配置

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agent_tasks
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./src:/app/src
    command: uvicorn src.main:app --host 0.0.0.0 --reload

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=agent_tasks
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## OpenClaw 集成方案

### 智能体 Heartbeat 配置

在 OpenClaw 的 `HEARTBEAT.md` 中添加:

```markdown
## Agent Task Manager Integration

### 每日状态上报
每天检查任务状态并上报到 Agent Task Manager:

```python
# 在 heartbeat 中调用
import requests

def report_to_task_manager():
    response = requests.post(
        "http://localhost:8000/api/v1/heartbeat",
        json={
            "agent_name": "my-agent",
            "agent_key": "${AGENT_KEY}",
            "status": "online",
            "tasks": get_current_tasks(),
            "tokens_consumed": get_token_usage()
        }
    )
    return response.json()
```
```

### Cron Job 配置

```json
{
  "name": "agent-status-report",
  "schedule": {"kind": "every", "everyMs": 3600000},
  "payload": {
    "kind": "agentTurn",
    "message": "Report current task status to Agent Task Manager API"
  }
}
```

## 下一步

1. 初始化项目结构和依赖
2. 创建数据库模型和迁移
3. 实现核心 API 端点
4. 添加认证和权限
5. 编写测试
6. 配置 Docker 部署
